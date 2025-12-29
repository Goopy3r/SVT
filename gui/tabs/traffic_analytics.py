"""
Traffic analytics tab
"""

import tkinter as tk
from tkinter import ttk
from collections import deque
import time
import psutil

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class TrafficAnalyticsTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📊 Traffic Analytics")

        self.setup_traffic_graph()

    def setup_traffic_graph(self):
        """Setup enhanced traffic visualization"""
        # Create frame for the enhanced graph
        graph_frame = tk.Frame(self.frame, bg="#1e1e1e")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if MATPLOTLIB_AVAILABLE:
            self.setup_matplotlib_graph(graph_frame)
        else:
            self.setup_fallback_graph(graph_frame)

    def setup_matplotlib_graph(self, parent):
        """Setup matplotlib-based graph"""
        # Create a 2x2 grid of plots
        self.traffic_fig = Figure(
            figsize=(10, 8), dpi=100, facecolor='#1e1e1e')

        # 1. Main Traffic Graph (Top Left)
        self.traffic_ax = self.traffic_fig.add_subplot(221)
        self.traffic_ax.set_facecolor('#2d3436')

        # 2. Traffic Composition Pie Chart (Top Right)
        self.pie_ax = self.traffic_fig.add_subplot(222)
        self.pie_ax.set_facecolor('#2d3436')

        # 3. Connection Frequency (Bottom Left)
        self.conn_ax = self.traffic_fig.add_subplot(223)
        self.conn_ax.set_facecolor('#2d3436')

        # 4. Risk Distribution (Bottom Right)
        self.risk_ax = self.traffic_fig.add_subplot(224)
        self.risk_ax.set_facecolor('#2d3436')

        # Configure main traffic graph
        self.configure_main_graph()

        # Create canvas
        self.traffic_canvas = FigureCanvasTkAgg(
            self.traffic_fig, master=parent)
        self.traffic_canvas.draw()
        self.traffic_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.traffic_canvas, parent)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize data storage
        self.init_data_storage()

        # Add statistics labels
        self.setup_stats_labels(parent)

        # Start updating graph
        self.app.root.after(500, self.update_traffic_graph)

    def configure_main_graph(self):
        """Configure main traffic graph"""
        self.traffic_ax.set_title(' Live Network Traffic', color='white',
                                  fontsize=11, pad=10, fontweight='bold')
        self.traffic_ax.set_xlabel(
            'Time (seconds ago)', color='white', fontsize=9)
        self.traffic_ax.set_ylabel(
            'Bytes per Second', color='white', fontsize=9)
        self.traffic_ax.tick_params(colors='white', labelsize=8)
        self.traffic_ax.grid(True, alpha=0.2, color='gray', linestyle='--')

        # Create enhanced lines with gradients
        self.sent_line, = self.traffic_ax.plot([], [], color='#ff4444',
                                               linewidth=2.5, label='Sent',
                                               alpha=0.9, marker='o', markersize=3,
                                               markevery=5)
        self.received_line, = self.traffic_ax.plot([], [], color='#44ff44',
                                                   linewidth=2.5, label='Received',
                                                   alpha=0.9, marker='s', markersize=3,
                                                   markevery=5)

        # Enhanced legend
        legend = self.traffic_ax.legend(facecolor='#404040', labelcolor='white',
                                        edgecolor='#505050', fontsize=9)
        legend.get_frame().set_alpha(0.8)

    def init_data_storage(self):
        """Initialize data storage for graphs"""
        self.traffic_data = {
            'time': deque(maxlen=120),  # 2 minutes of data
            'sent': deque(maxlen=120),
            'received': deque(maxlen=120),
            'sent_rate': deque(maxlen=120),
            'received_rate': deque(maxlen=120),
            'connections': deque(maxlen=60),  # Last minute of connections
            'risks': deque(maxlen=60)
        }

        self.peak_sent = 0
        self.peak_recv = 0
        self.total_sent_bytes = 0
        self.total_recv_bytes = 0
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0

    def setup_stats_labels(self, parent):
        """Setup statistics labels"""
        stats_frame = tk.Frame(parent, bg='#2d3436')
        stats_frame.pack(fill=tk.X, pady=(5, 0))

        self.stats_vars = {
            'current_sent': tk.StringVar(value="0 B/s"),
            'current_recv': tk.StringVar(value="0 B/s"),
            'peak_sent': tk.StringVar(value="0 B/s"),
            'peak_recv': tk.StringVar(value="0 B/s"),
            'total_sent': tk.StringVar(value="0 MB"),
            'total_recv': tk.StringVar(value="0 MB")
        }

        stats_grid = tk.Frame(stats_frame, bg='#2d3436')
        stats_grid.pack()

        stats_labels = [
            ("Current Sent:", "current_sent", "#ff4444"),
            ("Current Recv:", "current_recv", "#44ff44"),
            ("Peak Sent:", "peak_sent", "#ff8888"),
            ("Peak Recv:", "peak_recv", "#88ff88"),
            ("Total Sent:", "total_sent", "#ffaaaa"),
            ("Total Recv:", "total_recv", "#aaffaa")
        ]

        for i, (label, var_name, color) in enumerate(stats_labels):
            row = i // 3
            col = i % 3

            frame = tk.Frame(stats_grid, bg='#2d3436')
            frame.grid(row=row, column=col, padx=5, pady=2, sticky='w')

            tk.Label(frame, text=label, bg='#2d3436', fg='white',
                     font=('Arial', 8)).pack(side=tk.LEFT)
            tk.Label(frame, textvariable=self.stats_vars[var_name],
                     bg='#2d3436', fg=color, font=('Arial', 8, 'bold')).pack(side=tk.LEFT)

    def setup_fallback_graph(self, parent):
        """Setup fallback text-based graph"""
        fallback_frame = tk.Frame(parent, bg='#2d3436')
        fallback_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(fallback_frame,
                 text="📊 Advanced Graphs Unavailable\n\n"
                 "Install required packages for enhanced visualizations:\n\n"
                 "pip install matplotlib numpy\n"
                 "pip install cartopy (for maps)\n\n"
                 "Current features still work without graphs.",
                 bg="#2d3436", fg="white", font=("Arial", 10),
                 justify=tk.CENTER).pack(expand=True)

        # Simple text-based stats as fallback
        self.fallback_stats = tk.Text(fallback_frame, height=8, width=50,
                                      bg='#0a0a0a', fg='#00ff00',
                                      font=("Consolas", 9))
        self.fallback_stats.pack(pady=10)
        self.fallback_stats.insert(
            1.0, "Traffic statistics will appear here...")
        self.fallback_stats.config(state=tk.DISABLED)

        # Start updating fallback stats
        self.app.root.after(1000, self.update_fallback_stats)
        
    def update_stats_labels(self):
        """Update statistics labels with current values"""
        if hasattr(self, 'stats_vars'):
            try:
                # Calculate current rates from the last data points
                if self.traffic_data['sent_rate'] and self.traffic_data['received_rate']:
                    # Get last rates (convert deques to lists first)
                    sent_rates = list(self.traffic_data['sent_rate'])
                    recv_rates = list(self.traffic_data['received_rate'])
                    
                    current_sent = sent_rates[-1] if sent_rates else 0
                    current_recv = recv_rates[-1] if recv_rates else 0
                else:
                    current_sent = 0
                    current_recv = 0
                
                # Update the StringVars
                self.stats_vars['current_sent'].set(f"{self.format_bytes(current_sent)}/s")
                self.stats_vars['current_recv'].set(f"{self.format_bytes(current_recv)}/s")
                self.stats_vars['peak_sent'].set(f"{self.format_bytes(self.peak_sent)}/s")
                self.stats_vars['peak_recv'].set(f"{self.format_bytes(self.peak_recv)}/s")
                self.stats_vars['total_sent'].set(f"{self.format_bytes(self.total_sent_bytes)}")
                self.stats_vars['total_recv'].set(f"{self.format_bytes(self.total_recv_bytes)}")
                
            except Exception as e:
                print(f"Error updating stats labels: {e}")

    def update_traffic_graph(self):
        """Update all traffic visualizations"""
        if not MATPLOTLIB_AVAILABLE:
            self.app.root.after(1000, self.update_traffic_graph)
            return

        try:
            self.update_network_stats()
            self.update_main_graph()
            self.update_stats_labels()

            # Update other charts periodically
            current_time = time.time()
            if int(current_time) % 5 == 0:
                self.update_pie_chart()
            if int(current_time) % 10 == 0:
                self.update_connection_frequency()
            if int(current_time) % 15 == 0:
                self.update_risk_distribution()

            # Schedule next update
            self.app.root.after(500, self.update_traffic_graph)

        except Exception as e:
            print(f"Graph update error: {e}")
            self.app.root.after(1000, self.update_traffic_graph)

    def update_network_stats(self):
        """Update network statistics"""
        try:
            net_io = psutil.net_io_counters()
            current_time = time.time()

            # Calculate rates
            current_sent = net_io.bytes_sent - self.last_bytes_sent
            current_recv = net_io.bytes_recv - self.last_bytes_recv
            self.last_bytes_sent = net_io.bytes_sent
            self.last_bytes_recv = net_io.bytes_recv

            # Update totals and peaks
            self.total_sent_bytes = net_io.bytes_sent
            self.total_recv_bytes = net_io.bytes_recv
            self.peak_sent = max(self.peak_sent, current_sent)
            self.peak_recv = max(self.peak_recv, current_recv)

            # Add data to history
            self.traffic_data['time'].append(current_time)
            self.traffic_data['sent'].append(net_io.bytes_sent)
            self.traffic_data['received'].append(net_io.bytes_recv)
            self.traffic_data['sent_rate'].append(current_sent)
            self.traffic_data['received_rate'].append(current_recv)
        except Exception as e:
            print(f"Network stats error: {e}")

    def update_main_graph(self):
        """Update the main traffic graph"""
        if len(self.traffic_data['time']) < 2:
            return

        try:
            # Convert timestamps to relative seconds
            time_rel = [t - self.traffic_data['time'][0]
                        for t in self.traffic_data['time']]

            # Convert deques to lists before slicing
            sent_rate_list = list(self.traffic_data['sent_rate'])
            received_rate_list = list(self.traffic_data['received_rate'])

            # Get last 60 elements or all if less than 60
            last_60 = min(60, len(time_rel))

            # Update main lines
            self.sent_line.set_data(
                time_rel[-last_60:],
                sent_rate_list[-last_60:] if len(
                    sent_rate_list) >= last_60 else sent_rate_list
            )
            self.received_line.set_data(
                time_rel[-last_60:],
                received_rate_list[-last_60:] if len(
                    received_rate_list) >= last_60 else received_rate_list
            )

            # Adjust axes
            if sent_rate_list and received_rate_list:
                y_max = max(
                    max(sent_rate_list[-last_60:]) if len(
                        sent_rate_list) >= last_60 else max(sent_rate_list),
                    max(received_rate_list[-last_60:]) if len(
                        received_rate_list) >= last_60 else max(received_rate_list)
                ) * 1.1
                self.traffic_ax.set_ylim(0, max(y_max, 1000))

            if time_rel:
                x_min = min(
                    time_rel[-last_60:]) if len(time_rel) >= last_60 else min(time_rel)
                x_max = max(
                    time_rel[-last_60:]) if len(time_rel) >= last_60 else max(time_rel)
                self.traffic_ax.set_xlim(x_min, x_max)

            # Redraw
            self.traffic_canvas.draw_idle()

        except Exception as e:
            print(f"Graph update error: {e}")

    def update_pie_chart(self):
        """Update traffic composition pie chart"""
        self.pie_ax.clear()
        self.pie_ax.set_facecolor('#2d3436')

        if len(self.traffic_data['sent_rate']) >= 10:
            # Calculate averages
            avg_sent = sum(list(self.traffic_data['sent_rate'])[-10:]) / 10
            avg_recv = sum(list(self.traffic_data['received_rate'])[-10:]) / 10
            total = avg_sent + avg_recv

            if total > 0:
                sizes = [avg_sent, avg_recv]
                colors = ['#ff4444', '#44ff44']
                labels = [f'Sent\n{self.format_bytes(avg_sent)}/s',
                          f'Received\n{self.format_bytes(avg_recv)}/s']

                # Create pie chart
                wedges, texts, autotexts = self.pie_ax.pie(
                    sizes, colors=colors, labels=labels, autopct='%1.1f%%',
                    startangle=90, explode=(0.05, 0), shadow=True,
                    textprops={'color': 'white', 'fontsize': 9}
                )

                # Style the wedges
                for wedge in wedges:
                    wedge.set_edgecolor('#1e1e1e')
                    wedge.set_linewidth(1)

                # Style the text
                for text in texts:
                    text.set_color('white')
                    text.set_fontsize(8)

                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(8)
                    autotext.set_fontweight('bold')

                self.pie_ax.set_title(' Traffic Composition', color='white',
                                      fontsize=11, pad=10, fontweight='bold')

        self.traffic_canvas.draw_idle()

    def update_connection_frequency(self):
        """Update connection frequency chart"""
        self.conn_ax.clear()
        self.conn_ax.set_facecolor('#2d3436')

        try:
            # Get connection stats from monitor
            if hasattr(self.app, 'monitor'):
                stats = self.app.monitor.get_traffic_stats()

                # Get top processes
                top_processes = stats.get('top_processes', [])[:8]

                if top_processes:
                    processes = [p[0][:15] for p in top_processes]
                    counts = [p[1]['total'] for p in top_processes]

                    # Create bar chart
                    bars = self.conn_ax.barh(processes, counts,
                                             color='#0984e3', alpha=0.8,
                                             edgecolor='white', linewidth=0.5)

                    # Add count labels
                    for i, (bar, count) in enumerate(zip(bars, counts)):
                        width = bar.get_width()
                        self.conn_ax.text(width + max(counts) * 0.01,
                                          bar.get_y() + bar.get_height()/2,
                                          f'{count}', va='center',
                                          color='white', fontsize=8)

                    self.conn_ax.set_xlabel(
                        'Connections', color='white', fontsize=9)
                    self.conn_ax.set_title(' Top Processes by Connections',
                                           color='white', fontsize=11, pad=10, fontweight='bold')
                    self.conn_ax.tick_params(colors='white', labelsize=8)
                    self.conn_ax.grid(
                        True, alpha=0.2, color='gray', linestyle='--', axis='x')
                    self.conn_ax.invert_yaxis()

        except Exception as e:
            print(f"Connection frequency error: {e}")

        self.traffic_canvas.draw_idle()

    def update_risk_distribution(self):
        """Update risk distribution chart"""
        self.risk_ax.clear()
        self.risk_ax.set_facecolor('#2d3436')

        try:
            # Get risk scores from risk engine
            if hasattr(self.app, 'risk_engine'):
                # Categorize risks
                risk_levels = ['Low (0-3)', 'Medium (3-6)',
                               'High (6-8)', 'Critical (8-10)']
                risk_counts = [0, 0, 0, 0]

                for ip_score in self.app.risk_engine.ip_scores.values():
                    score = ip_score.get('score', 0)
                    if score < 3:
                        risk_counts[0] += 1
                    elif score < 6:
                        risk_counts[1] += 1
                    elif score < 8:
                        risk_counts[2] += 1
                    else:
                        risk_counts[3] += 1

                # Create bar chart with gradient colors
                colors = ['#00ff00', '#ffff00', '#ff6600', '#ff0000']
                
                # Create x positions for the bars
                x_pos = range(len(risk_levels))
                
                bars = self.risk_ax.bar(x_pos, risk_counts, color=colors,
                                        alpha=0.8, edgecolor='white', linewidth=0.5)

                # Add count labels
                for bar, count in zip(bars, risk_counts):
                    height = bar.get_height()
                    if height > 0:
                        self.risk_ax.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                                          str(count), ha='center', va='bottom',
                                          color='white', fontsize=9, fontweight='bold')

                self.risk_ax.set_xlabel(
                    'Risk Level', color='white', fontsize=9)
                self.risk_ax.set_ylabel('IP Count', color='white', fontsize=9)
                self.risk_ax.set_title(' Risk Distribution', color='white',
                                       fontsize=11, pad=10, fontweight='bold')
                self.risk_ax.tick_params(colors='white', labelsize=8)
                self.risk_ax.grid(True, alpha=0.2, color='gray',
                                  linestyle='--', axis='y')
                
                # Set x-ticks with labels - this is the corrected way
                self.risk_ax.set_xticks(x_pos)
                self.risk_ax.set_xticklabels(risk_levels, rotation=15, ha='right')

        except Exception as e:
            print(f"Risk distribution error: {e}")

        self.traffic_canvas.draw_idle()

    def update_fallback_stats(self):
        """Update fallback text statistics"""
        try:
            net_io = psutil.net_io_counters()

            # Calculate rates
            current_sent = net_io.bytes_sent - self.last_bytes_sent
            current_recv = net_io.bytes_recv - self.last_bytes_recv
            self.last_bytes_sent = net_io.bytes_sent
            self.last_bytes_recv = net_io.bytes_recv

            # Update totals
            self.total_sent_bytes = net_io.bytes_sent
            self.total_recv_bytes = net_io.bytes_recv

            # Update peaks
            self.peak_sent = max(self.peak_sent, current_sent)
            self.peak_recv = max(self.peak_recv, current_recv)

            # Prepare stats text
            stats_text = f"""
    ╔══════════════════════════════════════╗
    ║     NETWORK TRAFFIC STATISTICS       ║
    ╠══════════════════════════════════════╣
    ║                                      ║
    ║  📤 Current Upload: {self.format_bytes(current_sent):>10}/s  ║
    ║  📥 Current Download: {self.format_bytes(current_recv):>8}/s  ║
    ║                                      ║
    ║  🚀 Peak Upload: {self.format_bytes(self.peak_sent):>13}/s  ║
    ║  🚀 Peak Download: {self.format_bytes(self.peak_recv):>11}/s  ║
    ║                                      ║
    ║  📊 Total Sent: {self.format_bytes(self.total_sent_bytes):>15}  ║
    ║  📊 Total Received: {self.format_bytes(self.total_recv_bytes):>12}  ║
    ║                                      ║
    ╚══════════════════════════════════════╝
    """

            self.fallback_stats.config(state=tk.NORMAL)
            self.fallback_stats.delete(1.0, tk.END)
            self.fallback_stats.insert(1.0, stats_text)
            self.fallback_stats.config(state=tk.DISABLED)

            # Schedule next update
            self.app.root.after(1000, self.update_fallback_stats)

        except Exception as e:
            print(f"Fallback stats error: {e}")

    def format_bytes(self, bytes_num):
        """Format bytes to human readable format"""
        if bytes_num == 0:
            return "0 B"

        units = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        while bytes_num >= 1024 and i < len(units) - 1:
            bytes_num /= 1024
            i += 1

        if i == 0:  # Bytes
            return f"{bytes_num:.0f} B"
        elif i <= 2:  # KB or MB
            return f"{bytes_num:.1f} {units[i]}"
        else:  # GB or TB
            return f"{bytes_num:.2f} {units[i]}"
