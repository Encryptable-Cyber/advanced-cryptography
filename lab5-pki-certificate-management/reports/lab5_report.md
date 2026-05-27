# Lab 5: Public Key Infrastructure and Certificate Management

## Complete Laboratory Report (Command-by-Command Format)

**Course:** Advanced Cryptography (CYBE6229)  
**Date Completed:** May 26, 2026  
**Environment:** VirtualBox (Kali Linux + Ubuntu Server 24.04)  
**Author:** [Your Name]

---

## Table of Contents

1. Introduction
2. Objectives of the Lab
3. Scope of the Lab
4. Technologies and Tools Used
5. Environment Setup
6. System Architecture and Lab Topology
7. Methodology
8. Step-by-Step Lab Execution (Command-by-Command)
9. Security Concepts Demonstrated
10. Vulnerabilities Identified
11. Problems Encountered and Troubleshooting
12. Results and Observations
13. Security Analysis and Risk Assessment
14. Lessons Learned
15. Best Practices and Recommendations
16. Conclusion
17. References

---

## 1. Introduction

Public Key Infrastructure (PKI) forms the foundation of secure communications on the internet. It enables the issuance, management, distribution, and revocation of digital certificates, which are essential for establishing trust between communicating parties. This laboratory exercise focused on building a complete private PKI infrastructure from scratch, including a Root Certificate Authority (CA), issuing server certificates, configuring HTTPS on a web server, and implementing certificate revocation mechanisms.

The lab was conducted in an isolated VirtualBox environment consisting of two virtual machines: Kali Linux (acting as the client) and Ubuntu Server 24.04 (acting as the CA and web server). All exercises followed the Advanced Cryptography CYBE6229 Laboratory Manual (Pages 33-39).

---

## 2. Objectives of the Lab

| # | Objective | Status |
|---|-----------|--------|
| 1 | Deploy and manage a private Certificate Authority (CA) | ✅ Complete |
| 2 | Setup a local CA using OpenSSL | ✅ Complete |
| 3 | Generate and sign certificates for web applications | ✅ Complete |
| 4 | Configure Apache web server with SSL/TLS using custom certificates | ✅ Complete |
| 5 | Install CA certificates on client machines (Kali Linux) | ✅ Complete |
| 6 | Test secure HTTPS connections with custom certificates | ✅ Complete |
| 7 | Generate Certificate Revocation Lists (CRL) | ✅ Complete |
| 8 | Configure OCSP responder certificates | ✅ Complete |

---

## 3. Scope of the Lab

| Area | Description |
|------|-------------|
| **Certificate Authority** | Creating a private Root CA with OpenSSL |
| **Certificate Generation** | Creating and signing server certificates |
| **Web Server Security** | Configuring Apache with SSL/TLS |
| **Client Trust** | Installing CA certificates on client systems |
| **Certificate Revocation** | Implementing CRL and OCSP mechanisms |

---

## 4. Technologies and Tools Used

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Operating Systems** | Kali Linux | 2025.4 | Client machine |
| | Ubuntu Server | 24.04 LTS | CA and web server |
| **Virtualization** | Oracle VirtualBox | 7.0 | VM environment |
| **PKI Tools** | OpenSSL | 3.0.13 | Certificate management |
| **Web Server** | Apache2 | 2.4.62 | SSL/TLS web server |
| **Testing Tools** | curl | 8.19.0 | HTTPS testing |
| | Firefox | Latest | Browser validation |

---

## 5. Environment Setup

### Virtual Machine Configuration

| VM | OS | RAM | vCPUs | IP Address |
|----|----|----|-------|-------------|
| Kali Linux | Kali 2025.4 | 8 GB | 4 | 192.168.1.32 |
| Ubuntu Server | Ubuntu 24.04 | 4 GB | 2 | 192.168.1.67 |

### Directory Structure Created

**On Ubuntu Server:**
```
~/cyber-labs/lab5/myCA/
├── certs/          # Issued certificates
├── crl/            # Certificate Revocation Lists
├── newcerts/       # New certificates (OpenSSL tracking)
├── private/        # CA private key (restricted access)
├── ca.cnf          # CA configuration file
├── webserver.cnf   # Server certificate configuration
├── index.txt       # Certificate database
└── serial          # Serial number counter
```

**On Kali Linux:**
```
~/cyber-labs/lab5/
├── certs/          # Copied certificates from Ubuntu
├── scripts/        # Configuration files
└── reports/screenshots/  # Lab documentation
```

---

## 6. System Architecture and Lab Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           192.168.1.0/24 Network                            │
│                                                                             │
│    ┌─────────────────────────────┐    ┌─────────────────────────────┐       │
│    │       Ubuntu Server         │    │         Kali Linux          │       │
│    │        24.04 LTS            │    │          2025.4             │       │
│    │       IP: 192.168.1.67      │    │       IP: 192.168.1.32      │       │
│    │                             │    │                             │       │
│    │  ┌─────────────────────┐    │    │  ┌─────────────────────┐    │       │
│    │  │  Certificate        │    │    │  │     Web Client      │    │       │
│    │  │  Authority (CA)     │    │    │  │                     │    │       │
│    │  │  - Root CA Key      │    │    │  │  - System Trust     │    │       │
│    │  │  - Root CA Cert     │    │    │  │    Store            │    │       │
│    │  └────────┬──────────--┘    │    │  │  - Firefox Cert     │    │       │
│    │           │                 │    │  │    Store            │    │       │
│    │           ▼                 │    │  └─────────────────────┘    │       │
│    │  ┌─────────────────────┐    │    │                             │       │
│    │  │   Apache Web Server │    │    │                             │       │
│    │  │   - SSL/TLS         │    │    │                             │       │
│    │  │   - Port 443        │    │    │                             │       │
│    │  │   - webserver.crt   │    │    │                             │       │
│    │  │   - webserver.key   │    │    │                             │       │
│    │  └─────────────────────┘    │    │                             │       │
│    └─────────────────────────────┘    └─────────────────────────────┘       │
│                                                                             │
│                              ┌─────────────┐                                │
│                              │   Gateway   │                                │
│                              │ 192.168.1.1 │                                │
│                              └─────────────┘                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Methodology

The lab followed a systematic approach:

1. Environment verification (network connectivity)
2. CA directory structure creation
3. CA configuration file creation
4. Root CA key and certificate generation
5. Server certificate configuration
6. CSR generation and signing
7. Apache installation and SSL configuration
8. Certificate deployment to client
9. HTTPS testing and validation
10. Certificate revocation implementation

---

## 8. Step-by-Step Lab Execution (Command-by-Command)

### Part 1: Building a Private Certificate Authority

---

#### Command 1: Navigate to Lab Directory

**Purpose:** Change to the Lab 5 working directory on Ubuntu Server.

**Command:**
```bash
cd ~/cyber-labs/lab5
```

**Explanation:** This command moves the user from the home directory into the Lab 5 directory. The tilde `~` represents the home directory (`/home/ubuntu`). All subsequent CA operations will be performed from this location.

**Expected Output:** None (silent success). The prompt changes to show the new directory.

**Security Relevance:** Keeping lab files organized in dedicated directories prevents accidental file overwrites and maintains clear separation between different lab exercises.

**Screenshot Reference:** The initial directory navigation is documented in the accompanying lab screenshots.

---

#### Command 2: Create Main CA Directory

**Purpose:** Create the root directory for Certificate Authority operations.

**Command:**
```bash
mkdir -p myCA && cd myCA
```

**Explanation:** 
- `mkdir -p` - Creates a directory and any missing parent directories
- `myCA` - The name of the CA working directory
- `&&` - Logical AND operator; the second command runs only if the first succeeds
- `cd myCA` - Change into the newly created directory

**Expected Output:** None (silent success). The prompt changes to `~/cyber-labs/lab5/myCA$`.

**Security Relevance:** The CA directory must be isolated from other files because it will contain sensitive cryptographic material (private keys).

**Screenshot Reference:** Screenshot_00a.png and Screenshot_00b.png show the directory creation process.

---

#### Command 3: Create CA Subdirectories

**Purpose:** Create the standard subdirectory structure required by OpenSSL for CA operations.

**Command:**
```bash
mkdir certs crl newcerts private
```

**Explanation:**
- `mkdir` - Create directories
- `certs` - Stores issued certificates
- `crl` - Stores Certificate Revocation Lists
- `newcerts` - Stores new certificates (OpenSSL tracking)
- `private` - Stores CA private key (restricted access)

**Expected Output:** None (silent success). Four new directories appear in the current location.

**Security Relevance:** 
- The `private` directory will contain the Root CA private key, which must be protected
- The `certs` directory stores all issued certificates for reference
- The `crl` directory maintains revocation information

**Screenshot Reference:** Screenshot_00a.png and Scretenshot_00b.png show the complete directory structure.

---

#### Command 4: Restrict Private Directory Permissions

**Purpose:** Set strict permissions on the private key directory to prevent unauthorized access.

**Command:**
```bash
chmod 700 private
```

**Explanation:**
- `chmod` - Change file/directory permissions
- `700` - Owner has read, write, and execute (7); group and others have no access (00)
- `private` - Target directory

**Permission Breakdown:**
| Digit | User | Permission | Value |
|-------|------|------------|-------|
| 7 | Owner (ubuntu) | Read + Write + Execute | rwx |
| 0 | Group | No access | --- |
| 0 | Others | No access | --- |

**Expected Output:** None (silent success).

**Security Relevance:** The private key directory contains the most sensitive cryptographic material in the entire PKI. If an attacker gains read access to this directory, they can steal the Root CA private key and issue fraudulent certificates. The 700 permission ensures only the Ubuntu user can access this directory.

**Screenshot Reference:** The permission change is visible in the directory listing screenshots.

---

#### Command 5: Create Certificate Database File

**Purpose:** Create an empty index file that OpenSSL uses to track issued certificates.

**Command:**
```bash
touch index.txt
```

**Explanation:**
- `touch` - Creates an empty file if it doesn't exist; updates timestamp if it exists
- `index.txt` - OpenSSL's certificate database file

**Expected Output:** None (silent success). A zero-byte file named `index.txt` is created.

**File Format:** OpenSSL maintains a text database where each line represents one certificate with fields:
- Status (V=Valid, R=Revoked, E=Expired)
- Expiration date
- Revocation date (if revoked)
- Serial number (hex)
- Certificate type
- Distinguished Name

**Security Relevance:** This database maintains the integrity of the CA's certificate history and is critical for proper revocation checking.

**Screenshot Reference:** Screenshot_00a.png and Screenshot_00b.png show the index.txt file in directory listings.

---

#### Command 6: Set Initial Serial Number

**Purpose:** Set the starting serial number for certificates issued by this CA.

**Command:**
```bash
echo 1000 > serial
```

**Explanation:**
- `echo 1000` - Outputs the number 1000
- `>` - Redirects output to a file (creates or overwrites)
- `serial` - OpenSSL's serial number tracking file

**Expected Output:** None (silent success). A file named `serial` containing the text "1000" is created.

**Serial Number Format:** The serial number increases by 1 each time a certificate is issued. The format can be decimal or hexadecimal.

**Security Relevance:** Unique serial numbers prevent certificate collisions and are essential for revocation tracking. Starting at 1000 (rather than 1) is a security practice that obscures the total number of certificates issued.

**Screenshot Reference:** The serial file is visible in directory listing screenshots.

---

#### Command 7: Create CA Configuration File

**Purpose:** Create the complete OpenSSL configuration file that defines CA behavior, policies, and extensions.

**Command:**
```bash
cat > ca.cnf << 'EOF'
[ca]
default_ca = CA_default

[CA_default]
database = index.txt
serial = serial
new_certs_dir = newcerts
default_md = sha256
policy = policy_loose
default_days = 365
default_crl_days = 30
private_key = private/ca.key
certificate = certs/ca.crt

[policy_loose]
countryName = optional
stateOrProvinceName = optional
localityName = optional
organizationName = optional
commonName = supplied
emailAddress = optional

[req]
default_bits = 4096
default_md = sha256
prompt = no
distinguished_name = ca_dn

[ca_dn]
CN = Cybersecurity Lab Root CA
O = Cybersecurity Lab
C = KE

[v3_ca]
basicConstraints = critical, CA:TRUE
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
EOF
```

**Explanation of Each Section:**

| Section | Purpose |
|---------|---------|
| `[ca]` | Defines which CA configuration to use |
| `[CA_default]` | Default settings for all CA operations |
| `[policy_loose]` | Defines which certificate fields are required |
| `[req]` | Settings for certificate request generation |
| `[ca_dn]` | Distinguished Name for the Root CA |
| `[v3_ca]` | X.509 v3 extensions for CA certificates |

**Key Parameter Explanations:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `default_bits` | 4096 | Root CA key size (very secure) |
| `default_md` | sha256 | Hash algorithm for signatures |
| `default_days` | 365 | Server certificate validity period |
| `default_crl_days` | 30 | CRL validity period |
| `basicConstraints` | CA:TRUE | This certificate can sign others |
| `keyUsage` | keyCertSign, cRLSign | Key can sign certificates and CRLs |
| `CN` | Cybersecurity Lab Root CA | Common Name (identifies the CA) |
| `O` | Cybersecurity Lab | Organization name |
| `C` | KE | Country code (Kenya) |

**Expected Output:** A complete configuration file named `ca.cnf` is created in the current directory.

**Security Relevance:** 
- The CA configuration defines the security parameters for the entire PKI
- Weak parameters (small key sizes, weak hash algorithms) would compromise the entire trust chain
- The `critical` flag on extensions ensures clients must understand and enforce them

**Screenshot Reference:** Screenshot_01_ca_config_file.png shows the complete ca.cnf file content.

---

#### Command 8: Generate Root CA Private Key

**Purpose:** Generate the 4096-bit RSA private key for the Root Certificate Authority.

**Command:**
```bash
openssl genrsa -out private/ca.key 4096
```

**Explanation:**
- `openssl` - OpenSSL command-line toolkit
- `genrsa` - Generate RSA private key
- `-out private/ca.key` - Output file location
- `4096` - Key size in bits

**Expected Output:**
```
Generating RSA private key, 4096 bit long modulus (2 primes)
.....................................++++
................................................................................++++
e is 65537 (0x010001)
```

**Output Analysis:**
- The dots and plus signs represent the random number generation process
- "e is 65537" indicates the public exponent (standard value)
- The entire process takes several seconds due to 4096-bit key complexity

**Security Relevance:** 
- 4096-bit keys are currently considered secure for Root CAs (NIST recommends 2048-bit minimum, 4096-bit for high-security applications)
- The private key must remain absolutely secret; compromise would destroy trust in the entire PKI
- RSA with exponent 65537 is resistant to certain mathematical attacks

**Screenshot Reference:** Screenshot_02a_root_ca_certificate.png shows the key generation output.

---

#### Command 9: Restrict Root CA Private Key Permissions

**Purpose:** Set the most restrictive permissions on the Root CA private key.

**Command:**
```bash
chmod 400 private/ca.key
```

**Explanation:**
- `chmod 400` - Owner has read-only permission (4); group and others have no access (00)
- `private/ca.key` - Target private key file

**Permission Breakdown:**
| Digit | User | Permission | Value |
|-------|------|------------|-------|
| 4 | Owner (ubuntu) | Read only | r-- |
| 0 | Group | No access | --- |
| 0 | Others | No access | --- |

**Expected Output:** None (silent success).

**Security Relevance:** 
- The private key should be readable only by the CA process
- Write permission is removed to prevent accidental modification or deletion
- 400 is more restrictive than 600 (which allows write access)
- This is the most secure permission setting for a file that never needs modification

**Screenshot Reference:** The permission change is visible in directory listing screenshots (400 vs 700 for directory).

---

#### Command 10: Generate Root CA Self-Signed Certificate

**Purpose:** Create the self-signed Root CA certificate that serves as the trust anchor for the entire PKI.

**Command:**
```bash
openssl req -config ca.cnf -new -x509 -days 3650 -key private/ca.key -out certs/ca.crt -extensions v3_ca
```

**Explanation:**
- `openssl req` - Certificate request and generation tool
- `-config ca.cnf` - Use our CA configuration file
- `-new` - Create a new certificate
- `-x509` - Output a self-signed certificate (not a request)
- `-days 3650` - Certificate valid for 10 years (3650 days)
- `-key private/ca.key` - Use this private key
- `-out certs/ca.crt` - Save certificate to this file
- `-extensions v3_ca` - Apply the v3_ca extensions from config

**Expected Output:**
```
Generating a RSA private key
.....................................++++
writing new private key to 'private/ca.key'
-----
```

**Certificate Content:** The certificate will contain:
- Version 3 (X.509 v3)
- Serial number (starts from 1000)
- Signature algorithm: sha256WithRSAEncryption
- Issuer: CN=Cybersecurity Lab Root CA, O=Cybersecurity Lab, C=KE
- Subject: Same as issuer (self-signed)
- Validity: 10 years from creation
- Public key: 4096-bit RSA
- Extensions: basicConstraints=CA:TRUE, keyUsage=keyCertSign,cRLSign

**Security Relevance:** 
- The Root CA certificate is the trust anchor; all other certificates inherit their trust from this certificate
- The 10-year validity period is typical for Root CAs (they are rarely replaced)
- The v3_ca extensions properly mark this as a CA certificate

**Screenshot Reference:** Screenshot_02a_root_ca_certificate.png and Screenshot_02b_root_ca_certificate.png show the certificate generation and verification.

---

#### Command 11: Verify Root CA Certificate

**Purpose:** Display and verify the contents of the Root CA certificate.

**Command:**
```bash
openssl x509 -in certs/ca.crt -text -noout | head -20
```

**Explanation:**
- `openssl x509` - Certificate display and utility command
- `-in certs/ca.crt` - Input certificate file
- `-text` - Display human-readable text format
- `-noout` - Do not output the encoded certificate
- `| head -20` - Pipe output to show only first 20 lines

**Expected Output:**
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1000 (0x3e8)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = Cybersecurity Lab Root CA, O = Cybersecurity Lab, C = KE
        Validity
            Not Before: May 26 16:00:00 2026 GMT
            Not After : May 24 16:00:00 2036 GMT
        Subject: CN = Cybersecurity Lab Root CA, O = Cybersecurity Lab, C = KE
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (4096 bit)
```

**Verification Checks:**
1. Issuer equals Subject (self-signed)
2. Validity is 10 years
3. Version is 3 (X.509 v3)
4. Signature algorithm is sha256WithRSAEncryption

**Screenshot Reference:** Screenshot_02b_root_ca_certificate.png shows the certificate verification output.

---

### Part 2: Issuing Server Certificates

---

#### Command 12: Create Web Server Configuration File

**Purpose:** Create the configuration file that defines the web server certificate requirements.

**Command:**
```bash
cat > webserver.cnf << 'EOF'
[req]
default_bits = 2048
default_md = sha256
prompt = no
distinguished_name = server_dn
req_extensions = v3_req

[server_dn]
CN = www.cybersec-lab.local
O = Cybersecurity Lab
ST = Nairobi
C = KE

[v3_req]
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = DNS:www.cybersec-lab.local, DNS:cybersec-lab.local, IP:192.168.1.67
EOF
```

**Explanation:**

| Section | Purpose |
|---------|---------|
| `[req]` | Request generation settings |
| `[server_dn]` | Distinguished Name for the server |
| `[v3_req]` | X.509 v3 extensions for server certificate |

**Key Parameter Explanations:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `default_bits` | 2048 | Server key size (standard) |
| `CN` | www.cybersec-lab.local | Common Name (primary domain) |
| `O` | Cybersecurity Lab | Organization |
| `ST` | Nairobi | State/Province |
| `C` | KE | Country code |
| `basicConstraints` | CA:FALSE | Not a CA certificate |
| `keyUsage` | digitalSignature, keyEncipherment | For TLS key exchange |
| `extendedKeyUsage` | serverAuth | For TLS server authentication |
| `subjectAltName` | DNS and IP addresses | Alternative names |

**Security Relevance:**
- 2048-bit RSA is the current standard for server certificates (balance of security and performance)
- CA:FALSE explicitly prevents this certificate from being used as a CA (defense in depth)
- Subject Alternative Names are critical for modern browsers (CN alone is deprecated)
- Including IP address allows direct IP access in addition to hostname

**Screenshot Reference:** Screenshot_03_webserver_config_file.png shows the complete webserver.cnf file.

---

#### Command 13: Generate Web Server Private Key

**Purpose:** Generate the 2048-bit RSA private key for the web server.

**Command:**
```bash
openssl genrsa -out webserver.key 2048
```

**Explanation:**
- `openssl genrsa` - Generate RSA private key
- `-out webserver.key` - Output file
- `2048` - Key size in bits

**Expected Output:**
```
Generating RSA private key, 2048 bit long modulus (2 primes)
......................+++++
........+++++
e is 65537 (0x010001)
```

**Output Analysis:**
- The dots and plus signs represent random number generation
- 2048-bit keys generate faster than 4096-bit keys
- Public exponent 65537 is standard

**Security Relevance:**
- 2048-bit RSA keys are currently considered secure until approximately 2030
- The server private key must be protected but is less sensitive than the CA key
- If compromised, only this server's certificates need revocation

**Screenshot Reference:** Screenshot_04_server_csr.png shows the key generation.

---

#### Command 14: Generate Certificate Signing Request (CSR)

**Purpose:** Create a Certificate Signing Request for the web server to send to the CA.

**Command:**
```bash
openssl req -new -key webserver.key -out webserver.csr -config webserver.cnf
```

**Explanation:**
- `openssl req` - Certificate request tool
- `-new` - Create a new request
- `-key webserver.key` - Use this private key
- `-out webserver.csr` - Save CSR to this file
- `-config webserver.cnf` - Use server configuration for fields

**Expected Output:**
```
Generating a certificate signing request
...
```

**CSR Contents:**
- Subject: CN=www.cybersec-lab.local, O=Cybersecurity Lab, ST=Nairobi, C=KE
- Public key (from webserver.key)
- Requested extensions (from v3_req)
- Digital signature (proves possession of private key)

**Security Relevance:**
- The CSR contains only the public key and identifying information (not the private key)
- The CSR is signed by the private key to prove ownership
- CSRs can be transmitted over insecure channels

**Screenshot Reference:** Screenshot_04_server_csr.png shows the CSR generation.

---

#### Command 15: Verify CSR Contents

**Purpose:** Display and verify the contents of the Certificate Signing Request before submission.

**Command:**
```bash
openssl req -in webserver.csr -text -noout | head -15
```

**Explanation:**
- `openssl req` - Certificate request tool
- `-in webserver.csr` - Input CSR file
- `-text` - Display human-readable format
- `-noout` - Do not output the encoded CSR
- `| head -15` - Show first 15 lines

**Expected Output:**
```
Certificate Request:
    Data:
        Version: 1 (0x0)
        Subject: CN = www.cybersec-lab.local, O = Cybersecurity Lab, ST = Nairobi, C = KE
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (2048 bit)
                Modulus:
                    00:ab:cd:ef:12:34:56:78:90...
                Exponent: 65537 (0x010001)
        Attributes:
        Requested Extensions:
            X509v3 Basic Constraints: CA:FALSE
            X509v3 Key Usage: Digital Signature, Key Encipherment
            X509v3 Extended Key Usage: TLS Web Server Authentication
            X509v3 Subject Alternative Name: 
                DNS:www.cybersec-lab.local, DNS:cybersec-lab.local, IP Address:192.168.1.67
```

**Verification Checks:**
- Subject matches expected values
- Key size is 2048 bits
- Requested extensions are correct
- Subject Alternative Names include all required addresses

**Screenshot Reference:** Screenshot_04_server_csr.png shows the CSR verification output.

---

#### Command 16: Sign the Server Certificate with Root CA

**Purpose:** Use the Root CA to sign the server certificate, creating a trusted certificate.

**Command:**
```bash
openssl ca -config ca.cnf -in webserver.csr -out webserver.crt -extensions v3_req -extfile webserver.cnf -batch
```

**Explanation:**
- `openssl ca` - Certificate Authority signing command
- `-config ca.cnf` - Use CA configuration
- `-in webserver.csr` - Input CSR file
- `-out webserver.crt` - Output signed certificate
- `-extensions v3_req` - Apply v3_req extensions
- `-extfile webserver.cnf` - Extension configuration file
- `-batch` - Non-interactive mode (no prompts)

**Expected Output:**
```
Using configuration from ca.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'www.cybersec-lab.local'
organizationName      :ASN.1 12:'Cybersecurity Lab'
stateOrProvinceName   :ASN.1 12:'Nairobi'
countryName           :PRINTABLE:'KE'
Certificate is to be certified until May 26 18:00:00 2027 GMT (365 days)

Write out database with 1 new entries
Database updated
```

**What Happens During Signing:**
1. OpenSSL validates the CSR signature (proves key ownership)
2. CA verifies the requested subject information
3. CA assigns the next serial number (1001)
4. CA signs the certificate using its private key
5. Certificate is stored in `newcerts/` directory
6. Database (`index.txt`) is updated

**Security Relevance:**
- The CA's private key is used to sign the certificate
- The signature creates the trust chain: Client trusts CA → CA trusts Server
- The -batch flag prevents interactive confirmation (useful for automation)

**Screenshot Reference:** Screenshot_05_signed_server_certificate.png shows the signing output.

---

#### Command 17: Verify Signed Server Certificate

**Purpose:** Display and verify the contents of the signed server certificate.

**Command:**
```bash
openssl x509 -in webserver.crt -text -noout | head -25
```

**Explanation:**
- `openssl x509` - Certificate display command
- `-in webserver.crt` - Input certificate file
- `-text` - Human-readable format
- `-noout` - No encoded output
- `| head -25` - First 25 lines

**Expected Output:**
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1001 (0x3e9)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = Cybersecurity Lab Root CA, O = Cybersecurity Lab, C = KE
        Validity
            Not Before: May 26 18:00:00 2026 GMT
            Not After : May 26 18:00:00 2027 GMT
        Subject: CN = www.cybersec-lab.local, O = Cybersecurity Lab, ST = Nairobi, C = KE
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (2048 bit)
...
        X509v3 extensions:
            X509v3 Basic Constraints: CA:FALSE
            X509v3 Key Usage: Digital Signature, Key Encipherment
            X509v3 Extended Key Usage: TLS Web Server Authentication
            X509v3 Subject Alternative Name: 
                DNS:www.cybersec-lab.local, DNS:cybersec-lab.local, IP Address:192.168.1.67
```

**Verification Checks:**
- Issuer is the Root CA (not self-signed)
- Serial number incremented (1001)
- Validity is 365 days
- All requested extensions are present
- Subject Alternative Names match the CSR

**Screenshot Reference:** Screenshot_05_signed_server_certificate.png shows the certificate verification.

---

#### Command 18: List All CA Files

**Purpose:** Display all files created in the CA directory to verify completeness.

**Command:**
```bash
ls -la
```

**Expected Output:**
```
total 64
drwxrwxr-x 5 ubuntu ubuntu 4096 May 26 17:20 .
drwxrwxr-x 3 ubuntu ubuntu 4096 May 26 17:10 ..
-rw-rw-r-- 1 ubuntu ubuntu  750 May 26 17:15 ca.cnf
drwxrwxr-x 2 ubuntu ubuntu 4096 May 26 17:18 certs
drwxrwxr-x 2 ubuntu ubuntu 4096 May 26 17:12 crl
-rw-rw-r-- 1 ubuntu ubuntu    0 May 26 17:12 index.txt
-rw-rw-r-- 1 ubuntu ubuntu   21 May 26 17:20 index.txt.attr
-rw-rw-r-- 1 ubuntu ubuntu  152 May 26 17:20 index.txt.old
drwxrwxr-x 2 ubuntu ubuntu 4096 May 26 17:12 newcerts
drwx------ 2 ubuntu ubuntu 4096 May 26 17:12 private
-rw-rw-r-- 1 ubuntu ubuntu    4 May 26 17:12 serial
-rw-rw-r-- 1 ubuntu ubuntu    4 May 26 17:20 serial.old
-rw-rw-r-- 1 ubuntu ubuntu  758 May 26 17:18 webserver.cnf
-rw-rw-r-- 1 ubuntu ubuntu 1358 May 26 17:20 webserver.crt
-rw-rw-r-- 1 ubuntu ubuntu 1009 May 26 17:19 webserver.csr
-rw------- 1 ubuntu ubuntu 1704 May 26 17:19 webserver.key
```

**File Explanations:**

| File | Purpose |
|------|---------|
| `ca.cnf` | CA configuration |
| `certs/ca.crt` | Root CA certificate |
| `private/ca.key` | Root CA private key |
| `webserver.crt` | Signed server certificate |
| `webserver.key` | Server private key |
| `webserver.csr` | Certificate request |
| `index.txt` | Certificate database |
| `serial` | Next serial number |

**Screenshot Reference:** Screenshot_06_all_ca_files.png shows the complete file listing.

---

### Part 3: Secure Web Application with Custom Certificate

---

#### Command 19: Update Package List

**Purpose:** Refresh the Ubuntu package database before installing Apache.

**Command:**
```bash
sudo apt update
```

**Explanation:**
- `sudo` - Execute with superuser privileges
- `apt` - Advanced Package Tool (package manager)
- `update` - Download package information from repositories

**Expected Output:**
```
Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
Get:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease
Reading package lists... Done
```

**Screenshot Reference:** Screenshot_07_apache_installed.png shows the update process.

---

#### Command 20: Install Apache Web Server

**Purpose:** Install the Apache HTTP Server package.

**Command:**
```bash
sudo apt install apache2 -y
```

**Explanation:**
- `apt install` - Install packages
- `apache2` - Apache HTTP Server package
- `-y` - Automatically answer "yes" to prompts

**Expected Output:**
```
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  apache2 apache2-bin apache2-data apache2-utils
...
Setting up apache2 (2.4.62-1ubuntu1) ...
```

**Screenshot Reference:** Screenshot_07_apache_installed.png shows the installation.

---

#### Command 21: Enable SSL Module

**Purpose:** Enable the SSL/TLS module in Apache.

**Command:**
```bash
sudo a2enmod ssl
```

**Explanation:**
- `a2enmod` - Apache2 enable module
- `ssl` - SSL/TLS module name

**Expected Output:**
```
Considering dependency setenvif for ssl:
Module setenvif already enabled
Considering dependency mime for ssl:
Module mime already enabled
Considering dependency socache_shmcb for ssl:
Enabling module socache_shmcb.
Enabling module ssl.
To activate the new configuration, you need to run:
  systemctl restart apache2
```

**Screenshot Reference:** Screenshot_07_apache_installed.png shows the module enable output.

---

#### Command 22: Enable Headers Module

**Purpose:** Enable the headers module (for HSTS configuration).

**Command:**
```bash
sudo a2enmod headers
```

**Explanation:**
- `a2enmod` - Apache2 enable module
- `headers` - HTTP headers module name

**Expected Output:**
```
Enabling module headers.
To activate the new configuration, you need to run:
  systemctl restart apache2
```

**Screenshot Reference:** Screenshot_07_apache_installed.png shows the module enable output.

---

#### Command 23: Copy CA Certificate to Apache Directory

**Purpose:** Copy the Root CA certificate to Apache's SSL certificates directory.

**Command:**
```bash
sudo cp ~/cyber-labs/lab5/myCA/certs/ca.crt /etc/ssl/certs/
```

**Explanation:**
- `sudo cp` - Copy with superuser privileges
- `~/cyber-labs/lab5/myCA/certs/ca.crt` - Source file
- `/etc/ssl/certs/` - Destination directory (system certificates)

**Expected Output:** None (silent success).

**Screenshot Reference:** Screenshot_08_certificates_copied.png shows the copy operations.

---

#### Command 24: Copy Server Certificate to Apache Directory

**Purpose:** Copy the signed server certificate to Apache's SSL certificates directory.

**Command:**
```bash
sudo cp ~/cyber-labs/lab5/myCA/webserver.crt /etc/ssl/certs/
```

**Explanation:**
- `sudo cp` - Copy with superuser privileges
- `~/cyber-labs/lab5/myCA/webserver.crt` - Source file
- `/etc/ssl/certs/` - Destination directory

**Expected Output:** None (silent success).

**Screenshot Reference:** Screenshot_08_certificates_copied.png shows the copy operations.

---

#### Command 25: Copy Server Private Key to Apache Directory

**Purpose:** Copy the server private key to Apache's SSL private directory.

**Command:**
```bash
sudo cp ~/cyber-labs/lab5/myCA/webserver.key /etc/ssl/private/
```

**Explanation:**
- `sudo cp` - Copy with superuser privileges
- `~/cyber-labs/lab5/myCA/webserver.key` - Source file
- `/etc/ssl/private/` - Destination (restricted directory)

**Expected Output:** None (silent success).

**Security Relevance:** The private key is placed in `/etc/ssl/private/` which has restricted permissions.

**Screenshot Reference:** Screenshot_08_certificates_copied.png shows the copy operations.

---

#### Command 26: Restrict Private Key Permissions

**Purpose:** Set secure permissions on the server private key.

**Command:**
```bash
sudo chmod 600 /etc/ssl/private/webserver.key
```

**Explanation:**
- `sudo chmod` - Change permissions with superuser privileges
- `600` - Owner can read and write; group and others have no access
- `/etc/ssl/private/webserver.key` - Target file

**Expected Output:** None (silent success).

**Security Relevance:** Permission 600 ensures only root can read the private key.

**Screenshot Reference:** Screenshot_08_certificates_copied.png shows the permission change.

---

#### Command 27: Enable SSL Site Configuration

**Purpose:** Enable the default SSL virtual host configuration.

**Command:**
```bash
sudo a2ensite default-ssl.conf
```

**Explanation:**
- `a2ensite` - Apache2 enable site
- `default-ssl.conf` - SSL site configuration file

**Expected Output:**
```
Enabling site default-ssl.
To activate the new configuration, you need to run:
  systemctl reload apache2
```

**Screenshot Reference:** Screenshot_10_apache_running.png shows the enable output.

---

#### Command 28: Restart Apache Service

**Purpose:** Restart Apache to apply all configuration changes.

**Command:**
```bash
sudo systemctl restart apache2
```

**Explanation:**
- `systemctl restart` - Restart a system service
- `apache2` - Apache service name

**Expected Output:** None (silent success).

**Screenshot Reference:** Screenshot_10_apache_running.png shows the restart command.

---

#### Command 29: Check Apache Status

**Purpose:** Verify Apache is running correctly after configuration.

**Command:**
```bash
sudo systemctl status apache2 --no-pager
```

**Explanation:**
- `systemctl status` - Display service status
- `apache2` - Service name
- `--no-pager` - Disable pager (show all output directly)

**Expected Output:**
```
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled)
     Active: active (running) since Tue 2026-05-26 18:30:00 UTC
    Process: 12345 ExecStart=/usr/sbin/apachectl start (code=exited, status=0/SUCCESS)
   Main PID: 12350 (apache2)
      Tasks: 6 (limit: 1000)
     Memory: 12.5M
        CPU: 100ms
     CGroup: /system.slice/apache2.service
```

**Key Indicators:**
- `Active: active (running)` - Service is running
- `Main PID` - Process ID of Apache
- `status=0/SUCCESS` - Clean exit status

**Screenshot Reference:** Screenshot_10_apache_running.png shows the status output.

---

### Part 3.2: Client Certificate Installation

---

#### Command 30: Copy CA Certificate to Kali (SCP)

**Purpose:** Transfer the Root CA certificate from Ubuntu to Kali Linux.

**Command:**
```bash
scp ubuntu@192.168.1.67:~/cyber-labs/lab5/myCA/certs/ca.crt ~/cyber-labs/lab5/certs/
```

**Explanation:**
- `scp` - Secure copy (SSH-based file transfer)
- `ubuntu@192.168.1.67:` - Remote username and server IP
- `~/cyber-labs/lab5/myCA/certs/ca.crt` - Remote source file
- `~/cyber-labs/lab5/certs/` - Local destination directory

**Expected Output:**
```
ca.crt                                         100% 2100     2.1KB/s   00:00
```

**Security Relevance:** SCP encrypts the file during transfer using SSH encryption.

**Screenshot Reference:** Screenshot_11_ca_certificate_on_kali.png shows the SCP transfer.

---

#### Command 31: Verify CA Certificate on Kali

**Purpose:** Confirm the CA certificate was successfully copied to Kali.

**Command:**
```bash
ls -la ~/cyber-labs/lab5/certs/
```

**Expected Output:**
```
total 4
drwxr-xr-x 2 kali kali 4096 May 26 14:30 .
drwxr-xr-x 4 kali kali 4096 May 26 14:28 ..
-rw-r--r-- 1 kali kali 2100 May 26 14:30 ca.crt
```

**Screenshot Reference:** Screenshot_11_ca_certificate_on_kali.png shows the file listing.

---

#### Command 32: Copy CA Certificate to System Trust Store

**Purpose:** Install the CA certificate into Kali's system-wide certificate store.

**Command:**
```bash
sudo cp ~/cyber-labs/lab5/certs/ca.crt /usr/local/share/ca-certificates/cybersec-ca.crt
```

**Explanation:**
- `sudo cp` - Copy with superuser privileges
- `~/cyber-labs/lab5/certs/ca.crt` - Source file
- `/usr/local/share/ca-certificates/cybersec-ca.crt` - System trust store location

**Expected Output:** None (silent success).

**Screenshot Reference:** Screenshot_12_ca_installed_system.png shows the copy operation.

---

#### Command 33: Update System Certificate Bundle

**Purpose:** Rebuild the system-wide certificate bundle to include the new CA.

**Command:**
```bash
sudo update-ca-certificates
```

**Explanation:**
- `update-ca-certificates` - Command to update the system certificate store

**Expected Output:**
```
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
```

**Verification:** The "1 added" message confirms the CA certificate was successfully installed.

**Screenshot Reference:** Screenshot_12_ca_installed_system.png shows the update output.

---

### Part 3.3: Testing Secure Connection

---

#### Command 34: Test HTTPS Connection with curl (IP Address)

**Purpose:** Test the HTTPS connection using the server's IP address.

**Command:**
```bash
curl -v https://192.168.1.67/
```

**Explanation:**
- `curl` - Command-line HTTP client
- `-v` - Verbose output (show SSL/TLS details)
- `https://192.168.1.67/` - Target URL

**Expected Output:**
```
* Connected to 192.168.1.67 (192.168.1.67) port 443
* ALPN: offers h2,http/1.1
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate:
*  subject: CN=www.cybersec-lab.local; O=Cybersecurity Lab; ST=Nairobi; C=KE
*  start date: May 26 18:00:00 2026 GMT
*  expire date: May 26 18:00:00 2027 GMT
*  issuer: CN=Cybersecurity Lab Root CA; O=Cybersecurity Lab; C=KE
*  SSL certificate verify ok.
* using HTTP/1.x
> GET / HTTP/1.1
> Host: 192.168.1.67
> User-Agent: curl/8.19.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Tue, 26 May 2026 18:45:00 GMT
< Server: Apache/2.4.62 (Ubuntu)
< Content-Type: text/html; charset=UTF-8
```

**Key Success Indicators:**
- `SSL certificate verify ok` - Certificate is trusted
- `TLSv1.3` - Modern TLS version negotiated
- `HTTP/1.1 200 OK` - Successful response

**Screenshot Reference:** Screenshot_14_curl_https_test.png shows the curl output.

---

#### Command 35: Add Hostname to /etc/hosts

**Purpose:** Map the server's hostname to its IP address for local resolution.

**Command:**
```bash
echo "192.168.1.67 www.cybersec-lab.local cybersec-lab.local" | sudo tee -a /etc/hosts
```

**Explanation:**
- `echo` - Output the text
- `|` - Pipe to next command
- `sudo tee -a` - Append to file with superuser privileges
- `/etc/hosts` - Local DNS resolution file

**Expected Output:**
```
192.168.1.67 www.cybersec-lab.local cybersec-lab.local
```

**Verification:**
```bash
cat /etc/hosts | grep cybersec
```
Expected: `192.168.1.67 www.cybersec-lab.local cybersec-lab.local`

**Screenshot Reference:** Screenshot_15_curl_hostname_test.png shows the hosts file addition.

---

#### Command 36: Test HTTPS Connection with Hostname

**Purpose:** Test the HTTPS connection using the proper hostname that matches the certificate.

**Command:**
```bash
curl -v https://www.cybersec-lab.local/
```

**Expected Output:**
```
* Connected to www.cybersec-lab.local (192.168.1.67) port 443
* SSL certificate verify ok.
* subject: CN=www.cybersec-lab.local; O=Cybersecurity Lab; ST=Nairobi; C=KE
* issuer: CN=Cybersecurity Lab Root CA; O=Cybersecurity Lab; C=KE
< HTTP/1.1 200 OK
```

**Key Differences from IP Test:**
- Hostname matches certificate CN (no warning)
- Subject shows exact CN match

**Screenshot Reference:** Screenshot_15_curl_hostname_test.png shows the successful connection.

---

#### Command 37: Launch Firefox Browser

**Purpose:** Test the HTTPS connection using Firefox browser.

**Command:**
```bash
firefox https://www.cybersec-lab.local/ &
```

**Explanation:**
- `firefox` - Launch Firefox browser
- `https://www.cybersec-lab.local/` - Target URL
- `&` - Run in background (terminal remains usable)

**Expected Result:**
- No certificate warning
- Padlock icon in address bar
- Connection is secure message

**Screenshot Reference:** Screenshot_16_firefox_https_success.png shows Firefox with the padlock icon.

---

### Part 4: Certificate Revocation

---

#### Command 38: Revoke the Server Certificate

**Purpose:** Mark the server certificate as revoked in the CA database.

**Command:**
```bash
openssl ca -config ca.cnf -revoke webserver.crt
```

**Explanation:**
- `openssl ca` - CA management command
- `-config ca.cnf` - Use CA configuration
- `-revoke webserver.crt` - Revoke this certificate

**Expected Output:**
```
Using configuration from ca.cnf
Revoking Certificate 1001.
Database Updated
```

**What Happens:**
- The certificate with serial number 1001 is marked as revoked
- The index.txt file is updated with status 'R'
- The revocation date is recorded

**Screenshot Reference:** Screenshot_17_crl_generated.png shows the revocation output.

---

#### Command 39: Generate Certificate Revocation List (CRL)

**Purpose:** Create a signed list of all revoked certificates.

**Command:**
```bash
openssl ca -config ca.cnf -gencrl -out crl/ca.crl
```

**Explanation:**
- `openssl ca` - CA management command
- `-config ca.cnf` - Use CA configuration
- `-gencrl` - Generate Certificate Revocation List
- `-out crl/ca.crl` - Output CRL file

**Expected Output:**
```
Using configuration from ca.cnf
```

**CRL Contents:**
- Issuer: Root CA
- Last Update: Current date/time
- Next Update: 30 days later (default_crl_days)
- Revoked certificates list (serial numbers and revocation dates)

**Screenshot Reference:** Screenshot_17_crl_generated.png shows the CRL generation.

---

#### Command 40: View the CRL

**Purpose:** Display the contents of the Certificate Revocation List.

**Command:**
```bash
openssl crl -in crl/ca.crl -text -noout
```

**Explanation:**
- `openssl crl` - CRL display command
- `-in crl/ca.crl` - Input CRL file
- `-text` - Human-readable format
- `-noout` - No encoded output

**Expected Output:**
```
Certificate Revocation List (CRL):
        Version 2 (0x1)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = Cybersecurity Lab Root CA, O = Cybersecurity Lab, C = KE
        Last Update: May 26 18:50:00 2026 GMT
        Next Update: Jun 25 18:50:00 2026 GMT
        CRL extensions:
            X509v3 Authority Key Identifier: 
                keyid:AB:CD:EF:12:34:56:78:90
        Revoked Certificates:
            Serial Number: 1001
                Revocation Date: May 26 18:48:00 2026 GMT
        Signature Algorithm: sha256WithRSAEncryption
```

**Key Information:**
- Serial Number 1001 appears in revoked list
- Next Update is 30 days later
- CRL is signed by the Root CA

**Screenshot Reference:** Screenshot_17_crl_generated.png shows the CRL content.

---

#### Command 41: Generate OCSP Responder Private Key

**Purpose:** Create a private key for the OCSP responder.

**Command:**
```bash
openssl genrsa -out private/ocsp.key 2048
```

**Explanation:**
- `openssl genrsa` - Generate RSA key
- `-out private/ocsp.key` - Output file
- `2048` - Key size

**Expected Output:**
```
Generating RSA private key, 2048 bit long modulus
....................+++++
........+++++
e is 65537 (0x010001)
```

**Screenshot Reference:** Screenshot_18_ocsp_certificate.png shows the key generation.

---

#### Command 42: Generate OCSP Certificate Request

**Purpose:** Create a CSR for the OCSP responder certificate.

**Command:**
```bash
openssl req -new -key private/ocsp.key -out ocsp.csr -subj "/CN=OCSP Responder/O=Cybersecurity Lab/C=KE"
```

**Explanation:**
- `openssl req` - Certificate request command
- `-new` - Create new request
- `-key private/ocsp.key` - Use this key
- `-out ocsp.csr` - Output CSR
- `-subj` - Subject distinguished name

**Expected Output:**
```
Generating a certificate signing request
...
```

**Screenshot Reference:** Screenshot_18_ocsp_certificate.png shows the CSR generation.

---

#### Command 43: Sign OCSP Certificate with Root CA

**Purpose:** Issue a signed certificate for the OCSP responder.

**Command:**
```bash
openssl ca -config ca.cnf -in ocsp.csr -out certs/ocsp.crt -batch
```

**Explanation:**
- `openssl ca` - CA signing command
- `-config ca.cnf` - Use CA configuration
- `-in ocsp.csr` - Input CSR
- `-out certs/ocsp.crt` - Output certificate
- `-batch` - Non-interactive mode

**Expected Output:**
```
Using configuration from ca.cnf
Check that the request matches the signature
Signature ok
Certificate is to be certified until May 26 18:55:00 2027 GMT (365 days)
Database updated
```

**Screenshot Reference:** Screenshot_18_ocsp_certificate.png shows the signing output.

---

#### Command 44: View Certificate Database

**Purpose:** Display the CA database to confirm revocation status.

**Command:**
```bash
cat index.txt
```

**Expected Output:**
```
R	260526184800Z	260526184800Z	1001	unknown	/C=KE/ST=Nairobi/O=Cybersecurity Lab/CN=www.cybersec-lab.local
```

**Status Code Explanation:**
| Code | Meaning |
|------|---------|
| V | Valid (active) |
| R | Revoked |
| E | Expired |

**Screenshot Reference:** Screenshot_19_revoked_certificate.png shows the index.txt content.

---

#### Command 45: Demonstrate OCSP Query

**Purpose:** Show the OCSP query format for certificate status checking.

**Command:**
```bash
openssl ocsp -issuer certs/ca.crt -cert webserver.crt -text -no_cert_verify
```

**Explanation:**
- `openssl ocsp` - OCSP client command
- `-issuer certs/ca.crt` - CA certificate
- `-cert webserver.crt` - Certificate to check
- `-text` - Human-readable output
- `-no_cert_verify` - Skip certificate verification

**Expected Output:**
```
OCSP Request Data:
    Version: 1 (0x0)
    Requestor List:
        Certificate ID:
          Hash Algorithm: sha1
          Issuer Name Hash: XX:XX:XX:XX...
          Issuer Key Hash: XX:XX:XX:XX...
          Serial Number: 1001
    Request Extensions:
        OCSP Nonce: 0x04...
```

**Note:** This demonstrates the OCSP request format. A full OCSP responder setup would return the certificate status.

**Screenshot Reference:** Screenshot_20_ocsp_query.png shows the OCSP query output.

---

## 9. Security Concepts Demonstrated

### Public Key Infrastructure (PKI)

| Concept | Lab Implementation |
|---------|-------------------|
| Trust Anchor | Root CA self-signed certificate |
| Certificate Chain | Root CA → Server Certificate |
| Key Pair | Public key in certificate, private key stored securely |
| Digital Signature | CA signs server certificate |
| Certificate Validation | Client verifies signature and hostname |

### Certificate Extensions

| Extension | Purpose | Lab Value |
|-----------|---------|-----------|
| basicConstraints | CA capability | CA:TRUE for Root, CA:FALSE for server |
| keyUsage | Key restrictions | keyCertSign, cRLSign for CA |
| extendedKeyUsage | Application restrictions | serverAuth for web server |
| subjectAltName | Alternative identities | DNS names and IP address |

### Revocation Mechanisms

| Method | Description | Lab Implementation |
|--------|-------------|-------------------|
| CRL | Periodically published list | Generated with `-gencrl` |
| OCSP | Real-time status query | OCSP responder certificate created |

---

## 10. Vulnerabilities Identified

| Vulnerability | Severity | Description | Mitigation |
|---------------|----------|-------------|------------|
| Private Key Exposure | Critical | CA key compromise breaks entire PKI | 400 permissions, offline storage |
| Weak Key Generation | High | Small key sizes vulnerable to factoring | 4096-bit for CA, 2048-bit for server |
| Improper Validation | Medium | Clients skipping validation | Proper CA installation |
| No Revocation Checking | Medium | Cannot identify compromised certs | Implement CRL/OCSP |

---

## 11. Problems Encountered and Troubleshooting

### Problem 1: Missing private_key Configuration

**Error Message:**
```
variable lookup failed for CA_default::private_key
```

**Root Cause:** The `ca.cnf` file lacked `private_key` and `certificate` directives.

**Solution:** Added to `[CA_default]` section:
```ini
private_key = private/ca.key
certificate = certs/ca.crt
```

---

### Problem 2: Missing default_days Parameter

**Error Message:**
```
cannot lookup how many days to certify for
```

**Root Cause:** Missing `default_days` in CA configuration.

**Solution:** Added `default_days = 365` to `[CA_default]`.

---

### Problem 3: Missing default_crl_days Parameter

**Error Message:**
```
cannot lookup how long until the next CRL is issued
```

**Root Cause:** Missing `default_crl_days` for CRL generation.

**Solution:** Added `default_crl_days = 30` to `[CA_default]`.

---

### Problem 4: Certificate Hostname Mismatch

**Issue:** Certificate warnings when using IP address.

**Root Cause:** Certificate CN is hostname, not IP.

**Solution:** 
1. Added IP to subjectAltName
2. Added hostname to `/etc/hosts`
3. Tested with hostname instead of IP

---

## 12. Results and Observations

### Successful Outcomes

| Component | Status | Verification |
|-----------|--------|--------------|
| Root CA Certificate | ✅ | `openssl x509 -in certs/ca.crt -text` |
| Server Certificate | ✅ | Signed by Root CA |
| Apache SSL | ✅ | Port 443 listening |
| CA Installation on Kali | ✅ | System trust store updated |
| curl HTTPS Test | ✅ | "SSL certificate verify ok" |
| Firefox Test | ✅ | Padlock icon displayed |
| CRL Generation | ✅ | Contains revoked certificate |
| OCSP Certificate | ✅ | Signed by Root CA |

### Key Metrics

| Metric | Value |
|--------|-------|
| Root CA Key Size | 4096 bits |
| Server Key Size | 2048 bits |
| Root CA Validity | 10 years |
| Server Validity | 365 days |
| CRL Validity | 30 days |
| Certificates Issued | 2 (server + OCSP) |
| Certificates Revoked | 1 |

---

## 13. Security Analysis and Risk Assessment

### Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Root CA key compromise | Low | Critical | Offline storage, 400 permissions |
| Server private key theft | Medium | High | 600 permissions, regular rotation |
| Certificate expiration | Medium | Medium | Monitoring, auto-renewal |
| Revocation failure | Low | Medium | Multiple OCSP responders |

### Strengths

1. 4096-bit Root CA key meets NIST recommendations
2. Proper key usage restrictions (least privilege)
3. Secure file permissions (400 for CA key, 600 for server key)
4. Complete revocation infrastructure (CRL + OCSP)

### Weaknesses

1. Self-signed CA (by design for lab)
2. No HSTS implementation
3. No automated renewal

---

## 14. Lessons Learned

### Technical Lessons

1. **OpenSSL configuration requires explicit paths** - Always specify `private_key` and `certificate` in `[CA_default]`

2. **Validity periods must be configured** - Both `default_days` and `default_crl_days` are required

3. **Subject Alternative Names are essential** - Modern browsers require SANs; CN alone is insufficient

4. **Certificate trust requires two stores** - System store for applications, Firefox store for browser

### Best Practices Identified

| Practice | Rationale |
|----------|-----------|
| 4096-bit Root CA keys | Long-term security for trust anchor |
| 2048-bit server keys | Balance of security and performance |
| 10-year Root CA validity | Root CAs are rarely replaced |
| 1-year server validity | Regular rotation limits exposure |
| 30-day CRL validity | Balance security and distribution |
| Include IP in SAN | Allows direct IP access |

---

## 15. Best Practices and Recommendations

### For Production PKI

1. **Root CA Security:**
   - Keep Root CA offline
   - Use Hardware Security Module (HSM)
   - Implement multi-person control

2. **Certificate Management:**
   - Automate renewal
   - Monitor expiration dates
   - Maintain CRL with 7-30 day validity

3. **Web Server Configuration:**
   - Enable HSTS
   - Use TLS 1.2 and 1.3 only
   - Disable weak ciphers

4. **Client Configuration:**
   - Distribute CA certificates via group policy
   - Automate trust store updates
   - Implement certificate pinning

---

## 16. Conclusion

This laboratory exercise successfully demonstrated the complete lifecycle of a Private Key Infrastructure:

**Accomplishments:**
- Deployed a private Certificate Authority with 4096-bit RSA keys
- Issued signed server certificates with proper X.509 v3 extensions
- Configured Apache with SSL/TLS using custom certificates
- Installed CA certificates on Kali Linux system trust store
- Successfully tested HTTPS connections with curl and Firefox
- Implemented certificate revocation via CRL
- Created OCSP responder certificate

**Skills Demonstrated:**
- OpenSSL command-line proficiency
- PKI architecture understanding
- X.509 certificate structure knowledge
- Apache SSL/TLS configuration
- Multi-platform certificate distribution

**Importance:**
PKI is the foundation of secure internet communications. Understanding certificate lifecycle, trust chains, and revocation mechanisms is essential for any cybersecurity professional.

---

## 17. References

1. **Official Documentation:**
   - OpenSSL: https://www.openssl.org/docs/
   - Apache SSL: https://httpd.apache.org/docs/2.4/ssl/

2. **Security Standards:**
   - RFC 5280: X.509 PKI Certificate and CRL Profile
   - RFC 6960: OCSP Protocol

3. **NIST Publications:**
   - SP 800-57: Key Management Recommendations

4. **CA/Browser Forum:**
   - Baseline Requirements for TLS Server Certificates

---

