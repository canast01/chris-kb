# SRM — Operations



<div class="kb-summary">
SRM — Operations reference.
</div>

```
┌────────────────────────────────────────── SRM — Operations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  SRM — Day-to-Day Operations                                  │   │
│   │          Daily: review job status · check health alerts · verify last backup/replica          │   │
│   │            Weekly: review capacity trends · test restore sample · review error logs           │   │
│   │             Monthly: full restore test · review retention · audit service accounts            │   │
│   │              Quarterly: DR failover test · firmware review · update documentation             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Backup/Replicate      │  │           Monitor           │  │           Recover           │   │
│   │       srm-cli vm list       │  │      srm-cli plan test      │  │     srm-cli recovery run    │   │
│   │        Schedule jobs        │  │        Health checks        │  │       Instant restore       │   │
│   │        Retention mgmt       │  │       Capacity alerts       │  │        Failover test        │   │
│   │       Consistency grp       │  │          Log review         │  │          DR runbook         │   │
│   │        Policy updates       │  │         SLA tracking        │  │         Validate RTO        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────────── SRM — Operations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  SRM — Day-to-Day Operations                                  │   │
│   │          Daily: review job status · check health alerts · verify last backup/replica          │   │
│   │            Weekly: review capacity trends · test restore sample · review error logs           │   │
│   │             Monthly: full restore test · review retention · audit service accounts            │   │
│   │              Quarterly: DR failover test · firmware review · update documentation             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Backup/Replicate      │  │           Monitor           │  │           Recover           │   │
│   │       srm-cli vm list       │  │      srm-cli plan test      │  │     srm-cli recovery run    │   │
│   │        Schedule jobs        │  │        Health checks        │  │       Instant restore       │   │
│   │        Retention mgmt       │  │       Capacity alerts       │  │        Failover test        │   │
│   │       Consistency grp       │  │          Log review         │  │          DR runbook         │   │
│   │        Policy updates       │  │         SLA tracking        │  │         Validate RTO        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>PowerCLI cmdlets and REST API commands for SRM management.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Weekly and quarterly checks for protection groups, SRA, and recovery plans.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Recovery plans, test failover, planned migration, and cleanup runbooks.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Version compatibility, upgrade sequence, licensing, and EOL tracking.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>SRM configuration backup and restore procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for health checks, test failover, and recovery reporting.</span>
</a>

</div>
