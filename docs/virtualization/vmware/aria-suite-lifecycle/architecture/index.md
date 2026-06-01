# Aria Suite Lifecycle — Architecture

<div class="kb-summary">
Central management appliance for deploying and upgrading the full VMware Aria Suite. Orchestrates pre-check → snapshot → stage → upgrade → post-check as a single audited workflow; stores all credentials and certificates in the integrated Locker vault.
</div>

```
┌─────────────────────────────────────── Aria LCM — Architecture ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Aria Suite Lifecycle (formerly vRealize Suite LCM) = LCM appliance with embedded vIDM identity│   │
│   │    Manages lifecycle of Aria products (vRA/vROps/vRLI/vRNI) grouped into named Environments   │   │
│   │  Password Locker stores and encrypts credentials at rest; Certificate Locker manages product  │   │
│   │     Install/upgrade wizard orchestrates product deployment order and pre-check validation     │   │
│   │    DR replication between LCM instances; My VMware integration for product binary downloads   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines LCM appliance role · integrations connect identity and deployment targets     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │        LCM appliance        │  │         WS1/vIDM SSO        │  │       LCM sizing 4vCPU      │   │
│   │         Environments        │  │      vCenter deploy tgt     │  │        Env naming std       │   │
│   │       Password Locker       │  │         My VMware DL        │  │      Pwd Locker policy      │   │
│   │         Cert Locker         │  │        LDAP directory       │  │       Cert Locker std       │   │
│   │       Install/upgrade       │  │        NSX placement        │  │        Product compat       │   │
│   │        DR replication       │  │        NTP/DNS config       │  │        DR replication       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    How-it-works covers LCM appliance and Lockers · integrations connect identity and vCenter          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   How It Works   │   Integrations   │    Design Stds    │    Deployment    │     Key Stds     │   │
│   │  LCM appliance   │   vIDM/WS1 SSO   │     LCM sizing    │    Single LCM    │    Env naming    │   │
│   │   Environments   │  vCenter deploy  │     Env naming    │     DR pair      │    Pwd policy    │   │
│   │ Password Locker  │   My VMware DL   │    Cert policy    │    Multi-env     │  Compat matrix   │   │
│   │   Cert Locker    │  LDAP directory  │     DR replica    │    Enterprise    │    Locker std    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter (deployment target) · Identity provider  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM appliance     = Aria Suite Lifecycle virtual appliance; central orchestrator for all Aria        │
│  Environment       = Logical grouping in LCM containing related Aria products sharing the same vIDM   │
│  Password Locker   = Encrypted credential store in LCM; holds passwords for all products and          │
│  Certificate Locker = LCM certificate store; manages TLS certs for Aria products; supports CA-signed  │
│  vIDM (Identity Manager) = Embedded identity provider in LCM; provides SSO across all managed Aria    │
│  Product BOM       = Bill of Materials; version matrix listing compatible Aria product versions per   │
│  Install wizard    = LCM UI workflow for deploying a new Aria product into an existing Environment    │
│  Upgrade wizard    = LCM UI workflow for upgrading Aria products in dependency order with pre-check   │
│  Day-2 operations  = Post-install operations in LCM: cert rotation, password rotation, content        │
│  DR replication    = LCM appliance replication to a secondary site for disaster recovery failover     │
│  My VMware         = Broadcom/VMware portal integration; LCM downloads product binaries directly from │
│  Workspace ONE     = VMware identity and access management platform; can replace embedded vIDM in LCM │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────── Aria LCM — Architecture ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Aria Suite Lifecycle (formerly vRealize Suite LCM) = LCM appliance with embedded vIDM identity│   │
│   │    Manages lifecycle of Aria products (vRA/vROps/vRLI/vRNI) grouped into named Environments   │   │
│   │  Password Locker stores and encrypts credentials at rest; Certificate Locker manages product  │   │
│   │     Install/upgrade wizard orchestrates product deployment order and pre-check validation     │   │
│   │    DR replication between LCM instances; My VMware integration for product binary downloads   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines LCM appliance role · integrations connect identity and deployment targets     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │        LCM appliance        │  │         WS1/vIDM SSO        │  │       LCM sizing 4vCPU      │   │
│   │         Environments        │  │      vCenter deploy tgt     │  │        Env naming std       │   │
│   │       Password Locker       │  │         My VMware DL        │  │      Pwd Locker policy      │   │
│   │         Cert Locker         │  │        LDAP directory       │  │       Cert Locker std       │   │
│   │       Install/upgrade       │  │        NSX placement        │  │        Product compat       │   │
│   │        DR replication       │  │        NTP/DNS config       │  │        DR replication       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    How-it-works covers LCM appliance and Lockers · integrations connect identity and vCenter          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   How It Works   │   Integrations   │    Design Stds    │    Deployment    │     Key Stds     │   │
│   │  LCM appliance   │   vIDM/WS1 SSO   │     LCM sizing    │    Single LCM    │    Env naming    │   │
│   │   Environments   │  vCenter deploy  │     Env naming    │     DR pair      │    Pwd policy    │   │
│   │ Password Locker  │   My VMware DL   │    Cert policy    │    Multi-env     │  Compat matrix   │   │
│   │   Cert Locker    │  LDAP directory  │     DR replica    │    Enterprise    │    Locker std    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter (deployment target) · Identity provider  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM appliance     = Aria Suite Lifecycle virtual appliance; central orchestrator for all Aria        │
│  Environment       = Logical grouping in LCM containing related Aria products sharing the same vIDM   │
│  Password Locker   = Encrypted credential store in LCM; holds passwords for all products and          │
│  Certificate Locker = LCM certificate store; manages TLS certs for Aria products; supports CA-signed  │
│  vIDM (Identity Manager) = Embedded identity provider in LCM; provides SSO across all managed Aria    │
│  Product BOM       = Bill of Materials; version matrix listing compatible Aria product versions per   │
│  Install wizard    = LCM UI workflow for deploying a new Aria product into an existing Environment    │
│  Upgrade wizard    = LCM UI workflow for upgrading Aria products in dependency order with pre-check   │
│  Day-2 operations  = Post-install operations in LCM: cert rotation, password rotation, content        │
│  DR replication    = LCM appliance replication to a secondary site for disaster recovery failover     │
│  My VMware         = Broadcom/VMware portal integration; LCM downloads product binaries directly from │
│  Workspace ONE     = VMware identity and access management platform; can replace embedded vIDM in LCM │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

![Aria Suite Lifecycle Architecture](../../../../assets/aria-suite-lifecycle-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with vCenter, VIDM, NFS, and managed Aria products.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Pre-requisite checklist, upgrade sequencing, and DNS/NTP requirements.</span></a>
</div>

## Core Components

| Component | Role |
|---|---|
| LCM Appliance | Central orchestration, UI, REST API, Locker vault |
| Workspace ONE Access (VIDM) | Identity provider and SSO for all Aria products |
| vRealize Easy Installer | Bootstrap ISO for initial multi-product deployment |
| NFS Share | Binary repository (`.pak` files) and snapshot storage |
| NTP Server | Time synchronisation — mandatory; certificate operations fail on >5 s skew |
| DNS | Forward + reverse resolution required for every node FQDN |

