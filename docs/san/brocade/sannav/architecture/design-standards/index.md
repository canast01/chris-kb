# SANnav — Standards


<div class="kb-summary">
> Part of the [SANnav](../../index.md) reference.
</div>

---

## Overview

This page defines design standards, naming conventions, and configuration baselines for SANnav Management Portal deployments. Apply these standards during initial deployment and validate them during periodic operational reviews.

---

## Appliance Naming

| Object | Convention | Example |
|---|---|---|
| SANnav Portal VM | `sannav-<site>-<number>` | `sannav-dc1-01` |
| SANnav Global View VM | `sannav-gv-<site>` | `sannav-gv-prod` |
| Portal DNS record | `sannav-<site>.corp.example.com` | `sannav-dc1.corp.example.com` |
| Global View DNS record | `sannav-gv.corp.example.com` | |

Use DNS names, not IP addresses, in browser bookmarks and API clients. This allows the SANnav appliance IP to be changed (e.g. during DR) without client reconfiguration.

---

## Fabric and Resource Group Naming

SANnav groups switches into resource groups (called fabrics) that reflect the physical fabric topology:

| Object | Convention | Example |
|---|---|---|
| Fabric / resource group | `<site>-FABRIC-<id>` | `DC1-FABRIC-A`, `DC1-FABRIC-B` |
| Switch display name | `<site>-FC-<role>-<rack>-<unit>` | `DC1-FC-DIR-A01-U10` |

Apply consistent names at switch discovery time. SANnav uses the switch DNS name or IP if no display name is set, which makes large-fabric dashboards unreadable.

---

## Alert Policy Baseline

Define the following alert policy categories at minimum for all production fabrics:

| Category | Minimum Severity Threshold | Action |
|---|---|---|
| Port state change (F_Port down) | Warning | Email SAN team |
| Port state change (E_Port down) | Critical | Email SAN team + page on-call |
| ISL utilization > 80% | Warning | Email SAN team |
| MAPS CRC error violation | Warning | Email SAN team |
| MAPS loss-of-signal violation | Warning | Email SAN team |
| Switch health degraded | Critical | Email SAN team + page on-call |
| Firmware mismatch detected | Informational | Email SAN team |
| License expiry < 30 days | Warning | Email SAN team |

Alert emails should target a distribution list, not individual engineers, so that on-call rotation does not require SANnav reconfiguration.

---

## SNMP Configuration Baseline

All switches managed by SANnav must have SNMPv3 configured with credentials that match what SANnav has stored. Minimum configuration on each switch (FOS CLI):

```bash
# Add SNMPv3 user matching SANnav credentials
snmpconfig --set snmpv3 -index 1 -username sannav_mgmt \
  -authtype MD5 -authpasswd <auth-pass> \
  -privtype AES128 -privpasswd <priv-pass> \
  -rwcommunity sannav_rw

# Add SANnav as trap recipient
snmpconfig --set trapdest -index 1 \
  -trapdest <sannav-ip> -severity 4 \
  -username sannav_mgmt -authtype MD5 -authpasswd <auth-pass> \
  -privtype AES128 -privpasswd <priv-pass> -trapport 162

# Verify
snmpconfig --show snmpv3
snmpconfig --show trapdest
```
```
┌────────────────────────────────── Brocade SANnav — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│  Design principles: HA deployment, dedicated management VLAN, RBAC, TLS, backups.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Deployment Standards             │  │              Security Standards             │   │
│   │        HA pair: primary + standby VM         │  │         TLS 1.2+ for all web traffic        │   │
│   │           Separate management VLAN           │  │         TACACS+ mandatory; no local         │   │
│   │          4 vCPU / 16 GB RAM minimum          │  │        RBAC: read-only for operators        │   │
│   │            NTP for all timestamps            │  │         SNMPv3 only; disable v1/v2c         │   │
│   │          Dedicated mgmt DNS entries          │  │         IP whitelist for API access         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  HA ensures continuity; dedicated VLAN isolates management traffic from data plane.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Operational Standards             │  │            Scalability Guidelines           │   │
│   │        Backup: daily NFS; 30-day ret.        │  │         Max 1,000 switches per node         │   │
│   │        Alert review: daily MAPS check        │  │          Max 100,000 ports per node         │   │
│   │         Zone changes: change ticket          │  │        Separate instances per fabric        │   │
│   │        Firmware mgmt via SANnav only         │  │           Scale-out: additional VM          │   │
│   │           Quarterly SANnav upgrade           │  │        Storage: 2 TB for 90-day perf        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere host · shared datastore (2 TB+) · management Ethernet switch · NFS backup                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HA pair         = SANnav primary+standby VMs; standby syncs config and takes over                    │
│  Management VLAN = isolated VLAN for switch OOB and SANnav traffic; no user VLAN                      │
│  RBAC            = Role-Based Access Control; admin/operator/read-only roles in SANnav                │
│  NTP             = Network Time Protocol; all events timestamped; required for SIEM                   │
│  SNMPv3          = SNMP version 3; auth + privacy mode; disable v1/v2c in SANnav                      │
│  IP whitelist     = restrict REST API and management access to known source IPs                       │
│  TLS 1.2+        = minimum TLS version for SANnav HTTPS management GUI                                │
│  NFS backup      = daily SANnav configuration and database backup to NFS share                        │
│  MAPS check      = daily review of Monitoring and Alerting Policy Suite events                        │
│  Change ticket   = ITSM requirement; all zone changes need approved change record                     │
│  90-day perf     = SANnav default performance data retention; requires ~2 TB storage                  │
│  Scale-out       = deploy additional SANnav instances when port count exceeds limit                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

- Assign switches to the correct resource group immediately after discovery. Switches left in the default group are invisible to role-scoped SANnav operators.

---

## Backup Standards

| Backup Type | Frequency | Retention | Storage |
|---|---|---|---|
| SANnav full backup | Weekly | 4 copies | Remote NFS or SCP target |
| SANnav configuration export | Before every upgrade | Indefinite | Change management system |
| Individual switch zone backup | Before every zone change | 5 copies | SANnav backup repository |

Backup schedule is configured under **Administration > Backup**. Remote targets (SCP or NFS) are strongly recommended; relying on the local disk of the SANnav VM is not sufficient for DR.

---

## Firmware Management Standards

- Maintain a validated FOS version baseline for each hardware generation.
- Upload approved FOS images to SANnav before they are needed (avoids scrambling during incidents).
- Use SANnav scheduled upgrades for non-disruptive rolling upgrades across a fabric — never manually upgrade all switches simultaneously.
- Retain one previous FOS version in the SANnav image repository for rollback.

| Gen | Recommended minimum FOS | Notes |
|---|---|---|
| Gen 7 (G7xx, X7) | FOS 9.2.x | Required for 64G and NVMe-oF |
| Gen 6 (G6xx, X6) | FOS 9.1.x | 32G FC |
| Legacy Gen 5 | FOS 8.2.x | No new features; security patches only |

---

## User Account Standards

- No shared accounts. Each engineer must have an individual named account.
- Service accounts for automation or monitoring must be named `svc-<purpose>` and must use the minimum required role (Viewer for read-only; Operator for config changes).
- Local admin account is the break-glass only; password stored in vault; rotated quarterly.
- LDAP group membership controls all production access; local accounts for break-glass only.

---

## Change Management Integration

All SANnav configuration changes (zoning, firmware, MAPS policy deployment) must be performed within an approved change window. Document the following in the change record:

1. Current zone set (export from SANnav before change)
2. Target zone set (export after change)
3. SANnav version at time of change
4. Switch firmware versions at time of change
5. Post-change validation results
