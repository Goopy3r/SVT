"""
Home/overview tab
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import psutil
import time
from datetime import datetime

class HomeTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🏠 Home")
        
        # Create notebook for home tab
        home_notebook = ttk.Notebook(self.frame)
        home_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add sub-tabs
        self.setup_overview_tab(home_notebook)
        self.setup_live_monitor_tab(home_notebook)
        self.setup_statistics_tab(home_notebook)
    
    def setup_overview_tab(self, notebook):
        """Setup overview tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Overview")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create grid for overview widgets
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)
        
        # Status widgets
        status_widgets = [
            ("🟢 System Status", "All systems operational", "#00ff00"),
            ("🔴 Threats Blocked", "0 today", "#ff4444"),
            ("📊 Total Scans", "0", "#45b7d1"),
            ("🌍 Countries", "0", "#feca57"),
            ("⚙️ Processes", "0 monitored", "#ff6b6b"),
            ("🛡️ Protection", "Active", "#00cc66")
        ]
        
        for i, (title, value, color) in enumerate(status_widgets):
            frame = tk.Frame(main_frame, bg="#404040", relief=tk.RAISED, borderwidth=1)
            frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
            
            tk.Label(frame, text=title, bg="#404040", fg="white", 
                    font=("Arial", 9, "bold")).pack(pady=(5, 2))
            tk.Label(frame, text=value, bg="#404040", fg=color,
                    font=("Arial", 12, "bold")).pack(pady=(2, 5))
        
        # Recent activity
        activity_frame = tk.LabelFrame(main_frame, text="Recent Activity",
                                      bg="#404040", fg="white", padx=10, pady=10)
        activity_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.activity_text = scrolledtext.ScrolledText(activity_frame, height=6,
                                                      bg="#505050", fg="white",
                                                      font=("Consolas", 8))
        self.activity_text.pack(fill=tk.BOTH, expand=True)
        self.activity_text.insert(1.0, "System started...\n")
        self.activity_text.config(state=tk.DISABLED)
    
    def setup_live_monitor_tab(self, notebook):
        """Setup live monitor tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Live Monitor")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create live connection list
        columns = ('Time', 'Process', 'IP:Port', 'Risk', 'Country', 'Action')
        self.live_connections_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.live_connections_tree.heading(col, text=col)
            width = 70 if col in ['Time', 'Risk', 'Country'] else 120 if col == 'Action' else 150
            self.live_connections_tree.column(col, width=width, minwidth=50)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.live_connections_tree.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.live_connections_tree.xview)
        self.live_connections_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Layout
        self.live_connections_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg="#2d3436")
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        buttons = [
            ("▶️ Start Monitor", self.start_live_monitor),
            ("⏸️ Pause Monitor", self.pause_live_monitor),
            ("🗑️ Clear List", self.clear_live_monitor),
            ("📋 Copy Selected", self.copy_selected_connection)
        ]
        
        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                           bg="#404040", fg="white", relief=tk.FLAT, padx=5)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Start updating live connections
        self.app.root.after(2000, self.update_live_connections)
    
    def setup_statistics_tab(self, notebook):
        """Setup statistics tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Statistics")
        
        # Main frame
        main_frame = tk.Frame(frame, bg="#2d3436")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create text widget for statistics
        self.stats_text = scrolledtext.ScrolledText(main_frame, height=12,
                                                   bg="#505050", fg="white",
                                                   font=("Consolas", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Start updating statistics
        self.app.root.after(1000, self.update_stats_display)
    
    def update_live_connections(self):
        """Update live connections tree"""
        try:
            # Clear existing data
            for item in self.live_connections_tree.get_children():
                self.live_connections_tree.delete(item)
            
            # Get current connections
            connections = psutil.net_connections(kind='inet')
            current_time = time.time()
            
            # Add active connections to tree
            for conn in connections[:20]:  # Show last 20 connections
                try:
                    if not conn.pid or not conn.raddr:
                        continue
                    
                    # Get process info
                    try:
                        process = psutil.Process(conn.pid)
                        proc_name = process.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        proc_name = "unknown"
                    
                    # Get geolocation
                    geo = self.app.geo_locator.get_location(conn.raddr.ip)
                    
                    # Calculate risk
                    ip_risk = self.app.risk_engine.calculate_ip_risk(conn.raddr.ip, {
                        'vt_malicious': 0,
                        'vt_suspicious': 0,
                        'port': conn.raddr.port,
                        'country': geo['country']
                    })
                    
                    risk_level, _ = self.app.risk_engine.get_risk_level(ip_risk)
                    
                    # Determine action
                    action = "✅ Allowed"
                    if self.app.blocking_manager.is_process_blocked(proc_name):
                        action = "🚫 Process Blocked"
                    elif self.app.blocking_manager.is_ip_blocked(conn.raddr.ip):
                        action = "🚫 IP Blocked"
                    elif ip_risk >= 8:
                        action = "⚠️ High Risk"
                    
                    # Add to tree
                    self.live_connections_tree.insert('', 'end', values=(
                        datetime.now().strftime("%H:%M:%S"),
                        proc_name[:15],
                        f"{conn.raddr.ip}:{conn.raddr.port}",
                        f"{risk_level} ({ip_risk:.1f})",
                        geo['country'],
                        action
                    ))
                    
                except Exception:
                    continue
            
            # Keep only last 100 items
            items = self.live_connections_tree.get_children()
            if len(items) > 100:
                for item in items[:-100]:
                    self.live_connections_tree.delete(item)
                    
        except Exception as e:
            print(f"Live connections update error: {e}")
        
        # Schedule next update
        self.app.root.after(2000, self.update_live_connections)
    
    def update_stats_display(self):
        """Update statistics display"""
        try:
            stats = self.app.monitor.get_traffic_stats()
            
            stats_text = f"""
=== NETWORK STATISTICS ===

Total Connections: {stats['total_connections']}
Active Connections: {stats['active_connections']}
Unique IPs: {stats['unique_ips']}
Unique Processes: {stats['unique_processes']}

Top IPs by Connections:
"""
            for i, (ip, ip_stats) in enumerate(stats['top_ips'][:5], 1):
                stats_text += f"  {i}. {ip}: {ip_stats['total']} connections\n"
            
            stats_text += "\nTop Processes by Connections:\n"
            for i, (proc, proc_stats) in enumerate(stats['top_processes'][:5], 1):
                stats_text += f"  {i}. {proc}: {proc_stats['total']} connections\n"
            
            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            self.stats_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Stats update error: {e}")
        
        # Schedule next update
        self.app.root.after(5000, self.update_stats_display)
    
    def start_live_monitor(self):
        """Start live monitor"""
        self.app.update_console("▶️ Live monitor started\n", "info")
    
    def pause_live_monitor(self):
        """Pause live monitor"""
        self.app.update_console("⏸️ Live monitor paused\n", "info")
    
    def clear_live_monitor(self):
        """Clear live monitor"""
        for item in self.live_connections_tree.get_children():
            self.live_connections_tree.delete(item)
    
    def copy_selected_connection(self):
        """Copy selected connection info"""
        selection = self.live_connections_tree.selection()
        if selection:
            item = self.live_connections_tree.item(selection[0])
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(str(item['values']))
            self.app.update_console("📋 Connection info copied to clipboard\n", "info")