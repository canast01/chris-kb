---
tags:
  - dr
---
# IRE — Restore


<div class="kb-summary">
Restoration in the IRE follows a staged process: identify the latest clean backup within the retention window that predates the compromise event, retrieve and mount it in isolation, restore to isolated staging, validate in the clean room, then reintroduce to production only after sign-off. Retention windows of 30–90 days are typical for ransomware scenarios.
</div>
![IRE — Restore](../../../../assets/backup-dr-operations-ire-restore-index.svg)


```d2
direction: right

center: "DR Operations" {shape: hexagon}
restore_workflow: "Restore Workflow" {shape: rectangle}
reintroduction_to_production: "Reintroduction to Production" {shape: rectangle}
restore_time_estimates: "Restore Time Estimates" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

center -> restore_workflow
center -> reintroduction_to_production
center -> restore_time_estimates
center -> common_issues
```

## Restore Workflow

```mermaid
flowchart TD
    A([Declare IRE activation]) --> B[Identify recovery point\nRTO / RPO target]
    B --> C[Retrieve backup from immutable store\nto IRE staging]
    C --> D[Restore VM images / data\nto IRE compute]
    D --> E[Malware scan in clean room]
    E --> F{Scan clean?}
    F --> |No| G[Quarantine\nSelect earlier recovery point]
    G --> B
    F --> |Yes| H[Business validation\nApp team testing]
    H --> I{Validated?}
    I --> |No| J[Investigate data issues\nSelect earlier point if needed]
    J --> B
    I --> |Yes| K[DR lead sign-off]
    K --> L[Reintroduce to production\nIRE isolation maintained until complete]
    L --> M([IRE stand-down])
```


### Database Restore

```sql
-- SQL Server: restore to IRE SQL instance (from backup file on shared storage)
RESTORE DATABASE [recovered_db]
FROM DISK = '\\ire-fileserver\backups\prod_db_20260510.bak'
WITH
  MOVE 'prod_db'     TO 'D:\Data\recovered_db.mdf',
  MOVE 'prod_db_log' TO 'D:\Log\recovered_db_ldf',
  NORECOVERY,    -- leave in restoring state for log restore
  REPLACE;

-- Apply transaction logs
RESTORE LOG [recovered_db]
FROM DISK = '\\ire-fileserver\backups\prod_db_log_20260510_2300.bak'
WITH RECOVERY;  -- bring online after final log
```

## Reintroduction to Production

Only after clean room sign-off:

1. **Networking** — establish a controlled one-way network path from IRE to production (IRE → prod only; no return path).
2. **DNS cutover** — update DNS records to point to restored systems.
3. **Monitoring** — connect restored systems to monitoring before traffic goes live.
4. **Traffic cutover** — move load balancer / DNS traffic incrementally (canary first if possible).
5. **IRE decommission** — shut down IRE VMs and revoke all IRE credentials after successful production handover.

## Restore Time Estimates

| Data volume | Backup type | Typical restore time |
|---|---|---|
| < 500 GB VM | Azure RSV restore | 1–3 hours |
| 1 TB database | Full backup + log restore | 2–4 hours |
| 10 TB NAS volume | Snapshot clone (Pure) | < 30 minutes (metadata only) |
| 50 TB NAS volume | Tape restore | 8–24 hours |

Snapshot-based restores (Pure, Azure snapshot) are near-instant for the clone operation; time is dominated by malware scanning and validation.

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| Restore job fails with storage error | Staging storage account not in IRE VNet / inaccessible | Verify storage account network rules include IRE subnet |
| Restored VM cannot boot | OS volume corrupted in the backup | Try one recovery point earlier; check backup consistency settings |
| Database restore leaves DB in restoring state | `NORECOVERY` used without subsequent log restore | Apply remaining logs then `RESTORE DATABASE WITH RECOVERY` |
| Snapshot clone is instant but data appears wrong | Wrong snapshot selected (post-compromise) | Review snapshot timestamps; select from before estimated attack start |
