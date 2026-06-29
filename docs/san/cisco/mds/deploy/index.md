---
tags:
  - deployment
  - san
search:
  boost: 1.5
---

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
rack_and_cable: "Rack and Cable" {shape: rectangle}
initial_nxos_setup: "Initial NX-OS Setup" {shape: rectangle}
configure_vsan_and_port_channels: "Configure VSAN and Port Channels" {shape: rectangle}
zone_configuration: "Zone Configuration" {shape: rectangle}
ndfc_integration: "NDFC Integration" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> rack_and_cable
rack_and_cable -> initial_nxos_setup
initial_nxos_setup -> configure_vsan_and_port_channels
configure_vsan_and_port_channels -> zone_configuration
zone_configuration -> ndfc_integration
ndfc_integration -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# Cisco MDS — Initial Deployment

This guide covers deploying a Cisco MDS 9000 series SAN switch from physical installation through validated host connectivity. Applies to Cisco MDS 9132T, 9148T, 9396T fixed-port switches and MDS 9706/9710/9718 directors running NX-OS 8.x or 9.x.

---

## Prerequisites

**Hardware:**

- Cisco MDS 9000 series switch or director chassis with line card modules installed
- 16Gb, 32Gb, or 64Gb FC SFP transceivers (Cisco requires Cisco-branded optics unless `service unsupported-transceiver` is enabled)
- FC cables matching transceiver type (OM3/OM4 multi-mode for short runs)
- OOB management switch for MGMT0 Ethernet port

**Fabric design decisions (make before installing):**

- VSAN IDs: unique per logical fabric — typically VSAN 10 for Fabric A, VSAN 20 for Fabric B
- Domain ID: unique per switch within a VSAN — reserve one domain ID per switch
- Port channel grouping for ISLs if multiple links connect two switches
- Zone naming convention (e.g., `z_<hostname>_<hba_port>_<storage_wwn_short>`)

**Credentials and access:**

- Console cable (USB mini or RJ-45 depending on model) for initial setup
- NX-OS license: MDS switches require a SAN\_ENTERPRISE\_PKG license for advanced features (IVR, SME encryption). Base features (VSANs, zones) are included in the base license.
- Cisco NDFC (formerly DCNM) or Cisco Fabric Manager details if adding to centralized management

---

## Rack and Cable

1. Mount the switch in the rack using the provided rack ears. Directors go into a Cisco-supplied cabinet or a standard 42U rack with reinforced rails.
2. For director chassis: install Supervisor modules first (slots 1 and 2), then line cards. Do not mix 16G and 32G line cards in the same VSAN without verifying compatibility.
3. Connect redundant PDU cables from each power supply to separate circuit feeds.
4. Connect the MGMT0 port to the OOB management switch.
5. Install SFPs in ISL ports and connect ISL cables between switches.
6. Install SFPs in host-facing and storage-facing ports and connect cables.
7. Power on the switch. First boot takes 5–10 minutes. The supervisor STATUS LED turns solid green when NX-OS is ready.

---

## Initial NX-OS Setup

Connect via serial console (9600 baud, 8N1) for initial setup.

Walk through the setup dialog:

```text
Enter the switch name: mds-fab-a-01
Continue with Out-of-band (mgmt0) management configuration? (yes/no) [y]: y
Mgmt0 IPv4 address: 10.0.0.20
Mgmt0 IPv4 netmask: 255.255.255.0
IPv4 address of default gateway: 10.0.0.1
Configure advanced IP options? (yes/no) [n]: n
Enable the ssh service? (yes/no) [n]: y
Configure the ntp server? (yes/no) [n]: y
NTP server IPv4 address: 10.0.0.5
Configure CFS distribution? (yes/no) [y]: y
# Accept remaining defaults
```

Verify basic connectivity:

```bash
ping 10.0.0.1 vrf management
```


```text title="Expected output"
PING 10.0.0.1 (10.0.0.1) from 10.0.0.2 vrf management
56 data bytes
64 bytes from 10.0.0.1: icmp_seq=0 ttl=255 time=2.341 ms
64 bytes from 10.0.0.1: icmp_seq=1 ttl=255 time=1.987 ms
64 bytes from 10.0.0.1: icmp_seq=2 ttl=255 time=2.156 ms
64 bytes from 10.0.0.1: icmp_seq=3 ttl=255 time=2.104 ms
64 bytes from 10.0.0.1: icmp_seq=4 ttl=255 time=2.278 ms

--- 10.0.0.1 statistics ---
5 packets transmitted, 5 packets received, 0.00% packet loss
round-trip min/avg/max/stddev = 1.987/2.173/2.341/0.132 ms
```

!!! warning "Common errors"
    **`PING: cannot find vrf management`** — Verify the management VRF exists with `show vrf` and confirm it is configured on the switch.
    **`PING: sendto: No route to host`** — Check that the management interface is up with `show interface mgmt0` and that routing to 10.0.0.1 is configured.
    **`PING: sendto: Permission denied`** — Ensure you have administrative privileges; use `enable` to enter privileged EXEC mode before running the ping command.
**Apply NX-OS license:**

```bash
copy tftp://10.0.0.100/mds-license.lic bootflash:
license install bootflash:mds-license.lic
show license
```


```text title="Expected output"
Copying tftp://10.0.0.100/mds-license.lic to bootflash:mds-license.lic
[####################] 100%
Copy complete.

License Installation in progress. Please wait...
License installation completed successfully.

License Usage:
  License Level: Enterprise
  Features Enabled:
    - FC_SWITCHING
    - FCOE
    - ADVANCED_FEATURES
  Licenses Installed: 1
  License Expiration: 2026-12-31
```

!!! warning "Common errors"
    **`%Error opening tftp://10.0.0.100/mds-license.lic (Connection timed out)`** — Verify TFTP server is reachable and running on 10.0.0.100, and check network connectivity from the MDS switch.
    **`%License file is invalid or corrupted`** — Ensure the license file is a valid Cisco MDS .lic file and was not corrupted during transfer; re-download from Cisco if needed.
    **`%Insufficient space on bootflash`** — Free up space on bootflash using `delete bootflash:` command before copying the license file.
---

## Configure VSAN and Port Channels

**Create VSANs:**

VSANs logically segment the fabric. Create a VSAN for each fabric (A and B).

```bash
vsan database
  vsan 10 name "Fabric-A"
  vsan 20 name "Fabric-B"

# Verify:
show vsan
```


```text title="Expected output"
vsan 10 name Fabric-A
vsan 20 name Fabric-B

VSAN       Name                             State   Interoperability
----       ----                             -----   ----------------
1          VSAN0001                         active  default
10         Fabric-A                         active  default
20         Fabric-B                         active  default
```

!!! warning "Common errors"
    **`% Invalid command`** — Ensure you are in the correct configuration mode (enter `config t` then `vsan database` before entering VSAN definitions).
    **`% VSAN 10 already exists`** — Delete the existing VSAN with `no vsan 10` before redefining it, or use a different VSAN ID.
**Assign ports to VSANs:**

```bash
vsan database
  vsan 10 interface fc1/1-16    # Host-facing ports for Fabric A
  vsan 20 interface fc1/17-32   # (Not used on a single-fabric switch — adjust for your topology)
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode (`config t`) and that the MDS switch supports VSAN configuration.
    **`% Interface fc1/1-16 not found`** — Confirm the port range exists on your specific MDS model (e.g., MDS 9148S has fc1/1-48); adjust the range accordingly.
**Set the domain ID per VSAN:**

```bash
fcdomain domain 1 preferred vsan 10
fcdomain domain 2 preferred vsan 20
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode with `config t` and that the MDS switch supports fcdomain commands.
    **`% VSAN <vsan-id> does not exist`** — Create the VSAN first using `vsan <vsan-id>` command before assigning it as preferred in fcdomain configuration.
**Configure ISL Port Channels (if multiple ISL links exist):**

```bash
interface port-channel 1
  channel mode active
  switchport mode E
  switchport trunk allowed vsan 10

interface fc1/33
  channel-group 1 force
interface fc1/34
  channel-group 1 force

# Verify trunk:
show interface port-channel 1
show topology vsan 10
```


```text title="Expected output"
Port-channel1 is up
  Hardware is Fibre Channel
  Port WWN is 50:00:09:0f:1a:2b:3c:4d
  Admin port mode is E, Oper port mode is E
  Trunk mode is on
  Allowed VSANs: 10
  Active VSANs: 10
  Last clearing of "show interface" counters: never

Topology for VSAN 10:
  Domain ID: 1 (local)
  Switch Name: mds9710-01
  Switch WWN: 20:00:00:0d:ec:2a:3b:4c
  Connected to Domain 2 via port fc1/33 (port-channel 1)
  Fabric Port Count: 8
  F-Port Count: 24
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the exact syntax for your MDS firmware version; `switchport mode E` may need to be `switchport mode fport` or configured differently depending on the context.
    **`% Port fc1/33 is already bound to a channel group`** — Remove the port from any existing channel group with `no channel-group` before assigning it to port-channel 1.
    **`% VSAN 10 does not exist`** — Create the VSAN first using `vsan 10` in configuration mode before assigning it to the trunk.
---

## Zone Configuration

Cisco MDS uses Enhanced Zoning or Smart Zoning. Enhanced Zoning (default from NX-OS 8.x) allows per-VSAN zone databases and is recommended.

**Create zones using WWN-based membership:**

```bash
zone name z_esx01_hba0_pmax_fa1_p0 vsan 10
  member pwwn 10:00:00:90:fa:11:22:33   ! Host HBA WWN
  member pwwn 50:00:09:73:00:1a:2b:3c   ! Storage target WWN

zone name z_esx01_hba1_pmax_fa2_p0 vsan 10
  member pwwn 10:00:00:90:fa:11:22:34
  member pwwn 50:00:09:73:00:1a:2b:3d
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode (enter `config t` then `zone` submode) before entering zone member commands.
    **`% Incomplete command`** — Ensure each zone definition includes at least one `member pwwn` statement; incomplete zone configurations will be rejected.
**Create a zoneset and add zones:**

```bash
zoneset name zs_fabric_a vsan 10
  member z_esx01_hba0_pmax_fa1_p0
  member z_esx01_hba1_pmax_fa2_p0
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode by entering `config t` and `san-device-alias database` context first.
    **`% Zone member not found: z_esx01_hba0_pmax_fa1_p0`** — Create the zone and its device aliases before adding them to the zoneset using `zone name <zone_name> vsan 10` commands.
**Activate the zoneset:**

```bash
zoneset activate name zs_fabric_a vsan 10

# Save the zone configuration:
copy running-config startup-config
```


```text title="Expected output"
Zoneset: zs_fabric_a activated successfully for VSAN 10.
Copy complete.
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode (use `config terminal` first if needed).
    **`% Zoneset zs_fabric_a not found`** — Create the zoneset with `zoneset name zs_fabric_a vsan 10` before attempting to activate it.
**Verify zones:**

```bash
show zoneset active vsan 10
show zone member vsan 10
show fcns database vsan 10
# Host and storage WWNs should appear in the name server database
```


```text title="Expected output"
zoneset name: prod_zoneset vsan: 10
  zone name: zone_prod_hosts vsan: 10
    fcid 0x010001 [pwwn 50:00:09:73:00:12:a4:5f] [nwwn 50:00:09:73:00:12:a4:5e]
    fcid 0x010002 [pwwn 50:00:09:73:00:12:b8:3a] [nwwn 50:00:09:73:00:12:b8:39]
  zone name: zone_storage vsan: 10
    fcid 0x010101 [pwwn 50:00:14:40:5d:2c:a1:b0] [nwwn 50:00:14:40:5d:2c:a1:af]

VSAN: 10
Zone Member:
  Zone Name: zone_prod_hosts
    50:00:09:73:00:12:a4:5f
    50:00:09:73:00:12:b8:3a
  Zone Name: zone_storage
    50:00:14:40:5d:2c:a1:b0

FCNS Database for VSAN 10:
  PWWN: 50:00:09:73:00:12:a4:5f  NWWN: 50:00:09:73:00:12:a4:5e  FCID: 0x010001  Port Name: esx-host-01
  PWWN: 50:00:09:73:00:12:b8:3a  NWWN: 50:00:09:73:00:12:b8:39  FCID: 0x010002  Port Name: esx-host-02
  PWWN: 50:00:14:40:5d:2c:a1:b0  NWWN: 50:00:14:40:5d:2c:a1:af  FCID: 0x010101  Port Name: netapp-array-01
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the VSAN number exists with `show vsan` and confirm you are in the correct mode (config or exec).
    **`FCNS Database for VSAN 10: (empty)`** — Check that devices are logged in and zoning is activated with `show zoneset active vsan 10`; if empty, devices have not registered with the name server yet.
---

## NDFC Integration

Cisco Nexus Dashboard Fabric Controller (NDFC) provides centralized management for Cisco SAN fabrics.

**Enable SNMP on the MDS switch for NDFC discovery:**

```bash
snmp-server community public ro
snmp-server host 10.0.0.30 traps version 2c public
snmp-server enable traps all
```


```text title="Expected output"
(no output — commands complete silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct configuration mode (config-if or config) by checking the prompt ends with `(config)#` or `(config-if)#`.
    **`% Incomplete command`** — Ensure the SNMP community string and trap host IP are both specified; the syntax requires `snmp-server community <string> ro` and `snmp-server host <ip> traps version 2c <community>`.
**Enable CFS (Cisco Fabric Services) for zone distribution:**

CFS automatically distributes zone changes across all switches in the VSAN when activated.

```bash
cfs enable
cfs distribute
show cfs status
```


```text title="Expected output"
cfs enable
(no output — command completes silently)
cfs distribute
(no output — command completes silently)
show cfs status
CFS Status Information
    CFS State: enabled
    Configured fabric: MDS_Fabric_1
    Distribution Status: success
    Last distribution time: 2024-01-15 14:32:18 UTC
    Peers in sync: 4/4
    Pending changes: 0
```

!!! warning "Common errors"
    **`CFS is already enabled`** — CFS is already active; skip the `cfs enable` command or verify current state with `show cfs status` first.
    **`Distribution failed: peer switch unreachable`** — Verify all fabric switches are online and reachable using `show fabric status` before running `cfs distribute`.
    **`CFS State: disabled`** — Run `cfs enable` before attempting distribution; the feature must be activated on the switch.
**Add the MDS switch to NDFC:**

1. Log in to the NDFC web interface at `https://<ndfc_server>`.
2. Navigate to **SAN > Fabrics > Add Fabric**.
3. Enter the MDS switch management IP, credentials, and SNMP community.
4. NDFC discovers the switch and the VSAN topology.
5. Verify the switch appears in **SAN > Switches** with all VSANs correctly identified.

For initial NDFC deployment, see the Cisco DCNM deployment guide.

---

## Host Connectivity

After zoning is configured, verify hosts can see storage.

**Check name server entries:**

```bash
show fcns database detail vsan 10
# Verify host HBA WWNs and storage target WWNs both appear
# FC4 type should show SCSI FCP for storage targets
```


```text title="Expected output"
VSAN 10:
  Node Name: storage-target-01.example.com
  Node PWWN: 50:00:14:40:5a:2b:c1:e0
  Node NWWN: 50:00:14:40:5a:2b:c1:e1
  IP Address: 192.168.10.50
  IPA: 0x000001
  FC4 Types: SCSI FCP
  Symbolic Node Name: EMC VMAX5990 Storage Array

  Node Name: esx-host-07.example.com
  Node PWWN: 50:00:09:73:1a:4c:b2:f5
  Node NWWN: 50:00:09:73:1a:4c:b2:f6
  IP Address: 192.168.10.75
  IPA: 0x000002
  FC4 Types: SCSI FCP
  Symbolic Node Name: VMware ESXi 7.0 HBA

  Node Name: esx-host-08.example.com
  Node PWWN: 50:00:09:73:1a:4c:b3:a1
  Node NWWN: 50:00:09:73:1a:4c:b3:a2
  IP Address: 192.168.10.76
  IPA: 0x000003
  FC4 Types: SCSI FCP
  Symbolic Node Name: VMware ESXi 7.0 HBA
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct mode (enable mode on MDS switch) and use `show fcns database detail vsan <vsan-id>` syntax.
    **`VSAN <vsan-id> does not exist`** — Confirm the VSAN exists with `show vsan` and verify the VSAN ID is correct and active.
**Verify zone enforcement:**

```bash
show zone member pwwn 10:00:00:90:fa:11:22:33 vsan 10
# Should list the zones containing this HBA WWN
```


```text title="Expected output"
Zone Name: prod-app-zone
  pwwn 10:00:00:90:fa:11:22:33
  pwwn 10:00:00:90:fa:44:55:66
  pwwn 50:00:14:40:12:34:56:78

Zone Name: backup-zone
  pwwn 10:00:00:90:fa:11:22:33
  pwwn 50:00:14:40:87:65:43:21

Total of 2 zones found
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct MDS CLI mode (use `config terminal` if needed) and that the VSAN exists with `show vsan`.
    **`% VSAN 10 does not exist`** — Confirm VSAN 10 is created and active using `show vsan id 10`.
    **`% No zones found containing this member`** — Verify the WWN format is correct (use colons, not hyphens) and the HBA is actually zoned in VSAN 10 with `show zoneset active vsan 10`.
**From the host (Linux):**

```bash
rescan-scsi-bus.sh
lsscsi
multipath -ll
# Storage paths should be visible through the MDS switch
```


```text title="Expected output"
Scanning for SCSI devices...
Scanning host 0...
Scanning host 1...
Scanning host 2...
Scanning host 3...
Scanning host 4...
Scanning host 5...
Scanning host 6...
Scanning host 7...
Scanning host 8...
Scanning host 9...
Scanning host 10...
Scanning host 11...
Scanning host 12...
Scanning host 13...
Scanning host 14...
Scanning host 15...
Scanning host 16...
Scanning host 17...
Scanning host 18...
Scanning host 19...

[0:0:0:0]    disk    NETAPP   LUN              9800  /dev/sda 
[1:0:0:0]    disk    NETAPP   LUN              9800  /dev/sdb 
[2:0:0:0]    disk    NETAPP   LUN              9800  /dev/sdc 
[3:0:0:0]    disk    NETAPP   LUN              9800  /dev/sdd 
[4:0:0:0]    disk    NETAPP   LUN              9800  /dev/sde 
[5:0:0:0]    disk    NETAPP   LUN              9800  /dev/sdf 
[6:0:0:0]    disk    NETAPP   LUN              9800  /dev/sdg 
[7:0:0:0]    disk    NETAPP   LUN              9800  /dev/sdh 

mpatha (360a98000534d4b4a6d4e6f5a4b4c4d4e) dm-0 NETAPP,LUN
size=2.0T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 0:0:0:0 sda 8:0   active ready running
  |- 1:0:0:0 sdb 8:16  active ready running
  |- 2:0:0:0 sdc 8:32  active ready running
  `- 3:0:0:0 sdd 8:48  active ready running
mpathb (360a98000534d4b4a6d4e6f5a4b4c4d4f) dm-1 NETAPP,LUN
size=1.5T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 4:0:0:0 sde 8:64  active ready running
  |- 5:0:0:0 sdf 8:80  active ready running
  |- 6:0:0:0 sdg 8:96  active ready running
  `- 7:0:0:0 sdh 8:112 active ready running
```

!!! warning "Common errors"
    **`rescan-scsi-bus.sh: command not found`** — Install sg3
---

## Validate

**Fabric health check:**

```bash
show interface fc1/1-16 brief
# All connected ports should show State: up, Speed: 16G (or 32G)
# No ports should show State: down unexpectedly

show fcdomain vsan 10
# Principal switch and domain assignments should be consistent

show topology vsan 10
# ISL topology should match the cabling plan
```


```text title="Expected output"
fc1/1    -- up      16G   SFP    Fabric  fc1/1
fc1/2    -- up      16G   SFP    Fabric  fc1/2
fc1/3    -- up      16G   SFP    Fabric  fc1/3
fc1/4    -- up      16G   SFP    Fabric  fc1/4
fc1/5    -- up      16G   SFP    Fabric  fc1/5
fc1/6    -- down    --    SFP    Fabric  fc1/6
fc1/7    -- up      16G   SFP    Fabric  fc1/7
...
fc1/16   -- up      16G   SFP    Fabric  fc1/16

VSAN 10 Information:
  Principal Switch: mds-core-01 (Domain ID: 1)
  Local Switch Domain ID: 1
  Fabric Name: prod-fabric-01
  State: Stable

Topology for VSAN 10:
  mds-core-01 (Domain 1) -- ISL fc1/15 -- mds-core-02 (Domain 2)
  mds-core-02 (Domain 2) -- ISL fc1/16 -- mds-edge-01 (Domain 3)
  mds-edge-01 (Domain 3) -- ISL fc1/14 -- mds-core-01 (Domain 1)
```

!!! warning "Common errors"
    **`fc1/6    -- down    --    SFP    Fabric  fc1/6`** — Check SFP transceiver seating, cable connections, and run `show interface fc1/6` for detailed diagnostics including error counters.
    **`Domain ID conflict detected on VSAN 10`** — Verify domain IDs are unique across all switches in the fabric and reload the switch if a duplicate persists after reconfiguration.
    **`ISL port down: fc1/15 (mds-core-01 to mds-core-02)`** — Inspect the ISL cable for damage, reseat both SFP transceivers, and confirm speed negotiation with `show interface fc1/15 detail`.
**Error counter check:**

```bash
show interface fc1/1 counters
# Check: signal_loss, sync_loss, link_failure, invalid_crc
# All should be zero on a clean deployment

# Clear counters after initial verification:
clear counters interface fc1/1
```


```text title="Expected output"
Interface fc1/1
  Frames Transmitted:                    1,247,392
  Frames Received:                       1,245,018
  Transmit B2B Credit Zero:                    0
  Receive B2B Credit Zero:                    0
  Link Failures:                               0
  Sync Losses:                                 0
  Signal Losses:                               0
  Invalid CRCs:                                0
  Address Errors:                              0
  Delimiter Errors:                            0
  Disparity Errors:                            0
  Primitive Sequence Protocol Errors:          0

Clear counters on interface fc1/1
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the interface name matches your MDS model (e.g., `fc1/1` vs `Ethernet1/1`) and use `show interface` first to confirm the port exists.
    **`% Interface fc1/1 is down`** — Check physical cable connection and port status with `show interface fc1/1` before clearing counters on a non-operational link.
**End-to-end path verification:**

```bash
# Test FC ping from switch to a storage target port:
fcping pwwn 50:00:09:73:00:1a:2b:3c vsan 10 count 5
# Should show 5/5 successful responses
```


```text title="Expected output"
FCPING: 5 bytes from 50:00:09:73:00:1a:2b:3c: time=2.341 ms
FCPING: 5 bytes from 50:00:09:73:00:1a:2b:3c: time=2.156 ms
FCPING: 5 bytes from 50:00:09:73:00:1a:2b:3c: time=2.289 ms
FCPING: 5 bytes from 50:00:09:73:00:1a:2b:3c: time=2.412 ms
FCPING: 5 bytes from 50:00:09:73:00:1a:2b:3c: time=2.198 ms
--- 50:00:09:73:00:1a:2b:3c statistics ---
5 packets transmitted, 5 packets received, 0.00% packet loss
round-trip min/avg/max = 2.156/2.279/2.412 ms
```

!!! warning "Common errors"
    **`FCPING: No response from 50:00:09:73:00:1a:2b:3c`** — Verify the target PWWN is correct and the storage port is online and zoned to the initiator.
    **`FCPING: VSAN 10 is not configured`** — Create the VSAN first using `vsan <id>` command or confirm the VSAN number matches your fabric configuration.
    **`FCPING: Permission denied`** — Ensure you are in the correct VSAN context or have appropriate user role permissions to execute fcping commands.
**Traceroute within the fabric:**

```bash
fctrace pwwn 50:00:09:73:00:1a:2b:3c vsan 10
# Shows each hop through the fabric to the target port
```


```text title="Expected output"
PWWN: 50:00:09:73:00:1a:2b:3c VSAN: 10

Hop 1: Switch fcswitch-mds1 (IP: 192.168.1.10)
  Port: fc1/1 (Speed: 16 Gbps, State: Up)
  
Hop 2: Switch fcswitch-mds2 (IP: 192.168.1.11)
  Port: fc2/5 (Speed: 16 Gbps, State: Up)
  
Hop 3: Switch fcswitch-mds3 (IP: 192.168.1.12)
  Port: fc3/12 (Speed: 16 Gbps, State: Up)

Target Port Found:
  PWWN: 50:00:09:73:00:1a:2b:3c
  Device: EMC-VMAX-SN-000123456789
  Port: fc3/12
  Distance: 3 hops
```

!!! warning "Common errors"
    **`fctrace: PWWN not found in VSAN 10`** — Verify the PWWN is correct and the device is zoned into the specified VSAN using `fcping` or `zone name` commands.
    **`fctrace: VSAN 10 does not exist or is suspended`** — Confirm the VSAN is active with `show vsan` and ensure it is not in suspended state.
    **`fctrace: Command not found`** — Enable the fctrace feature on the MDS switch using `feature fctrace` in configuration mode.
Save configuration:

```bash
copy running-config startup-config
```


```text title="Expected output"
[########################################] 100.0%

Copy complete.
```

!!! warning "Common errors"
    **`% Error opening tftp://255.255.255.255/network-confg (Timed out)`** — Verify TFTP server is reachable and configured; use `ping` to test connectivity to the TFTP server IP.
    **`% Invalid command`** — Ensure you are in privileged EXEC mode (prompt shows `#`); type `enable` if needed.
---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Mds — Procedures](../operations/procedures/)
- [Mds — Common Issues](../troubleshooting/common-issues/)
- [Mds — How It Works](../architecture/how-it-works/)
