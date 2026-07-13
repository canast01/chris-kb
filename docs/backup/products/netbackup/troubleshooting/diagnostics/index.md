---
tags:
  - netbackup
  - troubleshooting
search:
  boost: 1.5
description: "NetBackup diagnostic commands: query failed jobs with bpdbjobs, check storage unit capacity with bpstulist and nbdevquery, verify policy and client..."
---
# NetBackup — Diagnostics

<div class="kb-summary">
NetBackup diagnostic commands: query failed jobs with bpdbjobs, check storage unit capacity with bpstulist and nbdevquery, verify policy and client config, increase verbose logging with bpsetconfig, check catalog consistency, and generate the nbsupport bundle for Veritas cases.

*Applies to: NetBackup 10.x on Linux master/media servers*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "bpdbjobs -jobid id -report\nRead exit code and error text" {shape: rectangle}
D: "bpstulist -U\nnbdevquery -listdp -stype PureDisk" {shape: rectangle}
E: "Check policy client list\nbppllist policyname -L" {shape: rectangle}
F: "bpdbm -consistency -verbose\nCheck PostgreSQL on master" {shape: rectangle}
G: "bplist -C client -t 0 -l\nVerify image exists and not expired" {shape: rectangle}
H: "H" {shape: rectangle}
I: "ping media-server\nnetstat -an | grep 1556" {shape: rectangle}
J: "Check media server status\nnbemmcmd -listhosts -machinetype media" {shape: rectangle}
K: "Check bpcd on client\nTest client-server connectivity" {shape: rectangle}
L: "vxlogview -o 118 -d 24h\nCheck nbjm log for detail" {shape: rectangle}
M: "Check MSDP health\ncacontrol --dsstat" {shape: rectangle}
N: "bpplschedrep policyname\nVerify schedule and backup window" {shape: rectangle}
O: "Check master disk and PostgreSQL\ndu -sh /usr/openv/netbackup/db" {shape: rectangle}
P: "Adjust retention or rerun\nbpexpdate to extend if needed" {shape: rectangle}
Q: "Collect nbsupport bundle\nfor Veritas SR" {shape: rectangle}
A: "NetBackup Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
H -> I
H -> J
H -> K
H -> L
D -> M
E -> N
F -> O
G -> P
I -> Q
J -> Q
K -> Q
L -> Q
M -> Q
N -> Q
O -> Q
P -> Q
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_failed_jobs: "Step 1 — Check failed jobs" {shape: rectangle}
step_2_check_storage_unit_and_pool_c: "Step 2 — Check storage unit and pool capacity" {shape: rectangle}
step_3_check_policy_and_client_confi: "Step 3 — Check policy and client configuration" {shape: rectangle}
step_4_check_media_server_status_and: "Step 4 — Check media server status and catalog" {shape: rectangle}
step_5_read_vxul_logs: "Step 5 — Read VxUL logs" {shape: rectangle}
step_6_increase_verbose_logging_temp: "Step 6 — Increase verbose logging temporarily" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_failed_jobs: investigate
symptom -> step_2_check_storage_unit_and_pool_c: investigate
symptom -> step_3_check_policy_and_client_confi: investigate
symptom -> step_4_check_media_server_status_and: investigate
symptom -> step_5_read_vxul_logs: investigate
symptom -> step_6_increase_verbose_logging_temp: investigate
step_1_check_failed_jobs -> resolution
step_2_check_storage_unit_and_pool_c -> resolution
step_3_check_policy_and_client_confi -> resolution
step_4_check_media_server_status_and -> resolution
step_5_read_vxul_logs -> resolution
step_6_increase_verbose_logging_temp -> resolution
```

## Before you begin

- **Access:** NetBackup admin role on the master server; root or sudo on Linux master/media servers
- **Gather first:** the failed job ID (from Admin Console or `bpdbjobs`), the exit code, the policy name, and the affected client hostname
- **Scope:** confirm whether the failure affects one client, one policy, one media server, or all backups
- **Exit codes:** NetBackup exit codes are specific — always look up the exact code in the Veritas documentation or `man bpdbjobs` before drawing conclusions

---

## Step 1 — Check failed jobs

```bash
# List all failed jobs in the last 24 hours
/usr/openv/netbackup/bin/admincmd/bpdbjobs -report -hoursago 24 -state failed
# Output: JobId, Type, State, Status, Policy, Schedule, Client, StartTime, EndTime

# Get detailed report for a specific job
/usr/openv/netbackup/bin/admincmd/bpdbjobs -jobid <job-id> -report
# Shows: every step, exit code, error message text, media server used, storage unit

# Common exit codes:
# 0    = successful
# 1    = partially successful
# 13   = file read failed (client-side permission or agent issue)
# 58   = can't connect to client (network, bpcd service)
# 96   = unable to allocate new media (no media available in pool)
# 196  = network connection broken to media server
# 213  = no storage units available for policy

# View all active jobs
/usr/openv/netbackup/bin/admincmd/bpdbjobs -report -hoursago 1 -state active
```


```text title="Expected output"
JobId,Type,State,Status,Policy,Schedule,Client,StartTime,EndTime
2847291,Backup,Failed,13,PROD_DB_DAILY,db_full_0200,db-prod-01.corp.local,2024-01-15 02:15:33,2024-01-15 02:47:22
2847289,Backup,Failed,58,CORP_FILES,incremental_0100,fileserver-02.corp.local,2024-01-15 01:30:44,2024-01-15 01:45:19
2847285,Backup,Failed,96,ARCHIVE_WEEKLY,weekly_sun_0000,backup-client-07.corp.local,2024-01-14 23:55:12,2024-01-15 00:22:08
2847279,Backup,Failed,213,EXCHANGE_2019,hourly_0300,exch-mb-01.corp.local,2024-01-14 21:10:05,2024-01-14 21:18:47

JobId: 2847291
Policy: PROD_DB_DAILY
Client: db-prod-01.corp.local
Status: 13 (file read failed)
Media Server: nbk-media-01.corp.local
Storage Unit: SU_DISK_POOL_01
Start Time: 2024-01-15 02:15:33
End Time: 2024-01-15 02:47:22
Exit Code: 13
Error Message: Cannot read file /var/lib/mysql/ibdata1 - Permission denied on client

JobId,Type,State,Status,Policy,Schedule,Client,StartTime,EndTime
2847295,Backup,Active,0,PROD_DB_DAILY,db_full_0200,db-prod-02.corp.local,2024-01-15 14:22:11,(in progress)
2847294,Backup,Active,0,CORP_FILES,incremental_0100,fileserver-03.corp.local,2024-01-15 14:18:47,(in progress)
2847293,Backup,Active,0,VMWARE_PROD,vm_backup_1400,esx-cluster-01.corp.local,2024-01-15 14:05:33,(in progress)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bpdbjobs: command not found` | Verify NetBackup is installed and add `/usr/openv/netbackup/bin/admincmd` to your PATH or use the full path. |
    | `Error: Cannot connect to database` | Ensure the NetBackup database service is running with `bpdbm status` and check connectivity to the master server. |
    | `Error: Invalid job ID <job-id>` | Use `bpdbjobs -report` without filters first to list valid job IDs, then substitute the actual numeric ID. |
---

## Step 2 — Check storage unit and pool capacity

```bash
# List all storage units with type, media server, and high watermark
/usr/openv/netbackup/bin/admincmd/bpstulist -U
# Columns: STU Name, Storage Type, Media Server, Free Space, Max MPX, High Watermark
# Problem: Free Space 0% or near High Watermark limit

# Check MSDP / AdvancedDisk pool utilization
/usr/openv/netbackup/bin/admincmd/nbdevquery -listdp -stype PureDisk -U
# Shows: disk pool name, total capacity, used capacity, available

# MSDP pool detailed health check
cacontrol --dsstat -d /msdp/data/dp1
# Expected: Status = Active; shows dedup ratio and throughput

# Check MSDP fingerprint database health
cacontrol --dbstat
# Expected: no errors; shows FP DB size

# List tape media by pool and status
/usr/openv/netbackup/bin/admincmd/vmquery -b -pn <volume-pool-name>
# Status: Active, Full, Frozen (frozen media = error; cannot be written)

# Check tape drives in robot
/usr/openv/netbackup/bin/admincmd/tpconfig -d
# Shows: drive name, serial, status (Up/Down)
```


```text title="Expected output"
Storage Unit List:
STU Name              Storage Type    Media Server      Free Space  Max MPX  High Watermark
stu-primary-disk     AdvancedDisk    mserver01.corp    45%         4        80%
stu-secondary-disk   AdvancedDisk    mserver02.corp    12%         4        80%
stu-tape-pool-1      Tape            mserver01.corp    89%         8        90%

Disk Pool Query:
Pool Name             Total Capacity  Used Capacity   Available
dp1-production        50.0 TB         42.3 TB         7.7 TB
dp2-archive           100.0 TB        98.5 TB         1.5 TB

MSDP Pool Health (dp1):
Status = Active
Dedup Ratio: 3.2:1
Throughput: 245 MB/s
Fingerprint DB Size: 18.4 GB

Fingerprint Database Status:
DB Status: Healthy
FP DB Size: 18.4 GB
Last Verification: 2024-01-15 03:22:15

Tape Media Pool (backup-monthly):
Media ID          Status    Capacity  Used      Pool Name
CLN001            Active    800 GB    650 GB    backup-monthly
CLN002            Full      800 GB    800 GB    backup-monthly
CLN003            Frozen    800 GB    750 GB    backup-monthly

Tape Drive Configuration:
Drive Name        Serial Number    Status    Drive Type
TLD1              SN-LTO8-0042     Up        LTO-8
TLD2              SN-LTO8-0043     Down      LTO-8
TLD3              SN-LTO9-0051     Up        LTO-9
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bpstulist: command not found` | Verify NetBackup is installed and `/usr/openv/netbackup/bin/admincmd/` is in PATH or use the full path. |
    | `cacontrol: error accessing /msdp/data/dp1: No such file or directory` | Confirm the MSDP pool mount point exists and is mounted; check `/etc/fstab` or `mount | grep msdp`. |
    | `vmquery: Media pool <volume-pool-name> not found` | Replace `<volume-pool-name>` with an actual pool name from `bpstulist` output (e.g., `backup-monthly`). |
---

## Step 3 — Check policy and client configuration

```bash
# List all policies with schedule and client detail
/usr/openv/netbackup/bin/admincmd/bppllist -allpolicies -L

# Check a specific policy schedule (backup windows, frequency, type)
/usr/openv/netbackup/bin/admincmd/bpplschedrep <policy-name>

# List catalog images available for a client
/usr/openv/netbackup/bin/admincmd/bplist -C <client-hostname> -t 0 -l
# -t 0 = any backup type; -l = long format with date and size

# Check registered clients and their attributes
/usr/openv/netbackup/bin/admincmd/bpplclients <policy-name> -L

# Verify policy is active and has valid clients
/usr/openv/netbackup/bin/admincmd/bppllist <policy-name> -L | grep -E "ACTIVE|CLIENT|SCHED"
```


```text title="Expected output"
Policy Name: prod-daily-backup
Policy Type: Standard
Active: Yes
Client: web-server-01.corp.local
Client: db-server-02.corp.local
Client: fileserver-03.corp.local
Schedule Name: weekday-incremental
Schedule Type: Incremental
Frequency: Every day at 22:00
Retention: 30 days
...

Policy: prod-daily-backup
Schedule: weekday-incremental
Window Start: 22:00 EST
Window End: 06:00 EST
Frequency: Daily (Mon-Sun)
Type: Incremental
Last Run: 2024-01-15 22:15:33
Next Run: 2024-01-16 22:00:00

Backup Images for Client: web-server-01.corp.local
Image ID: 1705363200 | Date: 2024-01-15 22:00:00 | Size: 487.3 GB | Status: COMPLETED
Image ID: 1705276800 | Date: 2024-01-14 22:00:00 | Size: 512.1 GB | Status: COMPLETED
Image ID: 1705190400 | Date: 2024-01-13 22:00:00 | Size: 498.7 GB | Status: COMPLETED
...

Registered Clients for Policy: prod-daily-backup
Client: web-server-01.corp.local | OS: Linux | Enabled: Yes
Client: db-server-02.corp.local | OS: Linux | Enabled: Yes
Client: fileserver-03.corp.local | OS: Windows | Enabled: Yes

ACTIVE: Yes
CLIENT: web-server-01.corp.local
CLIENT: db-server-02.corp.local
CLIENT: fileserver-03.corp.local
SCHED: weekday-incremental
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bppllist: policy 'prod-daily-backup' not found` | Verify the policy name spelling and that it exists in the NetBackup master server configuration. |
    | `bplist: client 'web-server-01.corp.local' is not registered` | Register the client in the NetBackup admin console or use `bpplclients` to add it to the policy. |
    | `Error: NetBackup master server is not running` | Start the NetBackup services on the master server with `/usr/openv/netbackup/bin/bpup -start`. |
---

## Step 4 — Check media server status and catalog

```bash
# List all registered hosts in EMM (Enterprise Media Manager)
/usr/openv/netbackup/bin/admincmd/nbemmcmd -listhosts

# Check media server status specifically
/usr/openv/netbackup/bin/admincmd/nbemmcmd -listhosts -machinetype mediaserver
# Expected: all media servers with Status = UP

# Re-register a media server if missing
/usr/openv/netbackup/bin/admincmd/nbemmcmd -updatehost -machinename <media-server> -machinetype mediaserver

# Check catalog database consistency
/usr/openv/netbackup/bin/admincmd/bpdbm -consistency -verbose
# Expected: no inconsistencies reported

# Check catalog disk usage
du -sh /usr/openv/netbackup/db/
# NetBackup catalog PostgreSQL database; should have > 20% free space on the partition

# Test network connectivity to media server
ping -c 10 <media-server>
traceroute <media-server>

# Verify vnetd port 1556 is listening on master and media
netstat -tulnp | grep 1556
```


```text title="Expected output"
Host Name                          Machine Type         Status
================================================================================
master-01.corp.local               master               UP
media-srv-01.corp.local            mediaserver          UP
media-srv-02.corp.local            mediaserver          UP
media-srv-03.corp.local            mediaserver          UP
client-backup-01.corp.local        client               UP

Host Name                          Machine Type         Status
================================================================================
media-srv-01.corp.local            mediaserver          UP
media-srv-02.corp.local            mediaserver          UP
media-srv-03.corp.local            mediaserver          UP

(no output — command completes silently)

4.2G	/usr/openv/netbackup/db/

PING media-srv-01.corp.local (192.168.10.45) 56(84) bytes of data.
64 bytes from media-srv-01.corp.local (192.168.10.45): icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from media-srv-01.corp.local (192.168.10.45): icmp_seq=2 ttl=64 time=2.41 ms
...
10 packets transmitted, 10 received, 0% packet loss, time 9012ms

tcp        0      0 0.0.0.0:1556            0.0.0.0:*               LISTEN      8934/vnetd
tcp6       0      0 :::1556                 :::*                    LISTEN      8934/vnetd
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nbemmcmd: command not found` | Verify NetBackup is installed and add `/usr/openv/netbackup/bin/admincmd` to PATH, or use the full path to the binary. |
    | `Host <media-server> is not registered in EMM` | Run `nbemmcmd -updatehost -machinename <media-server> -machinetype mediaserver` to register the missing media server. |
    | `netstat: command not found` | Use `ss -tulnp | grep 1556` instead, as netstat is deprecated on modern Linux systems. |
---

## Step 5 — Read VxUL logs

```bash
# VxUL logs location (Unified Logging)
ls /usr/openv/logs/

# Query logs by Origin ID (OID) and time range
# OID 117 = nbpem (policy execution manager — job dispatch)
vxlogview -o 117 -d 24h -t "DEBUG|WARNING|ERROR" | less

# OID 118 = nbjm (job manager — data transfer)
vxlogview -o 118 -d 24h -t "WARNING|ERROR" | less

# OID 119 = nbstserv (storage service — STU and media)
vxlogview -o 119 -d 24h -t "ERROR" | less

# OID 143 = nbwebsvc (NetBackup web service — API)
vxlogview -o 143 -d 24h -t "ERROR" | less

# Legacy log directories (pre-VxUL; create directories if debugging)
mkdir -p /usr/openv/netbackup/logs/bpcd     # client daemon
mkdir -p /usr/openv/netbackup/logs/bpbrm    # backup/restore manager
mkdir -p /usr/openv/netbackup/logs/bprd     # request daemon
mkdir -p /usr/openv/netbackup/logs/bpdm     # disk manager
```


```text title="Expected output"
audit.log
bprd.log
bpbrm.log
bpcd.log
bpdm.log
vxlogd.log
vxul.log

[OID:117 nbpem] 2024-01-15 14:32:18 DEBUG Job dispatch initiated for policy PROD_DAILY_BACKUP
[OID:117 nbpem] 2024-01-15 14:33:02 WARNING Schedule window exceeded by 45 seconds
[OID:117 nbpem] 2024-01-15 14:35:41 ERROR Failed to dispatch job 12847: insufficient media resources
[OID:117 nbpem] 2024-01-15 15:12:09 DEBUG Retry attempt 2 for policy PROD_DAILY_BACKUP
[OID:117 nbpem] 2024-01-15 16:04:33 ERROR Job 12848 terminated: client host unreachable (10.42.18.7)

[OID:118 nbjm] 2024-01-15 14:35:45 WARNING Data transfer rate below threshold: 45 MB/s (expected >100 MB/s)
[OID:118 nbjm] 2024-01-15 14:52:17 ERROR Job 12847 data transfer failed: socket timeout after 300s

[OID:119 nbstserv] 2024-01-15 15:18:33 ERROR STU device /dev/sg5 not responding

[OID:143 nbwebsvc] 2024-01-15 16:22:01 ERROR API request timeout: GET /api/v1/jobs/status (client: 192.168.1.105)

mkdir: created directory '/usr/openv/netbackup/logs/bpcd'
mkdir: created directory '/usr/openv/netbackup/logs/bpbrm'
mkdir: created directory '/usr/openv/netbackup/logs/bprd'
mkdir: created directory '/usr/openv/netbackup/logs/bpdm'
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vxlogview: command not found` | Verify VxUL is installed with `rpm -qa | grep VRTSvxul` and install the VxUL package if missing. |
    | `Permission denied` | Run the vxlogview and mkdir commands with `sudo` or as root user. |
    | `No such file or directory: /usr/openv/logs/` | Confirm NetBackup is installed in the default location or adjust the path to match your installation directory (check `echo $NB_INSTALL_DIR`). |
---

## Step 6 — Increase verbose logging temporarily

```bash
# Set verbose level to 3 (moderate) on master server
/usr/openv/netbackup/bin/admincmd/bpsetconfig -h <master-server> <<'EOF'
VERBOSE = 3
EOF
# Valid range: 0 (default) to 5 (maximum — very verbose; use briefly)

# After reproducing the issue, revert to default
/usr/openv/netbackup/bin/admincmd/bpsetconfig -h <master-server> <<'EOF'
VERBOSE = 0
EOF

# Set on a specific media server
/usr/openv/netbackup/bin/admincmd/bpsetconfig -h <media-server> <<'EOF'
VERBOSE = 3
EOF
```


```text title="Expected output"
Configuration updated successfully on master-server
VERBOSE set to 3
Configuration updated successfully on master-server
VERBOSE set to 0
Configuration updated successfully on media-server-01
VERBOSE set to 3
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bpsetconfig: invalid host <master-server>` | Replace `<master-server>` with the actual FQDN or IP address of your NetBackup master server (e.g., `nbmaster.corp.local`). |
    | `bpsetconfig: permission denied` | Run the command as root or with sudo, as NetBackup configuration changes require elevated privileges. |
    | `bpsetconfig: connection timeout to <media-server>` | Verify the media server is reachable and the NetBackup daemons are running with `bpps -a` on the target host. |
---

## Step 7 — Generate nbsupport bundle for Veritas SR

```bash
# Generate diagnostic bundle on the master server
/usr/openv/netbackup/bin/support/nbsupport
# Output: /tmp/nbsupport_<hostname>_<timestamp>.tar.gz
# Includes: VxUL logs, config files, job history, storage unit config

# Include job detail for the failing job in the SR
/usr/openv/netbackup/bin/admincmd/bpdbjobs -jobid <job-id> -report \
  > /tmp/job_${job_id}_report.txt

# Include storage unit status
/usr/openv/netbackup/bin/admincmd/bpstulist -U > /tmp/stu_status.txt
/usr/openv/netbackup/bin/admincmd/nbdevquery -listdp -stype PureDisk -U >> /tmp/stu_status.txt

# Upload to Veritas support portal with:
# - nbsupport .tar.gz file
# - Job ID, exit code, and time window of the issue
# - Policy name, client name, and storage unit name
```


```text title="Expected output"
NetBackup Support Utility
Gathering diagnostic information...
Collecting VxUL logs from /usr/openv/netbackup/logs/
Collecting configuration files...
Collecting job history...
Collecting storage unit configuration...
Creating archive...
Diagnostic bundle created: /tmp/nbsupport_nbmaster01_20240115_143022.tar.gz
Bundle size: 287 MB

Job ID 12847 Report:
Job ID: 12847
Policy: DailyBackup_Finance
Client: finance-db-01.corp.local
Schedule: Weekly-Full
Status: FAILED
Start Time: 01/15/2024 02:00:15
End Time: 01/15/2024 02:47:33
Exit Code: 1
Elapsed Time: 47 minutes 18 seconds

Storage Unit Status:
Storage Unit Name          Type          Status        Capacity
PureDisk_Primary           PureDisk      ONLINE        2.1 TB / 5.0 TB
PureDisk_Secondary         PureDisk      ONLINE        1.8 TB / 5.0 TB
Disk_Archive_01            Disk          ONLINE        847 GB / 1.0 TB
Disk_Archive_02            Disk          DEGRADED      156 GB / 1.0 TB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bpdbjobs: Job ID <job-id> not found` | Replace `<job-id>` with the actual numeric job ID from the failed backup job. |
    | `Permission denied: /tmp/nbsupport_*.tar.gz` | Run the nbsupport command as root or the netbackup service user (typically `netbackup`). |
    | `bpstulist: command not found` | Ensure you are running these commands on the NetBackup master server and the PATH includes `/usr/openv/netbackup/bin/admincmd/`. |
---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| VxUL (nbpem / nbjm) | `vxlogview -o 117 -d 24h` / `vxlogview -o 118 -d 24h` | Job dispatch and data transfer errors |
| Legacy logs | `/usr/openv/netbackup/logs/<daemon>/` | Pre-VxUL daemon logs |
| Catalog | `/usr/openv/netbackup/db/` (PostgreSQL) | Catalog inconsistency and size issues |
| bpdbjobs job report | `bpdbjobs -jobid <id> -report` | Step-by-step job trace with exit code |
| MSDP health | `cacontrol --dsstat` | Dedup pool health and fingerprint DB |
| Windows Event Log | Get-EventLog Application source NetBackup | Windows NBU errors |

---

## See also

- [NetBackup — Common Issues](../common-issues/)
- [NetBackup — Escalation](../escalation/)
- [NetBackup — Health Checks](../../operations/health-checks/)

## Verify resolution

- `bpdbjobs -report -hoursago 24 -state failed` shows no new failures for the affected policy/client
- `bpstulist -U` shows free space above the high watermark threshold on all affected storage units
- Trigger a manual backup of the affected policy: confirm it completes with exit code 0
- `vxlogview -o 118 -d 1h -t "ERROR"` shows no new errors in the last hour
