---
tags:
  - troubleshooting
  - veeam
  - backup
  - known-issues
---
# Veeam Backup & Replication — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Veeam bugs, error codes, and workarounds covering backup jobs, restore operations, and VMware integration.

*Applies to: Veeam B&R v12.x*
</div>

## Before you begin

- Veeam job errors appear in the job session details — double-click the session for step-by-step log.
- Veeam KB articles at `veeam.com/kb` by error code.
- Most VMware backup failures are VSS/snapshot issues on the guest or transport mode problems.

## VMware Backup

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Failed to create snapshot` on VM | Veeam v12.x | Existing snapshots on VM or consolidation required | Consolidate VM snapshots in vCenter; remove Veeam helper snapshots if orphaned | N/A |
| `An error occurred while consolidating disks` | Veeam v12.x | vCenter disk consolidation failing post-backup (VMDK lock) | Manually consolidate in vCenter; check ESXi host for locked VMDK | N/A |
| `Unable to truncate SQL logs` (app-aware processing) | Veeam v12.x | VSS writer failing on SQL Server in guest | Check VSS writer state in guest: `vssadmin list writers`; restart failing VSS writer service | N/A |
| Backup job switches to Network mode (unexpectedly slow) | Veeam v12.x | Hot-add or SAN transport failing silently; fallback to NBD | Check proxy VM: disk access or vCenter permissions; enable `failover to network mode = disabled` to force failure instead of silent fallback | N/A |

## Restore

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Instant Recovery VM shows `inaccessible` in vCenter | Veeam v12.x | iSCSI target from Veeam not connected to ESXi host | Disconnect and reconnect Instant Recovery disk; check Veeam iSCSI target on port 3260 | N/A |
| `Cannot restore — backup file is corrupted` | Veeam v12.x | Repository storage I/O error during backup write | Run `veeamzip -check` on backup file; use earlier restore point if available | N/A |

## Scale-Out Backup Repository (SOBR)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Capacity tier offload stuck | Veeam v12.x | S3 endpoint unreachable (port 443) | Verify TCP 443 from VBR server to S3 endpoint; check S3 credentials in SOBR settings | N/A |

## Ports

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Data mover connection timeout | Veeam v12.x | TCP 2500–5000 blocked between proxy and repository | Open TCP 2500–5000 between all Veeam proxies and repositories | N/A |

## See also

- [Veeam — Common Issues](common-issues.md)
- [Dell Data Domain — Known Issues](../../../storage/dell/data-domain/troubleshooting/known-issues/)
