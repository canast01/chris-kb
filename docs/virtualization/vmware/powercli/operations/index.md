# PowerCLI — Operations

<div class="kb-summary">
PowerCLI operational reference: cmdlet library, automation scripts, health check routines, operational procedures, and lifecycle management.
</div>

```text
┌─────────────────────────────────── PowerCLI — Operations Reference ───────────────────────────────────┐
│                                                                                                       │
│   Operational PowerCLI use cases: health checks, bulk operations, exports, and lifecycle tasks        │
│   All scripts follow a connect → query → act → verify pattern                                         │
│   Service accounts should be used for unattended scripts; avoid interactive prompts in automation     │
│                                                                                                       │
│   Health checks                                                                                       │
│   Daily routine: host connection state, VM power state, snapshot inventory, datastore capacity        │
│   Weekly: cluster HA status, vSAN health service, certificate expiry, alarm state                     │
│   Run health check script before and after every change window                                        │
│                                                                                                       │
│   Operational procedures                                                                              │
│   Host maintenance: set maintenance mode → wait for DRS drain → patch → exit maintenance              │
│   Bulk VM power: filter VMs by tag or folder → PowerOff or restart with confirmation                  │
│   Snapshot audit: find all VMs with snapshots older than N days → report or remove                    │
│   Datastore migration: Storage vMotion VMs from source to target datastore in a pipeline              │
│                                                                                                       │
│   Scripts and exports                                                                                 │
│   VM inventory report: CSV with VM name, CPU, RAM, OS, IP, tools version, snapshot count              │
│   Permissions export: role assignments per vCenter object for audit or rebuild                        │
│   Storage policy compliance: find VMs not meeting their assigned SPBM policy                          │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Get-VM     = retrieves VM objects; filter with -Name, -VMHost, -Datastore, -Tag                     │
│   Set-VM     = modifies VM properties; -NumCpu, -MemoryGB, -Notes; requires PoweredOff for hardware   │
│   Export-Csv = exports object properties to CSV; used for reports and audit exports                   │
│   Pipeline   = PowerShell object passing; Get-VM | Where-Object | ForEach-Object pattern              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Cmdlets for VMs, hosts, clusters, storage, networking, vSAN, and snapshots.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Production-ready scripts: VM inventory, host health, snapshot audit, vSAN reporting, and storage reports.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily and weekly platform health routine covering hosts, VMs, storage, and cluster state.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Common operational tasks: bulk VM operations, host maintenance, snapshot cleanup, and tag management.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Lifecycle</strong>
  <span>PowerCLI version upgrades, module management, and compatibility with vCenter versions.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>VM inventory exports, storage policy snapshots, permissions exports, tag backups, and module inventory.</span>
</a>

</div>
