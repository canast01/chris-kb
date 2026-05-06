# Brocade Fabric OS Standards

Switch naming follows the convention `<site>-san-sw<nn>` (e.g., `lon-san-sw01`), with fabric A and fabric B distinguished by odd/even numbering. Domain IDs are allocated per fabric from a predefined range documented in the SAN design register, with production Fabric A using 1–20 and Fabric B using 21–40. Zone names use the format `<hostname>_<hba_port>-<arrayname>_<target_port>` (e.g., `web01_0-netapp01_0a`), and aliases follow the same naming fields individually. ISL trunks are configured between all core-edge switch pairs, and SNMP community strings are managed via the secrets vault with quarterly rotation.

| Item | Standard |
|---|---|
| Switch name | `<site>-san-sw<nn>` |
| Domain ID range (Fabric A) | 1–20 |
| Domain ID range (Fabric B) | 21–40 |
| Zone name format | `<host>_<hba>-<array>_<port>` |
| ISL configuration | Trunk groups, minimum 2 ISLs per pair |
| SNMP | Vault-managed, quarterly rotation |
