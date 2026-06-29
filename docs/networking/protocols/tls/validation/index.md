---
tags:
  - networking
---
# TLS Validation

<div class="kb-summary">
Use these commands to verify TLS configuration on servers, check certificate validity, diagnose handshake failures, and confirm correct chain presentation.
</div>

```d2
direction: down

quick_validation_live_endpoint: "Quick Validation — Live Endpoint" {shape: rectangle}
certificate_validity_checks: "Certificate Validity Checks" {shape: rectangle}
chain_validation: "Chain Validation" {shape: rectangle}
protocol_and_cipher_checks: "Protocol and Cipher Checks" {shape: rectangle}
curl_validation: "curl Validation" {shape: rectangle}
validating_a_certificate_file: "Validating a Certificate File" {shape: rectangle}

quick_validation_live_endpoint -> certificate_validity_checks: uses
certificate_validity_checks -> chain_validation: uses
chain_validation -> protocol_and_cipher_checks: uses
protocol_and_cipher_checks -> curl_validation: uses
curl_validation -> validating_a_certificate_file: uses
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


```text title="Expected output"
CONNECTED(00000003)
depth=2 C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
verify return:1
depth=1 C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
verify return:1
depth=0 CN = api.example.com
verify return:1
---
Certificate chain
 0 s:CN = api.example.com
   i:C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
 1 s:C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
   i:C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
 2 s:C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
   i:C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIFWTCCBEGgAwIBAgIQD8JsY4FIJV/LwV3+I80rFDANBgkqhkiG9w0BAQsFADB1
...
-----END CERTIFICATE-----
subject=CN = api.example.com
issuer=C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: RSA-PSS
Server Temp Key: X25519, 253 bits
---
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: A7F2B8C9D1E4F6A2B3C5D7E9F1A3B5C7
    Session-ID-ctx: 
    Master-Key: (hidden)
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    Start Time: 1704067200
    Timeout   : 7200 (sec)
    Verify return code: 0 (ok)
```

!!! warning "Common errors"
    **`verify error:num=20:unable to get local issuer certificate`** — Add the missing intermediate CA certificate to your system's CA bundle or use `openssl s_client -CAfile /path/to/ca-bundle.crt`.
    **`connect: Connection refused`** — Verify the hostname and port are correct, and that the service is listening on that port with `netstat -tlnp | grep :443`.
    **`Verify return code: 21 (unable to verify the first certificate)`** — Check that the server certificate chain is complete; the server may be missing the intermediate certificate in its configuration.
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


```text title="Expected output"
notBefore=Jan 15 08:23:45 2023 GMT
notAfter=Jan 15 08:23:45 2025 GMT
subject=CN = api.example.com, O = Example Corp, C = US
X509v3 Subject Alternative Name: 
    DNS:api.example.com, DNS:*.example.com, DNS:api-backup.example.com
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2021 CA1
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            0a:1b:2c:3d:4e:5f:6a:7b:8c:9d:ae:bf:c0:d1:e2:f3
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 2021 CA1
        Validity
            Not Before: Jan 15 08:23:45 2023 GMT
            Not After : Jan 15 08:23:45 2025 GMT
        Subject: CN = api.example.com, O = Example Corp, C = US
```

!!! warning "Common errors"
    **`connect: Connection refused`** — Verify the hostname is correct and the service is listening on port 443 with `netstat -tlnp | grep 443`.
    **`unable to get local issuer certificate`** — This is expected output from s_client; the issuer information is still extracted correctly by the piped openssl x509 command.
    **`error in x509 parsing`** — Ensure the certificate chain is complete by testing with `openssl s_client -connect <hostname>:443 -showcerts` to diagnose intermediate certificate issues.
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


```text title="Expected output"
Subject: CN = api.example.com, O = Example Corp, C = US
Issuer: CN = DigiCert Global CA G2, O = DigiCert Inc, C = US
Verify return code: 0 (ok)
```

!!! warning "Common errors"
    **`verify error:num=20:unable to get local issuer certificate`** — Add the missing intermediate CA certificate to your CA bundle or use `-partial_chain` flag to accept partial chains.
    **`s_client: No such file or directory`** — Verify the CA bundle path exists with `ls -la /etc/ssl/certs/ca-certificates.crt` and update the path if using a different distribution (e.g., `/etc/pki/tls/certs/ca-bundle.crt` on RHEL).
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


```text title="Expected output"
depth=0, CN = example.com
verify error:num=18:self signed certificate
verify return:1
depth=0, CN = example.com
verify return:1
---
Certificate chain
 0 s:/CN=example.com
   i:/CN=example.com
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKp8Z7x9vQ2kMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
-----END CERTIFICATE-----
subject=/CN=example.com
issuer=/CN=example.com
---
No client certificate CA names sent
Peer signing digest: SHA256
Server Temp Key: ECDH, P-256, 256 bits
---
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : ECDHE-RSA-AES256-GCM-SHA384
    Session-ID: A7F3B2C1D4E5F6A7B8C9D0E1F2A3B4C5
    Master-Key: 8F7E6D5C4B3A2F1E0D9C8B7A6F5E4D3C2B1A0F9E8D7C6B5A4F3E2D1C0B9A8F7E6D5C4B3A2F1E0D9C8B7A6F5E4D3C2B1A0F9E8D7C6B5A4F3E2D1C0B9A8F
    Key-Arg   : None
    Compression: NONE
    Expansion: NONE
    Start Time: 1704067200
    Timeout   : 7200 (sec)
    Verify return code: 0 (ok)

Protocol  : TLSv1.3
Cipher    : TLS_AES_256_GCM_SHA384
Session reused: 0

alert handshake failure

Starting Nmap 7.92 ( https://nmap.org ) at Mon Jan 01 12:00:00 2024
Nmap scan report for example.com (192.0.2.45)
Host is up (0.042s latency).

PORT    STATE SERVICE
443/tcp open  https

| ssl-enum-ciphers:
|   TLSv1.2:
|     ciphers (8):
|       ECDHE-RSA-AES256-GCM-SHA384 - strong
|       ECDHE-RSA-AES128-GCM-SHA256 - strong
|       ECDHE-RSA-CHACHA20-POLY1305 - strong
|       AES256-GCM-SHA384 - strong
|     least strength: strong
|   TLSv1.3:
|     ciphers (3):
|       TLS_AES_256_GCM_SHA384 - strong
|       TLS_CHACHA20_POLY1305_SHA256 - strong
|       TLS_AES_128_GCM_SHA256 - strong
|     least strength: strong
|_
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


```text title="Expected output"
* Trying 203.0.113.42:443...
* Connected to prod-api.internal (203.0.113.42) port 443 (#0)
* ALPN: offers h2
* TLSv1.3 (OUT), TLS handshake, Client Hello (1):
* TLSv1.3 (IN), TLS handshake, Server Hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=prod-api.internal,O=Acme Corp,C=US
*  issuer: CN=Acme Internal CA,O=Acme Corp,C=US
*  expire date: Apr 15 09:22:31 2026 GMT
*  common name: prod-api.internal (matched)
*  issuer certificate CN=Acme Internal CA,O=Acme Corp,C=US
* SSL certificate verify ok.
< HTTP/1.1 200 OK
< Content-Type: application/json
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the self-signed CA to your system trust store or use `--cacert /path/to/ca.pem` to specify the certificate bundle.
    **`curl: (51) Unable to communicate securely with peer: requested domain name does not match the server's certificate`** — Verify the hostname matches the certificate CN/SAN, or use `-k` flag only for testing (never in production).
    **`curl: (77) error setting certificate verify locations`** — Ensure the CA bundle path is correct and readable with `ls -la /path/to/internal-ca.pem`.
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


```text title="Expected output"
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 04:a1:f2:8e:9c:3d:7b:5e (hex)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = US, O = Example CA, CN = Example Root CA
        Validity
            Not Before: Jan 15 10:22:33 2024 GMT
            Not After : Jan 14 10:22:33 2025 GMT
        Subject: C = US, O = Example Corp, CN = api.example.com
        Public-Key: (2048 bit, RSA)
        X509v3 extensions:
            X509v3 Subject Alternative Name: 
                DNS:api.example.com, DNS:*.example.com
d41d8cd98f00b204e9800998ecf8427e  -
d41d8cd98f00b204e9800998ecf8427e  -
d41d8cd98f00b204e9800998ecf8427e  -
d41d8cd98f00b204e9800998ecf8427e  -
cert.pem: OK
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the cert.pem file exists and is a valid PEM-formatted certificate, not DER or another format.
    **`unable to load Private Key`** — Check that key.pem is readable and contains a valid RSA private key; convert from PKCS#8 if needed with `openssl pkey -in key.pem -traditional -out key.pem`.
    **`error 20 at 0 depth lookup: unable to get local issuer certificate`** — Add the root CA certificate to the trust store or provide it with `-CAfile`, and ensure the certificate chain is complete with `-untrusted intermediate.crt`.
## OCSP / Revocation Check

```bash
# Get OCSP URL from certificate
openssl x509 -in cert.pem -noout -ocsp_uri

# Query OCSP responder
openssl ocsp -issuer intermediate.crt -cert cert.pem \
  -url <ocsp-url> -resp_text

# Expected: "cert.pem: good"
```


```text title="Expected output"
http://ocsp.digicert.com

Responder URL: http://ocsp.digicert.com
Cert status: good
This Update: Jan 15 10:23:45 2024 GMT
Next Update: Jan 22 10:23:45 2024 GMT

cert.pem: good
```

!!! warning "Common errors"
    **`Error querying OCSP responder`** — Verify the OCSP URL is correct and accessible by testing with `curl -I <ocsp-url>` first.
    **`issuer certificate does not have OCSP signing capability`** — Use the correct intermediate CA certificate that signed the end-entity certificate, or obtain the OCSP signing certificate from your CA.
    **`socket: Connection refused`** — Ensure your firewall allows outbound HTTPS to the OCSP responder URL and check network connectivity with `ping` or `nc`.
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


```text title="Expected output"
Cloning into 'testssl.sh'...
remote: Enumerating objects: 12847, done.
remote: Receiving objects: 100% (12847/12847), done.
Resolving deltas: 100% (8934/8934), done.

 Testing api.example.com:443

 Protocol  SSLv2      DISABLED
 Protocol  SSLv3      DISABLED
 Protocol  TLSv1      DISABLED
 Protocol  TLSv1.1    DISABLED
 Protocol  TLSv1.2    ENABLED
 Protocol  TLSv1.3    ENABLED

 Cipher Suites (TLSv1.3)
 TLS_AES_256_GCM_SHA384                   ECDHE           256 bits      PASS
 TLS_CHACHA20_POLY1305_SHA256             ECDHE           256 bits      PASS

 Cipher Suites (TLSv1.2)
 ECDHE-RSA-AES256-GCM-SHA384              ECDHE           256 bits      PASS
 ECDHE-RSA-CHACHA20-POLY1305              ECDHE           256 bits      PASS
 ...

 Certificate Information
 Subject CN=api.example.com
 Issuer CN=Let's Encrypt Authority X3
 Not Before 2023-06-15
 Not After  2024-09-13
 Days until expiry: 287 days
 SANs: api.example.com, *.api.example.com

 Vulnerabilities
 POODLE (SSLv3)                           NOT VULNERABLE
 BEAST                                    NOT VULNERABLE
 ROBOT                                    NOT VULNERABLE
 Heartbleed                               NOT VULNERABLE
```

!!! warning "Common errors"
    **`./testssl.sh: command not found`** — Ensure the script has execute permissions with `chmod +x testssl.sh` and run from the correct directory.
    **`ERROR: couldn't connect to host:port <hostname>:443`** — Verify the hostname is resolvable and port 443 is accessible; check firewall rules and DNS with `nslookup <hostname>`.
    **`bash: git: command not found`** — Install git using your package manager (`apt install git` on Debian/Ubuntu or `brew install git` on macOS).
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
