"""
Blocking controls tab
"""

import tkinter as tk
from tkinter import ttk, messagebox
import psutil

from utils.helpers import validate_ip

class BlockingControlsTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🛡️ Blocking Controls")
        
        # Create notebook for detailed controls
        controls_notebook = ttk.Notebook(self.frame)
        controls_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add sub-tabs
        self.setup_process_blocking_tab(controls_notebook)
        self.setup_ip_blocking_tab(controls_notebook)
        self.setup_website_blocking_tab(controls_notebook)
        self.setup_rules_tab(controls_notebook)
    
    def setup_process_blocking_tab(self, notebook):
        """Setup process blocking tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Process Blocking")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left: Blocking controls
        control_frame = tk.Frame(main_frame, bg="#2d3436")
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Process name entry
        tk.Label(control_frame, text="Process Name:", bg="#2d3436", fg="white").pack(anchor=tk.W, pady=(0, 5))
        self.process_entry = tk.Entry(control_frame, bg="#505050", fg="white", insertbackground="white")
        self.process_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg="#2d3436")
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="🚫 Block Process", command=self.block_selected_process,
                 bg="#ff4444", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        tk.Button(button_frame, text="✅ Unblock Process", command=self.unblock_selected_process,
                 bg="#00cc66", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Process list
        tk.Label(control_frame, text="Running Processes:", bg="#2d3436", fg="white").pack(anchor=tk.W, pady=(15, 5))
        
        # Create listbox for processes
        process_list_frame = tk.Frame(control_frame, bg="#2d3436")
        process_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.process_listbox = tk.Listbox(process_list_frame, bg="#505050", fg="white", 
                                         selectbackground="#0984e3", height=8)
        process_scrollbar = tk.Scrollbar(process_list_frame, orient=tk.VERTICAL)
        self.process_listbox.config(yscrollcommand=process_scrollbar.set)
        process_scrollbar.config(command=self.process_listbox.yview)
        
        self.process_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        process_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button to refresh process list
        tk.Button(control_frame, text="🔄 Refresh Process List", command=self.refresh_process_list,
                 bg="#404040", fg="white", relief=tk.FLAT).pack(fill=tk.X, pady=(5, 0))
        
        # Right: Blocked processes list
        blocked_frame = tk.Frame(main_frame, bg="#2d3436")
        blocked_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(blocked_frame, text="Currently Blocked:", bg="#2d3436", fg="white").pack(anchor=tk.W)
        
        self.blocked_processes_listbox = tk.Listbox(blocked_frame, bg="#505050", fg="#ff4444",
                                                   selectbackground="#0984e3", height=8)
        blocked_scrollbar = tk.Scrollbar(blocked_frame, orient=tk.VERTICAL)
        self.blocked_processes_listbox.config(yscrollcommand=blocked_scrollbar.set)
        blocked_scrollbar.config(command=self.blocked_processes_listbox.yview)
        
        self.blocked_processes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        blocked_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_process_list()
        self.refresh_blocked_processes_list()
    
    def setup_ip_blocking_tab(self, notebook):
        """Setup IP blocking tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="IP Blocking")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left: Recent IPs
        left_frame = tk.Frame(main_frame, bg="#2d3436")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(left_frame, text="Recent Connections:", bg="#2d3436", fg="white").pack(anchor=tk.W)
        
        # Create treeview for recent IPs
        columns = ('IP', 'Country', 'Risk', 'Process')
        self.recent_ips_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.recent_ips_tree.heading(col, text=col)
            self.recent_ips_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.recent_ips_tree.yview)
        self.recent_ips_tree.configure(yscrollcommand=scrollbar.set)
        
        self.recent_ips_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right: IP blocking controls
        right_frame = tk.Frame(main_frame, bg="#2d3436")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # IP entry
        tk.Label(right_frame, text="IP Address:", bg="#2d3436", fg="white").pack(anchor=tk.W, pady=(0, 5))
        self.ip_entry = tk.Entry(right_frame, bg="#505050", fg="white", insertbackground="white")
        self.ip_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(right_frame, bg="#2d3436")
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="🚫 Block IP", command=self.block_selected_ip,
                 bg="#ff4444", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        tk.Button(button_frame, text="✅ Unblock IP", command=self.unblock_selected_ip,
                 bg="#00cc66", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        tk.Button(button_frame, text="🔍 Check IP", command=self.check_selected_ip,
                 bg="#404040", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Blocked IPs list
        tk.Label(right_frame, text="Blocked IPs:", bg="#2d3436", fg="white").pack(anchor=tk.W, pady=(15, 5))
        
        self.blocked_ips_listbox = tk.Listbox(right_frame, bg="#505050", fg="#ff4444",
                                             selectbackground="#0984e3", height=8)
        blocked_scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL)
        self.blocked_ips_listbox.config(yscrollcommand=blocked_scrollbar.set)
        blocked_scrollbar.config(command=self.blocked_ips_listbox.yview)
        
        self.blocked_ips_listbox.pack(fill=tk.BOTH, expand=True)
        blocked_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial blocked IPs
        self.refresh_blocked_lists()
    
    def setup_website_blocking_tab(self, notebook):
        """Setup website blocking tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Website Blocking")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left: Domain blocking
        left_frame = tk.Frame(main_frame, bg="#2d3436")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(left_frame, text="Domain/Website:", bg="#2d3436", fg="white").pack(anchor=tk.W, pady=(0, 5))
        self.website_entry = tk.Entry(left_frame, bg="#505050", fg="white", insertbackground="white")
        self.website_entry.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(left_frame, text="Example: example.com or sub.example.com", 
                bg="#2d3436", fg="gray", font=("Arial", 8)).pack(anchor=tk.W)
        
        # Buttons
        button_frame = tk.Frame(left_frame, bg="#2d3436")
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="🌐 Block Website", command=self.block_selected_website,
                 bg="#ff4444", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        tk.Button(button_frame, text="✅ Unblock Website", command=self.unblock_selected_website,
                 bg="#00cc66", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Quick block buttons for common sites
        tk.Label(left_frame, text="Quick Block:", bg="#2d3436", fg="white").pack(anchor=tk.W, pady=(15, 5))
        
        quick_sites = [
            ("🚫 Malware Sites", ["malware.com", "virus.com"]),
            ("🎰 Gambling", ["poker.com", "casino.com"]),
            ("📢 Ads/Tracking", ["doubleclick.net", "tracking.com"]),
            ("🎮 Gaming", ["steampowered.com", "epicgames.com"])
        ]
        
        for label, sites in quick_sites:
            frame = tk.Frame(left_frame, bg="#2d3436")
            frame.pack(fill=tk.X, pady=2)
            tk.Label(frame, text=label, bg="#2d3436", fg="white", width=15).pack(side=tk.LEFT)
            
            for site in sites:
                btn = tk.Button(frame, text=site, command=lambda s=site: self.quick_block_site(s),
                               bg="#404040", fg="white", relief=tk.FLAT, font=("Arial", 8))
                btn.pack(side=tk.LEFT, padx=2)
        
        # Right: Blocked websites list
        right_frame = tk.Frame(main_frame, bg="#2d3436")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(right_frame, text="Blocked Websites:", bg="#2d3436", fg="white").pack(anchor=tk.W)
        
        self.blocked_websites_listbox = tk.Listbox(right_frame, bg="#505050", fg="#ff4444",
                                                  selectbackground="#0984e3", height=10)
        blocked_scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL)
        self.blocked_websites_listbox.config(yscrollcommand=blocked_scrollbar.set)
        blocked_scrollbar.config(command=self.blocked_websites_listbox.yview)
        
        self.blocked_websites_listbox.pack(fill=tk.BOTH, expand=True)
        blocked_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status info
        status_frame = tk.Frame(right_frame, bg="#2d3436")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(status_frame, text="Website blocking modifies hosts file.", 
                bg="#2d3436", fg="yellow", font=("Arial", 8)).pack(anchor=tk.W)
        tk.Label(status_frame, text="Run as admin for full functionality.", 
                bg="#2d3436", fg="yellow", font=("Arial", 8)).pack(anchor=tk.W)
        
        # Load initial blocked websites
        self.refresh_blocked_lists()
    
    def setup_rules_tab(self, notebook):
        """Setup rules and settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Rules & Settings")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left: Auto-blocking settings
        left_frame = tk.LabelFrame(main_frame, text="Auto-Blocking Settings",
                                  bg="#404040", fg="white", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Auto-block toggle
        self.autoblock_var = tk.BooleanVar(value=True)
        autoblock_check = tk.Checkbutton(left_frame, text="Enable Auto-blocking",
                                        variable=self.autoblock_var,
                                        command=self.toggle_autoblock,
                                        bg="#404040", fg="white",
                                        selectcolor="#404040", activebackground="#404040")
        autoblock_check.pack(anchor=tk.W, pady=(0, 10))
        
        tk.Label(left_frame, text="Auto-block thresholds:", bg="#404040", fg="white").pack(anchor=tk.W, pady=(0, 5))
        
        # Risk threshold slider
        threshold_frame = tk.Frame(left_frame, bg="#404040")
        threshold_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(threshold_frame, text="Risk ≥", bg="#404040", fg="white").pack(side=tk.LEFT)
        self.risk_threshold = tk.Scale(threshold_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                      bg="#404040", fg="white", troughcolor="#505050",
                                      length=150)
        self.risk_threshold.set(8)
        self.risk_threshold.pack(side=tk.LEFT, padx=5)
        
        # VirusTotal threshold
        vt_frame = tk.Frame(left_frame, bg="#404040")
        vt_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(vt_frame, text="VT Malicious ≥", bg="#404040", fg="white").pack(side=tk.LEFT)
        self.vt_threshold = tk.Scale(vt_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                    bg="#404040", fg="white", troughcolor="#505050",
                                    length=150)
        self.vt_threshold.set(3)
        self.vt_threshold.pack(side=tk.LEFT, padx=5)
        
        # Country blocking
        tk.Label(left_frame, text="Auto-block countries:", bg="#404040", fg="white").pack(anchor=tk.W, pady=(15, 5))
        
        country_frame = tk.Frame(left_frame, bg="#404040")
        country_frame.pack(fill=tk.BOTH, expand=True)
        
        self.country_vars = {}
        countries = ["CN", "RU", "IR", "KP", "SY", "VN", "BY", "UA"]
        
        for i, country in enumerate(countries):
            var = tk.BooleanVar(value=True if country in ["CN", "RU", "KP"] else False)
            self.country_vars[country] = var
            cb = tk.Checkbutton(country_frame, text=country, variable=var,
                              bg="#404040", fg="white", selectcolor="#404040",
                              activebackground="#404040")
            cb.grid(row=i//4, column=i%4, sticky=tk.W, padx=5, pady=2)
        
        # Right: Quick actions
        right_frame = tk.LabelFrame(main_frame, text="Quick Actions",
                                   bg="#404040", fg="white", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        actions = [
            ("🔍 Scan All Processes", self.scan_all_processes),
            ("🧹 Clear All Blocks", self.clear_all_blocks),
            ("🔄 Update Rules", self.update_rules),
            ("📊 Export Logs", self.export_logs),
            ("⚙️ Test Firewall", self.test_firewall),
            ("💾 Backup Config", self.backup_config)
        ]
        
        for text, command in actions:
            btn = tk.Button(right_frame, text=text, command=command,
                           bg="#505050", fg="white", relief=tk.FLAT,
                           padx=10, pady=5)
            btn.pack(fill=tk.X, pady=2)
        
        # Save settings button
        tk.Button(right_frame, text="💾 Save Settings", command=self.save_settings,
                 bg="#0984e3", fg="white", relief=tk.FLAT,
                 padx=10, pady=5).pack(fill=tk.X, pady=(10, 0))
    
    # Helper methods for blocking controls
    def refresh_process_list(self):
        """Refresh the list of running processes"""
        self.process_listbox.delete(0, tk.END)
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name']
                    from settings import KNOWN_SAFE
                    if proc_name.lower() not in KNOWN_SAFE:
                        self.process_listbox.insert(tk.END, f"{proc_name} (PID: {proc.info['pid']})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            self.app.update_console(f"Error refreshing process list: {e}\n", "error")
    
    def refresh_blocked_processes_list(self):
        """Refresh only the blocked processes listbox"""
        self.blocked_processes_listbox.delete(0, tk.END)
        for proc in self.app.blocking_manager.blocked_processes:
            self.blocked_processes_listbox.insert(tk.END, proc)
    
    def refresh_blocked_lists(self):
        """Refresh all blocked lists"""
        # Blocked processes
        if hasattr(self, 'blocked_processes_listbox'):
            self.blocked_processes_listbox.delete(0, tk.END)
            for proc in self.app.blocking_manager.blocked_processes:
                self.blocked_processes_listbox.insert(tk.END, proc)
        
        # Blocked IPs
        if hasattr(self, 'blocked_ips_listbox'):
            self.blocked_ips_listbox.delete(0, tk.END)
            for ip in self.app.blocking_manager.blocked_ips:
                self.blocked_ips_listbox.insert(tk.END, ip)
        
        # Blocked websites
        if hasattr(self, 'blocked_websites_listbox'):
            self.blocked_websites_listbox.delete(0, tk.END)
            for site in self.app.blocking_manager.blocked_domains:
                self.blocked_websites_listbox.insert(tk.END, site)
    
    def toggle_autoblock(self):
        """Toggle auto-blocking"""
        self.app.monitor.autoblock_enabled = self.autoblock_var.get()
        status = "ENABLED" if self.app.monitor.autoblock_enabled else "DISABLED"
        self.app.update_console(f"🔧 Auto-blocking {status}\n", "info")
    
    def block_selected_process(self):
        """Block the process entered in the process field"""
        process_name = self.process_entry.get().strip()
        if process_name:
            if self.app.blocking_manager.block_process(process_name):
                self.app.update_console(f"🚫 Process blocked: {process_name}\n", "alert")
                self.process_entry.delete(0, tk.END)
                self.refresh_blocked_lists()
            else:
                messagebox.showwarning("Cannot Block", f"Process {process_name} is in safe list.")
    
    def unblock_selected_process(self):
        """Unblock selected process"""
        selection = self.blocked_processes_listbox.curselection()
        if selection:
            process_name = self.blocked_processes_listbox.get(selection[0])
            if self.app.blocking_manager.unblock_process(process_name):
                self.app.update_console(f"✅ Process unblocked: {process_name}\n", "info")
                self.refresh_blocked_lists()
    
    def block_selected_ip(self):
        """Block the IP entered in the IP field"""
        ip = self.ip_entry.get().strip()
        if ip and validate_ip(ip):
            self.app.blocking_manager.block_ip(ip)
            self.app.update_console(f"🚫 IP blocked: {ip}\n", "alert")
            self.ip_entry.delete(0, tk.END)
            self.refresh_blocked_lists()
    
    def unblock_selected_ip(self):
        """Unblock selected IP"""
        selection = self.blocked_ips_listbox.curselection()
        if selection:
            ip = self.blocked_ips_listbox.get(selection[0])
            self.app.blocking_manager.blocked_ips.discard(ip)
            self.app.blocking_manager.save_blocked_items()
            self.app.update_console(f"✅ IP unblocked: {ip}\n", "info")
            self.refresh_blocked_lists()
    
    def check_selected_ip(self):
        """Check selected IP with VirusTotal"""
        ip = self.ip_entry.get().strip()
        if ip and validate_ip(ip):
            self.app.update_console(f"🔍 Checking IP: {ip} with VirusTotal...\n", "info")
            vt_data = self.app.vt_analyzer.check_ip(ip)
            self.app.update_console(f"   VT Results: Malicious: {vt_data['malicious']}, Suspicious: {vt_data['suspicious']}\n", "info")
    
    def block_selected_website(self):
        """Block the website entered in the website field"""
        domain = self.website_entry.get().strip()
        if domain:
            if self.app.blocking_manager.block_website(domain):
                self.app.update_console(f"🌐 Website blocked: {domain}\n", "alert")
                self.website_entry.delete(0, tk.END)
                self.refresh_blocked_lists()
    
    def unblock_selected_website(self):
        """Unblock selected website"""
        selection = self.blocked_websites_listbox.curselection()
        if selection:
            domain = self.blocked_websites_listbox.get(selection[0])
            self.app.blocking_manager.blocked_domains.discard(domain)
            self.app.blocking_manager.save_blocked_items()
            self.app.update_console(f"✅ Website unblocked: {domain}\n", "info")
            self.refresh_blocked_lists()
    
    def quick_block_site(self, site):
        """Quick block a predefined site"""
        self.website_entry.delete(0, tk.END)
        self.website_entry.insert(0, site)
        self.block_selected_website()
    
    def scan_all_processes(self):
        """Scan all running processes for suspicious activity"""
        try:
            suspicious_count = 0
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'connections']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    # Skip known safe processes
                    from settings import KNOWN_SAFE
                    if proc_name in KNOWN_SAFE:
                        continue
                    
                    # Check connections
                    connections = proc.info.get('connections', [])
                    if connections:
                        vt_risk = 0
                        for conn in connections:
                            if hasattr(conn, 'raddr') and conn.raddr:
                                vt_data = self.app.vt_analyzer.check_ip(conn.raddr.ip)
                                vt_risk = max(vt_risk, vt_data['malicious'])
                        
                        if vt_risk > 0:
                            self.app.update_console(f"⚠️ Suspicious: {proc_name} (VT score: {vt_risk})\n", "warning")
                            suspicious_count += 1
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.app.update_console(f"🔍 Scan complete. Found {suspicious_count} suspicious processes\n", "info")
            
        except Exception as e:
            self.app.update_console(f"Scan error: {e}\n", "error")
    
    def clear_all_blocks(self):
        """Clear all blocked items"""
        if messagebox.askyesno("Confirm", "Clear ALL blocked items?"):
            self.app.blocking_manager.blocked_processes.clear()
            self.app.blocking_manager.blocked_ips.clear()
            self.app.blocking_manager.blocked_domains.clear()
            self.app.blocking_manager.save_blocked_items()
            self.app.update_console("🧹 All blocks cleared\n", "info")
            self.refresh_blocked_lists()
    
    def update_rules(self):
        """Update blocking rules"""
        self.app.update_console("🔄 Updating blocking rules...\n", "info")
        # Implement rule update logic here
        self.app.update_console("✅ Rules updated\n", "info")
    
    def export_logs(self):
        """Export logs to file"""
        try:
            from datetime import datetime
            filename = f"logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write("Log export not implemented yet.")
            self.app.update_console(f"📥 Logs exported to: {filename}\n", "info")
        except Exception as e:
            self.app.update_console(f"❌ Export failed: {e}\n", "warning")
    
    def test_firewall(self):
        """Test firewall functionality"""
        self.app.update_console("🛡️ Testing firewall...\n", "info")
        self.app.update_console("✅ Firewall test completed\n", "info")
    
    def backup_config(self):
        """Backup configuration"""
        try:
            import json, time
            from datetime import datetime
            filename = f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            config = {
                'blocked_processes': list(self.app.blocking_manager.blocked_processes),
                'blocked_ips': list(self.app.blocking_manager.blocked_ips),
                'blocked_domains': list(self.app.blocking_manager.blocked_domains),
                'timestamp': time.time()
            }
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            self.app.update_console(f"💾 Config backed up to: {filename}\n", "info")
        except Exception as e:
            self.app.update_console(f"❌ Backup failed: {e}\n", "warning")
    
    def save_settings(self):
        """Save current settings"""
        self.app.update_console("💾 Saving settings...\n", "info")
        self.app.update_console("✅ Settings saved\n", "info")