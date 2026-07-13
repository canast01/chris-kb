---
tags:
  - operations
  - security
description: "Windows certificate operations use certutil for verification, revocation, and store management. Linux operations rely on openssl for inspection..."
---
# Certificates CLI Reference

<div class="kb-summary">
Windows certificate operations use `certutil` for verification, revocation, and store management. Linux operations rely on `openssl` for inspection, verification, and TLS connectivity testing.
</div>

 PowerShell provides `Get-ChildItem Cert:\` for the Windows certificate store and `Test-Certificate` for chain validation.

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Tool Selection by Task

```d2
direction: right

task: "task" {shape: rectangle}
opensslText: "openssl x509 -in cert.pem -noout -text" {shape: rectangle}
opensslModulus: "openssl x509 / rsa -noout -modulus\n+ md5sum comparison" {shape: rectangle}
opensslClient: "openssl s_client -connect host:443\n-servername host" {shape: rectangle}
opensslVerify: "openssl verify -CAfile root.pem\n-untrusted intermediate.pem cert.pem" {shape: rectangle}
certutil: "certutil -store My\ncertutil -verify cert.pem\ncertutil -addstore Root ca.crt" {shape: rectangle}
psStore: "Get-ChildItem Cert:\\LocalMachine\\My\nTest-Certificate" {shape: rectangle}
csrGen: "openssl req -new -newkey rsa:4096\n-keyout key.pem -out csr.pem" {shape: rectangle}

task -> opensslText
task -> opensslModulus
task -> opensslClient
task -> opensslVerify
task -> certutil
task -> psStore
task -> csrGen
```

---

## openssl — Inspection

Inspect certificates, keys, and chains before deploying or renewing.

```bash
# View all certificate fields
openssl x509 -in cert.pem -noout -text

# Show subject, issuer, and expiry only
openssl x509 -in cert.pem -noout -subject -issuer -dates

# Show SANs (Subject Alternative Names)
openssl x509 -in cert.pem -noout -text | grep -A1 "Subject Alternative"

# Compute SHA-1 thumbprint
openssl x509 -in cert.pem -noout -fingerprint -sha1

# Compute SHA-256 fingerprint
openssl x509 -in cert.pem -noout -fingerprint -sha256

# Inspect a PKCS#12 bundle
openssl pkcs12 -info -in cert.p12 -noout

# View a CSR
openssl req -in request.csr -noout -text
```


```text title="Expected output"
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 0a:1b:2c:3d:4e:5f:6a:7b
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = US, O = DigiCert Inc, CN = DigiCert Global Root CA
        Validity
            Not Before: Jan 15 10:00:00 2023 GMT
            Not After : Jan 15 10:00:00 2026 GMT
        Subject: C = US, ST = California, L = San Francisco, O = Example Corp, CN = api.example.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (2048 bit)
subject=C = US, ST = California, L = San Francisco, O = Example Corp, CN = api.example.com
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global Root CA
notBefore=Jan 15 10:00:00 2023 GMT
notAfter=Jan 15 10:00:00 2026 GMT
                X509v3 Subject Alternative Name: 
                    DNS:api.example.com, DNS:*.example.com, DNS:www.example.com
SHA1 Fingerprint=A1:B2:C3:D4:E5:F6:7A:8B:9C:0D:1E:2F:3A:4B:5C:6D:7E:8F:9A:0B
SHA256 Fingerprint=A1:B2:C3:D4:E5:F6:7A:8B:9C:0D:1E:2F:3A:4B:5C:6D:7E:8F:9A:0B:1C:2D:3E:4F:5A:6B:7C:8D:9E:0F:1A:2B
MAC verified OK
PKCS7 Encrypted data: pbeWithSHA1And3-KeyTripleDES-CBC, Iteration 2048
Certificate bag
Bag Attributes
    localKeyID: 01 00 00 00 
subject=/C=US/O=Example Corp/CN=api.example.com
issuer=/C=US/O=DigiCert Inc/CN=DigiCert Global Root CA
-----BEGIN CERTIFICATE REQUEST-----
MIICljCCAX4CAQAwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALRiMLAA...
-----END CERTIFICATE REQUEST-----
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the certificate file path is correct and the file contains valid PEM-formatted data (check for encoding issues or corruption).
    **`MAC verification failure`** — Ensure the correct password is provided when prompted for the PKCS#12 bundle, or the file may be corrupted.
    **`no start line:PEM routines:PEM_read_bio:no start line:../crypto/pem/pem_lib.c`** — Convert the certificate to PEM format using `openssl x509 -inform DER -in cert.der -
---

## openssl — Verification

```bash
# Verify certificate matches the private key (moduli must match)
openssl x509 -noout -modulus -in cert.pem | md5sum
openssl rsa  -noout -modulus -in key.pem  | md5sum

# Verify certificate against a CA bundle
openssl verify -CAfile ca-bundle.pem cert.pem

# Verify full chain (intermediate + root)
openssl verify -CAfile root.pem -untrusted intermediate.pem cert.pem

# Check days until expiry
openssl x509 -enddate -noout -in cert.pem |   awk -F= '{print $2}' | xargs -I{} date -d "{}" +%s |   awk -v now=$(date +%s) '{print int(($1-now)/86400)" days remaining"}'
```


```text title="Expected output"
d8e8fca2dc0f896fd7cb4cb0031ba249
d8e8fca2dc0f896fd7cb4cb0031ba249
cert.pem: OK
cert.pem: OK
47 days remaining
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the certificate file path is correct and the file is in PEM format (not DER); use `file cert.pem` to check.
    **`unable to load Private Key`** — Ensure the private key file exists and is readable; check permissions with `ls -l key.pem` and convert from DER if needed with `openssl rsa -in key.der -inform DER -out key.pem`.
    **`error 20 at 0 depth lookup: unable to get local issuer certificate`** — Add the issuing CA certificate to the CA bundle or use `-partial_chain` flag if the full chain is not available.
---

## openssl — TLS Testing

```bash
# Test TLS handshake and show server certificate
openssl s_client -connect <host>:443 -servername <host>

# Check specific TLS version support
openssl s_client -connect <host>:443 -tls1_2
openssl s_client -connect <host>:443 -tls1_3

# Show full certificate chain from a live endpoint
openssl s_client -connect <host>:443 -servername <host> 2>/dev/null |   openssl x509 -noout -text

# Test LDAPS
openssl s_client -connect <ldap_host>:636

# Test SMTPS
openssl s_client -connect <smtp_host>:465 -starttls smtp
```


```text title="Expected output"
CONNECTED(00000003)
depth=0 CN = api.example.com
verify error:num=20:unable to get local issuer certificate
verify return:1
depth=0 CN = api.example.com
verify return:1
---
Certificate chain
 0 s:CN = api.example.com
   i:C = US, O = Let's Encrypt, CN = R3
-----BEGIN CERTIFICATE-----
MIIFWzCCBEOgAwIBAgISA7x8z/9k7z8z/9k7z8z/9k7z MA0GCSqGSIb3DQEBBQsF
ADBLMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMTGV0J3MgRW5jcnlwdDEkMCIGA1UE
...
-----END CERTIFICATE-----
subject=CN = api.example.com
issuer=C = US, O = Let's Encrypt, CN = R3
---
Signature ok
subject=CN = api.example.com
issuer=C = US, O = Let's Encrypt, CN = R3
Public-Key: (2048 bit, RSA)
X509v3 Subject Alternative Name: 
    DNS:api.example.com, DNS:*.api.example.com
Not Before: Jan 15 08:22:14 2024 GMT
Not After : Apr 14 08:22:13 2024 GMT
```

!!! warning "Common errors"
    **`connect:errno=111 Connection refused`** — Verify the host is reachable and the port is open with `nc -zv <host> 443`.
    **`error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed`** — Add `-CAfile /etc/ssl/certs/ca-certificates.crt` to verify against your system's CA bundle, or use `-showcerts` to inspect the chain.
    **`error:1408F10B:SSL routines:SSL3_GET_RECORD:unexpected eof while reading`** — The service may not support TLS on that port; confirm the correct port and protocol with your service documentation.
---

## certutil — Windows

```bash
# Verify a certificate file
certutil -verify cert.pem

# Display certificate detail
certutil -dump cert.pem

# Check revocation (CRL/OCSP)
certutil -verify -urlfetch cert.pem

# Add a certificate to the Trusted Root store
certutil -addstore Root ca.crt

# Remove a certificate from the store by thumbprint
certutil -delstore My <thumbprint>

# List all certs in the Personal store
certutil -store My
```


```text title="Expected output"
================ Certificate Information ================
Certificate:
    Version: V3
    Serial Number: 0x4a2b8c9d1e5f7a3b
    Signature Algorithm: sha256RSA
    Issuer: CN=Example Root CA, O=Example Corp, C=US
    Subject: CN=server.example.com, O=Example Corp, C=US
    NotBefore: 1/15/2024 10:30 AM
    NotAfter: 1/15/2025 10:30 AM
    Public Key: RSA (2048 bits)
    Thumbprint: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0

Verifying certificate chain...
Certificate is valid.
Revocation check: Good (OCSP responder: ocsp.example.com)

Certificate "ca.crt" added to store.

Certificate deleted.

My "Personal" store has 3 certificates:
  0. server.example.com
     Serial: 0x4a2b8c9d1e5f7a3b
     Thumbprint: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  1. client.example.com
     Serial: 0x5b3c9d0e2f6g8b4c
     Thumbprint: b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1
  2. legacy.example.com
     Serial: 0x6c4d0e1f3g7h9c5d
     Thumbprint: c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2
```

!!! warning "Common errors"
    **`CertUtil: -verify command FAILED: 0x80092012 (-2146885614)`** — Ensure the certificate file path is correct and the file is not corrupted; try `certutil -dump cert.pem` first to verify the file is readable.
    **`CertUtil: -addstore command FAILED: 0x80070005 (E_ACCESSDENIED)`** — Run the command as Administrator (right-click Command Prompt and select "Run as administrator").
    **`CertUtil: -delstore command FAILED: 0x80092004 (-2146885628)`** — Verify the thumbprint is correct by listing certificates with `certutil -store My` and copy the exact thumbprint value.
---

## PowerShell — Windows Certificate Store

```powershell
# List all certs in the Personal (My) store
Get-ChildItem Cert:\LocalMachine\My | Select Subject, Thumbprint, NotAfter

# Find certificates expiring within 30 days
$cutoff = (Get-Date).AddDays(30)
Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.NotAfter -lt $cutoff }

# Find by thumbprint
Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Thumbprint -eq "<thumbprint>" }

# Validate certificate chain
Get-ChildItem Cert:\LocalMachine\My | Test-Certificate

# Export certificate to PEM
$cert = Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Subject -like "*<cn>*" }
[System.IO.File]::WriteAllBytes("C:\cert.cer", $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert))
```

---

## Key & CSR Generation

```bash
# Generate a 2048-bit RSA private key
openssl genrsa -out key.pem 2048

# Generate a 4096-bit RSA key
openssl genrsa -out key.pem 4096

# Generate an EC key (P-256)
openssl ecparam -name prime256v1 -genkey -noout -out ec-key.pem

# Create a CSR from an existing key
openssl req -new -key key.pem -out request.csr   -subj "/CN=<common_name>/O=<org>/C=<country>"

# Create a CSR with SANs (using a config file)
openssl req -new -key key.pem -out request.csr -config <(cat <<EOF
[req]
distinguished_name = dn
req_extensions = v3_req
prompt = no
[dn]
CN = <common_name>
[v3_req]
subjectAltName = DNS:<san1>,DNS:<san2>
EOF
)
```


```text title="Expected output"
Generating RSA private key, 2048 bit long modulus (2 primes)
.......+++
...................+++
e is 65537 (0x010001)
Generating RSA private key, 4096 bit long modulus (4 primes)
.............+++
.........................+++
e is 65537 (0x010001)
(no output — command completes silently)
You are about to be asked to enter information that will be incorporated
into your certificate request.
(no output — command completes silently)
```

!!! warning "Common errors"
    **`openssl: No such file or directory`** — Install OpenSSL with `apt-get install openssl` (Debian/Ubuntu) or `brew install openssl` (macOS).
    **`unable to load Private Key`** — Verify the key file exists and the path is correct with `ls -la key.pem`.
    **`error on line 1 of config request: unknown option`** — Ensure the heredoc syntax is correct and the config file is properly formatted without extra whitespace.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificates — Procedures](../procedures/)
- [Certificates — Health Checks](../health-checks/)
- [Certificates — Scripts](../scripts/)
- [Certificates — Backup and Restore](../backup-restore/)
- [Certificates — Install and Upgrade](../install-upgrade/)
- [Certificates — Common Issues](../../troubleshooting/common-issues/)
