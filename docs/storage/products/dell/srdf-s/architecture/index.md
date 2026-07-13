---
tags:
  - architecture
  - dell
description: "Dell PowerMax SRDF/S synchronous replication — every host write is committed to both R1 and R2 before acknowledgement, guaranteeing RPO = 0; requires..."
---
# SRDF/S — Architecture

<div class="kb-summary">
Dell PowerMax SRDF/S synchronous replication — every host write is committed to both R1 and R2 before acknowledgement, guaranteeing RPO = 0; requires ≤10ms inter-site RTT.

*Applies to: SRDF/S*
</div>

![SRDF/S — Architecture — Diagram](../../../../../assets/storage-dell-srdf-s-architecture-diagram.svg)


![SRDF/S Architecture](../../../../../assets/srdf-s-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Synchronous write commit model, pair states, RTT requirements, SYMCLI commands, and RTO targets.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>SRM automated failover, Solutions Enabler, and SRDF/Metro active-active variant.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>RTT thresholds, SRDF group naming, consistency group design, and failover runbook.</span></a>
</div>

| Pair State | Description | Host Write Impact |
|---|---|---|
| Synchronized | R1 and R2 identical; writes committed to both | Full protection, RPO = 0 |
| SyncInProg | Initial or resync copy in progress | R1 writable; R2 not consistent |
| Suspended | Replication paused | R1 writable; R2 stale |
| Failed Over | R1 unavailable; R2 writable | R2 takes production I/O |

