# SnapMirror — Diagnostics

> Part of the [SnapMirror Troubleshooting](../index.md) reference.

---

## Diagnostic Commands

```bash
# Show all relationships with lag time and health
snapmirror show -fields lag-time,healthy,status

# Show full detail for a specific relationship
snapmirror show -destination-path svm_dst:vol_dst

# Show transfer history for a relationship
snapmirror show-history -destination-path svm_dst:vol_dst

# List all destination relationships across the cluster
snapmirror list-destinations

# Show intercluster LIF status
network interface show -role intercluster

# Check SMBC mediator connectivity
snapmirror mediator show

# Show relationships in broken-off state
snapmirror show -relationship-status broken-off

# Abort a stuck transfer
snapmirror abort -destination-path svm_dst:vol_dst
```

## Log Locations

- **ONTAP EMS log** — `event log show -severity error -time-range <start>..<end>`
- **SnapMirror-specific EMS events** — `event log show -message-name snapmirror.*`
- **Transfer history** — `snapmirror show-history -destination-path svm_dst:vol_dst`
- **System Manager** — Protection > Relationships view shows a visual timeline of transfer health
