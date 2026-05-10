# PowerMax — Architecture Overview

## Overview

Dell PowerMax is an enterprise NVMe-oF all-flash array engineered for mission-critical tier-1 workloads. It is available in two models: **PowerMax 2000** (1–4 engines) and **PowerMax 8000** (1–8 engines). All flash media is NVMe, data is served over NVMe-oF (NVMe over Fibre Channel or NVMe/TCP) or traditional FC/iSCSI, and latency is consistently sub-millisecond at scale. The array runs PowerMaxOS (formerly Enginuity/HYPERMAX OS) and is managed via Unisphere for PowerMax or SYMCLI (Solutions Enabler).

```mermaid
graph TB
  FA1["FA Director A\nFC / NVMe-oF"] & FA2["FA Director B\nFC / NVMe-oF"] --> XB["Crossbar Interconnect"]
  SR1["SRDF Director A"] & SR2["SRDF Director B"] --> XB
  XB --> FLASH[("NVMe Flash\nNVMe-SCM / eTLC")]
  FA1 & FA2 --> FAB["SAN Fabric\n(Brocade / Cisco)"]
  FAB --> H(["Hosts — Oracle / SQL / SAP"])
  SR1 & SR2 -->|"SRDF/S or SRDF/A"| REMOTE["Remote PowerMax"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef net fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class FA1,FA2,SR1,SR2 ctrl
  class XB,FAB net
  class FLASH store
  class H host
  class REMOTE dr
```

## HA Topology

PowerMax is architected around no single point of failure:

- **Director redundancy**: Every engine has two directors (A and B). If one director fails, the peer director takes over all I/O for that engine without host disruption.
- **Global memory mirroring**: Write cache is mirrored across both directors of an engine. A director failure does not result in data loss.
- **Multi-pathing**: Hosts connect to ports on both directors. PowerPath or native MPIO ensures automatic path failover on director or port failure.
- **NVMe drive protection**: Data is protected by RAID-5 (3+1), RAID-6 (6+2 or 8+2), or SRDF-based site-level redundancy. No single drive loss causes data unavailability.
- **SRDF (Symmetrix Remote Data Facility)**: Synchronous (SRDF/S) and asynchronous (SRDF/A) replication to a remote array. SRDF/S provides zero RPO and is used for metropolitan DR; SRDF/A tolerates higher RTT for longer-distance DR with a bounded RPO.
- **Power and cooling**: Dual redundant power feeds and N+1 cooling fans per engine.

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
