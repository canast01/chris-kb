# SRM Security — Encryption

## Firewall Ports

| Source | Destination | Port | Purpose |
|---|---|---|---|
| SRM Server | vCenter | 443 | vSphere API |
| SRM Server | Remote SRM Server | 443, 8095 | Site pair communication |
| SRM Server | Array/SRA | 443, 9090 | SRA API calls |
| vSphere Replication | Remote vSphere Replication | 44046 | Replication traffic |

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
