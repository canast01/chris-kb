# ONTAP — Backup & Restore

> Backup configuration, restore procedures, and validation for NetApp ONTAP.

This page covers ONTAP-native backup and restore capabilities including snapshot-based recovery, SnapMirror failover, and integration with backup platforms.

## Snapshot-Based Restore

ONTAP snapshots are the primary on-array recovery mechanism. They are near-instant and do not require a separate backup infrastructure.

```bash
# List available snapshots for a volume
volume snapshot show -vserver <svm> -volume <vol>

# Restore a volume to a snapshot (volume must be offline or quiesced)
volume snapshot restore -vserver <svm> -volume <vol> -snapshot <snap_name>

# Online restore (non-disruptive for non-DR scenarios — requires SnapRestore license)
volume snapshot restore -vserver <svm> -volume <vol> -snapshot <snap_name> -online true
```

## SnapMirror Failover (DR Restore)

For disaster recovery, SnapMirror relationships replicate volumes to a secondary cluster. Failover involves breaking the relationship to make the destination writable.

```bash
# Break the SnapMirror relationship to activate the destination volume
snapmirror break -destination-path <dest_svm>:<dest_vol>

# After recovery, resync back to primary (reseeds from primary)
snapmirror resync -destination-path <dest_svm>:<dest_vol>
```

## SnapVault (Long-Term Retention)

SnapVault (XDP policy) creates independent backup copies on a secondary system with configurable retention policies — independent of the source snapshot schedule.

```bash
# View SnapVault relationships
snapmirror show -type XDP

# Initialize a SnapVault relationship
snapmirror initialize -destination-path <dest_svm>:<dest_vol>

# Manual backup update
snapmirror update -destination-path <dest_svm>:<dest_vol>
```

## SnapCenter Integration

SnapCenter provides application-consistent backup orchestration for ONTAP. It coordinates with VMware, Oracle, SQL Server, and other applications to ensure crash-consistent or application-consistent snapshots before triggering ONTAP snapshot creation. See the [SnapCenter section](../../../snapcenter/) for full coverage.

## Veeam Integration

Veeam Backup & Replication integrates with ONTAP storage snapshots via the storage integration plugin, enabling backup from storage snapshots without VM stun. See the [Integrations](../../architecture/integrations/) page for configuration details.

## Backup Validation Checklist

- [ ] Snapshot policies are configured and running on all protected volumes (`volume snapshot policy show`)
- [ ] SnapMirror lag is within RPO on all DR relationships (`snapmirror show -fields lag-time,healthy`)
- [ ] SnapVault relationships updated within retention schedule (`snapmirror show -type XDP`)
- [ ] Test restore performed from snapshot within the last 90 days
- [ ] SnapCenter or Veeam backup jobs showing success in the backup console
- [ ] AutoSupport delivering successfully — required for NetApp support to assist with data recovery
