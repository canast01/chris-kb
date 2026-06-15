---
tags:
  - architecture
  - netapp
---
# InsightIQ — Architecture

<div class="kb-summary">
InsightIQ is an on-premises virtual appliance that collects performance telemetry from PowerScale clusters via the OneFS REST API and stores it in a local PostgreSQL database for historical trend analysis and reporting.

*Applies to: InsightIQ*
</div>

```text
┌──────────────────────── NetApp InsightIQ — Performance Analytics Architecture ────────────────────────┐
│                                                                                                       │
│  Performance reporting and analytics application for NetApp clusters; collects                        │
│  metrics via PAPI/REST; generates capacity forecasts and performance trend reports.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Collection Architecture            │  │            Analytics Capabilities           │   │
│   │        Linux VM (separate appliance)         │  │             Capacity forecasting            │   │
│   │          PAPI/REST: cluster metrics          │  │             Performance trending            │   │
│   │         Poll interval: configurable          │  │              Workload analysis              │   │
│   │         Stores: local PostgreSQL DB          │  │          Usage reports: exportable          │   │
│   │         Multi-cluster: one instance          │  │          Chargebacks: by client IP          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  InsightIQ complements ActiveIQ; InsightIQ for on-prem deep-dive, ActiveIQ for health.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Report Types                 │  │                  Management                 │   │
│   │          Capacity: per volume/qtree          │  │            Web UI: browser-based            │   │
│   │          Throughput: MB/s over time          │  │           REST API: report export           │   │
│   │          Latency: ops response time          │  │           Email: scheduled PDF/CSV          │   │
│   │         Protocol: NFS/CIFS breakdown         │  │           Alerts: threshold-based           │   │
│   │           Client: per-IP breakdown           │  │          AD integration: user auth          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Linux VM (4 vCPU, 8 GB RAM, 200+ GB disk); management network access to all                          │
│  monitored clusters on HTTPS; outbound SMTP for email reports.                                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  InsightIQ      = NetApp/Isilon performance and capacity analytics application                        │
│  PAPI           = Platform API; cluster REST interface used for metric collection                     │
│  Capacity forecast= projects date when volume or cluster will reach threshold                         │
│  Performance trending= graphs throughput/latency/IOPS over days, weeks, months                        │
│  Workload analysis= identifies top clients and protocols consuming capacity                           │
│  Chargeback     = report showing per-client or per-group storage consumption                          │
│  PostgreSQL     = local DB inside InsightIQ VM; stores collected metrics                              │
│  ActiveIQ       = NetApp cloud health monitoring; complementary to InsightIQ                          │
│  Poll interval  = how often InsightIQ queries cluster (default: 5 minutes)                            │
│  Protocol breakdown= IOPS split between NFS, CIFS, iSCSI, FCP                                         │
│  Qtree          = ONTAP subdirectory with quota enforcement; InsightIQ tracks per-qtree               │
│  Scheduled report= PDF/CSV delivered by email on daily/weekly/monthly schedule                        │
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

