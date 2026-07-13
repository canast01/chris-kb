---
tags:
  - architecture
  - dell
description: "How It Works reference covering Overview, Delta Set Mechanics, Lag Reference, Connectivity."
---
# SRDF/A — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Delta Set Mechanics, Lag Reference, Connectivity.

*Applies to: SRDF/A*
</div>
![SRDF/A — How It Works](../../../../../assets/storage-dell-srdf-a-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Host Write" as HOST
participant "R1 Volume\n(source)" as R1
participant "SRDF/A Cycle\nBuffer" as BUF
participant "RDF Link\n(IP / FC)" as RDF
participant "R2 Volume\n(target)" as R2

HOST -> R1: Write I/O (acked immediately)
R1 -> BUF: Accumulate cycle (default 30s)
BUF -> RDF: Transmit cycle delta (compressed)
RDF -> R2: Apply cycle in order
R2 --> BUF: Cycle confirmed

note over BUF,R2
  Delta sets maintain write-order fidelity.
  RPO = transmission lag + 1 cycle.
end note
@enduml
```

## Overview

SRDF/A (Asynchronous) replicates data from a source PowerMax to a target PowerMax by capturing writes into time-bounded delta sets (cycles) and transmitting them in order. The source array acknowledges writes to the host before transmission — host write latency is not affected by WAN latency. RPO is determined by cycle time (default 30 seconds). R1 is the source (production); R2 is the target (DR).

## Delta Set Mechanics

1. Host writes to R1 go into the **active delta set** for the current cycle.
2. At the end of the cycle interval, the active delta set is **closed** and queued for transmission.
3. A new delta set opens for the next cycle.
4. The closed delta set is transmitted to R2 in sequence — each delta set applied in order, maintaining consistency.
5. When R2 confirms receipt, the cycle is complete and RPO resets.

```d2
direction: right

hostWrite: "Host Write to R1" {shape: rectangle}
activeDeltaSet: "Active Delta Set\n(accumulating writes" {shape: rectangle}
closeDeltaSet: "closeDeltaSet" {shape: rectangle}
newActive: "New Active Delta Set\nOpens for Next Cycle" {shape: rectangle}
transmit: "Transmit Delta Set\n→ WAN → R2" {shape: rectangle}
rpoReset: "RPO Resets\nCycle Complete" {shape: rectangle}
dse: "DSE Overflow Device\nActivated" {shape: rectangle}

hostWrite -> activeDeltaSet
closeDeltaSet -> newActive
closeDeltaSet -> transmit
transmit -> rpoReset
transmit -> dse
dse -> transmit
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

---

## See also

- [Srdf A — Design Standards](../design-standards/)
- [Srdf A — Integrations](../integrations/)
- [Srdf A — Deploy](../../deploy/)
