# InsightIQ — How It Works

```
┌────────────────────────────────────── InsightIQ — How It Works ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Step 1: Cluster Registration — add PowerScale cluster IP and PAPI credentials to InsightIQ  │   │
│   │    Step 2: Collection — InsightIQ polls PAPI every 30 seconds for all performance counters    │   │
│   │   Step 3: Storage — raw samples stored in PostgreSQL; older data rolled up to 5-min averages  │   │
│   │           Step 4: Analysis — UI queries DB to render dashboards and charts on demand          │   │
│   │         Step 5: Reporting — user builds or schedules reports; PDF/CSV export available        │   │
│   │     Step 6: Alert — threshold breach triggers email notification to configured recipients     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM on management cluster · PAPI from VM to cluster SmartConnect IP                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cluster registration = Adding cluster access zone IP and PAPI user to InsightIQ                      │
│  SmartConnect = PowerScale DNS load-balancing for PAPI connections across nodes                       │
│  PAPI credentials = Read-only admin user on PowerScale; InsightIQ uses for all polls                  │
│  Raw sample = 30-second metric reading stored at full resolution                                      │
│  Rollup = Aggregation process compressing old raw samples into hourly averages                        │
│  Dashboard = Pre-built or custom view of metrics over selected time range                             │
│  Report = Scheduled or on-demand document with metric tables and charts                               │
│  Threshold alert = Email sent when metric exceeds configured limit                                    │
│  SmartConnect zone = PowerScale DNS name resolving to available node IPs                              │
│  PostgreSQL = On-appliance DB; grows at ~10 GB/year per cluster at 30-sec interval                    │
│  PDF export = Formatted report for management sharing                                                 │
│  CSV export = Raw data download for spreadsheet or BI analysis                                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
InsightIQ is Dell EMC's performance analytics platform for NetApp PowerScale (Isilon) clusters, deployed as an on-premises virtual appliance. It collects, stores, and presents historical performance data for capacity planning, protocol analysis, and workload trending. A single InsightIQ instance can monitor multiple PowerScale clusters.

---

## Deployment Architecture



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
