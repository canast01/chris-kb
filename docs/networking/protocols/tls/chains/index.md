---
tags:
  - networking
description: "A certificate chain (or chain of trust) links a server certificate back to a trusted root CA through one or more intermediate CAs."
---
# TLS Certificate Chains

<div class="kb-summary">
A certificate chain (or chain of trust) links a server certificate back to a trusted root CA through one or more intermediate CAs.
</div>

If the chain is broken or incomplete, clients will reject the certificate.

## Chain Structure

```text
Root CA (self-signed, in OS/browser trust store)
  └── Intermediate CA (signed by Root CA)
        └── Server Certificate (signed by Intermediate CA)
```

The server presents its certificate plus all intermediate certificates. The client verifies each signature up to a trusted root.

## Why Chains Break

- Server configured with certificate only (no intermediate)
- Intermediate CA certificate not included in the bundle
- Wrong intermediate (from a different CA hierarchy)
- Intermediate and server certificate order reversed
- Root CA not in client's trust store (self-signed internal CA)

## Checking the Chain

```bash
# View full chain served by a live endpoint
openssl s_client -connect <hostname>:443 -servername <hostname>

# Output shows: Certificate chain
# 0 s:CN=web.example.com (server cert)
#   i:CN=Example Intermediate CA
# 1 s:CN=Example Intermediate CA
#   i:CN=Example Root CA

# Verify chain file locally
openssl verify -CAfile chain.pem server.crt

# Check chain order in a bundle file
openssl crl2pkcs7 -nocrl -certfile bundle.pem | \
  openssl pkcs7 -print_certs -noout
```


```text title="Expected output"
depth=0 CN=web.example.com
verify return:1
depth=1 CN=Example Intermediate CA
verify return:1
depth=2 CN=Example Root CA
verify return:1
Certificate chain
 0 s:CN=web.example.com
   i:CN=Example Intermediate CA
 1 s:CN=Example Intermediate CA
   i:CN=Example Root CA
 2 s:CN=Example Root CA
   i:CN=Example Root CA

server.crt: OK

subject=/CN=web.example.com
issuer=/CN=Example Intermediate CA
subject=/CN=Example Intermediate CA
issuer=/CN=Example Root CA
subject=/CN=Example Root CA
issuer=/CN=Example Root CA
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `verify error:num=20:unable to get local issuer certificate` | Add the missing intermediate CA to your chain.pem file or use `-CApath` to point to a directory containing root CAs. |
    | `error:0906D06C:PEM routines:PEM_read_bio:no start line` | Ensure bundle.pem contains valid PEM-formatted certificates with proper `-----BEGIN CERTIFICATE-----` headers. |
## Building a Chain Bundle

The bundle should be ordered: server cert → intermediate(s) → (optionally root).

```bash
# Concatenate into bundle
cat server.crt intermediate.crt > bundle.pem

# Optional: include root (some applications require it)
cat server.crt intermediate.crt root.crt > full-chain.pem

# Verify the bundle
openssl verify -CAfile root.crt -untrusted intermediate.crt server.crt
```


```text title="Expected output"
OK
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error 20 at 0 depth lookup: unable to get local issuer certificate` | Ensure the root certificate file path is correct and the certificate chain is complete; verify with `openssl x509 -in root.crt -text -noout`. |
    | `No such file or directory` | Confirm all three certificate files (server.crt, intermediate.crt, root.crt) exist in the current working directory using `ls -la *.crt`. |
## Configuring Chain in Common Web Servers

### nginx

```nginx
# nginx — combine cert and intermediates into one file
ssl_certificate     /etc/ssl/server-chain.pem;   # cert + intermediates
ssl_certificate_key /etc/ssl/server.key;

# Build the chain file:
# cat server.crt intermediate.crt > /etc/ssl/server-chain.pem
```

### Apache httpd

```apache
SSLCertificateFile    /etc/ssl/server.crt
SSLCertificateKeyFile /etc/ssl/server.key
SSLCACertificateFile  /etc/ssl/intermediate.crt  # or chain bundle
```

### HAProxy

```bash
# HAProxy expects cert + key + chain in one PEM file
cat server.crt intermediate.crt server.key > /etc/ssl/haproxy.pem
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: server.crt: No such file or directory` | Verify the certificate files exist in the current directory or provide absolute paths to their locations. |
    | `Permission denied` | Run the command with `sudo` or ensure your user has write permissions to `/etc/ssl/`. |
## Installing Internal CA Certificates

To make an internal CA trusted by Linux hosts:

```bash
# RHEL/Rocky
cp internal-ca.crt /etc/pki/ca-trust/source/anchors/
update-ca-trust

# Ubuntu/Debian
cp internal-ca.crt /usr/local/share/ca-certificates/
update-ca-certificates

# Verify
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt server.crt
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
Updating certificates in /etc/ssl/certs...
rehashing... done.
Running hooks in /etc/ca-certificates/update.d...
done.
verify OK
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `verify OK` | Ignore this; it indicates successful verification, not an error. |
    | `error 20 at 0 depth lookup: unable to get local issuer certificate` | The CA certificate was not properly installed; re-run `update-ca-certificates` after confirming the `.crt` file is in `/usr/local/share/ca-certificates/` with proper permissions. |
    | `cp: cannot stat 'internal-ca.crt': No such file or directory` | Verify the CA certificate file exists in the current working directory or provide the full path to the source file. |
## Online Chain Verification Tools

```bash
# SSL Labs (external)
# https://www.ssllabs.com/ssltest/

# Check chain via openssl — simulates client verification
openssl s_client -connect <hostname>:443 -servername <hostname> -verify_return_error

# Verify with specific CA bundle
curl --cacert /path/to/ca-bundle.pem https://<hostname>/
```


```text title="Expected output"
depth=0 C = US, ST = California, L = San Francisco, O = Acme Corp, CN = api.example.com
verify return:1
depth=1 C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 CA
verify return:1
depth=2 C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
verify return:1
DONE
---
  % Total    % Received % Xferd  Average Speed   Time    Current Dload  Upload   Current Left Speed
100   4521  100   4521    0     0   8432      0 --:--:-- 0:00:00 --:--:-- 0:00:00 100   4521  100   4521    0     0   8432      0 --:--:-- 0:00:00
<!DOCTYPE html>
<html>
<head><title>200 OK</title></head>
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `verify error:num=20:unable to get local issuer certificate` | Add the missing intermediate CA certificate to your bundle or use the system CA bundle with `curl -k` (if testing) or obtain the complete chain from your certificate provider. |
    | `curl: (60) SSL certificate problem: self signed certificate` | Either add the self-signed cert to your CA bundle with `cat /path/to/cert.pem >> /path/to/ca-bundle.pem`, or use `curl -k` for testing only. |
## Common Issues

| Symptom | Cause | Fix |
|---|---|---|
| `unable to get local issuer certificate` | Intermediate missing | Add intermediate CA to bundle |
| `certificate verify failed` | Internal CA not trusted | Install internal CA cert on client |
| `self signed certificate in certificate chain` | Root in chain but not in trust store | Install root CA or remove from chain |
| Chain shows only depth 0 | Server not sending intermediate | Configure server to send full chain |
| Chain correct in browser, fails in app | App uses its own trust store (Java) | Import CA into Java keystore: `keytool -import` |
