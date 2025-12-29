"""
Application settings and constants
"""

import platform 

# API Keys (Note: These are example keys - use your own)
VIRUSTOTAL_API_KEYS = [
    "aeb7a5459d0a64a13fc25d0478a3f330f6f816bba6a96e51c9589aa4f596c3cb",
    "6296a333da44f94e2ad8804c724aaca64e613f831287fee907136441fad80d0e",
    "e0f1019a4dd01f10499c804f41bc7b5b03764733a3956cd12525884668f5ca43"
]

# File paths
LOG_FILE = "network_guard.log"
BLOCKED_PROCESSES_FILE = "blocked_processes.json"
BLOCKED_IPS_FILE = "blocked_ips.json"
HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts" if platform.system() == "Windows" else "/etc/hosts"

# Known safe processes
KNOWN_SAFE = {
    "chrome.exe", "firefox.exe", "msedge.exe", "system", 
    "svchost.exe", "explorer.exe", "python.exe", "pythonw.exe",
    "code.exe", "notepad.exe", "cmd.exe", "powershell.exe"
}

# Suspicious patterns
SUSPICIOUS_PORTS = {
    23, 4444, 1337, 6667, 31337, 12345, 1243, 5554,
    9999, 10000, 6666, 6665, 8080, 81, 82, 83, 84,
    85, 86, 87, 88, 89, 8000, 8001, 9000, 9001,
    3389, 5900, 5901, 22, 21, 25, 110, 143, 445
}

# Risk scoring weights
RISK_WEIGHTS = {
    "vt_malicious": 0.25,
    "vt_suspicious": 0.15,
    "suspicious_port": 0.15,
    "suspicious_process": 0.10,
    "behavior_anomaly": 0.15,
    "domain_age": 0.05,
    "geo_risk": 0.05,
    "connection_frequency": 0.05,
    "data_volume": 0.05
}

# Country risk scores
COUNTRY_RISKS = {
    "CN": 0.8, "RU": 0.7, "IR": 0.7, "KP": 0.9,
    "US": 0.1, "GB": 0.1, "DE": 0.1, "CA": 0.1,
    "AU": 0.1, "JP": 0.1, "FR": 0.1, "BR": 0.2,
    "IN": 0.2, "UA": 0.4, "BY": 0.5, "SY": 0.8,
    "VN": 0.6, "TH": 0.3, "TR": 0.4, "PK": 0.7
}