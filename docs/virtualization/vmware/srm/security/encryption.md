---
tags:
  - security
  - srm
  - vmware
---
# SRM — Encryption


<div class="kb-summary">
Encryption reference covering Encryption at Recovery Site, Certificate Management for SRM Server, SRA Credential Storage Encryption, FIPS Mode.

*Applies to: SRM 8.x / 9.x*
</div>

  TLS Encryption Coverage
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

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## See also

- [SRM — Hardening](hardening/)
- [SRM — Health Checks](../operations/health-checks/)
