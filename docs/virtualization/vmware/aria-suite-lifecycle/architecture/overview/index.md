# Aria Suite Lifecycle — Architecture Overview

## Overview

Aria Suite Lifecycle (LCM) is a management appliance that deploys, upgrades, and manages the entire VMware Aria product suite from a single control plane. LCM eliminates the need to update each Aria product independently.

## Product Management Topology

```mermaid
graph TB
  LCM["Aria Suite Lifecycle\n(LCM appliance)"]
  LCM --> VROPS["Aria Operations"]
  LCM --> VRLI["Aria Ops for Logs"]
  LCM --> VRA["Aria Automation"]
  LCM --> VRNI["Aria Ops for Networks"]
  LCM --> REPO["Product Binaries Repo"]
  ADMIN(["vSphere Admin"]) -->|"web UI"| LCM
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class LCM mgmt
  class VROPS,VRLI,VRA,VRNI ctrl
  class ADMIN host
```

## Core Components

| Component | Role |
|---|---|
| LCM Appliance | Central orchestration, UI, API, Locker (certificate/password vault) |
| Workspace ONE Access (VIDM) | Identity provider and SSO for all Aria products |
| vRealize Easy Installer | Bootstrap ISO for initial multi-product deployment |
| NFS Share | Binary repository and snapshot storage |
| NTP Server | Time synchronisation — mandatory for certificate validity |
| DNS | Forward and reverse resolution required for every node FQDN |
