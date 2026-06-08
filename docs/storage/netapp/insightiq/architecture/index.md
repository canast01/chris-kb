# InsightIQ — Architecture

<div class="kb-summary">
InsightIQ is an on-premises virtual appliance that collects performance telemetry from PowerScale clusters via the OneFS REST API and stores it in a local PostgreSQL database for historical trend analysis and reporting.
</div>

```text
┌────────────────────────────────────── InsightIQ — Architecture ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Architecture: single VM appliance; internal PostgreSQL stores collected metrics        │   │
│   │           Collector: polls PowerScale PAPI every 30 seconds for performance counters          │   │
│   │            UI: embedded web server on port 443 serves dashboards and report builder           │   │
│   │         Data retention: configurable; default 2 years; older data rolled up or purged         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Single appliance polls PAPI; no agent on PowerScale nodes; storage grows ~10 GB/year/cluster       │
│                                                                                                       │
│                                                  ▼                                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Collection                  │  │                   Storage                   │   │
│   │                PAPI TCP 8080                 │  │               PostgreSQL on VM              │   │
│   │               30-sec interval                │  │              ~10 GB/yr/cluster              │   │
│   │              Protocol counters               │  │             Rollup for old data             │   │
│   │               Node-level stats               │  │            Configurable retention           │   │
│   │              Client/share stats              │  │              Backup recommended             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM: 4 vCPU/8 GB/200 GB disk · PowerScale: PAPI user needed on cluster                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PAPI = PowerScale Platform API on TCP 8080; InsightIQ polls this for all counters                    │
│  PAPI user = Read-only cluster admin account created on PowerScale for InsightIQ                      │
│  PostgreSQL = Embedded relational DB storing time-series metrics on InsightIQ VM                      │
│  30-second interval = Default collection cadence; lower for higher resolution (more disk)             │
│  Rollup = Aggregating 30-sec samples into 5-min then 1-hour averages for old data                     │
│  Retention = Configurable data retention period; default 2 years raw + 5 years rolled                 │
│  Protocol counters = NFS v3/v4, SMB, S3, HDFS IO stats per protocol per node                          │
│  Client stats = Per-client-IP IO breakdown; requires clientstats enabled on cluster                   │
│  Share stats = Per-NFS export or SMB share IO statistics                                              │
│  Embedded web = InsightIQ UI served from nginx on TCP 443 on the appliance VM                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![InsightIQ Architecture](../../../../assets/insightiq-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Deployment architecture, data collection, retention sizing, network requirements, and HA.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>PowerScale OneFS integration, SIEM forwarding, and email alerting.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, naming conventions, and configuration baselines.</span></a>
</div>

---

## Component Roles

| Component | Details |
|---|---|
| InsightIQ VM | OVA (VMware) or Linux installer; hosts collection engine and web dashboard |
| PostgreSQL | Local metrics database on the appliance |
| OneFS data connector | REST API pull from cluster management IP (port 8080) |

---

## Deployment Architecture


