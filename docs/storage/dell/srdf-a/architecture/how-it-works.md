---
tags:
  - architecture
  - dell
---
# SRDF/A — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Delta Set Mechanics, Lag Reference, Connectivity.

*Applies to: SRDF/A*
</div>

## Overview

SRDF/A (Asynchronous) replicates data from a source PowerMax to a target PowerMax by capturing writes into time-bounded delta sets (cycles) and transmitting them in order. The source array acknowledges writes to the host before transmission — host write latency is not affected by WAN latency. RPO is determined by cycle time (default 30 seconds). R1 is the source (production); R2 is the target (DR).

## Delta Set Mechanics

1. Host writes to R1 go into the **active delta set** for the current cycle.
2. At the end of the cycle interval, the active delta set is **closed** and queued for transmission.
3. A new delta set opens for the next cycle.
4. The closed delta set is transmitted to R2 in sequence — each delta set applied in order, maintaining consistency.
5. When R2 confirms receipt, the cycle is complete and RPO resets.

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
```text
┌──────────────────────────────────────── SRDF/A — How It Works ────────────────────────────────────────┐
│                                                                                                       │
│    SRDF/A data flow — from source to target through the protection pipeline:                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 1  Source / Production System                                 │   │
│   │            R1 Volume (Source)  — primary data on production PowerMax; host writes here        │   │
│   │               Host writes are intercepted or snapshotted by the SRDF/A agent/proxy            │   │
│   │                  Changed blocks tracked via CBT / journal / delta-set mechanism               │   │
│   │                 Consistency ensured at quiesce point before data transfer begins              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Changed data forwarded to the SRDF/A engine — compression and encryption applied in transit        │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        2  SRDF/A Engine                                       │   │
│   │         R2 Volume (Target)  — replica on DR PowerMax; receives delta sets asynchronously      │   │
│   │                    Data compressed, deduplicated, and encrypted before storage                │   │
│   │                  Metadata catalog updated; job status reported to control plane               │   │
│   │                                         symrdf establish                                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     3  Target / Repository                                    │   │
│   │          SRDF/A Engine       — delta-set formation: groups writes per cycle, ships to R2      │   │
│   │                  Recovery point written; retention policy applied automatically               │   │
│   │                                Restore: symrdf failover / failback                            │   │
│   │                     RTO driven by target storage performance and data volume                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports      │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology               │
│  R1            = source SRDF volume on production array; host writes flow here                        │
│  R2            = target SRDF volume on DR array; receives replicated data asynchronously              │
│  Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically          │
│  Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO                  │
│  symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore       │
│  SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth             │
│  Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle            │
│  Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts                   │
│  Restore       = after failover resolution, re-establishes replication with R1 as source              │
│  Establish     = initial sync or re-sync operation that copies R1 to R2 in full                       │
│  Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication                 │
│  FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link                      │
│  Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Lag Reference

| Lag Range | Assessment | Action |
|---|---|---|
| ≤ configured cycle time | Healthy — RPO is met | None — monitor |
| 2–5× cycle time | Warning — investigate link or write rate | Check link utilization and write rate |
| > 5× cycle time | Critical — RPO SLA breached | Immediate escalation; consider suspending non-critical groups |

## Connectivity

| Link Type | Use Case |
|---|---|
| FCIP (FC over IP) | Most common — FC-to-IP gateway over WAN |
| Dark fibre (FC) | Short distances only — adds no additional latency |
| iSLR (IP Short Range) | Newer PowerMax connectivity via IP directors |

**Bandwidth sizing:** Required bandwidth = peak_change_rate_MB_per_cycle / cycle_time_s × 1.20 (20% headroom).
