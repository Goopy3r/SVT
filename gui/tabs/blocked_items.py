"""
Blocked items view tab
"""

import tkinter as tk
from tkinter import ttk, messagebox

class BlockedItemsTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🚫 Blocked Items")
        
        # Create notebook for blocked items
        blocked_notebook = ttk.Notebook(self.frame)
        blocked_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add sub-tabs
        self.setup_blocked_processes_tab(blocked_notebook)
        self.setup_blocked_ips_tab(blocked_notebook)
        self.setup_blocked_websites_tab(blocked_notebook)
    
    def setup_blocked_processes_tab(self, notebook):
        """Setup blocked processes tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Processes")
        
        # Create treeview for blocked processes
        self.blocked_processes_tree = ttk.Treeview(frame, columns=('Process', 'Date Blocked'), 
                                                  show='headings', height=10)
        self.blocked_processes_tree.heading('Process', text='Process Name')
        self.blocked_processes_tree.heading('Date Blocked', text='Date Blocked')
        self.blocked_processes_tree.column('Process', width=250)
        self.blocked_processes_tree.column('Date Blocked', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.blocked_processes_tree.yview)
        self.blocked_processes_tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.blocked_processes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Button(button_frame, text="✅ Unblock Selected", command=self.unblock_selected_process_tree,
                 bg="#00cc66", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="🗑️ Remove All", command=self.remove_all_blocked_processes,
                 bg="#ff4444", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        
        # Load initial data
        self.refresh_blocked_processes_tree()
    
    def setup_blocked_ips_tab(self, notebook):
        """Setup blocked IPs tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="IP Addresses")
        
        self.blocked_ips_tree = ttk.Treeview(frame, columns=('IP Address', 'Country', 'Date Blocked'), 
                                            show='headings', height=10)
        self.blocked_ips_tree.heading('IP Address', text='IP Address')
        self.blocked_ips_tree.heading('Country', text='Country')
        self.blocked_ips_tree.heading('Date Blocked', text='Date Blocked')
        
        scrollbar2 = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.blocked_ips_tree.yview)
        self.blocked_ips_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.blocked_ips_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_blocked_ips_tree()
    
    def setup_blocked_websites_tab(self, notebook):
        """Setup blocked websites tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Websites")
        
        self.blocked_websites_tree = ttk.Treeview(frame, columns=('Website', 'Date Blocked'), 
                                                 show='headings', height=10)
        self.blocked_websites_tree.heading('Website', text='Website Domain')
        self.blocked_websites_tree.heading('Date Blocked', text='Date Blocked')
        
        scrollbar3 = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.blocked_websites_tree.yview)
        self.blocked_websites_tree.configure(yscrollcommand=scrollbar3.set)
        
        self.blocked_websites_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_blocked_websites_tree()
    
    def refresh_blocked_processes_tree(self):
        """Refresh blocked processes treeview"""
        # Clear existing data
        for item in self.blocked_processes_tree.get_children():
            self.blocked_processes_tree.delete(item)
        
        # Add blocked processes
        for process in self.app.blocking_manager.blocked_processes:
            self.blocked_processes_tree.insert('', 'end', values=(process, 'Unknown'))
    
    def refresh_blocked_ips_tree(self):
        """Refresh blocked IPs treeview"""
        # Clear existing data
        for item in self.blocked_ips_tree.get_children():
            self.blocked_ips_tree.delete(item)
        
        # Add blocked IPs
        for ip in self.app.blocking_manager.blocked_ips:
            # Get country info
            geo = self.app.geo_locator.get_location(ip)
            country = geo['country']
            self.blocked_ips_tree.insert('', 'end', values=(ip, country, 'Unknown'))
    
    def refresh_blocked_websites_tree(self):
        """Refresh blocked websites treeview"""
        # Clear existing data
        for item in self.blocked_websites_tree.get_children():
            self.blocked_websites_tree.delete(item)
        
        # Add blocked websites
        for domain in self.app.blocking_manager.blocked_domains:
            self.blocked_websites_tree.insert('', 'end', values=(domain, 'Unknown'))
    
    def unblock_selected_process_tree(self):
        """Unblock selected process from treeview"""
        selection = self.blocked_processes_tree.selection()
        if selection:
            item = self.blocked_processes_tree.item(selection[0])
            process_name = item['values'][0]
            if self.app.blocking_manager.unblock_process(process_name):
                self.blocked_processes_tree.delete(selection[0])
                self.app.update_console(f"✅ Process unblocked: {process_name}\n", "info")
    
    def remove_all_blocked_processes(self):
        """Remove all blocked processes"""
        if messagebox.askyesno("Confirm", "Remove ALL blocked processes?"):
            for item in self.blocked_processes_tree.get_children():
                self.blocked_processes_tree.delete(item)
            self.app.blocking_manager.blocked_processes.clear()
            self.app.blocking_manager.save_blocked_items()
            self.app.update_console("🧹 All blocked processes removed\n", "info")