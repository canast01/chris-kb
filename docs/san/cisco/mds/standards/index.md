# Cisco MDS Standards

Switch naming follows the convention `<site>-mds-sw<nn>` (e.g., `lon-mds-sw01`), with Fabric A and Fabric B distinguished by odd/even numbering. VSANs are allocated by function: production (VSAN 10/11), replication (VSAN 20/21), and management (VSAN 99), with Fabric A and B using separate VSAN IDs. Zone names use the format `<hostname>_<hba>-<arrayname>_<port>` consistent with Brocade standards for cross-fabric readability. NTP, SNMP, and AAA (TACACS+/RADIUS) are configured from a standard baseline template applied at switch provisioning. Port-channel ISLs require a minimum of two physical links per channel group.

| Item | Standard |
|---|---|
| Switch name | `<site>-mds-sw<nn>` |
| Production VSAN (Fabric A/B) | 10 / 11 |
| Replication VSAN (Fabric A/B) | 20 / 21 |
| Zone name format | `<host>_<hba>-<array>_<port>` |
| ISL port-channel | Minimum 2 links per channel group |
| AAA | TACACS+ primary, RADIUS fallback |
