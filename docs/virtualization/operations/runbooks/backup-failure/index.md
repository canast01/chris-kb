# VMware Backup Failure Runbook

## Identify Failed VMs

- Review the backup platform for failed or missed backup jobs
- Note the VM name, backup job name, error message, and failure time

## Review the Error Message

Common backup errors:
- Snapshot creation failure
- Snapshot consolidation warning
- Datastore out of space
- Network or proxy connectivity failure
- vCenter API error

## Check VM Snapshot State

- In vCenter: right-click the VM → Snapshots → Manage Snapshots
- Confirm no stale backup snapshots are present
- If consolidation is needed: right-click VM → Snapshots → Consolidate

## Check Datastore Free Space

- Confirm the datastore hosting the VM has sufficient free space
- Free space less than 10% can block snapshot creation

## Check Backup Proxy Health

- Confirm the backup proxy VM is powered on and reachable
- Review proxy logs in the backup platform

## Check Backup Repository

- Confirm the backup repository has sufficient free space
- Confirm the repository is accessible from the proxy

## Check vCenter Permissions

- Confirm the backup service account has the required vCenter permissions
- Review vCenter roles and recent permission changes

## Retry the Backup

- If the root cause is resolved, manually retry the backup job
- Monitor the retry and confirm it completes successfully

## Escalate Recurring Failures

- If the same VM fails repeatedly, escalate to the backup platform team
- Open a support case with the backup vendor if needed

## Document Resolution

- Update the backup platform job notes with the root cause and fix
- Update the incident ticket with findings and resolution
