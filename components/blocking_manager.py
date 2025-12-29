"""
Blocking manager for processes, IPs, and websites
"""

import json
import os
import platform
import subprocess
import time
from typing import Set, Dict, Any

import psutil
from settings import (
    BLOCKED_PROCESSES_FILE, 
    BLOCKED_IPS_FILE, 
    HOSTS_FILE,
    KNOWN_SAFE
)

class BlockingManager:
    def __init__(self):
        self.blocked_processes: Set[str] = set()
        self.blocked_ips: Set[str] = set()
        self.blocked_domains: Set[str] = set()
        self.load_blocked_items()
        
        # Store active process PIDs to kill
        self.active_processes: Dict[int, str] = {}
        
        # Browser blocking states
        self.browser_blocking_enabled = True
        
    def load_blocked_items(self):
        """Load blocked items from files"""
        try:
            # Load blocked processes
            if os.path.exists(BLOCKED_PROCESSES_FILE):
                with open(BLOCKED_PROCESSES_FILE, 'r') as f:
                    data = json.load(f)
                    self.blocked_processes = set(data.get('processes', []))
            
            # Load blocked IPs
            if os.path.exists(BLOCKED_IPS_FILE):
                with open(BLOCKED_IPS_FILE, 'r') as f:
                    data = json.load(f)
                    self.blocked_ips = set(data.get('ips', []))
                    self.blocked_domains = set(data.get('domains', []))
                    
        except Exception as e:
            print(f"Error loading blocked items: {e}")
    
    def save_blocked_items(self):
        """Save blocked items to files"""
        try:
            # Save blocked processes
            with open(BLOCKED_PROCESSES_FILE, 'w') as f:
                json.dump({
                    'processes': list(self.blocked_processes),
                    'timestamp': time.time()
                }, f)
            
            # Save blocked IPs
            with open(BLOCKED_IPS_FILE, 'w') as f:
                json.dump({
                    'ips': list(self.blocked_ips),
                    'domains': list(self.blocked_domains),
                    'timestamp': time.time()
                }, f)
                
        except Exception as e:
            print(f"Error saving blocked items: {e}")
    
    def block_process(self, process_name: str, process_pid: int = None) -> bool:
        """Block a process by name"""
        if process_name not in KNOWN_SAFE:
            self.blocked_processes.add(process_name.lower())
            self.save_blocked_items()
            
            if process_pid:
                self.kill_process(process_pid)
            
            print(f"Process blocked: {process_name}")
            return True
        return False
    
    def unblock_process(self, process_name: str) -> bool:
        """Unblock a process"""
        if process_name.lower() in self.blocked_processes:
            self.blocked_processes.remove(process_name.lower())
            self.save_blocked_items()
            return True
        return False
    
    def kill_process(self, pid: int) -> bool:
        """Kill a process by PID"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            try:
                process.wait(timeout=3)
            except psutil.TimeoutExpired:
                process.kill()
            print(f"Process killed: PID {pid}")
            return True
        except Exception as e:
            print(f"Failed to kill process {pid}: {e}")
            return False
    
    def block_ip(self, ip_address: str) -> bool:
        """Block an IP address"""
        self.blocked_ips.add(ip_address)
        self.save_blocked_items()
        
        # Also block in Windows Firewall if available
        if platform.system() == "Windows":
            self.block_ip_windows_firewall(ip_address)
        
        print(f"IP blocked: {ip_address}")
        return True
    
    def block_ip_windows_firewall(self, ip_address: str):
        """Block IP in Windows Firewall"""
        try:
            # Add firewall rule to block IP
            rule_name = f"BlockMalware_{ip_address.replace('.', '_')}"
            
            # Inbound rule
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name={rule_name}_IN',
                'dir=in',
                'action=block',
                f'remoteip={ip_address}',
                'enable=yes'
            ], capture_output=True, shell=True)
            
            # Outbound rule
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name={rule_name}_OUT',
                'dir=out',
                'action=block',
                f'remoteip={ip_address}',
                'enable=yes'
            ], capture_output=True, shell=True)
            
        except Exception as e:
            print(f"Windows Firewall blocking failed: {e}")
    
    def block_website(self, domain: str) -> bool:
        """Block a website by adding to hosts file"""
        try:
            self.blocked_domains.add(domain)
            self.save_blocked_items()
            
            # Read current hosts file
            with open(HOSTS_FILE, 'r') as f:
                lines = f.readlines()
            
            # Check if domain is already blocked
            domain_blocked = any(domain in line for line in lines)
            
            if not domain_blocked:
                # Add blocking entry
                blocking_entry = f"127.0.0.1 {domain}\n"
                blocking_entry += f"::1 {domain}\n"
                
                with open(HOSTS_FILE, 'a') as f:
                    f.write(blocking_entry)
                
                # Flush DNS cache
                self.flush_dns_cache()
                
                print(f"Website blocked: {domain}")
                return True
                
        except PermissionError:
            print(f"Permission denied. Try running as administrator/root to block websites.")
            return False
        except Exception as e:
            print(f"Error blocking website {domain}: {e}")
            return False
        
        return False
    
    def flush_dns_cache(self):
        """Flush DNS cache"""
        try:
            if platform.system() == "Windows":
                subprocess.run(['ipconfig', '/flushdns'], capture_output=True, shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['dscacheutil', '-flushcache'], capture_output=True)
            else:  # Linux
                subprocess.run(['systemd-resolve', '--flush-caches'], capture_output=True)
        except Exception as e:
            print(f"DNS flush failed: {e}")
    
    def is_process_blocked(self, process_name: str) -> bool:
        """Check if a process is blocked"""
        return process_name.lower() in self.blocked_processes
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if an IP is blocked"""
        return ip_address in self.blocked_ips
    
    def is_website_blocked(self, domain: str) -> bool:
        """Check if a website is blocked"""
        return domain in self.blocked_domains
    
    def check_and_block_suspicious(self, process_name: str, process_pid: int, 
                                  ip_address: str, risk_score: float) -> bool:
        """Automatically block if risk is critical"""
        if risk_score >= 8.0:  # CRITICAL risk
            if process_name and process_pid:
                self.block_process(process_name, process_pid)
            
            if ip_address and ip_address != '0.0.0.0':
                self.block_ip(ip_address)
            
            return True
        return False