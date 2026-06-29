---
tags:
  - netbackup
  - troubleshooting
search:
  boost: 1.5
---
# NetBackup — Common Issues

```bash
# Check bpcd is running on the client
bpps -a | grep bpcd

# Test connectivity from master to client on NetBackup port
telnet <client-hostname> 13782

# Review bpcd log on client
tail -200 /usr/openv/netbackup/logs/bpcd/log.<yyyymmdd>

# Review bpbrm log on master
tail -200 /usr/openv/netbackup/logs/bpbrm/log.<yyyymmdd>
```


```text title="Expected output"
root@master# bpps -a | grep bpcd
    root   2847     1  0 08:15 ?        00:00:02 /usr/openv/netbackup/bin/bpcd -standalone

root@master# telnet client-prod-01 13782
Trying 192.168.10.45...
Connected to client-prod-01.example.com.
Escape character is '^]'.
Connection closed by foreign host.

root@master# tail -200 /usr/openv/netbackup/logs/bpcd/log.20240115
01/15/2024 08:15:32 bpcd: started
01/15/2024 08:15:35 bpcd: listening on port 13782
01/15/2024 08:16:12 bpcd: connection from 192.168.10.10 (master-01)
01/15/2024 08:16:13 bpcd: backup job 12847 initiated
01/15/2024 08:17:45 bpcd: job 12847 completed successfully

root@master# tail -200 /usr/openv/netbackup/logs/bpbrm/log.20240115
01/15/2024 08:16:10 bpbrm: job 12847 queued for client client-prod-01
01/15/2024 08:16:12 bpbrm: initiating connection to 192.168.10.45:13782
01/15/2024 08:16:13 bpbrm: job 12847 sent to bpcd
01/15/2024 08:17:45 bpbrm: job 12847 completed with status 0
```

!!! warning "Common errors"
    **`bpcd: not found in process list`** — Restart bpcd on the client with `/usr/openv/netbackup/bin/bpcd -standalone` or verify the NetBackup installation is complete.
    **`telnet: Unable to connect to remote host: Connection refused`** — Verify port 13782 is open in the firewall between master and client, and that bpcd is listening on the client.
    **`tail: cannot open '/usr/openv/netbackup/logs/bpcd/log.20240115' for reading: No such file or directory`** — Correct the log filename date format (use `ls /usr/openv/netbackup/logs/bpcd/` to find the correct log file) or check that bpcd has actually run on that date.
```bash
# Check catalog backup job history
bplist -S <master-server> -policy NBU_Catalog -Listdead -d 01/01/1970 00:00:00

# Force an immediate catalog backup
bpbackup -p NBU_Catalog_Backup

# Check catalog database consistency
bpdbm -consistency -verbose
```

```text title="Expected output"
Job ID: 2847362918
Policy: NBU_Catalog
Client: nbu-master-01.corp.local
Schedule: NBU_Catalog_Full
Status: COMPLETED
Start Time: 01/15/2024 02:30:15
End Time: 01/15/2024 02:45:22
Elapsed Time: 15 minutes 7 seconds

Job ID: 2847251643
Policy: NBU_Catalog
Client: nbu-master-01.corp.local
Schedule: NBU_Catalog_Incr
Status: COMPLETED
Start Time: 01/14/2024 02:30:08
End Time: 01/14/2024 02:31:44
Elapsed Time: 1 minute 36 seconds

Submitting backup request for policy NBU_Catalog_Backup...
Job submitted successfully. Job ID: 2847398472
Backup initiated on nbu-master-01.corp.local

Checking catalog database consistency...
Database: /usr/openv/netbackup/db/data
Status: CONSISTENT
Total Records: 1247834
Orphaned Records: 0
Integrity Check: PASSED
Consistency verification completed successfully.
```

!!! warning "Common errors"
    **`bplist: invalid date format`** — Use the correct date format `MM/DD/YYYY HH:MM:SS` or omit the `-d` flag to list all jobs.
    **`bpbackup: policy NBU_Catalog_Backup not found`** — Verify the policy name exists with `bppllist` and use the exact policy name without extra characters.
    **`bpdbm: database locked by another process`** — Wait for any running backup or maintenance jobs to complete, or restart the NetBackup database manager with `bpdbm -restart`.
```bash
# Check all STU free space
bpstulist -U

# Check disk pool usage (MSDP / AdvancedDisk)
nbdevquery -listdp -stype PureDisk -U

# Expire old images to reclaim space
bpexpdate -policy <policyname> -d 0 -backupid <backup-id>

# Run image cleanup to actually reclaim the space
bpimage -cleanup
```

```text title="Expected output"
STU List:
STU Name                          Media Server         Free Space (GB)  Total Space (GB)
STU_PROD_001                      media-srv-01.corp    2847.5           5120.0
STU_PROD_002                      media-srv-02.corp    1203.8           5120.0
STU_PROD_003                      media-srv-03.corp    4092.1           5120.0
STU_LEGACY_001                    media-srv-04.corp    512.3            2048.0

Disk Pool List:
Pool Name              Media Server         Type       Free Space (GB)  Status
MSDP_Primary          media-srv-01.corp    PureDisk   8456.2           Active
MSDP_Secondary        media-srv-02.corp    PureDisk   3124.7           Active
AdvancedDisk_Archive  media-srv-03.corp    PureDisk   15892.4          Active

Expiring images for policy 'DAILY_BACKUPS' with backup ID 'bkp_20240115_001'...
Images marked for expiration: 47
Reclaim potential: 523.6 GB

Running image cleanup...
Cleanup started at 2024-01-15 14:32:18
Processing 47 expired images...
Reclaimed space: 523.6 GB
Cleanup completed successfully at 2024-01-15 14:35:42
```

!!! warning "Common errors"
    **`bpstulist: command not found`** — Ensure the NetBackup client or media server binaries are in your PATH, or source the NetBackup environment setup script (typically `. /usr/openv/netbackup/bin/bp.env`).
    **`nbdevquery: invalid option -- 's'`** — Use the correct syntax `nbdevquery -listdp -stype PureDisk` without extra spaces, or check your NetBackup version for the correct flag format.
    **`bpimage -cleanup: No images to process`** — Verify that expired images exist by running `bpimage -list` first; if none exist, ensure `bpexpdate` completed successfully and images were actually marked for expiration.
```bash
# Check MSDP pool status
cacontrol --dsstat -d <msdp-path>

# Check fingerprint database health
cacontrol --dbstat

# Review dedupe log for anomalies
tail -500 /usr/openv/netbackup/logs/spoold/log.<yyyymmdd>
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
A: "Status 25 — client connect refused" {shape: rectangle}
B: "Media manager volume busy" {shape: rectangle}
C: "Catalog backup failed" {shape: rectangle}
D: "Policy class mismatch" {shape: rectangle}
E: "Master / media server connectivity loss" {shape: rectangle}
A1: "A1" {shape: rectangle}
A2: "Start bpcd and verify port 13782 open — see Before you begin" {shape: rectangle}
A3: "Check bpbrm and bpcd logs for TLS or host ID error" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "Check ltid process and tpconfig -d — see Before you begin" {shape: rectangle}
B3: "Check for volume in use by another job; wait or cancel conflicting job" {shape: rectangle}
C1: "C1" {shape: rectangle}
C2: "Check MSDP pool and STU free space — see Before you begin" {shape: rectangle}
C3: "Run bpdbm -consistency and force catalog backup with bpbackup" {shape: rectangle}
D1: "D1" {shape: rectangle}
D2: "Correct policy type in NetBackup console to match client OS" {shape: rectangle}
D3: "Check schedule type and retention level for the policy" {shape: rectangle}
E1: "E1" {shape: rectangle}
E2: "Restart NetBackup services on master and check firewall rules" {shape: rectangle}
E3: "Check NBU CA host ID certificate validity on media server" {shape: rectangle}

S -> A
S -> B
S -> C
S -> D
S -> E
A1 -> A2
A1 -> A3
B1 -> B2
B1 -> B3
C1 -> C2
C1 -> C3
D1 -> D2
D1 -> D3
E1 -> E2
E1 -> E3
```

---

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Netbackup — Diagnostics](../diagnostics/)
- [Netbackup — Escalation](../escalation/)
- [Netbackup — Health Checks](../../operations/health-checks/)
