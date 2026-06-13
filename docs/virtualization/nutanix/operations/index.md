# Nutanix — Operations

<div class="kb-summary">
Day-to-day operations for Nutanix HCI — health monitoring, administrative procedures, backup and restore, CLI reference, and automation scripts. Covers both Prism Element and CLI-based operations.

*Applies to: AOS 6.x · AHV*
</div>

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                       NUTANIX OPERATIONS OVERVIEW                                                     │
│                                                                                                       │
│  DAILY                    WEEKLY                  AS-NEEDED                                           │
│  ────────────────────     ─────────────────────   ─────────────────                                   │
│  NCC critical checks  →   NCC full run        →   LCM upgrades                                        │
│  Cluster resilience   →   Disk health check   →   Node add/remove                                     │
│  Storage capacity     →   LCM inventory check →   Snapshot management                                 │
│  Active alerts        →   Replication status  →   PD failover/test                                    │
│  CVM health           →   Certificate expiry  →   Maintenance mode                                    │
│                                                                                                       │
│  TOOLS                                                                                                │
│  ──────────────────────────────────────────────────────────────                                       │
│  ncli   → cluster, storage, alerts, users, protection domains                                         │
│  acli   → VM lifecycle, networks, images, snapshots (AHV only)                                        │
│  ncc    → automated health checks (400+ tests)                                                        │
│  allssh → run a command across all CVMs in parallel                                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="health-checks/">
    <strong>Health Checks</strong>
    <span>Daily and weekly cluster health routine — NCC checks, resilience, storage capacity, CVM and AHV host health.</span>
  </a>
  <a class="kb-card" href="procedures/">
    <strong>Procedures</strong>
    <span>Maintenance mode, LCM upgrades, adding/removing nodes, cloning VMs, snapshot management, protection domains.</span>
  </a>
  <a class="kb-card" href="cli-reference/">
    <strong>CLI Reference</strong>
    <span>Complete ncli, acli, ncc, allssh, genesis, nodetool, and curator_cli command reference.</span>
  </a>
  <a class="kb-card" href="backup-restore/">
    <strong>Backup & Restore</strong>
    <span>Native snapshots, Protection Domain replication, Nutanix DR policies, Veeam, and HYCU integration.</span>
  </a>
  <a class="kb-card" href="scripts/">
    <strong>Scripts</strong>
    <span>Reusable scripts for health snapshots, NCC automation, storage reports, VM inventory, and maintenance helpers.</span>
  </a>
</div>
