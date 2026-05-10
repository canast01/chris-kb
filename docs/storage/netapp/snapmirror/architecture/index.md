# SnapMirror — Overview

> Part of the [SnapMirror Architecture](../) reference.

---

## Overview

SnapMirror is ONTAP's built-in replication engine, providing volume-level and SVM-level replication across ONTAP clusters. It supports three primary operating modes: asynchronous (SnapMirror Async, RPO-based), synchronous (SnapMirror Synchronous, zero RPO), and extended data protection (XDP/SnapVault, backup retention). Relationships are always managed from the destination cluster. SnapMirror Business Continuity (SMBC/AutomatedFailOver) extends synchronous replication with transparent host-level failover for SAN workloads.

## Replication Modes

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

## Replication Types

| Type | RPO | Description |
|---|---|---|
| SnapMirror Async | Configurable, minutes to hours | Standard volume replication; transfers run on a schedule; destination is read-only DP volume |
| SnapMirror Sync | Zero RPO | Every write acknowledged on both source and destination; requires <5ms RTT between clusters |
| SnapMirror Business Continuity (SMBC) | Zero RPO, transparent failover | Consistency group-based; mediator-assisted automatic failover; no host reconfiguration |
| SnapVault / XDP | Daily/weekly backup copies | Extended data protection; independent retention on destination; replaces legacy SnapVault |

## Connectivity

Intercluster LIFs must be on a dedicated replication network, separate from data and management traffic. ONTAP uses TCP ports 11104 and 11105 for intercluster replication. Cluster peering must be established before SVM peering, and SVM peering is required before any volume or SVM-level relationship can be created. Bandwidth requirements are driven by the daily change rate of source data — higher change rates require proportionally more replication bandwidth to sustain the configured RPO.

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
