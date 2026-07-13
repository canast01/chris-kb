---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
description: "How to escalate Brocade SANnav Management Portal issues to Broadcom support: what data to collect, how to generate the SANnav support bundle, step-by-step..."
---
# Brocade SANnav — Escalation

<div class="kb-summary">
How to escalate Brocade SANnav Management Portal issues to Broadcom support: what data to collect, how to generate the SANnav support bundle, step-by-step case creation on support.broadcom.com, and the escalation path when progress stalls.

*Applies to: SANnav Management Portal 2.x*
</div>
![Brocade SANnav — Escalation](../../../../assets/san-brocade-sannav-troubleshooting-escalation.svg)




---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
preescalation_selfcheck: "Pre-Escalation Self-Check" {shape: rectangle}
stepbystep_data_collection: "Step-by-Step Data Collection" {shape: rectangle}
how_to_open_the_sr_on_supportbroadco: "How to Open the SR on support.broadcom.com" {shape: rectangle}
escalation_path: "Escalation Path" {shape: rectangle}
what_not_to_do: "What NOT to Do" {shape: rectangle}
useful_commands_for_case_updates: "Useful Commands for Case Updates" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> preescalation_selfcheck: investigate
symptom -> stepbystep_data_collection: investigate
symptom -> how_to_open_the_sr_on_supportbroadco: investigate
symptom -> escalation_path: investigate
symptom -> what_not_to_do: investigate
symptom -> useful_commands_for_case_updates: investigate
preescalation_selfcheck -> resolution
stepbystep_data_collection -> resolution
how_to_open_the_sr_on_supportbroadco -> resolution
escalation_path -> resolution
what_not_to_do -> resolution
useful_commands_for_case_updates -> resolution
```

## Before you begin

- **Access required:** SSH access to the SANnav appliance VM; SANnav admin UI credentials; Broadcom support account at support.broadcom.com with active SANnav entitlement; FOS admin credentials on the managed switches
- **Freeze all fabric changes** during an active SANnav incident — zone configuration changes pushed to switches during a SANnav failure can leave fabrics in a partially committed state
- **Do NOT restart the SANnav service** during a failed upgrade without TAC direction — an incomplete restart during upgrade recovery can corrupt the SANnav database
- **Do NOT delete the SANnav database** (`/opt/brocade/sannav/postgres/data/`) without explicit TAC instruction — the database contains the only record of the historical fabric state TAC uses to diagnose the failure

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command / Location | Expected result |
|---|---|---|
| SANnav version | SSH: `sannav version` | Note full version (e.g. 2.3.0a) |
| SANnav UI accessibility | Browse to `https://<sannav-ip>/` | Login page loads |
| SANnav services | SSH: `sannav-admin status` | All services Running |
| Database status | SSH: `sannav-admin db-status` | PostgreSQL service running |
| Disk space | SSH: `df -h /opt/brocade/sannav` | Below 80% used |
| Switch discovery | SANnav UI → Inventory → Switches | All expected switches shown as Reachable |
| FOS version per switch | SANnav UI → Inventory → Switches → [switch] → Details | Note FOS version; check compatibility matrix |
| Recent alerts | SANnav UI → Alerts → Active | Note any critical alerts on the SANnav appliance itself |

---

## Step-by-Step Data Collection

### 1. Get the SANnav version and appliance health

```bash
# SSH to the SANnav appliance as admin
ssh admin@<sannav-ip>

# SANnav version
sannav version

# Service status
sannav-admin status

# Database status
sannav-admin db-status

# Disk space (SANnav data and log partitions)
df -h /opt/brocade/sannav
df -h

# Memory and CPU
free -h
uptime
```


```text title="Expected output"
admin@sannav-prod-01:~$ sannav version
SANnav Version: 2.3.1.0
Build: 20240115-143022
Release Date: January 15, 2024

admin@sannav-prod-01:~$ sannav-admin status
SANnav Services Status:
  sannav-core         : RUNNING (PID: 4521)
  sannav-db           : RUNNING (PID: 4389)
  sannav-api          : RUNNING (PID: 4612)
  sannav-collector    : RUNNING (PID: 4701)
  sannav-web          : RUNNING (PID: 4823)

admin@sannav-prod-01:~$ sannav-admin db-status
Database Status: HEALTHY
Connected Clients: 12
Replication Status: IN_SYNC
Last Backup: 2024-01-18 03:45:22 UTC

admin@sannav-prod-01:~$ df -h /opt/brocade/sannav
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       500G  387G  113G  78% /opt/brocade/sannav

admin@sannav-prod-01:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   45G   55G  45% /
/dev/sda2        50G   28G   22G  56% /var
/dev/sda3       500G  387G  113G  78% /opt/brocade/sannav
tmpfs            32G     0   32G   0% /dev/shm

admin@sannav-prod-01:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:           64Gi        48Gi        8Gi       512Mi        8Gi        15Gi
Swap:          16Gi       2.1Gi        14Gi

admin@sannav-prod-01:~$ uptime
 14:32:18 up 187 days, 14:22,  2 users,  load average: 2.14, 2.08, 1.97
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connection refused` | Verify SANnav appliance is reachable with `ping <sannav-ip>` and SSH service is running with `systemctl status ssh`. |
    | `sannav-admin: command not found` | Ensure you are logged in as the admin user and `/opt/brocade/sannav/bin` is in your PATH, or use the full path `/opt/brocade/sannav/bin/sannav-admin`. |
    | `Database Status: UNHEALTHY` | Check database logs with `sannav-admin db-logs` and restart the database service using `sannav-admin restart db`. |
### 2. Generate the SANnav support bundle

```bash
# SSH to the SANnav appliance
ssh admin@<sannav-ip>

# Generate the support bundle — this is mandatory for any TAC case
sannav support-bundle --output /tmp/sannav-diag-$(date +%Y%m%d).tar.gz

# Verify and check file size
ls -lh /tmp/sannav-diag-*.tar.gz

# Copy to a local workstation for upload
scp admin@<sannav-ip>:/tmp/sannav-diag-*.tar.gz /tmp/
```


```text title="Expected output"
admin@<sannav-ip>'s password: 
Last login: Wed Jan 15 14:32:18 2025 from 10.45.12.89
SANnav> sannav support-bundle --output /tmp/sannav-diag-20250115.tar.gz
Collecting system logs...
Collecting configuration data...
Collecting performance metrics...
Collecting fabric topology...
Support bundle generated successfully: /tmp/sannav-diag-20250115.tar.gz
-rw-r--r-- 1 admin admin 487M Jan 15 14:35 /tmp/sannav-diag-20250115.tar.gz
admin@10.45.67.23's password: 
sannav-diag-20250115.tar.gz                           100%  487MB   8.2MB/s   00:59
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sannav: command not found` | Verify you are logged into the SANnav appliance itself (not a switch) and that the sannav CLI is in your PATH; check with `which sannav`. |
    | `Permission denied (publickey,password)` | Ensure the admin account credentials are correct and SSH key-based authentication is configured, or use `ssh -v` to debug the connection. |
    | `No such file or directory` | The support-bundle command may have failed silently; re-run the command and check `/tmp/` for any partial `.tar.gz` files or error logs in `/var/log/sannav/`. |
### 3. Collect the SANnav service log (journalctl)

```bash
# SSH to the SANnav appliance
ssh admin@<sannav-ip>

# Collect the full SANnav service log from systemd journal
sudo journalctl -u sannav --no-pager --output short-iso > /tmp/sannav-journal-$(date +%Y%m%d).log

# Or last 2000 lines
sudo journalctl -u sannav -n 2000 --no-pager > /tmp/sannav-journal-recent.log

# Capture resource stats over a few minutes (for intermittent issues)
for i in {1..5}; do
  echo "=== $(date) ==="
  free -h
  df -h /opt/brocade/sannav
  uptime
  sleep 30
done > /tmp/sannav-perf-$(date +%Y%m%d).txt
```


```text title="Expected output"
admin@sannav-prod-01's password: 
(no output — command completes silently)
(no output — command completes silently)
=== Wed Jan 15 14:32:18 UTC 2025 ===
              total        used      available
Mem:           15Gi       12Gi         2.1Gi
Swap:          4.0Gi      1.2Gi        2.8Gi
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda3      500G  387G  113G  78% /opt/brocade/sannav
 14:32:18 up 127 days, 14:22,  2 users,  load average: 2.14, 1.98, 1.87
=== Wed Jan 15 14:32:48 UTC 2025 ===
              total        used      available
Mem:           15Gi       12Gi         2.0Gi
Swap:          4.0Gi      1.2Gi        2.8Gi
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda3      500G  387G  113G  78% /opt/brocade/sannav
 14:32:48 up 127 days, 14:23,  2 users,  load average: 2.09, 2.01, 1.89
=== Wed Jan 15 14:33:18 UTC 2025 ===
              total        used      available
Mem:           15Gi       12Gi         2.1Gi
Swap:          4.0Gi      1.2Gi        2.8Gi
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda3      500G  387G  113G  78% /opt/brocade/sannav
 14:33:18 up 127 days, 14:23,  2 users,  load average: 1.94, 1.99, 1.88
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sudo: journalctl: command not found` | Verify the SANnav appliance is running a systemd-based OS; if using an older version, use `tail -f /var/log/sannav.log` instead. |
    | `Permission denied (publickey,password)` | Confirm the admin account credentials and that SSH key-based or password authentication is enabled on the SANnav appliance. |
    | `No such file or directory: /opt/brocade/sannav` | Verify the SANnav installation path matches your deployment; check with `df -h` to locate the actual mount point. |
### 4. Run supportsave on affected switches

```bash
# SSH to each affected Brocade switch as admin
ssh admin@<switch-ip>

# Generate the switch support bundle
supportsave

# Switch version
firmwareshow

# Zoning status
cfgshow
nsshow
fabricshow
```


```text title="Expected output"
admin@switch-ip's password: 
Brocade Switch Admin CLI

switch:admin> supportsave
Generating support bundle...
Creating tar file /var/log/support/brocade_support_20240115_143022.tar.gz
Support bundle created successfully.
File size: 245 MB
Location: /var/log/support/brocade_support_20240115_143022.tar.gz

switch:admin> firmwareshow
Firmware Version: v8.2.1b
Build: 8.2.1.0.0.0.0
Serial Number: 0621A2B00C4E
Model: Brocade 6510

switch:admin> cfgshow
Defined configurations:
 0: PROD_ZONE_CFG (current)
 1: TEST_ZONE_CFG
 2: BACKUP_CFG

switch:admin> nsshow
 N Port wwn is 50:00:14:40:1b:2c:3d:4e
 Fabric Port Name: switch1
 Fabric Port wwn: 50:00:14:40:1b:2c:3d:4e
 State: Online
 Speed: 16Gb

switch:admin> fabricshow
Switch ID   Worldwide Name      Fabric Name         FC Address
------------------------------------------------------------------
   1        50:00:14:40:1b:2c:3d:4e  PROD_FABRIC_01      100.0000
   2        50:00:14:40:1b:2c:3d:4f  PROD_FABRIC_02      100.0001
   3        50:00:14:40:1b:2c:3d:50  PROD_FABRIC_03      100.0002
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,password).` | Verify SSH credentials and that the admin account is not locked; check `/etc/passwd` on the switch or contact your Brocade support team. |
    | `supportsave: command not found` | Ensure you are logged in as admin user and not in restricted shell mode; use `role show` to verify admin privileges. |
    | `Fabric is offline or not responding` | Check physical cable connections, port status with `portshow`, and verify switch is not in maintenance mode with `switchstatusshow`. |
Repeat `supportsave` on every switch in the affected fabric. TAC needs the switch-level data alongside the SANnav data.

### 5. Export the SANnav audit log

In the SANnav UI:
1. Click **Audit** (or navigate to **Administration → Audit Log**).
2. Set the time range to cover the 48 hours before the issue started.
3. Click **Export** → CSV.
4. Download and attach to the case.

The audit log shows every zone change, discovery action, and admin operation that occurred before the failure.

### 6. Write the timeline

```text
SANnav version: 2.3.0a build XXXXXXXX
Appliance: sannav-01.corp.local (VMware VM, 16 vCPU, 32 GB RAM)
Managed fabrics: 2 fabrics (Fabric-A: 12 switches, Fabric-B: 8 switches)
FOS versions: 9.1.0a, 9.0.1d (mixed — check compatibility matrix)
Issue first observed: 2026-06-14 13:00 UTC
Last confirmed working: 2026-06-14 12:00 UTC
Changes in 24h before the issue:
  - 11:30: SANnav upgrade 2.2.0 to 2.3.0a initiated via VAMI
  - 12:00: Upgrade completed; SANnav UI shows "Services Starting..."
  - 13:00: SANnav UI returns 502 Bad Gateway; login page not loading
  - 13:05: SSH: sannav-admin status shows "sannav-api" service in "Stopped" state
Steps already taken:
  - Did NOT restart the sannav-api service (awaiting TAC guidance)
  - Did NOT make any zone changes
  - sannav-journal: "FATAL: relation 'sannav.audit_log' does not exist" repeated
Blast radius: SANnav UI completely unavailable; zone changes not possible; fabric health monitoring blind
```

---

## How to Open the SR on support.broadcom.com

1. Go to **support.broadcom.com** and sign in with your Broadcom account.

2. Click **Open a Support Request**.

3. Under **Product Group**, select **Brocade Storage Networking** → **SANnav Management Portal**.

4. Under **Version**, select your SANnav version from Step 1.

5. Under **Severity**, select:
   - **Severity 1 — Critical**: SANnav UI completely unreachable; fabric management unavailable; zone changes impossible; switch discovery has stopped for all fabrics; no workaround
   - **Severity 2 — High**: Zone change operations failing; discovery partially working; SANnav UI accessible but specific operations fail; switch telemetry missing
   - **Severity 3 — Medium**: Single switch not discovered; specific feature broken; report generation failing; workaround exists
   - **Severity 4 — Low**: How-to question, pre-upgrade planning, feature question

6. In the **Summary** field: product + symptom + scope. Example: `SANnav 2.3.0a — UI inaccessible after upgrade from 2.2.0, sannav-api service stopped, 20 switches unmanaged`.

7. In the **Description** field, paste:
   - SANnav version and appliance resource state from Step 1
   - The journal error from Step 3 (the FATAL or ERROR line)
   - FOS versions across the fabric
   - The timeline from Step 6

8. Under **Attachments**, upload:
   - The SANnav support bundle from Step 2
   - The journalctl log from Step 3
   - supportsave archives from affected switches (Step 4)
   - The audit log CSV from Step 5

9. Click **Submit**. You receive a case number immediately.

10. **Severity 1 only:** call Broadcom TAC after submission:
    - North America: +1 877-486-9273 (24×7 for Severity 1)
    - EMEA: +44 (0)3453 700 100
    - State "Severity 1 — SANnav Management Portal down, 20 switches unmanaged, case XXXXXXXX" at the start of the call.

---

## Escalation Path

![Brocade SANnav — Escalation — Diagram](../../../../assets/san-brocade-sannav-troubleshooting-escalation-diagram.svg)

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Restart the SANnav service during a failed upgrade | An incomplete restart during upgrade recovery can corrupt the SANnav database, making recovery impossible without a full redeploy | Wait for TAC to review the journalctl log before any service restart |
| Push zone changes to switches during a SANnav incident | Zone changes pushed while SANnav is partially available can be committed to the switch but not recorded in the SANnav database, causing a configuration drift | Freeze all zone changes until SANnav is fully operational and confirmed in sync with the fabric |
| Delete the SANnav database directory | The database at `/opt/brocade/sannav/postgres/data/` contains historical fabric state; deleting it makes DB-level recovery impossible | Only delete if TAC explicitly instructs, after they have confirmed the data cannot be recovered |
| Change switch SNMP credentials or SSH credentials during the case | Changing credentials mid-case breaks SANnav's connection to the switches and changes the auth state TAC is diagnosing | Hold all credential changes until TAC confirms the issue is not auth-related |
| Upgrade SANnav again immediately after a failed upgrade | A second upgrade on a partially failed state may push the SANnav database into an unrecoverable mixed-version schema | Let TAC examine the failed upgrade log before any retry |
| Power off the SANnav VM during the investigation | Removes the ability for TAC to access live state via SSH; in-memory diagnostic data is lost | Request a controlled shutdown from TAC if a VM restart is needed |

---

## Useful Commands for Case Updates

```bash
# SSH to SANnav appliance as admin — paste these into every case update

# SANnav version
sannav version

# All service states
sannav-admin status

# Database status
sannav-admin db-status

# Disk space
df -h /opt/brocade/sannav

# Recent journal errors
sudo journalctl -u sannav --no-pager -n 200 | grep -i "error\|fatal\|exception"

# Resource state
free -h && uptime
```


```text title="Expected output"
SANnav Version: 2.3.1 Build 2024.01.15
SANnav Admin Version: 2.3.1

Service Status:
  sannav-core         RUNNING (pid 4821)
  sannav-api          RUNNING (pid 4823)
  sannav-collector    RUNNING (pid 4825)
  sannav-postgres     RUNNING (pid 4819)
  sannav-elasticsearch RUNNING (pid 4827)

Database Status:
  PostgreSQL: HEALTHY
  Last Backup: 2024-01-18 03:45:22 UTC
  Replication Status: SYNCED
  Connection Pool: 45/100 active

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda3      500G  287G  213G  58% /opt/brocade/sannav

Jan 18 14:32:11 sannav-prod sannav-collector[4825]: ERROR Failed to connect to fabric switch 10.20.15.44
Jan 18 14:28:03 sannav-prod sannav-api[4823]: EXCEPTION NullPointerException in fabric discovery task
Jan 18 13:55:47 sannav-prod sannav-core[4821]: ERROR Timeout waiting for elasticsearch cluster health

              total        used        free      shared  buff/cache   available
Mem:            31Gi       18Gi       8.2Gi      512Mi       4.8Gi       12Gi
Swap:           16Gi      2.1Gi       14Gi
 14:45:22 up 47 days, 3:22, 2 users, load average: 2.14, 1.87, 1.92
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sudo: journalctl: command not found` | Use `journalctl` without `sudo` prefix or verify the user has passwordless sudo configured in `/etc/sudoers`. |
    | `df: /opt/brocade/sannav: No such file or directory` | Verify SANnav is installed in the correct path with `ls -d /opt/brocade/sannav` or check mount points with `mount | grep brocade`. |
---

## Support SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| Sev 1 — Critical | SANnav down; zone management unavailable; all discovery stopped | < 30 min (24×7) |
| Sev 2 — High | Zone push failing; discovery partially working; specific operation broken | < 2 hours (24×7) |
| Sev 3 — Medium | Single switch not discovered; specific feature broken; workaround exists | < 8 hours |
| Sev 4 — Low | How-to, planning, compatibility question | Next business day |

---

## See also

- [SANnav — Diagnostics](../diagnostics/)
- [SANnav — Common Issues](../common-issues/)

---

## Verify resolution

- Browse to the SANnav UI at `https://<sannav-ip>/` and confirm the login page loads
- Log in and navigate to **Inventory → Switches** — all previously discovered switches appear as Reachable
- Navigate to **Zoning** and confirm zone changes can be pushed to the fabric (test with a non-production fabric or create a dummy zone)
- Run `sannav-admin status` on the appliance and confirm all services show Running
- Check the **Alerts** view for any critical alerts on the SANnav appliance itself
- Monitor for 15 minutes to confirm discovery remains active and no services enter a failed state
