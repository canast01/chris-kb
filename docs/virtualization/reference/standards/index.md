# Virtualization Standards

Build and operating standards for virtualization platforms.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Virtualization Standards Hub                         │
├──────────────────┬──────────────────┬──────────────────────────────────┤
│  Build Standards │  Config Standards│  Operational Standards           │
├──────────────────┼──────────────────┼──────────────────────────────────┤
│ • Naming         │ • Cluster HA/DRS │ • Access / RBAC                  │
│ • Host Build     │ • VM sizing      │ • Backup RPO/RTO tiers           │
│ • VM template    │ • Datastore type │ • Snapshot age/cleanup           │
│                  │   + thresholds   │ • Maintenance windows            │
│                  │ • Network MTU    │ • Tagging (env/owner/tier)       │
│                  │   + port groups  │                                  │
├──────────────────┴──────────────────┴──────────────────────────────────┤
│  All deviations must be documented with justification + team lead sign-off │
└─────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="naming-standard/">
  <strong>Naming Standard</strong>
  <span>Cluster, host, datastore, port group, VM, and folder naming guidance.</span>
</a>

<a class="kb-card" href="cluster-standard/">
  <strong>Cluster Standard</strong>
  <span>Cluster settings, HA, DRS, EVC, admission control, and baseline expectations.</span>
</a>

<a class="kb-card" href="host-build-standard/">
  <strong>Host Build Standard</strong>
  <span>ESXi host configuration, networking, storage, logging, NTP, DNS, and access.</span>
</a>

<a class="kb-card" href="datastore-standard/">
  <strong>Datastore Standard</strong>
  <span>Datastore naming, usage, capacity, alerting, and ownership.</span>
</a>

<a class="kb-card" href="vm-standard/">
  <strong>VM Standard</strong>
  <span>VM sizing, tools, snapshots, tags, naming, and lifecycle expectations.</span>
</a>

<a class="kb-card" href="access-standard/">
  <strong>Access Standard</strong>
  <span>Roles, groups, permissions, break-glass access, and review cadence.</span>
</a>


<a class="kb-card" href="backup-standards/">
  <strong>Backup Standards</strong>
  <span>Backup job requirements, retention targets, exclusion rules, and coverage verification.</span>
</a>

<a class="kb-card" href="maintenance-window-standards/">
  <strong>Maintenance Window Standards</strong>
  <span>Scheduling process, communication requirements, change freeze periods, and approval gates.</span>
</a>

<a class="kb-card" href="snapshot-standards/">
  <strong>Snapshot Standards</strong>
  <span>Maximum snapshot age, size limits, naming convention, and consolidation requirements.</span>
</a>

<a class="kb-card" href="tagging-standards/">
  <strong>Tagging Standards</strong>
  <span>Required tag categories, values, ownership assignment, and enforcement policy.</span>
</a>
</div>
