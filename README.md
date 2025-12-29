# Network Guard – Network Security Monitor

**Advanced Real-Time Network Security Scanner**  
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

**Network Guard** is a real-time network security monitoring application that continuously scans active network connections to identify and mitigate potential threats.

It combines multiple detection and analysis techniques, including:

- VirusTotal API reputation checks  
- IP geolocation analysis  
- Behavioral and port-based risk detection  

This multi-layered approach provides enhanced visibility and proactive protection against suspicious or malicious network activity.

---

## Key Features

- **Real-Time Network Monitoring**  
  Continuously scans all active inbound and outbound connections.

- **Intelligent Threat Detection**  
  Multi-layer risk scoring using VirusTotal reputation data, geolocation risk, and port analysis.

- **Automated Blocking**  
  Automatically blocks high-risk connections based on configurable thresholds.

- **Visual Dashboard**  
  Interactive world map with color-coded risk indicators.

- **Multi-Layer Blocking**  
  Block malicious activity by:
  - Process
  - IP address
  - Domain / website

- **Comprehensive Analytics**  
  Detailed traffic statistics, logs, and historical analysis.

- **Firewall Integration**  
  Automatic firewall rule creation when supported by the OS.

- **Cross-Platform Support**  
  Works on Windows, macOS, and Linux.

---

## Supported Operating Systems

| Operating System | Version              | Feature Support       | Notes |
|------------------|----------------------|-----------------------|-------|
| **Windows**      | 7, 8, 10, 11          | Full support          | Administrator privileges required for blocking |
| **macOS**        | 10.13+               | Most features         | Limited firewall integration |
| **Linux**        | Ubuntu 18.04+, Debian 10+, Fedora 32+ | Most features | Root required for some actions |

---

## Installation

### Prerequisites

- **Python 3.8 or newer**
- Active internet connection (VirusTotal + IP geolocation services)

---

### Step 1: Clone or Download

```bash
git clone https://github.com/yourusername/network-guard.git
cd network-guard
```

## Usage
- **Main Dashboard** — Live network map and connection monitor
- **Traffic Analytics** — Network statistics and visual graphs
- **Blocking Controls** — Block processes, IPs, and websites
- **Advanced Control** — Firewall rules and event logs

## Configuration
Obtain free API keys from:
[virustotal](https://www.virustotal.com/)
Edit settings.py:

```python
VIRUSTOTAL_API_KEYS = [
    "your_api_key_1",
    "your_api_key_2",
    "your_api_key_3"
]
```
Using multiple API keys helps avoid rate limits.
