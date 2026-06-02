# Aria Operations (Monitoring)

<div class="kb-summary">
VMware Aria Operations monitoring platform — architecture, health checks, capacity, alerting, dashboards, and operational runbooks.
</div>

```
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
