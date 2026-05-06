# NetApp SnapMirror Lifecycle

## ONTAP Version Compatibility

SnapMirror requires the destination cluster to run an ONTAP version equal to or newer than the source. Replication to an older ONTAP version is not supported and will fail at initialization.

| Source ONTAP | Minimum Destination | Notes |
|---|---|---|
| ONTAP 9.14 | ONTAP 9.14 | Same version recommended for SMBC |
| ONTAP 9.12 | ONTAP 9.12 | Destination-first upgrade required |
| ONTAP 9.10 | ONTAP 9.10 | Check IMT for feature compatibility |
| ONTAP 9.8 | ONTAP 9.8 | XDP policy features vary by minor version |

Always consult the [NetApp Interoperability Matrix Tool (IMT)](https://mysupport.netapp.com/matrix) before upgrading either cluster in a SnapMirror relationship.

## Policy and Relationship Management

- Review all SnapMirror relationships annually; retire stale relationships for volumes that no longer exist or are no longer in active use
- Document the purpose of each relationship: DR relationship, vault/backup, dev-refresh, or cloud replication
- Confirm that the SnapMirror policy schedule still aligns with the documented RPO — business requirements can change without the replication configuration being updated
- Annual DR test validates relationship health; any relationship not tested within 12 months should be flagged for review and testing before renewal
- Remove relationships before decommissioning source volumes: `snapmirror quiesce`, `snapmirror break`, `snapmirror delete`; then delete the destination volume

## SMBC / SnapMirror Sync Mediator

ONTAP Mediator provides the out-of-band witness for SMBC automatic failover decisions. Mediator version must be compatible with the ONTAP version on both clusters.

- Mediator VM requires updates when ONTAP is upgraded — check the [SMBC Mediator compatibility matrix](https://mysupport.netapp.com/matrix) before any ONTAP upgrade
- Mediator must remain reachable from both clusters at all times; loss of mediator connectivity does not stop I/O but disables automatic failover
- Mediator runs as a Linux VM; patch the OS independently of ONTAP upgrade cycles

## Retention Cleanup

- SnapVault / XDP vault retained copies consume destination volume capacity independent of the source; retention rules must be reviewed to prevent destination from filling
- Review retention policies annually; prune excess retained copies using `snapshot delete` on the destination volume when snapshots exceed the documented retention window
- Set destination volume autogrow thresholds and alerts to detect capacity creep before it causes transfer failures
- When retiring a SnapVault relationship, decide whether to retain existing destination snapshots for compliance before deleting the relationship
