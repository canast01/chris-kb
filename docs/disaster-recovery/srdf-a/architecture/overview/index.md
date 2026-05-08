# SRDF/A — Overview

> Part of the [SRDF/A](../../) reference.

---
## Overview

SRDF/A (Asynchronous) replicates data from a source PowerMax to a target PowerMax by capturing writes into time-bounded delta sets (cycles) and transmitting them in order. The source array acknowledges writes to the host before transmission, so host write latency is not directly affected by WAN latency — this is the key difference from SRDF/S.

**RPO** is determined by cycle time (default 30 seconds). If the WAN link fails, the R1 (source) continues accepting writes while the R2 (target) falls behind; RPO exposure equals the time since the last successful cycle completed at the target.

---

## Delta Set Mechanics

1. Host writes to R1 go into the **active delta set** for the current cycle.
2. At the end of the cycle interval, the active delta set is **closed** and queued for transmission.
3. A new delta set opens for the next cycle.
4. The closed delta set is transmitted to R2 in sequence — each delta set is applied in order, maintaining consistency.
5. When R2 confirms receipt, the cycle is complete and RPO resets.

Two delta sets are maintained simultaneously: one being transmitted (transmit delta set) and one accepting new writes (active delta set). A third set (overflow) is used when the transmit delta set is not clearing fast enough.

```mermaid
flowchart TD
    hostWrite["Host Write to R1"] --> activeDeltaSet["Active Delta Set\n(accumulating writes)"]
    activeDeltaSet -->|"cycle interval ends\n(default 30s)"| closeDeltaSet["Delta Set Closed\n& Queued"]
    closeDeltaSet --> newActive["New Active Delta Set\nOpens for Next Cycle"]
    closeDeltaSet --> transmit["Transmit Delta Set\n→ WAN → R2"]
    transmit -->|"R2 confirms receipt"| rpoReset["RPO Resets\nCycle Complete"]
    transmit -->|"link saturated / slow"| dse["DSE Overflow Device\nActivated"]
    dse -->|"link clears"| transmit

    style activeDeltaSet fill:#2563eb,color:#fff
    style closeDeltaSet fill:#b45309,color:#fff
    style transmit fill:#7c3aed,color:#fff
    style dse fill:#be123c,color:#fff
    style rpoReset fill:#15803d,color:#fff
```

---

## SRDF Group Design

An SRDF group (RDF group) is a logical container for R1/R2 device pairs. All pairs in a group share the same cycle boundary, meaning they are consistent with each other at failover.

- All devices representing a single application or workload should be in the **same SRDF group** to guarantee write-order consistency.
- Multiple SRDF groups can exist between the same two arrays, but each has independent cycle timers.
- Device group (`symdg`) is the management boundary for controlling replication (`symrdf -g <dgname>`).

---

## Connectivity

SRDF/A transmits over:

| Link Type | Use Case |
|---|---|
| FCIP (FC over IP) | Most common — FC-to-IP gateway over a WAN |
| Dark fibre (FC) | Short distances only — adds no additional latency |
| iSLR (IP Short Range) | Newer PowerMax connectivity via IP directors |

**Bandwidth sizing:** The required bandwidth equals the average write I/O rate × average block size × replication overhead (~1.1–1.2x). For SRDF/A, bandwidth headroom above the average is also needed to handle peak delta set sizes without cycle delay.

---

## Dual-Site Topology

```mermaid
graph TD
    subgraph siteA ["Site A — Production"]
        hosts["Production Hosts"]
        r1["PowerMax R1\n(Source Array)"]
        srdfDir1["SRDF Director Ports"]
        hosts -->|"host writes"| r1
        r1 --> srdfDir1
    end

    subgraph wan ["WAN / FCIP Link"]
        link["FCIP / Dark Fibre\nReplication Link"]
    end

    subgraph siteB ["Site B — DR"]
        srdfDir2["SRDF Director Ports"]
        r2["PowerMax R2\n(Target Array)"]
        dse["DSE Device\n(Overflow Buffer)"]
        drHosts["DR Hosts\n(standby)"]
        srdfDir2 --> r2
        r2 -.->|"only at failover"| drHosts
        r2 --- dse
    end

    srdfDir1 -->|"async delta sets\n~30s cycles"| link
    link --> srdfDir2
```

## Pair States

| State | Meaning | Normal? |
|---|---|---|
| Synchronized | R2 is up to date; no active delta sets pending | Yes — for SRDF/S only |
| Consistent | R2 is consistent and receiving cycles; the latest cycle is applied | Yes — normal SRDF/A state |
| SyncInProg | Synchronisation in progress after resume | Transient |
| Transmit Idle | No data being transmitted — link idle, no new writes, or link saturation | Investigate if unexpected |
| Suspended | Replication manually suspended | Expected if a suspension was performed |
| Failed Over | R1 devices are read-only; R2 devices are R/W | Active failover underway |
| Split | Devices are split — both R1 and R2 are R/W (data diverges from this point) | Only for planned operations |

---

## Licensing

SRDF/A requires:
- **SRDF/A license** on both source and target PowerMax arrays
- SRDF port licenses on the directors used for replication
- Optional: **TimeFinder/SnapVX** on the target to create local snapshots of R2 devices for backup offload

---

## Architecture Diagram (Logical)

```mermaid
graph LR
  PM_A["PowerMax Primary\nSite A — R1"] -->|"writes buffered"| CYCLE["Delta Set Extension\n(DSE — WAN buffer)"]
  CYCLE -->|"cycle flush\n~30s"| PM_B["PowerMax Secondary\nSite B — R2"]
  PM_B -.->|"RPO / lag monitor"| LAG["SRDF/A Cycle State"]
  PM_A --> HA(["Production Hosts"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PM_A ctrl
  class PM_B dr
  class CYCLE,LAG mgmt
  class HA host
```
