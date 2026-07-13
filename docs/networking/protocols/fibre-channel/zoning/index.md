---
tags:
  - networking
description: "Zoning restricts which initiators (HBAs) can communicate with which targets (storage ports) in a Fibre Channel fabric."
---
# FC Zoning

<div class="kb-summary">
Zoning restricts which initiators (HBAs) can communicate with which targets (storage ports) in a Fibre Channel fabric.
</div>

Every production fabric must have active zoning; unzoned fabrics allow all nodes to see each other.

```d2
direction: down

zone_types: "Zone Types" {shape: rectangle}
zoning_standards: "Zoning Standards" {shape: rectangle}
brocade_fos_zone_commands: "Brocade FOS — Zone Commands" {shape: rectangle}
cisco_mds_nxos_zone_commands: "Cisco MDS / NX-OS — Zone Commands" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

zone_types -> zoning_standards: uses
zoning_standards -> brocade_fos_zone_commands: uses
brocade_fos_zone_commands -> cisco_mds_nxos_zone_commands: uses
cisco_mds_nxos_zone_commands -> common_issues: uses
```

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


```text title="Expected output"
Defined configuration:
 cfg:	PROD_CFG
 zone:	esxi01_pure01_ctA1
 zone:	esxi01_pure01_ctB2
 zone:	storage_backup_zone

Active configuration:
 cfg:	PROD_CFG

Zone esxi01_pure01_ctA1:
  21:00:00:0a:1b:2c:3d:4e
  50:00:99:ff:ee:dd:cc:bb

Zone esxi01_pure01_ctB2:
  21:00:00:5f:6g:7h:8i:9j
  50:00:99:aa:bb:cc:dd:ee

21:00:00:0a:1b:2c:3d:4e;esxi01_pure01_ctA1;PROD_CFG;Active
50:00:99:ff:ee:dd:cc:bb;esxi01_pure01_ctA1;PROD_CFG;Active
```

!!! warning "Common errors"
    **`Invalid WWN format`** — Ensure WWN is formatted as 16 hexadecimal characters separated by colons (e.g., `21:00:00:xx:xx:xx:xx:xx`).
    **`Zone already exists`** — Use `zonedelete` to remove the existing zone before recreating it with `zonecreate`.
    **`Configuration is already active`** — Deactivate the current config with `cfgdisable` before enabling a different one.
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


```text title="Expected output"
VSAN: 10
Zoneset Name: PROD_ZONESET
Zoneset ID: 0x0100007b
Number of zones: 3
Zone Name: esxi01_pure01_ctA1
  pwwn 21:00:00:0a:1b:2c:3d:4e
  pwwn 50:00:99:ff:ee:dd:cc:bb
Zone Name: esxi01_pure01_ctB1
  pwwn 21:00:00:0a:1b:2c:3d:4f
  pwwn 50:00:99:ff:ee:dd:cc:bc
Zone Name: storage_array_zone
  pwwn 50:00:14:40:12:34:56:78
  pwwn 50:00:14:40:12:34:56:79

VSAN: 10
Zoneset Name: PROD_ZONESET
Zoneset ID: 0x0100007b
Number of zones: 3
Zone Name: esxi01_pure01_ctA1
  pwwn 21:00:00:0a:1b:2c:3d:4e
  pwwn 50:00:99:ff:ee:dd:cc:bb
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode (use `config t` for terminal configuration) and check VSAN number exists with `show vsan`.
    **`% Zone member already exists`** — Remove the duplicate PWWN entry from the zone definition or use `no member pwwn <address>` before re-adding with correct syntax.
    **`% Zoneset activation failed: conflicting zones detected`** — Run `show zone conflicts vsan 10` to identify overlapping zone members and resolve duplicate PWWN assignments across zones.
## Common Issues

| Symptom | Likely cause | Check |
|---|---|---|
| Host cannot see LUNs | Missing zone or wrong WWPN | `zoneshow` / `show zoneset active` |
| Zone works on one fabric, not the other | Zonesets not mirrored across fabrics | Compare active zonesets on both switches |
| New HBA not seen after zone change | Zone not activated after edit | `cfgenable` / `zoneset activate` |
| Performance issues after zoning change | Multiple initiators in same zone | Audit zone membership |
