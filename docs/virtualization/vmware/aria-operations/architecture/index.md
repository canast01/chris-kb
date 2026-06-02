# Aria Operations — Architecture

<div class="kb-summary">
Analytics cluster for vSphere performance, capacity, and compliance monitoring. Adapters collect metrics from vCenter, NSX, and storage; remote collectors extend reach into remote sites and DMZs without direct cluster connectivity.
</div>

```text
┌─────────────────────────────────── Aria Operations — Architecture ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Aria Operations (formerly vROps) — analytics cluster: primary + replica + data nodes per site │   │
│   │   Remote collectors deployed per site collect metrics without exposing firewall paths to the  │   │
│   │    Adapter instances per integration: vSphere, NSX-T, storage, ServiceNow, SIEM, email/SNMP   │   │
│   │  Dashboards and alerts surface health, risk, efficiency badges across vSphere, NSX, storage,  │   │
│   │  Capacity management and optimization actions right-size VMs and forecast resource exhaustion │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines the cluster internals · integrations connect adapters                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │      Analytics cluster      │  │       vSphere adapter       │  │     Cluster L/XL sizing     │   │
│   │      Remote collectors      │  │        NSX-T adapter        │  │       Remote coll/site      │   │
│   │      Adapter instances      │  │       Storage adapters      │  │      Adapter config std     │   │
│   │       Collector groups      │  │       ServiceNow ITSM       │  │       Data retain 6 mo      │   │
│   │      Dashboards+alerts      │  │          SIEM/Kafka         │  │         Alert policy        │   │
│   │        Capacity mgmt        │  │       Email/SNMP alert      │  │       Custom dash std       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    How-it-works covers cluster nodes · integrations connect adapters and ITSM                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   How It Works   │   Integrations   │    Design Stds    │    Deployment    │     Key Stds     │   │
│   │Analytics cluster │ vSphere adapter  │   Cluster sizing  │   Single node    │   Alert policy   │   │
│   │Remote collectors │  NSX-T adapter   │    Remote coll    │  Small cluster   │  Dashboard std   │   │
│   │Adapter instances │ Storage adapters │   Data retention  │    HA cluster    │   Naming conv    │   │
│   │ Collector groups │ ServiceNow intg  │  Custom policies  │   Multi-cloud    │     RBAC std     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (cluster nodes + remote collectors) · RAM DIMMs · Network NICs · vCenter/cloud targets       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Analytics cluster  = Primary + replica + data nodes forming the Aria Ops processing engine           │
│  Primary node       = Cluster leader; hosts the UI, API, and coordinates analytics workload           │
│  Replica node       = Standby for primary; takes over if primary fails; participates in analytics     │
│  Data node          = Additional analytics capacity node; scales metric ingestion and retention       │
│  Remote collector   = Lightweight VM per site; collects adapter data and forwards to cluster          │
│  Adapter instance   = Configured connection to a monitored product: vSphere, NSX, storage, cloud      │
│  Collector group    = Named group of remote collectors assigned to adapter instances for load sharing │
│  Dashboard          = Customizable view of metrics, badges, and alerts for a resource group           │
│  Alert definition   = Rule triggering notification when a metric crosses a threshold or symptom fires │
│  Capacity analytics = Forecasting engine projecting resource exhaustion based on trend analysis       │
│  Optimization action = Recommended change (right-size, power off, migrate) to improve efficiency      │
│  Badge              = Health/risk/efficiency score (0-100) summarising object state at a glance       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with vCenter, NSX, storage, and external monitoring tools.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, adapter configuration, and cluster design best practices.</span></a>
</div>

## Aria Operations Cluster Architecture

![Aria Operations Cluster Architecture](../../../../assets/aria-operations-architecture-overview.svg)

## Node Roles

| Node Role | Description |
|---|---|
| Primary | Hosts the UI, analytics controller, and cluster coordination |
| Primary Replica | Hot standby — automatically promoted if Primary fails |
| Data | Scale-out metric ingestion and storage nodes |
| Remote Collector | Lightweight proxy for remote sites/DMZs; forwards to cluster without joining it |
| Cloud Proxy | SaaS-hosted proxy for VMware Cloud on AWS integrations |

