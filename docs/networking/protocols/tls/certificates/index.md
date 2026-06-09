# TLS Certificates


<div class="kb-summary">
A TLS certificate is a signed X.509 document that binds a public key to an identity (hostname, IP, or service).
</div>

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Certificate                                                                                          │
│  ┌──────────────────────────────────────────────────────┐                                             │
│  │  Subject:  CN=web.example.com, O=Example Corp        │                                             │
│  │  SANs:     DNS:web.example.com, DNS:api.example.com  │                                             │
│  │            IP:10.0.0.10                              │                                             │
│  │  Issuer:   CN=Example Intermediate CA                │                                             │
│  │  Valid:    2026-01-01  to  2027-01-01                │                                             │
│  │  Key:      RSA 4096  (or ECDSA P-256)                │                                             │
│  │  Key Usage: Digital Signature, Key Encipherment      │                                             │
│  │  EKU:      TLS Web Server Authentication             │                                             │
│  ├──────────────────────────────────────────────────────┤                                             │
│  │  Signature: SHA-256 with RSA (by Intermediate CA)   │                                              │
│  └──────────────────────────────────────────────────────┘                                             │
│                                                                                                       │
│  Client checks: SAN matches hostname + not expired +                                                  │
│                 chain traces to trusted root CA                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
The certificate allows clients to verify they are talking to the correct server and to establish encrypted sessions.

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
