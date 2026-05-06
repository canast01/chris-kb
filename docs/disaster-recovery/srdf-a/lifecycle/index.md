# SRDF/A Lifecycle

SRDF/A feature availability is tied to the HYPERMAX OS version running on each PowerMax array; always verify compatibility before upgrading either site. The SRDF license is node-locked to the array serial number and must be re-applied after a controller board replacement. Firmware upgrades for arrays with active SRDF/A pairs require pausing replication, performing the non-disruptive upgrade (NDU), and then resuming — consistency groups must be validated after resumption.

- **Version matrix**: Confirm HYPERMAX OS parity (or supported mixed versions) between source and target arrays.
- **Upgrade procedure**: Pause SRDF/A → NDU on source → NDU on target → resume → validate cycle state.
- **EOL tracking**: VMAX3/All-Flash families reached EOS; PowerMax 2000/8000 generation is current.
- **Consistency group migration**: Plan device group migration during low-change-rate windows to minimise initial sync time.
