# SRDF/S Lifecycle

SRDF/S feature support is version-dependent on HYPERMAX OS; always verify that both arrays run a mutually supported OS version before enabling synchronous replication. Migration from VMAX SRDF/S to PowerMax involves establishing a new SRDF pair to the PowerMax target, performing a host-level cutover, and decommissioning the VMAX pair. During firmware upgrades, synchronous pairs are temporarily converted to asynchronous mode to avoid write-latency impact during the non-disruptive upgrade.

- **HYPERMAX OS compatibility**: Check Dell interoperability matrix for supported mixed-version pairing.
- **VMAX to PowerMax migration**: New SRDF pair creation → host cutover → old pair teardown.
- **Firmware upgrade**: Suspend to async → NDU source → NDU target → re-establish sync → validate `Synchronized` state.
- **Decommission procedure**: Quiesce host I/O → split pair → remove devices from SRDF group → delete group.
- **License lifecycle**: SRDF license is array-bound; track expiry dates in CMDB.
