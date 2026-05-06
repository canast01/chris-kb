# Brocade Fabric OS Standards

## Switch Naming

```
<site>-san-sw<nn>
```

| Site | Fabric A | Fabric B |
|---|---|---|
| DC1 | `dc1-san-sw01`, `dc1-san-sw03` | `dc1-san-sw02`, `dc1-san-sw04` |
| DC2 | `dc2-san-sw01`, `dc2-san-sw03` | `dc2-san-sw02`, `dc2-san-sw04` |

Convention: Fabric A = odd switch numbers, Fabric B = even. This makes fabric membership immediately identifiable from the hostname.

## Domain ID Allocation

Domain IDs must be unique within a fabric and allocated from a predefined range:

| Range | Fabric | Notes |
|---|---|---|
| 1–20 | Production Fabric A | Allocated from SAN design register |
| 21–40 | Production Fabric B | Separate range prevents conflicts |
| 41–60 | Replication Fabric | SRDF or RecoverPoint fabrics |
| 61–80 | DR Site Fabric A/B | Keep separate from production |

Document domain ID assignments in the SAN design register in CMDB.

## Zone and Alias Naming

```
Zone:   <hostname>_<hba_port>-<arrayname>_<target_port>
Alias:  <hostname>_<hba_port>   or   <arrayname>_<target_port>
```

Examples:
- Zone: `db01_0a-powermax01_0a` — host DB01 HBA0 port A to PowerMax array port 0A
- Alias: `db01_0a` (alias for the initiator WWPN), `powermax01_0a` (alias for target port)

Rules:
- One initiator per zone — never put two host WWPNs in the same zone
- Zones should contain: one host HBA port + required array target ports
- No single-target zones without a matching initiator (orphan cleanup)

## VSAN / Fabric Design

For Brocade, a single physical fabric spans all switches (unlike Cisco which uses VSANs):
- Production Fabric A: all switches in fabric A connected via ISLs
- Production Fabric B: all switches in fabric B — completely separate cable plant
- Switches must never be cabled between Fabric A and Fabric B

## ISL Standards

| Parameter | Standard |
|---|---|
| Minimum ISLs per switch pair | 2 (trunk group) |
| ISL speed | Equal to or greater than connected host/array port speed |
| Trunk group configuration | `porttrunkarea` configured on ISL ports |
| FSPF cost | Default (auto) unless explicit traffic engineering is required |

Verify trunk status:
```bash
trunkshow   # All ISL trunks and member ports
islshow     # ISL utilisation
```

## Security Standards

| Control | Standard |
|---|---|
| SNMP | SNMPv3 only; community strings in vault; quarterly rotation |
| Management access | SSH only; Telnet disabled; `sshutil disable telnet` |
| RADIUS/TACACS+ | All fabrics must use central AAA; local accounts for break-glass only |
| Audit logging | `auditcfg --set 1` — all logins and config changes logged |

## Firmware Standards

- All switches in a fabric must run the same Fabric OS version (FOS)
- New FOS versions applied to Fabric B first, validated, then Fabric A
- Minimum: stay within 1 major FOS version of Broadcom's current release
- Check FOS EOL: [support.broadcom.com](https://support.broadcom.com) → Product Lifecycle
