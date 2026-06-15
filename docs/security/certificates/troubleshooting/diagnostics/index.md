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

```text
┌───────────────────────── Security Certificates — Diagnostics ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Start here: openssl s_client -connect host:443 -showcerts → check notAfter and chain       │    │
│   │   TLS handshake fails: verify chain with openssl verify; check SAN matches hostname          │    │
│   │   Windows cert issues: Get-ChildItem Cert:\LocalMachine\My; certutil -verify cert.cer       │     │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Linux / OpenSSL                 │  │               Windows / ADCS                │   │
│   │   openssl s_client -connect host:443         │  │   Get-ChildItem Cert:\LocalMachine\My      │    │
│   │   openssl x509 -in cert.pem -noout -text     │  │   certutil -verify cert.cer               │     │
│   │   openssl verify -CAfile root.pem cert.pem   │  │   Test-Certificate; sc query certsvc      │     │
│   │   openssl s_client -status (OCSP stapling)   │  │   certutil -ping (ADCS CA reachability)   │     │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Client (browser / app) · TLS endpoint · CA server · CRL/OCSP responder · trust store                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│  SAN             = Subject Alternative Name; the X.509 extension that lists valid hostnames/IPs       │
│  AIA             = Authority Information Access; extension containing the issuing CA download URL     │
│  CDP             = CRL Distribution Point; extension with URL to download the certificate revocation  │
│  OCSP            = Online Certificate Status Protocol; real-time revocation check (faster than CRL)   │
│  Chain           = sequence from end-entity cert → intermediate(s) → root CA                          │
│  Trust store     = OS or browser list of trusted root CA certificates                                 │
│  certutil        = Windows built-in CLI for PKI operations; also Linux tool via openssl-legacy pkg    │
│  AIA fetching    = clients download missing intermediates from the AIA URL to build the chain         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TD
    A([Certificate Issue]) --> B{What type of problem?}
    B -->|TLS handshake failure in browser or app| C[openssl s_client -connect host:443 -showcerts\nRead: handshake failure, error code, chain presented]
    B -->|Certificate expired| D[echo | openssl s_client -connect host:443 2>/dev/null | openssl x509 -noout -dates\nCheck notAfter date]
    B -->|Wrong hostname / SAN mismatch| E[openssl x509 -in cert.pem -noout -text | grep -A5 'Subject Alternative'\nVerify hostname appears in SAN list]
    B -->|Chain validation error / untrusted CA| F[openssl s_client -connect host:443 -showcerts\nCount BEGIN CERTIFICATE blocks in output]
    B -->|Windows cert store issue| G[Get-ChildItem Cert:\LocalMachine\My\nTest-Certificate; certutil -verify]
    B -->|ADCS CA not issuing certs| H[certutil -ping\nsc query certsvc]
    B -->|OCSP or CRL check failing| I[openssl s_client -connect host:443 -status\ngrep OCSP Response]
    C --> J{Error in handshake?}
    J -->|ssl_error_rx_record_too_long| K[Check if HTTPS app is actually serving plain HTTP\nTry: curl -v http://host:443]
    J -->|certificate verify failed| L[Check chain and root CA trust\nopenssl verify -CAfile ca-bundle.pem cert.pem]
    J -->|hostname mismatch| E
    D --> M{notAfter in the past?}
    M -->|Yes| N[Replace certificate immediately\nRenew from CA; update on all servers]
    M -->|Within 30 days| O[Plan rotation now\nSet calendar reminder]
    F --> P{How many certs?}
    P -->|Only 1 END CERTIFICATE| Q[Server not sending intermediate\nAdd intermediate to server TLS config]
    P -->|2+ but still fails| R[Check root CA in client trust store\nopenssl verify -CAfile root.pem -untrusted int.pem cert.pem]
    G --> S[certutil -verify cert.cer\nCheck chain and revocation in output]
    H --> T[Check ADCS event log\nEvent Viewer → Application → CertificationAuthority]
    I --> U[Check CRL freshness\nopenssl crl -in IssuingCA.crl -inform DER -noout -text | grep Next Update]
    J --> V[Collect diagnostic output\nopenssl s_client -connect host:443 -showcerts > diag.txt 2>&1]
    K --> V
    L --> V
    N --> V
    O --> V
    Q --> V
    R --> V
    S --> V
    T --> V
    U --> V

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,J,M,P dark
    class C,D,E,F,G,H,I,K,L,N,O,Q,R,S,T,U action
    class V escalate
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

- [Certificates — Common Issues](common-issues/)
- [Certificates — Escalation](escalation/)

## Verify resolution

- `echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | openssl x509 -noout -dates` shows `notAfter` in the future and well beyond 30 days
- `openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt cert.pem` returns `cert.pem: OK`
- The application or browser that was showing a certificate error now connects without any TLS warning
- `openssl s_client -connect host:443 -showcerts 2>/dev/null | grep -c "BEGIN CERTIFICATE"` returns 2 or more (full chain is being served)
