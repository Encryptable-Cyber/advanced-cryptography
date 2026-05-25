# Lab 4 — Cryptanalysis and Attacks
## Man-in-the-Middle (MITM), Session Hijacking, HTTPS Security, and ARP Spoofing Defense

---

# Overview

This laboratory exercise focused on practical cryptographic attack techniques and defensive countermeasures within a controlled virtualized environment using Kali Linux and Ubuntu Server.

The lab demonstrated how attackers can intercept insecure network communications, steal credentials transmitted over HTTP, hijack authenticated user sessions using stolen cookies, and analyze the security differences between HTTP and HTTPS protocols.

The exercise also explored defensive mechanisms such as ARP spoofing detection, encrypted communication with TLS/HTTPS, and static ARP table protection.

---

# Objectives

The primary objectives of this lab were:

- Perform Man-in-the-Middle (MITM) attacks using ARP spoofing
- Capture plaintext HTTP credentials from intercepted traffic
- Demonstrate session hijacking using stolen session cookies
- Compare HTTP and HTTPS traffic visibility
- Analyze TLS encryption behavior
- Detect ARP spoofing activity
- Implement defenses against ARP spoofing attacks

---

# Skills Demonstrated

- ARP Spoofing
- Packet Sniffing
- Credential Interception
- Session Hijacking
- HTTP/HTTPS Analysis
- TLS Encryption Analysis
- Web Application Security Testing
- Network Traffic Inspection
- Security Hardening
- Defensive Network Monitoring

---

# Technologies and Tools Used

| Category | Technology |
|---|---|
| Operating System | Kali Linux 2025.4 |
| Operating System | Ubuntu Server 24.04 |
| MITM Framework | Bettercap |
| MITM Framework | Ettercap |
| Packet Capture | tcpdump |
| Encryption | OpenSSL |
| HTTP Client | curl |
| Network Monitoring | arpwatch |
| Scripting | Python 3 |
| Shell Scripting | Bash |
| Virtualization | Oracle VirtualBox |

---

# Virtual Lab Environment

The lab environment consisted of two virtual machines connected on the same bridged network.

| Machine | Role | IP Address |
|---|---|---|
| Kali Linux | Attacker | 192.168.1.32 |
| Ubuntu Server | Victim / Target | 192.168.1.67 |
| Gateway | Router | 192.168.1.1 |

---

# Attack Scenarios Performed

## 1. HTTP Credential Interception

A vulnerable HTTP login application was deployed on Ubuntu Server.

Using Bettercap and tcpdump, plaintext credentials transmitted through HTTP POST requests were intercepted successfully.

Example captured credentials:

```http
user=httpuser&pass=httppassword123
```

---

## 2. Session Hijacking

A session-enabled web application generated session cookies after successful login.

The session cookie was intercepted:

```http
Set-Cookie: sessionid=4fe8b4b5-2b9e-4dba-b058-17529c0dbd41
```

The stolen cookie was replayed using curl:

```bash
curl -H "Cookie: sessionid=4fe8b4b5-2b9e-4dba-b058-17529c0dbd41" \
http://192.168.1.67:8080/dashboard
```

Authenticated access was granted without requiring credentials, proving successful session hijacking.

---

## 3. HTTPS Security Demonstration

A self-signed TLS certificate was generated using OpenSSL and an HTTPS server was configured.

Traffic analysis demonstrated:

| Protocol | Result |
|---|---|
| HTTP | Credentials visible |
| HTTPS | Credentials encrypted |

HTTPS traffic appeared as encrypted binary data instead of readable plaintext.

---

## 4. ARP Spoofing Detection and Prevention

The lab demonstrated:
- ARP cache inspection
- ARP spoofing detection using arpwatch
- Static ARP entry creation
- Prevention of ARP poisoning attacks

Static ARP entries prevented unauthorized MAC address modification.

---

# Folder Structure

The `lab4/` directory is organized into multiple sections containing captures, scripts, reports, screenshots, and vulnerable server files.

```text
lab4/
├── captures/
│   └── https_comparison.pcap
│
├── reports/
│   ├── lab4_report.md
│   └── screenshots/
│       ├── Screenshot_00_ping&directories_created.png
│       ├── Screenshot_01_web_server_files.png
│       ├── Screenshot_02_bettercap_version.png
│       ├── Screenshot_03_kali_ips.png
│       ├── Screenshot_04_web_server_test.png
│       ├── Screenshot_05_ip_forwarding.png
│       ├── Screenshot_06_gateway_ip.png
│       ├── Screenshot_07_web_server_restarted.png
│       ├── Screenshot_08_kali_curl_test.png
│       ├── Screenshot_09_ip_forwarding.png
│       ├── Screenshot_10_bettercap_correct_interface.png
│       ├── Screenshot_11_captured_credentials.png
│       ├── Screenshot_12_ettercap_installed.png
│       ├── Screenshot_13_session_hijack_script.png
│       ├── Screenshot_14_session_server_running.png
│       ├── Screenshot15_ettercap_credentials.png
│       ├── Screenshot_16_session_hijacking_success.png
│       ├── Screenshot_17_self_signed_certificate.png
│       ├── Screenshot_18_https_server_running.png
│       ├── Screenshot19_http_credentials_visible.png
│       ├── Screenshot_20_https_no_credentials_visible.png
│       ├── Screenshot_21_https_connection.png
│       ├── Screenshot_22_two_servers_running.png
│       ├── Screenshot_23_http_credentials_captured.png
│       ├── Screenshot_24_https_encrypted_no_credentials.png
│       ├── Screenshot_25_https_server_received.png
│       ├── Screenshot_26_arpwatch_installed.png
│       └── Screenshot_27_anti_arp_spoof_script.png
│
├── scripts/
│   ├── anti_arp_spoof.sh
│   └── session_hijack.js
│
├── server/
│   ├── cert.pem
│   ├── https_server.py
│   ├── key.pem
│   ├── login_handler.py
│   ├── login.html
│   └── session_server.py
│
└── README.md
```

---

# Directory Descriptions

## captures/

Contains packet captures and traffic analysis files used during HTTP vs HTTPS comparison testing.

---

## reports/

Contains the complete laboratory documentation and all screenshots collected during practical execution.

### reports/screenshots/

Contains evidence of:
- ARP spoofing
- Bettercap execution
- Credential interception
- HTTPS encryption analysis
- Session hijacking
- ARP spoofing defense implementation

---

## scripts/

Contains attack and defense automation scripts.

### Included Scripts

| Script | Purpose |
|---|---|
| session_hijack.js | Bettercap session hijacking script |
| anti_arp_spoof.sh | Static ARP spoofing prevention script |

---

## server/

Contains vulnerable web applications and HTTPS server implementations used during testing.

### Included Server Files

| File | Purpose |
|---|---|
| login.html | Vulnerable login page |
| login_handler.py | Basic HTTP credential logger |
| session_server.py | Session-enabled HTTP server |
| https_server.py | HTTPS/TLS secured server |
| cert.pem | Self-signed TLS certificate |
| key.pem | TLS private key |

---

# Key Security Findings

| Security Issue | Impact |
|---|---|
| HTTP transmits credentials in plaintext | Credential theft |
| Session cookies can be replayed | Account hijacking |
| ARP spoofing enables MITM attacks | Traffic interception |
| HTTPS encrypts traffic | Prevents credential exposure |
| Static ARP entries mitigate spoofing | Network protection |

---

# Defensive Measures Demonstrated

- HTTPS/TLS encryption
- Secure session management
- ARP monitoring with arpwatch
- Static ARP entries
- Network traffic inspection
- Defense-in-depth security approach

---

# Lessons Learned

- HTTP should never be used for authentication systems.
- Session cookies are sensitive authentication tokens.
- HTTPS is essential for modern web security.
- ARP spoofing remains dangerous on local networks.
- Proper encryption significantly reduces attack success.
- Detection and prevention mechanisms must work together.

---

# Academic Context

This lab was completed as part of:

**Course:** Advanced Cryptography (CYBE6229)

The exercise provided practical exposure to:
- network-level attacks,
- cryptographic protections,
- authentication weaknesses,
- and modern defensive security controls.

---

# Disclaimer

This repository was created strictly for educational and authorized laboratory purposes within a controlled environment.

The techniques demonstrated here should never be used against systems or networks without explicit authorization.

---

# Author

Advanced Cryptography (CYBE6229) Laboratory Exercise  
Virtual Security Lab Environment  
Kali Linux + Ubuntu Server
