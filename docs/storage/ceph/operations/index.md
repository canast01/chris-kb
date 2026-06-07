# Ceph — Operations

<!-- diagram:ceph-operations -->

<div class="kb-summary">
Ceph day-2 operations: cluster health monitoring, OSD management, pool tuning, CRUSH map updates, RBD/CephFS/RGW administration, and routine maintenance procedures.
</div>

```text
┌─────────────────────────────────────────── Ceph Operations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Ceph Day-2 Operations                                     │   │
│   │          Six sub-sections: CLI, Health Checks, Procedures, Lifecycle, Backup, Scripts         │   │
│   │               Health baseline: HEALTH_OK + all OSDs up+in + all PGs active+clean              │   │
│   │           Before maintenance: set noout flag; ensure HEALTH_OK before removing flag           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                 ▼                               ▼                                 ▼                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌───────────────────────────────┐   │
│   │        Daily Health        │  │       OSD Management       │  │           Lifecycle           │   │
│   │      ceph health detail    │  │       OSD replacement      │  │         cephadm upgrade       │   │
│   │          PG status         │  │       Add/remove nodes     │  │         Upgrade sequence      │   │
│   │       Capacity review      │  │       CRUSH rebalance      │  │          RBD mirroring        │   │
│   └────────────────────────────┘  └────────────────────────────┘  └───────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="cli-reference/">
    <span class="kb-card-title">CLI Reference</span>
    <span class="kb-card-desc">ceph, ceph-admin, rbd, radosgw-admin, cephadm command reference</span>
  </a>
  <a class="kb-card" href="health-checks/">
    <span class="kb-card-title">Health Checks</span>
    <span class="kb-card-desc">Run This Routine: OSD health, PG status, MON quorum, capacity review</span>
  </a>
  <a class="kb-card" href="procedures/">
    <span class="kb-card-title">Procedures</span>
    <span class="kb-card-desc">OSD replacement, adding nodes, reweight, scrub scheduling, pool resize</span>
  </a>
  <a class="kb-card" href="install-upgrade/">
    <span class="kb-card-title">Lifecycle & Upgrades</span>
    <span class="kb-card-desc">cephadm upgrade, version compatibility, upgrade sequence, rollback</span>
  </a>
  <a class="kb-card" href="backup-restore/">
    <span class="kb-card-title">Backup & Restore</span>
    <span class="kb-card-desc">RBD snapshots and export, cluster config backup, crash dump export</span>
  </a>
  <a class="kb-card" href="scripts/">
    <span class="kb-card-title">Scripts</span>
    <span class="kb-card-desc">health-check.sh, osd-replace.sh, capacity-report.sh, pg-status.sh</span>
  </a>
</div>
