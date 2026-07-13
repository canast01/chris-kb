---
tags:
  - deployment
  - pure
search:
  boost: 1.5
---
# Pure Storage — Getting Started

This guide provides an orientation to deploying Pure Storage infrastructure, covering FlashArray block storage and FlashBlade NAS/object storage. Each product has its own dedicated deployment guide; this page summarizes the key first-day steps for each.

---

```d2
direction: right

plan: "Plan" {shape: oval}
flasharray_initial_config: "FlashArray Initial Config" {shape: rectangle}
host_connectivity: "Host Connectivity" {shape: rectangle}
protection_groups: "Protection Groups" {shape: rectangle}
pure1_setup: "Pure1 Setup" {shape: rectangle}
flashblade_initial_config: "FlashBlade Initial Config" {shape: rectangle}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> flasharray_initial_config
flasharray_initial_config -> host_connectivity
host_connectivity -> protection_groups
protection_groups -> pure1_setup
pure1_setup -> flashblade_initial_config
flashblade_initial_config -> verify
verify -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: Pure Storage PurityFA v6.5 — FlashArray GUI and Management](https://www.youtube.com/watch?v=5S-ry04rc18){ .md-button }
<!-- /video-link -->


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


```text title="Expected output"
The authenticity of host '10.42.18.55 (10.42.18.55)' can't be established.
ECDSA key fingerprint is SHA256:aBcD1EfGhIjKlMnOpQrStUvWxYz2345678901234567.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.42.18.55' (ECDSA) to the known_hosts file.
pureuser@10.42.18.55's password:
Pure Storage FlashBlade Setup Wizard v6.2.1
System Name: flashblade-prod-01
System ID: 8d4c2e1f-9a3b-4c5d-8e7f-1a2b3c4d5e6f
Current Status: Unconfigured
Starting setup process...
Configuration complete. System ready for use.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,password).` | Verify the pureuser account exists on the FlashBlade and the password is correct. |
    | `ssh: Could not resolve hostname <flashblade_ip>: Name or service not known` | Replace `<flashblade_ip>` with the actual management IP address of the FlashBlade system. |
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


```text title="Expected output"
Name                          Status    Model              Serial Number
blade-01                      OK        FlashArray//X70    PUREARRAY001A
blade-02                      OK        FlashArray//X70    PUREARRAY001B
blade-03                      OK        FlashArray//X70    PUREARRAY001C
blade-04                      OK        FlashArray//X70    PUREARRAY001D
blade-05                      OK        FlashArray//X70    PUREARRAY001E
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `purehw: command not found` | Ensure the Pure Hardware CLI tools are installed and the PATH includes the Pure installation directory. |
    | `Error: Unable to connect to management interface` | Verify network connectivity to the array management IP and that SSH credentials are properly configured. |
    | `Status: DEGRADED` | Check blade logs with `purehw logs <blade-name>` and contact Pure support if hardware failure is indicated. |
**Configure data network:**

```bash
# Create a data VIF (virtual interface) for NFS/S3 access
purenetwork create vip --name datavip01 --address 192.168.20.100 --gateway 192.168.20.1 --services data-eth
```


```text title="Expected output"
Virtual Interface created successfully
Name: datavip01
Address: 192.168.20.100
Gateway: 192.168.20.1
Netmask: 255.255.255.0
Services: data-eth
Status: Active
ID: vif-a7f2c9e1-4b8d-11ed-9c42-0242ac120002
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Address 192.168.20.100 already in use` | Verify the IP is not assigned to another interface using `purenetwork list vip` and choose an unused address. |
    | `Error: Invalid service type 'data-eth'` | Replace `data-eth` with a valid service name such as `data`, `nfs`, or `s3` (check available services with `purenetwork list services`). |
For a complete FlashBlade deployment walkthrough see [FlashBlade — Initial Deployment](../flashblade/deploy/index.md).

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

## See also

- [Evergreen](../evergreen/)
- [Evergreen One](../evergreen-one/)
- [Flasharray](../flasharray/)
- [Flashblade](../flashblade/)
- [Operations](../operations/)
- [Pure1](../pure1/)
- [Pure Storage — Overview](../)
