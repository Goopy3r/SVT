# SVT – System Visibility & Threats

**Advanced Real-Time System Visibility & Threats**  
A comprehensive network monitoring tool designed to detect, analyze, and block malicious network activity in real time.

⚠️ **Use only on systems you own or are explicitly authorized to monitor.**

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Supported Operating Systems](#supported-operating-systems)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [OS-Specific Notes](#os-specific-notes)
- [Troubleshooting](#troubleshooting)
- [Important Notes & Legal](#important-notes--legal)

---

## Overview

**System Visibility & Threats** is a real-time network security monitoring application that continuously scans active network connections to identify and mitigate potential threats.

It combines multiple detection and analysis techniques, including:

- VirusTotal API reputation checks  
- IP geolocation analysis  
- Behavioral and port-based risk detection  

This multi-layered approach provides enhanced visibility and proactive protection against suspicious or malicious network activity.

---

## Key Features

- **Real-Time Network Monitoring** — Continuous scanning of active connections  
- **Intelligent Threat Detection** — Multi-layer risk scoring  
- **Automated Blocking** — Configurable auto-blocking of high-risk traffic  
- **Visual Dashboard** — Interactive world map with risk indicators  
- **Multi-Layer Blocking** — Process, IP, and domain blocking  
- **Comprehensive Analytics** — Detailed traffic statistics and logs  
- **Firewall Integration** — Automatic firewall rule creation  
- **Cross-Platform Support** — Windows, macOS, and Linux  

---

## Supported Operating Systems

| OS | Version | Feature Support | Notes |
|----|--------|-----------------|-------|
| **Windows** | 7, 8, 10, 11 | Full support | Admin required |
| **macOS** | 10.13+ | Most features | Limited firewall |
| **Linux** | Ubuntu 18.04+, Debian 10+, Fedora 32+ | Most features | Root required |

---

## Installation

### Prerequisites

- Python 3.8+
- Active internet connection

### Clone Repository

```bash
git clone https://github.com/yourusername/network-guard.git
cd network-guard
```

### Install Dependencies

```bash
pip install psutil requests
pip install matplotlib numpy cartopy
```

### Run

```bash
python main.py
```

---

## Usage

- Live dashboard monitoring
- Traffic analytics and graphs
- Blocking controls for IPs, domains, and processes
- Firewall and log management

---

## Configuration

### VirusTotal API Keys

Edit `settings.py`:

```python
VIRUSTOTAL_API_KEYS = [
    "your_api_key_1",
    "your_api_key_2"
]
```

### Custom Settings

- KNOWN_SAFE
- SUSPICIOUS_PORTS
- COUNTRY_RISKS
- RISK_WEIGHTS

---

## OS-Specific Notes

### Windows
- Requires Administrator privileges
- Firewall and hosts file integration

### macOS
- Gatekeeper warnings possible
- Limited firewall control

### Linux
- Root privileges required
- SELinux/AppArmor may require adjustments

---

## Troubleshooting

| Issue | Solution |
|------|----------|
| Missing modules | `pip install psutil requests` |
| Permission denied | Run as admin/root |
| API limit reached | Use multiple keys |
| Map not loading | Install `cartopy` |

---

## Important Notes & Legal

- Authorization is required
- Comply with privacy laws
- Secure your API keys

⚠️ **Unauthorized monitoring may be illegal.** (maybe)
