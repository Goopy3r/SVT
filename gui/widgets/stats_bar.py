"""
Statistics bar widget
"""

import tkinter as tk

class StatsBar(tk.Frame):  # Changed: Inherit from tk.Frame
    def __init__(self, parent):
        super().__init__(parent, bg="#2d3436", height=40)  # Changed: Call parent constructor
        self.vars = {}
        
        # Don't create a new frame, use self (which is already a Frame)
        self.pack_propagate(False)
        
        self.setup_stats_labels()
    
    def setup_stats_labels(self):
        """Setup statistics labels"""
        stats_data = [
            ("Connections:", "connections_var", "#00ff00"),
            ("Active:", "active_var", "#45b7d1"),
            ("Threats:", "threats_var", "#ff0000"),
            ("VT Reqs:", "vt_var", "#ffa500"),
            ("IPs:", "ips_var", "#feca57"),
            ("Processes:", "processes_var", "#ff6b6b"),
        ]
        
        for i, (label_text, var_name, color) in enumerate(stats_data):
            frame = tk.Frame(self, bg="#2d3436")  # Changed: Use self instead of self.stats_frame
            frame.pack(side=tk.LEFT, padx=10)
            
            tk.Label(frame, text=label_text, bg="#2d3436", fg="white", 
                    font=("Arial", 9)).pack(side=tk.LEFT)
            
            var = tk.StringVar(value="0")
            self.vars[var_name] = var
            
            tk.Label(frame, textvariable=var, bg="#2d3436", fg=color,
                    font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        
        # Add scan status
        status_frame = tk.Frame(self, bg="#2d3436")  # Changed: Use self instead of self.stats_frame
        status_frame.pack(side=tk.RIGHT, padx=10)
        
        self.scan_status_var = tk.StringVar(value="🟢 Scanning")
        tk.Label(status_frame, textvariable=self.scan_status_var, bg="#2d3436", fg="#00ff00",
                font=("Arial", 9)).pack()
    
    def update_stats(self, connections=0, active=0, threats=0, 
                    vt_requests=0, ips=0, processes=0):
        """Update statistics values"""
        self.vars['connections_var'].set(str(connections))
        self.vars['active_var'].set(str(active))
        self.vars['threats_var'].set(str(threats))
        self.vars['vt_var'].set(str(vt_requests))
        self.vars['ips_var'].set(str(ips))
        self.vars['processes_var'].set(str(processes))
    
    def update_scan_status(self, status):
        """Update scan status"""
        self.scan_status_var.set(status)