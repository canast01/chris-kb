# SANnav — Operations


<div class="kb-summary">
SANnav day-to-day operations — dashboard monitoring, fabric discovery, alert management, firmware upgrades, and reporting.
</div>

```text
┌───────────────────────────────────────── SANnav — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Day-to-day SANnav operational tasks: health checks, fabric management, lifecycle       │   │
│   │     Health checks: fabric status dashboard, port error counters, SFP Tx/Rx, switch CPU/mem    │   │
│   │       Zone management: zone wizard, alias creation, zone set activation — changes logged      │   │
│   │      Lifecycle: SANnav version upgrade, FabricOS firmware job scheduling, backup/restore      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily health → fabric management tasks → scheduled maintenance and lifecycle ops                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Health Checks        │  │         Fabric Mgmt         │  │          Lifecycle          │   │
│   │       Dashboard review      │  │         Zone wizard         │  │        SANnav upgrade       │   │
│   │       Port error check      │  │       Alias management      │  │        FabricOS jobs        │   │
│   │       SFP power check       │  │       Zone activation       │  │        Config backup        │   │
│   │        Switch CPU/mem       │  │          Port admin         │  │         Restore test        │   │
│   │         Alert review        │  │        ISL monitoring       │  │       Performance rpt       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All zone changes require change ticket; activation logged in SANnav audit trail                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │    Frequency     │    SANnav path    │      Output      │      Notes       │   │
│   │  Fabric health   │      Daily       │     Dashboard     │  Status summary  │   Check alerts   │   │
│   │   Port errors    │      Daily       │ Inventory > Ports │  Error counters  │ Clear after fix  │   │
│   │  Config backup   │      Weekly      │   Admin > Backup  │   Backup file    │  Off-site copy   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SANnav VM · Brocade FC switches · ISL cables · FC SFP optics                             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Zone wizard   = SANnav GUI tool for creating zones, aliases, and zone sets step-by-step            │
│    Alias         = Named group of port WWNs; used in zone definitions for readability                 │
│    Zone set      = Named collection of zones; one zone set active per fabric at a time                │
│    Activation    = cfgenable equivalent; pushes the active zone set to all fabric switches            │
│    Port admin    = Enable/disable individual FC ports via SANnav without CLI access                   │
│    ISL           = Inter-Switch Link; trunk between switches; monitored for utilisation               │
│    FabricOS job  = SANnav firmware upgrade task targeting one or more switches                        │
│    Config backup = SANnav application backup (not switch backup); includes DB and settings            │
│    SFP power     = Optical Tx/Rx dBm values; SANnav alerts on out-of-range readings                   │
│    Error counter = CRC, Loss of Signal, Loss of Sync counts per port; nonzero = investigate           │
│    Audit trail   = SANnav log of all config changes including who, what, and when                     │
│    Performance   = SANnav bandwidth utilisation graphs per port and ISL over time                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Step-by-step operational procedures and runbooks.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Proactive SANnav health monitoring and validation routines.</span>
</a>

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known problems, symptoms, and resolution steps.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>SANnav installation, upgrade procedures, and version management.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Configuration backup, restore operations, and recovery validation.</span>
</a>

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>SANnav command reference for day-to-day operations.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for common operational tasks.</span>
</a>

</div>
