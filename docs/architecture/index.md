# Architecture

<div class="kb-summary">
Enterprise infrastructure architecture design guides covering high availability patterns, storage tiering, network topology, and disaster recovery design principles.
</div>

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="disaster-recovery-design/">
  <strong>Disaster Recovery Design</strong>
  <span>RPO/RTO targets, site topology, failover patterns, and DR architecture decision frameworks.</span>
</a>

<a class="kb-card" href="high-availability/">
  <strong>High Availability</strong>
  <span>Redundancy patterns, clustering options, failover design, and availability SLA considerations.</span>
</a>

<a class="kb-card" href="network-design/">
  <strong>Network Design</strong>
  <span>Topology, segmentation, routing, and naming standards for enterprise network architecture.</span>
</a>

<a class="kb-card" href="storage-design/">
  <strong>Storage Design</strong>
  <span>Tiering strategy, protocol selection, capacity planning, and array placement principles.</span>
</a>
</div>


```
┌─────────────────────────────────────────────────────────────────────┐
│                    Enterprise Infrastructure Overview               │
│                                                                     │
│  ┌──────────────────────┐        ┌──────────────────────────────┐   │
│  │   On-Premises DC      │        │        Cloud Platforms       │  │
│  │  ┌────────────────┐  │        │  ┌────────────┐ ┌─────────┐ │    │
│  │  │ ESXi / vSphere │  │        │  │    AWS     │ │  Azure  │ │    │
│  │  │  vSAN + NSX-T  │  │        │  │ EC2/EBS/S3 │ │  VMs    │ │    │
│  │  │   VxRail HCI   │  │        │  └────────────┘ └─────────┘ │    │
│  │  └───────┬────────┘  │        └──────────────┬───────────────┘   │
│  │          │            │                       │                   │
│  │  ┌───────▼────────┐  │   ExpressRoute/        │                   │
│  │  │  Integration   │◄─┼──────DX Connect────────┘                  │
│  │  │  Auth · Certs  │  │                                           │
│  │  │  NTP · DNS     │  │        ┌──────────────────────────────┐   │
│  │  └───────┬────────┘  │        │          Monitoring          │   │
│  │          │            │        │  Aria Ops · Pure1 · CloudIQ  │  │
│  │  ┌───────▼────────┐  │        └──────────────────────────────┘   │
│  │  │ DR / Backup    │  │                                           │
│  │  │ SRM · SRDF     │  │                                           │
│  │  │ Veeam · RP     │  │                                           │
│  │  └────────────────┘  │                                           │
│  └──────────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Enterprise Architecture Overview

```mermaid
graph TB
  COMP["Compute\nESXi · Linux · Windows"] --> FABRIC["SAN Fabric\nBrocade · Cisco MDS"]
  COMP --> NET["Network\nVDS · NSX · VLANs"]
  FABRIC --> STORE["Storage\nFlashArray · PowerMax · ONTAP"]
  NET --> STORE
  STORE -->|"replication"| DR["Disaster Recovery\nSRM · SRDF · RecoverPoint"]
  COMP --> MON["Monitoring\nAria Ops · CloudIQ · Pure1"]
  STORE --> MON
  COMP --> SEC["Security\nAD · CyberArk · PKI"]
  NET --> SEC
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef net fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mon fill:#b45309,stroke:#92400e,color:#fff
  classDef sec fill:#15803d,stroke:#166534,color:#fff
  class COMP,FABRIC ctrl
  class STORE store
  class NET net
  class DR dr
  class MON mon
  class SEC sec
```
