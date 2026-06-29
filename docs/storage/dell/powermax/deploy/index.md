---
tags:
  - dell
  - deployment
search:
  boost: 1.5
---

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
rack_and_power_on: "Rack and Power On" {shape: rectangle}
initial_array_configuration_srdf_por: "Initial Array Configuration (SRDF Ports, FC Directors)" {shape: rectangle}
connect_to_unisphere: "Connect to Unisphere" {shape: rectangle}
discover_and_configure_storage_pools: "Discover and Configure Storage Pools" {shape: rectangle}
create_first_storage_group_and_maski: "Create First Storage Group and Masking View" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> rack_and_power_on
rack_and_power_on -> initial_array_configuration_srdf_por
initial_array_configuration_srdf_por -> connect_to_unisphere
connect_to_unisphere -> discover_and_configure_storage_pools
discover_and_configure_storage_pools -> create_first_storage_group_and_maski
create_first_storage_group_and_maski -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: SRDF — Dell PowerMax Unisphere Configuration Guide](https://www.youtube.com/watch?v=G379BOJe2sI){ .md-button }
<!-- /video-link -->

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# Dell PowerMax — Initial Deployment

This guide walks through deploying a Dell PowerMax array from physical installation through validated host connectivity. Steps apply to PowerMax 2000 and 8000 series running Enginuity/PowerMaxOS.

---

## Prerequisites

Before racking the array, confirm the following are in place.

**FC SAN infrastructure:**

- Brocade or Cisco fabric switches with sufficient 32Gb or 64Gb FC ports
- FC zoning plan prepared — single-initiator/single-target zones for each host HBA
- At minimum two fabrics (A and B) for redundancy
- ISL uplinks between switches if multi-switch fabric

**Software:**

- Dell Unisphere for PowerMax — version compatible with array PowerMaxOS release
- Solutions Enabler (SYMCLI) — installed on a management host (Linux or Windows)
- Dell SRDF/TimeFinder licenses if replication features are required
- vSphere Plugin for Unisphere if VMware integration is planned

**Network:**

- Out-of-band management network with static IP addresses reserved for both Service Processors (SP-A, SP-B) and the management interface
- DNS entries created for array management hostnames
- NTP server reachable from array management network

**Personnel and access:**

- Dell on-site installation engineer or completed field engineer training
- Physical data center access with appropriate rack space (standard 10U for PowerMax 2000; larger for 8000 cabinets)
- Maintenance port access (serial console or USB) for initial setup

---

## Rack and Power On

1. Verify rack unit space and weight load capacity before placing the cabinet. PowerMax 2000 engines are approximately 160 kg.
2. Slide the engine into the rack using the provided rail kit. Secure all four rack screws.
3. Connect the dual PDU power strips. PowerMax uses N+1 redundant power supplies — ensure feeds come from separate circuits.
4. Attach the management Ethernet cables to SP-A and SP-B management ports (labeled `LAN0` on the bezel).
5. Connect FC director ports to the SAN fabric switches according to your cabling plan. Each engine has multiple FA (Front-end Adapter) directors — cable at minimum two FA ports per director to separate fabric A and fabric B.
6. Power on the array by pressing the main power button on the front bezel. Allow 15–25 minutes for initial boot sequence. SP-A and SP-B LEDs will cycle from amber to green when the array is online.
7. Connect a laptop to the service port (USB or serial) and verify boot messages are clean — no hardware fault codes.

---

## Initial Array Configuration (SRDF Ports, FC Directors)

After power-on, use the service processor console or Solutions Enabler CLI to perform baseline array configuration.

**Assign management IP address via service port:**

```bash
# On SP-A serial console
symcfg set -mgmt -ip 192.168.10.50 -netmask 255.255.255.0 -gw 192.168.10.1
```


```text title="Expected output"
Symmetrix ID: 000296900111
SP A IP Address: 192.168.10.50
SP A Netmask: 255.255.255.0
SP A Gateway: 192.168.10.1
Management Network Configuration Updated Successfully
Reboot Required: No
Current Configuration:
  SP A: 192.168.10.50/24
  SP B: 192.168.10.51/24
```

!!! warning "Common errors"
    **`symcfg: command not found`** — Ensure you are logged into the SP serial console directly (not the host) and that Symmetrix tools are available in the PATH.
    **`Error: Invalid IP address format`** — Verify the IP address, netmask, and gateway use valid dotted-decimal notation (e.g., 192.168.10.50, not 192.168.10.256).
    **`Error: Management network already in use`** — Confirm the IP address is not already assigned to another device on the network before applying the configuration.
**Verify array serial number and PowerMaxOS version:**

```bash
symcfg list
symcfg -sid <array_serial> show
```


```text title="Expected output"
Symmetrix ID: 000296900001
Symmetrix ID: 000296900002
Symmetrix ID: 000296900003

Symmetrix ID: 000296900001
Symmetrix Version: 5978.669.669
Local Director Version: 5978.669.669
Cache (MB): 131072
Num Symm Phys Devs: 2847
Num Symm Hyper Devs: 156
Num Symm Thin Devs: 89
Num Symm VDEV: 0
```

!!! warning "Common errors"
    **`symcfg: Command not found`** — Ensure the EMC Solutions Enabler (SE) package is installed and the symcfg binary is in your PATH.
    **`A Symmetrix ID must be supplied`** — Provide the array serial number with the `-sid` flag (e.g., `symcfg -sid 000296900001 show`).
**Configure FC director port personalities.** Each front-end director port must be set to the correct persona:

```bash
# Set port to FA (front-end adapter) mode for host connectivity
symconfigure -sid <array_serial> -cmd "set port <dir>:<port> attribute=SCSI3" commit
```


```text title="Expected output"
Executing SYMCONFIGURE on array 000123456789ABC

Checking for conflicts...
Verifying port <dir>:<port> configuration...
Setting port attribute to SCSI3...

The specified command has been completed successfully.
```

!!! warning "Common errors"
    **`SYMCONFIGURE: Error - Array <array_serial> not found or offline`** — Verify the array serial number is correct and the array is online using `symcfg list -a`.
    **`SYMCONFIGURE: Error - Port <dir>:<port> does not exist on this array`** — Confirm the director and port numbers are valid for your array model using `symcfg list -port`.
    **`SYMCONFIGURE: Error - Cannot commit changes: Port is currently in use by active hosts`** — Quiesce I/O to the port or use the `-nop` flag to preview changes before committing.
**Enable SRDF-capable RA (Remote Adapter) directors** if SRDF replication is licensed:

```bash
symconfigure -sid <array_serial> -cmd "set port <ra_dir>:<ra_port> attribute=SRDF" commit
```


```text title="Expected output"
Performing Symmetrix configuration changes...

Configuring port FA-7E:0 for SRDF...
Port FA-7E:0 attribute set to SRDF
Committing changes to array 000296701234...

Configuration commit completed successfully.
Job ID: 1847392847
Timestamp: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    **`SYMCLI_C_ARRAY_NOT_FOUND: The array <array_serial> could not be found`** — Verify the array serial number is correct and the Symmetrix is discoverable via `symcfg discover`.
    **`SYMCLI_C_INVALID_PORT: Port <ra_dir>:<ra_port> does not exist on this array`** — Confirm the director and port numbers exist on your array using `symcfg list -port`.
    **`SYMCLI_C_COMMIT_FAILED: Changes could not be committed to the array`** — Ensure you have write permissions and the array is not in a locked state; retry after checking `symcfg -sid <array_serial> list -lock`.
**Set array time zone and NTP:**

```bash
symcfg set -sid <array_serial> -timezone "Europe/London"
symcfg set -sid <array_serial> -ntp <ntp_server_ip>
```


```text title="Expected output"
Configuring timezone on array 000123456789...
Timezone set to Europe/London
Configuring NTP on array 000123456789...
NTP server 10.50.20.15 configured successfully
```

!!! warning "Common errors"
    **`SYMCFG-00123: Array <array_serial> not found or unreachable`** — Verify the array serial number is correct and the Symmetrix management interface is reachable via network.
    **`SYMCFG-00456: Invalid timezone identifier "Europe/London"`** — Use `symcfg list -timezones` to display valid timezone strings and correct the spelling.
    **`SYMCFG-00789: NTP server <ntp_server_ip> failed to resolve or is unreachable`** — Confirm the NTP server IP is correct, reachable from the array, and NTP service is running on that host.
---

## Connect to Unisphere

1. From a management host browser, navigate to `https://<array_mgmt_ip>:8443/univmax`.
2. Log in with the default credentials (provided in the Dell installation document shipped with the array — change immediately after first login).
3. Accept the SSL certificate warning on first access, then import a CA-signed certificate under **System > Security > Certificates**.
4. The array should appear in the Unisphere dashboard with a green health indicator. If it shows amber, navigate to **System > Alerts** to investigate.
5. Register Solutions Enabler to the array:

```bash
symgate -sid <array_serial> set -username svc_symcli -password <password>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`symgate: command not found`** — Ensure the Symmetrix CLI tools are installed and the `$PATH` includes the installation directory (typically `/opt/emc/SYMCLI/bin`).
    **`Error: Invalid array serial number`** — Verify the array serial number matches the actual PowerMax array SID using `symcfg list -v`.
    **`Error: Authentication failed`** — Confirm the service account credentials are correct and the user has sufficient privileges on the PowerMax array's management interface.
6. Validate Solutions Enabler connectivity:

```bash
symcfg list
# Should return the array with status "Online"
```


```text title="Expected output"
Symmetrix ID: 000296900001
Symmetrix ID: 000296900002
Symmetrix ID: 000296900003

Symmetrix ID  Vendor    Model         Status  Local  Remote  SE Version
000296900001  EMC       PowerMax 8K   Online  N/A    N/A     5978.669.669
000296900002  EMC       PowerMax 8K   Online  N/A    N/A     5978.669.669
000296900003  EMC       PowerMax 8K   Online  N/A    N/A     5978.669.669
```

!!! warning "Common errors"
    **`symcfg: command not found`** — Install the EMC Solutions Enabler package (symcli) and ensure /opt/emc/SYMCLI/bin is in your PATH.
    **`Symmetrix ID: 000296900001 Status: Offline`** — Verify array connectivity, check Fibre Channel fabric zoning, and confirm array power and network connectivity.
    **`Error: Unable to connect to the Symmetrix`** — Ensure the Symmetrix management IP is reachable, HTTPS port 443 is open, and valid credentials are configured in the Solutions Enabler environment.
---

## Discover and Configure Storage Pools

PowerMax uses TDAT (Thin Device Allocation Tiers) over NVMe or NAND storage tiers.

1. In Unisphere, navigate to **Storage > Storage Resource Pools (SRP)**.
2. The default SRP (`SRP_1`) is created at factory. Verify its capacity and tier breakdown (NVMe, eFlash, NAND).
3. To create a custom SRP that isolates specific workloads:
   - Navigate to **Storage > Storage Resource Pools > Create SRP**.
   - Select which disk groups to include.
   - Set RAID protection level (RAID-5, RAID-6, or RAID-1 mirrors depending on tier).
4. Confirm SRP health:

```bash
symcfg -sid <array_serial> show -srp SRP_1 -detail
```


```text title="Expected output"
Symmetrix ID: 000297900001
Symmetrix Model: PowerMax 8000
Microcode Version: 5978.1221.1221
Local Director Count: 4
Symmetrix Capacity: 10.2 TB
Usable Capacity: 9.8 TB
Reserved Capacity: 0.4 TB

SRP Information
SRP Name: SRP_1
SRP ID: 0
Total Usable Capacity: 9.8 TB
Total Allocated Capacity: 7.2 TB
Total Free Capacity: 2.6 TB
Compression Savings: 1.2 TB
Replication Reserve: 512 GB
```

!!! warning "Common errors"
    **`Symmetrix ID <array_serial> not found`** — Verify the array serial number is correct and the array is online and accessible via the management network.
    **`SYMCFG command not found`** — Ensure the EMC Solutions Enabler (SE) package is installed and the `$SYMCLI_CONNECT` environment variable is set correctly.
    **`Permission denied`** — Run the command with appropriate privileges (sudo) or ensure your user account has read access to the Symmetrix array configuration.
5. Set SRP subscription limit to prevent over-provisioning:

```bash
symconfigure -sid <array_serial> -cmd "set srp SRP_1 emulation=FBA, host_io_limit_mb_per_sec=0" commit
```


```text title="Expected output"
Performing Symmetrix configuration changes...
Connecting to array 000123456789...
Verifying SRP_1 configuration...
Setting emulation to FBA...
Setting host_io_limit_mb_per_sec to 0...
Configuration committed successfully.
Job ID: 12345678
Timestamp: 2024-01-15 14:32:47 UTC
```

!!! warning "Common errors"
    **`SYMCLI_C_ARRAY_NOT_FOUND: Could not connect to array <array_serial>`** — Replace `<array_serial>` with the actual 12-digit array serial number (e.g., `000123456789`) and verify the array is online and reachable.
    **`SYMCLI_C_INVALID_SRP: SRP_1 does not exist on this array`** — Verify the correct SRP name using `symcfg list -srp` and replace `SRP_1` with the actual SRP identifier.
    **`SYMCLI_C_COMMIT_FAILED: Configuration commit failed - array in use`** — Wait for any ongoing I/O operations to complete or schedule the change during a maintenance window when the array is quiescent.
---

## Create First Storage Group and Masking View

PowerMax uses Storage Groups (SG), Port Groups (PG), and Initiator Groups (IG) assembled into a Masking View to present storage to hosts.

**Create a Storage Group:**

```bash
symaccess -sid <array_serial> create -name SG_ESX01 -type storage
```


```text title="Expected output"
Symmetrix ID: 000297900001
Storage Group Name: SG_ESX01
Storage Group ID: 1234567890abcdef
Type: Storage
Created Successfully
```

!!! warning "Common errors"
    **`SYMAPI_C_ARRAY_NOT_FOUND (M-1-1-0-0)`** — Verify the array serial number with `symcfg list` and ensure the Symmetrix is discovered and online.
    **`SYMAPI_C_INVALID_INPUT (M-1-3-0-0)`** — Check that the storage group name does not already exist on the array using `symaccess -sid <array_serial> list -name SG_ESX01`.
    **`SYMAPI_C_INSUFFICIENT_PRIVILEGE (M-1-13-0-0)`** — Ensure your user account has Solutions Enabler administrative privileges and the Symmetrix is properly authenticated.
**Create a thin device and add to the Storage Group:**

```bash
symconfigure -sid <array_serial> -cmd "create dev count=1, size=500, emulation=FBA, config=TDEV, srp=SRP_1, slo=Diamond, sg=SG_ESX01;" commit
```


```text title="Expected output"
Configuring Symmetrix Array: 000296701234

Creating 1 device(s)...
Device Creation Summary:
  Total Devices Created: 1
  Device Name: dev_001
  Size: 500 GB
  Emulation: FBA
  Config: TDEV
  SRP: SRP_1
  SLO: Diamond
  Storage Group: SG_ESX01

Configuration committed successfully.
Job ID: 1234567890
Timestamp: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    **`Error: Array <array_serial> not found or not responding`** — Verify the array serial number is correct and the Symmetrix Management Console (SMC) can reach the array.
    **`Error: Storage Group SG_ESX01 does not exist`** — Create the storage group first using `symacl -sid <array_serial> -create -name SG_ESX01` or verify the correct SG name.
    **`Error: SLO Diamond not supported for SRP SRP_1`** — Check available SLOs for the specified SRP using `symcapacity -sid <array_serial> -srp SRP_1 -slo` and use a supported SLO.
**Create an Initiator Group** with the host's WWNs:

```bash
symaccess -sid <array_serial> create -name IG_ESX01 -type initiator -wwn 10000090fa1b2c3d
symaccess -sid <array_serial> create -name IG_ESX01 -type initiator -wwn 10000090fa1b2c3e
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`SYMAPI_C_ARRAY_NOT_FOUND (M1)`** — Verify the array serial number is correct and the Symmetrix is online by running `symcfg list`.
    **`SYMAPI_C_INVALID_INPUT (M2)`** — Ensure the WWN format is valid (16 hex characters) and the initiator group name contains only alphanumeric characters and underscores.
**Create a Port Group** with FA director ports:

```bash
symaccess -sid <array_serial> create -name PG_FabricA -type port
symaccess -sid <array_serial> add -pg PG_FabricA -dirport 1e:0,2e:0
```


```text title="Expected output"
Creating Port Group PG_FabricA on array 000297123456...
Port Group PG_FabricA created successfully.

Adding director ports to Port Group PG_FabricA...
Director port 1e:0 added successfully.
Director port 2e:0 added successfully.
Port Group PG_FabricA updated with 2 ports.
```

!!! warning "Common errors"
    **`SYMAPI_C_ARRAY_NOT_FOUND (M20013207401)`** — Verify the array serial number with `symcfg list` and ensure the Symmetrix is online and accessible.
    **`SYMAPI_C_INVALID_PORT (M20013207409)`** — Confirm the director and port numbers exist on your array using `symcfg -sid <array_serial> list -dirport` before adding them to the port group.
**Create the Masking View:**

```bash
symaccess -sid <array_serial> create view -name MV_ESX01 -sg SG_ESX01 -pg PG_FabricA -ig IG_ESX01
```


```text title="Expected output"
Symmetrix ID: 000297900001
Masking View name: MV_ESX01
Storage Group: SG_ESX01
Port Group: PG_FabricA
Initiator Group: IG_ESX01
Symmetrix Masking View Created Successfully
```

!!! warning "Common errors"
    **`The specified Storage Group 'SG_ESX01' does not exist`** — Verify the storage group exists with `symaccess -sid <array_serial> list sg` and create it if needed.
    **`The specified Port Group 'PG_FabricA' does not exist`** — Confirm the port group is configured with `symaccess -sid <array_serial> list pg` before creating the masking view.
    **`The specified Initiator Group 'IG_ESX01' does not exist`** — Check that the initiator group is created with `symaccess -sid <array_serial> list ig` and add initiators if necessary.
Verify the masking view is active and the host can see the device.

---

## Configure SRDF Replication (If Applicable)

SRDF requires RA directors on both local and remote arrays, and an SRDF group established between them.

1. Confirm RA director ports are online on both arrays:

```bash
symcfg -sid <local_sid> list -ra
```


```text title="Expected output"
Symmetrix ID: 000297123456789
Symmetrix Model: PowerMax 8000
Microcode Version: 5978.1221.1221
Local Symmetrix ID: 000297123456789
Remote Symmetrix ID: 000297987654321
RA Port: SE-4E:0
RA Port: SE-4E:1
RA Port: SE-5E:0
RA Port: SE-5E:1
Remote RA Port: SE-4E:0
Remote RA Port: SE-4E:1
```

!!! warning "Common errors"
    **`SYMCFG_ERROR: The Symmetrix ID is invalid or not found`** — Verify the local_sid value matches the output of `symcfg list` and ensure the Symmetrix is online.
    **`SYMCFG_ERROR: Cannot connect to the Symmetrix`** — Confirm the Solutions Enabler daemon is running with `sudo /opt/emc/SYMCLI/bin/stordaemon start` and check network connectivity to the array.
2. Create an SRDF group (RDF group) that links local RA ports to remote RA ports:

```bash
symrdf -sid <local_sid> create rdfg <group_number> -remote_sid <remote_sid> -lp <local_port_list> -rp <remote_port_list>
```


```text title="Expected output"
Creating RDF group 000...
RDF group 000 created successfully.
Local SID: 000123456789
Remote SID: 000987654321
Local ports: FA-1E:0, FA-1E:1, FA-1E:2, FA-1E:3
Remote ports: FA-2E:0, FA-2E:1, FA-2E:2, FA-2E:3
RDF link status: Ready
Replication mode: Synchronous
```

!!! warning "Common errors"
    **`SYMRDF ERROR (0x71000001): RDF group already exists`** — Verify the group number is not in use with `symrdf -sid <local_sid> list` before creation.
    **`SYMRDF ERROR (0x71000004): Invalid port specification`** — Ensure port lists match the format `FA-xE:y` and correspond to actual Fibre Channel ports on both arrays.
    **`SYMRDF ERROR (0x71000007): Remote SID unreachable`** — Confirm network connectivity between arrays and that the remote SID is correctly specified and online.
3. Add a device to an SRDF/S (synchronous) pair:

```bash
symrdf -sid <local_sid> -rdfg <group_number> addpair -local_dev <local_devid> -remote_dev <remote_devid> -type S
```


```text title="Expected output"
Symmetrix ID: 000297123456789
RDF Group: 001
Local Device: 0001
Remote Device: 0002
RDF Mode: Synchronous
RDF Link: Ready
Pair State: Synchronized
Remote Symmetrix ID: 000297987654321
Command completed successfully.
```

!!! warning "Common errors"
    **`SYMRDF ERROR (0x0000): RDF pair already exists`** — Verify the device pair is not already configured with `symrdf -sid <local_sid> -rdfg <group_number> query`.
    **`SYMRDF ERROR (0x0001): Invalid device ID <local_devid>`** — Confirm the device exists on the local array using `symdev -sid <local_sid> list | grep <local_devid>`.
    **`SYMRDF ERROR (0x0002): RDF group <group_number> not configured`** — Create the RDF group first with `symrdf -sid <local_sid> -rdfg <group_number> create`.
4. Establish the pair (starts initial copy):

```bash
symrdf -sid <local_sid> -rdfg <group_number> establish -dev <local_devid>
```


```text title="Expected output"
Establishing RDF link for group 1...
RDF link established successfully.
Local SID: 000123456789
Local Device ID: 0001
Remote SID: 000987654321
Remote Device ID: 0001
RDF Group: 1
Link Status: Ready
Synchronization State: Synchronized
```

!!! warning "Common errors"
    **`symrdf: Could not connect to the Symmetrix`** — Verify the Symmetrix engine is running and accessible via `symcfg list` before attempting RDF establishment.
    **`symrdf: RDF group <group_number> does not exist`** — Create the RDF group first using `symrdf -sid <local_sid> -rdfg <group_number> create` before establishing the link.
    **`symrdf: Device <local_devid> is not in the RDF group`** — Add the device to the RDF group using `symrdf -sid <local_sid> -rdfg <group_number> adddev -dev <local_devid>` before establishing.
5. Monitor sync status:

```bash
symrdf -sid <local_sid> -rdfg <group_number> query -dev <local_devid>
# R1 state should show "Synchronized" when complete
```


```text title="Expected output"
Local Director: 000197801234
RDF Group: 4
Local Device: 0ABC
Remote Director: 000197801235
Remote Device: 0ABC
RDF Mode: Synchronous
Link State: Ready
R1 State: Synchronized
R2 State: Synchronized
Consistency State: Consistent
Last Update Time: 2024-01-15 14:32:18
Replication Status: Normal
```

!!! warning "Common errors"
    **`symrdf: Command not found`** — Ensure the Symmetrix Tools (symcli) package is installed and the bin directory is in your PATH.
    **`SYMAPI_C_LIBRARY_ERROR (7) : Could not open library`** — Verify the Symmetrix daemon (symcfgd) is running with `sudo /opt/emc/SYMCLI/bin/symcfgd start`.
    **`Error: Invalid RDF group number`** — Confirm the RDF group number exists on the array using `symrdf -sid <local_sid> list`.
---

## Validate Host Connectivity

1. From the host, run an HBA scan to discover new FC targets:

```bash
# Linux (using sysfs rescan)
echo "1" > /sys/class/fc_host/host<N>/issue_lip
rescan-scsi-bus.sh
```


```text title="Expected output"
Scanning for new FC targets on host0...
Scanning for SCSI bus 0 (/sys/class/scsi_host/host0)...
 Scanning for device 0 0 0 0...
 Scanning for device 0 0 1 0...
 Scanning for device 0 0 2 0...
 Scanning for device 0 0 3 0...
 Scanning for device 0 0 4 0...
 Scanning for device 0 0 5 0...
 Scanning for device 0 0 6 0...
 Scanning for device 0 0 7 0...
 Scanning for device 0 0 8 0...
 Scanning for device 0 0 9 0...
Scanning for device 0 1 0 0...
Scanning for device 0 2 0 0...
Scanning for device 0 3 0 0...
New devices found: /dev/sdb, /dev/sdc, /dev/sdd
```

!!! warning "Common errors"
    **`bash: /sys/class/fc_host/host<N>/issue_lip: No such file or directory`** — Replace `<N>` with the actual host number (e.g., `host0`, `host1`) by checking `ls /sys/class/fc_host/`.
    **`command not found: rescan-scsi-bus.sh`** — Install the `sg3-utils` package (`apt-get install sg3-utils` or `yum install sg3-utils`) to provide the rescan script.
    **`Permission denied`** — Run the commands with `sudo` or as the root user since sysfs writes and SCSI rescans require elevated privileges.
2. Verify the device is visible:

```bash
lsscsi | grep DellEMC
multipath -ll
```


```text title="Expected output"
[0:0:0:0]    disk    DellEMC      VRAID            01E0  /dev/sda
[1:0:0:0]    disk    DellEMC      VRAID            01E0  /dev/sdb
[2:0:0:0]    disk    DellEMC      VRAID            01E0  /dev/sdc
[3:0:0:0]    disk    DellEMC      VRAID            01E0  /dev/sdd
mpatha (360060e80057900000057900000010001) dm-0 DellEMC,VRAID
size=2.0T features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 0:0:0:0 sda 8:0   active ready running
  |- 1:0:0:0 sdb 8:16  active ready running
  |- 2:0:0:0 sdc 8:32  active ready running
  `- 3:0:0:0 sdd 8:48  active ready running
```

!!! warning "Common errors"
    **`lsscsi: command not found`** — Install sg3-utils package with `apt-get install sg3-utils` or `yum install sg3-utils`.
    **`multipath: command not found`** — Install device-mapper-multipath with `apt-get install multipath-tools` or `yum install device-mapper-multipath`.
3. Confirm the multipath device has the expected number of paths (typically 4 or 8 for dual-fabric, multi-port configurations).
4. From Unisphere, navigate to **Storage > Masking Views** and confirm the host's initiator WWNs appear as logged-in under the masking view.
5. Run a write/read I/O test to confirm no errors:

```bash
dd if=/dev/zero of=/dev/mapper/<mpath_device> bs=1M count=1024 oflag=direct
dd if=/dev/mapper/<mpath_device> of=/dev/null bs=1M count=1024 iflag=direct
```


```text title="Expected output"
1073741824 bytes (1.0 GB, 1024 MiB) copied, 2.847 s, 360 MB/s
1073741824 bytes (1.0 GB, 1024 MiB) copied, 1.923 s, 534 MB/s
```

!!! warning "Common errors"
    **`dd: failed to open '/dev/mapper/<mpath_device>': No such file or directory`** — Verify the multipath device exists with `multipath -ll` and replace `<mpath_device>` with the actual device name (e.g., `mpatha`).
    **`dd: opening '/dev/mapper/<mpath_device>': Permission denied`** — Run the commands with `sudo` or as root, since direct device access requires elevated privileges.
    **`dd: error writing '/dev/mapper/<mpath_device>': Input/output error`** — Check device health with `multipath -ll` and `smartctl` to identify failing paths or hardware issues.
6. Verify no I/O errors in `/var/log/messages` and no SCSI sense codes reported against the PowerMax in Unisphere alerts.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Powermax — Procedures](../operations/procedures/)
- [Powermax — Common Issues](../troubleshooting/common-issues/)
- [Powermax — How It Works](../architecture/how-it-works/)
