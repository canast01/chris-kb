# Aria Ops for Networks — Operations

```
┌──────────── Aria Networks Operations Overview ─────────────────────────────────┐
│                                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │ CLI Ref      │  │ Health Checks│  │  Procedures  │  │ Install & Upgrade │   │
│  │ Platform CLI │  │ Platform VM  │  │ Add data src  │  │ OVA deploy order  │  │
│  │ Collector CLI│  │ Collector    │  │ NetFlow config│  │ Platform first    │  │
│  │ REST API     │  │ Data sources │  │ Microseg flow │  │ then Collectors   │  │
│  └──────────────┘  │ Flow ingestion│  │ Compliance rpt│  └───────────────────┘ │
│                    └──────────────┘  └──────────────┘                          │
│  ┌──────────────┐  ┌─────────────────────────────────────────────────────────┐ │
│  │ Backup &     │  │  Scripts (Python)                                       │ │
│  │ Restore      │  │  auth token │ list sources │ get flows │ open problems  │ │
│  │ Config export│  │  security recs CSV │ health check │ daily report       │  │
│  └──────────────┘  └─────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────┘
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
