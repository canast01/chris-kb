# InsightIQ Standards


<div class="kb-summary">
InsightIQ Standards reference covering Appliance Sizing Standards, Data Retention Policy, Cluster Connection Standards, Alert Thresholds, Dashboard Standards and 3 more sections.
</div>

```powershell
┌──────────────────────────────────── InsightIQ — Design Standards ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Platform Design                │  │                Data Standards               │   │
│   │               One VM per site                │  │             2-year min retention            │   │
│   │               200+ GB SSD disk               │  │               Client stats ON               │   │
│   │              All clusters added              │  │              30-sec collection              │   │
│   │             PAPI read-only acct              │  │                Backup nightly               │   │
│   │               Management VLAN                │  │           Report scheduled weekly           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM on management cluster · SSD VMDK · PAPI TCP 8080 to cluster                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  One VM per site = Each data centre site has a dedicated InsightIQ appliance                          │
│  200+ GB SSD = Disk allocation; SSD required for PostgreSQL write performance                         │
│  Client stats = isi_clientstats must be enabled on cluster for per-client breakdown                   │
│  Read-only PAPI account = InsightIQ cannot modify cluster; dedicated account per cluster              │
│  2-year retention = Minimum to support trend analysis and capacity planning                           │
│  Nightly backup = iiq_backup scheduled; archive to NFS before 07:00                                   │
│  Weekly report = Scheduled performance report emailed to storage team every Monday                    │
│  Management VLAN = InsightIQ isolated to management network; no access from users                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Appliance Sizing Standards

InsightIQ appliance sizing is based on the number of monitored clusters and the desired data retention period.

| Deployment Size | Clusters | vCPU | RAM | Data Disk |
|---|---|---|---|---|
| Small | Up to 5 | 2 | 4 GB | 200 GB |
| Medium | 6–15 | 4 | 8 GB | 400 GB |
| Large | 16–30 | 8 | 16 GB | 800 GB |

Add disk capacity for extended retention (approximately 1 GB/day/5-node cluster at default sample rates).

## Data Retention Policy

| Data Type | Retention | Notes |
|---|---|---|
| High-resolution metrics | 90 days | Default; standard for operations |
| Aggregated daily metrics | 365 days | Used for capacity planning and trend reports |

Retention is configured per cluster connection in the InsightIQ web UI: **Administration > Clusters > [Cluster] > Data Retention**.

## Cluster Connection Standards

- All cluster connections must use a dedicated read-only OneFS service account: `svc-insightiq`
- Do not use shared admin credentials or personal accounts
- Service account password rotation: every 12 months; update in InsightIQ immediately after rotation
- Each cluster must have a descriptive display name in InsightIQ using the format: `<site>-pscale-<number>` (e.g., `dc1-pscale-01`)

## Alert Thresholds

| Metric | Warning | Critical |
|---|---|---|
| NFS latency (ms) | 5 | 10 |
| SMB latency (ms) | 5 | 10 |
| HTTP latency (ms) | 20 | 50 |
| Cluster CPU usage | 70% | 85% |
| Disk throughput utilisation | 70% | 85% |
| InsightIQ appliance disk (data volume) | 75% | 85% |

Latency thresholds are environment-specific; adjust for workload type (e.g., media workloads may have higher latency baselines). Document any custom thresholds with rationale.

## Dashboard Standards

| Dashboard | Purpose | Review Frequency |
|---|---|---|
| Cluster Overview | Per-cluster throughput, latency, CPU | Daily |
| Protocol Breakdown | NFS/SMB/HTTP throughput comparison | Weekly |
| Top Clients | Highest-traffic client IPs per cluster | Weekly |
| Capacity Trend | Node and pool usage over time | Weekly |

Dashboards are accessed via the InsightIQ web UI. Share report links or PDF exports for weekly capacity planning meetings.

## Report Schedule

| Report | Schedule | Format | Audience |
|---|---|---|---|
| Weekly Utilisation Report (per cluster) | Weekly, Monday 08:00 | PDF/CSV | Storage team |
| Monthly Capacity Planning Report | Monthly, 1st Monday | PDF | Storage team + management |
| Protocol Throughput Summary | Weekly | PDF | Application teams (on request) |

Reports are generated via **Administration > Reports > Scheduled Reports** and emailed to the configured distribution list.

## Credential Standards

- InsightIQ web UI admin account: use a team service account (`svc-iiq-admin`), not personal accounts
- LDAP integration: preferred over local accounts for auditing and centralised access control
- HTTPS enforced: HTTP access disabled; self-signed certificate replaced with internal CA-signed certificate
- Backup files: encrypted at rest; stored in the team backup storage location

## Change Management

All changes to InsightIQ (cluster additions/removals, threshold changes, software upgrades) must be documented in ServiceNow as standard change records and communicated to the storage ops team.
