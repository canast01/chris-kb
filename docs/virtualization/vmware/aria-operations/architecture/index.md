---
tags:
  - architecture
  - aria-operations
  - vmware
---
# Aria Operations — Architecture

<div class="kb-summary">
Analytics cluster for vSphere performance, capacity, and compliance monitoring. Adapters collect metrics from vCenter, NSX, and storage; remote collectors extend reach into remote sites and DMZs without direct cluster connectivity.

*Applies to: Aria Operations 8.x*
</div>

```text
┌────────────────────────── Aria Operations Architecture — Analytics Cluster ───────────────────────────┐
│                                                                                                       │
│  Analytics cluster for vSphere performance, capacity, and compliance; adapters                        │
│  collect metrics from vCenter/NSX/storage; remote collectors extend reach.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Cluster Architecture             │  │               Data Collection               │   │
│   │           Primary + replica nodes            │  │         vCenter adapter: 5 min poll         │   │
│   │          Data nodes: metric storage          │  │         NSX adapter: topology + perf        │   │
│   │           Witness node: HA quorum            │  │       Storage adapters: array metrics       │   │
│   │          HBase: time-series storage          │  │       Remote collector: DMZ/WAN reach       │   │
│   │         Cassandra: config + metadata         │  │         SDDC Health: self-monitoring        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Remote collectors send data to cluster without requiring cluster to reach targets.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Analytics and Alerting            │  │           Capacity and Compliance           │   │
│   │         Workload Optimization: DRS+          │  │          Capacity: runway forecast          │   │
│   │        What-if: cluster sizing model         │  │          Reclaim: idle VM detection         │   │
│   │       Alert: symptom + recommendation        │  │         Compliance: benchmark packs         │   │
│   │          Custom dashboard: widgets           │  │          Pricing: cost per VM model         │   │
│   │          Reports: scheduled PDF/CSV          │  │        Predictive DRS: sends forecast       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Linux VMs (Photon OS) for each node; shared NFS for backups; cluster needs                           │
│  connectivity to all vCenter instances and adapters on TCP 443.                                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Primary node    = master node; UI + API + orchestration                                              │
│  Data node       = stores time-series metrics in HBase                                                │
│  Remote collector= separate VM; collects from isolated networks                                       │
│  Adapter         = plugin connecting Aria Ops to a data source                                        │
│  HBase           = distributed time-series store; metric retention                                    │
│  Cassandra       = config and relationship metadata store                                             │
│  Symptom         = threshold crossing or anomaly on a metric                                          │
│  Alert           = grouped symptoms with recommendation and action                                    │
│  Workload Opt    = automated vMotion recommendations via DRS integration                              │
│  Capacity runway = days until resource exhaustion at current growth rate                              │
│  Predictive DRS  = sends 60-min demand forecast to vCenter DRS                                        │
│  Compliance pack = benchmark rules; CIS, vSphere Security Hardening Guide                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Aria Operations Cluster Architecture](../../../../assets/aria-operations-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with vCenter, NSX, storage, and external monitoring tools.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, adapter configuration, and cluster design best practices.</span></a>
</div>

## Node Roles

| Node Role | Description |
|---|---|
| Primary | Hosts the UI, analytics controller, and cluster coordination |
| Primary Replica | Hot standby — automatically promoted if Primary fails |
| Data | Scale-out metric ingestion and storage nodes |
| Remote Collector | Lightweight proxy for remote sites/DMZs; forwards to cluster without joining it |
| Cloud Proxy | SaaS-hosted proxy for VMware Cloud on AWS integrations |

## Deployment Sizing

| Deployment Size | Nodes | Use Case |
|---|---|---|
| Small (xSmall) | 1 node | Lab / proof-of-concept |
| Medium | Primary + Replica | Up to ~3,000 VMs |
| Large | Primary + Replica + 2–4 Data Nodes | Up to ~10,000 VMs |
| Extra Large | Primary + Replica + 4+ Data Nodes | Enterprise fleet |

---

## Analytics Cluster Topology
