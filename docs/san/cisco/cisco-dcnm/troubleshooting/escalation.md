---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
description: "How to escalate Cisco DCNM (Data Center Network Manager) issues to Cisco TAC: what data to collect, how to generate the DCNM support bundle and MDS show..."
---
# Cisco DCNM — Escalation

<div class="kb-summary">
How to escalate Cisco DCNM (Data Center Network Manager) issues to Cisco TAC: what data to collect, how to generate the DCNM support bundle and MDS show tech-support, step-by-step case creation on case.cisco.com, and the escalation path when progress stalls.

*Applies to: Cisco DCNM 11.x — standalone VM or Native HA deployment managing MDS / Nexus SAN fabrics*
</div>
![Cisco DCNM — Escalation](../../../../assets/san-cisco-cisco-dcnm-troubleshooting-escalation.svg)




---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
preescalation_selfcheck: "Pre-Escalation Self-Check" {shape: rectangle}
stepbystep_data_collection: "Step-by-Step Data Collection" {shape: rectangle}
how_to_open_the_sr_on_caseciscocom: "How to Open the SR on case.cisco.com" {shape: rectangle}
escalation_path: "Escalation Path" {shape: rectangle}
what_not_to_do: "What NOT to Do" {shape: rectangle}
useful_commands_for_case_updates: "Useful Commands for Case Updates" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> preescalation_selfcheck: investigate
symptom -> stepbystep_data_collection: investigate
symptom -> how_to_open_the_sr_on_caseciscocom: investigate
symptom -> escalation_path: investigate
symptom -> what_not_to_do: investigate
symptom -> useful_commands_for_case_updates: investigate
preescalation_selfcheck -> resolution
stepbystep_data_collection -> resolution
how_to_open_the_sr_on_caseciscocom -> resolution
escalation_path -> resolution
what_not_to_do -> resolution
useful_commands_for_case_updates -> resolution
```

## Before you begin

- **Access required:** Root or admin SSH access to the DCNM VM; DCNM admin web console credentials; Cisco CCO account at case.cisco.com; credentials for each managed MDS or Nexus switch
- **Do NOT restart DCNM services** before collecting the support bundle — a restart clears the in-memory service state and logs that TAC needs to diagnose the issue; collect the bundle first, then restart if directed by TAC
- **Do NOT make zone changes** during an active DCNM incident — if DCNM is partially functional, zone pushes in an unstable state can corrupt the zone database or leave switches in a mixed state
- **Do NOT upgrade DCNM mid-incident** — do not attempt a DCNM upgrade to resolve the issue unless explicitly directed by TAC with a targeted bugfix version

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| DCNM version | `cat /var/dcnm/version` | Note full version (e.g., 11.5.4.0) |
| Service state | `appmgr status` | All services Running |
| Database state | `appmgr database-status` | Database running; no errors |
| Disk space | `df -h` | DCNM data volumes below 80% used |
| Memory | `free -h` | Sufficient free memory; no OOM in `dmesg` |
| Java heap | Run: see Step 3 | GC utilization below 95% |
| Managed switch reachability | DCNM UI → Switches | All managed MDS switches in Manageable state |
| Fabric replication | DCNM UI → Fabrics | Fabrics in normal sync state |

---

## Step-by-Step Data Collection

### 1. Get the DCNM version and deployment type

```bash
# SSH to the DCNM VM as root or admin

# DCNM version string
cat /var/dcnm/version

# For Native HA: check which node is primary
appmgr ha-status

# DCNM deployment mode
appmgr show-deployment-mode
```


```text title="Expected output"
DCNM Version: 12.1.2.0 (Build 12.1.2.0.20231015)

Primary Node: dcnm-node-01.example.com (192.168.1.100)
Secondary Node: dcnm-node-02.example.com (192.168.1.101)
HA Status: HEALTHY
Sync Status: IN_SYNC
Last Sync Time: 2024-01-15 14:32:18 UTC

Deployment Mode: Native HA
Active Controller: dcnm-node-01
Standby Controller: dcnm-node-02
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: /var/dcnm/version: No such file or directory` | Verify DCNM is installed by checking `/opt/dcnm/version` or running `dcnm --version` instead. |
    | `appmgr: command not found` | SSH directly to the DCNM VM and ensure you are logged in as root; appmgr is only available on the DCNM appliance itself, not remotely. |
    | `HA Status: UNHEALTHY - Node dcnm-node-02 unreachable` | Check network connectivity between nodes and verify both DCNM services are running with `systemctl status dcnm-*`. |
### 2. Collect the DCNM support bundle

```bash
# This is the primary artifact for Cisco TAC — collect BEFORE any restart
# Run as root; the bundle takes 5–10 minutes to generate

/usr/local/cisco/dcm/dcnm/bin/collect-support-bundle.sh \
  --output /tmp/dcnm-support-$(date +%Y%m%d%H%M).tar.gz

# Verify the bundle was created
ls -lh /tmp/dcnm-support-*.tar.gz

# Transfer to your workstation for upload to the TAC case
scp root@<dcnm-vm>:/tmp/dcnm-support-$(date +%Y%m%d%H%M).tar.gz ./
```


```text title="Expected output"
Collecting DCNM support bundle...
Gathering system logs... [████████████████████] 100%
Gathering database diagnostics... [████████████████████] 100%
Gathering fabric inventory... [████████████████████] 100%
Gathering configuration snapshots... [████████████████████] 100%
Bundle creation completed successfully.
Support bundle saved to: /tmp/dcnm-support-202501151430.tar.gz

-rw-r--r-- 1 root root 847M Jan 15 14:30 /tmp/dcnm-support-202501151430.tar.gz

root@dcnm-vm:/tmp/dcnm-support-202501151430.tar.gz                100% 847MB   12.4MB/s   01:08
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `/usr/local/cisco/dcm/dcnm/bin/collect-support-bundle.sh: Permission denied` | Run the command with `sudo` or as the root user directly. |
    | `tar: Error is not recoverable: exiting now` | Ensure `/tmp` has at least 2GB of free space using `df -h /tmp` and clear old bundles if needed. |
    | `scp: command not found` | Install OpenSSH client on your workstation with `apt-get install openssh-client` (Ubuntu/Debian) or `brew install openssh` (macOS). |
### 3. Capture DCNM service state and resource snapshot

```bash
# All DCNM service states
appmgr status > /tmp/dcnm-services-$(date +%Y%m%d).txt

# Database health
appmgr database-status >> /tmp/dcnm-services-$(date +%Y%m%d).txt

# OS resources (disk, memory, CPU)
df -h >> /tmp/dcnm-services-$(date +%Y%m%d).txt
free -h >> /tmp/dcnm-services-$(date +%Y%m%d).txt
uptime >> /tmp/dcnm-services-$(date +%Y%m%d).txt

# Java heap utilization for the DCNM server process
DCNM_PID=$(ps aux | grep "[d]cnm-server" | awk '{print $2}' | head -1)
if [ -n "$DCNM_PID" ]; then
  jstat -gcutil "${DCNM_PID}" 1s 10 >> /tmp/dcnm-services-$(date +%Y%m%d).txt
fi

# DCNM application log tail (most recent errors)
tail -500 /var/log/dcnm/dcnm.log > /tmp/dcnm-log-tail-$(date +%Y%m%d).txt 2>/dev/null || \
  journalctl -u dcnm --since "4 hours ago" > /tmp/dcnm-log-tail-$(date +%Y%m%d).txt
```


```text title="Expected output"
S.No  Service Name                    Admin State    Oper State
1     dcnm-server                     UP             UP
2     dcnm-scheduler                  UP             UP
3     dcnm-maapi                      UP             UP
4     dcnm-ha-peer                    UP             DOWN
5     postgres                        UP             UP

Database Status: HEALTHY
Replication Lag: 0 ms
Last Backup: 2024-01-15 03:45:22 UTC

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1      500G  287G  213G  58% /
/dev/sdb1      2.0T  1.8T  200G  90% /var/log

              total        used        free      shared  buff/cache   available
Mem:           64Gi        48Gi        8.2Gi      512Mi        7.8Gi        15Gi
Swap:          16Gi       2.1Gi        13Gi

 10:42:23 up 127 days, 14:33,  2 users,  load average: 2.14, 1.87, 1.92

 S0     S1     E     O      M1     M2   CCS    CCSU    EU     TT   PTGU   GCT
 0.00  15.23  42.18  8.92  58.34  22.11  0.00   0.00  12.45  145.2  0.0   2.341
 0.00  16.01  41.95  9.15  59.12  21.88  0.00   0.00  12.67  148.9  0.0   2.356
 0.00  15.87  42.34  8.78  58.67  22.33  0.00   0.00  12.51  146.5  0.0   2.348

2024-01-15T10:38:45.123Z INFO  [dcnm-server] Fabric sync completed for fabric-prod-01
2024-01-15T10:39:12.456Z WARN  [dcnm-scheduler] Task queue depth: 234 pending jobs
2024-01-15T10:40:01.789Z INFO  [dcnm-maapi] Device 10.48.1.5 reachability confirmed
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `jstat: command not found` | Install the Java Development Kit (JDK) on the DCNM appliance or verify the JAVA_HOME environment variable is set correctly. |
    | `/var/log/dcnm/dcnm.log: No such file or directory` | Confirm the DCNM service is running and the log directory exists; if using systemd-journald exclusively, the fallback to journalctl will capture logs automatically. |
    | `Permission denied` | Run the script with sudo or ensure the user has read access to /var/log/dcnm/ and /proc/[pid]/stat for the DCNM process. |
### 4. Capture database diagnostics

```bash
# Connect to DCNM PostgreSQL and capture key table sizes
psql -U postgres sane -c "
SELECT relname, pg_size_pretty(pg_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_relation_size(relid) DESC
LIMIT 20;" > /tmp/dcnm-db-$(date +%Y%m%d).txt

# Total database sizes
psql -U postgres -c "
SELECT datname, pg_size_pretty(pg_database_size(datname))
FROM pg_database
ORDER BY pg_database_size(datname) DESC;" >> /tmp/dcnm-db-$(date +%Y%m%d).txt
```


```text title="Expected output"
relname                     |    size
-------------------------------------------------+----------
 fabric_device_inventory                        | 2847 MB
 switch_config_history                          | 1923 MB
 interface_statistics                           | 1456 MB
 policy_deployment_log                          | 892 MB
 device_event_log                               | 756 MB
 fabric_topology_cache                          | 634 MB
 vlan_mapping_table                             | 512 MB
 route_table_snapshot                           | 389 MB
 ...
(20 rows)

 datname  |  pg_database_size
----------+-------------------
 sane     | 14 GB
 postgres | 45 MB
 template1| 8 MB
(3 rows)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL: role "postgres" does not exist` | Verify the PostgreSQL superuser exists or use the correct role name with `-U dcnm_user` instead. |
    | `psql: error: database "sane" does not exist` | Confirm the DCNM database name is correct; check with `psql -U postgres -l` to list available databases. |
    | `Permission denied` | Ensure the user running the script has write permissions to `/tmp` or redirect output to a writable directory like `/var/log/dcnm/`. |
### 5. Collect show tech-support from affected MDS switches

```bash
# SSH to each affected MDS switch and run show tech-support
# This is required in addition to the DCNM support bundle

ssh admin@<mds-switch-ip>
show tech-support > /tmp/mds-tech-$(hostname)-$(date +%Y%m%d).txt
exit

# Transfer the tech-support file
scp admin@<mds-switch-ip>:/tmp/mds-tech-*.txt ./
```


```text title="Expected output"
The authenticity of host '192.168.100.45' can't be established.
ECDSA key fingerprint is SHA256:aBcD1234EfGhIjKlMnOpQrStUvWxYz5678+9/0=.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.100.45' (ECDSA) to /etc/ssh/known_hosts.
Password: 
mds-switch-01# show tech-support > /tmp/mds-tech-mds-switch-01-20240115.txt
mds-switch-01# exit
Connection to 192.168.100.45 closed.
mds-tech-mds-switch-01-20240115.txt                    100% |*****| 45678 KB  00:12
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,password).` | Verify the admin account credentials and ensure SSH is enabled on the MDS switch with `show ssh server status`. |
    | `No such file or directory` | Confirm the tech-support file was successfully created on the switch by SSH'ing back and running `ls -la /tmp/mds-tech-*.txt` before attempting the scp transfer. |
### 6. Export the DCNM audit log

In the DCNM UI:
1. Navigate to **Administration** → **Credentials** → **Audit Log**.
2. Set the time range to cover 48 hours before the incident.
3. Click **Export** → **CSV**.
4. Save the file and include it in the TAC case attachment.

### 7. Write the timeline

```text
DCNM version: 11.5.4.0
Deployment: Standalone VM (VMware ESXi 7.0 U3)
VM resources: 16 vCPU, 32 GB RAM, 500 GB disk
Managed fabrics: SAN Fabric A (MDS 9710 x2, MDS 9396T x4), SAN Fabric B (MDS 9396T x2)
Managed switch NX-OS: 8.4(2a) on all MDS switches
Issue first observed: 2026-06-15 14:00 UTC
Last confirmed healthy: 2026-06-15 12:00 UTC
Changes in 24h before the issue:
  - 11:30: DCNM upgraded from 11.5.2 to 11.5.4.0 (upgrade completed successfully per UI)
  - 12:00: DCNM appeared healthy post-upgrade
  - 14:00: All managed switches moved to "Unreachable" state in DCNM; fabric discovery stopped
  - 14:05: appmgr status: sne-service is in "Stopped" state; attempting restart fails
  - 14:10: Disk utilization on /var/lib/pgsql: 95% — database may have run out of space
Steps already taken:
  - Did NOT restart the entire DCNM VM
  - Did NOT make any zone changes
  - Verified MDS switches are reachable via SSH independently — switches operational, only DCNM is down
  - Checked /var/dcnm/version: confirms upgrade applied (11.5.4.0)
Blast radius: All DCNM fabric management unavailable; no zone changes can be pushed; monitoring stopped
```

---

## How to Open the SR on case.cisco.com

1. Go to **case.cisco.com** and sign in with your Cisco CCO account.

2. Click **Create New Case**.

3. Under **Product**, type "Data Center Network Manager" and select **Cisco DCNM**.

4. Enter the DCNM version string from Step 1.

5. Under **Severity**, select:
   - **Severity 1 — Production Down**: DCNM is completely unavailable and no fabric management can be performed; zone changes cannot be pushed to any fabric; a production fabric is degraded and DCNM data is required for recovery
   - **Severity 2 — Major Impact**: DCNM UI is accessible but a core function is broken (zone push failing, fabric discovery stopped for specific fabrics, performance data unavailable); workaround is partial
   - **Severity 3 — Moderate Impact**: DCNM functioning with minor issues; some features not working but fabric management is intact; workaround available
   - **Severity 4 — Minimal Impact**: How-to, DCNM configuration question, best practice, upgrade planning question

6. In the **Summary** field: version + symptom. Example: `DCNM 11.5.4.0 — sne-service stopped after upgrade, all managed switches Unreachable, fabric management unavailable`.

7. In the **Description** field, paste:
   - DCNM version and deployment type (Step 1)
   - `appmgr status` output (Step 3)
   - Key log errors from the DCNM log (Step 3)
   - Database size findings if relevant (Step 4)
   - The timeline from Step 7

8. Under **Attachments**, upload:
   - `dcnm-support-*.tar.gz` from Step 2 (primary artifact)
   - `mds-tech-*.txt` from Step 5 for each affected MDS switch
   - Audit log CSV from Step 6
   - `dcnm-db-*.txt` if database issue is suspected

9. Click **Submit**. You receive a case number immediately.

10. **Severity 1 only:** call Cisco TAC after submission:
    - North America: +1-800-553-2447 (24×7)
    - State "Severity 1 — DCNM completely down, fabric management unavailable, case XXXXXXXX" at the start of the call.

---

## Escalation Path

![Cisco DCNM — Escalation — Diagram](../../../../assets/san-cisco-cisco-dcnm-troubleshooting-escalation-diagram.svg)

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Restart DCNM before collecting the support bundle | A restart clears the in-memory service state and the current log buffer; TAC needs state data from the moment of failure | Run `collect-support-bundle.sh` before any restart; then restart only if TAC directs it |
| Make zone changes while DCNM is unstable | A zone push from an unstable DCNM can push an incomplete zone database to the MDS fabric, leaving switches with mixed active/inactive zone configurations | Freeze all zone changes until DCNM is stable and confirmed healthy |
| Upgrade DCNM to try to resolve the issue | Applying a new DCNM version to an already-broken installation may compound the failure state and make root cause harder to determine | Only upgrade with TAC providing the specific target version and documented procedure |
| Delete DCNM PostgreSQL database files to free disk space | The DCNM databases (sane and pmdb) contain all fabric topology and historical configuration data; deleting them requires a full DCNM rediscovery and configuration rebuild | Expand the disk allocated to the DCNM VM; let TAC identify which tables are safe to archive |
| Reboot the DCNM VM without TAC direction | A VM reboot may recover a hung service but may also mask the root cause; TAC often needs the state before restart | Reboot only on TAC's explicit direction after the support bundle has been collected |
| Remove and re-add managed switches in DCNM | Removing a switch from DCNM management deletes its configuration history; re-adding triggers a full rediscovery that may fail if the underlying issue is on the DCNM side | Let TAC investigate the discovery failure before any switch removal from management |

---

## Useful Commands for Case Updates

```bash
# SSH to DCNM VM — paste into every case update

# DCNM service states
appmgr status

# Disk utilization (watch for /var/lib/pgsql filling up)
df -h

# DCNM service log tail (last 100 lines)
tail -100 /var/log/dcnm/dcnm.log 2>/dev/null || journalctl -u dcnm --since "30 min ago"

# Database running check
appmgr database-status
```


```text title="Expected output"
[dcnm@dcnm-prod-01 ~]$ appmgr status
dcnm-web: running
dcnm-backend: running
dcnm-database: running
dcnm-scheduler: running
dcnm-messaging: running

[dcnm@dcnm-prod-01 ~]$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   32G   15G  68% /
/dev/sda2       100G   87G   10G  89% /var/lib/pgsql
/dev/sda3       200G  145G   48G  74% /opt/dcnm
tmpfs            16G     0   16G   0% /dev/shm

[dcnm@dcnm-prod-01 ~]$ tail -100 /var/log/dcnm/dcnm.log 2>/dev/null || journalctl -u dcnm --since "30 min ago"
2024-01-15 14:32:18 [INFO] DCNM backend initialized successfully
2024-01-15 14:32:45 [INFO] Database connection pool established: 25 connections
2024-01-15 14:33:02 [INFO] Scheduler started: 12 jobs queued
2024-01-15 14:35:17 [WARN] Fabric sync delayed for fabric-prod-dc1 (retry 2/5)
2024-01-15 14:36:01 [INFO] Fabric sync completed for fabric-prod-dc1 in 2847ms

[dcnm@dcnm-prod-01 ~]$ appmgr database-status
Database Status: HEALTHY
PostgreSQL Version: 12.8
Active Connections: 18/25
Replication Status: STREAMING
Last Backup: 2024-01-15 02:00:15 UTC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `appmgr: command not found` | Ensure you are logged into the DCNM VM directly (not a remote host) and that /opt/dcnm/bin is in your PATH. |
    | `/var/log/dcnm/dcnm.log: No such file or directory` | The log file may not exist yet; use `journalctl -u dcnm --since "30 min ago"` instead, or verify the DCNM service started with `systemctl status dcnm`. |
    | `Database Status: UNHEALTHY` | Check PostgreSQL process with `systemctl status postgresql` and verify /var/lib/pgsql has at least 5GB free space using `df -h`. |
---

## Support SLA Reference

| Contract | Severity | Definition | Initial Response SLA |
|---|---|---|---|
| SMARTnet 24×7 | Sev-1 | DCNM completely unavailable; fabric management down | < 1 hour (24×7) |
| SMARTnet 24×7 | Sev-2 | Core function broken; zone push failing; workaround partial | < 2 hours (24×7) |
| SMARTnet 24×7 | Sev-3 | Partial feature loss; workaround available | < 4 hours (business hours) |
| SMARTnet 24×7 | Sev-4 | How-to, general question | Next business day |
| SMARTnet 8×5 | Sev-1 | As above | < 2 hours (business hours) |

---

## See also

- [Cisco DCNM — Diagnostics](../diagnostics/)
- [Cisco DCNM — Common Issues](../common-issues/)

---

## Verify resolution

- Run `appmgr status` and confirm all DCNM services are Running
- Verify the DCNM UI is accessible and all managed MDS switches show Manageable state in the fabric view
- Run a test zone push to a non-production VSAN to confirm zone distribution is working
- Check DCNM UI → Fabrics and confirm all fabrics are in normal sync state
- Run `df -h` and confirm disk utilization is below 80% on all DCNM volumes
- Monitor `appmgr status` over 15 minutes to confirm no services cycle back to a stopped state
