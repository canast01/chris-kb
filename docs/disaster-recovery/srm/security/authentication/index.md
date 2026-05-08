# SRM Security — Authentication

## Site Pair Service Account

The SRM site pair connection uses a service account on each vCenter:

```
Account: svc-srm-pair@domain.local
Privileges: SRM plug-in permissions + read access to vCenter inventory
```

- Do not use a named personal account — must survive staff changes
- Rotate password every 90 days (coordinate rotation on both sites simultaneously to avoid pair disconnect)
- Document the account in the service account inventory in CMDB

To update credentials after rotation: SRM UI → Site Recovery → Sites → Edit Site Pair Credentials

## Certificate Management

Replace default self-signed certificates in production deployments:

1. Generate CSR on SRM server
2. Sign with internal CA (or public CA for partner-site connections)
3. Install certificate: SRM → vCenter → Site Recovery → Certificates → Replace

Certificates used by SRM:
- SRM ↔ vCenter: VMCA-issued or custom
- SRM ↔ SRM (inter-site): Must be mutually trusted (both sites' CAs in trust stores)
- SRM ↔ SRA: Inherits SRM trust store

Track expiry dates in certificate inventory; SRM stops functioning if certificates expire.
