# Aria Suite Lifecycle — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Product Management Topology.
</div>

## Overview

Aria Suite Lifecycle (LCM) is a management appliance that deploys, upgrades, and manages the entire VMware Aria product suite from a single control plane. LCM eliminates per-product upgrade complexity by orchestrating pre-checks, snapshots, binary staging, sequential node upgrades, and post-checks as a single audited workflow. All credentials and certificates are stored in the integrated **Locker** vault.

## Product Management Topology

```mermaid
graph TB
  LCM["Aria Suite Lifecycle\n(LCM appliance)"]
  LCM --> VROPS["Aria Operations"]
  LCM --> VRLI["Aria Ops for Logs"]
  LCM --> VRA["Aria Automation"]
  LCM --> VRNI["Aria Ops for Networks"]
  LCM --> REPO["Product Binaries Repo\n(NFS /data)"]
  ADMIN(["vSphere Admin"]) -->|"web UI"| LCM
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class LCM mgmt
  class VROPS,VRLI,VRA,VRNI ctrl
  class ADMIN host
```text
┌────────────────────────────────────── How Aria Suite LCM Works ───────────────────────────────────────┐
│                                                                                                       │
│  Depot sync, environment creation, product deployment, and cert management in LCM.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Depot & Content                │  │            Environment Lifecycle            │   │
│   │          Depot: online or local NFS          │  │           Create environment in UI          │   │
│   │          Sync PAK files from depot           │  │           Associate vCenter + vIDM          │   │
│   │           Download: vROps/vRLI/vRA           │  │           Add products one by one           │   │
│   │          Binary stored on LCM disk           │  │          LCM runs pre-checks first          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Depot provides binaries; environments group products; LCM orchestrates deployment.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Product Deployment Flow            │  │            Certificate Management           │   │
│   │           1. Select PAK from depot           │  │           Import cert to LCM trust          │   │
│   │        2. LCM deploys OVA to vSphere         │  │          Assign cert to environment         │   │
│   │          3. LCM configures product           │  │          LCM pushes cert to product         │   │
│   │         4. Product joins environment         │  │            Rotate cert via LCM UI           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; vCenter for product VM deployment; NFS/S3 for depot storage                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Depot               = Content source: VMware online or local NFS with PAK files                      │
│  PAK File            = Product Activation Key; contains binaries for deploy/upgrade                   │
│  Environment         = LCM grouping of related products sharing vCenter and vIDM                      │
│  Pre-check           = LCM automated validation before deployment or upgrade                          │
│  OVA Deploy          = LCM deploys product VM from OVA via vCenter API                                │
│  Product Config      = LCM automates post-deploy config: IP, DNS, vIDM registration                   │
│  Cert Trust Store    = LCM internal store of trusted CA certs and product certs                       │
│  Cert Assignment     = Linking a TLS cert to a specific product in an environment                     │
│  Cert Rotation       = LCM-orchestrated cert replacement across all product nodes                     │
│  vIDM Registration   = Product registration with vIDM for SSO; done by LCM                            │
│  Logscraper          = LCM diagnostic tool collecting logs from all products                          │
│  Content Sync        = LCM downloads and caches PAK files from online depot                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌────────────────────────────── Aria Suite LCM — Product Upgrade Workflow ──────────────────────────────┐
│                                                                                                       │
│    LCM orchestrates rolling upgrades across all Aria products in an environment.                      │
│    Each upgrade has a pre-check gate and a VM snapshot rollback point.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Pre-Upgrade Phase               │  │           Upgrade Execution Phase           │   │
│   │       1. LCM syncs PAK from depot/NFS        │  │       5. LCM deploys PAK to product VM      │   │
│   │       2. Pre-check: disk space + certs       │  │        6. Services restarted in order       │   │
│   │      3. Pre-check: product health green      │  │      7. LCM polls health API until pass     │   │
│   │      4. VM snapshot taken (rollback pt)      │  │      8. Post-upgrade health validation      │   │
│   │        Pre-check fail → abort, no change     │  │      9. Snapshots removed after N days      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Rollback: if upgrade fails post-snapshot, revert VM snapshot to prior state.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Upgrade Order in Environment         │  │          Cert and Password Rotation         │   │
│   │   vIDM upgraded first (identity provider)    │  │       LCM renews certs before upgrade       │   │
│   │        Aria Operations upgraded next         │  │     Locker vault holds product passwords    │   │
│   │           Aria Operations for Logs           │  │         Passwords rotated via LCM UI        │   │
│   │        Aria Automation upgraded last         │  │    Certificate expiry check in pre-check    │   │
│   │      Order enforced by dependency graph      │  │      vIDM cert must be valid before all     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    LCM VM · vCenter for snapshot/deploy · NFS or online depot for PAK files                           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PAK file        = Product Activation Key; binary package for deploy or upgrade                     │
│    Depot           = binary store: VMware online (SFTP) or local NFS with PAK files                   │
│    Environment     = LCM grouping: one vCenter + one vIDM + associated Aria products                  │
│    Pre-check       = automated validation gate before any upgrade begins                              │
│    Snapshot        = VM-level rollback point taken immediately before upgrade                         │
│    Locker          = LCM vault storing product passwords and certificates securely                    │
│    vIDM            = VMware Identity Manager; SSO provider for all Aria products                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| API Path | Purpose |
|---|---|
| `/lcm/authz/api/v2` | Authentication — login and token management |
| `/lcm/lcmservice/api/v2/environments` | Environment and product inventory |
| `/lcm/lcmservice/api/v2/requests` | Request tracking and audit |
| `/lcm/locker/api/v2/certificates` | Locker — certificate management |
| `/lcm/locker/api/v2/passwords` | Locker — password management |
