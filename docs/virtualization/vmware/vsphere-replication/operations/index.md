# vSphere Replication — Operations

<div class="kb-summary">
vSphere Replication — Operations reference.
</div>

```text
┌────────────────────────────────── vSphere Replication — Operations ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Monitor replication status for all protected VMs; check RPO compliance and missed sync counts │   │
│   │   Configure replication: select VM, set RPO, choose target datastore and network compression  │   │
│   │ Pause and resume replication: maintenance window operations; resume to trigger full delta sync│   │
│   │   Test recovery: recover to isolated test network; validate VM boots at target; revert test   │   │
│   │   Appliance upgrades: upgrade VRMS and VRS before upgrading protected VMs and vCenter hosts   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor RPO compliance · lifecycle upgrades appliances before hosts · automation via SRM │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │        RPO compliance       │  │         VRMS upgrade        │  │          SRM plans          │   │
│   │         Missed sync         │  │         VRS upgrade         │  │           REST API          │   │
│   │          Rep health         │  │        Cert rotation        │  │       Aria Ops alerts       │   │
│   │         Pause/resume        │  │         vCenter upg         │  │        Scheduled test       │   │
│   │        Test recovery        │  │        Config backup        │  │         VR API calls        │   │
│   │        BW utilisation       │  │         Post-upg val        │  │        Monitoring API       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops track RPO and sync health · lifecycle upgrades appliances · automation tests and alerts  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │   VR REST API    │     RPO: met     │    Configure VM   │   VRMS upgrade   │  Config export   │   │
│   │   vSphere API    │     Sync: ok     │     Pause rep     │   VRS upgrade    │   Rep metadata   │   │
│   │     SRM API      │    BW: normal    │     Resume rep    │  Cert rotation   │  Restore config  │   │
│   │   Aria Ops API   │  Appliance: up   │   Test recovery   │   Post-upg val   │   Site re-pair   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (VRMS + VRS) · RAM DIMMs · WAN link · Target storage array or vSAN · vCenter appliance       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO compliance     = All replicated VMs meeting their configured RPO within the monitoring window    │
│  Missed sync        = Replication cycle that failed to complete within the RPO window; alerts in      │
│  Pause replication  = Temporarily halting delta sync; all changes accumulate until resumed            │
│  Resume replication = Restarting replication after pause; triggers full delta resync of changed blocks│
│  Test recovery      = Recovering replica to isolated test network; validates DR readiness without     │
│  Bandwidth usage    = Network throughput consumed by replication; monitored to prevent link saturation│
│  VRMS upgrade       = OVF/VAMI-based upgrade of the management appliance; must precede VRS upgrade    │
│  VRS upgrade        = Upgrade of the replication server appliance; precedes vCenter and host upgrades │
│  Configuration backup = Export of VR replication config; used for recovery if appliance rebuild needed│
│  Site pairing health = vCenter-to-vCenter VR trust relationship; must be green for replication to     │
│  SRM recovery plan  = Orchestrated failover workflow that uses VR replicas as recovery source         │
│  VR REST API        = HTTP API for querying and managing replication config programmatically          │
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
