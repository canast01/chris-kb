---
tags:
  - dr
  - troubleshooting
search:
  boost: 1.5
---
# Backup Failures Troubleshooting

<div class="kb-summary">
Backup Failures Troubleshooting reference covering Overview, Failure Classification, Diagnostic Flowchart, Commvault Troubleshooting, NetBackup Troubleshooting and 4 more sections.
</div>

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Overview

Backup failures directly degrade recovery capability. This guide covers failure classification and deep troubleshooting for Veeam Backup & Replication, Commvault, and Veritas NetBackup in enterprise environments. Address failures within the RTO window defined for each protection tier.

---

## Failure Classification

| Failure Type | Typical Symptom | Primary Tool | First Check |
|---|---|---|---|
| Network timeout | Job fails after X minutes; "connection reset" in log | ping, Test-NetConnection | MTU, firewall, proxy bypass |
| Agent error | Guest processing failed; VSS error in job log | Veeam Guest Log; Event Viewer | VSS writers, agent version |
| Repository full | "Not enough space" error; job aborted | df -h; Get-VBRRepository | Free capacity; maintenance mode |
| Snapshot failure | "Failed to create VM snapshot"; CBT error | vSphere events; VMware KB | VMware snapshot consolidation |
| VSS error | "Backup job completed with warnings"; app-consistent fail | vssadmin list writers | VSS writer state; service restart |
| Authentication failure | "Access denied" to guest or repository | Security event log | Service account credentials / SPNs |
| Catalog corruption | Restore points missing; import fails | Veeam catalog rebuild | Database consistency check |
| CBT reset | Full backup unexpectedly triggered | esxcli storage core; CBT flag | Reset CBT flag on VMDK |

---

## Diagnostic Flowchart

```d2
direction: right

A: "Backup Job Failed" {shape: rectangle}
B: "Identify error in job log" {shape: rectangle}
L: "vSphere client: check VM snapshots\nCheck for delta consolidation needed" {shape: rectangle}
M: "Consolidate snapshots\nReset CBT if required" {shape: rectangle}
N: "Check repo free space\ndf -h / Get-VBRRepository" {shape: rectangle}
O: "Delete expired restore points\nScale-out repo expansion" {shape: rectangle}
T: "Check service account in job\nTest-ADServiceAccount" {shape: rectangle}
U: "Reset password\nVerify AD group membership" {shape: rectangle}
D: "Test-NetConnection to repo\nCheck MTU / proxy" {shape: rectangle}
F: "Engage network team\nCheck firewall rules" {shape: rectangle}
G: "Check throughput: iperf3\nVerify backup window" {shape: rectangle}
H: "vssadmin list writers\nCheck for Failed state" {shape: rectangle}
J: "Restart VSS writers\nnet stop / net start" {shape: rectangle}
K: "Check VSS event log\nApplication Log Event 8193/12293" {shape: rectangle}
P: "Check Veeam agent log\nC:\ProgramData\Veeam\Backup\" {shape: rectangle}
R: "Update agent to match VBR version" {shape: rectangle}
S: "Re-push agent\nCheck firewall port 2500-3300" {shape: rectangle}

A -> B
L -> M
N -> O
T -> U
```

### VSS Error Investigation

```cmd
rem List VSS writers and state
vssadmin list writers

rem Expected healthy output:
rem Writer name: 'SqlServerWriter'
rem    Writer Id: {a65faa63-5ea8-4ebc-9dbd-a0c4db26912a}
rem    Writer Instance Id: {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}
rem    State: [1] Stable
rem    Last error: No error

rem A failed writer shows:
rem    State: [8] Failed
rem    Last error: Retryable error
```

```powershell
# Restart common VSS writers
$writers = @(
    'VSS',
    'SQLWriter',
    'MSExchangeWriter',
    'System Writer'
)
foreach ($svc in @('VSS','SQLWriter','MSExchangeIS','BITS')) {
    Restart-Service -Name $svc -Force -ErrorAction SilentlyContinue
    Write-Host "Restarted $svc"
}
```

---

## Commvault Troubleshooting

### Job Status

```bash
# List recent backup jobs (run on CommServe or via CLI)
qlist job -t backup -n 20

# Example output:
# JOBID  TYPE    STATUS     CLIENT          SUBCLIENT   START              END
# 10234  Backup  Completed  srv-prod-db01   default     05/08 02:00:03     05/08 03:45:11
# 10235  Backup  Failed     srv-prod-app02  default     05/08 02:00:05     05/08 02:17:33

# Get failure reason for a specific job
qoperation execscript -sn QS_GetJobFailureReason -si 10235

# List active jobs
qlist job -t backup -st running
```


```text title="Expected output"
JOBID  TYPE    STATUS     CLIENT          SUBCLIENT   START              END
10234  Backup  Completed  srv-prod-db01   default     05/08 02:00:03     05/08 03:45:11
10235  Backup  Failed     srv-prod-app02  default     05/08 02:00:05     05/08 02:17:33
10236  Backup  Completed  srv-prod-web01  default     05/08 03:00:12     05/08 04:22:47
10237  Backup  Failed     srv-prod-db02   default     05/08 04:00:08     05/08 04:35:19
10238  Backup  Running    srv-prod-app03  default     05/08 05:00:01     -
10239  Backup  Completed  srv-prod-web02  default     05/08 05:30:44     05/08 06:15:22

Job Failure Reason for Job ID: 10235
Error Code: 31:4
Error Message: Failed to connect to the client. Verify network connectivity and firewall rules.

JOBID  TYPE    STATUS     CLIENT          SUBCLIENT   START              END
10238  Backup  Running    srv-prod-app03  default     05/08 05:00:01     -
10240  Backup  Running    srv-prod-db03   default     05/08 05:45:22     -
```

!!! warning "Common errors"
    **`qlist: command not found`** — Ensure the CommServe client is installed and the PATH includes the Commvault bin directory (typically `/opt/commvault/Base/bin`).
    **`Error Code: 31:4 - Failed to connect to the client`** — Verify network connectivity between CommServe and the client, check firewall rules, and confirm the client service is running with `systemctl status cvd`.
    **`qoperation execscript: Invalid script name 'QS_GetJobFailureReason'`** — Verify the exact script name and job ID syntax; use `qoperation execscript -sn QS_GetJobFailureReason -si <jobid>` with a valid numeric job ID.
### Log Locations and Analysis

| Component | Log File |
|---|---|
| File System Agent | `/var/log/commvault/Log_Files/clBackup.log` |
| MediaAgent | `/var/log/commvault/Log_Files/CVMA.log` |
| cvfwd (network) | `/var/log/commvault/Log_Files/cvfwd.log` |
| CommServe | `C:\Program Files\Commvault\ContentStore\Log Files\cvd.log` |

```bash
# Check cvfwd log for network errors
grep -i "error\|fail\|timeout" /var/log/commvault/Log_Files/cvfwd.log | tail -50

# Check connectivity from client to MediaAgent
telnet mediaagent01.corp.example.com 8400
```


```text title="Expected output"
2024-01-15 14:32:18 [ERROR] Connection timeout to MediaAgent mediaagent01.corp.example.com:8400 after 30s
2024-01-15 14:33:05 [WARN] Failed to authenticate with CommServe, retrying...
2024-01-15 14:33:42 [ERROR] Socket error: Connection refused on port 8400
2024-01-15 14:34:19 [ERROR] Backup job failed: Unable to reach MediaAgent within timeout window
2024-01-15 14:35:01 [WARN] Network latency detected: 450ms round-trip to mediaagent01
2024-01-15 14:35:47 [ERROR] Failed to write to staging area: Disk quota exceeded
2024-01-15 14:36:22 [ERROR] Timeout waiting for MediaAgent response (120s exceeded)

Trying 10.42.18.105...
telnet: Unable to connect to remote host: Connection timed out
```

!!! warning "Common errors"
    **`telnet: Unable to connect to remote host: Connection timed out`** — Verify MediaAgent is running (`systemctl status commvault-ma`), check firewall rules allow port 8400, and confirm DNS resolution with `nslookup mediaagent01.corp.example.com`.
    **`Socket error: Connection refused on port 8400`** — Restart the MediaAgent service with `systemctl restart commvault-ma` and verify the cvfwd daemon is listening on port 8400 using `netstat -tlnp | grep 8400`.
    **`Backup job failed: Unable to reach MediaAgent within timeout window`** — Increase the network timeout in CommServe backup policy settings or check for network congestion/packet loss using `ping -c 10 mediaagent01.corp.example.com`.
### Commvault Job Failure Reason Codes

| Code | Meaning | Fix |
|---|---|---|
| 19:65 | Network error between client and MA | Check firewall port 8400; verify cvfwd |
| 19:70 | MediaAgent offline | Start cvd service on MA |
| 14:61 | Disk library full | Extend disk library or prune old jobs |
| 9:77 | VSS snapshot failure | Investigate VSS writers on client |
| 69:59 | Tape drive offline | Physical check; clean drive |

---

## NetBackup Troubleshooting

### Job Status

```bash
# List recent jobs with status
bpdbjobs -report -all_columns -M master01.corp.example.com

# Filter failed jobs only
bpdbjobs -report -M master01 | grep " 1 " | head -20

# Get detailed job info
bpdbjobs -jobid 123456 -all_columns

# Query error detail
bperror -S master01 -jobid 123456 -l
```


```text title="Expected output"
Job ID    Policy Name          Client Name              Schedule      Status  Elapsed Time  KB Processed
123456    PROD_DB_DAILY        db-server-01.corp.local  Full_Backup   1       02:45:30      524288000
123457    PROD_DB_DAILY        db-server-02.corp.local  Full_Backup   0       00:15:22      1048576000
123458    PROD_APP_WEEKLY      app-server-03.corp.local Incremental   1       01:22:15      262144000
123459    PROD_DB_DAILY        db-server-04.corp.local  Full_Backup   1       03:10:45      786432000
123460    PROD_MAIL_DAILY      mail-server-01.corp.local Full_Backup   0       00:08:33      2097152000

Job ID    Policy Name          Client Name              Schedule      Status  Elapsed Time  KB Processed
123456    PROD_DB_DAILY        db-server-01.corp.local  Full_Backup   1       02:45:30      524288000
123458    PROD_APP_WEEKLY      app-server-03.corp.local Incremental   1       01:22:15      262144000
123459    PROD_DB_DAILY        db-server-04.corp.local  Full_Backup   1       03:10:45      786432000

Job ID: 123456
Policy Name: PROD_DB_DAILY
Client Name: db-server-01.corp.local
Schedule: Full_Backup
Status: 1 (Failed)
Elapsed Time: 02:45:30
KB Processed: 524288000
Error Code: 6
Start Time: 2024-01-15 22:30:15
End Time: 2024-01-16 01:15:45
Backup Type: Full

Error detail for job 123456:
Error Code: 6
Message: Cannot open file - permission denied on /var/lib/mysql/ibdata1
Client: db-server-01.corp.local
Time: 2024-01-16 01:15:42
```

!!! warning "Common errors"
    **`bpdbjobs: command not found`** — Ensure the NetBackup client or admin console is installed and the PATH includes the NetBackup bin directory (typically `/usr/openv/netbackup/bin`).
    **`Error: Cannot connect to master01.corp.example.com`** — Verify the master server hostname is correct, the NetBackup services are running on the master, and network connectivity exists from your current host.
    **`bperror: invalid jobid 123456`** — Confirm the job ID exists by running `bpdbjobs -report` first and use a valid job ID from the output.
### NetBackup Status Code Reference

| Status Code | Meaning | Fix |
|---|---|---|
| 0 | Successful | — |
| 13 | File read failed | Check permissions on backup path |
| 23 | Socket read failed | Network issue between client and master |
| 41 | Network connection timed out | Firewall; NB ports 1556, 13724 |
| 58 | Client timed out | Slow disk on client; increase CLIENT_READ_TIMEOUT |
| 83 | Media mount failure | Check robot / tape library |
| 99 | NDMP backup failure | Check NDMP service on NAS |
| 196 | Client backup was not attempted | Backup window missed; check schedule |

```bash
# Check backup client connectivity
bptestbpcd -client client01.corp.example.com

# Verify NetBackup daemon status on client
/usr/openv/netbackup/bin/bpps -a

# Check catalog health
bpdbm -consistency -M master01
```


```text title="Expected output"
client01.corp.example.com: PASSED (response time: 42ms)

NetBackup processes on client01.corp.example.com:
  PID     PPID    COMMAND
  2847    1       /usr/openv/netbackup/bin/bprd
  2891    2847    /usr/openv/netbackup/bin/bpsched
  2934    2847    /usr/openv/netbackup/bin/bpdbm
  3012    2847    /usr/openv/netbackup/bin/bptm
  3156    2847    /usr/openv/netbackup/bin/bpcd

Catalog consistency check on master01:
  Checking database integrity...
  Total records scanned: 1,247,392
  Inconsistencies found: 0
  Status: HEALTHY
  Check completed in 187 seconds
```

!!! warning "Common errors"
    **`bptestbpcd: command not found`** — Ensure NetBackup client is installed and `/usr/openv/netbackup/bin` is in your PATH, or use the full path `/usr/openv/netbackup/bin/bptestbpcd`.
    **`Connection refused on client01.corp.example.com port 13782`** — Verify the NetBackup daemon (bpcd) is running on the client with `/usr/openv/netbackup/bin/bpps -a` and check firewall rules allow port 13782 between master and client.
    **`bpdbm: Catalog database locked by another process`** — Wait for any running backup or restore jobs to complete, or check for hung processes with `bpps -a` and kill stale processes if necessary.
---

## Repository Capacity Checks

```bash
# Linux: disk usage on repository mount
df -h /backup
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sdb1        20T   18T  2.0T  90% /backup

# Find largest directories consuming space
du -sh /backup/* | sort -rh | head -10

# Windows: check backup drive
Get-PSDrive -Name D | Select-Object Name, Used, Free |
    ForEach-Object {
        [PSCustomObject]@{
            Drive   = $_.Name
            UsedGB  = [math]::Round($_.Used/1GB, 1)
            FreeGB  = [math]::Round($_.Free/1GB, 1)
            UsedPct = [math]::Round($_.Used/($_.Used+$_.Free)*100, 1)
        }
    }
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb1        20T   18T  2.0T  90% /backup

18G	/backup/daily-2024-01-15
16G	/backup/daily-2024-01-14
14G	/backup/weekly-2024-01-08
12G	/backup/monthly-2024-01
8.5G	/backup/daily-2024-01-13
7.2G	/backup/archive-prod-db
6.8G	/backup/daily-2024-01-12
5.4G	/backup/incremental-cache
4.1G	/backup/daily-2024-01-11
3.9G	/backup/temp-staging

Drive UsedGB FreeGB UsedPct
----- ------ ------ -------
    D  1847.3  152.7    92.4
```

!!! warning "Common errors"
    **`du: cannot access '/backup/daily-2024-01-15': Permission denied`** — Run the command with `sudo` or ensure the user has read permissions on the backup directory.
    **`Get-PSDrive : Cannot find drive. Does the drive 'D' exist?`** — Verify the backup drive letter with `Get-PSDrive` and replace 'D' with the correct drive letter.
---

## Network Path Validation to Backup Target

```powershell
# Test TCP connectivity to backup repository (Veeam default ports 2500-3300)
Test-NetConnection -ComputerName repo01.corp.example.com -Port 2500
Test-NetConnection -ComputerName repo01.corp.example.com -Port 2501

# Measure throughput with iperf3 (install on both ends)
# Server side:
iperf3 -s -p 5201
# Client side:
iperf3 -c repo01.corp.example.com -p 5201 -t 30 -P 4

# Example good output:
# [SUM]   0.00-30.00  sec  33.8 GBytes  9.69 Gbits/sec    0   sender
```

---

## Top 10 Veeam Error Codes with Fixes

| Error | Message | Fix |
|---|---|---|
| Agent failed to process method {DataTransfer.SyncDisk} | CBT error on VMDK | Reset CBT: disable/enable CBT via PowerCLI |
| Cannot open VDDK transport: VDDK error 2 | VDDK library missing or version mismatch | Reinstall matching VDDK on proxy |
| Failed to call RPC function 'StartRPCServer' | Guest agent not responding | Re-push Veeam agent; check firewall 6160/6162 |
| Snapshot creation failed | VMware snapshot error | Consolidate existing snapshots; check VMFS space |
| Repository <name> is not accessible | Network/auth to repo | Verify share path; credentials; SMB port 445 |
| Warning: Cannot truncate transaction logs | SQL log truncation failed | Check SQL VSS writer; verify sysadmin on account |
| GetBackupFiles error — invalid path | Changed proxy or repo path | Rescan backup files; update job config |
| GFS retention policy conflict | Archival chain broken | Disable GFS temporarily; rebuild chain |
| Failed to check whether Veeam Installer Service is installed | WMI failure | Restart WMI service on guest |
| VDDK transport mode: SAN — no LUN access | SAN zoning or iSCSI IQN issue | Switch proxy to NBD mode; fix SAN zoning |

---

## Escalation Criteria

Escalate to backup vendor TAC or infrastructure team when:

- Any Tier-1 protected system has missed 2+ consecutive backup cycles
- Repository is above 85% capacity with no automated pruning available
- VSS writer failures persist after service restart (possible OS corruption)
- CBT resets are recurring on the same VM (VMware or storage-level issue)
- NetBackup master server catalog is reporting consistency errors
- Backup window is consistently exceeding the defined maintenance window
- DR test restore fails — RPO/RTO commitments at risk
- Ransomware suspected: check for mass deletion of restore points

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [DR Operations — Known Issues](../known-issues.md)
- [DR Operations — Troubleshooting Overview](../)
- [DR Operations — Overview](../../)
