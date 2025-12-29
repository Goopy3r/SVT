"""
Console widget for displaying logs
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import csv
from datetime import datetime

class ConsoleWidget:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        # Create main frame
        self.main_frame = tk.Frame(parent, bg="#2d3436")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Console text area
        self.console = scrolledtext.ScrolledText(
            self.main_frame,
            bg="#0a0a0a",
            fg="#00ff00",
            font=("Consolas", 9),
            height=20,
            wrap=tk.WORD
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tags for coloring
        self.configure_tags()
        
        # Control buttons
        self.setup_buttons()
    
    def configure_tags(self):
        """Configure text tags for coloring"""
        self.console.tag_config("alert", foreground="#ff0000", font=("Consolas", 9, "bold"))
        self.console.tag_config("warning", foreground="#ff6600")
        self.console.tag_config("info", foreground="#00ff00")
        self.console.tag_config("low", foreground="#00cc00")
        self.console.tag_config("error", foreground="#ff0000", background="#330000")
    
    def setup_buttons(self):
        """Setup console control buttons"""
        button_frame = tk.Frame(self.main_frame, bg="#2d3436")
        button_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        buttons = [
            ("🗑️ Clear", self.clear_console),
            ("📊 Export", self.export_data),
            ("🔄 Refresh", self.refresh_display),
            ("📷 Map", self.capture_map),
            ("🔍 Test Scan", self.test_scan)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg="#404040",
                fg="white",
                font=("Arial", 8),
                relief=tk.FLAT,
                padx=5,
                pady=2
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def insert(self, text, tag="info"):
        """Insert text into console with specified tag"""
        self.console.insert(tk.END, text, tag)
        self.console.see(tk.END)
        
        # Limit console size
        lines = self.console.get("1.0", tk.END).split('\n')
        if len(lines) > 200:
            self.console.delete("1.0", f"{len(lines)-100}.0")
    
    def clear_console(self):
        """Clear the console"""
        self.console.delete(1.0, tk.END)
    
    def export_data(self):
        """Export data to file"""
        try:
            filename = f"network_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Time', 'Process', 'IP', 'Port', 'Country', 'Risk'])
                
                # Get connection data from monitor
                for proc_name, connections in self.app.monitor.connections_history.items():
                    for conn in connections[-100:]:  # Last 100 connections
                        writer.writerow([
                            datetime.fromtimestamp(conn['timestamp']).strftime('%H:%M:%S'),
                            proc_name,
                            conn['remote_ip'],
                            conn['remote_port'],
                            conn['country'],
                            f"{self.app.risk_engine.ip_scores[conn['remote_ip']]['score']:.1f}" 
                            if conn['remote_ip'] in self.app.risk_engine.ip_scores else "0.0"
                        ])
            
            self.insert(f"✅ Data exported to: {filename}\n", "info")
            
        except Exception as e:
            self.insert(f"❌ Export failed: {e}\n", "warning")
    
    def refresh_display(self):
        """Refresh all displays"""
        # Refresh process list if method exists
        if hasattr(self.app, 'refresh_process_list'):
            self.app.refresh_process_list()
        
        # Refresh blocked lists if method exists
        if hasattr(self.app, 'refresh_blocked_lists'):
            self.app.refresh_blocked_lists()
        
        # Redraw map if canvas exists
        if hasattr(self.app, 'map_viz') and self.app.map_viz.canvas:
            self.app.map_viz.canvas.draw()
        
        self.insert("🔄 Display refreshed\n", "info")
    
    def capture_map(self):
        """Capture map screenshot"""
        try:
            if self.app.map_viz.fig:
                filename = f"map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                self.app.map_viz.fig.savefig(filename, dpi=100, bbox_inches='tight')
                self.insert(f"📸 Map saved: {filename}\n", "info")
        except Exception as e:
            self.insert(f"❌ Capture failed: {e}\n", "warning")
    
    def test_scan(self):
        """Test scanning functionality"""
        try:
            import psutil
            connections = psutil.net_connections(kind='inet')
            count = 0
            
            for conn in connections:
                if conn.raddr and conn.raddr.ip not in ['127.0.0.1', '::1', '0.0.0.0']:
                    count += 1
            
            self.insert(f"Test Scan: Found {count} external connections\n", "info")
            
        except Exception as e:
            self.insert(f"Test Scan Error: {e}\n", "error")