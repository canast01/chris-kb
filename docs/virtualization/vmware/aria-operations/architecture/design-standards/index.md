# Aria Operations — Standards

```text
┌────────────────────────────────── Aria Operations Design Standards ───────────────────────────────────┐
│                                                                                                       │
│  Node sizing, cluster topology, and policy design standards for Aria Operations (vROps).              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Node Sizing                  │  │               Cluster Topology              │   │
│   │         Small: <1500 objects, 4 vCPU         │  │            Master node: always 1            │   │
│   │         Medium: <5000 objects, 8vCPU         │  │           Replica: HA standby node          │   │
│   │        Large: <15000 objects, 16vCPU         │  │         Data nodes: scale analytics         │   │
│   │           RAM: 32-256 GB by sizing           │  │          Remote collector: per site         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Sizing drives node count; topology drives HA; policy design drives alert quality.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Policy Design Standards            │  │              Storage & Network              │   │
│   │         Default policy: base alerts          │  │          SSD datastore recommended          │   │
│   │         Custom policy: per workload          │  │         1 GbE min; 10 GbE preferred         │   │
│   │         Alert criticality: 1-5 scale         │  │           NFS or vSAN shared store          │   │
│   │           Symptom + recommendation           │  │          Dedicated management VLAN          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps VMs on vSphere cluster; SSD-backed NFS or vSAN datastore; management VLAN                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master Node         = Primary vROps node; hosts UI, analytics, and cluster management                │
│  Replica Node        = Standby master; takes over if master fails for HA                              │
│  Data Node           = Analytics scale-out node; adds capacity for more objects                       │
│  Remote Collector    = Lightweight VM deployed per site; forwards data to cluster                     │
│  Object              = Any monitored entity: VM, host, datastore, application                         │
│  Policy              = Named set of alert thresholds and capacity model settings                      │
│  Symptom             = Single condition (e.g. CPU > 90%) contributing to an alert                     │
│  Recommendation      = Action suggested by vROps when an alert fires                                  │
│  Alert Criticality   = Severity 1-5 scale; 1=info, 5=critical for vROps alerts                        │
│  CaSA Store          = Configuration and Support Archive; vROps internal config DB                    │
│  Management Pack     = Plugin extending vROps with additional adapters and dashboards                 │
│  Adapter             = Collection plugin; connects vROps to a specific data source                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
Aria Operations — Sizing and Deployment Reference
┌─────────────────────────────────────────────────────┐
│  Cluster Size Selection                             │
│                                                     │
│  Extra Small  Primary only    4 vCPU / 16 GB RAM    │
│               up to 500 VMs                         │
│                                                     │
│  Small        Primary only    8 vCPU / 32 GB RAM    │
│               up to 1,500 VMs                       │
│                                                     │
│  Medium       Primary         8 vCPU / 32 GB RAM    │
│               + Replica       8 vCPU / 32 GB RAM    │
│               up to 3,500 VMs                       │
│                                                     │
│  Large        Primary + Replica + 2 × Data          │
│               up to 10,000 VMs                      │
│                                                     │
│  XL           Primary + Replica + 4+ × Data         │
│               10,000+ VMs                           │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  Infrastructure Requirements                        │
│  ┌─────────────────────────────────────────────┐    │
│  │ DNS: A + PTR for every node                 │    │
│  │ NTP: drift < 1 second across all nodes      │    │
│  │ TLS: CA-signed cert (not self-signed)        │   │
│  │ SMTP: relay configured for alert email       │   │
│  │ LDAP/AD: bind account + group DNs ready     │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  Remote Collector (per remote site):                │
│  2 vCPU / 4 GB RAM · connects via 4505/4506         │
└─────────────────────────────────────────────────────┘
```

## Naming Conventions

| Object | Convention | Example |
|--------|-----------|---------|
| Primary node | `aria-ops-primary-<site>` | `aria-ops-primary-dc1` |
| Replica node | `aria-ops-replica-<site>` | `aria-ops-replica-dc1` |
| Data node | `aria-ops-data-<site>-<nn>` | `aria-ops-data-dc1-01` |
| Remote collector | `aria-rc-<site>` | `aria-rc-remote01` |
| Cloud proxy | `aria-cp-<cloud>-<region>` | `aria-cp-aws-eu-west` |
| vCenter adapter | `<vcenter-fqdn>` | `vcsa01.domain.local` |

---

## Build Baseline

### Node Configuration (per role)

| Role | vCPU | RAM | OS Disk | Data Disk |
|------|------|-----|---------|-----------|
| Primary (medium) | 8 | 32 GB | 100 GB | 500 GB |
| Replica (medium) | 8 | 32 GB | 100 GB | 500 GB |
| Data Node | 8 | 32 GB | 100 GB | 1 TB |
| Remote Collector | 2 | 4 GB | 60 GB | — |

### Required Infrastructure

- DNS A record and reverse (PTR) for every node
- NTP configured on all nodes (drift < 1 second within cluster)
- Valid TLS certificate (CA-signed recommended; see [Security](../../security/index.md))
- SMTP relay configured for alert email delivery
- AD/LDAP group mapped for RBAC roles

---

## Configuration Checklist

### Pre-deployment

- [ ] DNS A + PTR records created for all nodes
- [ ] NTP source configured and reachable
- [ ] vCenter service account created with read-only role (minimum) or Administrator for full remediation actions
- [ ] NSX service account created
- [ ] SMTP relay details available
- [ ] AD/LDAP bind account and group DNs documented

### Post-deployment

- [ ] Cluster status shows **Online** in Administration > Cluster Management
- [ ] All adapter instances show **Collecting** (green)
- [ ] Alert definitions reviewed and tuned (disable noisy defaults)
- [ ] Super Metrics / custom dashboards imported
- [ ] Notification rules configured (email, webhook, ITSM)
- [ ] Backup/snapshot schedule confirmed
- [ ] TLS certificate replaced with CA-signed cert
- [ ] LDAP auth configured and tested

---

## Alert Policy Standards

- Default alert policies are inherited; create **custom alert policies** per object type.
- Set criticality thresholds per environment (prod vs. non-prod groups).
- Suppress alerts during maintenance windows using Maintenance Schedules.

---

## Related Sections

- [Architecture](../index.md) — node roles and sizing
- [Operations](../../operations/index.md) — daily checks and health monitoring
- [Security](../../security/index.md) — RBAC roles and TLS
