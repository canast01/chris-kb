# InsightIQ — How It Works

InsightIQ is Dell EMC's performance analytics platform for NetApp PowerScale (Isilon) clusters, deployed as an on-premises virtual appliance. It collects, stores, and presents historical performance data for capacity planning, protocol analysis, and workload trending. A single InsightIQ instance can monitor multiple PowerScale clusters.

---

## Deployment Architecture

```mermaid
graph TB
  PS["PowerScale Cluster\n(OneFS API)"] -->|"performance telemetry"| IIQ["InsightIQ Server\n(analytics VM)"]
  IIQ --> PERF["Performance Dashboards\nIOPS · Throughput · Latency"]
  IIQ --> CAP["Capacity Trending\n& Protocol Breakdown"]
  IIQ --> REP["Scheduled Reports\nPDF / CSV export"]
  ADMIN(["Storage Admin"]) -->|"browser"| IIQ
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PS ctrl
  class IIQ,PERF,CAP,REP cloud
  class ADMIN host
```

---

## Component Roles

| Component | Details |
|---|---|
| Deployment | OVA (VMware) or Linux installer on dedicated VM |
| Database | PostgreSQL (local to appliance — stores all collected metrics) |
| Data Collection | OneFS InsightIQ data connector (REST API pull from cluster management IP) |
| Presentation | Web dashboard (HTTP/HTTPS) |
| Multi-cluster | Yes — multiple clusters per instance; no per-cluster licensing constraints |

---

## Data Collection

- **Collection interval**: configurable; default is 30-second samples aggregated to 5-minute buckets
- **Protocol**: HTTPS REST API to OneFS management IP (port 8080)
- **Metrics collected**: total throughput, per-protocol throughput (NFS/SMB/HTTP), CPU utilisation, disk I/O, node-level metrics, client IP activity
- **Authentication**: dedicated read-only OneFS service account (`svc-insightiq`)

---

## Storage and Retention

InsightIQ stores all metrics in a local PostgreSQL database. Retention period is configured per cluster connection.

| Retention Period | Estimated Disk Usage (5 nodes) |
|---|---|
| 30 days | ~20 GB |
| 90 days (standard) | ~60 GB |
| 180 days | ~120 GB |
| 365 days | ~240 GB |

Standard retention policy: **90 days high-resolution**. Extending retention requires additional disk capacity on the InsightIQ VM.

---

## Sizing Guidelines

| Parameter | Minimum | Recommended |
|---|---|---|
| vCPU | 2 | 4 |
| RAM | 4 GB | 8 GB |
| Disk (OS + application) | 40 GB | 80 GB |
| Disk (data volume) | 200 GB / 5 clusters | 400 GB / 5 clusters |

Allocate a separate VMDK for the PostgreSQL data directory to simplify capacity management.

---

## Network Requirements

| Source | Destination | Port | Purpose |
|---|---|---|---|
| InsightIQ appliance | OneFS cluster management IP | TCP 8080 | Performance data collection |
| Browser | InsightIQ appliance | TCP 80 / 443 | Web dashboard access |
| InsightIQ appliance | SMTP relay | TCP 25 / 587 | Alert email delivery |
| InsightIQ appliance | Syslog / SIEM | UDP/TCP 514 | Appliance event forwarding |

---

## High Availability

InsightIQ does not have native HA. Protect the appliance with:

- Regular `pg_dump` database backups (automated daily cron job)
- VM-level snapshots before upgrades
- VM backup via vCenter backup agent to DR location

---

## Supported OneFS Versions

InsightIQ version compatibility with OneFS must be validated using the NetApp Interoperability Matrix Tool (IMT) before any OneFS upgrade. For OneFS 9.5+, consider whether native OneFS performance views may supplement InsightIQ for simpler use cases.
