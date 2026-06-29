---
tags:
  - operations
  - san
---
# Cisco MDS 9000 — Common Operational Issues
![Cisco MDS 9000 — Common Operational Issues](../../../../assets/san-cisco-mds-operations-common-issues.svg)

```bash
# Identify the port and check detailed status
show interface fc1/3

# Check SFP / transceiver health
show interface fc1/3 transceiver

# Look for port error reason
show interface fc1/3 | include reason

# Check recent log events for this interface
show logging last 100 | grep fc1/3
```


```text title="Expected output"
fc1/3 is up
  Hardware is Fibre Channel, SFP is present
  Port WWN is 50:00:09:73:00:12:a4:5c
  Admin port mode is F, Oper port mode is F
  Allowed speeds: 1,2,4,8,16 Gbps
  Operating speed: 16 Gbps
  Flow Control is off
  Receive data (Mb/s): 1247, Transmit data (Mb/s): 892
  Frames transmitted: 45821903, Frames received: 48392847
  Errors: 0, Discards: 0, CRC: 0

SFP Information for fc1/3:
  SFP is present
  Type: LC connector
  Transceiver is present
  Part Number: XCVR-FC16G-SW
  Serial Number: FDO2412A1K5
  Transceiver temperature: 38 degrees Celsius
  Transceiver voltage: 3.31 Volts
  Transceiver current: 42.3 mA
  Transceiver RX power: -2.1 dBm
  Transceiver TX power: -1.8 dBm

(no output — command completes silently)

2024 Jan 15 14:22:31 +00:00 mds-switch-01 %MDS-4-LINK_UP: Interface fc1/3, changed state to up
2024 Jan 15 14:22:28 +00:00 mds-switch-01 %MDS-4-LINK_DOWN: Interface fc1/3, changed state to down
2024 Jan 15 14:22:15 +00:00 mds-switch-01 %MDS-3-XCEIVER_TEMP_WARNING: Transceiver temperature on fc1/3 is 68 degrees
```

!!! warning "Common errors"
    **`Invalid command`** — Verify the interface exists with `show interface brief` and use correct syntax like `show interface fc1/3` (not `show interface fc 1/3`).
    **`% Invalid command`** — Ensure you are in the correct CLI mode; use `config terminal` if configuration commands are needed, or exit to privileged EXEC mode with `exit`.
    **`Interface fc1/3 does not exist`** — Confirm the port number is valid for your MDS model using `show interface brief | grep fc` and check if the module is installed.
```bash
# Find the reason for errDisabled
show interface fc1/4 | include err

# Check recent log for the error event
show logging last 100 | grep fc1/4
```

```text title="Expected output"
fc1/4 is err-disabled
fc1/4 is Ethernet, SFP 8Gfc
  MTU 2176 bytes, type is -- Fibre Channel
  Port mode is F, FCID is 0x620400
  Speed is 8 Gb/s
  Transmit B2B Credit is 0
  Receive B2B Credit is 0
  RxQ U: 0/2048 P: 0/2048 C: 0/2048
  Trunk port: Disabled
  Trunking mode: OFF
  Error Disabled: loopback-detected
  Last clearing of "show interface" counters: 1d2h

2024 Jan 15 14:32:18 +00:00 mds9710-switch %MDS-4-FCERR_LOOPBACK_DETECTED: Loopback detected on port fc1/4
2024 Jan 15 14:32:17 +00:00 mds9710-switch %MDS-3-FCERR_LINK_FAILURE: Link failure on port fc1/4 (reason code: 0x4)
2024 Jan 15 14:32:15 +00:00 mds9710-switch %MDS-2-FCERR_INVALID_ATTACH: Invalid attach on port fc1/4
2024 Jan 15 14:32:12 +00:00 mds9710-switch %MDS-3-FCERR_SPEED_MISMATCH: Speed mismatch detected on port fc1/4 (local 8Gb/s, remote 4Gb/s)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct mode (enable mode required); use `enable` command first.
    **`% Ambiguous command: "show interface fc1/4 | include err"`** — Use pipe syntax correctly with `show interface fc1/4 | include "err-disabled"` or remove the pipe and use `show interface fc1/4` to view full details.
```bash
# After resolving the root cause:
interface fc1/4
  shutdown
  no shutdown

# Confirm port comes up
show interface fc1/4
```
```d2
direction: right

A: "Host cannot see storage" {shape: rectangle}
B: "show flogi database vsan 10\n| grep host-pwwn" {shape: rectangle}
C: "Host in\nFLOGI?" {shape: rectangle}
D: "Check port state\nCheck VSAN assignment\nCheck cable and SFP" {shape: rectangle}
E: "show flogi database vsan 10\n| grep storage-pwwn" {shape: rectangle}
F: "Storage in\nFLOGI?" {shape: rectangle}
G: "Check array port state\nCheck VSAN membership on array port" {shape: rectangle}
H: "show zone member pwwn\nhost-pwwn vsan 10" {shape: rectangle}
I: "Zone with both\ndevices exists?" {shape: rectangle}
J: "Create zone with initiator\nand target device aliases\nActivate zone set" {shape: rectangle}
K: "show zoneset active vsan 10\n| grep zone-name" {shape: rectangle}
L: "Zone set\nactive?" {shape: rectangle}
M: "zoneset activate name\nzoneset-name vsan 10" {shape: rectangle}
N: "Verify WWPNs in zone match\nFLOGI pWWN exactly\nCheck for alias typos" {shape: rectangle}

A -> B
B -> C
C -> D
C -> E
E -> F
F -> G
F -> H
H -> I
I -> J
I -> K
K -> L
L -> M
L -> N
```
```bash
# Step 1 — Is the host HBA logged into the fabric?
show flogi database vsan 10 | grep <host-pwwn>
# If missing: the HBA hasn't logged in — check port state and VSAN assignment

# Step 2 — Is the storage target logged in?
show flogi database vsan 10 | grep <storage-pwwn>

# Step 3 — Is there a zone containing both?
show zone member pwwn <host-pwwn> vsan 10
# Output should show the zone name and the storage port alias

# Step 4 — Is the zone set active?
show zoneset active vsan 10 | grep <zone-name>

# Step 5 — Are both devices in the same VSAN?
show vsan membership interface fc<x/y>   # for host port
show vsan membership interface fc<x/z>   # for storage port
```

```text title="Expected output"
FLOGI Database for VSAN 10:
PWWN: 50:00:14:40:5b:2c:a1:e0  (Host: esx-prod-01)  LoggedIn
PWWN: 50:00:0b:42:3d:1f:c8:7a  (Storage: netapp-svm01)  LoggedIn

Zone Member Information for PWWN 50:00:14:40:5b:2c:a1:e0 in VSAN 10:
Zone Name: prod_esx_to_netapp
  Member: 50:00:14:40:5b:2c:a1:e0 (esx-prod-01)
  Member: 50:00:0b:42:3d:1f:c8:7a (netapp-svm01)

Active ZoneSet for VSAN 10:
ZoneSet Name: prod_zoneset_active
  Zone: prod_esx_to_netapp  Status: Active

VSAN Membership:
Interface fc4/12 is in VSAN 10
Interface fc5/8 is in VSAN 10
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the exact PWWN format (50:00:xx:xx:xx:xx:xx:xx) and ensure you're using the correct show command syntax for your MDS firmware version.
    **`% No matching entries found`** — Check that the host HBA has completed FLOGI login by verifying port status with `show interface fc<x/y>` and confirming the VSAN is assigned to that port.
    **`Zone member not found in active zoneset`** — Activate the zoneset containing both devices using `zoneset activate name <zoneset-name> vsan 10` and verify with `show zoneset active vsan 10`.
```bash
# Check zone status for errors
show zone status vsan 10

# Common cause: enhanced zoning enabled and commit required
zone commit vsan 10

# Then activate
zoneset activate name <zoneset-name> vsan 10
```

```text title="Expected output"
VSAN: 10
zoneset name: production-zoneset
zone name: zone-db-servers
  members:
    50:00:09:73:00:12:34:56 (Storage-Array-01)
    50:00:09:73:00:12:34:57 (Storage-Array-02)
zone name: zone-app-servers
  members:
    50:00:0a:8b:00:45:67:89 (AppServer-01)
    50:00:0a:8b:00:45:67:8a (AppServer-02)

Zoning session in progress. Commit required.

Zone commit in progress...
Commit successful. All changes have been committed to VSAN 10.

Zoneset activation in progress...
Zoneset 'production-zoneset' activated successfully for VSAN 10.
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the zoneset name exists with `show zoneset name <zoneset-name> vsan 10` before activation.
    **`% Zoning session in progress. Commit required.`** — Run `zone commit vsan 10` to commit pending changes before attempting activation.
    **`% VSAN 10 does not exist`** — Confirm the VSAN is created and active with `show vsan` before executing zone commands.
```bash
# Verify current alias-to-WWPN mapping
show device-alias database | grep <alias-name>

# Verify active zone members (resolved WWPNs)
show zoneset active vsan 10

# If stale: deactivate, re-commit alias DB, reactivate
device-alias commit
zoneset activate name <zoneset-name> vsan 10
```

```text title="Expected output"
device-alias name prod-storage-01 pwwn 50:00:14:40:5a:2c:8b:9f
device-alias name prod-storage-02 pwwn 50:00:14:40:5a:2c:8b:a0

zone name prod-zone vsan 10
  member pwwn 50:00:14:40:5a:2c:8b:9f
  member pwwn 20:00:00:0b:84:d1:4f:2e
zone name backup-zone vsan 10
  member pwwn 50:00:14:40:5a:2c:8b:a0
  member pwwn 20:00:00:0b:84:d1:4f:2f

Zoneset name prod-zoneset vsan 10 activated
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode (enter `config t` first if needed).
    **`% Zoneset activation failed: database commit in progress`** — Wait 30 seconds for the previous commit to complete, then retry the zoneset activation.
```bash
# List all zones in VSAN
show zone vsan 10

# Find zones containing a specific WWPN no longer in FLOGI
show zone member pwwn <old-pwwn> vsan 10

# Remove the member from the zone
zone name <zone-name> vsan 10
  no member device-alias <old-alias>

# Activate and commit
zoneset activate name <zoneset-name> vsan 10
zone commit vsan 10
copy running-config startup-config
```

```text title="Expected output"
VSAN: 10
  zone name prod-db-zone
    member device-alias prod-db-01
    member device-alias prod-db-02
    member device-alias san-switch-01
  zone name backup-zone
    member device-alias backup-01
    member device-alias backup-02
  zone name legacy-zone
    member pwwn 50:00:14:40:5a:2b:c1:e0

Zone member information for PWWN 50:00:14:40:5a:2b:c1:e0 in VSAN 10:
  Zone: legacy-zone
    Status: Active

(no output — command completes silently)

Zoneset name prod-zoneset activated successfully for VSAN 10
Zone commit successful for VSAN 10
Copy complete
```

!!! warning "Common errors"
    **`ERROR: Zone <zone-name> does not exist in VSAN 10`** — Verify the exact zone name with `show zone vsan 10` and ensure you're in the correct VSAN.
    **`ERROR: Member device-alias <old-alias> not found in zone <zone-name>`** — Confirm the device-alias exists in the zone using `show zone member` before attempting removal.
    **`ERROR: Zoneset <zoneset-name> is currently active and cannot be modified`** — Deactivate the zoneset first with `no zoneset activate name <zoneset-name> vsan 10` before making changes.
```bash
# Check ISL port detail
show interface fc2/1

# Check trunk state
show trunk

# Check port-channel (if ISLs are bundled)
show port-channel summary
show interface san-port-channel 1

# Check topology
show topology
show fcdomain domain-list vsan 10
```

```text title="Expected output"
fc2/1 is trunking
  Hardware is Fibre Channel, SFP is present
  Port WWN is 50:00:09:73:a2:1c:5f:01
  Admin port mode is F, Oper port mode is F
  Trunk mode is ON
  Trunk allowed VLANs on this Port: 1-4094
  Operational Speed is 16 Gbps
  Rate mode is dedicated
  Port mode is TL Port
  Transmit B2B Credit is 64

Trunk Information
  Trunk ID: 1
  Trunk State: up
  Trunk Master: mds9710-1
  Trunk Members: 2
    mds9710-1 fc2/1
    mds9710-2 fc2/1

Port-channel Summary
  Group  Port-channel  Protocol  Ports
  ------+-------------+---------+---------------------------------------------
  1      san-port-channel 1  FSPF    fc2/1(P)  fc2/2(P)  fc2/3(P)

san-port-channel 1 is up
  Hardware is Port Channel
  Port WWN is 50:00:09:73:a2:1c:5f:10
  Admin port mode is F, Oper port mode is F
  Speed is 48 Gbps
  Transmit B2B Credit is 192

Topology Information
  Switch WWN: 50:00:09:73:a2:1c:5f:00
  Switch Name: mds9710-1
  Switch Domain ID: 1
  Fabric Name: prod-san-fabric

Domain List for VSAN 10
  Domain ID  Switch Name          WWN
  ---------  -------------------  -------------------------
  1          mds9710-1            50:00:09:73:a2:1c:5f:00
  2          mds9710-2            50:00:09:73:a2:1c:5f:80
  3          mds9710-3            50:00:09:73:a2:1c:5f:81
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct mode (use `config terminal` for configuration commands, or ensure you are in exec mode for show commands).
    **`% Port fc2/1 does not exist`** — Confirm the port number is valid for your MDS model and that the module is installed and online using `show module`.
```bash
# Confirm rapid flap events in log
show logging last 100 | grep fc1/6

# Check error counters
show interface fc1/6 counters errors

# Check SFP optical power
show interface fc1/6 transceiver
```

```text title="Expected output"
2024 Jan 15 14:32:18 +00:00 mds9148-switch1 %ETHPORT-5-IF_DOWN_LINK_FAILURE: Interface fc1/6 is down (Link failure or not operational at received power level)
2024 Jan 15 14:32:22 +00:00 mds9148-switch1 %ETHPORT-6-IF_UP: Interface fc1/6 is up in mode F
2024 Jan 15 14:32:28 +00:00 mds9148-switch1 %ETHPORT-5-IF_DOWN_LINK_FAILURE: Interface fc1/6 is down (Link failure or not operational at received power level)
2024 Jan 15 14:32:35 +00:00 mds9148-switch1 %ETHPORT-6-IF_UP: Interface fc1/6 is up in mode F
2024 Jan 15 14:33:01 +00:00 mds9148-switch1 %ETHPORT-5-IF_DOWN_LINK_FAILURE: Interface fc1/6 is down (Link failure or not operational at received power level)

Interface fc1/6
  Errors:
    CRC errors:                    847
    Encoding disparity errors:     0
    Frames too long:               0
    Frames too short:              0
    Link failures:                 23
    Loss of signal:                19
    Loss of sync:                  18
    Primitive sequence protocol errors: 0

SFP Information for fc1/6:
  Transceiver is present
  Type: SFP+ (SFP+ 10Gb Fibre Channel)
  Identifier: 0x03
  Connector type: LC
  Encoding: 64B66B
  Nominal Bit Rate: 4300 MBps
  Link length SM: 10 km
  Vendor Name: FINISAR CORP
  Vendor OUI: 00 90 65
  Vendor PN: FTLX8571D3BCL
  Vendor SN: UY34K2A
  Transceiver Temp: 38 degrees Celsius
  Transceiver Voltage: 3.29 V
  Current Tx Power: -2.1 dBm
  Current Rx Power: -18.7 dBm
```

!!! warning "Common errors"
    **`show: command not found`** — Prepend the command with `conf t` context or use the full `show` syntax; if in bash, use `ssh admin@switch "show logging last 100 | grep fc1/6"` to run on the MDS device.
    **`Interface fc1/6 is administratively down`** — Enable the interface with `no shutdown` in interface configuration mode before checking counters.
    **`Current Rx Power: -24.3 dBm`** — Replace the SFP transceiver as optical power is below the -20 dBm minimum threshold for reliable operation.
```bash
interface fc1/6
  shutdown
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Ensure you are in the correct configuration mode by entering `config t` before issuing interface commands.
    **`% Interface does not exist`** — Verify the interface exists on your MDS switch using `show interface brief` before attempting to configure it.
```bash
# Check overall CPU
show system resources

# Identify the top consuming process
show processes cpu sort | head -20

# Check if port flap storm is the cause (high FC-related process CPU)
show logging last 200 | grep -i "link down\|flogi"
```

```text title="Expected output"
System Memory Information:
  Total Memory:    8192 MB
  Used Memory:     6144 MB
  Free Memory:     2048 MB
  Memory Usage:    75%

CPU States   : 42% user, 18% system, 5% nice, 35% idle
CPU0         : 45% user, 16% system, 4% nice, 35% idle
CPU1         : 39% user, 20% system, 6% nice, 35% idle

PID    Name                 CPU Time   %CPU
1234   fspf                 02:34:12   18.5
5678   fcns                 01:45:33   12.3
9012   fcs                  01:23:45   8.7
3456   snmp                 00:56:22   5.2
7890   syslogd              00:34:11   3.1
2345   vsan_mgr             00:28:09   2.8
6789   ipv4_mgr             00:19:45   1.9
...

2024 Jan 15 14:32:18 +00:00 mds9710-1 %FSPF-2-LINK_DOWN: Link 0/1 (FC1/1) down
2024 Jan 15 14:32:19 +00:00 mds9710-1 %FC-2-FLOGI_FAILED: FLOGI failed for VSAN 1 on port FC1/1
2024 Jan 15 14:32:22 +00:00 mds9710-1 %FSPF-2-LINK_DOWN: Link 0/2 (FC1/2) down
2024 Jan 15 14:32:23 +00:00 mds9710-1 %FC-2-FLOGI_FAILED: FLOGI failed for VSAN 1 on port FC1/2
2024 Jan 15 14:32:45 +00:00 mds9710-1 %FSPF-2-LINK_UP: Link 0/1 (FC1/1) up
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the exact command syntax for your MDS firmware version using `show ?` to list available commands.
    **`% Incomplete command`** — Add the full command path; try `show system resources` instead of partial command names.
    **`% Permission denied`** — Ensure your user role has "network-admin" or equivalent privileges; check with `show role name <your-role>`.
```bash
show fcdomain vsan 10
show fcdomain domain-list vsan 10
```

```text title="Expected output"
VSAN 10 Information:
  Domain ID: 42
  WWN: 20:00:00:05:73:a1:2b:c0
  Principal: Yes
  State: Stable
  Interfaces: fc1/1, fc1/2, fc1/3, fc1/4

Domain List for VSAN 10:
  Domain 42 (Local) — 20:00:00:05:73:a1:2b:c0 — Principal
  Domain 15 — 20:00:00:05:73:a2:3d:e1 — Stable
  Domain 28 — 20:00:00:05:73:a3:4f:a2 — Stable
  Domain 51 — 20:00:00:05:73:a4:5g:b3 — Stable
  Domain 63 — 20:00:00:05:73:a5:6h:c4 — Stable
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the VSAN exists with `show vsan` and confirm you are in the correct mode (use `config t` if needed).
    **`VSAN 10 does not exist`** — Create the VSAN first using `vsan 10` in config mode, then enable it with `no shutdown`.
```bash
fcdomain domain 3 static vsan 10
# Then bring up the ISL
interface fc2/1
  no shutdown
```

```text title="Expected output"
fcdomain domain 3 static vsan 10
(no output — command completes silently)
interface fc2/1
  no shutdown
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode (use `config t` first) and that the syntax matches your MDS firmware version.
    **`% VSAN 10 does not exist`** — Create the VSAN first using `vsan 10` command before assigning it to the fcdomain.
```bash
# Review install status
show install all status

# Review install log
show install all failure-reason
```

```text title="Expected output"
Install Status:
  Installed Package: system-4.2(8a)S6
  Installed Package: kickstart-4.2(8a)S6
  Last Install Date: Dec 15 2024 14:32:18 +00:00
  Install State: Success
  
Install Failure Reason:
  No failures detected in current installation.
  Last successful install: system-4.2(8a)S6 on Dec 15 2024 14:32:18 +00:00
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct mode (use `config terminal` if needed) and that the MDS switch supports these install commands.
    **`% Feature not enabled: install`** — Enable the install feature with `feature install` in configuration mode before running install status commands.
```bash
install all nxos bootflash:<image-name>
```

```text title="Expected output"
Verifying image bootflash:/nxos.9.3.7.bin
[####################] 100%
Extracting nxos image
[####################] 100%
Image is valid
Setting NXOS image as boot image...
Boot image set to bootflash:/nxos.9.3.7.bin
Reboot is required to activate the image. Issue "reload" command.
```

!!! warning "Common errors"
    **`Error: Image file not found at bootflash:<image-name>`** — Verify the image filename exists in bootflash using `dir bootflash:` and correct any typos in the image name.
    **`Error: Insufficient space in bootflash. Required: 2048 MB, Available: 512 MB`** — Delete old images with `delete bootflash:<old-image>` or add additional storage before retrying the install command.
    **`Error: Image verification failed - corrupted or invalid image`** — Re-copy the image file to bootflash using SCP or SFTP and verify the checksum matches the release notes.
```bash
# Always save after any change
copy running-config startup-config

# Or use the checkpoint mechanism before changes
checkpoint pre-change
```

```text title="Expected output"
Saving the current running configuration to startup configuration...
[OK]

Checkpoint created successfully.
Checkpoint name: pre-change
Checkpoint ID: 2847-5f3a-9c2d-1b4e
Created: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode (enable mode for `copy` command); use `enable` first if needed.
    **`% Destination filename [startup-config]?`** — Press Enter to confirm the default destination or specify an alternative filename; the command requires explicit confirmation.
```bash
show startup-config | head -20
# Confirm timestamp matches the last intended save
```


```text title="Expected output"
version 9.2(2)
no feature telemetry
feature npiv
feature fport-channel-trunk
feature analytics
no feature ssh
feature http-server
feature https-server
feature sso
feature tacacs+
feature radius
feature ldap
feature ntp
feature snmp
feature rmon
feature syslog
feature lldp
feature fcanalytics
feature fcdomain
feature fcns
...
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct mode (exec or config) and that the `show` command is supported on this MDS version.
    **`% Incomplete command`** — Ensure the pipe character and `head` command are properly supported; some MDS versions require `show startup-config | grep` instead.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Cisco MDS 9000 — Backup and Restore](backup-restore.md)
- [Cisco MDS 9000 — CLI Reference](cli-reference.md)
- [Cisco MDS 9000 — Health Checks](health-checks.md)
- [MDS — Operations](index.md)
- [Cisco MDS — Architecture](../../architecture/)
- [Cisco MDS — Initial Deployment](../../deploy/)
- [MDS — Security](../../security/)
- [MDS — Troubleshooting](../../troubleshooting/)
