# VCF — Encryption


<div class="kb-summary">
Encryption reference covering vSAN Encryption.
</div>

VCF Encryption — Certificate and Data Flow
```text
┌──────────────────────────────── VMware Cloud Foundation — Encryption ─────────────────────────────────┐
│                                                                                                       │
│  VCF encryption covers transport (TLS 1.2+), vSAN at-rest encryption, VM encryption,                  │
│  and SDDC Manager credential vault; all keys via external KMS.                                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Transport Encryption             │  │               vSAN Encryption               │   │
│   │         All APIs: TLS 1.2+ enforced          │  │            Cluster-level AES-256            │   │
│   │         NSX: TLS between components          │  │              KMS: KMIP protocol             │   │
│   │           SDDC Mgr: TLS to all VCF           │  │              DEK/KEK hierarchy              │   │
│   │            Backup: encrypted SFTP            │  │          Re-key: rolling no outage          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Transport protects management plane; vSAN encryption protects data at rest.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Management            │  │              SDDC Manager Vault             │   │
│   │          SDDC Mgr: rotate all certs          │  │         Service passwords: encrypted        │   │
│   │          Custom CA: enterprise PKI           │  │            SDDC DB: AES encrypted           │   │
│   │           VMCA: default per domain           │  │          Optional: HashiCorp Vault          │   │
│   │        Expiry: 30d alert in SDDC Mgr         │  │          Master key: admin password         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  KMS must be highly available on management network; SDDC Manager DB encryption                       │
│  key is derived from the admin password — protect and rotate it.                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+     = minimum transport security for all VCF APIs                                           │
│  vSAN enc     = cluster-level AES-256 encryption of all disk data                                     │
│  KMS          = Key Management Server; KMIP protocol; holds KEKs                                      │
│  KMIP         = Key Management Interoperability Protocol; port 5696                                   │
│  DEK          = Data Encryption Key; per disk group                                                   │
│  KEK          = Key Encryption Key; from KMS; wraps DEKs                                              │
│  Re-key       = rotate KEK without downtime; new KEK wraps existing DEKs                              │
│  SDDC vault   = encrypted store for all component service passwords                                   │
│  VMCA         = vSphere Certificate Authority; per-domain default CA                                  │
│  Custom CA    = replace VMCA with enterprise PKI via SDDC Mgr                                         │
│  HashiCorp Vault= optional external credential store for SDDC Mgr                                     │
│  Master key   = SDDC Mgr DB encryption; derived from admin password                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────── VMware Cloud Foundation — Encryption ─────────────────────────────────┐
│                                                                                                       │
│  VCF encryption covers transport (TLS 1.2+), vSAN at-rest encryption, VM encryption,                  │
│  and SDDC Manager credential vault; all keys via external KMS.                                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Transport Encryption             │  │               vSAN Encryption               │   │
│   │         All APIs: TLS 1.2+ enforced          │  │            Cluster-level AES-256            │   │
│   │         NSX: TLS between components          │  │              KMS: KMIP protocol             │   │
│   │           SDDC Mgr: TLS to all VCF           │  │              DEK/KEK hierarchy              │   │
│   │            Backup: encrypted SFTP            │  │          Re-key: rolling no outage          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Transport protects management plane; vSAN encryption protects data at rest.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Management            │  │              SDDC Manager Vault             │   │
│   │          SDDC Mgr: rotate all certs          │  │         Service passwords: encrypted        │   │
│   │          Custom CA: enterprise PKI           │  │            SDDC DB: AES encrypted           │   │
│   │           VMCA: default per domain           │  │          Optional: HashiCorp Vault          │   │
│   │        Expiry: 30d alert in SDDC Mgr         │  │          Master key: admin password         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  KMS must be highly available on management network; SDDC Manager DB encryption                       │
│  key is derived from the admin password — protect and rotate it.                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+     = minimum transport security for all VCF APIs                                           │
│  vSAN enc     = cluster-level AES-256 encryption of all disk data                                     │
│  KMS          = Key Management Server; KMIP protocol; holds KEKs                                      │
│  KMIP         = Key Management Interoperability Protocol; port 5696                                   │
│  DEK          = Data Encryption Key; per disk group                                                   │
│  KEK          = Key Encryption Key; from KMS; wraps DEKs                                              │
│  Re-key       = rotate KEK without downtime; new KEK wraps existing DEKs                              │
│  SDDC vault   = encrypted store for all component service passwords                                   │
│  VMCA         = vSphere Certificate Authority; per-domain default CA                                  │
│  Custom CA    = replace VMCA with enterprise PKI via SDDC Mgr                                         │
│  HashiCorp Vault= optional external credential store for SDDC Mgr                                     │
│  Master key   = SDDC Mgr DB encryption; derived from admin password                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────────────────┐
│  vSAN Data-at-Rest Encryption                                                                         │
│                                                                                                       │
│  KMS Server ──► vCenter vSAN configuration                                                            │
│  Cluster → Configure → vSAN → Services                                                                │
│  → Data-at-Rest Encryption → Enable                                                                   │
│                                                                                                       │
│  Key rotation: live operation (no downtime)                                                           │
│  KMS HA is critical — loss = datastore inaccessible                                                   │
└─────────────────────────────────────────────────────┘
```text
┌──────────────────────────────── VMware Cloud Foundation — Encryption ─────────────────────────────────┐
│                                                                                                       │
│  VCF encryption covers transport (TLS 1.2+), vSAN at-rest encryption, VM encryption,                  │
│  and SDDC Manager credential vault; all keys via external KMS.                                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Transport Encryption             │  │               vSAN Encryption               │   │
│   │         All APIs: TLS 1.2+ enforced          │  │            Cluster-level AES-256            │   │
│   │         NSX: TLS between components          │  │              KMS: KMIP protocol             │   │
│   │           SDDC Mgr: TLS to all VCF           │  │              DEK/KEK hierarchy              │   │
│   │            Backup: encrypted SFTP            │  │          Re-key: rolling no outage          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Transport protects management plane; vSAN encryption protects data at rest.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Management            │  │              SDDC Manager Vault             │   │
│   │          SDDC Mgr: rotate all certs          │  │         Service passwords: encrypted        │   │
│   │          Custom CA: enterprise PKI           │  │            SDDC DB: AES encrypted           │   │
│   │           VMCA: default per domain           │  │          Optional: HashiCorp Vault          │   │
│   │        Expiry: 30d alert in SDDC Mgr         │  │          Master key: admin password         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  KMS must be highly available on management network; SDDC Manager DB encryption                       │
│  key is derived from the admin password — protect and rotate it.                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+     = minimum transport security for all VCF APIs                                           │
│  vSAN enc     = cluster-level AES-256 encryption of all disk data                                     │
│  KMS          = Key Management Server; KMIP protocol; holds KEKs                                      │
│  KMIP         = Key Management Interoperability Protocol; port 5696                                   │
│  DEK          = Data Encryption Key; per disk group                                                   │
│  KEK          = Key Encryption Key; from KMS; wraps DEKs                                              │
│  Re-key       = rotate KEK without downtime; new KEK wraps existing DEKs                              │
│  SDDC vault   = encrypted store for all component service passwords                                   │
│  VMCA         = vSphere Certificate Authority; per-domain default CA                                  │
│  Custom CA    = replace VMCA with enterprise PKI via SDDC Mgr                                         │
│  HashiCorp Vault= optional external credential store for SDDC Mgr                                     │
│  Master key   = SDDC Mgr DB encryption; derived from admin password                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Lead times:**

| Timeline | Action |
|---|---|
| 60 days | Plan renewal — raise change ticket |
| 30 days | Schedule maintenance window |
| 7 days | Treat as P2 — renew immediately |

## vSAN Encryption

For workload domains handling sensitive data:

1. Deploy and configure a KMS (Key Management Server)
2. In vCenter: Cluster → Configure → vSAN → Services → Data-at-Rest Encryption → Enable
3. Define a key rotation schedule (annual minimum or per policy)
4. Ensure the KMS is highly available — KMS loss makes the vSAN datastore inaccessible

Key rotation: vCenter → vSAN → Key Management → Rotate Keys (live operation, no downtime required).
