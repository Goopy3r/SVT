# Network Guard – Network Security Monitor

**Advanced Real-Time Network Security Scanner** — A comprehensive network monitoring tool that detects, analyzes, and blocks malicious network activity.  
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

Network Guard is a real-time network security monitoring application that actively scans, detects, and blocks malicious network connections on your system. It combines multiple detection methods including VirusTotal API integration, geolocation analysis, and behavioral pattern recognition to provide comprehensive threat protection.

---

## Key Features

- **Real-time Network Monitoring** – Continuous scanning of all active network connections  
- **Intelligent Threat Detection** – Multi-layer risk scoring using VirusTotal, geolocation, and port analysis  
- **Automated Blocking** – Automatic blocking of high-risk connections based on configurable thresholds  
- **Visual Dashboard** – Interactive world map showing connection origins with color-coded risk levels  
- **Multi-Layer Blocking** – Process, IP address, and website blocking capabilities  
- **Comprehensive Analytics** – Detailed traffic statistics and connection logs  
- **Firewall Integration** – Automatic firewall rule creation for blocked IPs  
- **Cross-Platform Support** – Works on Windows, macOS, and Linux  

---

## Supported Operating Systems

| OS      | Version                                   | Features                | Notes                                   |
|--------|--------------------------------------------|-------------------------|-----------------------------------------|
| Windows | 7, 8, 10, 11                              | Full feature support    | Admin required for website blocking     |
| macOS   | 10.13+                                   | Most features supported | Limited firewall integration            |
| Linux   | Ubuntu 18.04+, Debian 10+, Fedora 32+     | Most features supported | Root needed for some operations         |

---

## Installation

### Prerequisites

- Python **3.8 or higher**
- Internet connection (for VirusTotal API and geolocation)

---

### Step 1: Clone / Download

```bash
git clone https://github.com/yourusername/network-guard.git
cd network-guard
