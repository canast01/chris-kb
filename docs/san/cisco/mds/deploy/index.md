---
tags:
  - deployment
  - san
search:
  boost: 1.5
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

```text
┌───────────────────────── Cisco MDS Deployment — Initial Setup to Production ──────────────────────────┐
│                                                                                                       │
│  Day-0 setup: license, NTP, AAA; create VSANs and assign ports; zone initiators                       │
│  to targets per VSAN; discover in NDFC; validate I/O with fctrace and fcping.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Phase 1: Day-0 Switch Setup          │  │           Phase 2: VSAN and Zoning          │   │
│   │            Install NX-OS license             │  │         Create VSAN per fabric role         │   │
│   │            Configure NTP servers             │  │           Assign FC ports to VSAN           │   │
│   │            Set TACACS+/RADIUS AAA            │  │         Create device aliases (WWN)         │   │
│   │        Enable features: fcoe/npv/etc         │  │         Create zones: 1 init + 1 tgt        │   │
│   │           Configure mgmt IP + VRF            │  │          Activate zone set per VSAN         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Device aliases persist across reboots; always use aliases not raw WWNs in zones.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Phase 3: ISL and NDFC             │  │             Phase 4: Validation             │   │
│   │         Configure TE port ISL trunks         │  │        show flogi database: HBA check       │   │
│   │         Verify allowed VSANs on ISL          │  │         fcping: initiator to target         │   │
│   │         Add switch to NDFC discovery         │  │          fctrace: path hop tracing          │   │
│   │            Sync zone DB via NDFC             │  │         show zoneset active: confirm        │   │
│   │           Enable SNMP v3 for NDFC            │  │        Host: rescan HBA after zoning        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS switches in SAN racks; cabled to host HBAs and storage ports; separate                           │
│  A and B fabric physical paths; management network cable to mgmt0 port.                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VSAN          = Virtual SAN; logical fabric; keep prod storage on dedicated VSAN                     │
│  Zone          = access control pair: one initiator (HBA) + one or more targets                       │
│  Device alias  = human-readable WWN label; use instead of raw hex in zones                            │
│  Zone set      = collection of zones activated as a group on a VSAN                                   │
│  TE port       = trunked E port; ISL carrying multiple VSANs between switches                         │
│  FLOGI         = Fabric Login; HBA login event; first step to reach storage                           │
│  fcping        = FC-layer ping; confirms path between initiator and target WWN                        │
│  fctrace       = FC path trace (like traceroute); shows hop-by-hop FCID path                          │
│  NDFC          = Nexus Dashboard Fabric Controller; central MDS management                            │
│  AAA           = Authentication, Authorization, Accounting; TACACS+ preferred                         │
│  NTP           = required; fabric domain elections can fail if clocks diverge                         │
│  Feature       = NX-OS capability flag; must enable (e.g. feature npv) before use                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

**Apply NX-OS license:**

```bash
copy tftp://10.0.0.100/mds-license.lic bootflash:
license install bootflash:mds-license.lic
show license
```

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

**Assign ports to VSANs:**

```bash
vsan database
  vsan 10 interface fc1/1-16    # Host-facing ports for Fabric A
  vsan 20 interface fc1/17-32   # (Not used on a single-fabric switch — adjust for your topology)
```

**Set the domain ID per VSAN:**

```bash
fcdomain domain 1 preferred vsan 10
fcdomain domain 2 preferred vsan 20
```

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

**Create a zoneset and add zones:**

```bash
zoneset name zs_fabric_a vsan 10
  member z_esx01_hba0_pmax_fa1_p0
  member z_esx01_hba1_pmax_fa2_p0
```

**Activate the zoneset:**

```bash
zoneset activate name zs_fabric_a vsan 10

# Save the zone configuration:
copy running-config startup-config
```

**Verify zones:**

```bash
show zoneset active vsan 10
show zone member vsan 10
show fcns database vsan 10
# Host and storage WWNs should appear in the name server database
```

---

## NDFC Integration

Cisco Nexus Dashboard Fabric Controller (NDFC) provides centralized management for Cisco SAN fabrics.

**Enable SNMP on the MDS switch for NDFC discovery:**

```bash
snmp-server community public ro
snmp-server host 10.0.0.30 traps version 2c public
snmp-server enable traps all
```

**Enable CFS (Cisco Fabric Services) for zone distribution:**

CFS automatically distributes zone changes across all switches in the VSAN when activated.

```bash
cfs enable
cfs distribute
show cfs status
```

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

**Verify zone enforcement:**

```bash
show zone member pwwn 10:00:00:90:fa:11:22:33 vsan 10
# Should list the zones containing this HBA WWN
```

**From the host (Linux):**

```bash
rescan-scsi-bus.sh
lsscsi
multipath -ll
# Storage paths should be visible through the MDS switch
```

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

**Error counter check:**

```bash
show interface fc1/1 counters
# Check: signal_loss, sync_loss, link_failure, invalid_crc
# All should be zero on a clean deployment

# Clear counters after initial verification:
clear counters interface fc1/1
```

**End-to-end path verification:**

```bash
# Test FC ping from switch to a storage target port:
fcping pwwn 50:00:09:73:00:1a:2b:3c vsan 10 count 5
# Should show 5/5 successful responses
```

**Traceroute within the fabric:**

```bash
fctrace pwwn 50:00:09:73:00:1a:2b:3c vsan 10
# Shows each hop through the fabric to the target port
```

Save configuration:

```bash
copy running-config startup-config
```

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
