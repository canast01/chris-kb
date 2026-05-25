# Aria Ops for Logs — Operations

```text
┌─────────────────────────────────────── Aria Logs — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Alert management and dashboard queries; agent health monitoring across all forwarding hosts  │   │
│   │  Disk usage and retention enforcement: monitor partition fill rate; expand disks proactively  │   │
│   │   Content pack management: import, update, and validate packs for new log source onboarding   │   │
│   │  Forwarder configuration for SIEM integration: filter, tag, and stream log events externally  │   │
│   │   vRLI upgrade sequence: backup config, upgrade nodes in order, validate post-upgrade health  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops review alerts and agents · lifecycle upgrades nodes safely                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │         Alert review        │  │        vRLI upgrades        │  │        vRLI REST API        │   │
│   │       Dashboard query       │  │        Pre-chk backup       │  │      Content pk import      │   │
│   │         Agent health        │  │        Node upg order       │  │       Agent config API      │   │
│   │          Disk usage         │  │        Agent upgrade        │  │          Alert API          │   │
│   │        Source health        │  │      Content pk update      │  │          Query API          │   │
│   │      Content pk status      │  │          Cert renew         │  │        VLQL scripted        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor agents and disk · lifecycle upgrades safely                                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  REST API calls  │  Cluster: green  │     Alert tune    │   Upgrade node   │  Config export   │   │
│   │   VLQL queries   │ Agents: sending  │   Add log source  │   Agent update   │   Content bkp    │   │
│   │    Alert API     │    Disk: <80%    │   Forwarder cfg   │  Content pk upg  │  Restore config  │   │
│   │  Content pk API  │ Sources: active  │   Retention chk   │   Post-upg val   │   Log archive    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (master + workers) · RAM DIMMs · Network NICs · High-capacity log storage · Syslog network   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Content pack       = Pre-built field extractors and dashboards; imported via UI or REST API          │
│  vRLI agent         = Host-based log forwarder; reports sending state visible in admin sources page   │
│  Alert pipeline     = Log-match rule triggering email, webhook, or vROps notification on condition    │
│  VLQL query         = vRLI Query Language statement for filtering, grouping, and charting log events  │
│  Log forwarder      = Cluster feature streaming matched events to SIEM via syslog or REST endpoint    │
│  Disk retention     = Automatic deletion of oldest log partitions when disk reaches configured        │
│  HA cluster upgrade = Sequenced upgrade: master node last; workers upgraded first to preserve         │
│  Source health      = Admin UI view showing per-source event rate and last-received timestamp         │
│  REST API           = vRLI API for querying events, managing alerts, sources, and content packs       │
│  Interactive analytics = VLQL query workspace for ad-hoc investigation with chart and table views     │
│  Log ingestion rate = Events-per-second metric; baseline for disk capacity planning and alerting      │
│  Content pack version = Versioned pack release; update to get new dashboards and field extractors     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────────── Aria Logs — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Alert management and dashboard queries; agent health monitoring across all forwarding hosts  │   │
│   │  Disk usage and retention enforcement: monitor partition fill rate; expand disks proactively  │   │
│   │   Content pack management: import, update, and validate packs for new log source onboarding   │   │
│   │  Forwarder configuration for SIEM integration: filter, tag, and stream log events externally  │   │
│   │   vRLI upgrade sequence: backup config, upgrade nodes in order, validate post-upgrade health  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops review alerts and agents · lifecycle upgrades nodes safely                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │         Alert review        │  │        vRLI upgrades        │  │        vRLI REST API        │   │
│   │       Dashboard query       │  │        Pre-chk backup       │  │      Content pk import      │   │
│   │         Agent health        │  │        Node upg order       │  │       Agent config API      │   │
│   │          Disk usage         │  │        Agent upgrade        │  │          Alert API          │   │
│   │        Source health        │  │      Content pk update      │  │          Query API          │   │
│   │      Content pk status      │  │          Cert renew         │  │        VLQL scripted        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor agents and disk · lifecycle upgrades safely                                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  REST API calls  │  Cluster: green  │     Alert tune    │   Upgrade node   │  Config export   │   │
│   │   VLQL queries   │ Agents: sending  │   Add log source  │   Agent update   │   Content bkp    │   │
│   │    Alert API     │    Disk: <80%    │   Forwarder cfg   │  Content pk upg  │  Restore config  │   │
│   │  Content pk API  │ Sources: active  │   Retention chk   │   Post-upg val   │   Log archive    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (master + workers) · RAM DIMMs · Network NICs · High-capacity log storage · Syslog network   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Content pack       = Pre-built field extractors and dashboards; imported via UI or REST API          │
│  vRLI agent         = Host-based log forwarder; reports sending state visible in admin sources page   │
│  Alert pipeline     = Log-match rule triggering email, webhook, or vROps notification on condition    │
│  VLQL query         = vRLI Query Language statement for filtering, grouping, and charting log events  │
│  Log forwarder      = Cluster feature streaming matched events to SIEM via syslog or REST endpoint    │
│  Disk retention     = Automatic deletion of oldest log partitions when disk reaches configured        │
│  HA cluster upgrade = Sequenced upgrade: master node last; workers upgraded first to preserve         │
│  Source health      = Admin UI view showing per-source event rate and last-received timestamp         │
│  REST API           = vRLI API for querying events, managing alerts, sources, and content packs       │
│  Interactive analytics = VLQL query workspace for ad-hoc investigation with chart and table views     │
│  Log ingestion rate = Events-per-second metric; baseline for disk capacity planning and alerting      │
│  Content pack version = Versioned pack release; update to get new dashboards and field extractors     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────────── Aria Logs — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Alert management and dashboard queries; agent health monitoring across all forwarding hosts  │   │
│   │  Disk usage and retention enforcement: monitor partition fill rate; expand disks proactively  │   │
│   │   Content pack management: import, update, and validate packs for new log source onboarding   │   │
│   │  Forwarder configuration for SIEM integration: filter, tag, and stream log events externally  │   │
│   │   vRLI upgrade sequence: backup config, upgrade nodes in order, validate post-upgrade health  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops review alerts and agents · lifecycle upgrades nodes safely                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │         Alert review        │  │        vRLI upgrades        │  │        vRLI REST API        │   │
│   │       Dashboard query       │  │        Pre-chk backup       │  │      Content pk import      │   │
│   │         Agent health        │  │        Node upg order       │  │       Agent config API      │   │
│   │          Disk usage         │  │        Agent upgrade        │  │          Alert API          │   │
│   │        Source health        │  │      Content pk update      │  │          Query API          │   │
│   │      Content pk status      │  │          Cert renew         │  │        VLQL scripted        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor agents and disk · lifecycle upgrades safely                                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  REST API calls  │  Cluster: green  │     Alert tune    │   Upgrade node   │  Config export   │   │
│   │   VLQL queries   │ Agents: sending  │   Add log source  │   Agent update   │   Content bkp    │   │
│   │    Alert API     │    Disk: <80%    │   Forwarder cfg   │  Content pk upg  │  Restore config  │   │
│   │  Content pk API  │ Sources: active  │   Retention chk   │   Post-upg val   │   Log archive    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (master + workers) · RAM DIMMs · Network NICs · High-capacity log storage · Syslog network   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Content pack       = Pre-built field extractors and dashboards; imported via UI or REST API          │
│  vRLI agent         = Host-based log forwarder; reports sending state visible in admin sources page   │
│  Alert pipeline     = Log-match rule triggering email, webhook, or vROps notification on condition    │
│  VLQL query         = vRLI Query Language statement for filtering, grouping, and charting log events  │
│  Log forwarder      = Cluster feature streaming matched events to SIEM via syslog or REST endpoint    │
│  Disk retention     = Automatic deletion of oldest log partitions when disk reaches configured        │
│  HA cluster upgrade = Sequenced upgrade: master node last; workers upgraded first to preserve         │
│  Source health      = Admin UI view showing per-source event rate and last-received timestamp         │
│  REST API           = vRLI API for querying events, managing alerts, sources, and content packs       │
│  Interactive analytics = VLQL query workspace for ad-hoc investigation with chart and table views     │
│  Log ingestion rate = Events-per-second metric; baseline for disk capacity planning and alerting      │
│  Content pack version = Versioned pack release; update to get new dashboards and field extractors     │
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
