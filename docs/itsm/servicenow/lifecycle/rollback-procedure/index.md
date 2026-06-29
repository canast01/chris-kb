---
tags:
  - servicenow
---
# Rollback Procedure

<div class="kb-summary">
Restores a system to its last known-good state when a change produces failures, instability, or unacceptable risk. Rollback must be faster and safer than attempting to fix the issue forward during an incident.

*Applies to: ServiceNow*
</div>

## Decision Framework

```d2
direction: right

B: "B" {shape: rectangle}
C: "Declare success\nClose change ticket" {shape: rectangle}
D: "D" {shape: rectangle}
E: "Attempt fix\nwith ops lead approval" {shape: rectangle}
F: "ROLLBACK" {shape: rectangle}
G: "G" {shape: rectangle}
H: "Execute rollback" {shape: rectangle}
I: "Validate rollback" {shape: rectangle}
J: "Incident report\nand change re-plan" {shape: rectangle}
A: "Change Applied" {shape: rectangle}

B -> C
D -> E
D -> F
G -> C
G -> F
F -> H
H -> I
I -> J
```

```bash
# Windows — uninstall cumulative update
wusa /uninstall /kb:<KBnumber> /quiet /norestart
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: 0x80240017 - CBS_E_NOT_APPLICABLE`** — Verify the KB number matches an installed update using `wmic qfe list brief` and confirm the update is not a prerequisite for other installed patches.
    **`Error: 0x80070005 - Access Denied`** — Run the command prompt as Administrator; right-click cmd.exe and select "Run as administrator" before executing wusa.
## Method 3 — Configuration Revert

```bash
# Ansible — revert to previous playbook version
git checkout <previous-commit> -- playbooks/site.yml
ansible-playbook -i inventory/production/ playbooks/site.yml --limit <hostname>

# Manual file revert from backup copy
cp /etc/nginx/nginx.conf.bak.$(date +%F) /etc/nginx/nginx.conf
nginx -t && systemctl reload nginx

# Cisco IOS — revert to startup config
copy startup-config running-config

# Arista EOS
configure replace checkpoint://pre-change-<hostname>
```


```text title="Expected output"
Updated 1 path from the index
PLAY [all] *********************************************************************
TASK [Gathering Facts] *********************************************************
ok: [web-prod-01.internal]
TASK [Deploy site configuration] ***********************************************
ok: [web-prod-01.internal]
PLAY RECAP *********************************************************************
web-prod-01.internal       : ok=2    changed=0    unreachable=0    failed=0
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
Reloading nginx: [  OK  ]
*Mar 15 14:32:18.456 UTC: %SYS-5-CONFIG_I: Configured from console by admin on vty0 (10.45.12.8)
Preparing to replace running-config with startup-config
[OK]
Executing checkpoint replace on device
Rollback completed successfully. 1247 lines restored.
```

!!! warning "Common errors"
    **`fatal: your current branch 'main' is ahead of <previous-commit>`** — Ensure the commit hash exists in your repository history using `git log` and verify the correct commit SHA.
    **`nginx: [error] open() "/etc/nginx/nginx.conf.bak.2025-01-15" failed (2: No such file or directory)`** — Confirm the backup file exists with the correct date format using `ls -la /etc/nginx/nginx.conf.bak.*` before attempting restore.
    **`% Invalid command`** — Verify the device is in enable mode with `enable` and that the startup-config exists using `show startup-config | include Running`.
## Method 4 — Database Rollback

```bash
# PostgreSQL — restore from pre-change dump
pg_restore -h <host> -U postgres -d <db> --clean /backups/<db>-pre-change-$(date +%F).dump

# SQL Server
RESTORE DATABASE [dbname] FROM DISK = 'D:\Backups\dbname_pre_change.bak'
  WITH REPLACE, RECOVERY, STATS=10;

# PostgreSQL PITR
# In recovery.conf:
# recovery_target_time = '2026-05-10 02:00:00'
```


```text title="Expected output"
pg_restore: connecting to database "servicenow_prod"
pg_restore: dropping DATABASE servicenow_prod
pg_restore: creating DATABASE servicenow_prod
pg_restore: connecting to new database "servicenow_prod"
pg_restore: processing data for table "public.incident"
pg_restore: processing data for table "public.change_request"
pg_restore: processing data for table "public.cmdb_ci_server"
pg_restore: restoring table data for ID 2847 (public.incident)
pg_restore: restoring table data for ID 2851 (public.change_request)
pg_restore: [archiver] worker process failed: Exit code 1
pg_restore: setting owner and privileges on schema public
pg_restore: [archiver] set_session_authorization must be called after the initial connection
```

!!! warning "Common errors"
    **`pg_restore: [archiver] could not open input file "/backups/servicenow_prod-pre-change-2026-05-10.dump": No such file or directory`** — Verify the backup file exists at the specified path and the date variable expands correctly by running `ls -la /backups/` first.
    **`FATAL: role "postgres" does not exist`** — Create the postgres user with `createuser -s postgres` or use an existing superuser role with the `-U` flag.
    **`ERROR: database "servicenow_prod" is being accessed by other users`** — Terminate active connections with `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='servicenow_prod';` before restore.
## Method 5 — Full Backup Restore

```bash
# Veeam — restore entire VM from backup
$backup = Get-VBRBackup -Name "Production VMs"
$restorePoint = Get-VBRRestorePoint -Backup $backup -Name "HOSTNAME" | Select-Object -Last 1
Start-VBRRestoreVM -RestorePoint $restorePoint -PowerState PowerOn
```


```text title="Expected output"
Name                    : HOSTNAME
BackupId                : 36d4a8c2-7f1b-4e9a-b2d1-5c8e9f3a1b2c
CreationTime            : 2024-01-15 02:30:45
Size                    : 487 GB
IsCorrupted             : False

Restore job started: Job_20240115_143022
JobId                   : 8b9c2d1e-4f5a-6b7c-8d9e-0f1a2b3c4d5e
Status                  : Running
Progress                : 45%
ETA                     : 00:12:30

VM HOSTNAME restore completed successfully
PowerState              : PowerOn
RestoreTime             : 2024-01-15 14:45:22
```

!!! warning "Common errors"
    **`Get-VBRBackup : Cannot find backup with name "Production VMs"`** — Verify the exact backup name with `Get-VBRBackup | Select-Object Name` and update the script accordingly.
    **`Start-VBRRestoreVM : Restore point is corrupted or inaccessible`** — Check backup integrity with `Get-VBRBackup -Name "Production VMs" | Get-VBRRestorePoint | Where-Object {$_.IsCorrupted -eq $true}` and select an earlier restore point.
    **`Access denied: Insufficient permissions to restore VM`** — Ensure your Veeam service account has Restore operator role or higher in Veeam Backup & Replication console.
**Expected time:** 30–120 minutes depending on backup size.

## Post-Rollback Validation

```bash
systemctl --failed
journalctl -p err -n 50 --no-pager
curl -sk https://<app-url>/health

# Confirm the specific change is reverted
<version-check-command>   # e.g. rpm -q nginx, vmware -v
```


```text title="Expected output"
● nginx.service
● postgresql.service

2 units in failed state.

Jan 15 10:42:33 app-prod-01 nginx[2847]: error: bind() to 0.0.0.0:443 failed (98: Address already in use)
Jan 15 10:42:32 app-prod-01 systemd[1]: nginx.service: Main process exited, code=exited, status=1/FAILURE
Jan 15 10:42:15 app-prod-01 postgresql[3124]: FATAL: could not access private key file "/etc/pgsql/server.key": Permission denied
Jan 15 10:42:14 app-prod-01 kernel: Out of memory: Kill process 5891 (java) score 412 or sacrifice child
Jan 15 10:41:58 app-prod-01 systemd[1]: postgresql.service: Main process exited, code=exited, status=1/FAILURE

{
  "status": "unhealthy",
  "version": "2.14.3-rev847",
  "uptime_seconds": 142,
  "database": "disconnected",
  "timestamp": "2025-01-15T10:43:22Z"
}

nginx-1.24.0-1.el8.x86_64
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification, or import the CA certificate into your system trust store.
    **`journalctl: command not found`** — Install systemd-devel package or use `tail -f /var/log/messages` on systems without journalctl support.
    **`systemctl: command not found`** — Verify you are running as root or with sudo, and that systemd is installed on this system.
## Rollback Checklist

| Step | Done |
|---|---|
| Decision made by on-call lead or change manager | ☐ |
| Rollback method selected | ☐ |
| Stakeholders notified of rollback | ☐ |
| Rollback executed | ☐ |
| Post-rollback validation complete | ☐ |
| Services confirmed stable | ☐ |
| Application team confirmed OK | ☐ |
| Monitoring alerts cleared | ☐ |
| Pre-change snapshot removed (if reverted) | ☐ |
| Change ticket updated to "Rolled Back" | ☐ |
| Incident / PIR ticket opened | ☐ |

## Post-Rollback Actions

1. **Incident ticket** — document what failed and the timeline
2. **Root cause analysis** — identify why the change caused failure
3. **Re-plan the change** — fix the root cause before re-scheduling
4. **PIR** — for Sev1/Sev2 impact events
5. **Test in staging** — validate the fix in non-production first
