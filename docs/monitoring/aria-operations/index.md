# Aria Operations (Monitoring)

<div class="kb-summary">
VMware Aria Operations monitoring platform — architecture, health checks, capacity, alerting, dashboards, and operational runbooks.
</div>

```text
┌───────────────────────────────── Aria Operations — Platform Overview ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          VMware Aria Operations (vROps) — Analytics-Driven Infrastructure Monitoring          │   │
│   │        Architecture: Master node + Replica node + Collector nodes (data nodes optional)       │   │
│   │        Data sources: vCenter · NSX · vSAN · Storage adapters (Unity, PowerStore, ONTAP)       │   │
│   │       Key features: capacity forecasting · anomaly detection · compliance · workload opt      │   │
│   │             Access: HTTPS/443 · REST API · vracli · vami_config · vRSLCM lifecycle            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Aria Ops is the primary on-prem analytics tool for all vSphere, NSX, and vSAN workloads            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │         Integrations        │   │
│   │         Master node         │  │       Alert management      │  │       vCenter adapter       │   │
│   │         Replica node        │  │      Capacity planning      │  │         NSX adapter         │   │
│   │      Collector node(s)      │  │          Dashboards         │  │       Storage adapters      │   │
│   │       Data node (opt)       │  │       Compliance packs      │  │      ServiceNow plugin      │   │
│   │        REST API :443        │  │      Workload optimise      │  │      Log Insight plugin     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Aria Ops cluster: 3+ VMs on vSphere · Minimum 4 vCPU/16 GB per node · vPostgres embedded DB          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master node       = Primary analytics node; hosts UI, REST API, and orchestration services           │
│  Replica node      = Hot standby for master; promotes automatically on master failure                 │
│  Collector node    = Remote data collector; deployed near data sources to reduce WAN load             │
│  Data node         = Additional analytics/storage node; added for large-scale environments            │
│  Adapter           = Plugin connecting Aria Ops to a data source (vCenter, NSX, storage, etc.)        │
│  Compliance pack   = Pre-built policy set (e.g. CIS, DISA STIG) for configuration compliance          │
│  Capacity forecast = ML projection of when a resource reaches its configured threshold                │
│  Workload optimize = Aria Ops recommendation to rebalance VMs across hosts for efficiency             │
│  vracli            = Command-line interface for Aria Ops cluster administration                       │
│  vami_config       = VAMI-based configuration CLI for network and services on Aria Ops appliance      │
│  vRSLCM            = vRealize Suite Lifecycle Manager; deploys and upgrades Aria Ops                  │
│  REST API          = HTTPS API on port 443; used for alert queries, object inventory, reports         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
┌──────────────────────────────── Aria Operations — Deployment Sequence ────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  vCenter service account: read-only + deploy VM + push metrics permission                             │
│  Sizing: primary node 8 vCPU / 32 GB RAM / 512 GB disk (scale to cluster for >500 VMs)                │
│  DNS A+PTR records for all Aria Ops nodes  ·  NTP sources reachable  ·  NTP synced                    │
│  Ports: 443 (HTTPS UI)  ·  443 (adapter to vCenter)  ·  514/udp (syslog in)                           │
│  Licence key for Aria Operations Advanced or Enterprise from Customer Connect                         │
│                                                                                                       │
│                                        │  deploy primary node OVA                                     │
│                                        ▼                                                              │
│  Step 2 · Primary Node                                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Aria Operations OVA to vCenter  ·  set IP, gateway, DNS, NTP during deployment                │
│  Power on  ·  open https://<node-ip>  ·  run initial setup wizard                                     │
│  Set admin password  ·  accept EULA  ·  activate licence (paste licence key)                          │
│  Wait for primary node to reach Running state  ·  takes 15–20 minutes on first boot                   │
│  Verify: Admin → Cluster Management  ·  primary node shows Online + Running                           │
│                                                                                                       │
│                                        │  add replica and data nodes                                  │
│                                        ▼                                                              │
│  Step 3 · Replica & Data Nodes                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy additional OVAs for replica nodes (minimum 2 for HA cluster)                                  │
│  During OVA deployment: set role to Data and set primary node IP as master                            │
│  Nodes auto-register  ·  Admin → Cluster Management shows all nodes joining                           │
│  Expand cluster to add analytics nodes for larger deployments (>1000 VMs)                             │
│  Verify all nodes Online  ·  cluster quorum established  ·  metrics processing active                 │
│                                                                                                       │
│                                        │  deploy remote collectors                                    │
│                                        ▼                                                              │
│  Step 4 · Remote Collectors                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Remote Collector OVA at each remote site or DMZ segment                                       │
│  During deploy: set role to Remote Collector  ·  set primary node FQDN + shared key                   │
│  RC registers to primary  ·  Admin → Remote Collectors shows RC Online                                │
│  Assign data sources to RC to route collection through local collector (reduces WAN)                  │
│  Verify RC health  ·  confirm data flowing from remote vCenter through RC                             │
│                                                                                                       │
│                                        │  add data sources and adapters                               │
│                                        ▼                                                              │
│  Step 5 · Adapters & Data Sources                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add vCenter adapter: Data Sources → Add → VMware vSphere  ·  enter vCenter FQDN + creds              │
│  Add NSX-T adapter  ·  vSAN adapter  ·  storage adapters (PowerStore, Pure, NetApp)                   │
│  Management packs: install from Marketplace for non-vSphere targets (AWS, Azure, SQL)                 │
│  Verify adapter collection status  ·  all adapters should show Collecting                             │
│  Allow 30 minutes for initial inventory walk  ·  verify VMs and hosts appear in dashboard             │
│                                                                                                       │
│                                        │  configure alerts and dashboards                             │
│                                        ▼                                                              │
│  Step 6 · Alerts & Dashboards                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Import management pack content  ·  activate relevant alert definitions per environment               │
│  Configure notification plugins: SMTP  ·  ServiceNow  ·  Slack  ·  PagerDuty webhook                  │
│  Tune noisy alerts: suppress known environment deviations  ·  set alert criticality                   │
│  Create custom dashboards for: vSAN health, cluster capacity, VM rightsizing                          │
│  Enable Continuous Availability (CA) if dual-site deployment  ·  configure witness node               │
│  Baseline: document capacity headroom and first rightsizing recommendations                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>Deployment topology, cluster sizing, adapter configuration, and vCenter integration.</span></a>
<a class="kb-card" href="design-standards/"><strong>Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>VMware, backup tools, monitoring, authentication, and API integration.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
<a class="kb-card" href="alerts/"><strong>Alerts</strong><span>Alert configuration, thresholds, and notification setup.</span></a>
<a class="kb-card" href="capacity/"><strong>Capacity</strong><span>Capacity planning, forecasting, and thresholds.</span></a>
<a class="kb-card" href="dashboards/"><strong>Dashboards</strong><span>Dashboard setup, views, and key metrics.</span></a>
<a class="kb-card" href="reports/"><strong>Reports</strong><span>Capacity trend reports, SLA summary export, scheduled delivery, and data archiving.</span></a>
</div>
