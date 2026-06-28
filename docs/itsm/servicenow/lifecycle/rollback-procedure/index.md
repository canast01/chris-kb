---
tags:
  - servicenow
---
# Rollback Procedure


<div class="kb-summary">
Restores a system to its last known-good state when a change produces failures, instability, or unacceptable risk. Rollback must be faster and safer than attempting to fix the issue forward during an incident.

*Applies to: ServiceNow*
</div>
![Rollback Procedure](../../../../assets/itsm-servicenow-lifecycle-rollback-procedure-index.svg)


```d2
direction: right

center: "ServiceNow" {shape: hexagon}
decision_framework: "Decision Framework" {shape: rectangle}
method_3_configuration_revert: "Method 3 — Configuration Revert" {shape: rectangle}
method_4_database_rollback: "Method 4 — Database Rollback" {shape: rectangle}
method_5_full_backup_restore: "Method 5 — Full Backup Restore" {shape: rectangle}
postrollback_validation: "Post-Rollback Validation" {shape: rectangle}
rollback_checklist: "Rollback Checklist" {shape: rectangle}

center -> decision_framework
center -> method_3_configuration_revert
center -> method_4_database_rollback
center -> method_5_full_backup_restore
center -> postrollback_validation
center -> rollback_checklist
```

## Decision Framework

```mermaid
flowchart TD
    A[Change Applied] --> B{Post-change\nvalidation}
    B -->|All checks pass| C[Declare success\nClose change ticket]
    B -->|Failure detected| D{Fix forward\nin < 30 min?}
    D -->|Yes| E[Attempt fix\nwith ops lead approval]
    D -->|No| F[ROLLBACK]
    E --> G{Fixed?}
    G -->|Yes| C
    G -->|No| F
    F --> H[Execute rollback]
    H --> I[Validate rollback]
    I --> J[Incident report\nand change re-plan]
```


```bash
# Windows — uninstall cumulative update
wusa /uninstall /kb:<KBnumber> /quiet /norestart
```

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

## Method 5 — Full Backup Restore

```bash
# Veeam — restore entire VM from backup
$backup = Get-VBRBackup -Name "Production VMs"
$restorePoint = Get-VBRRestorePoint -Backup $backup -Name "HOSTNAME" | Select-Object -Last 1
Start-VBRRestoreVM -RestorePoint $restorePoint -PowerState PowerOn
```

**Expected time:** 30–120 minutes depending on backup size.

## Post-Rollback Validation

```bash
systemctl --failed
journalctl -p err -n 50 --no-pager
curl -sk https://<app-url>/health

# Confirm the specific change is reverted
<version-check-command>   # e.g. rpm -q nginx, vmware -v
```

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
