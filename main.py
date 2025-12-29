#!/usr/bin/env python3
"""
Network Guard - Main Application Entry Point
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import SimpleNetworkGuard
from utils.logger import log

if __name__ == "__main__":
    print("=" * 60)
    print("Network Guard - Malware Blocker Edition") 
    print("Continuous Scanning & Blocking Mode")
    print("=" * 60)
    
    # Check if running as admin/root for full blocking
    import platform
    if platform.system() == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print("⚠️ Warning: Not running as administrator.")
                print("💡 Run as admin for full website blocking capabilities.")
        except:
            pass
    
    print("=" * 60)
    print("Starting malware detection and blocking system...")
    print("Auto-blocking: ENABLED")
    print("=" * 60)
    
    try:
        app = SimpleNetworkGuard()
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")