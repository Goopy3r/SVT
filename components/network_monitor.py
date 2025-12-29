"""
Network connection monitoring
"""

import time
import threading
from datetime import datetime
from collections import defaultdict, deque
from typing import Dict, List, Set, Any, Optional, Callable
import psutil

from components.virustotal import VirusTotalAnalyzer
from components.geolocator import GeoLocator
from components.risk_scoring import RiskScoringEngine
from components.map_visualizer import MapVisualizer
from components.blocking_manager import BlockingManager

class NetworkMonitor:
    def __init__(self, vt_analyzer: VirusTotalAnalyzer, geo_locator: GeoLocator,
                 risk_engine: RiskScoringEngine, map_viz: MapVisualizer, 
                 blocking_manager: BlockingManager):
        self.vt_analyzer = vt_analyzer
        self.geo_locator = geo_locator
        self.risk_engine = risk_engine
        self.map_viz = map_viz
        self.blocking_manager = blocking_manager
        
        self.connections_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.active_connections: Set[str] = set()
        self.alert_callback: Optional[Callable] = None
        self.gui_callback: Optional[Callable] = None
        
        self.traffic_by_ip: Dict[str, Dict[str, int]] = defaultdict(lambda: {'in': 0, 'out': 0, 'total': 0})
        self.traffic_by_process: Dict[str, Dict[str, int]] = defaultdict(lambda: {'in': 0, 'out': 0, 'total': 0})
        self.connection_count = 0
        self.running = True
        self.autoblock_enabled = True
        
        # Add reference to root window for GUI updates
        self.root = None
    
    def set_alert_callback(self, callback: Callable):
        """Set callback for alerts"""
        self.alert_callback = callback
    
    def set_gui_callback(self, callback: Callable):
        """Set callback for GUI updates"""
        self.gui_callback = callback
    
    def stop(self):
        """Stop the monitor"""
        self.running = False
    
    def monitor_connections(self):
        """Monitor network connections continuously"""
        if self.gui_callback:
            self.root.after(0, self.gui_callback, "🔍 Network monitor started\n", "info")
            self.root.after(0, self.gui_callback, 
                           f"🚫 Blocking {len(self.blocking_manager.blocked_processes)} processes "
                           f"and {len(self.blocking_manager.blocked_ips)} IPs\n", "info")
        
        while self.running:
            try:
                # Get all current connections
                connections = psutil.net_connections(kind='inet')
                current_time = time.time()
                new_connections = 0
                blocked_count = 0
                
                # Create a set of current connection IDs
                current_connection_ids = set()
                
                for conn in connections:
                    try:
                        if not conn.pid or not conn.raddr:
                            continue
                        
                        # Skip loopback and local addresses
                        if conn.raddr.ip in ['127.0.0.1', '::1', '0.0.0.0']:
                            continue
                        
                        # Skip if port is 0
                        if conn.raddr.port == 0:
                            continue
                        
                        # Get process info
                        try:
                            process = psutil.Process(conn.pid)
                            proc_name = process.name()
                            proc_exe = process.exe()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            proc_name = "unknown"
                            proc_exe = ""
                        
                        # Check if process is blocked
                        if self.blocking_manager.is_process_blocked(proc_name):
                            blocked_count += 1
                            self.blocking_manager.kill_process(conn.pid)
                            continue
                        
                        # Check if IP is blocked
                        if self.blocking_manager.is_ip_blocked(conn.raddr.ip):
                            blocked_count += 1
                            continue
                        
                        conn_id = f"{conn.pid}:{proc_name}:{conn.raddr.ip}:{conn.raddr.port}"
                        current_connection_ids.add(conn_id)
                        
                        if conn_id not in self.active_connections:
                            # New connection found
                            self.active_connections.add(conn_id)
                            self.process_new_connection(conn, proc_name, proc_exe, current_time)
                            new_connections += 1
                            
                    except Exception as e:
                        if self.gui_callback:
                            self.root.after(0, self.gui_callback, f"Error: {e}\n", "error")
                        continue
                
                # Remove connections that are no longer active
                expired_connections = self.active_connections - current_connection_ids
                self.active_connections = self.active_connections - expired_connections
                
                # Clean up old connections from history
                self.cleanup_old_connections()
                
                # Log scan results
                if self.gui_callback:
                    if new_connections > 0:
                        self.root.after(0, self.gui_callback, 
                                       f"📡 Scan: Found {new_connections} new connections\n", "info")
                    if blocked_count > 0:
                        self.root.after(0, self.gui_callback, 
                                       f"🚫 Blocked {blocked_count} connections\n", "alert")
                
            except Exception as e:
                if self.gui_callback:
                    self.root.after(0, self.gui_callback, f"Monitor error: {e}\n", "error")
            
            # Wait before next scan
            time.sleep(1)  # Scan every second
    
    def process_new_connection(self, conn: Any, proc_name: str, proc_exe: str, timestamp: float):
        """Process a new network connection"""
        try:
            rip = conn.raddr.ip
            rport = conn.raddr.port
            
            # Get geolocation
            geo = self.geo_locator.get_location(rip)
            
            # Get VirusTotal data
            vt_data = {'malicious': 0, 'suspicious': 0, 'harmless': 0, 
                      'undetected': 0, 'as_owner': 'Unknown'}
            
            # Calculate risk scores
            ip_risk = self.risk_engine.calculate_ip_risk(rip, {
                'vt_malicious': vt_data['malicious'],
                'vt_suspicious': vt_data['suspicious'],
                'port': rport,
                'country': geo['country']
            })
            
            # Auto-block if risk is critical
            if self.autoblock_enabled and ip_risk >= 8.0:
                self.blocking_manager.check_and_block_suspicious(proc_name, conn.pid, rip, ip_risk)
                if self.gui_callback:
                    self.root.after(0, self.gui_callback, 
                                   f"🚫 AUTO-BLOCKED: {proc_name} → {rip} (Risk: {ip_risk:.1f})\n", "alert")
                return
            
            # Update map visualization
            if geo['lat'] != 0 and geo['lon'] != 0:
                self.map_viz.update_connection(geo['lat'], geo['lon'], ip_risk)
            
            # Send to GUI console
            if self.gui_callback:
                risk_level, risk_color = self.risk_engine.get_risk_level(ip_risk)
                
                # Format the message
                timestamp_str = datetime.now().strftime("%H:%M:%S")
                log_msg = (
                    f"[{timestamp_str}] {proc_name[:15]:<15} → {rip:<15}:{rport:<5} "
                    f"Risk: {risk_level} ({ip_risk:.1f}) "
                    f"{geo['country']}\n"
                )
                
                tag = "info" if risk_level == "LOW" else "warning" if risk_level == "MEDIUM" else "alert"
                self.root.after(0, self.gui_callback, log_msg, tag)
            
            # Store connection data
            conn_data = {
                'timestamp': timestamp,
                'process_name': proc_name,
                'process_exe': proc_exe,
                'process_pid': conn.pid,
                'remote_ip': rip,
                'remote_port': rport,
                'country': geo['country'],
                'country_name': geo['country_name'],
                'city': geo['city'],
                'lat': geo['lat'],
                'lon': geo['lon'],
                'vt_malicious': vt_data['malicious'],
                'vt_suspicious': vt_data['suspicious'],
                'as_owner': vt_data['as_owner']
            }
            
            # Store in history
            self.connections_history[proc_name].append(conn_data)
            
            # Update traffic stats
            self.traffic_by_ip[rip]['out'] += 1
            self.traffic_by_ip[rip]['total'] += 1
            self.traffic_by_process[proc_name]['out'] += 1
            self.traffic_by_process[proc_name]['total'] += 1
            self.connection_count += 1
            
            # Check for VirusTotal in background thread
            threading.Thread(target=self.check_virustotal_background, 
                           args=(rip, rport, proc_name, conn.pid), 
                           daemon=True).start()
            
        except Exception as e:
            if self.gui_callback:
                self.root.after(0, self.gui_callback, f"Process error: {e}\n", "error")
                
    def cleanup_old_connections(self):
        """Remove old connections from history"""
        current_time = time.time()
        cutoff = current_time - 300  # 5 minutes
        
        for proc_name in list(self.connections_history.keys()):
            self.connections_history[proc_name] = [
                conn for conn in self.connections_history[proc_name]
                if conn['timestamp'] > cutoff
            ]
            
            if not self.connections_history[proc_name]:
                del self.connections_history[proc_name]
    
    def get_traffic_stats(self) -> Dict[str, Any]:
        """Get traffic statistics"""
        return {
            'total_connections': self.connection_count,
            'unique_ips': len(self.traffic_by_ip),
            'unique_processes': len(self.traffic_by_process),
            'top_ips': sorted(self.traffic_by_ip.items(), 
                             key=lambda x: x[1]['total'], reverse=True)[:10],
            'top_processes': sorted(self.traffic_by_process.items(), 
                                   key=lambda x: x[1]['total'], reverse=True)[:10],
            'active_connections': len(self.active_connections)
        }
        
    def check_virustotal_background(self, ip: str, port: int, process_name: str, pid: int):
        """Check VirusTotal in background thread"""
        try:
            vt_data = self.vt_analyzer.check_ip(ip)
            
            # Update risk with VT data
            ip_risk = self.risk_engine.calculate_ip_risk(ip, {
                'vt_malicious': vt_data['malicious'],
                'vt_suspicious': vt_data['suspicious'],
                'port': port,
                'country': 'Unknown'
            })
            
            # Auto-block if malicious
            if self.autoblock_enabled and (vt_data['malicious'] > 2 or ip_risk >= 8.0):
                self.blocking_manager.block_process(process_name, pid)
                self.blocking_manager.block_ip(ip)
                
                if self.gui_callback:
                    timestamp_str = datetime.now().strftime("%H:%M:%S")
                    warning_msg = f"[{timestamp_str}] 🚫 VT AUTO-BLOCK: {process_name} → {ip} Malicious: {vt_data['malicious']}\n"
                    self.root.after(0, self.gui_callback, warning_msg, "alert")
                    
        except Exception as e:
            pass