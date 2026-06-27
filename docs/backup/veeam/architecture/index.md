---
tags:
  - architecture
  - veeam
---
# Veeam — Architecture

<div class="kb-summary">
Veeam Backup & Replication architecture — Backup Server manages scheduling, Proxies handle data movement via VADP or agent, and SOBR provides tiered storage with immutable object offload.

*Applies to: Veeam Backup & Replication 12.x*
</div>

![Veeam — Architecture — Diagram](../../../assets/backup-veeam-architecture-diagram.svg)


![Veeam Architecture](../../../assets/veeam-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Proxy transport modes, SOBR tiers, supported platforms, retention schedule, and sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware vSphere, Hyper-V, physical agents, and cloud (AWS/Azure) integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Job naming, retention schedule, SOBR design, proxy placement, and immutability settings.</span></a>
</div>

| Component | Role |
|---|---|
| Backup Server | Management, scheduler, config DB; Windows Server + SQL |
| Backup Proxy | Data mover; reads VM data via VADP (hot-add, Direct NFS, NBD) or agent |
| Backup Repository | Target storage for .vbk/.vib backup files |
| Scale-Out Backup Repository (SOBR) | Tiered pool: performance extent (fast disk) + capacity tier (object storage) |
| Veeam ONE | Monitoring, alerting, and reporting; separate server |

