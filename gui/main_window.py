"""
Main application window
"""

import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime

from settings import VIRUSTOTAL_API_KEYS
from components.virustotal import VirusTotalAnalyzer
from components.geolocator import GeoLocator
from components.blocking_manager import BlockingManager
from components.risk_scoring import RiskScoringEngine
from components.map_visualizer import MapVisualizer
from components.network_monitor import NetworkMonitor

from gui.widgets.stats_bar import StatsBar
from gui.widgets.console import ConsoleWidget
from gui.tabs.traffic_analytics import TrafficAnalyticsTab
from gui.tabs.blocking_controls import BlockingControlsTab
from gui.tabs.home_tab import HomeTab
from gui.tabs.blocked_items import BlockedItemsTab
from gui.tabs.advanced_controls import AdvancedControlsTab

class SimpleNetworkGuard:
    def __init__(self):
        # Initialize components
        self.vt_analyzer = VirusTotalAnalyzer(VIRUSTOTAL_API_KEYS)
        self.geo_locator = GeoLocator()
        self.blocking_manager = BlockingManager()
        self.risk_engine = RiskScoringEngine(self.blocking_manager)
        self.map_viz = MapVisualizer()
        
        self.monitor = NetworkMonitor(
            self.vt_analyzer, self.geo_locator,
            self.risk_engine, self.map_viz,
            self.blocking_manager
        )
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("🌍 Network Guard - Malware Blocker")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a1a")
        
        # Setup GUI with bottom tabs
        self.setup_gui()
        
        # Start monitoring - pass GUI callback
        self.monitor.set_alert_callback(self.handle_alert)
        self.monitor.set_gui_callback(self.update_console)
        self.monitor.root = self.root  # Give monitor access to root for after()
        
        # Create and start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor.monitor_connections, daemon=True)
        self.monitor_thread.start()
        
        # Start statistics update
        self.root.after(1000, self.update_statistics)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        self.monitor.stop()
        self.root.destroy()
    
    def setup_gui(self):
        """Setup the main GUI layout with bottom tabs"""
        # Main container with 3 sections
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top section: Stats bar
        self.stats_bar = StatsBar(main_frame)
        self.stats_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Middle section: Map and Console
        middle_frame = tk.Frame(main_frame, bg="#1a1a1a")
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Left: Map (50%)
        map_frame = tk.LabelFrame(middle_frame, text="🌍 Live Map", 
                                 bg="#2d3436", fg="white", font=("Arial", 10, "bold"))
        map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.map_widget = self.map_viz.create_map(map_frame)
        
        # Right: Console (50%)
        console_frame = tk.LabelFrame(middle_frame, text="📋 Live Monitor", 
                                     bg="#2d3436", fg="white", font=("Arial", 10, "bold"))
        console_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.console = ConsoleWidget(console_frame, self)
        
        # Bottom section: Tabbed interface
        bottom_frame = tk.Frame(main_frame, bg="#1a1a1a")
        bottom_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 0))
        
        # Create notebook for bottom tabs
        self.bottom_notebook = ttk.Notebook(bottom_frame, height=250)
        self.bottom_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration for tabs
        self.configure_tab_style()
        
        # Add tabs
        self.traffic_tab = TrafficAnalyticsTab(self.bottom_notebook, self)
        self.blocking_tab = BlockingControlsTab(self.bottom_notebook, self)
        self.home_tab = HomeTab(self.bottom_notebook, self)
        self.blocked_tab = BlockedItemsTab(self.bottom_notebook, self)
        self.advanced_tab = AdvancedControlsTab(self.bottom_notebook, self)
    
    def configure_tab_style(self):
        """Configure tab styles"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2d3436', borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#404040', 
                       foreground='white',
                       padding=[10, 2],
                       font=('Arial', 9))
        style.map('TNotebook.Tab', 
                 background=[('selected', '#0984e3'), ('active', '#404040')],
                 foreground=[('selected', 'white'), ('active', 'white')])
    
    def handle_alert(self, alert):
        """Handle incoming alerts"""
        time_str = datetime.now().strftime("%H:%M:%S")
        
        alert_text = (
            f"[{time_str}] ⚠️ ALERT: {alert['process'][:15]} → {alert['remote_ip']}:{alert['port']}\n"
            f"   Risk: {alert['ip_risk']:.1f} | {alert['country']} | "
            f"VT: {alert['vt_malicious']}⚠️\n"
            f"{'─'*50}\n"
        )
        
        self.update_console(alert_text, "alert")
    
    def update_console(self, text, tag="info"):
        """Update console with new text"""
        self.console.insert(text, tag)
        
        # Also update activity text if available
        if hasattr(self, 'activity_text'):
            self.activity_text.config(state=tk.NORMAL)
            self.activity_text.insert(tk.END, text)
            self.activity_text.see(tk.END)
            self.activity_text.config(state=tk.DISABLED)
    
    def update_statistics(self):
        """Update statistics display"""
        try:
            stats = self.monitor.get_traffic_stats()
            
            # Update stats bar
            self.stats_bar.update_stats(
                connections=stats['total_connections'],
                active=len(self.monitor.active_connections),
                threats=sum(1 for ip in self.risk_engine.ip_scores.values() if ip['score'] > 3),
                vt_requests=self.vt_analyzer.request_count,
                ips=stats['unique_ips'],
                processes=stats['unique_processes']
            )
            
            # Update scan status
            status = "🟢 Scanning" if self.monitor.running else "🔴 Stopped"
            self.stats_bar.update_scan_status(status)
            
        except Exception as e:
            print(f"Stats update error: {e}")
        
        # Continue updating statistics every second
        self.root.after(1000, self.update_statistics)