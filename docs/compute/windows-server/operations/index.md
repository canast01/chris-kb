# Windows Server — Operations


```
┌───────────────────────────────────── Windows Server — Operations ─────────────────────────────────────┐
│                                                                                                       │
│  Windows Server day-to-day operations: patching, AD management, monitoring, and backups.              │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Patch Management      │  │        AD Operations        │  │          Monitoring         │   │
│   │     WSUS / Intune / MECM    │  │    User / group lifecycle   │  │     Event Viewer alerts     │   │
│   │    Patch Tuesday cadence    │  │   GPO create + test + link  │  │     Performance Monitor     │   │
│   │     WSFC: rolling update    │  │  OU delegation: least priv  │  │     Task Scheduler jobs     │   │
│   │    Test in non-prod first   │  │   AD recycle bin: restore   │  │      SNMP / WMI / WinRM     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · Domain Controllers · WSUS server · backup storage                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  WSUS         = Windows Server Update Services; on-prem patch distribution                            │
│  MECM         = Microsoft Endpoint Configuration Manager; enterprise patching                         │
│  Patch Tuesday= second Tuesday of month; Microsoft releases cumulative updates                        │
│  WSFC         = Windows Server Failover Cluster; rolling update with CAU                              │
│  CAU          = Cluster Aware Updating; non-disruptive patch application                              │
│  AD Recycle Bin= restore deleted objects within tombstone lifetime (default 180d)                     │
│  OU delegation= grant specific permissions on OU without Domain Admin                                 │
│  WMI          = Windows Management Instrumentation; query system state                                │
│  Task Scheduler= built-in job scheduler; XML-based task definitions                                   │
│  Event Viewer = Windows event log GUI; filter by ID/source/level                                      │
│  Performance Monitor= real-time/historical counter data; PerfMon.exe                                  │
│  SNMP         = network monitoring protocol; available via Windows feature                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
</div>
