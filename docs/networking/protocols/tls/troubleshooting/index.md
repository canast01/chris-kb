---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
description: "TLS troubleshooting — certificate chain validation failures, handshake timeouts, cipher negotiation errors, SNI mismatches, and expired certificate..."
---
# TLS — Troubleshooting

<div class="kb-summary">
TLS troubleshooting — certificate chain validation failures, handshake timeouts, cipher negotiation errors, SNI mismatches, and expired certificate diagnosis.
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
quick_diagnosis: "Quick Diagnosis" {shape: rectangle}
common_errors_and_fixes: "Common Errors and Fixes" {shape: rectangle}
certificate_chain_validation: "Certificate Chain Validation" {shape: rectangle}
sni_issues: "SNI Issues" {shape: rectangle}
mtls_troubleshooting: "mTLS Troubleshooting" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> quick_diagnosis: investigate
symptom -> common_errors_and_fixes: investigate
symptom -> certificate_chain_validation: investigate
symptom -> sni_issues: investigate
symptom -> mtls_troubleshooting: investigate
symptom -> verify_resolution: investigate
quick_diagnosis -> resolution
common_errors_and_fixes -> resolution
certificate_chain_validation -> resolution
sni_issues -> resolution
mtls_troubleshooting -> resolution
verify_resolution -> resolution
```

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Quick Diagnosis

```bash
# Test TLS handshake and show certificate chain
openssl s_client -connect host:443 -servername host.example.com </dev/null 2>&1 | \
  grep -E 'subject|issuer|verify|SSL-Session|Protocol|Cipher'

# Check certificate expiry
echo | openssl s_client -connect host:443 -servername host.example.com 2>/dev/null | \
  openssl x509 -noout -dates

# Check which TLS versions are accepted
for ver in tls1 tls1_1 tls1_2 tls1_3; do
  echo -n "$ver: "
  echo | openssl s_client -connect host:443 -"$ver" 2>&1 | grep -E 'Protocol|connect: Connection refused|alert'
done
```


```text title="Expected output"
subject=CN = host.example.com, O = Example Corp, C = US
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2021 CA1
verify return:1
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
notBefore=Jan 15 10:22:33 2024 GMT
notAfter=Jan 14 10:22:32 2025 GMT
tls1: alert handshake failure
tls1_1: alert handshake failure
tls1_2: Protocol  : TLSv1.2
tls1_3: Protocol  : TLSv1.3
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `connect: Connection refused` | Verify the host is reachable and listening on port 443 with `nc -zv host 443`. |
    | `alert handshake failure` | The server does not support that TLS version; check server configuration or use a supported version like TLSv1.2 or TLSv1.3. |
    | `verify return:0` | The certificate chain is invalid; check that the server is presenting the complete chain or that your system's CA bundle is up-to-date with `update-ca-certificates`. |
## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `CERTIFICATE_VERIFY_FAILED` | CA not trusted by client | Install CA cert in client trust store |
| `SSL_ERROR_RX_RECORD_TOO_LONG` | Plain HTTP on TLS port | Check if server is returning HTTP not HTTPS |
| `ERR_CERT_DATE_INVALID` | Certificate expired | Renew certificate |
| `ERR_CERT_COMMON_NAME_INVALID` | CN/SAN doesn't match hostname | Check SAN; use `openssl x509 -noout -text` |
| `SSL_ERROR_HANDSHAKE_FAILURE_ALERT` | No cipher in common | Check `ssl_ciphers` config; client may not support TLS 1.3 |
| `ERR_SSL_PROTOCOL_ERROR` | TLS version mismatch | Enable TLS 1.2+ on server; update client if it only supports < TLS 1.2 |

## Certificate Chain Validation

```bash
# Full chain verification
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/server.crt

# Check if intermediate cert is included in bundle
openssl s_client -connect host:443 2>/dev/null | openssl x509 -noout -subject -issuer

# Build chain manually for verification
cat server.crt intermediate.crt > chain.pem
openssl verify -CAfile root-ca.crt chain.pem
```


```text title="Expected output"
/etc/ssl/certs/server.crt: OK
subject=CN = example.com, O = Example Corp, C = US
issuer=CN = Example Intermediate CA, O = Example Corp, C = US
(no output — command completes silently)
chain.pem: OK
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `/etc/ssl/certs/server.crt: error 20 at 0 depth lookup: unable to get local issuer certificate` | Add the intermediate certificate to your CA bundle or verify the intermediate cert is in the correct directory. |
    | `error:0900006e:PEM routines:PEM_read_bio:no start line` | Ensure the certificate file is in valid PEM format and not corrupted; check with `file /etc/ssl/certs/server.crt`. |
## SNI Issues

```bash
# Without SNI (older clients)
openssl s_client -connect host:443

# With SNI (required for virtual hosting / CDN)
openssl s_client -connect host:443 -servername actual.hostname.com

# Difference: check if different certificates are presented
```


```text title="Expected output"
# Without SNI (older clients)
depth=0 CN = *.cdn.example.com
verify error:num=20:unable to verify the first certificate
verify return:1
---
Certificate chain
 0 s:/CN=*.cdn.example.com
   i:/C=US/O=Let's Encrypt/CN=R3
-----BEGIN CERTIFICATE-----
MIIFXzCCBEegAwIBAgISA7k8z1...
-----END CERTIFICATE-----
---
Server certificate
subject=/CN=*.cdn.example.com
issuer=/C=US/O=Let's Encrypt/CN=R3
---

# With SNI (required for virtual hosting / CDN)
depth=0 CN = api.example.com
verify error:num=20:unable to verify the first certificate
verify return:1
---
Certificate chain
 0 s:/CN=api.example.com
   i:/C=US/O=Let's Encrypt/CN=R3
-----BEGIN CERTIFICATE-----
MIIFYzCCBEugAwIBAgISBnK9p2...
-----END CERTIFICATE-----
---
Server certificate
subject=/CN=api.example.com
issuer=/C=US/O=Let's Encrypt/CN=R3
---
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `connect: Connection refused` | Verify the host is reachable and listening on port 443 with `nc -zv host 443`. |
    | `error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed` | Add `-showcerts` to inspect the full chain, or use `-CAfile /etc/ssl/certs/ca-certificates.crt` if the CA bundle is missing. |
    | `error:1408F10B:SSL routines:ssl3_get_cipher_list:no ciphers available` | The server may require specific TLS versions; try adding `-tls1_2` or `-tls1_3` to force a protocol version. |
## mTLS Troubleshooting

```bash
# Present client certificate
openssl s_client -connect host:443 \
  -cert client.crt -key client.key \
  -CAfile ca.crt

# Error: 'no certificate returned' → server not configured for mTLS
# Error: 'alert certificate required' → server requires mTLS but no cert presented
```


```text title="Expected output"
CONNECTED(00000000)
depth=0 /C=US/ST=California/L=San Francisco/O=Example Corp/CN=host.example.com
verify return:1
---
Certificate chain
 0 s:/C=US/ST=California/L=San Francisco/O=Example Corp/CN=host.example.com
   i:/C=US/ST=California/O=Example Corp/CN=Example Root CA
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIDazCCAlOgAwIBAgIUK7x8n3+vZr4Q9mJ5pL2k9vZ8xQowDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yNDAxMTUxMDMwMDBaFw0yNTAx
-----END CERTIFICATE-----
subject=/C=US/ST=California/L=San Francisco/O=Example Corp/CN=host.example.com
issuer=/C=US/ST=California/O=Example Corp/CN=Example Root CA
---
No client certificate CA names sent
---
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: A7F3B2C1D9E4F5A6B8C2D1E3F4A5B6C7
    Master-Key: 2F4A5B6C7D8E9F0A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0C1D2E3F
    Key-Arg   : None
    Compression: None
    Expansion : None
    Start Time: 1705318200
    Timeout   : 7200 (sec)
    Verify return code: 0 (ok)
---
DONE
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure` | Verify the client certificate and key are valid and match the server's expectations; check that the CA file contains the correct root certificate. |
    | `error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed` | Ensure the CA file specified with `-CAfile` contains the issuing CA certificate for the server's certificate chain. |
    | `error:02001002:system library:fopen:No such file or directory` | Verify the paths to `client.crt`, `client.key`, and `ca.crt` are correct and the files exist in the current directory or use absolute paths. |
---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Certificates](../certificates/)
- [Chains](../chains/)
- [Ciphers](../ciphers/)
- [Expiration](../expiration/)
- [Validation](../validation/)
- [TLS — Overview](../)
