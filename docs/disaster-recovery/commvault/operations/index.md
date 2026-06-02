# Commvault — Operations



<div class="kb-summary">
Commvault — Operations reference.
</div>

```
┌─────────────────────────────── Commvault Operations — Day-to-Day Tasks ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Commvault Operations Scope                                  │   │
│   │        Covers: backup/restore, health checks, CLI, install/upgrade, scripts, procedures       │   │
│   │       Primary interfaces: Command Center (web), CommCell Console (Java), qoperation CLI       │   │
│   │       Daily: monitor job activity, check alerts, verify SLA compliance, review failures       │   │
│   │        Weekly: run reports, validate aux copies, check DDB health, review storage usage       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Operational domains map to separate runbooks: backup-restore, health, install, procedures          │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Backup/Restore    │     Health Checks     │    Install/Upgrade    │      Scripts/CLI      │   │
│   │     Job monitoring    │      CV_DIAG logs     │      SP download      │     qoperation run    │   │
│   │    On-demand backup   │     DDB validation    │     Upgrade wizard    │       qlist jobs      │   │
│   │    Granular restore   │    MA connectivity    │    Pre-req checker    │     qmodify policy    │   │
│   │       SLA report      │     Alerts review     │     Rollback plan     │     REST API calls    │   │
│   │    Aux copy status    │    Disk space check   │   Post-upgrade test   │       Python SDK      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Operations workstation needs Java JRE (CommCell Console) or browser (Command Center)                 │
│  CLI qoperation runs on CommServe or any Windows/Linux host with CV client installed                  │
│  Network: ops console needs TCP 8401 to CommServe, 443 for Command Center                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  qoperation     = Commvault CLI binary on CommServe for submitting jobs and changes                   │
│  qlist          = Commvault CLI for listing jobs, clients, policies, and library status               │
│  qmodify        = Commvault CLI for modifying subclients, schedules, and policies                     │
│  SLA            = Service Level Agreement; Commvault tracks backup success rate vs target             │
│  Job Activity   = CommCell Console/Command Center view of all running and queued jobs                 │
│  Alerts         = Configured thresholds triggering email/SNMP on job failures or disk low             │
│  DDB Validation = Integrity scan of dedup database to detect/repair corruption                        │
│  Aux Copy       = Secondary copy replication job; must be monitored for lag/failures                  │
│  SP             = Service Pack; Commvault patch bundle (e.g. SP32, SP33)                              │
│  CV_DIAG        = Commvault diagnostic log collector; gathers logs from all components                │
│  REST API       = Commvault REST API (v4) for programmatic management and automation                  │
│  Command Center = Modern web-based management UI on CommServe port 443                                │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>qcommand, qlist, qoperation, REST API, and job management.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily checks, job review, MediaAgent health, and DDB monitoring.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Change readiness, maintenance windows, and operational procedures.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install &amp; Upgrade</strong>
  <span>Version matrix, upgrade workflow, and lifecycle management.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup &amp; Restore</strong>
  <span>Backup policies, restore procedures, and recovery validation.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for health checks and operations.</span>
</a>

</div>
