# Cisco DCNM — Health Checks


<div class="kb-summary">
> Part of the [Cisco DCNM](../../index.md) reference.
</div>

---

## Overview

Run these checks on a regular schedule — daily for critical SAN environments, weekly minimum for all production fabrics. Checks are performed via the DCNM web GUI, REST API, and the DCNM appliance CLI.

---

## 1. DCNM Appliance Health

### GUI

Navigate to **Administration > System > System Status**. Verify:
- All services show **Running**
- Disk usage below 80%
- Memory usage below 85%

### Appliance CLI

```bash
ssh root@dcnm-dc1.corp.example.com

# DCNM service status
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status
# All services should show as running

# Disk usage
df -h
# Alert if /var/lib/pgsql or /var/dcnm is > 80% used

# Database size
du -sh /var/lib/pgsql/data/

# Check DCNM server log for errors
grep -i "ERROR\|SEVERE\|Exception" /var/log/dcnm/server.log | tail -50

# NTP status
timedatectl status
# Expected: synchronized: yes
```
┌───────────────────────────────────── Cisco DCNM — Health Checks ──────────────────────────────────────┐
│                                                                                                       │
│  DCNM health checks: dashboard alerts, switch status, ISL load, zone consistency.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            DCNM Dashboard Health             │  │             Switch-Level Health             │   │
│   │       SNMP alerts: active by severity        │  │          show system health: all OK         │   │
│   │        Fabric topology: no split VSAN        │  │          show environment: temp/PSU         │   │
│   │          Port inventory: no offline          │  │          show interface: no errors          │   │
│   │         NX-OS currency: < 2 versions         │  │          show version: verify build         │   │
│   │          Zone set: saved == active           │  │         show flogi database: logins         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DCNM dashboard and MDS show commands are first-line health checks; run daily.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              ISL & VSAN Health               │  │             DCNM Platform Health            │   │
│   │        show interface trunk: ISL util        │  │          DCNM services: all running         │   │
│   │           ISL > 70% util: add more           │  │             DB: disk usage < 80%            │   │
│   │            show vsan: all active             │  │          HA sync: primary = standby         │   │
│   │        Credit starvation: pause check        │  │           Backup: last job success          │   │
│   │           Port error rate < 10/day           │  │          Cert expiry > 60 days left         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Cisco MDS switch chassis · SFP transceivers · ISL FC cables · DCNM VM resources                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  show system health= MDS NX-OS command; reports module and fabric health status                       │
│  show environment = MDS NX-OS; shows temperature, fan, and PSU sensor readings                        │
│  show flogi database= FC login database; verifies all HBAs are logged into fabric                     │
│  show vsan        = VSAN state; confirms all VSANs are active and not suspended                       │
│  show interface trunk= ISL trunk status and utilisation counters                                      │
│  Credit starvation= FC flow control issue; BB credits exhausted; causes pause                         │
│  Zone set saved   = saved zone database should match active; divergence = risk                        │
│  DCNM HA sync    = primary and standby DCNM databases must be synchronised                            │
│  Cert expiry      = TLS certificate monitored; alert 60 days before expiry                            │
│  NX-OS currency   = keep MDS within 2 major versions of latest supported release                      │
│  Backup status    = nightly DCNM backup job result; alert on failure                                  │
│  VSAN split       = VSAN partition causing isolation; major incident requiring fix                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────── Cisco DCNM — Health Checks ──────────────────────────────────────┐
│                                                                                                       │
│  DCNM health checks: dashboard alerts, switch status, ISL load, zone consistency.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            DCNM Dashboard Health             │  │             Switch-Level Health             │   │
│   │       SNMP alerts: active by severity        │  │          show system health: all OK         │   │
│   │        Fabric topology: no split VSAN        │  │          show environment: temp/PSU         │   │
│   │          Port inventory: no offline          │  │          show interface: no errors          │   │
│   │         NX-OS currency: < 2 versions         │  │          show version: verify build         │   │
│   │          Zone set: saved == active           │  │         show flogi database: logins         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DCNM dashboard and MDS show commands are first-line health checks; run daily.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              ISL & VSAN Health               │  │             DCNM Platform Health            │   │
│   │        show interface trunk: ISL util        │  │          DCNM services: all running         │   │
│   │           ISL > 70% util: add more           │  │             DB: disk usage < 80%            │   │
│   │            show vsan: all active             │  │          HA sync: primary = standby         │   │
│   │        Credit starvation: pause check        │  │           Backup: last job success          │   │
│   │           Port error rate < 10/day           │  │          Cert expiry > 60 days left         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Cisco MDS switch chassis · SFP transceivers · ISL FC cables · DCNM VM resources                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  show system health= MDS NX-OS command; reports module and fabric health status                       │
│  show environment = MDS NX-OS; shows temperature, fan, and PSU sensor readings                        │
│  show flogi database= FC login database; verifies all HBAs are logged into fabric                     │
│  show vsan        = VSAN state; confirms all VSANs are active and not suspended                       │
│  show interface trunk= ISL trunk status and utilisation counters                                      │
│  Credit starvation= FC flow control issue; BB credits exhausted; causes pause                         │
│  Zone set saved   = saved zone database should match active; divergence = risk                        │
│  DCNM HA sync    = primary and standby DCNM databases must be synchronised                            │
│  Cert expiry      = TLS certificate monitored; alert 60 days before expiry                            │
│  NX-OS currency   = keep MDS within 2 major versions of latest supported release                      │
│  Backup status    = nightly DCNM backup job result; alert on failure                                  │
│  VSAN split       = VSAN partition causing isolation; major incident requiring fix                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Active Alarms

Navigate to **Monitor > Alarms > Active Alarms**. Triage:

| Severity | Action |
|---|---|
| Critical | Immediate response |
| Major | Assign and respond within 4 hours |
| Minor | Review and acknowledge within 24 hours |
| Warning | Review daily |

Suppress acknowledged alarms that have no current operational impact. Use the **Acknowledge** function to track ownership.

---

## 6. Zone Set Consistency

Navigate to **SAN > Zoning > Active Zone Sets**. Verify:
- The correct zone set is active in each VSAN
- Zone member count matches expectations (unexpected changes may indicate unauthorised zone modifications)

```bash
# On MDS switch to verify zone set consistency
show zoneset active vsan <vsan-id>
# Compare against expected zone set exported from DCNM
```

---

## 7. End Device Inventory

Navigate to **SAN > End Devices**. Verify:
- Expected host HBAs and storage ports are listed and Online
- No unexpected FC IDs (may indicate rogue devices or fabric segment leakage)
- Device alias assignments are correct

---

## 8. Performance Manager Data

Navigate to **Monitor > Performance > Interfaces**. Verify:
- Performance data is being collected for all managed switches (data should be current; if last update is > 10 minutes ago, PM polling may have stalled)
- No sustained high-utilization ISLs approaching capacity
- No growing error counters on any port

---

## Weekly Health Check Summary

| Check | Pass Criterion | Location |
|---|---|---|
| DCNM services running | All services: Running | Admin > System Status |
| Disk usage < 80% | < 80% | Appliance CLI / Admin |
| NTP synchronized | Yes | Appliance CLI |
| All switches managed | 0 unmanageable | SAN > Fabrics |
| All VSANs active | 0 isolated/inactive | SAN > VSANs |
| All ISLs up | 0 ISL down | SAN > ISLs |
| ISL utilization | No ISL > 70% sustained | Monitor > Performance |
| No unacknowledged critical alarms | 0 critical unacked | Monitor > Alarms |
| Active zone set correct | Matches expected | SAN > Zoning |
| Performance data current | Last poll < 10 min | Monitor > Performance |
| DB backup successful | Last backup < 8 days | Backup log |
