# Aria Operations — Standards

```
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
