# SRM — Encryption


<div class="kb-summary">
Encryption reference covering Encryption at Recovery Site, Certificate Management for SRM Server, SRA Credential Storage Encryption, FIPS Mode.
</div>

  TLS Encryption Coverage
```text
┌───────────────────────────────────────────────────────────────┐
│  Traffic Path                        Encryption               │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ SRM ↔ SRM (site pairing, TCP 9086)    TLS 1.2+       │     │
│  │ SRM ↔ vCenter (TCP 443)               TLS 1.2+       │     │
│  │ SRM ↔ Storage Array SRA (TCP 443)     TLS 1.2+       │     │
│  │ VRA ↔ VRA mgmt (TCP 44046)            TLS 1.2+       │     │
│  │ ESXi ──► VRA replication (TCP 31031)  Optional AES   │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                               │
│  Enable per-VM replication encryption:                        │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ vCenter → [VM] → Configure Replication → Edit        │     │
│  │   Enable Replication Data Encryption: Yes (AES-256)  │     │
│  └──────────────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────── VMware SRM — Encryption ───────────────────────────────────────┐
│                                                                                                       │
│  SRM encrypts management traffic via TLS; replication traffic encryption depends on                   │
│  the replication method (vSphere Replication uses TLS; array replication varies).                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          SRM Management Encryption           │  │            Replication Encryption           │   │
│   │              All APIs: TLS 1.2+              │  │          vSphere Rep: TLS in-flight         │   │
│   │            Site pair: mutual TLS             │  │             ABR: array-specific             │   │
│   │            UI access: HTTPS only             │  │             Dell SRDF: encrypted            │   │
│   │         SQL: TLS to local/remote DB          │  │            NetApp SnapMirror: TLS           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SRM management uses TLS; verify replication traffic encryption with storage team.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Data at Rest                 │  │            Certificate Standards            │   │
│   │              VM disks: vSAN enc              │  │           SRM cert: enterprise PKI          │   │
│   │             SQL DB: TDE optional             │  │               TLS 1.2 minimum               │   │
│   │         Replica VMs: same as source          │  │             Cert expiry: monitor            │   │
│   │         Windows: BitLocker on CS VM          │  │            Replace: re-pair sites           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Replication traffic traverses WAN; verify WAN encryption (IPSEC/MPLS) for ABR;                       │
│  vSphere Replication encrypts its own traffic with TLS.                                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+      = minimum for SRM management and site pair traffic                                     │
│  Mutual TLS    = both SRM Servers present certs to each other                                         │
│  vSphere Rep TLS= vSphere Replication encrypts replication traffic                                    │
│  ABR           = Array-Based Replication; encryption varies by array                                  │
│  SRDF          = Dell EMC replication; supports encryption                                            │
│  SnapMirror    = NetApp replication; TLS between arrays                                               │
│  TDE           = Transparent Data Encryption; SQL Server feature                                      │
│  BitLocker     = Windows disk encryption; for SRM Server VM disks                                     │
│  vSAN enc      = replica VMs retain vSAN encryption on recovery site                                  │
│  WAN enc       = IPSEC or encrypted MPLS for array replication over WAN                               │
│  PKI cert      = replace self-signed with enterprise cert for compliance                              │
│  Re-pair       = after cert replacement; required for site pair trust                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

After replacing the SRM Server cert, update the thumbprint at the remote site:
```text
Recovery Site → Site Recovery → Site Pair → Edit → Accept new thumbprint
```

---

## SRA Credential Storage Encryption

SRA credentials (array username/password or API token) are stored encrypted by SRM. The encryption key is tied to the SRM installation — do not restore SRM from a backup to a different machine without re-entering SRA credentials.

---

## FIPS Mode

SRM 8.x and later support FIPS 140-2 mode when deployed on FIPS-enabled vSphere. Requirements:
- vCenter must be in FIPS mode
- All SRM components must be on FIPS-capable versions
- VRA appliances must be configured for FIPS mode during deployment

Check VMware FIPS compliance documentation before enabling.
