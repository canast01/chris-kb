# NSX — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware NSX. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```
NSX Operational Cadence
┌─────────────────────────────────────────────────────────┐
│  Daily                                                  │
│  ├── NSX Manager cluster: get cluster status → STABLE   │
│  ├── Transport nodes: GET /transport-nodes/status → UP  │
│  ├── Geneve tunnels: get tunnel status → no DOWN        │
│  ├── BGP sessions: get bgp neighbor summary → Established│
│  └── Open alarms: GET /alarms?severity=CRITICAL → 0     │
│                                                         │
│  Weekly                                                 │
│  ├── Certificate expiry check (alert at < 60 days)      │
│  ├── Backup verified on SFTP (file present, < 7 days)   │
│  ├── TEP IP pool utilisation (> 10 IPs free)            │
│  └── Edge cluster HA state review                       │
│                                                         │
│  Pre-Change                                             │
│  ├── Manual backup: POST /api/v1/node/backups/create    │
│  ├── Confirm all TNs UP, no critical alarms             │
│  └── Rollback plan documented (restore from backup)     │
│                                                         │
│  Post-Change                                            │
│  ├── Verify realisation: policy/api/v1/infra/realized-  │
│  │   state/realized-entities?intent_path=<obj>          │
│  ├── Re-check alarms, TN status, BGP                    │
│  └── Traceflow test for DFW changes                     │
└─────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Commands, syntax, and quick reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Routine checks, service validation, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Day-to-day operational tasks and how-to guides.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation, upgrade, patching, and decommission.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup configuration, restore procedures, and validation.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and reusable code.</span>
</a>

</div>
