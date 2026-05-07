# SnapCenter Backup Jobs
## Viewing Job History

In the SnapCenter UI:
1. Navigate to **Monitor → Jobs**
2. Filter by resource group, policy, or date range
3. Click a job to view detailed logs

Job statuses:
| Status | Meaning |
|---|---|
| Completed | Backup succeeded |
| Completed with warnings | Succeeded with non-critical issues |
| Failed | Backup failed — review job log |
| Running | Job in progress |

## Running a Backup On-Demand

1. Navigate to **Resources** → select the resource group or resource
2. Click **Back Up Now**
3. Select the policy to apply
4. Confirm and monitor via **Monitor → Jobs**

## Checking Backup Copies

```
Resources → [Select Resource] → Manage Copies → Snapshots
```

Verify:
- Most recent snapshot timestamp
- Retention count matches policy
- SnapMirror copy (if configured) is present

## Troubleshooting Failed Jobs

1. Open the failed job in **Monitor → Jobs**
2. Review the job log for the error step
3. Common causes:
   - Plugin not responding on host
   - Snapshot creation failed (array busy or full)
   - SnapMirror update failed after snapshot

```bash
# Check ONTAP for snapshot-related errors
event log show -severity error -time ">1h"

# Check SnapMirror status
snapmirror show -health false
```

## Backup Retention

- Retention is defined in the policy applied to the resource group
- SnapCenter enforces retention by deleting older snapshots automatically
- Verify retention compliance under **Resources → Manage Copies**

## Re-running a Failed Backup

1. Resolve the root cause (plugin, storage, network)
2. Navigate to **Monitor → Jobs** → right-click failed job → **Re-run**
   — or —
   Run a new on-demand backup

## Common Issues

| Issue | Cause | Action |
|---|---|---|
| Plugin host unreachable | Agent offline | Restart SnapCenter plugin service on host |
| Snapshot creation failed | Array busy | Retry; check ONTAP alerts |
| SnapMirror update failed | Destination unreachable | Check SnapMirror relationship |
| Retention not enforced | Policy misconfiguration | Review and reapply retention policy |
