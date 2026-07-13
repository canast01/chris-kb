---
tags:
  - networking
description: "TLS reference — certificate chain validation, cipher suites, SNI, mTLS, OCSP/CRL revocation, and common TLS failure diagnosis."
---
# TLS

<div class="kb-summary">
TLS reference — certificate chain validation, cipher suites, SNI, mTLS, OCSP/CRL revocation, and common TLS failure diagnosis.
</div>

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

<a class="kb-card" href="validation/"><strong>Validation</strong><span>Certificate chain validation, handshake verification, and openssl testing.</span></a>
<a class="kb-card" href="ciphers/"><strong>Cipher Suites</strong><span>TLS 1.2/1.3 cipher suite reference, weak cipher identification, and remediation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>TLS handshake failures, certificate errors, and SNI troubleshooting.</span></a>

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

```

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

```text title="Expected output"
Subject: CN = api.example.com, O = Example Corp, C = US
Issuer: CN = DigiCert Global CA G2, O = DigiCert Inc, C = US
Not Before: Jan 15 00:00:00 2023 GMT
Not After: Jan 14 23:59:59 2025 GMT
Subject Alternative Name: 
    DNS:api.example.com, DNS:*.example.com, DNS:example.com

notBefore=Jan 15 00:00:00 2023 GMT
notAfter=Jan 14 23:59:59 2025 GMT

Protocol  : TLSv1.3
Cipher    : TLS_AES_256_GCM_SHA384
Certificate chain
 0 s:CN = api.example.com, O = Example Corp, C = US
   i:CN = DigiCert Global CA G2, O = DigiCert Inc, C = US
Verify return code: 0 (ok)

CONNECTED(00000003)
depth=0 CN = api.example.com, O = Example Corp, C = US
verify OK

---BEGIN CERTIFICATE---
MIIFWTCCBEGgAwIBAgIQD8NVVaAfqJ1j7K4Q4slaQDANBgkqhkiG9w0BAQsFADBG
...
---END CERTIFICATE---
subject=CN = api.example.com, O = Example Corp, C = US
issuer=CN = DigiCert Global CA G2, O = DigiCert Inc, C = US
```

!!! warning "Common errors"
    **`unable to get local issuer certificate`** — Add the `-CAfile /etc/ssl/certs/ca-certificates.crt` flag or ensure your system's CA bundle is up-to-date with `update-ca-certificates`.
    **`error:1404B410:SSL routines:CT_PARSE_SCI_LIST:unexpected eof while parsing`** — The target host is not responding on port 443 or the hostname is incorrect; verify connectivity with `nc -zv <host> 443` first.
    **`Protocol : TLSv1.2` when testing with `-tls1_3`** — The server does not support TLS 1.3; check server configuration or use `-tls1_2` to verify the highest supported version.
```bash
## Install testssl.sh for comprehensive audit
curl -O https://testssl.sh/testssl.sh
chmod +x testssl.sh
./testssl.sh <host>:443

## Quick cipher check with nmap
nmap --script ssl-enum-ciphers -p 443 <host>
```
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
```apache
SSLProtocol -all +TLSv1.2 +TLSv1.3
SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder on
SSLSessionTickets off
```
```bash
## Check if OCSP stapling is working
openssl s_client -connect <host>:443 -status -servername <host> 2>/dev/null | \
  grep -A 10 "OCSP response"
```

```text title="Expected output"
OCSP response: 
======================================
OCSP Response Data:
    OCSP Response Status: successful (0x0)
    Response Type: Basic OCSP Response
    Version: 1 (0x0)
    Responder Id: C = US, O = Let's Encrypt, CN = R3
    Produced At: Jan 15 10:32:15 2024 GMT
    Responses:
    Certificate ID:
      Hash Algorithm: sha1
      Issuer Name Hash: 8D8C5EC3D85F4D67A13A535F941D142B
      Issuer Key Hash: 142EB317B75856CBAE500940E61FAF9D
      Serial Number: 03AB5891D116DCC8EF490A4528F247D2E1C
    This Update: Jan 15 10:32:15 2024 GMT
    Next Update: Jan 22 10:32:15 2024 GMT
    Cert Status: good
```

!!! warning "Common errors"
    **`OCSP response: none`** — The server is not configured to staple OCSP responses; enable OCSP stapling in your web server configuration (e.g., `ssl_stapling on;` in nginx or `SSLUseStapling on` in Apache).
    **`error in s_client`** — Verify the hostname and port are correct, the server is reachable, and TLS is enabled on that port using `nc -zv <host> 443` first.
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


```text title="Expected output"
cert.pem: OK
Cert Status: good
```

!!! warning "Common errors"
    **`error 20 at 0 depth lookup: unable to get local issuer certificate`** — Ensure the root.pem file contains the correct root CA certificate and is readable; verify the certificate chain is complete.
    **`Error querying OCSP responder`** — The OCSP responder may be unavailable or the URL may be incorrect; verify network connectivity and that the certificate's OCSP URI is valid with `openssl x509 -in cert.pem -noout -text | grep -A1 "OCSP"`.