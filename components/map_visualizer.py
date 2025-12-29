"""
Map visualization component
"""

import tkinter as tk
from typing import Optional

# Try to import optional packages
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False

class MapVisualizer:
    def __init__(self):
        self.fig: Optional[Figure] = None
        self.ax = None
        self.canvas: Optional[FigureCanvasTkAgg] = None
        self.connection_lines = []
        self.ip_positions = {}
        
    def create_map(self, parent: tk.Widget) -> tk.Widget:
        """Create map visualization"""
        try:
            if CARTOPY_AVAILABLE:
                return self.create_globe_map(parent)
            else:
                return self.create_simple_map(parent)
        except Exception as e:
            print(f"Map creation error: {e}")
            return self.create_fallback_map(parent)
    
    def create_globe_map(self, parent: tk.Widget) -> tk.Widget:
        """Create globe map with cartopy"""
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        
        # Set globe extent
        self.ax.set_global()
        
        # Add map features
        self.ax.add_feature(cfeature.LAND, facecolor='#2d3436', alpha=0.8)
        self.ax.add_feature(cfeature.OCEAN, facecolor='#0984e3', alpha=0.5)
        self.ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor='white')
        self.ax.add_feature(cfeature.BORDERS, linewidth=0.3, edgecolor='gray', alpha=0.5)
        
        # Add gridlines
        gl = self.ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
        gl.xlabels_top = False
        gl.ylabels_right = False
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        widget = self.canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)
        
        return widget
    
    def create_simple_map(self, parent: tk.Widget) -> tk.Frame:
        """Create simple map using matplotlib"""
        frame = tk.Frame(parent, bg='#2d3436')
        
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Draw simple continents
        continents = {
            'NA': (-130, -60, 20, 70),
            'SA': (-80, -35, -55, 12),
            'EU': (-10, 40, 35, 70),
            'AF': (-20, 50, -35, 35),
            'AS': (40, 150, 10, 70),
            'AU': (110, 155, -45, -10)
        }
        
        for name, (x1, x2, y1, y2) in continents.items():
            self.ax.fill([x1, x2, x2, x1], [y1, y1, y2, y2], color='#2d3436', alpha=0.7)
        
        self.ax.set_xlim(-180, 180)
        self.ax.set_ylim(-90, 90)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('#0984e3')
        self.ax.set_title('🌍 Network Connections', color='white', fontsize=10)
        self.ax.grid(True, alpha=0.3, color='gray')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return frame
    
    def create_fallback_map(self, parent: tk.Widget) -> tk.Frame:
        """Create fallback text display"""
        frame = tk.Frame(parent, bg='#2d3436')
        label = tk.Label(frame, text="🌍 Map visualization\nInstall: pip install cartopy", 
                       bg='#2d3436', fg='white', font=('Arial', 10))
        label.pack(expand=True)
        return frame
    
    def update_connection(self, remote_lat: float, remote_lon: float, risk_level: float = 0):
        """Update map with a new connection"""
        if not self.ax:
            return
        
        try:
            # Convert risk level to color
            if risk_level >= 8:
                color = '#ff0000'
                linewidth = 2
            elif risk_level >= 6:
                color = '#ff6600'
                linewidth = 1.5
            elif risk_level >= 4:
                color = '#ffff00'
                linewidth = 1
            else:
                color = '#00ff00'
                linewidth = 0.5
            
            # Draw connection line
            line = self.ax.plot([0, remote_lon], [0, remote_lat], 
                              color=color, linewidth=linewidth, alpha=0.7)[0]
            self.connection_lines.append(line)
            
            # Draw endpoint marker
            self.ax.scatter(remote_lon, remote_lat, s=30, color=color, 
                          edgecolor='white', linewidth=1, zorder=10)
            
            # Redraw
            self.canvas.draw()
            
            # Keep only last 50 connections
            if len(self.connection_lines) > 50:
                old_line = self.connection_lines.pop(0)
                old_line.remove()
                
        except Exception as e:
            print(f"Map update error: {e}")