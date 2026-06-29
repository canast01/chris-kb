---
tags:
  - operations
  - security
---
# Certificate Trust Store Management

<div class="kb-summary">
Adding CA certificates to OS and application trust stores so that TLS connections to internal services succeed. Covers Linux (RHEL, Ubuntu/Debian), Windows (machine store and GPO), Java keystores, and verification commands.
</div>

```d2
direction: down

ubuntu_debian: "Ubuntu / Debian" {shape: rectangle}
rhel_rocky_almalinux: "RHEL / Rocky / AlmaLinux" {shape: rectangle}
windows_local_machine_store: "Windows — Local Machine Store" {shape: rectangle}
windows_gpo_domain_distribution: "Windows — GPO (Domain Distribution)" {shape: rectangle}
java_keystore: "Java Keystore" {shape: rectangle}
verification_commands: "Verification Commands" {shape: rectangle}

ubuntu_debian -> rhel_rocky_almalinux: uses
rhel_rocky_almalinux -> windows_local_machine_store: uses
windows_local_machine_store -> windows_gpo_domain_distribution: uses
windows_gpo_domain_distribution -> java_keystore: uses
java_keystore -> verification_commands: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Ubuntu / Debian

```bash
cp internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt
update-ca-certificates
# Verify
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt server.crt
```


```text title="Expected output"
cp: created directory '/usr/local/share/ca-certificates' (if needed)
Processing triggers for ca-certificates (20230311ubuntu1) ...
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ssl/certs/post-update-hooks.d...
done.
OK
server.crt: OK
```

!!! warning "Common errors"
    **`cp: cannot create regular file '/usr/local/share/ca-certificates/internal-ca.crt': Permission denied`** — Run the command with `sudo` or as root.
    **`error 18 at 0 depth lookup: self signed certificate`** — The CA certificate itself is self-signed; use `openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt -untrusted internal-ca.crt server.crt` if server.crt is signed by the intermediate CA.
## RHEL / Rocky / AlmaLinux

```bash
cp internal-ca.crt /etc/pki/ca-trust/source/anchors/internal-ca.crt
update-ca-trust extract
# Verify
trust list | grep "internal-ca"
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
     internal-ca
       type: certificate
       class: root-ca
       sha256: 3f7e2a1b9c4d8e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e
       expires: 2034-11-22 14:32:10 UTC
       sha1: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b
```

!!! warning "Common errors"
    **`cp: cannot stat 'internal-ca.crt': No such file or directory`** — Verify the certificate file exists in the current directory or provide the full path to the source certificate.
    **`update-ca-trust: command not found`** — Install the ca-certificates package using your distribution's package manager (apt-get install ca-certificates on Debian/Ubuntu, or yum install ca-certificates on RHEL/CentOS).
    **`trust list | grep "internal-ca"` returns no results** — Confirm the certificate was successfully copied to /etc/pki/ca-trust/source/anchors/ and that update-ca-trust extract completed without errors.
## Windows — Local Machine Store

```powershell
# Import CA cert to Trusted Root CA store on a single machine
certutil -addstore "Root" internal-ca.crt

# Verify
certutil -viewstore -enterprise Root | findstr "Corp"
```

## Windows — GPO (Domain Distribution)

1. Open **Group Policy Management** and create or edit a GPO linked to the domain.
2. Navigate to: `Computer Configuration → Windows Settings → Security Settings → Public Key Policies → Trusted Root Certification Authorities`
3. Right-click → **Import** → select the CA certificate file.
4. Apply the GPO and run `gpupdate /force` on a test machine.
5. Verify: open `certlm.msc` → Trusted Root Certification Authorities → check the CA appears.

This distributes the Root CA certificate to all domain-joined machines automatically at next Group Policy refresh.

## Java Keystore

```bash
# Import CA cert into JVM trust store
keytool -import \
  -alias internal-ca \
  -file internal-ca.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit \
  -noprompt

# Verify
keytool -list -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit | grep internal-ca
```


```text title="Expected output"
Owner: root, Permissions: 644
Certificate was added to keystore
internal-ca, Jan 15, 2025, trustedCertEntry, Certificate fingerprint (SHA-256): 8F:2A:B4:C9:E1:D7:3F:5B:A2:C8:E4:F1:9D:6B:2C:A7:E9:F3:1A:4D:B5:C2:E8:F4:2B:6A:D1:E5:3C:7F:A9
```

!!! warning "Common errors"
    **`keytool error: java.io.FileNotFoundException: /path/to/jdk/lib/security/cacerts (No such file or directory)`** — Verify `$JAVA_HOME` is set correctly with `echo $JAVA_HOME` and points to a valid JDK installation.
    **`keytool error: java.lang.Exception: Certificate already exists with alias <internal-ca>`** — Delete the existing certificate first using `keytool -delete -alias internal-ca -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit`.
    **`keytool error: java.lang.Exception: Invalid keystore format`** — Ensure the cacerts file has not been corrupted; restore from backup or verify file permissions with `ls -l $JAVA_HOME/lib/security/cacerts`.
---

## Verification Commands

### openssl Chain Verification

```bash
# Full chain verification
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt server.crt

# Verify chain from a specific CA file
openssl verify -CAfile internal-ca.crt -untrusted intermediate.crt server.crt

# Inspect certificate details
openssl x509 -in server.crt -noout -text | grep -E "Subject:|Issuer:|Not After|Not Before|DNS:"

# Check certificate fingerprint (compare with expected)
openssl x509 -in server.crt -noout -fingerprint -sha256

# Test live TLS trust from the OS
openssl s_client -connect <hostname>:443 -CAfile /etc/ssl/certs/ca-certificates.crt </dev/null 2>&1 | grep -E "Verify return|Certificate chain"
```


```text title="Expected output"
depth=0, verify ok
Subject: CN=server.example.com, O=Example Corp, C=US
Issuer: CN=Internal CA, O=Example Corp, C=US
Not Before: Jan 15 10:23:45 2024 GMT
Not After: Jan 15 10:23:45 2025 GMT
DNS: server.example.com, DNS: *.example.com
SHA256 Fingerprint=A1:B2:C3:D4:E5:F6:07:18:29:3A:4B:5C:6D:7E:8F:90:A1:B2:C3:D4:E5:F6:07:18:29:3A:4B:5C:6D:7E
Verify return code: 0 (ok)
Certificate chain
 0 s:CN=server.example.com
   i:CN=Internal CA
```

!!! warning "Common errors"
    **`verify error:num=20:unable to get local issuer certificate`** — Add the issuing CA certificate to the trust store or use `-untrusted` flag with the intermediate certificate path.
    **`verify error:num=10:certificate has expired`** — Renew the certificate before its "Not After" date or check system time synchronization with `timedatectl`.
    **`error:0A000086:SSL routines::certificate verify failed`** — Ensure the CA bundle file path is correct and readable, or verify the certificate chain is complete with all intermediate certificates included.
### TLS Debug

```bash
# Full TLS handshake trace
openssl s_client -connect <host>:443 -showcerts </dev/null

# Check what CA signed the certificate
openssl s_client -connect <host>:443 </dev/null 2>/dev/null | openssl x509 -noout -issuer

# curl verbose TLS debug
curl -v --cacert /path/to/internal-ca.crt https://<host>/endpoint

# Python — test with custom CA
REQUESTS_CA_BUNDLE=/path/to/internal-ca.crt python3 -c "import requests; print(requests.get('https://<host>').status_code)"
```


```text title="Expected output"
CONNECTED(00000000)
depth=2 C = US, O = Internal Root CA, CN = Internal Root CA v3
verify return:1
depth=1 C = US, O = Internal Intermediate CA, CN = Internal Intermediate CA
verify return:1
depth=0 C = US, ST = California, L = San Francisco, O = ACME Corp, CN = api.acme.internal
verify return:1
---
Certificate chain
 0 s:C = US, ST = California, L = San Francisco, O = ACME Corp, CN = api.acme.internal
   i:C = US, O = Internal Intermediate CA, CN = Internal Intermediate CA
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIUZ7k9nQ2mK8vL5pQ9xR8K3vF7d2swDQYJKoZIhvcNAQEL
...
-----END CERTIFICATE-----
issuer=C = US, O = Internal Intermediate CA, CN = Internal Intermediate CA
*   Trying 10.42.8.15:443...
* Connected to api.acme.internal (10.42.8.15) port 443 (#0)
* TLS 1.3 (OUT), TLS handshake, Client hello (1):
* TLS 1.3 (IN), TLS handshake, Server hello (2):
* TLS 1.3 (IN), TLS handshake, Certificate (11):
* TLS 1.3 (IN), TLS handshake, Finished (20):
* TLS 1.3 (OUT), TLS change cipher spec (1):
* TLS 1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate:
*  subject: C=US; ST=California; L=San Francisco; O=ACME Corp; CN=api.acme.internal
*  issuer: C=US; O=Internal Intermediate CA; CN=Internal Intermediate CA
*  SSL certificate verify ok.
> GET /endpoint HTTP/1.1
< HTTP/1.1 200 OK
200
```

!!! warning "Common errors"
    **`verify error:num=20:unable to get local issuer certificate`** — Add the intermediate and root CA certificates to your system trust store or specify them explicitly with `--cacert` or `REQUESTS_CA_BUNDLE`.
    **`curl: (60) SSL certificate problem: self signed certificate in certificate chain`** — Provide the full certificate chain (root + intermediate) in a single PEM file, or use `curl -k` to skip verification for testing only.
    **`requests.exceptions.SSLError: HTTPSConnectionPool(host='<host>', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationFailed(...)))`** — Ensure the `REQUESTS_CA_BUNDLE` path is correct and readable, or set `REQUESTS_CA_BUNDLE` to the absolute path of your internal CA certificate.
### Bulk Expiry Check

```bash
# Check expiry of a file
openssl x509 -in server.crt -noout -enddate

# Check expiry on a live endpoint
echo | openssl s_client -connect <host>:443 2>/dev/null | openssl x509 -noout -enddate

# Bulk check for certs expiring within 30 days
for cert in /etc/ssl/certs/*.crt; do
  expiry=$(openssl x509 -in "$cert" -noout -enddate 2>/dev/null | cut -d= -f2)
  if openssl x509 -in "$cert" -noout -checkend 2592000 2>/dev/null; then :
  else echo "EXPIRING: $cert — $expiry"; fi
done
```


```text title="Expected output"
notAfter=Jan 15 12:34:56 2025 GMT

depth=0 CN = api.example.com
verify return:1
notAfter=Jan 15 12:34:56 2025 GMT

EXPIRING: /etc/ssl/certs/old-api.crt — Jan  8 09:22:15 2025 GMT
EXPIRING: /etc/ssl/certs/staging.crt — Jan 12 14:50:33 2025 GMT
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the certificate file exists and is readable with `ls -la` and check the file path is correct.
    **`unable to connect to <host>:443`** — Ensure the host is reachable, the port is correct, and no firewall is blocking the connection with `nc -zv <host> 443`.
    **`Certificate will expire`** — Renew the certificate immediately using your CA or certificate management tool before the expiry date passes.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificates — Procedures](../procedures/)
- [Certificates — Health Checks](../health-checks/)
- [Certificates — CLI Reference](../cli-reference/)
- [Certificates — Scripts](../scripts/)
- [Certificates — Backup and Restore](../backup-restore/)
- [Certificates — Install and Upgrade](../install-upgrade/)
- [Certificates — Common Issues](../../troubleshooting/common-issues/)
