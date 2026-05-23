# 🔐 Lab 2: Secure Hashing and Digital Signatures

## 📚 Course Information
- **Course:** Advanced Cryptography (CYBE6229)
- **Platform:** Kali Linux Virtual Machine
- **Lab Topic:** Hash Functions, Password Cracking, Digital Signatures, and Collision Analysis

---

# 📖 Overview

This laboratory demonstrates practical cryptographic security concepts through hands-on exercises involving:

- Weak hash cracking
- Hash performance benchmarking
- RSA digital signatures
- MD5 collision demonstrations
- Secure hashing verification with SHA-256

The objective of this lab is to understand why outdated cryptographic algorithms such as MD5 and SHA-1 are considered insecure and how modern cryptographic techniques protect integrity and authenticity.

---

# 📂 Project Structure

```text
lab2/
├── hashes/
├── signatures/
├── collisions/
├── reports/
└── README.md
```

---

# 🧪 Part 1 — Breaking Weak Hashes

## Objectives
- Generate MD5 password hashes
- Crack hashes using dictionary attacks
- Compare MD5 vs SHA-256 performance
- Analyze password security weaknesses

## Activities Performed
- Generated password hashes using MD5
- Used HashCat and John the Ripper for cracking
- Tested weak passwords against common wordlists
- Benchmarked hashing speeds

## Key Findings
| Algorithm | Security Status | Notes |
|-----------|-----------------|------|
| MD5 | ❌ Broken | Extremely fast to crack |
| SHA-1 | ⚠ Deprecated | Collision attacks exist |
| SHA-256 | ✅ Secure | Recommended modern standard |

---

# ✍️ Part 2 — Digital Signatures

## Objectives
- Generate RSA key pairs
- Sign documents securely
- Verify document authenticity
- Detect tampering attempts

## Activities Performed
- Generated 2048-bit RSA private/public keys
- Signed files using OpenSSL
- Verified signatures successfully
- Demonstrated verification failure after file tampering

## Security Concepts Demonstrated
- Authentication
- Integrity
- Non-repudiation

---

# 💥 Part 3 — Hash Collision Demonstration

## Objectives
- Demonstrate practical MD5 collisions
- Compare collision resistance with SHA-256

## Activities Performed
- Tested two different files producing identical MD5 hashes
- Verified SHA-256 generates unique hashes for different inputs

## Result
- MD5 collisions were successfully reproduced
- SHA-256 remained collision-resistant

---

# 🛠️ Tools and Technologies

| Tool | Purpose |
|------|---------|
| HashCat | Password cracking |
| John the Ripper | Dictionary attacks |
| OpenSSL | RSA key generation and signatures |
| Python | Collision testing scripts |
| Kali Linux | Penetration testing environment |

---

# 🔒 Security Lessons Learned

1. MD5 and SHA-1 should never be used for modern security applications.
2. Fast hashing algorithms are dangerous for password storage.
3. Digital signatures provide integrity and authenticity verification.
4. Private keys must always remain confidential.
5. SHA-256 remains secure for modern cryptographic applications.

---

# 📊 Practical Skills Demonstrated

- Cryptographic hash analysis
- Password auditing
- Digital signature implementation
- RSA key management
- Security benchmarking
- Collision testing
- Linux command-line security tools

---

# 💼 Professional Relevance

This lab reflects real-world cybersecurity practices used in:

- Penetration Testing
- Security Engineering
- PKI Administration
- Compliance Auditing
- Incident Response
- Secure Software Development

---

# 🚀 Future Improvements

- Implement salted password hashing
- Explore bcrypt and Argon2
- Analyze TLS certificate signatures
- Perform SHA-3 comparisons

---

# 📜 License

This repository is intended for educational and academic purposes only.

---

# 👨‍💻 Author

Advanced Cryptography Laboratory Work  
Kali Linux Security Environment
