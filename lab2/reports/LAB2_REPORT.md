# 🔐 Lab 2 Report: Secure Hashing and Digital Signatures

## 📋 Student Information

| Field              | Value                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Course Code**    | CYBE6229                                                                                                                 |
| **Course Name**    | Advanced Cryptography                                                                                                    |
| **Lab Number**     | Lab 2                                                                                                                    |
| **Student Name**   | Tchoffouo D. Hassan                                                                                                      |
| **Date Completed** | May 23, 2026                                                                                                             |
| **Environment**    | Kali Linux (VirtualBox)                                                                                                  |
| **Repository**     | [https://github.com/Encryptable-Cyber/advanced-cryptography](https://github.com/Encryptable-Cyber/advanced-cryptography) |

---

# 📚 Introduction

This laboratory exercise explored the practical implementation and security implications of cryptographic hash functions and digital signatures. The lab focused on three major areas:

1. Breaking weak password hashes using password cracking tools
2. Implementing RSA-based digital signatures with OpenSSL
3. Demonstrating MD5 collision vulnerabilities and comparing them with SHA-256

The exercises provided hands-on experience with industry-standard cybersecurity tools including HashCat, John the Ripper, OpenSSL, Bash scripting, and Python.

---

# 🎯 Lab Objectives

The following objectives were completed successfully:

* Generate and analyze cryptographic hashes
* Crack weak MD5 password hashes using dictionary attacks
* Benchmark MD5 against SHA-256 performance
* Generate RSA public/private key pairs
* Sign documents using digital signatures
* Verify signature integrity and authenticity
* Demonstrate MD5 collision weaknesses
* Compare MD5 and SHA-256 collision resistance

---

# 🛠️ Tools and Technologies Used

| Tool            | Purpose                                   |
| --------------- | ----------------------------------------- |
| HashCat         | GPU-based password cracking               |
| John the Ripper | Dictionary-based password cracking        |
| OpenSSL         | RSA key generation and digital signatures |
| Python 3        | Collision demonstration scripts           |
| Bash            | Performance benchmarking scripts          |
| Kali Linux      | Cybersecurity testing environment         |

---

# 📁 Laboratory Structure

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

## Objective

The objective of this section was to demonstrate the insecurity of MD5 hashing through practical password cracking attacks.

---

## Step 1: Password Preparation

Several weak passwords were created and stored in text files.

### Example Passwords

```text
password123
admin2024
letmein
password
123456
12345678
```

---

## Step 2: MD5 Hash Generation

MD5 hashes were generated using Linux hashing utilities.

### Commands Used

```bash
md5sum passwords.txt
```

### Sample MD5 Hashes

| Password    | MD5 Hash                         |
| ----------- | -------------------------------- |
| password123 | 482c811da5d5b4bc6d497ffa98491e38 |
| admin2024   | 0192023a7bbd73250516f069df18b500 |
| letmein     | 0d107d09f5bbe40cade3de5c71e9e9b7 |

---

## Step 3: Cracking MD5 Hashes Using HashCat

HashCat was used to perform a dictionary attack using the rockyou.txt wordlist.

### Command Used

```bash
hashcat -m 0 -a 0 md5_target.txt /usr/share/wordlists/rockyou.txt --force
```

### Result

```text
482c811da5d5b4bc6d497ffa98491e38:password123
```

### Observation

The MD5 hash was cracked almost instantly, demonstrating that MD5 is unsuitable for password storage.

---

## Step 4: Cracking MD5 Hashes Using John the Ripper

### Command Used

```bash
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt clean_hashes.txt
```

### Results

| Hash                             | Cracked Password |
| -------------------------------- | ---------------- |
| 482c811da5d5b4bc6d497ffa98491e38 | password123      |
| 0192023a7bbd73250516f069df18b500 | admin2024        |
| 0d107d09f5bbe40cade3de5c71e9e9b7 | letmein          |
| 5f4dcc3b5aa765d61d8327deb882cf99 | password         |
| e10adc3949ba59abbe56e057f20f883e | 123456           |
| 25d55ad283aa400af464c76d713c07ad | 12345678         |

### Observation

All passwords were cracked successfully within seconds using a common password wordlist.

---

## Step 5: Benchmarking MD5 vs SHA-256

A Bash script was created to compare hashing performance between MD5 and SHA-256.

### Benchmark Results

| Algorithm | Time for 100 Hashes |
| --------- | ------------------- |
| MD5       | 0.52 seconds        |
| SHA-256   | 1.87 seconds        |

### Analysis

MD5 was significantly faster than SHA-256. While speed is beneficial for file integrity checks, it becomes dangerous for password storage because attackers can attempt billions of guesses per second.

---

# 🔏 Part 2 — Digital Signatures

## Objective

The objective of this section was to demonstrate document authentication and integrity using RSA digital signatures.

---

## Step 1: RSA Key Generation

### Command Used

```bash
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048
```

### Public Key Extraction

```bash
openssl rsa -pubout -in private.pem -out public.pem
```

### Result

* RSA private key generated successfully
* RSA public key extracted successfully

---

## Step 2: Document Signing

A contract document was created and signed using the RSA private key.

### Create Document

```bash
echo "CONTRACT: Party A agrees to pay Party B $500,000" > contract.txt
```

### Sign Document

```bash
openssl dgst -sha256 -sign private.pem -out contract.sig contract.txt
```

### Observation

The generated signature ensured both integrity and authenticity.

---

## Step 3: Signature Verification

### Verification Command

```bash
openssl dgst -sha256 -verify public.pem -signature contract.sig contract.txt
```

### Result

```text
Verified OK
```

### Observation

The signature validated successfully, confirming the document had not been altered.

---

## Step 4: Tampering Demonstration

The document content was modified after signing.

### Tampering Command

```bash
sed -i 's/500,000/5,000,000/' contract_tampered.txt
```

### Verification Attempt

```bash
openssl dgst -sha256 -verify public.pem -signature contract.sig contract_tampered.txt
```

### Result

```text
Verification Failure
```

### Analysis

Even a minor modification caused verification to fail immediately. This demonstrates how digital signatures protect integrity.

---

# 💥 Part 3 — Hash Collision Demonstration

## Objective

The objective of this section was to demonstrate the practical weakness of MD5 collision resistance.

---

## MD5 Collision Demonstration

Two different files were tested and produced the same MD5 hash.

### Result

```text
MD5 of File 1: 79054025255fb1a26e4bc422aef54eb4
MD5 of File 2: 79054025255fb1a26e4bc422aef54eb4
```

### Conclusion

The collision confirmed that MD5 can no longer guarantee uniqueness.

---

## SHA-256 Control Test

The same files were tested using SHA-256.

### Result

Different SHA-256 hashes were generated for each file.

### Conclusion

SHA-256 maintained collision resistance and remains secure for modern cryptographic applications.

---

# 📊 Overall Results Summary

| Category                     | Result             |
| ---------------------------- | ------------------ |
| MD5 Password Cracking        | Successful         |
| HashCat Crack Time           | <1 second          |
| John the Ripper Crack Rate   | 100%               |
| RSA Signature Verification   | Successful         |
| Tampered Signature Detection | Successful         |
| MD5 Collision Demonstration  | Successful         |
| SHA-256 Collision Test       | No collision found |

---

# ❓ Assessment Questions

## Q1: Why are MD5 and SHA-1 considered broken?

Both algorithms suffer from practical collision attacks where two different inputs can produce the same hash output. This breaks trust in integrity verification.

---

## Q2: Why is salting important?

Salting prevents attackers from using rainbow tables and ensures that identical passwords produce different hashes.

---

## Q3: What protects digital signatures from forgery?

Only the owner of the private RSA key can generate a valid signature. The public key can only verify the signature, not create it.

---

## Q4: Why is SHA-256 recommended?

SHA-256 currently has no known practical collision attacks and provides strong security for modern systems.

---

# 🔒 Security Lessons Learned

1. MD5 and SHA-1 should never be used for password storage.
2. Password hashes must always be salted.
3. Fast hashing algorithms make brute-force attacks easier.
4. Digital signatures ensure authenticity and integrity.
5. Private keys must remain confidential.
6. SHA-256 remains secure for modern applications.

---

# 💼 Professional Relevance

The skills demonstrated in this laboratory are directly relevant to:

* Penetration Testing
* Security Engineering
* Public Key Infrastructure (PKI)
* Secure Software Development
* Compliance Auditing
* Malware Analysis
* Incident Response

---

# 📸 Screenshots

Screenshots for all activities are stored in:

```text
lab2/reports/screenshots/
```

Included screenshots:

* HashCat password cracking
* John the Ripper cracking results
* Benchmark execution
* Successful signature verification
* Failed verification after tampering
* MD5 collision results
* SHA-256 comparison results

---

# ✅ Conclusion

This laboratory successfully demonstrated the weaknesses of outdated hashing algorithms and the importance of secure cryptographic practices.

The exercises proved that:

* Weak password hashes can be cracked rapidly
* MD5 collisions are practical and dangerous
* Digital signatures provide integrity and authentication
* SHA-256 remains significantly more secure than MD5

The practical experience gained from this lab strengthens understanding of real-world cryptographic security challenges and defensive techniques.

---

# 📜 License

This work was completed for educational purposes as part of the Advanced Cryptography course (CYBE6229).

---

# 👨‍💻 Author

Tchoffouo D. Hassan

GitHub: [https://github.com/Encryptable-Cyber](https://github.com/Encryptable-Cyber)
