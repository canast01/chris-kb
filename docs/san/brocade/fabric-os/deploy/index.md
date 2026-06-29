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

**Set the switch name:**

```bash
switchName "sw-fabric-a-01"
```

**Set management IP (if not using DHCP):**

```bash
ipaddrset
# Follow the interactive prompt to set:
# Ethernet IP Address: 10.0.0.10
# Ethernet Subnetmask: 255.255.255.0
# Gateway IP Address: 10.0.0.1
```

**Configure NTP:**

```bash
tsclockserver "10.0.0.5"
# Verify NTP sync:
tsclockserver
date
```

**Configure DNS:**

```bash
dnsconfig --add 10.0.0.53
```

**Enable SSH (if not already enabled):**

```bash
sshutil enable
```

---

## Set Domain ID and Fabric Parameters

The domain ID uniquely identifies the switch within the fabric. All fabric parameters must be consistent across all switches.

**Disable the switch before modifying fabric parameters:**

```bash
switchDisable
```

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

**Re-enable the switch:**

```bash
switchEnable
```

**Verify domain ID and fabric formation:**

```bash
fabricShow
# All switches in the fabric should appear with their domain IDs
# The "Principal" switch is shown with an asterisk

switchShow
# Switch state should be "Online"
```

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

**Verify zones are active:**

```bash
cfgShow
# Shows the active zone configuration and all zone members

zoneShow
# Lists all zones and their members
```

**Confirm name server entries (hosts and storage logged in):**

```bash
nsAllShow
# Lists all N_Ports registered in the name server — verify host and storage WWNs appear
```

---

## ISL Configuration

ISL (Inter-Switch Links) connect switches within a fabric. Trunking groups ISLs into a logical high-bandwidth pipe.

**Verify ISL ports are connected and online:**

```bash
switchShow
# ISL ports show type "E" and state "Online"
# Trunked ports show type "T"
```

**Enable ISL trunking on ISL port groups:**

```bash
portCfgTrunkPort <port_number> 1
# Repeat for each port in the trunk group (ports must be adjacent: 0-7, 8-15, etc.)
```

**Verify trunk master and member ports:**

```bash
trunkShow
# Shows trunk groups, master port, and aggregate bandwidth
```

**Check ISL topology:**

```bash
topologyShow
# Displays fabric topology including which switches connect via which ISL ports
```

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

**Verify host-to-storage path visibility:**

From the host, scan for new FC targets and verify the storage volumes are visible. For a Linux host:

```bash
rescan-scsi-bus.sh
lsscsi
multipath -ll
```

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
