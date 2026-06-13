---
tags:
  - deployment
  - pure
---
# Pure Storage — Getting Started

```text
┌──────────────────────────────── Pure Storage — First-Day Orientation ─────────────────────────────────┐
│                                                                                                       │
│  FlashArray (block) — First-Day Steps                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  1. Connect array to management VLAN; identify DHCP IP or connect directly to management port         │
│  2. Browse to https://<array-IP>; log in with credentials from Quick Start guide (inside box)         │
│  3. Complete Initial Setup Wizard: array name, static management IP, DNS, NTP, admin password         │
│  4. Verify hardware health: Storage → Array → all controllers, shelves, drives green                  │
│  5. Create networks: Settings → Network → add data interfaces (iSCSI/FC/NVMe-oF VIFs)                 │
│  6. Provision volumes; register hosts; run first I/O test; register with Pure1 monitoring             │
│                                                                                                       │
│                              │                                 │                                      │
│           FlashArray //X series                       FlashBlade //S or //E series                    │
│           block: iSCSI, FC, NVMe-oF                   NAS: NFS v3/v4.1; object: S3                    │
│                                                                                                       │
│  FlashBlade (NAS/object) — First-Day Steps                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  1. Rack 4U chassis; connect OOB management switch to chassis management module (dual ports)          │
│  2. Browse to chassis management IP; complete setup wizard: array name, IP, NTP, DNS                  │
│  3. Create data VIFs: System → Network → VIFs; assign 100GbE data port IPs per blade                  │
│  4. Create file systems (NFS) or object store buckets (S3); assign capacity and protocols             │
│  5. Mount NFS export or configure S3 endpoint on clients; run first read/write test                   │
│  6. Enable replication if DR is required (ActiveDR for block, native replication for NAS/object)      │
│                                                                                                       │
│  Shared Operational Baseline                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Register both arrays in Pure1 (pure1.purestorage.com) for cloud-based health monitoring              │
│  Enable PhoneHome/SupportAssist: Settings → Support → Enable Remote Assistance                        │
│  Record: array serials, management VIPs, data VIF IPs, Pure1 organisation name                        │
│  Set capacity alert thresholds; schedule quarterly firmware review against Pure1 recommendations      │
│                                                                                                       │
│  GLOSSARY                                                                                             │
│  Purity//FA  — firmware running on FlashArray controllers (block array OS)                            │
│  Purity//FB  — firmware running on FlashBlade chassis (NAS/object array OS)                           │
│  VIF         — Virtual Interface; a floating data IP bound to a physical network port                 │
│  Pure1       — cloud-based monitoring and support portal for all Pure arrays                          │
│  ActiveCluster— synchronous replication between two FlashArrays (zero RPO, zero RTO)                  │
│  ActiveDR    — asynchronous replication for FlashArray to a remote site                               │
│  DirectFlash — Pure's NVMe flash modules; proprietary form factor, not commodity SSDs                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This guide provides an orientation to deploying Pure Storage infrastructure, covering FlashArray block storage and FlashBlade NAS/object storage. Each product has its own dedicated deployment guide; this page summarizes the key first-day steps for each.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## FlashArray Initial Config

Pure FlashArray (//X and //C series) runs Purity//FA and is managed through the Purity web interface or the `purefa_info` / REST API.

**Factory arrival and initial access:**

A newly delivered FlashArray arrives with the management interface pre-configured for DHCP. Connect it to your management VLAN and identify its IP from your DHCP server, or connect directly to the management port and access the factory default IP.

1. Browse to `https://<flasharray_ip>` and log in with credentials on the array's Quick Start guide (printed on the inside of the shipping box).
2. Accept the EULA on first login.
3. The **Initial Setup Wizard** launches automatically. Complete:
   - Array name
   - Management IP (static), subnet mask, gateway
   - DNS servers
   - NTP servers
   - Admin password
4. Click **Finish**. The array reboots to apply the new management IP.

**Verify array health:**

After the reboot, log back in at the new management IP and confirm:

- All hardware components show green in **Storage > Array** view
- All controllers, shelves, and drives are recognized
- No alerts shown in the **Alerts** panel

**Configure data network interfaces:**

Navigate to **Storage > Ports** and configure iSCSI or NVMe-oF ports (or note FC port WWPNs for zoning). See the FlashArray deployment guide for step-by-step port configuration.

For a complete deployment walkthrough see [FlashArray — Initial Deployment](../flasharray/deploy/index.md).

---

## Host Connectivity

FlashArray presents volumes to hosts via iSCSI, Fibre Channel, or NVMe-oF. The key steps across all protocols:

**iSCSI:**

- Configure iSCSI interfaces on the array with static IPs on the iSCSI VLAN
- On the host, discover and log in to the array iSCSI targets
- Register the host on the array using its IQN
- Create a volume and connect it to the host
- Verify multipath shows the correct number of paths

**Fibre Channel:**

- Zone host HBA ports to FlashArray FC target ports (single-initiator/single-target zones)
- On the array, the host registers automatically when its WWPNs log in
- Create a volume and connect it to the host
- Verify 4 or 8 paths via multipath

**NVMe-oF:**

- Configure NVMe-oF interfaces on the array (Purity 6.x+)
- On the host, set up the NVMe over Fabrics initiator and discover the array
- Create a volume and connect to the host NQN
- Verify NVMe multipath via `nvme list` and `nvme path -v`

All host types (Linux, Windows, VMware ESXi) require installing the Pure Storage host utilities or vSphere plugin for optimal multipath settings.

---

## Protection Groups

FlashArray uses Protection Groups to manage snapshot and replication schedules for sets of volumes.

**Create a protection group:**

1. Navigate to **Storage > Protection Groups > New Protection Group**.
2. Name the group (e.g., `pg_sql_prod`).
3. Add volumes to the group — all volumes that need crash-consistent snapshots together (e.g., all volumes belonging to one SQL Server).
4. Add a snapshot schedule:
   - Frequency: every 1 hour
   - Retention: keep for 24 hours (local), then replicate and keep for 7 days (on target)
5. If replication is licensed, add a replication target (another FlashArray or Pure Cloud Block Store).
6. Click **Create**.

Verify snapshots are being created:

Navigate to **Storage > Snapshots** and confirm protection group snapshots appear on the configured schedule.

---

## Pure1 Setup

Pure1 is Pure Storage's cloud-based AIOps and monitoring platform. Register your array to gain proactive health monitoring, capacity planning, and support case integration.

1. Navigate to **System > Support** in the Purity UI.
2. Enable **Phone Home** (sends telemetry to Pure1). This requires the array management interface to reach `support.purestorage.com` on TCP 443.
3. Log in to `https://pure1.purestorage.com` with your Pure Storage support portal credentials.
4. The array should appear automatically after Phone Home is enabled (within 15–30 minutes).
5. In Pure1, configure:
   - Alert notification emails under **Account > Notifications**
   - Capacity threshold alerts (e.g., alert when array reaches 80% used)
   - Performance baseline review in the **Analytics** section

---

## FlashBlade Initial Config

FlashBlade (//S and //E series) runs Purity//FB and is managed through the FlashBlade UI or REST API.

**Physical setup:**

FlashBlade chassis ships in a 4U enclosure with blade modules pre-installed. Pure Storage field engineers typically handle initial racking and blade installation for new deployments.

1. Connect chassis management ports to the OOB management switch.
2. Connect data network ports (100GbE) to the front-end data switches.
3. Power on the chassis and wait for all blades to come online (15–20 minutes).

**Initial configuration via CLI:**

SSH to the chassis management IP (provided by DHCP or factory default) and run the setup script:

```bash
ssh pureuser@<flashblade_ip>
purity setup
```

The setup wizard prompts for:

- Array name
- Management IP (static)
- NTP server
- DNS server
- Admin password

**Verify blade health:**

```bash
purehw list
# All blades should show status OK
```

**Configure data network:**

```bash
# Create a data VIF (virtual interface) for NFS/S3 access
purenetwork create vip --name datavip01 --address 192.168.20.100 --gateway 192.168.20.1 --services data-eth
```

For a complete FlashBlade deployment walkthrough see [FlashBlade — Initial Deployment](../flashblade/deploy/index.md).
