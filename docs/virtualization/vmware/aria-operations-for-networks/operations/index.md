---
tags:
  - aria-networks
  - operations
  - vmware
---
# Aria Ops for Networks — Operations

<div class="kb-summary">
Aria Ops for Networks daily operations — data source management, flow analysis, path visibility, and alert configuration.

*Applies to: Aria Networks 6.x*
</div>

```text
┌───────────────────────────────────── Aria Networks — Operations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Network intent checks for policy compliance; flow analysis queries for traffic patterns per  │   │
│   │Path trace for troubleshooting connectivity issues between any two endpoints in the environment│   │
│   │     Alert review for topology changes; security group auditing for microsegmentation drift    │   │
│   │  Lifecycle: vRNI upgrades via Platform UI; upgrade Platform first then Collector VMs at each  │   │
│   │    Automation: REST API for path trace, flow query, alert management, and scheduled report    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops verify network intent · lifecycle keeps platform current                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │        Intent checks        │  │        vRNI upgrades        │  │        vRNI REST API        │   │
│   │         Alert review        │  │      Platform+coll upg      │  │        Path trace API       │   │
│   │        Flow analysis        │  │       Data src re-auth      │  │        Flow query API       │   │
│   │        Sec grp audit        │  │         SNMP compat         │  │          Alert API          │   │
│   │          Path trace         │  │          Cert renew         │  │          Report API         │   │
│   │       Dashboard review      │  │        Config backup        │  │          Python SDK         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch policy drift · lifecycle upgrades Platform before Collectors                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  REST API calls  │   Platform: ok   │    Intent check   │   Upgrade plat   │  Config export   │   │
│   │  Flow query API  │  Collectors: up  │     Path trace    │   Coll upgrade   │  API config bk   │   │
│   │    Alert API     │  Data srcs: ok   │   Sec grp audit   │  Data src auth   │  Restore config  │   │
│   │    Python SDK    │   Alerts: none   │    Flow report    │   Post-upg val   │   Log archive    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · NSX/vCenter/Physical switches           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Network intent    = Defined policy for how traffic should flow between workloads; verified against   │
│  Path trace        = On-demand trace of the actual network path between two endpoints in the          │
│  Flow analysis     = Query of historical flow data to identify communication patterns and anomalies   │
│  Security group audit = Comparison of current security group membership against expected baseline     │
│  Data source       = Configured NSX/vCenter/switch/cloud connection; requires re-auth after cred      │
│  Collector health  = Status of each site Collector VM; must show connected and collecting for valid   │
│  REST API          = Aria Networks REST API; supports path trace, flow query, alert, and report       │
│  Platform upgrade  = Upgrade Platform VM first using built-in UI wizard before upgrading any          │
│  Collector upgrade = Per-site upgrade of Collector VMs after Platform VM upgrade is validated         │
│  SNMP v3           = SNMPv3 credentials for physical switch collection; compat check needed at upgrade│
│  VPC flow logs     = Cloud provider flow logs from AWS/Azure ingested for hybrid network visibility   │
│  Alert threshold   = Configurable metric limit that triggers an Aria Networks alert for topology      │
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

