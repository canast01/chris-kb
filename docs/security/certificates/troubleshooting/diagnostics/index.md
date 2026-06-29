---
tags:
  - security
  - troubleshooting
search:
  boost: 1.5
---
# Certificates — Diagnostics

<div class="kb-summary">
Certificate diagnostic commands: check expiry and SANs with openssl s_client, verify the full chain with openssl verify, test OCSP stapling and CRL freshness, inspect Windows certificate stores with certutil and Get-ChildItem, add root CAs to Linux trust stores, and collect a diagnostic bundle for escalation.

*Applies to: Linux (RHEL/Ubuntu) · Windows Server · OpenSSL 3.x · ADCS*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "openssl s_client -connect host:443 -showcerts\nRead: handshake failure, error code, chain presented" {shape: rectangle}
D: "echo  openssl x509 -noout -dates\nCheck notAfter date" {shape: rectangle}
E: "openssl x509 -in cert.pem -noout -text | grep -A5" {shape: rectangle}
F: "openssl s_client -connect host:443 -showcerts\nCount BEGIN CERTIFICATE blocks in output" {shape: rectangle}
G: "Get-ChildItem Cert:\LocalMachine\My\nTest-Certificate; certutil -verify" {shape: rectangle}
H: "certutil -ping\nsc query certsvc" {shape: rectangle}
I: "openssl s_client -connect host:443 -status\ngrep OCSP Response" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Check if HTTPS app is actually serving plain HTTP\nTry: curl -v http://host:443" {shape: rectangle}
L: "Check chain and root CA trust\nopenssl verify -CAfile ca-bundle.pem cert.pem" {shape: rectangle}
M: "M" {shape: rectangle}
N: "Replace certificate immediately\nRenew from CA; update on all servers" {shape: rectangle}
O: "Plan rotation now\nSet calendar reminder" {shape: rectangle}
P: "P" {shape: rectangle}
Q: "Server not sending intermediate\nAdd intermediate to server TLS config" {shape: rectangle}
R: "Check root CA in client trust store\nopenssl verify -CAfile root.pem -untrusted int.pem\ncert.pem" {shape: rectangle}
S: "certutil -verify cert.cer\nCheck chain and revocation in output" {shape: rectangle}
T: "Check ADCS event log\nEvent Viewer → Application → CertificationAuthority" {shape: rectangle}
U: "Check CRL freshness\nopenssl crl -in IssuingCA.crl -inform DER -noout\n-text | grep Next Update" {shape: rectangle}
V: "V" {shape: rectangle}
A: "Certificate Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
B -> I
J -> K
J -> L
J -> E
M -> N
M -> O
P -> Q
P -> R
G -> S
H -> T
I -> U
K -> V
L -> V
N -> V
O -> V
Q -> V
R -> V
S -> V
T -> V
U -> V
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_certificate_expiry_and_: "Step 1 — Check certificate expiry and basic fields" {shape: rectangle}
step_2_inspect_certificate_fields_an: "Step 2 — Inspect certificate fields and SAN" {shape: rectangle}
step_3_verify_the_certificate_chain: "Step 3 — Verify the certificate chain" {shape: rectangle}
step_4_check_ocsp_and_crl: "Step 4 — Check OCSP and CRL" {shape: rectangle}
step_5_windows_certificate_store_dia: "Step 5 — Windows certificate store diagnostics" {shape: rectangle}
step_6_add_root_ca_to_linux_trust_st: "Step 6 — Add root CA to Linux trust store" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_certificate_expiry_and_: investigate
symptom -> step_2_inspect_certificate_fields_an: investigate
symptom -> step_3_verify_the_certificate_chain: investigate
symptom -> step_4_check_ocsp_and_crl: investigate
symptom -> step_5_windows_certificate_store_dia: investigate
symptom -> step_6_add_root_ca_to_linux_trust_st: investigate
step_1_check_certificate_expiry_and_ -> resolution
step_2_inspect_certificate_fields_an -> resolution
step_3_verify_the_certificate_chain -> resolution
step_4_check_ocsp_and_crl -> resolution
step_5_windows_certificate_store_dia -> resolution
step_6_add_root_ca_to_linux_trust_st -> resolution
```

## Before you begin

- **Access:** admin credentials on the servers where certificates are installed; access to the CA (ADCS, Venafi, or public CA) for renewal
- **Gather first:** the exact error message from the browser or application (`ERR_CERT_DATE_INVALID`, `ssl_error_rx_record_too_long`, `CERTIFICATE_VERIFY_FAILED`), the hostname the client is connecting to, and whether this is a new cert or an existing one that just expired
- **Scope:** confirm whether the issue affects one endpoint, one CA, or a class of certificates (e.g., all internal certs signed by a specific intermediate)

---

## Step 1 — Check certificate expiry and basic fields

```bash
# Check certificate expiry on a live HTTPS endpoint
echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer
# Expected: notAfter date in the future; subject matches the hostname
# Problem: notAfter in the past = certificate expired

# Check expiry of a certificate file
openssl x509 -in cert.pem -noout -dates -subject -issuer

# Days remaining (negative = already expired)
echo $(( ($(openssl x509 -in cert.pem -noout -enddate \
  | cut -d= -f2 | xargs -I{} date -d '{}' +%s) - $(date +%s)) / 86400 )) days remaining

# Batch check multiple endpoints
for host in app1.corp.example.com app2.corp.example.com vcenter.corp.example.com; do
  expiry=$(echo | openssl s_client -connect $host:443 -servername $host 2>/dev/null \
    | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "$host: $expiry"
done
```


```text title="Expected output"
notBefore=Jan 15 09:22:14 2023 GMT
notAfter=Jan 15 09:22:14 2025 GMT
subject=CN = app1.corp.example.com, O = Example Corp, C = US
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2021 CA1

notBefore=Feb 20 14:33:05 2022 GMT
notAfter=Feb 20 14:33:05 2024 GMT
subject=CN = *.internal.example.com, O = Example Corp, C = US
issuer=C = US, O = Let's Encrypt, CN = R3

247 days remaining

app1.corp.example.com: Jan 15 09:22:14 2025 GMT
app2.corp.example.com: Mar 22 16:45:30 2025 GMT
vcenter.corp.example.com: Dec 10 11:18:22 2024 GMT
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the certificate file path is correct and readable with `ls -la cert.pem`.
    **`Temporary failure in name resolution`** — Ensure the hostname resolves with `nslookup <host>` and check network connectivity to port 443.
    **`date: invalid date`** — The certificate may be malformed; validate it with `openssl x509 -in cert.pem -text -noout` to inspect the enddate field format.
---

## Step 2 — Inspect certificate fields and SAN

```bash
# Full certificate text dump
openssl x509 -in cert.pem -noout -text

# Subject Alternative Names only (hostnames and IPs the cert is valid for)
openssl x509 -in cert.pem -noout -text | grep -A5 "Subject Alternative Name"
# Expected: DNS:hostname.corp.example.com listed here
# Problem: hostname not in SAN list = TLS hostname mismatch error

# From a live endpoint (captures what the server actually presents)
echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null \
  | openssl x509 -noout -text | grep -A10 "Subject Alternative Name"

# Check key size and algorithm (< 2048 RSA or MD5/SHA1 signature = rejected by modern clients)
openssl x509 -in cert.pem -noout -text | grep -E "Public Key Algorithm|RSA Public-Key|Signature Algorithm"
# Expected: RSA Public-Key: (2048 bit) or higher; Signature Algorithm: sha256WithRSAEncryption

# Check AIA and CDP extensions
openssl x509 -in cert.pem -noout -text | grep -A3 "Authority Information"
openssl x509 -in cert.pem -noout -text | grep -A3 "CRL Distribution"
```


```text title="Expected output"
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 0x4a7b9c2e1f5d8a3b
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=US, ST=California, O=Example Corp, CN=Example Corp CA
        Validity
            Not Before: Jan 15 10:23:45 2023 GMT
            Not After : Jan 15 10:23:45 2025 GMT
        Subject: C=US, ST=California, O=Example Corp, CN=hostname.corp.example.com
        X509v3 Subject Alternative Name:
            DNS:hostname.corp.example.com, DNS:*.corp.example.com, IP Address:10.42.8.15
        X509v3 Authority Information Access:
            CA Issuers - URI:http://ca.example.com/certs/root.crt
            OCSP - URI:http://ocsp.example.com
        X509v3 CRL Distribution Points:
            Full Name:
              URI:http://crl.example.com/example-ca.crl
        Public Key Algorithm: rsaEncryption
            RSA Public-Key: (2048 bit)
            Modulus:
                00:a7:3f:2b:8c:d4:e1:9a:...
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the certificate file path is correct and the file contains valid PEM-formatted data (check for `-----BEGIN CERTIFICATE-----` header).
    **`Verify return code: 21 (unable to verify the first certificate)`** — The server certificate chain is incomplete; ensure the full chain including intermediate certificates is installed on the server.
    **`hostname.corp.example.com not found in Subject Alternative Name list`** — Add the hostname to the certificate's SAN extension or request a new certificate that includes all required hostnames.
---

## Step 3 — Verify the certificate chain

```bash
# Show the full chain presented by a server
openssl s_client -connect <host>:443 -showcerts </dev/null 2>/dev/null
# Count BEGIN CERTIFICATE blocks: 1 = only leaf (missing intermediate); 2+ = chain included

# Save the chain to a file for offline analysis
openssl s_client -connect <host>:443 -showcerts </dev/null 2>/dev/null \
  > /tmp/server-chain.pem

# Verify cert against a CA bundle
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt cert.pem
# Expected: cert.pem: OK
# Problem: unable to get local issuer certificate = missing intermediate in trust store

# Verify with explicit intermediate (not in system trust store)
openssl verify -CAfile root.pem -untrusted intermediate.pem cert.pem

# Download the intermediate CA from the AIA URL (if server is not sending it)
AIA_URL=$(openssl x509 -in cert.pem -noout -text | grep -A2 "CA Issuers" | grep URI | awk '{print $2}')
curl -o /tmp/intermediate.crt "$AIA_URL"
# Convert DER to PEM if needed
openssl x509 -inform DER -in /tmp/intermediate.crt -out /tmp/intermediate.pem

# Build a full chain bundle for nginx/Apache (leaf first)
cat server.crt /tmp/intermediate.pem > /tmp/fullchain.pem
openssl storeutl -noout -text -certs /tmp/fullchain.pem | grep "Subject:"
# Expected: leaf cert subject first, intermediate subject second
```


```text title="Expected output"
CONNECTED(00000000)
depth=2 C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
verify return:1
depth=1 C = US, O = DigiCert Inc, CN = DigiCert SHA2 Secure Server CA
verify return:1
depth=0 C = US, ST = California, L = San Francisco, O = Example Corp, CN = api.example.com
verify return:1
-----BEGIN CERTIFICATE-----
MIIFWTCCBEGgAwIBAgIQD8CSqAc/vTQH3o/QyLkDFjANBgkqhkiG9w0BAQsFADB1
...
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIEsTCCA5mgAwIBAgIQBOHnpZ5l0X8ZyJD4tQ5ezDANBgkqhkiG9w0BAQsFADBh
...
-----END CERTIFICATE-----

cert.pem: OK

Subject: CN = api.example.com, O = Example Corp, ST = California, C = US
Subject: CN = DigiCert SHA2 Secure Server CA, O = DigiCert Inc, C = US
```

!!! warning "Common errors"
    **`unable to get local issuer certificate`** — Add the missing intermediate certificate to your trust store or use `openssl verify -untrusted intermediate.pem cert.pem`.
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Download the intermediate CA from the AIA URL in the certificate and add it to your fullchain bundle before the root.
    **`openssl x509: Unable to load certificate`** — Verify the certificate file exists and is in PEM format; convert from DER if needed with `openssl x509 -inform DER -in cert.crt -out cert.pem`.
---

## Step 4 — Check OCSP and CRL

```bash
# Test OCSP stapling on a live endpoint (server must support stapling)
openssl s_client -connect <host>:443 -status -tlsextdebug 2>&1 | \
  grep -i "OCSP Response"
# Expected: OCSP Response Status: successful; Response Verify OK
# Problem: no OCSP response = server is not stapling (may trigger revocation check by client)

# Check CRL freshness (must have a valid Next Update in the future)
openssl crl -in IssuingCA.crl -inform DER -noout -text | grep -E "Last Update|Next Update"
# Expected: Next Update in the future
# Problem: Next Update in the past = stale CRL; clients may reject certs from this CA

# Download and check a CRL from the CDP URL
CDP_URL=$(openssl x509 -in cert.pem -noout -text | grep -A2 "CRL Distribution" | grep URI | awk '{print $2}')
curl -o /tmp/issuing-ca.crl "$CDP_URL"
openssl crl -in /tmp/issuing-ca.crl -inform DER -noout -text | grep "Next Update"

# Test OCSP manually
OCSP_URL=$(openssl x509 -in cert.pem -noout -text | grep "OCSP" | awk '{print $NF}')
openssl ocsp -issuer intermediate.pem -cert cert.pem \
  -url "$OCSP_URL" -CAfile ca-bundle.pem -noverify -text 2>&1 | head -20
# Expected: Response verify OK; cert status: good
```


```text title="Expected output"
OCSP response: no response text in server reply
depth=0 /CN=api.example.com
verify return:1

Last Update: Jan 15 10:23:45 2025 GMT
Next Update: Jan 22 10:23:45 2025 GMT

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Download Speed   Time    Time remaining
100  1234  100  1234    0     0   8456      0 --:--:-- --:--:-- --:--:-- --:--:--
Next Update: Jan 22 10:23:45 2025 GMT

OCSP Response Data:
    OCSP Response Status: successful (0x0)
    Response Type: Basic OCSP Response
    Version: 1 (0x0)
    Responder Id: C = US, O = DigiCert Inc, CN = DigiCert OCSP Responder
    Produced At: Jan 15 12:34:56 2025 GMT
    Responses:
    Certificate ID:
      Hash Algorithm: sha1
      Issuer Name Hash: 3D2A1B4C5E6F7A8B9C0D1E2F3A4B5C6D
      Issuer Key Hash: 1A2B3C4D5E6F7A8B9C0D1E2F3A4B5C6D
      Serial Number: 0A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D
    Cert Status: good
    This Update: Jan 15 12:34:56 2025 GMT
    Next Update: Jan 16 12:34:56 2025 GMT
```

!!! warning "Common errors"
    **`OCSP response: no response text in server reply`** — Verify the server supports OCSP stapling with `openssl s_client -connect <host>:443 -status` and check server configuration (nginx/Apache must have stapling enabled).
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Add the `-k` flag to curl or ensure your system CA bundle is current with `update-ca-certificates` on Linux.
    **`unable to load Issuer certificate`** — Verify the intermediate.pem path is correct and contains the actual issuer certificate, not the end-entity cert, using `openssl x509 -in intermediate.pem -noout -subject`.
---

## Step 5 — Windows certificate store diagnostics

```powershell
# List all certificates in the Local Machine personal store
Get-ChildItem Cert:\LocalMachine\My |
  Select-Object Thumbprint, Subject, NotAfter, Issuer |
  Sort-Object NotAfter | Format-Table

# Find certificates expiring within 30 days
$cutoff = (Get-Date).AddDays(30)
Get-ChildItem Cert:\LocalMachine\My |
  Where-Object { $_.NotAfter -lt $cutoff } |
  Select-Object Subject, NotAfter | Format-Table

# Validate certificate chain and revocation
Get-ChildItem Cert:\LocalMachine\My | Test-Certificate -AllowUntrustedRoot

# Detailed certificate validation (chain + revocation + policy)
certutil -verify cert.cer
# Expected: "CertUtil: -verify command completed successfully"
# Problem: revocation failure, chain build error, or policy constraint failure

# Check if ADCS CA service is running
sc query certsvc
# Expected: STATE: 4 RUNNING

# Test ADCS CA reachability
certutil -ping
# Expected: "CertUtil: -ping command completed successfully"

# View CA information
certutil -cainfo
# Shows: CA name, CA type, CA certificate, pending requests count
```

---

## Step 6 — Add root CA to Linux trust store

New internal CA certificates need to be distributed to all Linux hosts.

```bash
# Debian / Ubuntu
cp internal-root-ca.crt /usr/local/share/ca-certificates/
update-ca-certificates
# Expected: "1 added, 0 removed; done."

# RHEL / CentOS / Rocky
cp internal-root-ca.crt /etc/pki/ca-trust/source/anchors/
update-ca-trust
# Expected: no output (silent success)

# Verify the root CA is now trusted
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt internal-server.crt
# Expected: internal-server.crt: OK

# Test a service that was failing (e.g., curl, git)
curl -v https://internal-service.corp.example.com/health
# Expected: TLS handshake completes; no certificate verify error
```


```text title="Expected output"
# Debian / Ubuntu
Reading package lists... Done
Processing triggers for ca-certificates (20230311ubuntu0.22.04.1) ...
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.

# RHEL / CentOS / Rocky
(no output — command completes silently)

# Verify the root CA is now trusted
internal-server.crt: OK

# Test a service that was failing (e.g., curl, git)
*   Trying 10.42.8.15:443...
* Connected to internal-service.corp.example.com (10.42.8.15) port 443 (#0)
* TLS 1.3 connection using TLS_AES_256_GCM_SHA384
* Server certificate:
*  subject: CN=internal-service.corp.example.com
*  issuer: CN=Internal Root CA
*  SSL certificate verify ok.
> GET /health HTTP/1.1
< HTTP/1.1 200 OK
< Content-Type: application/json
{"status":"healthy"}
```

!!! warning "Common errors"
    **`cp: cannot stat 'internal-root-ca.crt': No such file or directory`** — Verify the certificate file exists in the current directory or provide the full path to the source file.
    **`error: certificate verify failed`** — Run `update-ca-certificates` (Debian/Ubuntu) or `update-ca-trust` (RHEL/CentOS) after copying the CA certificate, then retry the verification command.
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Ensure the root CA certificate was copied to the correct system trust store path and the update command completed successfully.
---

## Step 7 — Collect certificate diagnostic bundle

```bash
# Linux — collect certificate diagnostic output
{
  echo "=== Date ==="
  date
  echo "=== Remote cert chain ==="
  openssl s_client -connect <host>:443 -showcerts -servername <host> \
    </dev/null 2>&1
  echo "=== Cert dates and subject ==="
  openssl x509 -in cert.pem -noout -dates -subject -issuer 2>/dev/null
  echo "=== Verify ==="
  openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt cert.pem 2>&1
  echo "=== OCSP ==="
  openssl s_client -connect <host>:443 -status </dev/null 2>&1 | grep -i ocsp
} > /tmp/cert-diag-$(date +%Y%m%d).txt

# Windows — collect certificate diagnostic output
Get-ChildItem Cert:\LocalMachine\My | Export-Csv C:\Temp\certs.csv
certutil -verify cert.cer > C:\Temp\certutil-verify.txt 2>&1
certutil -cainfo >> C:\Temp\certutil-verify.txt 2>&1

# Include in the escalation case:
# - openssl s_client output (shows what chain the server is presenting)
# - certutil -verify output (shows Windows chain build and revocation result)
# - The certificate file if the CA needs to examine it
# - The exact error message from the browser or application
# - Time the issue started and any recent CA or certificate changes
```


```text title="Expected output"
=== Date ===
Thu Mar 14 09:47:23 UTC 2024
=== Remote cert chain ===
CONNECTED(00000003)
depth=0 C = US, ST = California, L = San Francisco, O = Example Corp, CN = api.example.com
verify return:1
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKp8Z7x9vQ2kMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
...
-----END CERTIFICATE-----
=== Cert dates and subject ==="
notBefore=Jan 15 00:00:00 2024 GMT
notAfter=Jan 14 23:59:59 2025 GMT
subject=C = US, ST = California, O = Example Corp, CN = api.example.com
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2021 CA1
=== Verify ===
cert.pem: OK
=== OCSP ===
OCSP response: successful (0x0)
Cert Status: good
This Update: Mar 14 08:30:15 2024 GMT
Next Update: Mar 21 08:30:15 2024 GMT

C:\Users\Admin> Get-ChildItem Cert:\LocalMachine\My | Export-Csv C:\Temp\certs.csv
C:\Users\Admin> certutil -verify cert.cer > C:\Temp\certutil-verify.txt 2>&1
CertUtil: -verify command completed successfully.
C:\Users\Admin> certutil -cainfo >> C:\Temp\certutil-verify.txt 2>&1
CertUtil: -cainfo command completed successfully.
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the cert.pem file exists in the current directory and is readable with `ls -la cert.pem`.
    **`error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed`** — The certificate chain is incomplete or the CA bundle is missing; add the intermediate CA to the chain or update `/etc/ssl/certs/ca-certificates.crt` with `sudo update-ca-certificates`.
    **`OCSP response: unauthorized (0x6)`** — The OCSP responder rejected the request, likely due to network filtering; verify outbound HTTPS access to the OCSP responder URL or disable OCSP stapling validation temporarily.
---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| Linux CA trust | `/etc/ssl/certs/` (Linux) | Root CAs trusted by the system |
| Windows cert store | `Cert:\LocalMachine\My` | End-entity certs bound to IIS, RDP, etc. |
| ADCS event log | `Event Viewer → Application → CertificationAuthority` | Certificate request failures, CRL publishing |
| ADCS CA log | `certutil -log` | Issuance and revocation events |
| Application TLS log | varies by app (`/var/log/nginx/error.log`, IIS logs) | SSL handshake errors at the application layer |

---

## See also

- [Certificates — Common Issues](../common-issues/)
- [Certificates — Escalation](../escalation/)

## Verify resolution

- `echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | openssl x509 -noout -dates` shows `notAfter` in the future and well beyond 30 days
- `openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt cert.pem` returns `cert.pem: OK`
- The application or browser that was showing a certificate error now connects without any TLS warning
- `openssl s_client -connect host:443 -showcerts 2>/dev/null | grep -c "BEGIN CERTIFICATE"` returns 2 or more (full chain is being served)
