# Cisco SAN

<div class="kb-summary">
Cisco SAN knowledge base articles, operational procedures, troubleshooting notes, and command references.
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="mds/">
  <strong>MDS</strong>
  <span>Cisco MDS Fibre Channel switches — CLI, zoning, VSANs, ports, and diagnostics.</span>
</a>

<a class="kb-card" href="cisco-dcnm/">
  <strong>DCNM</strong>
  <span>Data Center Network Manager for SAN fabric management and monitoring.</span>
</a>

<a class="kb-card" href="nexus-dashboard/">
  <strong>Nexus Dashboard</strong>
  <span>Fabric assurance, analytics, and network management.</span>
</a>

</div>

## Cisco MDS Fabric Topology

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                          VSAN 10 (Production)                           │
  │                                                                         │
  │  ┌───────────────────────────┐     ┌───────────────────────────┐        │
  │  │   MDS-9710 Director A     │     │   MDS-9710 Director B     │        │
  │  │                           │     │                           │        │
  │  │  Slot 1: 48p 32Gb FC      │     │  Slot 1: 48p 32Gb FC      │        │
  │  │  Slot 2: 48p 32Gb FC      │─────│  Slot 2: 48p 32Gb FC      │        │
  │  │  Slot 3: 4x 100G ISL      │ ISL │  Slot 3: 4x 100G ISL      │        │
  │  └──────┬──────────┬─────────┘     └─────────┬──────────┬──────┘        │
  │         │          │                         │          │               │
  │    Fabric A    Fabric A                 Fabric B    Fabric B            │
  │         │          │                         │          │               │
  │  ┌──────▼──┐  ┌────▼────┐           ┌────────▼──┐  ┌───▼─────┐         │
  │  │ESXi-01  │  │ESXi-02  │           │ESXi-01    │  │ESXi-02  │         │
  │  │HBA0     │  │HBA0     │           │HBA1       │  │HBA1     │         │
  │  └─────────┘  └─────────┘           └───────────┘  └─────────┘         │
  │                                                                         │
  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
  │  │  FlashArray  │    │  PowerMax    │    │  NetApp AFF  │               │
  │  │  CT0: Fab A  │    │  Dir A: Fa A │    │  Node 1: Fa A│               │
  │  │  CT1: Fab B  │    │  Dir B: Fa B │    │  Node 2: Fa B│               │
  │  └──────────────┘    └──────────────┘    └──────────────┘               │
  └─────────────────────────────────────────────────────────────────────────┘
```
