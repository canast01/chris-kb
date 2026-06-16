---
tags:
  - netapp
  - operations
---
# SnapMirror — Install & Upgrade


<div class="kb-summary">
SnapMirror install and upgrade: ONTAP cluster peering prerequisites, intercluster LIF creation, and SnapMirror policy migration between ONTAP major versions.

*Applies to: SnapMirror*
</div>
```text
┌─────────────────────────────── NetApp SnapMirror — Install and Upgrade ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SnapMirror installation and upgrade: deployment and version management procedures       │   │
│   │         Pre-upgrade: back up configuration, check compatibility, review release notes         │   │
│   │      Upgrade: rolling upgrade preserves service; non-disruptive on dual-controller arrays     │   │
│   │           Post-upgrade: verify all services running; run health check; notify users           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Plan → backup config → upgrade staging → upgrade production → validate                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Async            │  │        Periodic sync        │  │         RPO: minutes        │   │
│   │             Sync            │  │           Zero RPO          │  │          Sub-ms lag         │   │
│   │            SM-BC            │  │        Active-active        │  │        Transparent FO       │   │
│   │            Vault            │  │        Long retention       │  │         Backup copy         │   │
│   │            Cloud            │  │         ONTAP → CVO         │  │       Cloud DR/backup       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │ Async SnapMirror │  DR replication  │    SM protocol    │   Certificate    │   RPO minutes    │   │
│   │ Sync SnapMirror  │  Zero-RPO sync   │    SM protocol    │   Certificate    │ StrictSync/Sync  │   │
│   │      SM-BC       │ Active-active SA │    SM protocol    │     Mediator     │    No RPO/RTO    │   │
│   │    SnapVault     │ Backup retention │    SM protocol    │   Certificate    │ Longer retentio  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Source ONTAP cluster · destination ONTAP cluster · intercluster LIFs · WAN link          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapMirror         = ONTAP replication; transfers only changed blocks after initial baseline sync  │
│    Intercluster LIF   = dedicated logical interface for SnapMirror traffic between clusters           │
│    SnapMirror policy  = defines schedule, retention, and transfer type (async/sync/vault)             │
│    Baseline transfer  = first full snapshot transfer establishing the SnapMirror relationship         │
│    Update             = incremental transfer; only sends new or changed blocks since last successfu...│
│    Snapmirror break   = breaks the DR relationship; activates destination volume for read-write       │
│    Resync             = re-establishes a broken SnapMirror relationship from the last common snapshot │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN volumes│
│    Mediator           = ONTAP Mediator; quorum service for SM-BC running on Linux VM at third site    │
│    SnapVault          = SnapMirror variant for backup retention; destination has independent schedule │
│    MirrorAndVault     = policy combining SnapMirror DR and SnapVault backup retention copies          │
│    Fanout             = single source volume replicating to multiple destination clusters simultane...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## ONTAP Version Compatibility

SnapMirror requires the destination cluster to run an ONTAP version equal to or newer than the source. Replication to an older ONTAP version is not supported and will fail at initialization.

| Source ONTAP | Minimum Destination | Notes |
|---|---|---|
| ONTAP 9.14 | ONTAP 9.14 | Same version recommended for SMBC |
| ONTAP 9.12 | ONTAP 9.12 | Destination-first upgrade required |
| ONTAP 9.10 | ONTAP 9.10 | Check IMT for feature compatibility |
| ONTAP 9.8 | ONTAP 9.8 | XDP policy features vary by minor version |

Always consult the [NetApp Interoperability Matrix Tool (IMT)](https://imt.netapp.com/matrix/imt.html) before upgrading either cluster in a SnapMirror relationship.

## Policy and Relationship Management

- Review all SnapMirror relationships annually; retire stale relationships for volumes that no longer exist or are no longer in active use
- Document the purpose of each relationship: DR relationship, vault/backup, dev-refresh, or cloud replication
- Confirm that the SnapMirror policy schedule still aligns with the documented RPO — business requirements can change without the replication configuration being updated
- Annual DR test validates relationship health; any relationship not tested within 12 months should be flagged for review and testing before renewal
- Remove relationships before decommissioning source volumes: `snapmirror quiesce`, `snapmirror break`, `snapmirror delete`; then delete the destination volume

## SMBC / SnapMirror Sync Mediator

ONTAP Mediator provides the out-of-band witness for SMBC automatic failover decisions. Mediator version must be compatible with the ONTAP version on both clusters.

- Mediator VM requires updates when ONTAP is upgraded — check the [SMBC Mediator compatibility matrix](https://imt.netapp.com/matrix/imt.html) before any ONTAP upgrade
- Mediator must remain reachable from both clusters at all times; loss of mediator connectivity does not stop I/O but disables automatic failover
- Mediator runs as a Linux VM; patch the OS independently of ONTAP upgrade cycles

## Retention Cleanup

- SnapVault / XDP vault retained copies consume destination volume capacity independent of the source; retention rules must be reviewed to prevent destination from filling
- Review retention policies annually; prune excess retained copies using `snapshot delete` on the destination volume when snapshots exceed the documented retention window
- Set destination volume autogrow thresholds and alerts to detect capacity creep before it causes transfer failures
- When retiring a SnapVault relationship, decide whether to retain existing destination snapshots for compliance before deleting the relationship

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Snapmirror — Procedures](procedures/)
- [Snapmirror — Health Checks](health-checks/)
- [Snapmirror — Deploy](../deploy/)
