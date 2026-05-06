# SRDF/S CLI Reference

All SRDF/S management is performed via SYMCLI (Solutions Enabler). Commands require appropriate RBAC permissions and must be run from a Solutions Enabler host with connectivity to the target array. Always specify `-g <group>` to scope operations to the correct SRDF group and avoid unintended impact to other pairs.

| Command | Purpose |
|---|---|
| `symrdf query -g <group>` | Show pair states for all devices in the group |
| `symrdf list -v` | List all SRDF groups with verbose state detail |
| `symrdf establish -g <group>` | Establish (re-sync) an SRDF pair |
| `symrdf suspend -g <group>` | Suspend replication (converts to async temporarily) |
| `symrdf failover -g <group>` | Perform a failover to the R2 (target) side |
| `symrdf failback -g <group>` | Fail back to the original R1 (source) side |
| `symrdf resync -g <group>` | Resynchronise after a split or failover |
| `symcfg list -rdfg` | List all SRDF groups and port/link states |
| `symdg list` | List device groups including SRDF group membership |
