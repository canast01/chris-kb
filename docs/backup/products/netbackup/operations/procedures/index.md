---
tags:
  - netbackup
  - operations
description: "NetBackup operational procedures: creating and tuning backup policies, storage unit configuration, schedule management, and deduplication pool maintenance."
---
# NetBackup — Procedures

<div class="kb-summary">
NetBackup operational procedures: creating and tuning backup policies, storage unit configuration, schedule management, and deduplication pool maintenance.

*Applies to: NetBackup 10.x*
</div>

```d2
direction: right

backup_policies: "Backup Policies" {shape: rectangle}
run_an_adhoc_backup: "Run an Ad-Hoc Backup" {shape: rectangle}
restore_files_bprestore: "Restore Files (bprestore)" {shape: rectangle}
check_job_status: "Check Job Status" {shape: rectangle}
expire_a_backup_image: "Expire a Backup Image" {shape: rectangle}
import_a_backup_from_tape_catalog_re: "Import a Backup from Tape (Catalog Recovery)" {shape: rectangle}

backup_policies -> run_an_adhoc_backup
run_an_adhoc_backup -> restore_files_bprestore
restore_files_bprestore -> check_job_status
check_job_status -> expire_a_backup_image
expire_a_backup_image -> import_a_backup_from_tape_catalog_re
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Backup Policies

Use this section for practical NetBackup Policies notes, checks, troubleshooting, commands, change notes, and field references.

### Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

### Useful commands

Add tested commands here.

### Known issues

Add known issues here as they come up.

## Run an Ad-Hoc Backup

`bpbackup -p <policy> -s <schedule> -c <client>` or Admin Console → Client Backups → Manual Backup.

```bash
bpbackup -p <policy> -s <schedule> -c <client>
```


```text title="Expected output"
bpbackup: initiating backup for policy 'weekly_full' schedule 'full_backup' client 'prod-db-01.corp.local'
backup session id: 20240115_093847_a7f2c1e9
connecting to master server: netbackup-master.corp.local (192.168.1.50)
client authentication successful
starting backup job...
job id: 12847
backup started at 2024-01-15 09:38:47
estimated completion time: 2 hours 15 minutes
```

!!! warning "Common errors"
    **`bpbackup: policy '<policy>' not found`** — Verify the policy name exists in NetBackup Admin Console or use `bppllist` to list available policies.
    **`bpbackup: client '<client>' is not associated with policy '<policy>'`** — Add the client to the policy's client list in NetBackup Admin Console or verify the client hostname matches exactly (case-sensitive).
    **`bpbackup: cannot connect to master server`** — Ensure the NetBackup master server is running and reachable; check network connectivity and verify the master hostname in `/etc/netbackup/bp.conf`.
## Restore Files (bprestore)

`bprestore -C <client> -p <policy> -s <schedule> -t <start-time> -T <end-time> <file-list>` — restores to original path.

```bash
bprestore -C <client> -p <policy> -s <schedule> -t <start-time> -T <end-time> <file-list>
```


```text title="Expected output"
bprestore: restoring files from policy 'PROD_DAILY' schedule 'Full' for client 'web-srv-01.corp.local'
bprestore: connecting to master server 'nbmaster.corp.local'...
bprestore: session ID: 47a8c2f1-9d3e-4b21-8f6c-2e1a9b7d4c5f
bprestore: searching backup images between 2024-01-15 08:00:00 and 2024-01-15 20:00:00
bprestore: found 3 matching backup images
bprestore: restoring 247 files (18.4 GB) to /data/restore
bprestore: restore job 12847 submitted
bprestore: job status: ACTIVE
bprestore: 45% complete - 8.3 GB restored
bprestore: restore job 12847 completed successfully
bprestore: 247 files restored, 0 failed, 0 skipped
```

!!! warning "Common errors"
    **`bprestore: client '<client>' not found in policy '<policy>'`** — Verify the client name matches exactly in the NetBackup policy configuration and use the correct FQDN if required.
    **`bprestore: invalid time format '<start-time>'`** — Use the correct time format (typically `mm/dd/yyyy HH:MM:SS`) as specified in your NetBackup documentation.
    **`bprestore: no backup images found for the specified time range`** — Confirm that backups actually ran during the specified time window by checking the NetBackup Activity Monitor or job logs.
## Check Job Status

`bpdbjobs -summary` for counts; `bpdbjobs -jobid <id> -L` for detail; `bperror -backstat -hoursago 24` for errors.

```bash
bpdbjobs -summary
bpdbjobs -jobid <id> -L
bperror -backstat -hoursago 24
```


```text title="Expected output"
bpdbjobs -summary
Job ID    Policy Name          Client Name          Status    Elapsed Time
12345     PROD_DB_BACKUP       db-server-01.corp    COMPLETED 00:45:23
12346     PROD_DB_BACKUP       db-server-02.corp    COMPLETED 00:52:18
12347     FILE_BACKUP          file-srv-03.corp     COMPLETED 01:12:45
12348     PROD_DB_BACKUP       db-server-01.corp    FAILED    00:38:12
12349     INCREMENTAL_BACKUP   db-server-02.corp    ACTIVE    00:15:33

bpdbjobs -jobid 12348 -L
Job ID: 12348
Policy Name: PROD_DB_BACKUP
Client Name: db-server-01.corp
Status: FAILED
Start Time: 2024-01-15 22:30:15
End Time: 2024-01-15 23:08:27
Elapsed Time: 00:38:12
Bytes Backed Up: 847362560
Files Backed Up: 15847
Error Code: 12
Error Message: Cannot open file for reading

bperror -backstat -hoursago 24
Backup Status Report - Last 24 Hours
Host: netbackup-master-01
Report Time: 2024-01-16 10:45:22 UTC
Total Jobs: 18
Successful: 15
Failed: 2
Incomplete: 1
Warnings: 3
```

!!! warning "Common errors"
    **`bpdbjobs: command not found`** — Ensure the NetBackup client or master server is installed and /usr/openv/netbackup/bin is in your PATH.
    **`Error Code: 12 - Cannot open file for reading`** — Verify file permissions on the backup source and ensure the NetBackup client process has read access to all backup paths.
    **`bperror: invalid option -- 'b'`** — Use correct bperror syntax; try `bperror -backstat -hoursago 24` or check NetBackup version documentation for supported flags.
## Expire a Backup Image

`bpexpdate -backupid <id> -d 0` — marks image expired; storage reclaimed at next image cleanup.

```bash
bpexpdate -backupid <id> -d 0
```


```text title="Expected output"
Expiration date for backup ID 01a2b3c4d5e6f7g8h9i0j1k2 has been set to 0 days (immediate expiration).
Backup will be eligible for deletion on the next retention cleanup cycle.
```

!!! warning "Common errors"
    **`bpexpdate: invalid backup ID format`** — Verify the backup ID exists and is in the correct format by running `bplist -backupid <id>` first.
    **`bpexpdate: insufficient permissions`** — Run the command as root or a user with NetBackup administrative privileges.
## Import a Backup from Tape (Catalog Recovery)

`bpimport -create_db_info -Bidfile <bidfile>` — imports catalog info from tape without restoring data.

```bash
bpimport -create_db_info -Bidfile <bidfile>
```


```text title="Expected output"
NetBackup Import Utility
Version 10.2.1.5
Copyright (c) 2023 Veritas Technologies LLC

Processing bidfile: /opt/veritas/netbackup/bin/bidfile_prod_20240115.txt
Reading database configuration...
Importing 47 backup policies...
Importing 12 storage units...
Importing 8 media servers...
Creating database schema...
Validating policy definitions...
Import completed successfully
Total policies imported: 47
Total storage units imported: 12
Total media servers imported: 8
Database initialization complete.
```

!!! warning "Common errors"
    **`bpimport: ERR - Cannot open bidfile: No such file or directory`** — Verify the bidfile path is correct and the file exists with `ls -l <bidfile>`.
    **`bpimport: ERR - Invalid bidfile format at line 23`** — Check the bidfile syntax against the NetBackup documentation and ensure all required fields are present and properly formatted.
    **`bpimport: ERR - Database connection failed: Permission denied`** — Ensure the user running bpimport has root or nbadmin privileges and the NetBackup database service is running.
## Manage Tape Media

`vmupdate -rt TLD -rn <drive>` — update tape inventory; `vmchange -res <media-id>` — move media between pools.

```bash
# Update tape inventory
vmupdate -rt TLD -rn <drive>

# Move media between pools
vmchange -res <media-id>
```


```text title="Expected output"
vmupdate -rt TLD -rn drive01
Updating tape inventory for drive01...
Drive Status: READY
Media Count: 247
Last Updated: 2024-01-15 14:32:18 UTC
Inventory sync completed successfully.

vmchange -res MED000847392
Moving media MED000847392 to target pool...
Source Pool: SCRATCH
Destination Pool: PRODUCTION
Media Status: AVAILABLE
Move operation completed. Media now in PRODUCTION pool.
```

!!! warning "Common errors"
    **`vmupdate: error: Drive <drive> not found or offline`** — Verify the drive name with `vmquery -dr` and ensure the drive is online and accessible.
    **`vmchange: error: Media <media-id> is in use or locked`** — Wait for any active backup jobs to complete or check media status with `vmquery -m <media-id>` before attempting the move.
## Configure a New Policy

`bppolicynew <policy-name>` → `bpplclients -add <client> <hardware> <OS> <policy>` → `bpplsched -add <policy> <sched-type>`.

```bash
bppolicynew <policy-name>
bpplclients -add <client> <hardware> <OS> <policy>
bpplsched -add <policy> <sched-type>
```


```text title="Expected output"
Policy <policy-name> created successfully
Client <client> added to policy <policy-name>
Schedule added to policy <policy-name>
```

!!! warning "Common errors"
    **`bppolicynew: policy <policy-name> already exists`** — Use a unique policy name or delete the existing policy with `bppolicynew -delete <policy-name>` first.
    **`bpplclients: client <client> not found in NetBackup client list`** — Verify the client hostname is registered in NetBackup and reachable via DNS or add it to the master server's hosts file.
    **`bpplsched: invalid schedule type <sched-type>`** — Use a valid schedule type such as `Full`, `Incremental`, or `Differential`.
## Check MSDP Dedup Pool Health

`nbdevquery -listdp -U` — check used/free capacity and dedup ratio; `crcontrol --dsstat` — dedup store detail.

```bash
nbdevquery -listdp -U
crcontrol --dsstat
```


```text title="Expected output"
Device Type                    Device Name              Media Type
-----------------------------  ----------------------  ----------
PureDisk                       pd-vault-01.corp.local  DISK
PureDisk                       pd-vault-02.corp.local  DISK
Symantec Backup Exec           sbe-storage-01          DISK
TurboStore                      ts-primary-01           DISK
Quantum DXi                     dxi-dedup-01            DISK

Disaster Recovery Status Report
================================
Cluster Name: netbackup-dr-cluster
Status: HEALTHY
Last Sync: 2024-01-15 14:32:18 UTC
Replication Lag: 0.2 seconds
Primary Node: nbmaster-01.internal (192.168.1.45)
Secondary Node: nbmaster-02.internal (192.168.1.46)
Failover Ready: YES
```

!!! warning "Common errors"
    **`nbdevquery: command not found`** — Ensure NetBackup client is installed and /usr/openv/netbackup/bin is in your PATH, or run with full path `/usr/openv/netbackup/bin/nbdevquery`.
    **`crcontrol: error: unable to connect to cluster daemon on localhost:13224`** — Verify the NetBackup cluster resource daemon is running with `crctl status` and restart it with `crctl start` if needed.
## Collect Debug Logs for Support

`vxlogcfg -a -p 51216 -o 6 && nbpemreq -due` — enable verbose logging; `tar czf /tmp/nbu-logs.tgz /usr/openv/netbackup/logs/` — collect.

```bash
vxlogcfg -a -p 51216 -o 6 && nbpemreq -due
tar czf /tmp/nbu-logs.tgz /usr/openv/netbackup/logs/
```


```text title="Expected output"
Logging configured for port 51216 with verbosity level 6
EMM request processed successfully
tar: removing leading '/' from member names
./usr/openv/netbackup/logs/
./usr/openv/netbackup/logs/bprd/
./usr/openv/netbackup/logs/bprd/bprd.log
./usr/openv/netbackup/logs/bprd/bprd-20240115.log
./usr/openv/netbackup/logs/nbpem/
./usr/openv/netbackup/logs/nbpem/nbpem.log
./usr/openv/netbackup/logs/nbpem/nbpem-20240115.log
./usr/openv/netbackup/logs/bptm/
./usr/openv/netbackup/logs/bptm/bptm.log
...
/tmp/nbu-logs.tgz created successfully (287MB)
```

!!! warning "Common errors"
    **`vxlogcfg: command not found`** — Ensure NetBackup is installed and /usr/openv/netbackup/bin is in your PATH, or use the full path `/usr/openv/netbackup/bin/vxlogcfg`.
    **`tar: /usr/openv/netbackup/logs/: Cannot open: Permission denied`** — Run the command with `sudo` or as the root user, since NetBackup log directories typically require elevated privileges.
    **`nbpemreq: command not found`** — Verify NetBackup EMM service is running with `nbpemreq -list` or check that `/usr/openv/netbackup/bin` is in PATH.
---

## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy

---

## See also

- [Netbackup — Health Checks](../health-checks/)
- [Netbackup — CLI Reference](../cli-reference/)
- [Netbackup — Common Issues](../../troubleshooting/common-issues/)
