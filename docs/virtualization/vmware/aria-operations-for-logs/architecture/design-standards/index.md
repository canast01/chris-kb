# Aria Ops for Logs — Standards

## Naming Convention

Follow the same naming scheme as other LCM-managed appliances:

```
vrli-<env>-<node#>.<domain>
```

| Environment | Master Node | Worker Nodes |
|---|---|---|
| Production | `vrli-prod-01.corp.local` | `vrli-prod-02.corp.local`, `vrli-prod-03.corp.local` |
| DR/Standby | `vrli-dr-01.corp.local` | `vrli-dr-02.corp.local` |
| Development | `vrli-dev-01.corp.local` | — |

---

## Deployment Size Reference

| Size | Nodes | vCPUs (per node) | RAM (per node) | Disk (per node) | Daily Ingestion |
|---|---|---|---|---|---|
| Extra Small | 1 (Master only) | 4 | 8 GB | 200 GB | Up to 20 GB/day |
| Small | 1 (Master only) | 8 | 18 GB | 500 GB | Up to 75 GB/day |
| Medium (HA) | 3 (1 Master + 2 Workers) | 8 | 18 GB | 500 GB | Up to 225 GB/day |
| Large (HA) | 6 (1 Master + 5 Workers) | 8 | 18 GB | 1 TB | Up to 500 GB/day |

For production, deploy a minimum 3-node cluster (1 master + 2 workers) for high availability. The master handles query coordination and the UI; workers provide additional ingestion throughput and storage.

Add worker nodes to scale horizontally — ingestion capacity scales linearly with workers.

---

## Pre-Deployment Checklist

- [ ] DNS A record created for each node FQDN — verify: `nslookup vrli-prod-01.corp.local`
- [ ] DNS PTR record for each node IP — verify: `nslookup <ip>`
- [ ] NTP reachable; time delta < 1 second — verify: `chronyc tracking`
- [ ] Static IPs reserved in IPAM for all nodes
- [ ] Firewall rules permit inbound on ports 514 (UDP), 1514 (TCP), 9543 (TCP), 443 (TCP)
- [ ] Sufficient disk space: minimum 500 GB per node for standard production retention (30 days)
- [ ] CA certificate chain ready for import (leaf + intermediate + root)
- [ ] SMTP relay accessible for alert notifications
- [ ] vCenter credentials available for the vSphere content pack configuration

---

## Log Retention Standards

| Data Tier | Retention | Storage |
|---|---|---|
| Hot (searchable, interactive analytics) | 30 days (default) | Local node disk |
| Warm (archived, not in real-time search) | 90–365 days | NFS archive target |
| Cold (compliance archive) | 1–7 years | Object storage or tape |

Configure retention:
```
Administration → General → Retention → set retention period in days
Administration → Archiving → configure NFS archive target
```

---

## Content Pack Standards

| Content Pack | Source | Purpose |
|---|---|---|
| vSphere | Built-in | ESXi and vCenter log parsing and dashboards |
| NSX for vSphere | Marketplace | NSX-V controller and edge log parsing |
| NSX-T | Marketplace | NSX-T manager and edge log parsing |
| Linux | Marketplace | Generic Linux syslog parsing |
| Windows | Marketplace | Windows Event Log parsing |

Install content packs: **Administration → Content Packs → Marketplace → Browse → Install**.

Naming convention for custom content packs (developed in-house): `<org>-<system>-<version>.vlcp`

---

## Alert Severity Standards

Define alert severity tiers consistently across all custom alert definitions:

| Severity | Threshold | Notification | Example |
|---|---|---|---|
| Critical | Service-affecting; immediate action required | PagerDuty / on-call | Authentication service down |
| Error | Degraded state; action required within hours | Email + Teams | High rate of login failures |
| Warning | Unusual pattern; investigate today | Email | Elevated SCSI errors |
| Info | Informational only | Dashboard only | User login events |

---

## Cluster Sizing Rules

- Do not exceed 75% disk utilisation on any node — add a worker or expand disk before this threshold
- If a single node's disk is full, the cluster stops ingesting until space is freed
- Worker nodes can be added without downtime by joining them to the existing cluster via the master UI

Monitor disk usage:
```bash
# From master node SSH
df -h /var/log/loginsight
# Or via UI: Administration → Cluster → node list shows disk utilisation per node
```
