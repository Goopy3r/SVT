fully update all the code and make this better in the .md format and lague :

\# Network Guard – Network Security Monitor

\*\*Advanced Real-Time Network Security Scanner\*\* — A comprehensive network monitoring tool that detects, analyzes, and blocks malicious network activity.

⚠️ \*\*Use only on systems you own or are explicitly authorized to monitor.\*\*

\---

\## Table of Contents

\- \[Overview\](#overview)

\- \[Key Features\](#key-features)

\- \[Supported Operating Systems\](#supported-operating-systems)

\- \[Installation\](#installation)

\- \[Usage\](#usage)

\- \[Configuration\](#configuration)

\- \[OS-Specific Notes\](#os-specific-notes)

\- \[Troubleshooting\](#troubleshooting)

\- \[Important Notes & Legal\](#important-notes--legal)

\---

\## Overview

\*\*Network Guard\*\* is a real-time network security monitoring application that actively scans, detects, and blocks malicious network connections on your system. It combines multiple detection methods including:

\- VirusTotal API integration

\- Geolocation analysis

\- Behavioral and port-based risk detection

to provide comprehensive threat protection.

\---

\## Key Features

\- \*\*Real-time Network Monitoring\*\* — Continuous scanning of all active network connections

\- \*\*Intelligent Threat Detection\*\* — Multi-layer risk scoring using VirusTotal, geolocation, and port analysis

\- \*\*Automated Blocking\*\* — Automatically blocks high-risk connections based on configurable thresholds

\- \*\*Visual Dashboard\*\* — Interactive world map with color-coded risk indicators

\- \*\*Multi-Layer Blocking\*\* — Process, IP address, and website blocking

\- \*\*Comprehensive Analytics\*\* — Detailed traffic statistics and logs

\- \*\*Firewall Integration\*\* — Automatic firewall rule creation

\- \*\*Cross-Platform Support\*\* — Windows, macOS, and Linux

\---

\## Supported Operating Systems

| OS | Version | Features | Notes |

|----|--------|----------|------|

| \*\*Windows\*\* | 7, 8, 10, 11 | Full feature support | Admin required for website blocking |

| \*\*macOS\*\* | 10.13+ | Most features supported | Limited firewall integration |

| \*\*Linux\*\* | Ubuntu 18.04+, Debian 10+, Fedora 32+ | Most features supported | Root required for some features |

\---

\## Installation

\### Prerequisites

\- \*\*Python 3.8+\*\*

\- Active internet connection (VirusTotal + geolocation)

\---

\### Step 1: Clone or Download

\`\`\`bash

git clone https://github.com/yourusername/network-guard.git

cd network-guard

\# Required dependencies

pip install psutil requests

\# Optional (enhanced visuals)

pip install matplotlib numpy cartopy

\# Run Command Prompt or PowerShell as Administrator

python main.py

\`\`\`

\## macOS

\`\`\`bash

brew install python-tk

python main.py

\`\`\`

\## Linux (Fedora / RHEL)

\`\`\`bash

sudo dnf install python3-tkinter

pip install psutil requests

python main.py

\`\`\`

GUI Interface

Main Dashboard — Live map and connection monitor

Traffic Analytics — Statistics and graphs

Blocking Controls — Block processes, IPs, and websites

Blocked Items — View and manage blocked entities

Advanced Controls — Firewall rules and logs

Monitoring Flow

Application starts scanning automatically

Suspicious connections are flagged with risk levels

High-risk connections are blocked (if enabled)

Analytics are available in the Traffic tab

Configuration

VirusTotal API Keys

Obtain free API keys from:

https://www.virustotal.com/

Edit settings.py:

VIRUSTOTAL\_API\_KEYS = \[

"your\_api\_key\_1",

"your\_api\_key\_2",

"your\_api\_key\_3"

\]

Custom Settings (settings.py)

KNOWN\_SAFE — Trusted processes

SUSPICIOUS\_PORTS — Ports flagged as suspicious

COUNTRY\_RISKS — Risk scores per country

RISK\_WEIGHTS — Detection weighting

GUI Settings

Auto-blocking thresholds

Country-based filtering

Performance tuning

OS-Specific Notes

Windows

Administrator privileges required

Automatic Windows Firewall integration

Hosts file modification requires elevation

Antivirus false positives possible

macOS

Gatekeeper warnings may appear

Limited firewall support

Script permissions may be required

Linux

Root privileges required for website blocking

Firewall commands vary by distro

SELinux/AppArmor may require adjustments

DNS cache flushing varies

Troubleshooting

Common Issues

Missing Modules

pip install psutil requests

Permission Errors (Windows)

Run Command Prompt as Administrator

VirusTotal API Limits

Free tier: 4 requests per minute

Use multiple API keys

Paid API recommended for heavy use

Map Not Displaying

pip install cartopy

High CPU Usage

Reduce scan interval

Limit CPU usage in settings

Close unused tabs

Error Reference

ErrorSolution

Permission deniedRun as Administrator / root

tkinter not foundInstall python3-tk / python-tk

No API keysAdd keys to settings.py

Firewall rule failedCheck firewall permissions

Important Notes & Legal

Legal Disclaimer

Authorization Required — Monitor only systems you own or have permission to monitor

Privacy Laws — Comply with GDPR, CCPA, and local laws

VirusTotal TOS — Follow API usage rules

Security Considerations

Keep API keys secure

Logs may contain sensitive IP data

False positives are possible

Performance Notes

Real-time scanning uses CPU/RAM

Minimal network overhead

Logs consume disk space

Support

Report issues via GitHub

Keep software updated

Read documentation and code comments

⚠️ WARNING:

Unauthorized network monitoring may violate local, state, or federal law.

Always obtain proper authorization before using this tool.
