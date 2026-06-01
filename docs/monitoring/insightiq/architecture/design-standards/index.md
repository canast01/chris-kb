# InsightIQ — Design Standards

<div class="kb-summary">
VM sizing, data retention policy, network access requirements, naming conventions, and configuration baselines for InsightIQ deployments.
</div>

```
┌──────────────────────────────────── InsightIQ — Design Standards ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Deployment Standards             │  │             Collection Standards            │   │
│   │            Dedicated VM per site             │  │           30-sec interval default           │   │
│   │             200 GB disk minimum              │  │              All clusters added             │   │
│   │             SSD-backed datastore             │  │             Client stats enabled            │   │
│   │            Backup config nightly             │  │             PAPI read-only user             │   │
│   │             2-year retention min             │  │                 TLS for PAPI                │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM on management cluster · SSD datastore · TCP 8080/443 to PowerScale                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Dedicated VM = InsightIQ on separate VM from monitored workloads                                     │
│  SSD datastore = Flash storage for PostgreSQL write performance at 30-sec intervals                   │
│  Client stats = isi_clientstats enabled on PowerScale; required for per-client breakdown              │
│  PAPI read-only = Minimum-privilege user; cannot modify cluster configuration                         │
│  TLS for PAPI = HTTPS connection to PAPI; verify certificate or accept self-signed                    │
│  2-year retention = Minimum raw data retention for trend analysis and compliance                      │
│  Backup config = InsightIQ appliance backup includes config and DB; NFS or SCP target                 │
│  200 GB minimum = Disk allocation for ~5 clusters at 30-sec interval over 2 years                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## VM Sizing

| Parameter | Minimum | Recommended (production) |
|---|---|---|
| vCPU | 4 | 8 |
| RAM | 8 GB | 16 GB |
| OS disk | 100 GB | 100 GB |
| Data disk | 500 GB | 1–2 TB (per retention requirements) |

Data disk sizing: approximately 10 GB per monitored node per month of retention. A 4-node cluster at 12-month retention requires ~480 GB.

## Retention Policy

| Data Granularity | Default Retention | Recommended |
|---|---|---|
| 5-second samples | 14 days | 14 days |
| 30-second rollup | 3 months | 6 months |
| 5-minute rollup | 12 months | 24 months |

- Do not extend fine-grained retention beyond 30 days — disk growth is significant
- Increase 5-minute rollup retention for capacity trending purposes

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| InsightIQ VM | `insightiq-{site}-{seq}` | `insightiq-dc1-01` |
| Monitored cluster display name | Match OneFS cluster name exactly | `ps-cluster-prod-01` |

## Network Requirements

| Source | Destination | Protocol | Port | Purpose |
|---|---|---|---|---|
| InsightIQ VM | PowerScale mgmt IP | HTTPS | 8080 | OneFS REST API (data collection) |
| InsightIQ VM | PowerScale mgmt IP | HTTPS | 443 | OneFS REST API (newer OneFS versions) |
| Admin workstation | InsightIQ VM | HTTPS | 443 | Web dashboard access |
| InsightIQ VM | SMTP relay | SMTP | 25 / 587 | Alert email delivery |

## Configuration Checklist

- [ ] InsightIQ OVA deployed on management cluster
- [ ] Static IP assigned; hostname resolves in DNS
- [ ] Service account created on each PowerScale cluster (read-only, audit role)
- [ ] Each PowerScale cluster added to InsightIQ with service account credentials
- [ ] Data collection status green for all clusters
- [ ] Retention policy configured per standards above
- [ ] Email notification configured for capacity threshold alerts
- [ ] Backup: VM snapshot or file-level backup of data disk, daily
