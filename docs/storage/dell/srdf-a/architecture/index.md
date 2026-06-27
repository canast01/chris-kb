---
tags:
  - architecture
  - dell
---
# SRDF/A — Architecture

<div class="kb-summary">
Dell PowerMax SRDF/A asynchronous replication — delta set cycle model buffers writes and transmits to R2 on a ~30-second cycle; RPO equals the last completed cycle.

*Applies to: SRDF/A*
</div>

![SRDF/A — Architecture — Diagram](../../../../assets/storage-dell-srdf-a-architecture-diagram.svg)


![SRDF/A Architecture](../../../../assets/srdf-a-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Delta set mechanics, SRDF group design, pair states, SYMCLI commands, and bandwidth sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>SRM, Solutions Enabler, and TimeFinder/SnapVX for backup offload.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>SRDF group naming, cycle time standards, lag thresholds, and DSE sizing.</span></a>
</div>

| State | Meaning | Normal? |
|---|---|---|
| Consistent | R2 is consistent and receiving cycles | Yes — normal SRDF/A state |
| SyncInProg | Synchronisation in progress after resume | Transient |
| Transmit Idle | No data being transmitted | Investigate if unexpected |
| Suspended | Replication manually suspended | Expected for maintenance |
| Failed Over | R1 read-only; R2 writable | Active failover underway |

