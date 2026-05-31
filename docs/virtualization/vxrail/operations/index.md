# VxRail Operations

VxRail operations notes for daily checks, maintenance windows, node work, expansion, support cases, and post-change validation.
```text
┌───────────────────────────────────────── VxRail — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Daily VxRail cluster operations: health checks via VxRail plugin and iDRAC          │   │
│   │        Maintenance window procedures; node maintenance mode workflow and DRS evacuation       │   │
│   │        Cluster expansion node addition; support case preparation with bundle generation       │   │
│   │            Post-change validation; LCM failure triage; pre-upgrade readiness checks           │   │
│   │       Change management log; alert review from OMIVV, SupportAssist, and vCenter alarms       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch cluster issues · maintenance keeps nodes updated · cluster mgmt handles expansion  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │         Maintenance         │  │         Cluster Mgmt        │   │
│   │         Daily checks        │  │         Maint window        │  │        Cluster expand       │   │
│   │        VxRail plugin        │  │       Node maint mode       │  │        Node add guide       │   │
│   │         iDRAC alarms        │  │        Pre-maint chk        │  │          Rebalance          │   │
│   │         vSAN resync         │  │        Change window        │  │         Support case        │   │
│   │         Node health         │  │       Post-change val       │  │       LCM fail triage       │   │
│   │         Alert review        │  │          Change log         │  │        Pre-upg checks       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops surface issues early · maintenance follows change process                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Daily Chks    │   Maint Window   │     Node Maint    │  Cluster Expnd   │   Support Case   │   │
│   │  VxRail plugin   │  Pre-maint chk   │     Maint mode    │  Add node guide  │    Bundle gen    │   │
│   │   iDRAC alarms   │  Change window   │    DRS evacuate   │    Rebalance     │   Log collect    │   │
│   │  vSAN resync=0   │   Work perform   │    FW+ESXi upg    │   vSAN expand    │  SupportAssist   │   │
│   │  ESXi connected  │  Post-chng val   │     Exit maint    │  Cluster health  │    GSS portal    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC OOB · 25GbE NICs · ToR switches                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VxRail plugin     = vCenter plugin aggregating cluster health from VxRail Manager into a single view │
│  Maintenance mode  = ESXi state evacuating VMs via DRS before node-level maintenance or upgrade       │
│  DRS evacuation    = DRS migrates all VMs off a host via vMotion before maintenance mode is entered   │
│  Cluster expansion = Adding new VxRail nodes to an existing cluster via guided VxRail Manager workflow│
│  Post-change val   = Checks vSAN health, ESXi connectivity, iDRAC status, and alarms after any change │
│  Support bundle    = Log archive generated by VxRail Manager for Dell GSS case submission             │
│  SupportAssist     = Dell proactive support service; opens cases automatically on hardware fault      │
│  LCM failure triage = Investigating why an LCM upgrade stalled; review LCM logs and pre-check output  │
│  Pre-upgrade check = Health and readiness validation run before initiating an LCM upgrade job         │
│  Change management = Formal process for scheduling, approving, and documenting cluster changes        │
│  iDRAC             = Integrated Dell Remote Access Controller; hardware health and OOB access         │
│  Node-by-node      = LCM upgrade pattern: maintenance → upgrade → validate → next node in sequence    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-5">

<a class="kb-card" href="daily-checks/">
  <strong>Daily Checks</strong>
  <span>Daily VxRail cluster checks across VxRail Manager, vCenter, ESXi, vSAN, and hardware.</span>
</a>

<a class="kb-card" href="maintenance-window/">
  <strong>Maintenance Window</strong>
  <span>Preparation, execution, validation, and communication during VxRail maintenance.</span>
</a>

<a class="kb-card" href="node-maintenance/">
  <strong>Node Maintenance</strong>
  <span>Node-level maintenance planning, evacuation, validation, and return to service.</span>
</a>

<a class="kb-card" href="cluster-expansion/">
  <strong>Cluster Expansion</strong>
  <span>Node add planning, compatibility, network checks, and validation.</span>
</a>

<a class="kb-card" href="support-case-prep/">
  <strong>Support Case Prep</strong>
  <span>Evidence, timeline, logs, screenshots, and clear issue summary for Dell support.</span>
</a>

<a class="kb-card" href="post-change-validation/">
  <strong>Post-Change Validation</strong>
  <span>Validation after lifecycle, hardware, configuration, or support changes.</span>
</a>

<a class="kb-card" href="lcm-failure-triage/">
  <strong>LCM Failure Triage</strong>
  <span>Diagnose stuck or failed VxRail LCM upgrades — bundle validation, component errors, and remediation steps.</span>
</a>

<a class="kb-card" href="node-health-review/">
  <strong>Node Health Review</strong>
  <span>Per-node health review covering hardware alerts, disk groups, network state, and iDRAC status.</span>
</a>

<a class="kb-card" href="pre-upgrade-checks/">
  <strong>Pre-Upgrade Checks</strong>
  <span>Pre-upgrade readiness checks for VxRail — compatibility, cluster health, free capacity, and snapshot state.</span>
</a>
</div>
