# SRM Security — Authentication

```
┌──────────────────────────────────────── SRM — Authentication ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  SRM — Authentication Methods                                 │   │
│   │        vCenter SSO / AD integration; SRM admin role; site-pairing certificate exchange        │   │
│   │                 Management UI: HTTPS on 443 (SRM HTTPS) — browser-based login                 │   │
│   │               API: bearer token or service account; rotate credentials quarterly              │   │
│   │                 Inter-component: certificate-based mutual TLS between engines                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Human Access                 │  │                Machine Access               │   │
│   │            AD / LDAP integration             │  │               Service account               │   │
│   │              SAML SSO optional               │  │               API key / token               │   │
│   │                 MFA via IdP                  │  │               Certificate auth              │   │
│   │            Session timeout 15 min            │  │              Rotate every 90 d              │   │
│   │              Audit login events              │  │             Vault-stored secrets            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Site Pair Service Account

The SRM site pair connection uses a service account on each vCenter:

```text
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
