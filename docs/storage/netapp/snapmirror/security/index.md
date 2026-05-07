# NetApp SnapMirror Security
## Intercluster Authentication

Cluster peering uses a pre-shared passphrase negotiated at peer establishment time. The passphrase is used once to authenticate the relationship; subsequent replication traffic uses TLS-encrypted channels. From ONTAP 9.6 onwards, all intercluster communication is TLS encrypted by default. Cluster peer relationships should be reviewed annually and stale peers removed.

## Encryption in Transit

SnapMirror Transfer Data Encryption (TDE) encrypts replication traffic end-to-end between clusters. Encryption is configured per relationship and does not require IPsec on the network layer.

```bash
# Enable encryption on an existing SnapMirror relationship
snapmirror modify -destination-path svm_dst:vol_dst -encryption-algorithm aes-256

# Verify encryption is enabled
snapmirror show -destination-path svm_dst:vol_dst -fields encryption-algorithm
```

Encryption in transit is mandatory for any replication relationship crossing a network segment that is not fully controlled (e.g., WAN links, third-party interconnects).

## RBAC

- SnapMirror operations (`update`, `initialize`, `resync`, `show`) require `vsadmin` or cluster admin role
- `snapmirror break` and `snapmirror resync` must be restricted to designated DR admins — these operations change data access and replication direction
- Create a custom ONTAP role scoped to SnapMirror-only operations for teams that need monitoring access without the ability to break or resync relationships:

```bash
security login role create -role snapmirror-monitor -cmddirname "snapmirror show" -access readonly
security login role create -role snapmirror-monitor -cmddirname "snapmirror show-history" -access readonly
```

## Audit Logging

- All SnapMirror relationship changes (create, modify, delete, break, resync) are recorded in the ONTAP audit log
- EMS generates events for all transfer completions, failures, and lag threshold breaches — route these to your SIEM or syslog server
- Review audit logs after any DR test to confirm only authorized operations were performed

```bash
# Show recent SnapMirror-related EMS events
event log show -message-name snapmirror.*

# Show security audit log for relationship changes
security audit log show
```

## Destination Volume Protection

Destination (DP) volumes are read-only by design — the replication engine enforces this at the WAFL layer. No client or user can write to a destination volume while a SnapMirror relationship is active. This eliminates the risk of accidental data modification on the replication target. Access to the destination volume is restricted to the replication engine and cluster admin operations; no data LIFs serve the destination volume until a `snapmirror break` is explicitly run.
