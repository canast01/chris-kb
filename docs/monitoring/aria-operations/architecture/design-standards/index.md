# Aria Operations — Design Standards

<div class="kb-summary">
Cluster sizing, Management Pack governance, alert configuration baselines, naming conventions, and configuration standards for Aria Operations deployments.
</div>

## Cluster Sizing Standards

| Environment | Topology | Rationale |
|---|---|---|
| Lab / PoC | 1-node xSmall | No HA; dev/test only |
| Production ≤ 3,000 VMs | Primary + Replica | Standard HA pair |
| Production ≤ 10,000 VMs | Primary + Replica + 2–4 Data Nodes | Scale-out for metric volume |
| Enterprise fleet > 10,000 VMs | Primary + Replica + 4+ Data Nodes | Maximum scale |

- Always deploy an even number of Data Nodes (analytics partitioning)
- Remote Collectors required for any site > 100ms RTT from the analytics cluster
- Dedicate at least one Remote Collector per site; do not co-locate with the cluster nodes

## VM Sizing

| Node Role | vCPU | RAM | Disk |
|---|---|---|---|
| Primary / Replica (Medium) | 8 | 32 GB | 1 TB |
| Primary / Replica (Large) | 16 | 48 GB | 2 TB |
| Data Node | 8 | 32 GB | 2 TB |
| Remote Collector | 4 | 16 GB | 100 GB |

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Analytics cluster node | `ariaops-{role}-{site}-{seq}` | `ariaops-primary-dc1-01` |
| Remote Collector | `ariaops-rc-{site}-{seq}` | `ariaops-rc-dc2-01` |
| Management Pack | Match vendor name exactly | `VMware NSX-T Management Pack` |
| Alert definition | `{Severity} - {Object type} - {Condition}` | `Critical - VM - CPU Contention > 90%` |

## Alert Configuration Baseline

| Alert Tier | Notification Target | SLA |
|---|---|---|
| Critical | PagerDuty / on-call runbook | Immediate |
| Warning | Email distribution list | 4-hour acknowledgement |
| Info | Dashboard only | No notification |

- Suppress alert storms during maintenance windows using Maintenance Mode on affected objects
- Set `Alert Expiry` to 7 days for warning-level alerts; 30 days for info
- Enable `Auto-Cancel` only for alerts with self-healing remediation

## Management Pack Standards

- Install Management Packs only from the VMware Marketplace or vendor-official sources
- Validate MP version compatibility with the Aria Operations release before upgrade
- Restrict MP installation to the `ariaops-admin` service account — not personal accounts
- Document all installed MPs in the CMDB with version and owning team
- Review unused MPs quarterly and remove if no active dashboards or alerts depend on them

## Configuration Checklist

- [ ] NTP configured on all nodes (source: site NTP server, not ESXi host)
- [ ] SMTP relay configured and tested (send test alert)
- [ ] LDAP / AD authentication configured; local admin account documented in CyberArk
- [ ] Remote Collectors registered and health-green in the cluster inventory
- [ ] vCenter adapter added and collection status healthy
- [ ] Retention policy set per org standard (default: 6 months for fine-grained, 12 months for rollup)
- [ ] Backup job scheduled (snapshot or file-level of the VM, daily)
