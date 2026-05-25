# Site Recovery Manager — Operations

```text
┌────────────────────────────────────────── SRM — Operations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Replication status and RPO compliance monitoring; protection group health checks daily    │   │
│   │     Test failover on schedule; recovery plan validation; planned migration for maintenance    │   │
│   │       Reprotect after failover to restore replication in reverse direction for failback       │   │
│   │      Lifecycle: upgrade SRM on both sites; run pre-checks; validate partner compatibility     │   │
│   │       Automation: SRM REST API, PowerCLI SRM, PG API, Recovery plan API for at-scale ops      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor RPO and PG health · lifecycle upgrades both sites                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │      Replication status     │  │      SRM upgrades both      │  │         SRM REST API        │   │
│   │        RPO compliance       │  │        Appliance mode       │  │         PowerCLI SRM        │   │
│   │          PG health          │  │        Pre-check run        │  │            PG API           │   │
│   │        Recovery plan        │  │        Partner compat       │  │      Recovery plan API      │   │
│   │        Test schedule        │  │        Test post-upg        │  │           Test API          │   │
│   │         Alert review        │  │        HBCR agent upg       │  │      Inventory map API      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch RPO breaches early · lifecycle upgrades both sites together                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │   SRM REST API   │    Replic: ok    │   Test failover   │   SRM upg both   │  SRM config bk   │   │
│   │   PowerCLI SRM   │  RPO: compliant  │    Planned migr   │     HBCR upg     │  Recovery plan   │   │
│   │      PG API      │   PG: healthy    │     Reprotect     │  Pre-check run   │  Mapping backup  │   │
│   │   Recovery API   │   Test: passed   │     IP custom     │   Post-upg val   │  Restore config  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers (SRM VMs both sites) · vSAN/SAN storage · WAN/DCI link · Network connectivity            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Protection group   = Set of VMs replicated and recovered together; health monitored daily            │
│  Recovery plan      = Ordered runbook; validated by test failover before a real event                 │
│  Test failover      = Isolated recovery validation; confirms plan works without impacting production  │
│  Planned migration  = Zero-RPO controlled site move for scheduled maintenance or evacuation           │
│  Failover           = Emergency activation of recovery site; may have data loss up to RPO             │
│  Reprotect          = Post-failover operation that reverses replication to enable failback            │
│  RPO compliance     = Monitoring that replication lag stays within the configured RPO threshold       │
│  HBCR (Host-Based Changed Block Replication) = vSphere Replication agent on ESXi hosts                │
│  SRM REST API       = REST interface for automating protection group and recovery plan operations     │
│  PowerCLI SRM       = PowerShell cmdlets for SRM automation: plan execution, PG management            │
│  Inventory mapping  = Config object linking protected site resources to recovery site equivalents     │
│  Partner site       = The paired remote site in an SRM configuration; protected or recovery role      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
