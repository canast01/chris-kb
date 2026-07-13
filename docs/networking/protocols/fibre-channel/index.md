---
tags:
  - networking
description: "Fibre Channel reference — WWPN/WWNN addressing, zoning, fabric login (FLOGI), multipathing, and SAN fabric health."
---
# Fibre Channel

<div class="kb-summary">
Fibre Channel reference — WWPN/WWNN addressing, zoning, fabric login (FLOGI), multipathing, and SAN fabric health.
</div>

```xml

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="fabric-login/">
  <strong>Fabric Login</strong>
  <span>Fabric Login notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="paths/">
  <strong>Paths</strong>
  <span>Paths notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostic steps, and resolution guides.</span>
</a>

<a class="kb-card" href="wwns/"><strong>WWNs</strong><span>World Wide Names — WWPN/WWNN addressing, assignment, and management.</span></a>
<a class="kb-card" href="zoning/"><strong>Zoning</strong><span>FC fabric zoning — hard/soft zoning, zone sets, and best practices.</span></a>

</div>

## Key Concepts

| Concept | Description |
|---|---|
| WWN (World Wide Name) | 64-bit unique identifier for HBAs and storage ports |
| WWPN (Port Name) | WWN of a specific FC port |
| WWNN (Node Name) | WWN of the HBA adapter |
| FLOGI | Fabric Login — HBA registers with the switch |
| FCNS (Name Server) | Switch database mapping WWPN to FC address |
| Zone | Defines which initiators can see which targets |
| VSAN | Virtual SAN — logical fabric isolation on Cisco MDS |
| ISL | Inter-Switch Link — trunk between fabric switches |

## FC Port Speeds

| Speed | Standard |
|---|---|
| 8G | FC8 |
| 16G | FC16 |
| 32G | FC32 |
| 64G | FC64 |

## Health Checks — Cisco MDS

```

```bash
## Port status
show interface fc brief

## FLOGI database — confirmed logged-in devices
show flogi database

## FC Name Server — host-to-storage mapping
show fcns database

## Active zones
show zoneset active

## Interface error counters
show interface fc1/1 counters errors

## Port utilisation
show interface fc1/1 counters brief
```

```text title="Expected output"
Interface   Status       Speed    Role
fc1/1       online       16 Gbps  F-port
fc1/2       online       16 Gbps  F-port
fc1/3       online       16 Gbps  F-port
fc1/4       sfpAbsent    --       --
fc1/5       notConnected 16 Gbps  F-port

FLOGI Database:
 FCID       Port Name           Node Name           Interface
 0x010001   50:00:09:73:a1:2b:c0:01  50:00:09:73:a1:2b:c0:00  fc1/1
 0x010002   50:00:0b:44:d2:5e:f1:02  50:00:0b:44:d2:5e:f1:00  fc1/2
 0x010003   50:00:1a:88:c9:3f:b2:03  50:00:1a:88:c9:3f:b2:00  fc1/3

FCNS Database:
 Port ID    Port Name                    Node Name
 0x010001   esx-host-01.storage.local    esx-host-01-wwn
 0x010002   array-lun-02.storage.local   array-lun-02-wwn
 0x010003   backup-server.storage.local  backup-server-wwn

Active Zoneset: production_zones
 Zone: zone_esx_to_array
  Members: esx-host-01, storage-array-01

 Zone: zone_backup_to_array
  Members: backup-server, storage-array-01

Interface fc1/1 Error Counters:
 CRC Errors:           0
 Enc-Out Errors:       0
 Too Many BBB Errors:  0
 Link Failures:        0
 Loss of Sync:         0

Interface fc1/1 Counters (brief):
 Frames In:    2847392
 Frames Out:   2651847
 Bytes In:     1.2 GB
 Bytes Out:    987 MB
 Utilization:  34%
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid command` | Verify the switch model supports these show commands (some older switches use different syntax like `show interface fcp` instead of `show interface fc`). |
    | `FLOGI database is empty` | Confirm HBAs are properly zoned and logged in; check `show flogi database` for pending FLOGI requests with `show flogi pending`. |
    | `Interface fc1/1 not found` | Use `show interface fc brief` first to list valid port names, as numbering varies by switch model (e.g., `Ethernet1/1` vs `fc1/1`). |
```bash
## Switch and port status
switchshow

## Port error counters
porterrshow

## FLOGI entries
nsshow

## Active zoning
cfgshow | head -30
cfgactvshow

## Per-port stats
portshow <port-number>
```

```text title="Expected output"
Switch Information
    switchName:    fabric-switch-01
    switchType:    109.1
    switchState:   Online
    switchMode:    Native
    switchRole:    Principal
    Fabric ID:     1
    FC Address ID: 010000
    WWN:           50:00:14:40:66:8b:2d:e0
    Model:         Brocade G620
    Serial Num:    BES2410K123456
    FC Port Count: 16
    FC Ports Online: 14
    FC Ports Offline: 2
    FC Ports Testing: 0

Port Error Statistics:
    Port  0: Link Failures: 0, Loss of Sync: 0, Loss of Signal: 0
    Port  1: Link Failures: 2, Loss of Sync: 1, Loss of Signal: 0
    Port  2: Link Failures: 0, Loss of Sync: 0, Loss of Signal: 0
    Port  3: Link Failures: 127, Loss of Sync: 45, Loss of Signal: 12
    Port  4: Link Failures: 0, Loss of Sync: 0, Loss of Signal: 0
    ...

FLOGI Login Entries:
    Index Port   PWWN                   NWWN                   Fabric Login
    0     0      50:00:14:40:aa:bb:cc:01 50:00:14:40:aa:bb:cc:00 Yes
    1     1      50:00:14:40:dd:ee:ff:02 50:00:14:40:dd:ee:ff:00 Yes
    2     2      50:00:14:40:11:22:33:03 50:00:14:40:11:22:33:00 Yes

Defined configuration:
    cfg: fabric-prod
    cfg: fabric-backup
    cfg: fabric-test

Active configuration:
    cfg: fabric-prod
    Zone: prod-storage-zone
    Zone: prod-compute-zone
    Zone: prod-backup-zone

Port 3 Statistics:
    Port Speed: 16 Gbps
    Port Status: Online
    Frames Transmitted: 1847293
    Frames Received: 1923847
    Bytes Transmitted: 4782910234
    Bytes Received: 4921847293
    CRC Errors: 0
    Timeout Discards: 0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `switchshow: command not found` | Verify you are logged into the Fibre Channel switch via SSH/Telnet, not a Linux host; use `ssh admin@<switch-ip>` to connect. |
    | `Error: Port <port-number> does not exist` | Confirm the port number is within the valid range for your switch model (typically 0-15 for 16-port switches) using `switchshow` first. |
    | `Permission denied` | Ensure your user account has administrative privileges on the switch; contact your switch administrator to grant the necessary role. |
```bash
conf t
zone name <zone-name> vsan <vsan-id>
  member pwwn <host-wwpn>
  member pwwn <storage-wwpn>
zoneset activate name <zoneset-name> vsan <vsan-id>
```

```text title="Expected output"
config# conf t
config# zone name prod-zone-01 vsan 1
config-zone# member pwwn 50:00:14:40:5a:2b:c1:e0
config-zone# member pwwn 50:00:09:73:48:3f:a2:d1
config-zone# zoneset activate name prod-zoneset-01 vsan 1
Zoneset activation initiated. Please wait...
Zoneset prod-zoneset-01 activated successfully on VSAN 1.
config-zone# exit
config#
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid command` | Verify you are in the correct configuration mode (conf t) and that the switch supports zoning commands. |
    | `% Zone member already exists` | Remove the duplicate PWWN entry or use a different zone name before adding the member again. |
    | `% VSAN <vsan-id> does not exist` | Create the VSAN first using `vsan <vsan-id>` command before attempting to create zones in it. |
```bash
zoneadd "<zone-name>", "<wwpn>"
cfgsave
cfgenable "<zoneset-name>"
```


```text title="Expected output"
Zone configuration updated successfully.
Configuration saved to flash memory.
Zone set 'zoneset-name' enabled.
Zoning changes will take effect after fabric initialization.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Invalid WWPN format` | Ensure the WWPN is in the correct format (16 hexadecimal characters, typically formatted as xx:xx:xx:xx:xx:xx:xx:xx). |
    | `Zone name already exists` | Use a unique zone name or delete the existing zone before creating a new one with `zonedelete "<zone-name>"`. |
    | `Zone set does not exist` | Verify the zone set name exists with `cfgshow` before attempting to enable it. |