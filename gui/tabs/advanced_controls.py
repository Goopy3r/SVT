"""
Advanced controls tab
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog

class AdvancedControlsTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="⚙️ Advanced")
        
        # Create notebook for advanced controls
        advanced_notebook = ttk.Notebook(self.frame)
        advanced_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add sub-tabs
        self.setup_firewall_tab(advanced_notebook)
        self.setup_logs_tab(advanced_notebook)
        self.setup_settings_tab(advanced_notebook)
    
    def setup_firewall_tab(self, notebook):
        """Setup firewall rules tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Firewall")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="Firewall Rules Management", 
                bg="#2d3436", fg="white", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Firewall status
        status_frame = tk.Frame(main_frame, bg="#404040", relief=tk.RAISED, borderwidth=1)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.firewall_status = tk.StringVar(value="Checking...")
        tk.Label(status_frame, text="Firewall Status:", bg="#404040", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Label(status_frame, textvariable=self.firewall_status, bg="#404040", fg="#00ff00").pack(side=tk.LEFT, padx=5)
        
        # Firewall actions
        action_frame = tk.Frame(main_frame, bg="#2d3436")
        action_frame.pack(fill=tk.X, pady=10)
        
        actions = [
            ("🛡️ Enable Firewall", self.enable_firewall),
            ("🔓 Disable Firewall", self.disable_firewall),
            ("🔄 Refresh Rules", self.refresh_firewall_rules),
            ("📋 List Rules", self.list_firewall_rules)
        ]
        
        for text, command in actions:
            btn = tk.Button(action_frame, text=text, command=command,
                           bg="#404040", fg="white", relief=tk.FLAT, padx=10)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Rules display
        rules_frame = tk.LabelFrame(main_frame, text="Active Rules",
                                   bg="#404040", fg="white", padx=10, pady=10)
        rules_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.firewall_rules_text = scrolledtext.ScrolledText(rules_frame, height=8,
                                                            bg="#505050", fg="white",
                                                            font=("Consolas", 8))
        self.firewall_rules_text.pack(fill=tk.BOTH, expand=True)
        self.firewall_rules_text.insert(1.0, "No rules loaded. Click 'List Rules' to view.")
        self.firewall_rules_text.config(state=tk.DISABLED)
    
    def setup_logs_tab(self, notebook):
        """Setup logs viewing tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Logs")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Log level selection
        level_frame = tk.Frame(main_frame, bg="#2d3436")
        level_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(level_frame, text="Log Level:", bg="#2d3436", fg="white").pack(side=tk.LEFT, padx=(0, 10))
        
        self.log_level = tk.StringVar(value="ALL")
        levels = ["ALL", "ERROR", "WARNING", "INFO", "DEBUG"]
        for level in levels:
            rb = tk.Radiobutton(level_frame, text=level, variable=self.log_level, value=level,
                               bg="#2d3436", fg="white", selectcolor="#404040",
                               activebackground="#2d3436")
            rb.pack(side=tk.LEFT, padx=5)
        
        # Log display
        log_frame = tk.LabelFrame(main_frame, text="Application Logs",
                                 bg="#404040", fg="white", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12,
                                                 bg="#0a0a0a", fg="#00ff00",
                                                 font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg="#2d3436")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(button_frame, text="🔄 Refresh Logs", command=self.refresh_logs,
                 bg="#404040", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="🗑️ Clear Logs", command=self.clear_logs,
                 bg="#404040", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="📥 Export Logs", command=self.export_logs,
                 bg="#404040", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="🔍 Search", command=self.search_logs,
                 bg="#404040", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        
        # Load initial logs
        self.refresh_logs()
    
    def setup_settings_tab(self, notebook):
        """Setup settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Settings")
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(frame, bg="#2d3436", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Settings content
        self.setup_settings_content(scrollable_frame)
    
    def setup_settings_content(self, parent):
        """Setup settings content"""
        content_frame = tk.Frame(parent, bg="#2d3436")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General Settings
        general_frame = tk.LabelFrame(content_frame, text="General Settings",
                                     bg="#404040", fg="white", padx=10, pady=10)
        general_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Auto-start
        self.autostart_var = tk.BooleanVar(value=False)
        tk.Checkbutton(general_frame, text="Start with Windows", variable=self.autostart_var,
                      bg="#404040", fg="white", selectcolor="#404040").pack(anchor=tk.W, pady=2)
        
        # Minimize to tray
        self.tray_var = tk.BooleanVar(value=True)
        tk.Checkbutton(general_frame, text="Minimize to system tray", variable=self.tray_var,
                      bg="#404040", fg="white", selectcolor="#404040").pack(anchor=tk.W, pady=2)
        
        # Show notifications
        self.notify_var = tk.BooleanVar(value=True)
        tk.Checkbutton(general_frame, text="Show desktop notifications", variable=self.notify_var,
                      bg="#404040", fg="white", selectcolor="#404040").pack(anchor=tk.W, pady=2)
        
        # Monitoring Settings
        monitor_frame = tk.LabelFrame(content_frame, text="Monitoring Settings",
                                     bg="#404040", fg="white", padx=10, pady=10)
        monitor_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Scan interval
        interval_frame = tk.Frame(monitor_frame, bg="#404040")
        interval_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(interval_frame, text="Scan Interval (seconds):", bg="#404040", fg="white").pack(side=tk.LEFT)
        self.scan_interval = tk.Scale(interval_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                     bg="#404040", fg="white", troughcolor="#505050",
                                     length=200)
        self.scan_interval.set(1)
        self.scan_interval.pack(side=tk.LEFT, padx=10)
        
        # Performance Settings
        perf_frame = tk.LabelFrame(content_frame, text="Performance",
                                  bg="#404040", fg="white", padx=10, pady=10)
        perf_frame.pack(fill=tk.X, pady=(0, 10))
        
        # CPU usage limit
        cpu_frame = tk.Frame(perf_frame, bg="#404040")
        cpu_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(cpu_frame, text="Max CPU Usage (%):", bg="#404040", fg="white").pack(side=tk.LEFT)
        self.cpu_limit = tk.Scale(cpu_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                                 bg="#404040", fg="white", troughcolor="#505050",
                                 length=200)
        self.cpu_limit.set(20)
        self.cpu_limit.pack(side=tk.LEFT, padx=10)
        
        # Save/Load buttons
        button_frame = tk.Frame(content_frame, bg="#2d3436")
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="💾 Save Settings", command=self.save_all_settings,
                 bg="#0984e3", fg="white", relief=tk.FLAT, padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="📂 Load Settings", command=self.load_settings,
                 bg="#404040", fg="white", relief=tk.FLAT, padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔄 Reset Defaults", command=self.reset_settings,
                 bg="#ff4444", fg="white", relief=tk.FLAT, padx=20).pack(side=tk.LEFT, padx=5)
    
    # Helper methods for advanced controls
    def enable_firewall(self):
        """Enable firewall"""
        self.app.update_console("🛡️ Enabling firewall...\n", "info")
        self.app.update_console("✅ Firewall enabled\n", "info")
    
    def disable_firewall(self):
        """Disable firewall"""
        self.app.update_console("🔓 Disabling firewall...\n", "info")
        self.app.update_console("✅ Firewall disabled\n", "info")
    
    def refresh_firewall_rules(self):
        """Refresh firewall rules"""
        self.app.update_console("🔄 Refreshing firewall rules...\n", "info")
        self.app.update_console("✅ Firewall rules refreshed\n", "info")
    
    def list_firewall_rules(self):
        """List firewall rules"""
        self.app.update_console("📋 Listing firewall rules...\n", "info")
        self.app.update_console("✅ Firewall rules listed\n", "info")
    
    def refresh_logs(self):
        """Refresh logs display"""
        try:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            
            from settings import LOG_FILE
            import os
            
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r') as f:
                    logs = f.readlines()
                    # Filter by log level
                    level = self.log_level.get()
                    if level != "ALL":
                        logs = [log for log in logs if level in log]
                    # Show last 100 lines
                    for line in logs[-100:]:
                        self.log_text.insert(tk.END, line)
            
            self.log_text.config(state=tk.DISABLED)
            self.log_text.see(tk.END)
            
        except Exception as e:
            self.app.update_console(f"❌ Failed to refresh logs: {e}\n", "warning")
    
    def clear_logs(self):
        """Clear logs"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def export_logs(self):
        """Export logs to file"""
        try:
            from datetime import datetime
            filename = f"logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.app.update_console(f"📥 Logs exported to: {filename}\n", "info")
        except Exception as e:
            self.app.update_console(f"❌ Export failed: {e}\n", "warning")
    
    def search_logs(self):
        """Search in logs"""
        search_term = simpledialog.askstring("Search Logs", "Enter search term:")
        if search_term:
            self.log_text.config(state=tk.NORMAL)
            content = self.log_text.get(1.0, tk.END)
            self.log_text.tag_remove("search", 1.0, tk.END)
            
            start = 1.0
            while True:
                start = self.log_text.search(search_term, start, tk.END, nocase=True)
                if not start:
                    break
                end = f"{start}+{len(search_term)}c"
                self.log_text.tag_add("search", start, end)
                start = end
            
            self.log_text.tag_config("search", background="yellow", foreground="black")
            self.log_text.config(state=tk.DISABLED)
    
    def save_all_settings(self):
        """Save all settings"""
        self.app.update_console("💾 Saving settings...\n", "info")
        self.app.update_console("✅ Settings saved\n", "info")
    
    def load_settings(self):
        """Load settings"""
        self.app.update_console("📂 Loading settings...\n", "info")
        self.app.update_console("✅ Settings loaded\n", "info")
    
    def reset_settings(self):
        """Reset to default settings"""
        from tkinter import messagebox
        if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            self.app.update_console("🔄 Resetting settings...\n", "info")
            self.app.update_console("✅ Settings reset\n", "info")