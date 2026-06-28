---
tags:
  - architecture
  - dell
---
# SRDF/S — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Write Commit Model, RTT Requirements, Recovery Time Standards.

*Applies to: SRDF/S*
</div>
![SRDF/S — How It Works](../../../../assets/storage-dell-srdf-s-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Host" as HOST
participant "R1 Volume\n(source)" as R1
participant "RDF Link\n(FC / IP)" as RDF
participant "R2 Volume\n(target)" as R2

HOST -> R1: Write I/O
R1 -> RDF: Synchronous mirror write
RDF -> R2: Write to remote
R2 --> RDF: Write hardened ACK
RDF --> R1: Remote confirmed
R1 --> HOST: I/O complete (zero RPO)

note over R1,R2: Both sites must acknowledge\nbefore host I/O completes.\nDistance limit: ~200 km (latency).
@enduml
```

## Overview

SRDF/S (Synchronous) provides zero-data-loss replication between two PowerMax arrays. Every host write is committed to both the source (R1) and target (R2) before an acknowledgement is returned to the host. This guarantees RPO = 0 at the cost of write latency, which is directly proportional to inter-site round-trip time (RTT). Use case: financial transaction systems, active-active cluster workloads, and DR configurations where RPO = 0 is contractually required.

## Write Commit Model

```mermaid
graph LR
  PM_A["PowerMax Primary\nSite A — R1"] -->|"SRDF/S synchronous\n(≤10ms RTT)"| PM_B["PowerMax Secondary\nSite B — R2"]
  PM_A --> HA(["Production Hosts\nSite A"])
  PM_B -.->|"read-only\n(Synchronized state)"| HB(["Standby Hosts\nSite B"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PM_A ctrl
  class PM_B dr
  class HA host
  class HB dr
```

## RTT Requirements

| Site Distance | Typical RTT | Max Acceptable | Notes |
|---|---|---|---|
| Campus / same campus | < 1ms | 2ms | Ideal for SRDF/S |
| Metro (≤ 100km dark fibre) | 1–5ms | 5ms | Within spec |
| Metro (> 100km) | 5–10ms | ≤ 10ms | Borderline — test under peak load |
| WAN (> 200km) | > 10ms | Not recommended | Use SRDF/A instead |

## Recovery Time Standards

| RTO Category | Target |
|---|---|
| Planned failover (SRM automated) | < 15 minutes |
| Unplanned failover (manual) | < 30 minutes |
| Post-failover data validation | < 60 minutes |

---

## See also

- [Srdf S — Design Standards](design-standards/)
- [Srdf S — Integrations](integrations/)
- [Srdf S — Deploy](../deploy/)
