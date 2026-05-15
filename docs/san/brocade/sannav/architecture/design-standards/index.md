# SANnav — Standards

> Part of the [SANnav](../../) reference.

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

In SANnav, enter these credentials under **Discovery > Add Switch > SNMP Credentials**.

---

## Switch Discovery Standards

- All switches must be discovered with **HTTPS credentials** (FOS REST API, not legacy SNMP-only management).
- Use dedicated SANnav service account on each switch rather than the `admin` account:

```bash
# On each managed switch (FOS CLI)
userconfig --add sannav_svc -r admin -p <password>
# Role "admin" is required for zoning and firmware operations.
# Use "user" role for read-only SANnav deployments.
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
