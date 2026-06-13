---
tags:
  - operations
  - windows
---
# SQL Server — Operations

<div class="kb-summary">
Health checks, procedures, CLI, backup/restore, upgrades, and scripts.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌─────────────────────────────────────── SQL Server — Operations ───────────────────────────────────────┐
│                                                                                                       │
│   Six operational sub-sections covering the full DBA day-to-day workflow for SQL Server               │
│   Backup/restore and health checks are the most time-sensitive regular activities                     │
│   Install/upgrade covers both in-place and side-by-side major version upgrade paths                   │
│                                                                                                       │
│   Sub-sections                                                                                        │
│   Health Checks: AG health, blocking chains, wait stats, disk usage, SQL Agent job status             │
│   Procedures: manual failover, database attach/detach, log shipping switchover                        │
│   CLI Reference: sqlcmd, Invoke-Sqlcmd, BCP, Backup-SqlDatabase, key DMV queries                      │
│   Backup/Restore: full/differential/log backup strategy, RESTORE WITH NORECOVERY, PITR                │
│   Install/Upgrade: in-place upgrade, compatibility level management, post-upgrade steps               │
│   Scripts: automated backup rotation, index maintenance, AG health check, blocking alerts             │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Always On AG   = Availability Group; check with sys.dm_hadr_availability_replica_states             │
│   wait stats     = sys.dm_os_wait_stats; top wait types reveal system bottlenecks                     │
│   RESTORE NORECOVERY = keeps database in restoring state; required for log chain restore              │
│   IndexOptimize  = Ola Hallengren proc; industry-standard index fragmentation maintenance             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="health-checks/">Health Checks</a>
  <a class="kb-card" href="procedures/">Procedures</a>
  <a class="kb-card" href="cli-reference/">Cli Reference</a>
  <a class="kb-card" href="backup-restore/">Backup Restore</a>
  <a class="kb-card" href="install-upgrade/">Install Upgrade</a>
  <a class="kb-card" href="scripts/">Scripts</a>
</div>

