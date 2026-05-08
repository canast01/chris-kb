# NSX — Architecture Overview

## NSX Overlay Architecture

```mermaid
graph TB
  MGR["NSX Manager\n(3-node cluster)"] --> TN["Transport Nodes\n(ESXi hosts + Edge VMs)"]
  TN --> TZ["Transport Zones\n(Overlay + VLAN)"]
  TZ --> SEG["Segments\n(logical switches)"]
  SEG --> T1["Tier-1 Gateway\n(distributed routing per tenant)"]
  T1 --> T0["Tier-0 Gateway\n(north-south on Edge Nodes)"]
  T0 --> PHY["Physical Network\n(underlay — BGP / static)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class MGR ctrl
  class TN,TZ net
  class SEG,T1,T0 net
  class PHY host
```

## Key Concepts

- **NSX Manager cluster** (3 nodes) provides the management and control plane
- **Transport Nodes** are ESXi hosts and Edge VMs prepared with NSX kernel modules (TEPs)
- **TEP (Tunnel Endpoint)** is the VMkernel interface used for GENEVE overlay encapsulation
- **Segments** are logical Layer 2 networks — equivalent to VLANs but overlay-based
- **Tier-1 Gateways** provide distributed routing per tenant; run on all ESXi hosts
- **Tier-0 Gateways** handle north-south routing; run on Edge Nodes and peer with physical underlay via BGP or static routes
- **DFW (Distributed Firewall)** enforces micro-segmentation statefully at the vNIC level on every ESXi host
