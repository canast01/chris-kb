# NetApp SnapMirror Architecture

## Overview

SnapMirror is ONTAP's built-in replication engine, providing volume-level and SVM-level replication across ONTAP clusters. It supports three primary operating modes: asynchronous (SnapMirror Async, RPO-based), synchronous (SnapMirror Synchronous, zero RPO), and extended data protection (XDP/SnapVault, backup retention). Relationships are always managed from the destination cluster. SnapMirror Business Continuity (SMBC/AutomatedFailOver) extends synchronous replication with transparent host-level failover for SAN workloads.


## Replication Modes

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                    SnapMirror Architecture                               │
  │                                                                          │
  │  Source Cluster                            Destination Cluster           │
  │  ─────────────────────────────────         ────────────────────────────  │
  │  ┌───────────────────────────────┐         ┌──────────────────────────┐  │
  │  │  SVM / Volume (R/W)           │         │  SVM / Volume (DP/RO)    │  │
  │  │                               │         │                          │  │
  │  │  SnapMirror Async  ───────────┼─────────►  RPO = schedule interval │  │
  │  │  (XDP / SnapVault)            │         │  (hourly / daily)        │  │
  │  │                               │         │                          │  │
  │  │  SnapMirror Sync  ◄───────────┼─────────►  RPO = 0 (synchronous)  │  │
  │  │  (SM-S / SMBC)                │  NVLOG  │  AutomatedFailOver (SAN) │  │
  │  │                               │  mirror │                          │  │
  │  └───────────────────────────────┘         └──────────────────────────┘  │
  │                                                                          │
  │  Relationship management always from destination:                        │
  │  snapmirror create / initialize / update / resync / break / quiesce     │
  │                                                                          │
  │  Mediator (SM-S): third cluster or host — tiebreak for transparent      │
  │  failover when both clusters disagree on primary state                  │
  └──────────────────────────────────────────────────────────────────────────┘
```

## Replication Types

| Type | RPO | Description |
|---|---|---|
| SnapMirror Async | Configurable, minutes to hours | Standard volume replication; transfers run on a schedule; destination is read-only DP volume |
| SnapMirror Sync | Zero RPO | Every write acknowledged on both source and destination; requires <5ms RTT between clusters |
| SnapMirror Business Continuity (SMBC) | Zero RPO, transparent failover | Consistency group-based; mediator-assisted automatic failover; no host reconfiguration |
| SnapVault / XDP | Daily/weekly backup copies | Extended data protection; independent retention on destination; replaces legacy SnapVault |

## Components

- **Source volume** — read/write volume on the source cluster; the origin of replicated data
- **Destination volume** — DP (data protection) type, read-only; managed by the replication engine
- **SnapMirror policy** — defines rules, schedule, and retention for the relationship
- **Cluster peer relationship** — trust relationship between two ONTAP clusters; prerequisite for all SnapMirror
- **SVM peer relationship** — required for cross-SVM replication; establishes peer trust at the data SVM layer
- **Intercluster LIFs** — dedicated network interfaces used exclusively for SnapMirror replication traffic

## Connectivity

Intercluster LIFs must be on a dedicated replication network, separate from data and management traffic. ONTAP uses TCP ports 11104 and 11105 for intercluster replication. Cluster peering must be established before SVM peering, and SVM peering is required before any volume or SVM-level relationship can be created. Bandwidth requirements are driven by the daily change rate of source data — higher change rates require proportionally more replication bandwidth to sustain the configured RPO.

## Sizing Guidelines

Estimate required replication bandwidth using:

```
Required bandwidth = (Daily change rate × source volume size) / replication window (seconds)
```

| Replication Type | Latency Requirement | Bandwidth Requirement |
|---|---|---|
| SnapMirror Async | No strict requirement | Based on change rate and schedule window |
| SnapMirror Sync | <5ms RTT (sustained) | Write throughput of source workload |
| SMBC | <5ms RTT (sustained) | Write throughput of consistency group |

For SnapMirror Sync and SMBC, sustained inter-site latency above 10ms will cause automatic demotion to async mode.
