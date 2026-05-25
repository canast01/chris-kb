# FC Zoning

Zoning restricts which initiators (HBAs) can communicate with which targets (storage ports) in a Fibre Channel fabric.

```text
        ZONING: INITIATOR + TARGET → ZONE → ZONE SET → FABRIC
┌─────────────────────────────────────────────────────────────────┐
│  Zone: esxi01_pure01_ctA1                                       │
│  ┌───────────────────────┐    ┌───────────────────────────────┐ │
│  │ Initiator             │    │ Target                        │ │
│  │ WWPN: 21:00:00:xx:... │    │ WWPN: 50:00:99:xx:...        │ │
│  │ (Host HBA port)       │    │ (Storage ctrl port)           │ │
│  └───────────┬───────────┘    └────────────┬──────────────────┘ │
│              └──────────────┬──────────────┘                    │
│                             │ zone member                       │
│                      ┌──────▼──────┐                           │
│                      │  ZONE SET   │  ◄── cfgenable / activate  │
│                      │  PROD_CFG   │                            │
│                      └──────┬──────┘                           │
│                             │                                   │
│                      ┌──────▼──────┐                           │
│                      │   FABRIC    │  enforces zone membership  │
│                      │  (switches) │  blocks unlisted WWPNs     │
│                      └─────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
``` Every production fabric must have active zoning; unzoned fabrics allow all nodes to see each other.

## Zone Types

| Type | Membership | Notes |
|---|---|---|
| **WWN zoning** | World Wide Port Name | Preferred — survives port moves, hardware-independent |
| **Port zoning** | Switch domain:port | Rigid; breaks on HBA replacement or port change |
| **Mixed** | WWN + port | Avoid — complex and error-prone |

## Zoning Standards

- One initiator per zone — never put two initiators in the same zone
- Include all target ports the initiator should access
- Name zones: `<initiator-host>_<target-array>_<port>` e.g. `esxi01_pure01_ctA1`
- Use a single zoneset per fabric; activate on both switches in a dual-fabric config

## Brocade FOS — Zone Commands

```bash
# View active zoneset
cfgshow

# Create a zone
zonecreate "esxi01_pure01_ctA1", "21:00:00:xx:xx:xx:xx:xx;50:00:99:xx:xx:xx:xx:xx"

# Add zone to config
cfgadd "PROD_CFG", "esxi01_pure01_ctA1"

# Activate the config
cfgenable "PROD_CFG"

# Verify zone membership
zoneshow "esxi01_pure01_ctA1"

# Show all zones containing a WWN
nsallshow | grep <wwn>
```

## Cisco MDS / NX-OS — Zone Commands

```bash
# Show active zoneset
show zoneset active vsan 10

# Create zone
zone name esxi01_pure01_ctA1 vsan 10
  member pwwn 21:00:00:xx:xx:xx:xx:xx
  member pwwn 50:00:99:xx:xx:xx:xx:xx

# Add to zoneset and activate
zoneset name PROD_ZONESET vsan 10
  member esxi01_pure01_ctA1

zoneset activate name PROD_ZONESET vsan 10

# Verify
show zone name esxi01_pure01_ctA1 vsan 10
show zoneset active vsan 10
```

## Common Issues

| Symptom | Likely cause | Check |
|---|---|---|
| Host cannot see LUNs | Missing zone or wrong WWPN | `zoneshow` / `show zoneset active` |
| Zone works on one fabric, not the other | Zonesets not mirrored across fabrics | Compare active zonesets on both switches |
| New HBA not seen after zone change | Zone not activated after edit | `cfgenable` / `zoneset activate` |
| Performance issues after zoning change | Multiple initiators in same zone | Audit zone membership |
