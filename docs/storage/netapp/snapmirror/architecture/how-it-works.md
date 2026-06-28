---
tags:
  - architecture
  - netapp
---
# SnapMirror — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Replication Types, Components, Connectivity, Key Commands and 2 more sections.

*Applies to: SnapMirror*
</div>
![SnapMirror — How It Works](../../../../assets/storage-netapp-snapmirror-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Source Volume\n(primary SVM)" as SRC
participant "SnapMirror Engine" as SM
participant "Intercluster LIF\n(TCP 11104 / 11105)" as NET
participant "Destination Volume\n(DP — read-only)" as DST

SRC -> SM: Initialize relationship
SM -> SRC: Baseline Snapshot
SM -> NET: Transfer baseline (full copy)
NET -> DST: Write baseline
DST --> SM: Baseline complete

loop Scheduled update
  SM -> SRC: New Snapshot
  SM -> SM: Delta vs last transfer Snapshot
  SM -> NET: Transfer delta blocks
  NET -> DST: Apply delta
  DST --> SM: LSN updated
  SM -> SRC: Delete previous transfer Snapshot
end

note over SM,DST: Break + promote DST\nto R/W for DR activation
@enduml
```

## Overview

SnapMirror is ONTAP's built-in replication engine, providing volume-level and SVM-level replication across ONTAP clusters. It supports three primary operating modes: asynchronous (SnapMirror Async, RPO-based), synchronous (SnapMirror Synchronous, zero RPO), and extended data protection (XDP/SnapVault, backup retention). Relationships are always managed from the destination cluster. SnapMirror Business Continuity (SMBC/AutomatedFailOver) extends synchronous replication with transparent host-level failover for SAN workloads.

## Replication Types

| Type | RPO | Description |
|---|---|---|
| SnapMirror Async | Configurable, minutes to hours | Standard volume replication; transfers run on a schedule; destination is read-only DP volume |
| SnapMirror Sync | Zero RPO | Every write acknowledged on both source and destination; requires <5ms RTT between clusters |
| SnapMirror Business Continuity (SMBC) | Zero RPO, transparent failover | Consistency group-based; mediator-assisted automatic failover; no host reconfiguration |
| SnapVault / XDP | Daily/weekly backup copies | Extended data protection; independent retention on destination; replaces legacy SnapVault |

```mermaid
graph LR
  SRC["Source Volume\nSVM / Cluster A"] -->|"SnapMirror replication\n(incremental block diff)"| DST["Destination Volume\nSVM / Cluster B — read-only"]
  SRC --> SNAP[("Local Snapshots")]
  DST -->|"break to activate for DR"| DRACT["DR Active Volume\n(after SnapMirror break)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class SRC,DST ctrl
  class SNAP store
  class DRACT dr
```

## Components

| Component | Description |
|---|---|
| Source volume | Read/write volume on the source cluster; the origin of replicated data |
| Destination volume | DP (data protection) type, read-only; managed by the replication engine |
| SnapMirror policy | Defines rules, schedule, and retention for the relationship |
| Cluster peer relationship | Trust relationship between two ONTAP clusters; prerequisite for all SnapMirror |
| SVM peer relationship | Required for cross-SVM replication; establishes peer trust at the data SVM layer |
| Intercluster LIFs | Dedicated network interfaces used exclusively for SnapMirror replication traffic |
| ONTAP Mediator | External Linux VM used as a quorum witness for SMBC automatic failover |

## Connectivity

Intercluster LIFs must be on a dedicated replication network, separate from data and management traffic. ONTAP uses TCP ports 11104 and 11105 for intercluster replication. Cluster peering must be established before SVM peering, and SVM peering is required before any volume or SVM-level relationship can be created.

| Replication Type | Latency Requirement | Bandwidth Requirement |
|---|---|---|
| SnapMirror Async | No strict requirement | Based on change rate and schedule window |
| SnapMirror Sync | <5ms RTT (sustained) | Write throughput of source workload |
| SMBC | <5ms RTT (sustained) | Write throughput of consistency group |

Estimate required replication bandwidth: `(Daily change rate × source volume size) / replication window (seconds)`

## Key Commands

```bash
# Show all relationships with lag time and health
snapmirror show -fields lag-time,healthy,last-transfer-end-timestamp

# Show full detail for a specific relationship
snapmirror show -destination-path svm_dst:vol_dst

# Show relationships in broken-off state
snapmirror show -relationship-status broken-off

# Trigger immediate incremental update
snapmirror update -destination-path svm_dst:vol_dst

# Resync a broken-off relationship
snapmirror resync -destination-path svm_dst:vol_dst

# Break a relationship for DR failover (makes destination read-write)
snapmirror break -destination-path svm_dst:vol_dst

# Initialize a new relationship (baseline transfer)
snapmirror initialize -destination-path svm_dst:vol_dst

# Quiesce a relationship (pause future transfers, finishes current)
snapmirror quiesce -destination-path svm_dst:vol_dst

# Show transfer history
snapmirror show-history -destination-path svm_dst:vol_dst
```

## DR Failover Sequence

1. **Detect RPO breach or site failure** — identify that the source is unavailable or lag has exceeded the RPO threshold
2. **Quiesce the relationship** — `snapmirror quiesce -destination-path svm_dst:vol_dst` (allows in-flight transfer to complete)
3. **Break the relationship** — `snapmirror break -destination-path svm_dst:vol_dst` (makes destination read-write)
4. **Mount/present the destination volume to DR hosts** — rescan iSCSI/FC on host or remount NFS exports
5. **Start application on DR hosts** — verify data integrity; bring application online
6. **Failback** — once source site recovers, reverse resync: `snapmirror resync -destination-path svm_src:vol_src` (treating the original source as the new destination until fully synced)
7. **Final reverse resync** — break and remount on original source hosts; re-establish the original replication direction

## SVM-Level Replication

SVM DR replicates the full SVM configuration (volumes, LIFs, NFS exports, CIFS shares, igroups) in addition to data:

```bash
# Create an SVM DR relationship
snapmirror create -source-path svm_src: -destination-path svm_dst: -type XDP -policy MirrorAllSnapshots

# Initialize SVM DR baseline
snapmirror initialize -destination-path svm_dst:

# Update SVM DR configuration
snapmirror update -destination-path svm_dst:

# Activate SVM at DR site
snapmirror break -destination-path svm_dst:
vserver start -vserver svm_dst
```

---

## See also

- [Snapmirror — Design Standards](../design-standards/)
- [Snapmirror — Integrations](../integrations/)
- [Snapmirror — Deploy](../../deploy/)
