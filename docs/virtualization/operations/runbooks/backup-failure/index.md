# VMware Backup Failure Runbook


<div class="kb-summary">
VMware Backup Failure Runbook reference covering Identify Failed VMs, Review the Error Message, Check VM Snapshot State, Check Datastore Free Space, Check Backup Proxy Health and 5 more sections.
</div>

```text
┌──────────────────────────────────── VMware Backup Failure Runbook ────────────────────────────────────┐
│                                                                                                       │
│    Identify failed VMs, diagnose the error, remediate, and verify before closing                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Identify + Diagnose              │  │                 Fix + Verify                │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │        Check console for failed jobs         │  │           Check VM snapshot state           │   │
│   │          Note VM, job, error, time           │  │          Right-click VM → Snapshots         │   │
│   │                Common errors:                │  │         Consolidate stale snapshots         │   │
│   │          · Snapshot creation failed          │  │         Free datastore space if full        │   │
│   │        · Snapshot consolidation warn         │  │           Fix proxy / network path          │   │
│   │           · Datastore out of space           │  │          Retry failed job manually          │   │
│   │          · Network / proxy failure           │  │             Verify job succeeded            │   │
│   │             · vCenter API error              │  │          Document in change record          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Snapshot      = Point-in-time copy of VM disk state; backup creates and removes per job            │
│    Consolidation = Merging leftover snapshot files into base disk; run if stale snap exists           │
│    Proxy         = Backup proxy server that performs data movement; check connectivity                │
│    CBT           = Changed Block Tracking; VMware API tracking changed disk blocks for backup         │
│    quiesce       = VSS snapshot with application-consistent state; fails if VMware tools old          │
│    Orphaned snap = Snapshot in datastore but not in vCenter; causes silent disk growth                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
