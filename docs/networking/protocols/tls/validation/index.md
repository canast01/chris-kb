---
tags:
  - networking
---
# TLS Validation


<div class="kb-summary">
Use these commands to verify TLS configuration on servers, check certificate validity, diagnose handshake failures, and confirm correct chain presentation.
</div>

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  openssl s_client -connect <host>:443 -servername <host>                                              │
│                                                                                                       │
│  Check output fields:                                                                                 │
│  ├── Verify return code: 0 (ok)       ✓  chain valid                                                  │
│  ├── Protocol: TLSv1.3                ✓  (TLSv1.1 = fail)                                             │
│  ├── Cipher: TLS_AES_256_GCM_SHA384   ✓  strong cipher                                                │
│  ├── depth=0  CN=web.example.com      ✓  server cert                                                  │
│  ├── depth=1  CN=Intermediate CA      ✓  intermediate sent                                            │
│  └── depth=2  CN=Root CA              ✓  chain complete                                               │
│                                                                                                       │
│  Additional checks:                                                                                   │
│  openssl x509 -noout -dates ─────────► check notAfter                                                 │
│  openssl x509 -noout -ext subjectAltName ► hostname in SAN                                            │
│  openssl x509 -modulus | md5sum       ┐                                                               │
│  openssl rsa  -modulus | md5sum       ┘ ► must match                                                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Quick Validation — Live Endpoint

```bash
# Full TLS handshake details
openssl s_client -connect <hostname>:443 -servername <hostname>

# Key fields to check in output:
# Verify return code: 0 (ok)     ← chain verified
# Protocol: TLSv1.3              ← protocol version
# Cipher: TLS_AES_256_GCM_SHA384 ← cipher negotiated
# depth=2 CN=Root CA             ← chain depth (0=server, 1=intermediate, 2=root)
```

## Certificate Validity Checks

```bash
# Expiry date
openssl s_client -connect <hostname>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -dates

# Subject and SANs (verify hostname coverage)
openssl s_client -connect <hostname>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -ext subjectAltName

# Issuer (confirm correct CA)
openssl s_client -connect <hostname>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -issuer

# Full certificate text
openssl s_client -connect <hostname>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -text
```

## Chain Validation

```bash
# Show the full chain presented
openssl s_client -connect <hostname>:443 -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -text | grep -E "Subject:|Issuer:"

# Verify chain against a specific CA bundle
openssl s_client -connect <hostname>:443 \
  -CAfile /etc/ssl/certs/ca-certificates.crt \
  -verify_return_error

# Expected: Verify return code: 0 (ok)
```

## Protocol and Cipher Checks

```bash
# Force specific TLS version (test what the server accepts)
openssl s_client -connect <hostname>:443 -tls1_2
openssl s_client -connect <hostname>:443 -tls1_3

# Confirm TLS 1.0/1.1 is rejected (should fail)
openssl s_client -connect <hostname>:443 -tls1_1
# Expected: alert handshake failure

# Enumerate all ciphers (nmap)
nmap --script ssl-enum-ciphers -p 443 <hostname>
```

## curl Validation

```bash
# Standard HTTPS request (uses system CA trust)
curl -sv https://<hostname>/

# Specify CA bundle (useful for internal CA)
curl --cacert /path/to/internal-ca.pem https://<hostname>/

# Show only TLS details
curl -sv https://<hostname>/ 2>&1 | grep -E "SSL|TLS|certificate|expire|issuer"

# Ignore certificate errors (testing only — never production)
curl -k https://<hostname>/
```

## Validating a Certificate File

```bash
# Check cert file is valid PEM
openssl x509 -in cert.pem -noout -text

# Check private key matches certificate
openssl x509 -modulus -noout -in cert.pem | md5sum
openssl rsa  -modulus -noout -in key.pem  | md5sum
# Both md5 values must match

# Check CSR matches certificate
openssl req  -modulus -noout -in request.csr | md5sum
openssl x509 -modulus -noout -in cert.pem    | md5sum

# Verify cert against CA
openssl verify -CAfile ca.crt -untrusted intermediate.crt cert.pem
```

## OCSP / Revocation Check

```bash
# Get OCSP URL from certificate
openssl x509 -in cert.pem -noout -ocsp_uri

# Query OCSP responder
openssl ocsp -issuer intermediate.crt -cert cert.pem \
  -url <ocsp-url> -resp_text

# Expected: "cert.pem: good"
```

## Comprehensive Scan — testssl.sh

```bash
# Install
git clone https://github.com/drwetter/testssl.sh
cd testssl.sh

# Full scan
./testssl.sh <hostname>:443

# Key output sections:
# - Protocol support (TLS versions)
# - Cipher categories (forward secrecy, AEAD, weak ciphers)
# - Certificate (expiry, chain, SAN)
# - Vulnerabilities (POODLE, BEAST, ROBOT, SWEET32, etc.)
```

## Validation Checklist

| Check | Command | Pass |
|---|---|---|
| Verify return code 0 | `openssl s_client` | `Verify return code: 0 (ok)` |
| Protocol TLS 1.2+ | `openssl s_client` | `Protocol: TLSv1.2` or `TLSv1.3` |
| Hostname in SAN | `openssl x509 -ext subjectAltName` | Hostname listed |
| Cert not expired | `openssl x509 -dates` | `notAfter` in the future |
| Chain complete | depth 0, 1, 2 in s_client | `depth=2` shows root |
| Key matches cert | `md5sum` comparison | Both hashes identical |
| TLS 1.0/1.1 rejected | `openssl s_client -tls1_1` | Connection fails |

## Common Errors

| Error | Meaning | Fix |
|---|---|---|
| `certificate has expired` | Past `notAfter` | Renew and deploy certificate |
| `certificate verify failed` | Chain untrusted | Install CA cert; check chain bundle |
| `hostname mismatch` | CN/SAN doesn't match | Reissue cert with correct SAN |
| `handshake failure` | No common cipher/protocol | Adjust cipher list or TLS version config |
| `key values mismatch` | Key and cert don't match | Use the key that was generated with this cert's CSR |
