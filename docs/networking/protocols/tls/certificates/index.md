---
tags:
  - networking
---
# TLS Certificates

<div class="kb-summary">
A TLS certificate is a signed X.509 document that binds a public key to an identity (hostname, IP, or service).
</div>

The certificate allows clients to verify they are talking to the correct server and to establish encrypted sessions.

```d2
direction: down

certificate_components: "Certificate Components" {shape: rectangle}
certificate_types: "Certificate Types" {shape: rectangle}
reading_a_certificate: "Reading a Certificate" {shape: rectangle}
generating_a_csr: "Generating a CSR" {shape: rectangle}
certificate_formats: "Certificate Formats" {shape: rectangle}
key_sizes_and_algorithms: "Key Sizes and Algorithms" {shape: rectangle}

certificate_components -> certificate_types: uses
certificate_types -> reading_a_certificate: uses
reading_a_certificate -> generating_a_csr: uses
generating_a_csr -> certificate_formats: uses
certificate_formats -> key_sizes_and_algorithms: uses
```

## Certificate Components

| Field | Description | Example |
|---|---|---|
| Subject | Identity the cert belongs to | `CN=web.example.com` |
| Issuer | CA that signed the certificate | `CN=Example Internal CA` |
| Subject Alternative Names (SANs) | All hostnames / IPs the cert covers | `web.example.com, api.example.com, 10.0.0.10` |
| Not Before / Not After | Validity window | `2026-01-01` to `2027-01-01` |
| Public Key | Used for encryption | RSA 2048/4096 or ECDSA P-256/P-384 |
| Signature | CA's digital signature over the cert | SHA-256 with RSA |
| Key Usage | Permitted operations | `Digital Signature, Key Encipherment` |
| Extended Key Usage | Application-specific use | `TLS Web Server Authentication` |

## Certificate Types

| Type | Issued to | Typical use |
|---|---|---|
| **DV (Domain Validated)** | Domain owner only | Public websites (Let's Encrypt) |
| **OV (Organization Validated)** | Verified organization | Internal services, public corporate sites |
| **EV (Extended Validation)** | Full business verification | High-assurance external portals |
| **Wildcard** | `*.example.com` | Covers all subdomains at one level |
| **SAN / Multi-SAN** | Multiple explicit names | Services with many hostnames |
| **Client cert** | User or service identity | Mutual TLS (mTLS) |
| **Code signing** | Software publisher | Signing executables |

## Reading a Certificate

```bash
# View cert details from a file
openssl x509 -in certificate.pem -noout -text

# Quick view — subject, issuer, dates, SANs
openssl x509 -in certificate.pem -noout \
  -subject -issuer -dates -ext subjectAltName

# View cert served by a live server
openssl s_client -connect <hostname>:443 -servername <hostname> </dev/null 2>/dev/null \
  | openssl x509 -noout -text

# Check expiry only
openssl x509 -in certificate.pem -noout -enddate
```


```text title="Expected output"
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 04:a1:8f:2e:9c:d7:b3:44:e5:6f:21:9a
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2021 CA1
        Validity
            Not Before: Jan 15 00:00:00 2024 GMT
            Not After : Jan 14 23:59:59 2025 GMT
        Subject: CN = api.example.com
        X509v3 Subject Alternative Name:
            DNS:api.example.com, DNS:*.api.example.com, DNS:example.com

subject=CN = api.example.com
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2021 CA1
notBefore=Jan 15 00:00:00 2024 GMT
notAfter=Jan 14 23:59:59 2025 GMT
X509v3 Subject Alternative Name:
    DNS:api.example.com, DNS:*.api.example.com

notAfter=Jan 14 23:59:59 2025 GMT
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the certificate file path is correct and the file contains valid PEM-formatted data (check for `-----BEGIN CERTIFICATE-----` header).
    **`error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure`** — Ensure the hostname matches the certificate's CN or SAN, and the server is reachable on port 443 with TLS enabled.
    **`No certificate returned by server`** — Add `-showcerts` flag to `s_client` to debug the connection, or verify the server is responding to TLS handshakes on the specified port.
## Generating a CSR

```bash
# Generate private key and CSR together
openssl req -newkey rsa:4096 -keyout server.key -out server.csr \
  -subj "/CN=web.example.com/O=Example Corp/C=GB"

# CSR with SANs (requires config file)
cat > san.cnf <<EOF
[req]
req_extensions = v3_req
distinguished_name = dn
[dn]
[v3_req]
subjectAltName = DNS:web.example.com, DNS:api.example.com, IP:10.0.0.10
EOF

openssl req -newkey rsa:4096 -keyout server.key -out server.csr \
  -config san.cnf -subj "/CN=web.example.com"
```


```text title="Expected output"
Generating a RSA private key
.......................................................................................................................+++++
.+++++
writing new private key to 'server.key'
-----
(no output — command completes silently)
Generating a RSA private key
.......................................................................................................................+++++
.+++++
writing new private key to 'server.key'
-----
```

!!! warning "Common errors"
    **`Can't open config file: san.cnf`** — Ensure the config file is created in the current working directory before running the second openssl command.
    **`unable to write 'random state'`** — Run the commands with appropriate write permissions to the working directory, or use a temporary directory with `cd /tmp` first.
    **`req: Unrecognized flag -config`** — Verify your OpenSSL version supports the `-config` flag (available in OpenSSL 1.0.0+); use `openssl version` to check.
## Certificate Formats

| Format | Extension | Description | Convert |
|---|---|---|---|
| PEM | `.pem`, `.crt`, `.cer` | Base64, human-readable headers | Default for Linux |
| DER | `.der`, `.cer` | Binary format | `openssl x509 -inform DER` |
| PKCS#12 | `.pfx`, `.p12` | Cert + key bundled | Windows / Java |
| PKCS#7 | `.p7b`, `.p7c` | Cert chain, no key | IIS |

```bash
# PEM → PKCS#12 (for Windows)
openssl pkcs12 -export -out server.pfx \
  -inkey server.key -in server.crt -certfile chain.pem

# PKCS#12 → PEM
openssl pkcs12 -in server.pfx -nokeys -out cert.pem
openssl pkcs12 -in server.pfx -nocerts -nodes -out key.pem
```


```text title="Expected output"
Enter Export Password:
Verifying - Enter Export Password:
(no output — command completes silently)
MAC verified OK
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error outputting keys from pkcs12 file for writing`** — Ensure the PKCS#12 file is not corrupted and you entered the correct import password when prompted.
    **`Mac verify error`** — The PKCS#12 file password is incorrect; re-run the command and enter the matching export password used during creation.
## Key Sizes and Algorithms

| Algorithm | Minimum | Recommended | Notes |
|---|---|---|---|
| RSA | 2048 bits | 4096 bits | Universal compatibility |
| ECDSA | P-256 | P-384 | Smaller keys, faster — prefer for new deployments |
| Ed25519 | — | — | Not widely supported for TLS certs yet |

## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| `Certificate not trusted` | Chain incomplete or unknown CA | Install intermediate CA; check bundle |
| `Name mismatch` | Hostname not in SAN or CN | `openssl x509 -noout -ext subjectAltName` |
| `Certificate expired` | Past `Not After` date | Replace certificate; set up expiry alerts |
| `Wrong key for certificate` | Mismatched key and cert | `openssl x509 -modulus` and `openssl rsa -modulus` — must match |
