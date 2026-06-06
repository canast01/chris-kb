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

**Verify array serial number and PowerMaxOS version:**

```bash
symcfg list
symcfg -sid <array_serial> show
```

**Configure FC director port personalities.** Each front-end director port must be set to the correct persona:

```bash
# Set port to FA (front-end adapter) mode for host connectivity
symconfigure -sid <array_serial> -cmd "set port <dir>:<port> attribute=SCSI3" commit
```

**Enable SRDF-capable RA (Remote Adapter) directors** if SRDF replication is licensed:

```bash
symconfigure -sid <array_serial> -cmd "set port <ra_dir>:<ra_port> attribute=SRDF" commit
```

**Set array time zone and NTP:**

```bash
symcfg set -sid <array_serial> -timezone "Europe/London"
symcfg set -sid <array_serial> -ntp <ntp_server_ip>
```

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

6. Validate Solutions Enabler connectivity:

```bash
symcfg list
# Should return the array with status "Online"
```

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

5. Set SRP subscription limit to prevent over-provisioning:

```bash
symconfigure -sid <array_serial> -cmd "set srp SRP_1 emulation=FBA, host_io_limit_mb_per_sec=0" commit
```

---

## Create First Storage Group and Masking View

PowerMax uses Storage Groups (SG), Port Groups (PG), and Initiator Groups (IG) assembled into a Masking View to present storage to hosts.

**Create a Storage Group:**

```bash
symaccess -sid <array_serial> create -name SG_ESX01 -type storage
```

**Create a thin device and add to the Storage Group:**

```bash
symconfigure -sid <array_serial> -cmd "create dev count=1, size=500, emulation=FBA, config=TDEV, srp=SRP_1, slo=Diamond, sg=SG_ESX01;" commit
```

**Create an Initiator Group** with the host's WWNs:

```bash
symaccess -sid <array_serial> create -name IG_ESX01 -type initiator -wwn 10000090fa1b2c3d
symaccess -sid <array_serial> create -name IG_ESX01 -type initiator -wwn 10000090fa1b2c3e
```

**Create a Port Group** with FA director ports:

```bash
symaccess -sid <array_serial> create -name PG_FabricA -type port
symaccess -sid <array_serial> add -pg PG_FabricA -dirport 1e:0,2e:0
```

**Create the Masking View:**

```bash
symaccess -sid <array_serial> create view -name MV_ESX01 -sg SG_ESX01 -pg PG_FabricA -ig IG_ESX01
```

Verify the masking view is active and the host can see the device.

---

## Configure SRDF Replication (If Applicable)

SRDF requires RA directors on both local and remote arrays, and an SRDF group established between them.

1. Confirm RA director ports are online on both arrays:

```bash
symcfg -sid <local_sid> list -ra
```

2. Create an SRDF group (RDF group) that links local RA ports to remote RA ports:

```bash
symrdf -sid <local_sid> create rdfg <group_number> -remote_sid <remote_sid> -lp <local_port_list> -rp <remote_port_list>
```

3. Add a device to an SRDF/S (synchronous) pair:

```bash
symrdf -sid <local_sid> -rdfg <group_number> addpair -local_dev <local_devid> -remote_dev <remote_devid> -type S
```

4. Establish the pair (starts initial copy):

```bash
symrdf -sid <local_sid> -rdfg <group_number> establish -dev <local_devid>
```

5. Monitor sync status:

```bash
symrdf -sid <local_sid> -rdfg <group_number> query -dev <local_devid>
# R1 state should show "Synchronized" when complete
```

---

## Validate Host Connectivity

1. From the host, run an HBA scan to discover new FC targets:

```bash
# Linux (using sysfs rescan)
echo "1" > /sys/class/fc_host/host<N>/issue_lip
rescan-scsi-bus.sh
```

2. Verify the device is visible:

```bash
lsscsi | grep DellEMC
multipath -ll
```

3. Confirm the multipath device has the expected number of paths (typically 4 or 8 for dual-fabric, multi-port configurations).
4. From Unisphere, navigate to **Storage > Masking Views** and confirm the host's initiator WWNs appear as logged-in under the masking view.
5. Run a write/read I/O test to confirm no errors:

```bash
dd if=/dev/zero of=/dev/mapper/<mpath_device> bs=1M count=1024 oflag=direct
dd if=/dev/mapper/<mpath_device> of=/dev/null bs=1M count=1024 iflag=direct
```

6. Verify no I/O errors in `/var/log/messages` and no SCSI sense codes reported against the PowerMax in Unisphere alerts.
