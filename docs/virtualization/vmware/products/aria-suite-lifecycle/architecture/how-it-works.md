---
tags:
  - architecture
  - aria-lcm
  - vmware
description: "How It Works reference covering Overview, Product Management Topology."
---
# Aria Suite Lifecycle — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Product Management Topology.

*Applies to: Aria Suite Lifecycle 8.x*
</div>
![Aria Suite Lifecycle — How It Works](../../../../../assets/virtualization-vmware-aria-suite-lifecycle-architecture-how-.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Admin" as ADM
participant "Aria Suite LCM\n(lifecycle manager)" as LCM
participant "My VMware\n(download portal)" as MV
participant "Content Locker\n(NFS / datastore)" as CL
participant "Aria Product\n(vROps / vRLI / vRA)" as PROD
participant "vCenter\n(deployment target)" as VC

ADM -> LCM: Create environment + product mapping
LCM -> MV: Download product binaries
MV --> LCM: OVA / ISO
LCM -> CL: Store binaries
ADM -> LCM: Deploy / upgrade product
LCM -> VC: Deploy OVA
VC --> LCM: VM deployed
LCM -> PROD: Bootstrap + configure
PROD --> LCM: Health check passed
LCM --> ADM: Product ready
@enduml
```

## Overview

Aria Suite Lifecycle (LCM) is a management appliance that deploys, upgrades, and manages the entire VMware Aria product suite from a single control plane. LCM eliminates per-product upgrade complexity by orchestrating pre-checks, snapshots, binary staging, sequential node upgrades, and post-checks as a single audited workflow. All credentials and certificates are stored in the integrated **Locker** vault.

## Product Management Topology

```d2
direction: right

LCM: "Aria Suite Lifecycle\n(LCM appliance" {shape: rectangle}
VROPS: "Aria Operations" {shape: rectangle}
VRLI: "Aria Ops for Logs" {shape: rectangle}
VRA: "Aria Automation" {shape: rectangle}
VRNI: "Aria Ops for Networks" {shape: rectangle}
REPO: "Product Binaries Repo\n(NFS /data" {shape: rectangle}
ADMIN: "vSphere Admin" {shape: rectangle}

LCM -> VROPS
LCM -> VRLI
LCM -> VRA
LCM -> VRNI
LCM -> REPO
ADMIN -> LCM
```

| API Path | Purpose |
|---|---|
| `/lcm/authz/api/v2` | Authentication — login and token management |
| `/lcm/lcmservice/api/v2/environments` | Environment and product inventory |
| `/lcm/lcmservice/api/v2/requests` | Request tracking and audit |
| `/lcm/locker/api/v2/certificates` | Locker — certificate management |
| `/lcm/locker/api/v2/passwords` | Locker — password management |

## See also

- [Aria Suite Lifecycle — Standards](../design-standards/)
- [Aria Suite Lifecycle — Deploy](../../deploy/)
- [Aria Suite Lifecycle — Integrations](../integrations/)
