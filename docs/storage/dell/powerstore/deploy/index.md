---
tags:
  - dell
  - deployment
search:
  boost: 1.5
---
# Dell PowerStore — Initial Deployment

```text
┌──────────────────────────────── Dell PowerStore — Deployment Sequence ────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Hardware: 2U rack space (single-node) or 4U (dual-node); dual PDU circuits                           │
│  Network: 25GbE switches for data/iSCSI/NVMe-oF; FC switches if FC is planned                         │
│  IPs reserved: Node A mgmt, Node B mgmt, Cluster VIP, iSCSI data ports per node                       │
│  Software: PowerStore Manager (embedded); license file (.lic) from Dell                               │
│  Confirm NTP server and syslog/SMTP server availability before racking                                │
│                                                                                                       │
│                                        │  rack and cable                                              │
│                                        ▼                                                              │
│  Step 2 · Rack, Cable, and Power On                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Mount appliance using rail kit; cable SAS expansion shelves if ordered                               │
│  Connect management Ethernet from Node A and Node B to OOB management switch                          │
│  Connect 25GbE data ports to data switches; at least two ports per node for LACP bonding              │
│  Connect FC ports to SAN fabric A and B if FC is planned; connect both PSU cables to separate PDUs    │
│  Power on Node A first, then Node B; allow 20 min; status LED turns solid green when ready            │
│                                                                                                       │
│                                        │  run setup wizard                                            │
│                                        ▼                                                              │
│  Step 3 · PowerStore Manager Setup Wizard                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Browse to cluster management VIP; complete initial setup wizard: cluster name, NTP, DNS              │
│  Configure network interfaces: management, iSCSI, NVMe-oF, or FC storage ports                        │
│  Upload license file: Settings → Licensing → Import; verify all licensed features activate            │
│  Set up SMTP/syslog alerting; create local admin account and change default passwords                 │
│                                                                                                       │
│                                        │  provision storage                                           │
│                                        ▼                                                              │
│  Step 4 · Storage Provisioning                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Create storage pools (PowerStore auto-manages underlying RAID via RAID-5/6 based on drive count)     │
│  Create volumes (block), NAS servers and file systems (NAS), or vVols for VMware workloads            │
│  Apply protection policies (snapshots, replication, CloudIQ-based recommendations) per volume         │
│                                                                                                       │
│                                        │  connect hosts                                               │
│                                        ▼                                                              │
│  Step 5 · Host Connectivity                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Register hosts: Storage → Hosts → Add; provide host name, OS type, and initiators (iQN or WWPNs)     │
│  Assign volumes: Hosts → Attach Volume; select volume and access mode (Read/Write)                    │
│  For VMware: configure VASA provider; register PowerStore in vCenter for vVols                        │
│  Rescan host HBAs/iSCSI initiators; confirm volumes appear; format per OS runbook                     │
│                                                                                                       │
│                                        │  validate                                                    │
│                                        ▼                                                              │
│  Step 6 · Validation and Baseline                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Run system health check: Dashboard → Health → All Components green                                   │
│  Record baseline: cluster serial, node serials, pool capacity, volume-to-host mappings                │
│  Enable CloudIQ telemetry via SupportAssist/SCG for proactive health monitoring                       │
│  Schedule capacity alert thresholds (default 80%); document DR replication topology if configured     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This guide covers initial deployment of a Dell PowerStore appliance from physical installation through validated connectivity. Applies to PowerStore T-series (500T, 1000T, 3000T, 5000T, 9000T) running PowerStoreOS 3.x.

---

## Prerequisites

**Hardware:**

- Rack space confirmed (2U for single-node; 4U for dual-node appliance pair)
- Dual PDU circuits — PowerStore uses N+1 redundant power supplies
- 25GbE switches for data and iSCSI/NVMe-oF connectivity
- 16Gb or 32Gb FC switches if FC connectivity is planned
- At minimum two Ethernet links from each node for LACP bonding

**Network planning:**

| Component                | IP            |
|--------------------------|---------------|
| Node A management        | 10.0.0.10     |
| Node B management        | 10.0.0.11     |
| Cluster management VIP   | 10.0.0.12     |
| iSCSI/NVMe data port A   | 10.0.10.20    |
| iSCSI/NVMe data port B   | 10.0.10.21    |

**Software and licenses:**

- Dell PowerStore Manager (embedded, browser-accessible)
- License file (`.lic`) from Dell — covers capacity and optional features (replication, analytics)
- NTP server accessible from the management network
- Syslog or SMTP server for alert forwarding

---

## Rack, Cable, and Power On

1. Mount the PowerStore appliance into the rack using the supplied rail kit. Dual-node configurations require both nodes in adjacent rack units.
2. Cable SAS expansion shelves (if ordered) from the expansion ports on Node A and Node B to the shelf using the factory-labeled SAS cables.
3. Connect management Ethernet from Node A and Node B management ports to the OOB management switch.
4. Connect data network ports (25GbE) to your data switches. Use at least two ports per node for link aggregation.
5. Connect FC ports to your SAN fabric if FC is planned — at minimum two ports per node to separate fabric A and B.
6. Connect both PSU cables per node to separate PDU circuits.
7. Press the power button on Node A first, then Node B. Allow 20 minutes for both nodes to boot and form the cluster. The status LED turns solid green when the appliance is ready.

---

## Run PowerStore Manager Setup Wizard

PowerStore Manager is embedded on the cluster and accessible via browser.

1. From a host on the management network, open a browser and navigate to `https://<Node_A_IP>`.
2. The browser redirects to the **Setup Wizard** on first access.
3. Step through the wizard pages:

   **Network configuration:**
   - Set the cluster management VIP (hosts use this for all management operations after setup).
   - Assign the node management IPs if not already set via DHCP during boot.
   - Set default gateway and DNS servers.

   **Time settings:**
   - Set NTP server address and time zone.

   **License:**
   - Upload the `.lic` file provided by Dell. Click **Validate** to confirm it activates.

   **Naming:**
   - Set the cluster name. This name appears in alerts and replication relationships.

4. Click **Apply** and wait for the cluster to reinitialize (~5 minutes). The wizard redirects to the PowerStore Manager dashboard on completion.
5. Change the default admin password immediately under **Settings > Security > Users**.

---

## Configure Network

After initial setup, configure the data-plane network interfaces used by hosts.

**Configure Ethernet data interfaces:**

1. Navigate to **Settings > Network > Network Settings**.
2. Click on the appliance and select the Ethernet ports designated for iSCSI or NVMe-oF.
3. Set IP addresses, subnet masks, and MTU (9000 for jumbo frames — recommended for iSCSI/NVMe-oF).
4. Apply link aggregation (LACP) if your switch supports it:
   - Select two ports and assign a bond interface.
   - Configure the switch-side port-channel to match.

**Configure VLAN tagging:**

1. Under each port's settings, set the VLAN ID if data traffic is isolated to a specific VLAN.

**Configure FC (if applicable):**

1. FC ports are recognized automatically. Navigate to **Settings > Hardware > Ports** and confirm all FC ports show **Operational**.
2. Note the FC port WWNs — use these for SAN zoning.

---

## Create First Volume

PowerStore uses volumes (block) and file systems (NAS) as primary storage objects, provisioned from a central storage pool per appliance.

**Create a volume:**

1. Navigate to **Storage > Volumes > Create Volume**.
2. Enter a volume name (e.g., `vol_sql01_data`).
3. Set the size (e.g., 500 GiB). PowerStore volumes are thin-provisioned by default.
4. Select the appliance to host the volume.
5. Optionally select a performance tier or policy (if differentiated performance tiers are configured).
6. Click **Create**.

**Verify via CLI (optional):**

```bash
# Using PowerStore CLI (pstcli) from a management host
pstcli --address <cluster_vip> --user admin --password <password> volume query --name vol_sql01_data
```

---

## Configure Host Connectivity

**Register a host:**

1. Navigate to **Compute > Hosts > Add Host**.
2. Enter the host name and select the OS type (Linux, Windows, VMware ESXi).
3. Add initiators:
   - **iSCSI:** Enter the host's IQN (`cat /etc/iscsi/initiatorname.iscsi` on Linux).
   - **FC:** WWPNs appear automatically after zoning is complete.
   - **NVMe-oF:** Enter the host's NQN (`cat /etc/nvme/hostnqn` on Linux).
4. Click **Add**.

**Attach a volume to a host:**

1. Select the volume created above.
2. Click **Attach > Host** and select the host.
3. Assign a logical unit number (LUN) or leave it auto-assigned.
4. Click **Attach**.

The volume is immediately presented. On a Linux host:

```bash
rescan-scsi-bus.sh
lsblk
multipath -ll
```

---

## Set Up Data Protection

**Snapshot policies:**

1. Navigate to **Protection > Protection Policies > Create Policy**.
2. Name the policy (e.g., `hourly_24h`).
3. Add a snapshot rule:
   - Interval: every 1 hour
   - Retention: 24 hours
4. Assign the policy to the volume or file system under **Storage > Volumes > [volume] > Protection**.

**Replication (if licensed):**

1. Navigate to **Protection > Replication Rules > Create**.
2. Set the RPO (e.g., 5 minutes for synchronous, 1 hour for asynchronous).
3. Navigate to **Protection > Remote Systems > Add Remote System** and enter the peer PowerStore cluster VIP and credentials.
4. Create a replication session linking the local volume to a remote volume.
5. Monitor replication state under **Protection > Replication Sessions**.

---

## Validate

1. From the PowerStore Manager dashboard, confirm all nodes, disks, and power supplies show green health indicators under **Infrastructure > Hardware**.
2. Verify the host can see the volume with correct path count:

```bash
multipath -ll
# Expect 2 or 4 paths depending on port and fabric count
```

3. Run a quick I/O test to confirm no errors:

```bash
dd if=/dev/zero of=/dev/mapper/<mpath_dev> bs=1M count=512 oflag=direct
```

4. Check PowerStore Manager **Monitoring > Performance** — latency should be sub-millisecond for NVMe-based appliances at low queue depth.
5. Confirm no active alerts under **Monitoring > Alerts**.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window
