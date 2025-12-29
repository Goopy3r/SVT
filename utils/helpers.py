"""
Helper functions and utilities
"""

import socket
import re
from typing import Optional

def validate_ip(ip: str) -> bool:
    """Validate IP address format"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def format_bytes(bytes_num: int) -> str:
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

def is_valid_domain(domain: str) -> bool:
    """Validate domain name format"""
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return bool(re.match(pattern, domain))