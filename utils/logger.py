"""
Logging utilities
"""

from datetime import datetime
from settings import LOG_FILE

def log(msg, level="INFO"):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    full_msg = f"{timestamp} | {level} | {msg}"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")
    
    print(full_msg)