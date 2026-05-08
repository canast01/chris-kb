# Cisco DCNM — Health Checks

> Part of the [Cisco DCNM](../../) reference.

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

---

## 2. Fabric Discovery Status

### GUI

Navigate to **SAN > Fabrics**. For each fabric:
- All expected switches should be **Manageable** or **Managed** state
- Switch count should match expected
- No switches in **Unmanageable** or **Unknown** state

If a switch shows **Unmanageable**:
1. Verify SSH connectivity: from DCNM appliance, `ssh dcnm_mgmt@<switch-ip>`
2. Verify SNMP: `snmpget -v3 -u dcnm_poll -l authPriv -a SHA -A <auth-pass> -x AES -X <priv-pass> <switch-ip> sysDescr.0`
3. Check DCNM discovery log: `grep "<switch-ip>" /var/log/dcnm/discovery.log | tail -20`

---

## 3. VSAN Health

Navigate to **SAN > VSANs**. For each production VSAN:
- VSAN should be **Active** on all member switches
- No VSAN isolation events in the event log

### CLI Verification on Switch

```bash
# On MDS switch (NX-OS CLI)
show vsan
# All production VSANs should be Active

show vsan membership
# Confirm expected ports are in expected VSANs

show vsan <vsan-id> membership
# No unexpected ports
```

---

## 4. ISL Health and Utilization

Navigate to **SAN > ISLs**. For each fabric:
- All ISLs should show **Up** state
- Utilization columns: review for sustained high utilization (> 70%)
- Error columns: any CRC or signal loss errors require investigation

```bash
# On MDS switch for ISL detail
show topology
show interface fc<slot/port> counters detail
# Check: input errors, CRC, output discard
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
