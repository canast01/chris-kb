---
tags:
  - san
  - security
---
# Cisco Nexus Dashboard — Security Authentication

*Applies to: Cisco MDS / NX-OS*
![Cisco Nexus Dashboard — Security Authentication](../../../../assets/san-cisco-nexus-dashboard-security-authentication.svg)

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Import corporate CA certificate for LDAPS trust
acs certificates import-ca --cert /tmp/corp-ca.crt --name corp-ldap-ca

# Verify
acs certificates show-ca
```


```text title="Expected output"
Last login: Thu Jan 16 14:32:18 2025 from 10.45.12.88

Nexus Dashboard CLI v3.2.1.4a
Type 'help' for command reference

nd-dc1-1# acs certificates import-ca --cert /tmp/corp-ca.crt --name corp-ldap-ca
Certificate imported successfully
Certificate Name: corp-ldap-ca
Thumbprint: a7:f3:2e:9c:14:b8:61:d5:47:3a:8f:22:e9:5b:1c:6d
Expiry: 2026-03-15 23:59:59 UTC
Status: Active

nd-dc1-1# acs certificates show-ca
CA Certificate: corp-ldap-ca
  Thumbprint: a7:f3:2e:9c:14:b8:61:d5:47:3a:8f:22:e9:5b:1c:6d
  Issued By: CN=Corporate Root CA,O=Example Corp,C=US
  Valid From: 2023-03-16 00:00:00 UTC
  Valid Until: 2026-03-15 23:59:59 UTC
  Status: Active
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Certificate file not found: /tmp/corp-ca.crt` | Verify the certificate file exists at the specified path and is readable by the ndadmin user. |
    | `Error: Invalid certificate format. Expected PEM or DER encoded X.509 certificate` | Ensure the certificate file is properly formatted; convert from PKCS#12 or other formats using `openssl x509 -in cert.p12 -out cert.crt`. |
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Nexus Dashboard — Access Control](../access-control/)
- [Nexus Dashboard — Hardening](../hardening/)
- [Nexus Dashboard — Encryption](../encryption/)
