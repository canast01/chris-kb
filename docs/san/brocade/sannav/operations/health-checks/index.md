# SANnav — Health Checks

> Part of the [SANnav](../../) reference.

---

## Overview

Run these checks on a scheduled basis — daily for critical fabric environments, at minimum weekly for all production fabrics. Checks are split between the SANnav web GUI, the SANnav REST API, and the appliance OS CLI.

---

## 1. SANnav Appliance Health

### GUI

Navigate to **Administration > System Status**. Verify:
- All services show **Running** (UI, Server, Discovery, Event Engine)
- Disk usage is below 80%
- Database status is **Healthy**

### Appliance CLI

```bash
# SSH to appliance
ssh admin@sannav-dc1.corp.example.com

# Check service status
sannav status
# Expected: all services: running

# Check disk usage
df -h /opt/sannav
# Alert if Use% > 80

# Check application logs for errors
grep -i "ERROR\|FATAL" /opt/sannav/logs/server.log | tail -50

# Check discovery engine for unreachable switches
grep "unreachable\|connection refused\|timeout" /opt/sannav/logs/discovery.log | tail -30

# Check event engine
grep -i "ERROR" /opt/sannav/logs/event-engine.log | tail -20

# Check NTP sync
timedatectl status
# Expected: "synchronized: yes"
```

---

## 2. Fabric Discovery Status

### GUI

Navigate to **Dashboard > Fabric Summary**. For each managed fabric:

- All expected switches should show **Online** status (green)
- Switch count should match the expected number
- No switches should be in **Unreachable** or **Unknown** state

If any switch shows **Unreachable**:
1. Confirm the switch is powered on and accessible by IP
2. Verify HTTPS credentials: navigate to **Discovery > Switches**, click the switch, and click **Test Connection**
3. Confirm SNMPv3 credentials match: **Discovery > Switches > SNMP Settings**

### REST API

```bash
TOKEN=$(curl -sk -X POST https://sannav-dc1.corp.example.com/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"svc-monitor","password":"<pass>"}}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['authToken'])")

# List all switches and their connectivity status
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool | grep -E '"name"|"connectivityState"'

# Expected connectivityState: "REACHABLE" for all switches
```

---

## 3. Port State Checks

### GUI

Navigate to **Inventory > Ports**. Filter by:
- Port State: **Offline** or **Faulty** — investigate any unexpected offline ports
- Port Type: **E_Port** — check all ISL ports are **Online**

### Check ISL Utilization

Navigate to **Monitor > Performance > ISLs**. Review the 24-hour utilization graph for each ISL. Raise a capacity concern if any ISL consistently exceeds 70% utilization.

---

## 4. Active Alerts Review

Navigate to **Events > Active Alerts**. Triage all open alerts:

| Severity | Action |
|---|---|
| Critical | Immediate investigation required |
| Warning | Review within 4 hours; assign owner |
| Informational | Review daily; close or acknowledge |

Close stale alerts that have been resolved at the switch level but not acknowledged in SANnav. Unacknowledged alerts accumulate and mask new genuine alerts.

---

## 5. MAPS Policy Violation Review

Navigate to **Monitor > MAPS Violations**. Review the last 24-hour violation summary:

- **CRC errors** — indicates a failing SFP, cable, or connector. Locate the port and inspect hardware.
- **Loss of signal (LOS)** — intermittent physical layer problem. Check cable seating, SFP, and patch panel connections.
- **Fabric watch ITW** — invalid transmission word errors. Often co-occurs with CRC; same root cause.
- **FC credit zero** — buffer credit starvation. Indicates congestion or a slow-drain device.
- **FC credit recovery** — CREDIT_LOSS events. May indicate a misconfigured port speed or faulty HBA.

---

## 6. Firmware Version Audit

Navigate to **Inventory > Switches**. Add the **Firmware Version** column to the view and export the list. Compare against the approved firmware baseline for each hardware generation.

Any switch below the minimum approved version should be scheduled for upgrade. Group switches by firmware version to identify clusters that can be upgraded together.

---

## 7. License Validity

Navigate to **Administration > License Management**. Verify:
- No licenses are expired
- Remaining days on near-expiry licenses (< 60 days: raise with procurement)
- Licensed port count covers the number of managed ports in the fabric

---

## 8. Backup Status

Navigate to **Administration > Backup**. Verify the last scheduled backup completed successfully and is dated within the expected window. If the last backup is older than 8 days (for weekly schedule), investigate.

---

## Weekly Health Check Summary

| Check | Pass Criterion | Tool |
|---|---|---|
| SANnav services all running | All: Running | Appliance CLI / Admin UI |
| Disk usage | < 80% | Appliance CLI |
| NTP synchronized | Yes | Appliance CLI |
| All switches reachable | 0 unreachable | SANnav dashboard |
| No critical active alerts | 0 critical | SANnav Events |
| No ISLs > 70% sustained utilization | No congestion | SANnav Performance |
| MAPS violations reviewed | No unactioned critical | SANnav MAPS |
| All switches at approved firmware | 0 below baseline | SANnav Inventory |
| No expired licenses | 0 expired | SANnav Admin |
| Recent backup successful | < 8 days old | SANnav Admin |
