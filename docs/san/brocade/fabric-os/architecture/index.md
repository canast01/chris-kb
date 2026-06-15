---
tags:
  - architecture
  - san
---
# Brocade Fabric OS — Architecture

<div class="kb-summary">
Fabric OS runs on Brocade/Broadcom FC switches in dual-fabric core-edge topology. Principal switch election, distributed name server, WWN-based zoning, ISL trunks, Virtual Fabrics (FID partitioning), and MAPS health monitoring are the core platform mechanisms.

*Applies to: Brocade FOS 9.x*
</div>

```text
┌─────────────────────────────── Brocade Fabric OS — FC SAN Architecture ───────────────────────────────┐
│                                                                                                       │
│  Dual-fabric core-edge topology; principal switch election via highest domain ID;                     │
│  WWN-based zoning, ISL trunks, Virtual Fabrics (FID), and MAPS monitoring.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Fabric Architecture              │  │           Zoning and Name Service           │   │
│   │        Dual-fabric: A + B independent        │  │           WWN zoning: recommended           │   │
│   │        Core: director-class switches         │  │          Port zoning: for debugging         │   │
│   │          Edge: fixed-port switches           │  │           Zone set: active + saved          │   │
│   │         Principal: elects domain IDs         │  │         DNS: distributed name server        │   │
│   │        ISL: inter-switch link (trunk)        │  │         FDMI: HBA attribute register        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Zoning enforced at login: initiator can only see targets in the same zone.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Virtual Fabrics (FID)             │  │            MAPS Health Monitoring           │   │
│   │        Partition one switch: 2+ FIDs         │  │          Rules: port, fabric, perf          │   │
│   │        Each FID: own domain ID + zone        │  │          Policies: default + custom         │   │
│   │         Base fabric: management only         │  │          Actions: email/SNMP/fence          │   │
│   │       Chassis context: cross-FID view        │  │           Dashboard: mapspoliccopy          │   │
│   │          Requires Advanced License           │  │          CRC errors: key SAN metric         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Brocade G720 / G730 directors (bladed) or X7 fixed switches; dual power;                             │
│  FC SFP+ optics (32G/64G); physical A/B fabric separation via separate cables.                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FOS           = Fabric OS; Brocade/Broadcom FC switch operating system                               │
│  Principal switch= elects domain IDs for the fabric; highest WWN or priority                          │
│  Domain ID     = 1-byte fabric-unique switch identifier; 1-239 range                                  │
│  WWN           = World Wide Name; 64-bit unique ID for HBAs and switch ports                          │
│  Zone          = access control group; one initiator + one or more targets                            │
│  Zone set      = collection of zones activated on the fabric                                          │
│  ISL           = Inter-Switch Link; FC connection between switches                                    │
│  Trunk         = ISL trunk group; multiple ISLs load-balanced as one                                  │
│  FID           = Fabric ID; Virtual Fabric partition identifier                                       │
│  MAPS          = Monitoring and Alerting Policy Suite; proactive health checks                        │
│  DNS           = Distributed Name Server; tracks WWNs logged in to fabric                             │
│  FDMI          = Fabric Device Management Interface; HBA attributes                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Fabric OS Architecture](../../../../assets/fabric-os-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with SANnav, vCenter, and storage arrays.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Dual-fabric design, zoning model, domain ID, and ISL trunking standards.</span></a>
</div>

## Platform Reference

| Platform | Type | Max Ports | Notes |
|---|---|---|---|
| G620 | Fixed | 64× 32G FC | Mid-range |
| G720 | Fixed | 64× 64G FC | High-performance fixed |
| X7-4 | Director | Up to 192 FC | 4-slot director — dual CP, non-disruptive upgrades |
| X7-8 | Director | Up to 384 FC | 8-slot director — dual CP, non-disruptive upgrades |
| 6510 | Fixed | 48× 16G FC | End-of-sale — plan migration |

## Dual-Fabric Topology

