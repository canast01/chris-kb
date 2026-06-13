---
tags:
  - dell
  - deployment
---
# Dell Unity XT — Initial Deployment

```text
┌───────────────────────────────── Dell Unity XT — Deployment Sequence ─────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Hardware: 2U rack space (base chassis) + DAE shelves if capacity expansion ordered                   │
│  Network: 10GbE/25GbE for iSCSI/NFS; FC switches if FC planned; OOB management network                │
│  IPs reserved: SP-A mgmt, SP-B mgmt, iSCSI data ports per SP; DNS and NTP details noted               │
│  Licenses: Dell capacity-based licence key files; LDAP/AD details for directory authentication        │
│  Unisphere for Unity (embedded HTML5) — accessible from management IP once powered on                 │
│                                                                                                       │
│                                        │  rack and cable                                              │
│                                        ▼                                                              │
│  Step 2 · Rack, Cable, and Power On                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Mount Unity chassis using rail kit; attach DAE shelves if ordered via SAS cables                     │
│  Connect SP-A and SP-B management ports to OOB management switch                                      │
│  Connect data ports (iSCSI or FC) to data switches / SAN fabric A and B                               │
│  Connect dual PSU cables to separate PDU circuits; power on; allow 15 min for initialisation          │
│                                                                                                       │
│                                        │  run setup wizard                                            │
│                                        ▼                                                              │
│  Step 3 · Unisphere Initial Setup                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Browse to SP-A management IP (Unisphere for Unity); complete Setup Wizard                            │
│  Set array name, management IPs, NTP, DNS, SMTP/syslog alert destinations                             │
│  Upload licence key: System → Settings → Licenses → Import Licence File                               │
│  Join Active Directory or LDAP if NAS or directory-based auth is required                             │
│                                                                                                       │
│                                        │  configure pools and volumes                                 │
│                                        ▼                                                              │
│  Step 4 · Storage Pools and Volume Provisioning                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Auto-configure pool: Unity recommends pool layout based on available drives — accept or customise    │
│  Create LUNs for block workloads: specify size, pool, host access, optional thin provisioning         │
│  Create NAS server and file systems for NFS/SMB; assign to a storage pool                             │
│  Create VMware datastores (NFS or iSCSI LUNs) if vSphere integration is planned                       │
│                                                                                                       │
│                                        │  connect hosts                                               │
│                                        ▼                                                              │
│  Step 5 · Host Connectivity                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Register hosts: Hosts → Create; provide host name, OS, and initiators (iQN or FC WWPNs)              │
│  Assign LUNs to hosts: LUN → Access → Hosts; select host and access mode                              │
│  Configure FC zoning if applicable: submit zone changes for each initiator/target pair                │
│  Rescan host storage adapters; confirm LUNs visible; format and label per OS runbook                  │
│                                                                                                       │
│                                        │  validate and baseline                                       │
│                                        ▼                                                              │
│  Step 6 · Validation and Baseline                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Run Unisphere health check: System → Health → all SPs, drives, ports, fans green                     │
│  Record: array serial, SP serials, pool names, LUN IDs, host-to-LUN mapping table                     │
│  Enable SupportAssist/CloudIQ telemetry for proactive monitoring                                      │
│  Set capacity alert thresholds; schedule quarterly health review task in ITSM                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This guide covers the initial deployment of a Dell Unity XT array from physical installation through validated host access. Applies to Unity XT 380, 480, 680, and 880 models running OE 5.x.

---

## Prerequisites

**Hardware checklist:**

- Rack space confirmed (2U for base chassis; additional DAEs if capacity expansion is included)
- Dual AC power circuits available — Unity XT uses N+1 redundant PSUs
- 10GbE or 25GbE switches for iSCSI/NFS management and data paths
- FC switches (Brocade or Cisco) if FC connectivity is planned
- Management workstation on same subnet or routed access to array management IP

**Software and licensing:**

- Dell EMC Unisphere for Unity (HTML5 interface, embedded on the array)
- License key files provided by Dell — Unity uses a capacity-based license model
- NTP server details for time synchronization
- LDAP/AD server details if directory-based authentication is required

**IP address plan:**

| Component          | IP            |
|--------------------|---------------|
| SP-A management    | 192.168.1.50  |
| SP-B management    | 192.168.1.51  |
| iSCSI port 0 SP-A  | 10.0.10.10    |
| iSCSI port 0 SP-B  | 10.0.10.11    |
| NAS pool NFS VIP   | 10.0.10.20    |

Adjust for your environment before proceeding.

---

## Rack and Cable

1. Mount the Unity XT chassis into the rack using the supplied rail kit. Tighten all four rack post screws before applying weight.
2. If DAE (Disk Array Enclosure) expansion shelves are included, rack them directly below the main chassis and cable the SAS expansion ports using the factory-labeled cables (SAS-A to SP-A, SAS-B to SP-B).
3. Connect PSU cables from each PSU to separate PDU circuits.
4. Connect SP-A and SP-B management Ethernet ports to your OOB management switch.
5. Connect iSCSI or FC data ports:
   - For iSCSI: connect 10/25GbE ports to data switches
   - For FC: connect 16/32Gb FC ports to SAN switches (cable at least two ports per SP to separate fabrics)
6. Power on the array. Initial boot takes 10–15 minutes. The SP-A and SP-B fault LEDs will be amber during boot and turn off (no fault) when the array is ready.

---

## Run Unisphere Initial Configuration Wizard

Unity XT embeds Unisphere directly on the array. No external server is needed for the initial setup wizard.

1. Connect a laptop directly to the array's service port Ethernet or to the same management VLAN and browse to `https://192.168.0.1` (factory default IP for SP-A management port).
2. Log in with default credentials: `admin` / `Password123#` — these are printed on the array's service tag. Change them immediately.
3. The **Initial Configuration Wizard** launches automatically on first login. Work through each page:
   - **DNS:** Enter your DNS server IP addresses.
   - **NTP:** Enter the NTP server address. Unity XT requires accurate time for replication and LDAP.
   - **SMTP:** Enter email relay server for alert notifications.
   - **Licenses:** Upload the `.lic` file provided by Dell. Without a valid license, capacity is limited to evaluation mode.
4. Accept the EULA and click **Finish**. Unisphere will reinitialize and redirect to the dashboard.
5. Change the admin password under **Settings > Users and Groups > admin > Change Password**.

---

## Configure Network Interfaces

After the wizard completes, configure data-path network interfaces.

**iSCSI interfaces:**

1. Navigate to **Settings > Network > iSCSI Interfaces**.
2. Click **Create** and fill in:
   - SP: SP-A
   - Port: ethernet port (e.g., `eth0`)
   - IP address / subnet mask / gateway
   - VLAN tag (if applicable)
3. Repeat for SP-B on the corresponding port. Ensure SP-A and SP-B iSCSI IPs are on the same subnet but different ports for multipath.

**FC interfaces:**

1. Navigate to **Settings > FC Initiators**.
2. FC ports appear automatically after cabling. Confirm all ports show **Link Up** status.
3. Note the WWPNs for each SP — these will be used in SAN zoning.

**NFS/SMB management interface (NAS):**

1. Navigate to **Settings > Network > File Interfaces**.
2. Create a NAS server interface with the NFS/SMB VIP and associate it with the NAS pool (created in the next step).

---

## Create Storage Pools

Unity XT uses storage pools that contain tiers (SSD, SAS, NL-SAS). All LUNs and file systems are provisioned from pools.

1. Navigate to **Storage > Pools > Create**.
2. Enter a pool name (e.g., `Pool_SSD`).
3. Choose pool type:
   - **All Flash** — all drives are SSD/NVMe
   - **Hybrid** — mix of SSD and spinning disk with auto-tiering
4. Add disk groups to the pool. Select the drives detected from the chassis and expansion shelves.
5. Set RAID type per disk group:
   - RAID-5 (4+1) or RAID-6 (6+2) for flash
   - RAID-6 (6+2) recommended for NL-SAS
6. Set pool alert threshold (e.g., alert when pool reaches 80% used).
7. Click **Create**. Pool initialization runs in the background and takes a few minutes.

Verify pool status:

```bash
uemcli /stor/config/pool show -detail
```

---

## Configure iSCSI or FC Host Access

**iSCSI initiator registration:**

1. On the host, note the iSCSI initiator IQN:

```bash
cat /etc/iscsi/initiatorname.iscsi
```

2. In Unisphere, navigate to **Hosts > Create Host**.
3. Enter the host name and select **iSCSI** as the initiator type.
4. Add the host's IQN to the host object.
5. Set the host operating system type (Linux, Windows, VMware ESXi, etc.) — this sets the correct host I/O profile.

**FC initiator registration:**

1. Zone the host HBA ports to the Unity FC ports in the SAN fabric (single-initiator/single-target zones).
2. In Unisphere, navigate to **Hosts > Create Host**.
3. Select **Fibre Channel** as initiator type.
4. The host's logged-in WWPNs should appear in the discovery list — add them.

---

## Create First LUN or File System

**Block LUN:**

1. Navigate to **Storage > Block Storage > LUNs > Create**.
2. Enter a LUN name, select the pool, and set the size.
3. Set **Host access**: click **Add** and select the host created above.
4. Set the **LUN type** (thin is default). Click **Create**.
5. The LUN is immediately presented to the host. On a Linux host, rescan:

```bash
rescan-scsi-bus.sh
multipath -ll
```

**NFS File System:**

1. Navigate to **Storage > File Storage > File Systems > Create**.
2. Enter a name, select a NAS server, and set the size.
3. Create an NFS export under the file system with appropriate host access controls.
4. Mount from the host:

```bash
mount -t nfs <NAS_VIP>:/export/fs01 /mnt/unity_nfs
```

---

## Validate

**Check array health:**

1. Unisphere dashboard should show all components green. Navigate to **System > Hardware** and verify all SP, disk, and PSU LEDs match physical status.
2. Run the built-in health check:

```bash
uemcli /sys/time show
uemcli /sys/health show
```

**Verify LUN path count from host:**

```bash
multipath -ll
# Each LUN should show 4 active paths (2 per SP) for dual-fabric iSCSI or FC
```

**Confirm pool statistics:**

1. Navigate to **Performance > Storage Pools** and verify I/O latency is normal (sub-1ms for SSD pools under light load).
2. Confirm no alerts are active in **System > Alerts**.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window
