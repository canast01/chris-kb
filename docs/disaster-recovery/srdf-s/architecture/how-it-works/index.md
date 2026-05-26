# SRDF/S — How It Works

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
```

## Components

| Component | Role |
|---|---|
| R1 device | Source (production) SRDF device; hosts write to R1 |
| R2 device | Target (DR) SRDF device; read-only during normal operation |
| SRDF Director Ports | Dedicated RDF ports on each PowerMax carrying replication traffic |
| SRDF Groups (RDFG) | Logical groupings of device pairs replicating together as a consistency group |
| Device Pairs | One R1 device mapped to one R2 device of identical size |
| Solutions Enabler (SE) | Dell management CLI host with gatekeeper LUN access for SYMCLI operations |

## Pair States

| Pair State | Description | Host Write Impact |
|---|---|---|
| Synchronized | R1 and R2 are identical; every R1 write goes synchronously to R2 | Full protection, RPO = 0 |
| SyncInProg | Initial or resync copy in progress | R1 writable; R2 not consistent |
| Suspended | Replication paused; R1 continues without mirroring | R1 writable; R2 stale |
| Failed Over | R1 unavailable; R2 is now writable | R2 takes production I/O |
| Split | Pair manually split; both volumes are independent | Both writable; no replication |
| Partitioned | RDF link interrupted; pair state indeterminate | Depends on link recovery |

## Key Commands

```bash
# Summary query for all devices in an RDFG group
symrdf -g 10 query

# Detailed output including track counts and link state
symrdf -g 10 query -detail

# Find any device not in Synchronized state
symrdf -g 10 query | grep -v Synchronized

# Check RDF director and port status
symcfg list -dir all -rdf

# Suspend replication (planned maintenance)
symrdf -g 10 -type S suspend -noprompt

# Resume from Suspended back to Synchronized
symrdf -g 10 -type S resume -noprompt

# Establish (initial sync or re-establish after split)
symrdf -g 10 -type S establish -noprompt

# Failover (manual, when R1 is unavailable)
symrdf -g 10 -type S failover -noprompt

# Restore (copy R2 data back to R1 after Failed Over)
symrdf -g 10 -type S restore -noprompt
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
