# Aria Operations — Standards

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
- Valid TLS certificate (CA-signed recommended; see [Security](../security/))
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

- [Architecture](../architecture/) — node roles and sizing
- [Operations](../operations/) — daily checks and health monitoring
- [Security](../security/) — RBAC roles and TLS
