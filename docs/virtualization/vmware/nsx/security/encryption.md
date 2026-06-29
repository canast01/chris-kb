---
tags:
  - nsx
  - nsx-4
  - security
  - vmware
---
# NSX — Encryption
![NSX — Encryption](../../../../assets/virtualization-vmware-nsx-security-encryption.svg)

```bash
# From a client machine — test TLS negotiation
openssl s_client -connect nsx-manager.example.local:443 -tls1   # Should fail (TLS 1.0 rejected)
openssl s_client -connect nsx-manager.example.local:443 -tls1_1 # Should fail (TLS 1.1 rejected)
openssl s_client -connect nsx-manager.example.local:443 -tls1_2 # Should succeed
openssl s_client -connect nsx-manager.example.local:443 -tls1_3 # Should succeed if TLS 1.3 enabled

# Check the presented certificate
openssl s_client -connect nsx-manager.example.local:443 -tls1_2 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer
```


```text title="Expected output"
CONNECTED(00000000)
139701234567890:error:1410D0B9:SSL routines:SSL_CTX_set_tlsext_host_name:tlsext alert fatal:../ssl/statem/statem_clnt.c:239:
connect:errno=1
---
CONNECTED(00000000)
139701234567890:error:1410D0B9:SSL routines:SSL_CTX_set_tlsext_host_name:tlsext alert fatal:../ssl/statem/statem_clnt.c:239:
connect:errno=1
---
CONNECTED(00000000)
depth=0 CN = nsx-manager.example.local, O = VMware, C = US
verify return:1
---
Certificate chain
 0 s:CN = nsx-manager.example.local, O = VMware, C = US
   i:CN = NSX-Manager-CA, O = VMware, C = US
---
CONNECTED(00000000)
depth=0 CN = nsx-manager.example.local, O = VMware, C = US
verify return:1
---
notBefore=Jan 15 08:32:14 2024 GMT
notAfter=Jan 14 08:32:14 2026 GMT
subject=CN = nsx-manager.example.local, O = VMware, C = US
issuer=CN = NSX-Manager-CA, O = VMware, C = US
```

!!! warning "Common errors"
    **`connect:errno=111`** — Verify NSX Manager is running and listening on port 443 with `curl -k https://nsx-manager.example.local/api/v1/node`.
    **`verify return:1 (self signed certificate)`** — This is expected for self-signed NSX certs; use `-CAfile` with your NSX CA bundle or ignore with `-showcerts` for validation purposes only.
    **`error:1410D0B9:SSL routines:SSL_CTX_set_tlsext_host_name:tlsext alert fatal`** — Confirm the hostname resolves correctly and matches the certificate CN with `nslookup nsx-manager.example.local` and `openssl x509 -in cert.pem -noout -text`.
```bash
# List all imported certificates
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/trust-management/certificates" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for c in d.get('results', []):
    cid   = c.get('id', '?')
    name  = c.get('display_name', '?')
    expiry = c.get('not_after', '?')
    print(f'  {cid:<40} {name:<30} expires={expiry}')
"

# Thumbprint of the API certificate (used for vCenter trust)
nsxcli
get certificate api thumbprint
```

```text title="Expected output"
aebc1234-5678-90ab-cdef-1234567890ab   nsx-manager-cert                expires=2026-03-15T14:22:00Z
  b2cd5678-90ab-cdef-1234-567890abcdef   vcenter-integration-cert        expires=2025-11-20T08:45:30Z
  c3de9012-34ab-cdef-1234-567890abcdef   backup-cert-old                 expires=2024-08-10T16:33:15Z
  d4ef3456-78cd-ef01-2345-67890abcdef1   edge-cluster-cert               expires=2027-01-05T09:18:42Z

nsx> get certificate api thumbprint
a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0

nsx> exit
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification, or import the NSX Manager's CA certificate into your system trust store.
    **`jq: command not found`** — Install `python3-json` or use the built-in `python3 -c` JSON parser as shown in the example instead of piping to `jq`.
    **`error: unauthorized (401)`** — Verify the admin credentials are correct and the user has API access permissions in NSX Manager's role-based access control settings.
```bash
# Step 1 — Generate a CSR on NSX Manager
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "CsrProperties",
    "display_name": "nsx-api-cert",
    "subject": {
      "attributes": [
        {"key": "CN", "value": "nsx-manager.example.local"},
        {"key": "O",  "value": "Corp Inc"},
        {"key": "C",  "value": "GB"}
      ]
    },
    "key_size": "2048",
    "algorithm": "RSA",
    "extensions": {
      "dns_names": ["nsx-manager.example.local"],
      "ip_addresses": ["10.0.0.50"]
    }
  }' \
  "https://<nsx-manager>/api/v1/trust-management/csrs" | python3 -m json.tool
```

```text title="Expected output"
{
  "resource_type": "CsrProperties",
  "id": "a7f3c2e1-9b4d-4f8a-b2c5-d8e9f1a3b5c7",
  "display_name": "nsx-api-cert",
  "pem": "-----BEGIN CERTIFICATE REQUEST-----\nMIICljCCAX4CAQAwQDELMAkGA1UEBhMCR0IxEDAOBgNVBAoTB0NvcnAgSW5jMRsw\nGQYDVQQDExJuc3gtbWFuYWdlci5leGFtcGxlLmxvY2FsMIIBIjANBgkqhkiG9w0B\nAQEFAAOCAQ8AMIIBCgKCAQEAyZ4k2vL8n9pQ5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2\nxL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5m\nK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ\n9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2\nmJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8q\nR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL\n9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4\npQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8v\nK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL5mK3vZ9xL2mJ8qR7vL9mN4pQ8vK2xL\n5mK3vZ
```
```bash
# Step 2 — Import the signed certificate
CERT_PEM=$(cat nsx-api-signed.crt | awk '{printf "%s\\n", $0}')
KEY_PEM=$(cat nsx-api.key | awk '{printf "%s\\n", $0}')

curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{
    \"pem_encoded\": \"${CERT_PEM}\",
    \"private_key\": \"${KEY_PEM}\"
  }" \
  "https://<nsx-manager>/api/v1/trust-management/certificates?action=import"
# Returns the certificate ID
```

```text title="Expected output"
{
  "certificate_id": "91a2c4e8-7f3b-4d2a-9e1c-5b6a3f8d2e4c",
  "pem_encoded": "-----BEGIN CERTIFICATE-----\nMIIDXTCCAkWgAwIBAgIJAKp8Z7vN4mK5MA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV\n...",
  "subject": "CN=nsx-manager.lab.local,O=Infrastructure,C=US",
  "issuer": "CN=Lab-Root-CA,O=Infrastructure,C=US",
  "valid_from": "2024-01-15T10:30:00Z",
  "valid_until": "2026-01-14T10:30:00Z",
  "key_size": 2048,
  "signature_algorithm": "sha256WithRSAEncryption",
  "resource_type": "Certificate",
  "self_link": "https://nsx-manager.lab.local/api/v1/trust-management/certificates/91a2c4e8-7f3b-4d2a-9e1c-5b6a3f8d2e4c"
}
```

!!! warning "Common errors"
    **`{"error_code":400,"error_message":"Invalid PEM encoding in request body"}`** — Verify certificate and key files are not corrupted and contain proper BEGIN/END markers by running `head -1 nsx-api-signed.crt` and `head -1 nsx-api.key`.
    **`{"error_code":401,"error_message":"Unauthorized"}`** — Confirm NSX Manager credentials are correct and the admin user has certificate management permissions.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command or import the NSX Manager's CA certificate into your system trust store.
```bash
# Step 3 — Apply the certificate to the API endpoint
curl -sk -u 'admin:password' \
  -X POST \
  "https://<nsx-manager>/api/v1/node/services/http?action=apply_certificate&certificate_id=<cert-id>"
```

```text title="Expected output"
{
  "service": "http",
  "status": "success",
  "certificate_id": "urn:uuid:a4f2c8e1-9b3d-47e2-8c1f-6d5a2e9f4b1c",
  "applied_at": "2024-01-15T14:32:18.456Z",
  "thumbprint": "3d:a4:f2:c8:e1:9b:3d:47:e2:8c:1f:6d:5a:2e:9f:4b",
  "expires": "2025-01-15T14:32:18Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification, or import the NSX Manager's CA certificate into your system trust store.
    **`{"error_code":400,"error_message":"Certificate ID not found or invalid"}`** — Verify the certificate exists on the NSX Manager by running `curl -sk -u 'admin:password' https://<nsx-manager>/api/v1/certificates` and confirm the certificate_id value.
    **`curl: (7) Failed to connect to <nsx-manager> port 443: Connection refused`** — Confirm the NSX Manager hostname/IP is correct and the API service is running with `curl -sk -u 'admin:password' https://<nsx-manager>/api/v1/node/services/http`.
```bash
# Check expiry of all NSX-managed certificates
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/trust-management/certificates?details=true" | \
  python3 -c "
import sys, json
from datetime import datetime, timezone
d = json.load(sys.stdin)
now = datetime.now(timezone.utc)
for c in d.get('results', []):
    name   = c.get('display_name', c.get('id','?'))
    expiry = c.get('not_after','')
    if expiry:
        exp_dt = datetime.fromisoformat(expiry.replace('Z','+00:00'))
        days   = (exp_dt - now).days
        flag   = '' if days > 60 else '  *** EXPIRING SOON' if days > 14 else '  *** EXPIRED/CRITICAL'
        print(f'  {name:<40} expires={expiry[:10]}  days_remaining={days}{flag}')
"
```

```text title="Expected output"
nsx-manager.corp.local              expires=2025-08-14  days_remaining=187
  nsx-edge-01.corp.local              expires=2025-06-22  days_remaining=125
  nsx-controller-01.corp.local        expires=2025-03-10  days_remaining=42  *** EXPIRING SOON
  nsx-controller-02.corp.local        expires=2024-12-18  days_remaining=-28  *** EXPIRED/CRITICAL
  api-cert-internal                   expires=2025-09-30  days_remaining=234
  backup-cert-old                     expires=2024-11-05  days_remaining=-72  *** EXPIRED/CRITICAL
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification, or import the NSX manager's CA certificate into your system trust store.
    **`jq: command not found`** — Ensure Python 3 is installed and the JSON parsing script is correctly formatted; alternatively, pipe to `jq '.results[] | {display_name, not_after}'` if jq is available.
    **`curl: (7) Failed to connect to <nsx-manager> port 443: Connection refused`** — Verify the NSX Manager hostname/IP is correct, the API service is running (`systemctl status nsx-manager`), and the management network is reachable.
```bash
# On NSX Manager node
nsxcli
set service syslog exporter siem-tls level info protocol TLS server 10.0.0.100 port 6514

# Verify
get service syslog exporters
```

```text title="Expected output"
NSX CLI (version 3.2.1.0.0)
> set service syslog exporter siem-tls level info protocol TLS server 10.0.0.100 port 6514
Syslog exporter 'siem-tls' configured successfully.

> get service syslog exporters
Exporter Name    Protocol  Server         Port  Level  Status
siem-tls         TLS       10.0.0.100     6514  info   connected
syslog-default   UDP       127.0.0.1      514   warn   connected
```

!!! warning "Common errors"
    **`Error: Exporter name 'siem-tls' already exists`** — Use a unique exporter name or delete the existing exporter with `delete service syslog exporter siem-tls` first.
    **`Error: Unable to connect to server 10.0.0.100:6514 - connection timeout`** — Verify the SIEM server is reachable and listening on port 6514 by running `nc -zv 10.0.0.100 6514` from the NSX Manager node.
    **`Error: TLS certificate validation failed for server 10.0.0.100`** — Import the SIEM server's CA certificate into NSX Manager using `set service syslog exporter siem-tls ca-cert <cert-path>`.
```bash
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{\"pem_encoded\": \"$(cat siem-ca.crt | awk '{printf "%s\\n", $0}')\"}" \
  "https://<nsx-manager>/api/v1/trust-management/certificates?action=import"
```


```text title="Expected output"
{
  "certificate_id": "d8f4c2a1-9e7b-4f3c-b1d6-2a5e8c9f0b3d",
  "pem_encoded": "-----BEGIN CERTIFICATE-----\nMIIDXTCCAkWgAwIBAgIJAKp8Z7c5Q9mNMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV\nBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX\naWRnaXRzIFB0eSBMdGQwHhcNMjMwNzE1MDkzMDAwWhcNMjQwNzE0MDkzMDAwWjBF\nMQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50\nZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB\nCgKCAQEA2x5Z...\n-----END CERTIFICATE-----\n",
  "resource_type": "TrustedCertificate",
  "system_owned": false
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification, or import the NSX manager's own certificate first.
    **`{"httpStatus":400,"error_code":107,"module_name":"common","error_message":"Invalid PEM format"}`** — Ensure the certificate file is valid PEM format and the awk command properly escapes newlines; test with `cat siem-ca.crt | head -2`.
    **`curl: (7) Failed to connect to <nsx-manager> port 443: Connection refused`** — Verify the NSX Manager hostname/IP is correct and the API service is running with `curl -sk https://<nsx-manager>/api/v1/cluster/status`.
## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## See also

- [NSX — Hardening](../hardening/)
- [NSX — Health Checks](../../operations/health-checks/)
