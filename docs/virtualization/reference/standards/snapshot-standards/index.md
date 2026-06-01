# VMware Snapshot Standards


<div class="kb-summary">
VMware Snapshot Standards reference covering Snapshots Are Temporary, Approved Use Cases, Maximum Snapshot Age, Snapshot Size Monitoring, Cleanup Responsibility and 3 more sections.
</div>

## Snapshots Are Temporary

Snapshots are not backups. They should be used for short-term protection during changes and removed after validation.

## Approved Use Cases

- Pre-change snapshot during a maintenance window
- Backup product snapshots (managed by the backup tool)
- Temporary rollback point during a test or upgrade

## Maximum Snapshot Age

- Change-related snapshots: remove within 24–48 hours of change completion
- Test snapshots: remove within the agreed test period
- No snapshot should remain for more than 7 days without review

## Snapshot Size Monitoring

- Monitor snapshot size via Aria Operations or vCenter alarms
- Large snapshots consume datastore capacity and degrade VM performance

## Cleanup Responsibility

- The team that created the snapshot is responsible for removing it
- Snapshots left by backup products are managed by the backup team

## Alerting for Old Snapshots

- Configure vCenter or Aria Operations to alert on snapshots older than 3 days
- Review the snapshot report weekly

## Risk of Long-Running Snapshots

- Snapshot files grow continuously as the VM writes data
- Committing a large snapshot can cause temporary VM storage performance impact
- Datastores can fill unexpectedly due to uncontrolled snapshot growth

## Emergency Consolidation

If a snapshot cannot be deleted cleanly:
1. Check for running consolidation tasks in vCenter
2. Right-click VM → **Snapshot** → **Consolidate**
3. If consolidation fails, open a VMware support case — do not attempt forced removal without guidance
