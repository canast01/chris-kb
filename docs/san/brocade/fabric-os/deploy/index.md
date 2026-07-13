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
initial_switch_configuration: "Initial Switch Configuration" {shape: rectangle}
set_domain_id_and_fabric_parameters: "Set Domain ID and Fabric Parameters" {shape: rectangle}
zone_configuration: "Zone Configuration" {shape: rectangle}
isl_configuration: "ISL Configuration" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> rack_and_cable
rack_and_cable -> initial_switch_configuration
initial_switch_configuration -> set_domain_id_and_fabric_parameters
set_domain_id_and_fabric_parameters -> zone_configuration
zone_configuration -> isl_configuration
isl_configuration -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: SAN Storage & iSCSI Network Design | Full Redundancy + Multipathing for VMware](https://www.youtube.com/watch?v=KqEUn5WBgVQ){ .md-button }
<!-- /video-link -->


- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# Brocade FabricOS — Initial Deployment

This guide covers deploying a Brocade SAN switch (running Fabric OS) from physical installation through a validated, production-ready FC fabric. Applies to Brocade G620, G630, and X7 directors running Fabric OS 9.x.

---

## Prerequisites

**Hardware:**

- Brocade switch (fixed-port) or director chassis (Brocade X7-4 or X7-8) with blade modules installed
- 32Gb or 64Gb SFP+ transceivers matching the switch and HBA port types
- FC cables (OM4 multi-mode for short runs; single-mode for inter-building or long ISL runs)
- OOB management switch with DHCP (for initial IP discovery) or a pre-planned management IP

**Plan the fabric design before powering on:**

- Domain IDs must be unique within a fabric — reserve one domain ID per switch and document them before starting
- Fabric parameters (BB credits, E_D_TOV, R_A_TOV) must match across all switches in the fabric
- Zone plan prepared: single-initiator/single-target zones, named by server and storage port
- At minimum two separate fabrics (Fabric A and Fabric B) for host redundancy

**Tools and access:**

- Serial console cable (RJ-45 to DB-9 adapter) or out-of-band SSH access
- Brocade Network Advisor or SANnav for ongoing management (configured in a later step)
- SSH client on the management workstation

---

## Rack and Cable

1. Mount the switch or director chassis into the rack using the provided bracket kit. Secure all four rack screws.
2. For director chassis: install blade modules into the chassis slots according to the port layout plan. Blades seat into active slots and power on automatically when chassis is powered.
3. Connect the power cables from each power supply to separate PDU circuits (N+1 redundancy).
4. Connect the management Ethernet port (labeled `MGMT` or `ETH0`) to the OOB management switch.
5. Install SFP transceivers into the ports designated for ISL (inter-switch links) and for host / storage connections.
6. Connect ISL cables first (between switches, if this is a multi-switch fabric), then host HBA cables, then storage array FC port cables.
7. Power on the switch. Initial boot takes 3–5 minutes. The status LED on the chassis turns solid green when Fabric OS is ready.

---

## Initial Switch Configuration

Connect to the switch via serial console (115200 baud, 8N1) or via the default management IP if DHCP is in use.

**Change default passwords:**

```bash
# Default credentials: admin / password (and root / fibranne)
# Log in as admin:
login: admin
password: password

# Change admin password immediately:
passwd admin
# Enter and confirm a new strong password

passwd root
```


```text title="Expected output"
Brocade Fabric OS (v9.1.0)
Copyright (c) 1995-2023 Brocade Communications Systems, Inc.
All Rights Reserved.

Login: admin
Password: 
You are logged in as: admin
Type help for a list of commands.

admin> passwd admin
Please enter new password: 
Please re-enter new password: 
Password changed successfully.

admin> passwd root
Please enter new password: 
Please re-enter new password: 
Password changed successfully.

admin>
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Password too short (minimum 8 characters required)` | Ensure the new password is at least 8 characters long and includes uppercase, lowercase, numbers, and special characters. |
    | `Passwords do not match` | Re-enter both passwords carefully, ensuring they are identical on the second prompt. |
**Set the switch name:**

```bash
switchName "sw-fabric-a-01"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `switchName: command not found` | Ensure you are in the Brocade FOS CLI environment (telnet/SSH to the switch) rather than a standard bash shell. |
    | `Invalid switch name format` | Use only alphanumeric characters and hyphens; switch names cannot exceed 63 characters or contain spaces. |
**Set management IP (if not using DHCP):**

```bash
ipaddrset
# Follow the interactive prompt to set:
# Ethernet IP Address: 10.0.0.10
# Ethernet Subnetmask: 255.255.255.0
# Gateway IP Address: 10.0.0.1
```


```text title="Expected output"
Brocade Fabric OS IP Address Configuration Utility
==================================================

Current Network Configuration:
  Ethernet IP Address: 0.0.0.0
  Ethernet Subnetmask: 0.0.0.0
  Gateway IP Address: 0.0.0.0

Enter Ethernet IP Address [0.0.0.0]: 10.0.0.10
Enter Ethernet Subnetmask [0.0.0.0]: 255.255.255.0
Enter Gateway IP Address [0.0.0.0]: 10.0.0.1

Validating configuration...
Configuration validated successfully.

Applying network settings...
Network configuration updated.
Please restart the switch for changes to take effect.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Invalid IP address format` | Ensure all IP addresses are entered in dotted-decimal notation (e.g., 10.0.0.10) with no spaces or special characters. |
    | `Gateway IP Address must be on the same subnet as Ethernet IP Address` | Verify the gateway IP falls within the 10.0.0.0/24 subnet (10.0.0.1–10.0.0.254). |
**Configure NTP:**

```bash
tsclockserver "10.0.0.5"
# Verify NTP sync:
tsclockserver
date
```


```text title="Expected output"
Time Server: 10.0.0.5
(no output — command completes silently)
Time Server: 10.0.0.5
Wed Oct 18 14:32:47 UTC 2024
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `tsclockserver: command not found` | Ensure you are logged into the Brocade switch via SSH or serial console, not a Linux host; this command only exists on FabricOS. |
    | `Error: Invalid IP address "10.0.0.5"` | Verify the NTP server IP is reachable from the switch and is a valid, active NTP server on your network. |
**Configure DNS:**

```bash
dnsconfig --add 10.0.0.53
```


```text title="Expected output"
DNS server 10.0.0.53 added successfully
Current DNS configuration:
  Primary: 10.0.0.53
  Secondary: 10.0.0.54
  Tertiary: Not configured
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `dnsconfig: Invalid IP address format` | Verify the IP address is in valid dotted-decimal notation (e.g., 10.0.0.53). |
    | `dnsconfig: DNS server already exists` | Remove the duplicate entry with `dnsconfig --remove 10.0.0.53` before re-adding it. |
**Enable SSH (if not already enabled):**

```bash
sshutil enable
```


```text title="Expected output"
SSH Utility has been enabled.
SSH service is running on port 22.
SSH key generation completed successfully.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sshutil: command not found` | Ensure you are logged into the Brocade switch console or SSH session with administrative privileges, as sshutil is a switch-native command. |
    | `Permission denied` | Run the command with admin credentials or switch to the admin user account before executing sshutil commands. |
---

## Set Domain ID and Fabric Parameters

The domain ID uniquely identifies the switch within the fabric. All fabric parameters must be consistent across all switches.

**Disable the switch before modifying fabric parameters:**

```bash
switchDisable
```


```text title="Expected output"
Fabric OS v9.1.0
Switch: brocade-switch-01 (Serial: 0123456789ABCDEF)
Current state: Online
Disabling switch...
Switch disabled successfully.
All ports have been brought offline.
Fabric participation disabled.
Switch is now in disabled state.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `switchDisable: command not found` | Ensure you are logged into the Fabric OS CLI (via SSH or console) and have appropriate admin privileges; this command only works within the FOS shell, not the Linux host shell. |
    | `Permission denied` | Verify your user account has admin-level credentials; use `userconfig --show` to check your current role and request elevation if needed. |
**Set the domain ID:**

```bash
configure
# At the "Fabric parameters" prompt, set:
# Domain: 1       (use 2, 3, 4... for each additional switch in the fabric)
# BB credits: 16  (adjust based on distance and speed)
# R_A_TOV: 10000  (match across all switches)
# E_D_TOV: 2000   (match across all switches)
# Accept all other defaults unless documented otherwise
```


```text title="Expected output"
Fabric OS Configuration Tool v9.1.2
=====================================

Entering configuration mode...

Fabric Parameters Configuration
--------------------------------
Domain ID [1-239]: 1
Buffer-to-Buffer Credits [0-32]: 16
R_A_TOV (ms) [5000-120000]: 10000
E_D_TOV (ms) [1000-10000]: 2000
Enable FICON mode? [y/n]: n
Enable Fabric Watch? [y/n]: y

Configuration Summary:
  Domain: 1
  BB Credits: 16
  R_A_TOV: 10000 ms
  E_D_TOV: 2000 ms
  FICON: disabled
  Fabric Watch: enabled

Apply configuration? [y/n]: y
Configuration applied successfully. Switch will reboot in 30 seconds.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Domain ID 1 already in use on fabric` | Choose an unused domain ID between 2–239 that is not already assigned to another switch in the fabric. |
    | `Error: R_A_TOV (10000) does not match peer switch (5000)` | Set R_A_TOV to the same value across all switches in the fabric before committing the configuration. |
    | `Error: Invalid BB Credits value 16 for ISL speed 4Gbps` | Reduce BB Credits to 8 or lower, or increase ISL speed to 8Gbps or higher to support 16 credits. |
**Re-enable the switch:**

```bash
switchEnable
```


```text title="Expected output"
Fabric OS v9.1.0
Copyright (c) 2023 Broadcom Inc. All rights reserved.

Switch Status: ENABLED
Switch Role: Principal Switch
Fabric Name: prod-fabric-01
Switch WWN: 10:00:00:27:f8:4a:b2:c1
IP Address: 192.168.1.100
Uptime: 45 days 12:34:56

Enabled ports: 48/48
Port Status: Online
Fabric Participation: Active
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `switchEnable: command not found` | Ensure you are logged into the Brocade switch via SSH or serial console, not a local shell. |
    | `Permission denied` | Verify your user account has administrative privileges; use `userConfig --show` to check role assignments. |
**Verify domain ID and fabric formation:**

```bash
fabricShow
# All switches in the fabric should appear with their domain IDs
# The "Principal" switch is shown with an asterisk

switchShow
# Switch state should be "Online"
```


```text title="Expected output"
Switch Name: brocade-switch-01
Switch State: Online
Fabric ID: 100
Domain ID: 1
Principal Switch: Yes *
Fabric Mode: Native
Fabric Port Status: Online

Switch Name: brocade-switch-02
Switch State: Online
Fabric ID: 100
Domain ID: 2
Principal Switch: No
Fabric Mode: Native
Fabric Port Status: Online

Switch Name: brocade-switch-03
Switch State: Online
Fabric ID: 100
Domain ID: 3
Principal Switch: No
Fabric Mode: Native
Fabric Port Status: Online
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `switchShow: command not found` | Ensure you are logged into the Brocade switch CLI (via SSH or console) and not a Linux shell; use `ssh admin@<switch-ip>` to connect. |
    | `Fabric ID mismatch detected` | Verify all switches have the same Fabric ID configured; use `fabricShow` to confirm and reconfigure mismatched switches with `configDefault` if needed. |
    | `Switch State: Offline` | Check physical ISL (Inter-Switch Link) connections between fabric members and verify switch power and network connectivity. |
---

## Zone Configuration

Zoning controls which initiators (host HBAs) can communicate with which targets (storage array ports).

**Best practice:** Single-initiator/single-target zones. Each zone contains one host port WWN and one storage port WWN.

**Create zones for a host with two HBAs connecting to a PowerMax:**

```bash
# Create zones
zoneCreate "zone_esx01_hba0_pmax_fa1e_p0", "10:00:00:90:fa:11:22:33;50:00:09:73:00:1a:2b:3c"
zoneCreate "zone_esx01_hba1_pmax_fa2e_p0", "10:00:00:90:fa:11:22:34;50:00:09:73:00:1a:2b:3d"

# Add zones to a zone configuration (cfg)
cfgCreate "cfg_fabric_a", "zone_esx01_hba0_pmax_fa1e_p0;zone_esx01_hba1_pmax_fa2e_p0"

# Enable the zone configuration
cfgEnable "cfg_fabric_a"

# Save to flash (make it persistent across reboots)
cfgSave
```


```text title="Expected output"
Zone "zone_esx01_hba0_pmax_fa1e_p0" has been created successfully.
Zone "zone_esx01_hba1_pmax_fa2e_p0" has been created successfully.
Configuration "cfg_fabric_a" has been created successfully.
Configuration "cfg_fabric_a" has been enabled successfully.
You are about to save the Defined zoning configuration. Continue? (yes, y, no, n): [no] yes
Zoning configuration saved to flash memory.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Zone name already exists` | Delete the existing zone with `zoneDelete "zone_esx01_hba0_pmax_fa1e_p0"` before recreating it. |
    | `Invalid WWN format in zone member list` | Verify WWN syntax is exactly 16 hexadecimal characters (e.g., `50:00:09:73:00:1a:2b:3c`) with colons separating each pair. |
    | `Configuration is already enabled` | Run `cfgDisable "cfg_fabric_a"` first if you need to modify the active configuration. |
**Verify zones are active:**

```bash
cfgShow
# Shows the active zone configuration and all zone members

zoneShow
# Lists all zones and their members
```


```text title="Expected output"
Defined configuration:
 cfg: prod-fabric-01
  zone: zone-storage-prod (members: 50:00:09:73:00:1a:b4:c1 50:00:09:73:00:1a:b4:c2)
  zone: zone-app-servers (members: 50:00:09:73:00:1a:b4:d1 50:00:09:73:00:1a:b4:d2 50:00:09:73:00:1a:b4:d3)
  zone: zone-backup-vsan (members: 50:00:09:73:00:1a:b4:e1)

Active configuration:
 cfg: prod-fabric-01

Zone Information:
 zone: zone-storage-prod
  50:00:09:73:00:1a:b4:c1 (Storage-Array-01)
  50:00:09:73:00:1a:b4:c2 (Storage-Array-02)
 zone: zone-app-servers
  50:00:09:73:00:1a:b4:d1 (AppServer-01)
  50:00:09:73:00:1a:b4:d2 (AppServer-02)
  50:00:09:73:00:1a:b4:d3 (AppServer-03)
 zone: zone-backup-vsan
  50:00:09:73:00:1a:b4:e1 (Backup-Node-01)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `zoneShow: command not found` | Verify you are logged into the Brocade switch CLI (not the Linux shell) by checking the prompt shows `switch>` or `switch#`. |
    | `Access denied` | Ensure your user account has sufficient privileges; request admin or operator role from the fabric administrator. |
**Confirm name server entries (hosts and storage logged in):**

```bash
nsAllShow
# Lists all N_Ports registered in the name server — verify host and storage WWNs appear
```


```text title="Expected output"
Fabric OS (v9.1.0)

    N_Port Name Server
    =====================================================
    Port Name                           Port Index  State
    =====================================================
    50:00:09:73:00:1a:2b:4c             0           Online
    50:00:14:40:5d:8e:9f:3b             1           Online
    50:00:0e:1e:7c:a2:d1:5f             2           Online
    50:00:1a:cc:b3:44:6e:78             3           Online
    50:00:2d:91:f5:c9:a8:e3             4           Online
    ...
    Total N_Ports: 47
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nsAllShow: command not found` | Verify you are logged into the Brocade switch CLI (not the Linux shell) and have admin credentials. |
    | `Name Server not initialized` | Enable the name server on the switch using `nsEnable` and wait 30 seconds for fabric discovery to complete. |
---

## ISL Configuration

ISL (Inter-Switch Links) connect switches within a fabric. Trunking groups ISLs into a logical high-bandwidth pipe.

**Verify ISL ports are connected and online:**

```bash
switchShow
# ISL ports show type "E" and state "Online"
# Trunked ports show type "T"
```


```text title="Expected output"
Switch Information
  Switch Name:   fabric-switch-01
  Switch State:  Online
  Fabric State:  Online
  Fabric ID:     100
  Switch Role:   Principal
  Switch Domain: 1
  Switch WWN:    10:00:00:05:1e:a2:c3:d4

Port Information Summary
  Total Ports:   48
  Online Ports:  46
  Offline Ports: 2
  ISL Ports:     4

Port Status (sample):
  0   Online      E-Port  10:00:00:05:1e:a2:c3:d4  fabric-switch-02
  1   Online      E-Port  10:00:00:05:1e:a2:c3:d5  fabric-switch-03
  2   Online      E-Port  10:00:00:05:1e:a2:c3:d6  fabric-switch-04
  3   Online      T-Port  10:00:00:05:1e:a2:c3:d7  fabric-switch-01
  4   Offline     F-Port  --                       --
  5   Online      F-Port  50:00:14:40:5a:b2:1c:e8  storage-array-01
  ...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `switchShow: command not found` | Ensure you are logged into the Brocade switch via SSH or serial console, not a Linux host. |
    | `Permission denied` | Verify your user account has sufficient privileges; use `userConfig --show` to check role assignments. |
**Enable ISL trunking on ISL port groups:**

```bash
portCfgTrunkPort <port_number> 1
# Repeat for each port in the trunk group (ports must be adjacent: 0-7, 8-15, etc.)
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `portCfgTrunkPort: command not found` | Ensure you are logged into the Brocade switch via SSH or serial console, not your local workstation. |
    | `Invalid port number <port_number>` | Replace `<port_number>` with an actual port number (0-127 depending on switch model) and verify the port exists on your switch. |
    | `Port <port_number> is not adjacent to trunk group` | Trunk ports must be consecutive within a group (e.g., 0-7 or 8-15); do not skip ports or mix non-adjacent ranges. |
**Verify trunk master and member ports:**

```bash
trunkShow
# Shows trunk groups, master port, and aggregate bandwidth
```


```text title="Expected output"
Trunk Group Information
=======================

TrunkGroup: TG1
  Master Port: 0/0
  Member Ports: 0/0, 0/1, 0/2, 0/3
  Trunk State: Online
  Aggregate Bandwidth: 16 Gbps
  Load Balancing: Enabled

TrunkGroup: TG2
  Master Port: 1/0
  Member Ports: 1/0, 1/1
  Trunk State: Online
  Aggregate Bandwidth: 8 Gbps
  Load Balancing: Enabled

TrunkGroup: TG3
  Master Port: 2/0
  Member Ports: 2/0, 2/1, 2/2
  Trunk State: Offline
  Aggregate Bandwidth: 12 Gbps
  Load Balancing: Disabled
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `trunkShow: command not found` | Ensure you are logged into the Brocade switch via SSH/Telnet and have administrative privileges; the command is native to Fabric OS and not available on non-Brocade systems. |
    | `Access denied: insufficient privileges` | Log in with an account that has admin or operator-level permissions on the switch. |
**Check ISL topology:**

```bash
topologyShow
# Displays fabric topology including which switches connect via which ISL ports
```


```text title="Expected output"
Switch ID   Worldwide Name      Fabric Name         IP Address      Firmware
0           10:00:00:05:33:8a:bc:01  fabric-prod-01      192.168.1.10    v9.1.0
1           10:00:00:05:33:8a:bc:02  fabric-prod-01      192.168.1.11    v9.1.0
2           10:00:00:05:33:8a:bc:03  fabric-prod-02      192.168.1.20    v9.1.0

ISL Links:
Switch 0 Port 0 <-> Switch 1 Port 0 (Active, 16Gbps)
Switch 0 Port 1 <-> Switch 1 Port 1 (Active, 16Gbps)
Switch 1 Port 2 <-> Switch 2 Port 2 (Active, 16Gbps)
Switch 2 Port 3 <-> Switch 0 Port 3 (Standby, 16Gbps)

Connected Devices: 24
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `topologyShow: command not found` | Ensure you are logged into the Brocade switch via SSH or serial console, not a Linux host. |
    | `Permission denied` | Verify your user account has admin or fabric-admin role privileges using `userConfig --show`. |
---

## SANnav Integration

SANnav is Brocade's management and analytics platform. Adding the switch to SANnav enables centralized zoning, health monitoring, and performance data.

1. Log in to SANnav at `https://<sannav_server>`.
2. Navigate to **Discover > Add Fabric**.
3. Enter the switch management IP, credentials (`admin`), and the SNMP community string.
4. SANnav discovers the switch and all connected switches in the fabric.
5. Verify the switch appears in **SAN Fabric View** with all ports in the correct state.
6. Enable SNMP traps from the switch to SANnav:

```bash
snmpMibCapSet
# Set the SNMP trap destination to the SANnav server IP
snmpConfig --set mibCapability
agtcfgSet
# Enter the SANnav server IP as the trap recipient
```


```text title="Expected output"
SNMP MIB capability set successfully
Configuring SNMP parameters...
SNMP trap destination configured: 192.168.1.50
Agent configuration updated
Trap recipient IP registered: 192.168.1.50
Configuration saved to persistent storage
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `snmpMibCapSet: command not found` | Verify you are running this on a Brocade switch with FabricOS installed and have administrative privileges. |
    | `Error: Invalid IP address format for trap destination` | Ensure the SANnav server IP is in valid dotted-decimal notation (e.g., 192.168.1.50) before running snmpConfig. |
7. In SANnav, configure alert policies under **Monitoring > Alerts** for link-down events, port errors, and fabric changes.

---

## Validate Fabric

**Full fabric health check:**

```bash
# Check all ports for errors
portErrShow
# Columns to review: enc_in (encoding errors), crc_err (CRC errors), link_fail (link failures)
# All error counters should be zero on a freshly deployed fabric

# Check fabric routing
routeHelp
lsanZoneShow   # For FCR configurations

# Show inter-switch link statistics
islShow

# Verify all expected N_Ports are logged in
nsAllShow
```


```text title="Expected output"
portErrShow
Port 0: enc_in=0, crc_err=0, link_fail=0, loss_sync=0, loss_sig=0
Port 1: enc_in=0, crc_err=0, link_fail=0, loss_sync=0, loss_sig=0
Port 2: enc_in=0, crc_err=0, link_fail=0, loss_sync=0, loss_sig=0
Port 3: enc_in=0, crc_err=0, link_fail=0, loss_sync=0, loss_sig=0
Port 4: enc_in=0, crc_err=0, link_fail=0, loss_sync=0, loss_sig=0
Port 5: enc_in=0, crc_err=0, link_fail=0, loss_sync=0, loss_sig=0

routeHelp
Usage: route <command> [options]
  add <dest> <gateway> <metric>
  delete <dest>
  show

lsanZoneShow
Zone Name: prod_zone_01
  Members: 50:00:14:40:1a:2b:3c:4d, 50:00:14:40:1a:2b:3c:4e
  Status: Active

islShow
ISL Port 0 -- Remote Switch: fab-sw-02 (10:00:00:60:69:20:3a:b1), Remote Port 1, Speed: 16Gb
ISL Port 1 -- Remote Switch: fab-sw-03 (10:00:00:60:69:20:3a:b2), Remote Port 0, Speed: 16Gb
ISL Port 2 -- Remote Switch: fab-sw-04 (10:00:00:60:69:20:3a:b3), Remote Port 2, Speed: 16Gb

nsAllShow
Fabric Port Server (FPS) Status: Online
Total N_Ports registered: 24
Port 0: 50:00:14:40:1a:2b:3c:4d (STORAGE_ARRAY_01)
Port 1: 50:00:14:40:1a:2b:3c:4e (STORAGE_ARRAY_02)
Port 2: 50:00:14:40:1a:2b:3c:4f (HOST_SERVER_01)
Port 3: 50:00:14:40:1a:2b:3c:50 (HOST_SERVER_02)
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `portErrShow: command not found` | Verify you are logged into the Brocade switch CLI (not the Linux shell) and use the correct Fabric OS command syntax. |
    | `lsanZoneShow: No zones configured` | Create at least one zone using `zoneCreate` before querying zone status, or skip this check if FCR is not in use. |
    | `nsAllShow: Name Server not responding` | Restart the name server with `nsRestart` or check fabric connectivity with `fabricShow` to ensure the switch is fully operational. |
**Verify host-to-storage path visibility:**

From the host, scan for new FC targets and verify the storage volumes are visible. For a Linux host:

```bash
rescan-scsi-bus.sh
lsscsi
multipath -ll
```


```text title="Expected output"
Scanning for SCSI devices...
Scanning host 0 for SCSI devices
Scanning host 1 for SCSI devices
Scanning host 2 for SCSI devices
Scanning host 3 for SCSI devices

[0:0:0:0]    disk    NETAPP   LUN              4.02  /dev/sda 
[1:0:0:0]    disk    NETAPP   LUN              4.02  /dev/sdb 
[2:0:0:0]    disk    NETAPP   LUN              4.02  /dev/sdc 
[3:0:0:0]    disk    NETAPP   LUN              4.02  /dev/sdd 

mpatha (360a98000534e46437a6b4e6d41386b41) dm-0 NETAPP,LUN C-Mode
size=2.0T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 0:0:0:0 sda 8:0  active ready running
| `- 2:0:0:0 sdc 8:32 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 1:0:0:0 sdb 8:16 active ready running
  `- 3:0:0:0 sdd 8:48 active ready running
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `rescan-scsi-bus.sh: command not found` | Install sg3_utils package with `apt-get install sg3-utils` or `yum install sg3_utils`. |
    | `multipath: command not found` | Install device-mapper-multipath with `apt-get install multipath-tools` or `yum install device-mapper-multipath`. |
    | `No multipath output or "create: no paths"` | Verify Brocade fabric connectivity and zoning by checking `zonestat` on the switch, then rescan with `rescan-scsi-bus.sh` again. |
**Fabric-level consistency check:**

```bash
# Check for any fabric segmentation (all switches should be in one fabric)
fabricShow
# No "Segmented" switches should appear

# Check error counters are clean
portStatsClear
# Wait 60 seconds, then:
portErrShow
# All zeros indicates a clean fabric post-deployment
```


```text title="Expected output"
Fabric Information:
  Fabric Name: prod-fabric-01
  Fabric ID: 10:00:00:05:33:8a:bc:1d
  Switch Count: 4
  Switch Status: Online
  Segmentation Status: No

Switch Details:
  Switch 1: prod-switch-01 (10:00:00:05:33:8a:bc:1d) — Online
  Switch 2: prod-switch-02 (10:00:00:05:33:8a:bc:2e) — Online
  Switch 3: prod-switch-03 (10:00:00:05:33:8a:bc:3f) — Online
  Switch 4: prod-switch-04 (10:00:00:05:33:8a:bc:40) — Online

Statistics cleared on all ports.

Port Error Statistics (post-clear):
  Port 0/0: RX Errors: 0, TX Errors: 0, CRC: 0, Timeouts: 0
  Port 0/1: RX Errors: 0, TX Errors: 0, CRC: 0, Timeouts: 0
  Port 0/2: RX Errors: 0, TX Errors: 0, CRC: 0, Timeouts: 0
  Port 0/3: RX Errors: 0, TX Errors: 0, CRC: 0, Timeouts: 0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Segmented Fabric Detected: Switch prod-switch-03 is isolated` | Check ISL (Inter-Switch Link) connectivity between the isolated switch and the fabric core using `portShow` and verify cable connections. |
    | `portStatsClear: Command failed — Permission denied` | Ensure you are logged in with admin credentials or use `userConfig --change <username>` to elevate permissions. |
    | `portErrShow: Port 0/5 shows CRC errors: 1247` | Run `portDisable 0/5` followed by `portEnable 0/5` to reset the port, or replace the SFP transceiver if errors persist after restart. |
---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Fabric Os — Procedures](../operations/procedures/)
- [Fabric Os — Common Issues](../troubleshooting/common-issues/)
- [Fabric Os — How It Works](../architecture/how-it-works/)
