# VMware Backup Standards


<div class="kb-summary">
VMware Backup Standards reference covering Critical VM Backup Policy, Standard VM Backup Policy, vCenter Backup, Snapshot Handling, Backup Monitoring and 2 more sections.
</div>

## Critical VM Backup Policy

- Daily backup minimum
- 30-day retention minimum
- Application-aware backup where supported
- Test restore at least quarterly

## Standard VM Backup Policy

- Daily or weekly backup
- 14-day retention minimum
- Restore test at least annually

## vCenter Backup

- File-based backup via VAMI daily
- Keep at least 3 copies
- Encryption password stored securely
- Backup target must be off the vSAN datastore

## Snapshot Handling

- Backup products must clean up their own snapshots after each job
- Alert if a backup snapshot is older than 24 hours
- Manual change-related snapshots must be removed within 48 hours

## Backup Monitoring

- Review backup job results daily
- Alert on any failed or missed backup
- Include backup status in the weekly health check

## Backup Failure Escalation

- Retry failed backup once
- If retry fails, investigate and escalate within 24 hours
- Critical VMs with no successful backup for more than 48 hours must be escalated immediately

## Backup Evidence Retention

- Keep backup job reports for 90 days
- Document restore tests with date and result
