---
title: TLS
---

# TLS and HTTPS


<div class="kb-summary">
TLS (Transport Layer Security) provides encryption, integrity, and authentication for network communications.
</div>

        TLS HANDSHAKE (TLS 1.3 simplified)
```text
┌─────────────┐                              ┌──────────────────┐
│   Client    │                              │     Server                                               │
└──────┬──────┘                              └────────┬─────────┘
```
       │  1. ClientHello                              │
       │  (supported ciphers, TLS version)            │
       │ ────────────────────────────────────────────►│
       │  2. ServerHello + Certificate                │
       │  (chosen cipher, server cert + chain)        │
       │ ◄────────────────────────────────────────────│
       │  3. Key Exchange                             │
       │  (client verifies cert, derives shared key) │
       │ ────────────────────────────────────────────►│
       │  4. Finished (encrypted with shared key)    │
       │ ◄════════════════════════════════════════════│
       │                                             │
       │  All application data encrypted             │
       │ ◄════════════════════════════════════════════│
```xml


<div class="kb-grid kb-grid-1">

<a class="kb-card" href="certificates/">
  <strong>Certificates</strong>
  <span>Certificates notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="chains/">
  <strong>Chains</strong>
  <span>Chains notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="expiration/">
  <strong>Expiration</strong>
  <span>Expiration notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="validation/">
  <strong>Validation</strong>
  <span>Validation notes, checks, commands, and references.</span>
</a>

</div>
## Protocol Versions

| Version | Status | Notes |
|---|---|---|
| SSLv3 | Prohibited | POODLE vulnerability — disable everywhere |
| TLS 1.0 | Deprecated | PCI-DSS non-compliant after June 2018 |
| TLS 1.1 | Deprecated | No support in modern browsers |
| TLS 1.2 | Current minimum | Required for most compliance frameworks |
| TLS 1.3 | Preferred | Faster handshake; stronger cipher suites |

## Certificate and Handshake Inspection

```bash
## Check certificate details for a live service
echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | \
  openssl x509 -noout -text | grep -E "Subject:|Issuer:|Not Before:|Not After:|Subject Alternative Name" -A1

## Check expiry only
echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | \
  openssl x509 -noout -dates

## Show full TLS handshake (negotiated version + cipher)
openssl s_client -connect <host>:443 -servername <host> 2>&1 | \
  grep -E "Protocol|Cipher|Certificate chain|Verify"

## Force specific TLS version (testing)
openssl s_client -connect <host>:443 -tls1_2
openssl s_client -connect <host>:443 -tls1_3

## Check certificate chain completeness
openssl s_client -connect <host>:443 -showcerts 2>/dev/null | grep -E "^---$|subject=|issuer="
```

## Cipher Suite Audit

```bash
## Install testssl.sh for comprehensive audit
curl -O https://testssl.sh/testssl.sh
chmod +x testssl.sh
./testssl.sh <host>:443

## Quick cipher check with nmap
nmap --script ssl-enum-ciphers -p 443 <host>
```

## Server Configuration

**nginx — recommended TLS config:**
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;

## HSTS (once TLS is confirmed working)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

**Apache:**
```apache
SSLProtocol -all +TLSv1.2 +TLSv1.3
SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder on
SSLSessionTickets off
```

## OCSP Stapling Verification

```bash
## Check if OCSP stapling is working
openssl s_client -connect <host>:443 -status -servername <host> 2>/dev/null | \
  grep -A 10 "OCSP response"
```

## Certificate Validation

```bash
## Verify a certificate chain (cert.pem + intermediate.pem + root.pem)
openssl verify -CAfile root.pem -untrusted intermediate.pem cert.pem

## Check OCSP status
openssl ocsp \
  -issuer intermediate.pem \
  -cert cert.pem \
  -url $(openssl x509 -in cert.pem -noout -ocsp_uri) \
  -resp_text 2>/dev/null | grep "Cert Status"
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| SSL handshake failure | Negotiated version/cipher | Check both sides support same TLS version; update older client |
| Certificate not trusted | Chain completeness | Serve intermediate CA cert in chain; verify with `openssl verify` |
| HSTS pre-loaded but cert expired | HSTS + expiry | Renew cert before HSTS expiry; users will be blocked until cert valid |
| Mixed content warning | HTTP resources on HTTPS page | Update embedded resource URLs to HTTPS |
| Certificate name mismatch | SANs | Verify cert SANs include the hostname being accessed |
