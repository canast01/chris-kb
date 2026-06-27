---
tags:
  - architecture
  - dell
---
# RecoverPoint — Architecture

<div class="kb-summary">
Dell EMC RecoverPoint journal-based replication — RPA clusters intercept writes via splitters and maintain a rolling journal enabling point-in-time recovery across CDP, CRR, and CLR modes.

*Applies to: RecoverPoint 5.x*
</div>

![RecoverPoint — Architecture — Diagram](../../../../assets/storage-dell-recoverpoint-architecture-diagram.svg)


![RecoverPoint Architecture](../../../../assets/recoverpoint-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>RPA topology, splitter types, consistency groups, journal sizing, and HA model.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>PowerMax, Unity, VPLEX, and RecoverPoint for VMs (RP4VM).</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>CG naming, journal sizing formula, RPO targets, and RPA cluster placement.</span></a>
</div>

| Mode | Description | RPO |
|---|---|---|
| CDP (Continuous Data Protection) | Local journal; recover to any point in time | ~0 seconds |
| CRR (Continuous Remote Replication) | Async replication to DR site | Seconds to minutes |
| CLR (Concurrent Local and Remote) | Simultaneous local CDP + remote CRR | Per-copy |

