---
tags:
  - deployment
  - vxrail
---
# VxRail — Initial Deployment

Dell VxRail is a hyperconverged infrastructure (HCI) appliance that ships as a pre-racked, pre-validated set of nodes combining compute, storage (vSAN), and networking in a single Dell-engineered and Dell-supported stack. The First Run Wizard automates cluster formation, vCenter deployment, and vSAN configuration. This page covers a greenfield deployment from physical rack to a fully validated, support-registered VxRail cluster.

---

## Prerequisites

**Hardware:**

- Dell-supplied VxRail nodes from the Dell Hardware Compatibility List (HCL) — do not mix non-VxRail nodes into a VxRail cluster
- Minimum node count: 3 nodes for standard vSAN (FTT=1); 4 nodes for FTT=2 (recommended for production)
- 25GbE top-of-rack (ToR) switches with LACP support (Dell PowerSwitch S-series recommended for VxRail BOM)
- Rack units and PDU power verified — confirm each node's dual PSU power draw against PDU capacity

**Network (must be configured before First Run):**

| VLAN | Purpose | MTU |
|---|---|---|
| Management | iDRAC, ESXi management, vCenter, VxRail Manager | 1500 |
| vSAN | vSAN storage traffic | 9000 |
| vMotion | Live migration | 9000 |
| NSX TEP (if NSX) | Geneve tunnel encapsulation | 9000 |

- Static IP assignments planned for: iDRAC (per node), ESXi management (per node), vCenter, VxRail Manager, NSX Manager (if applicable)
- DNS A records and PTR records created for all FQDNs before starting First Run
- NTP source reachable from the management VLAN

**Licences:**

- vSphere Enterprise Plus or vSphere Foundation licence keys
- vSAN licence key (if not using vSAN ESA bundled licence)
- NSX licence key (if deploying NSX)
- VxRail support contract active in the Dell support portal (required for Phone Home / automated support)

---

## Cable and Power On Nodes

1. Rack nodes in sequence — label iDRAC ports and data NIC ports on each node during racking (reference the VxRail Network Planning Guide for your node model).
2. Connect **iDRAC** ports to the out-of-band management switch (dedicated OOB network, not the ToR data switch).
3. Connect **data NICs** to ToR switches:
   - Port 1 on each NIC → ToR switch A
   - Port 2 on each NIC → ToR switch B
   - This gives redundant uplinks for all traffic (management, vSAN, vMotion) via bonding/LACP
4. Connect power cables → power on nodes.
5. Verify iDRAC accessible for each node:
   - Open browser to each iDRAC IP → confirm iDRAC web UI loads
   - Verify no hardware alerts in iDRAC → **Dashboard → System Health → all green**
6. Confirm all nodes complete POST with no error codes on the front-panel LCD.

---

## Configure Network Prerequisites

Network configuration must be completed on the ToR switches before launching the VxRail First Run Wizard. First Run will fail or produce incorrect results if VLANs are not in place.

1. Log in to ToR switch A and switch B.
2. Create all required VLANs (management, vSAN, vMotion, NSX TEP if applicable) on both switches.
3. Configure uplink ports to the nodes as **trunk ports** (802.1Q tagged) carrying all required VLANs:

```text
   interface ethernet 1/1/1
     description VxRail-Node1-NIC1
     switchport mode trunk
     switchport trunk allowed vlan 100,200,300,400
     spanning-tree portfast
   ```

4. Configure MTU 9000 (jumbo frames) on all ports carrying vSAN and vMotion VLANs — this must be end-to-end across both switches and all uplinks.
5. Verify switch-to-switch inter-link (ISL) carries all VLANs and MTU 9000.
6. Validate LACP if using port-channel / LAG — confirm LACP PDUs negotiating on node uplinks (check switch LACP neighbour table after nodes boot ESXi).

---

## Run VxRail First Run Wizard

The First Run Wizard deploys vCenter, configures vSAN, and forms the cluster automatically. It runs from VxRail Manager embedded in the first node's iDRAC.

1. Open a browser to the iDRAC IP of the **first node** (the node designated as the initial bootstrap node).
2. From iDRAC → **VxRail** tab → launch **VxRail Manager First Run**.
3. Accept the EULA.
4. Enter global cluster settings:
   - Cluster name
   - vCenter FQDN and IP (VxRail will deploy an embedded vCenter — enter the target FQDN now)
   - SSO domain name and administrator password
   - DNS server IPs
   - NTP server address
5. Enter per-node settings for each discovered node:
   - ESXi management IP and hostname (FQDN)
   - iDRAC IP (pre-populated if DHCP assigned — override with static)
6. Enter VxRail Manager IP and FQDN.
7. Enter VLAN IDs for management, vSAN, vMotion (and NSX TEP if applicable).
8. Review the summary page — verify all IPs, FQDNs, and VLANs before proceeding. Errors here require re-running First Run.
9. Click **Start Deployment** and monitor progress. Full cluster formation typically takes 60–90 minutes.
10. First Run completes → browser redirects to vCenter login page at the configured FQDN.

---

## Configure vSAN Disk Groups

The First Run Wizard automatically claims eligible disks and builds disk groups. Verify and adjust as needed post-deployment.

1. Log in to vCenter → **Cluster → Configure → vSAN → Disk Management**.
2. Confirm all nodes appear with disk groups claimed:
   - Each node should show at least one disk group
   - Disk group composition: 1 cache tier device (NVMe or SSD) + 1–7 capacity tier devices
3. Verify FTT policy is appropriate for your node count:
   - 3 nodes: FTT=1 (RAID-1 mirroring) — tolerates 1 node failure
   - 4+ nodes: FTT=1 or FTT=2 (RAID-5/6 or RAID-1) — review capacity vs. protection trade-off
4. Navigate to **Cluster → Configure → vSAN → Services → Default Storage Policy** → confirm the default policy matches your FTT target.
5. Check vSAN health: **Cluster → Monitor → vSAN → Health** → all checks green.
6. If any disk group shows faulted or missing drives:
   - vCenter → Disk Management → identify the affected node and disk group
   - Check iDRAC → **Storage → Physical Disks** for hardware errors on the specific drive
   - Replace failed drive if hardware fault confirmed, then re-claim disk group

---

## Deploy NSX (if applicable)

If the deployment includes NSX for network virtualisation, VxRail Lifecycle Management (LCM) handles NSX deployment within a VCF-style automated workflow — do not install NSX manually.

1. Log in to **VxRail Manager** (`https://<vxrail-manager-fqdn>`).
2. Navigate to **Lifecycle Management → NSX**.
3. Click **Deploy NSX**.
4. Provide NSX Manager deployment details:
   - NSX Manager FQDN and target IP
   - NSX Manager admin credentials
   - Target cluster and datastore for the NSX Manager appliance
5. VxRail LCM deploys the NSX Manager OVA, waits for it to initialise, and then configures the NSX transport nodes on all VxRail hosts automatically.
6. Monitor progress in VxRail Manager → **LCM → Tasks**.
7. Once complete, verify in NSX Manager UI:
   - **System → Fabric → Nodes → Host Transport Nodes** → all VxRail hosts listed with status **Success**
   - **System → Fabric → Nodes → NSX Manager Cluster** → single or three-node manager cluster healthy

---

## Validate the Cluster

Run a structured validation pass before declaring the cluster production-ready.

**vSAN health (vCenter):**

```text
vCenter → Cluster → Monitor → vSAN → Health
```

All health checks must be green. Pay particular attention to:

- **Network Health:** vSAN vmkernel adapters reachable across all hosts
- **Physical Disk Health:** no faulted or absent disks
- **Performance Service:** vSAN Performance Service enabled and collecting stats

**VxRail Manager inventory:**

```text
VxRail Manager → Inventory → Nodes
```

All nodes must show **Healthy** with no active alerts.

**CLI validation on a VxRail node (SSH to ESXi host):**

```bash
esxcli vsan health cluster list
```

All checks return **GREEN**. Investigate any **YELLOW** or **RED** item before proceeding.

```bash
esxcli vsan storage list
```

Confirm all disk groups and their member disks are visible and healthy.

**Network validation:**

- vCenter → **Cluster → Configure → Networking → VMkernel Adapters** → confirm vmk adapters for management, vSAN, vMotion, and NSX TEP are present on all hosts with correct IPs
- Run a vMotion test: live-migrate a test VM between two nodes → confirm migration completes without error

**Capacity check:**

- vCenter → **Cluster → Monitor → vSAN → Capacity** → confirm usable capacity matches expected value for the disk configuration and FTT policy

---

## Register with VxRail Support

Phone Home (Secure Remote Services / SRS) enables Dell to proactively monitor hardware and automatically create support requests for hardware failures.

1. Log in to **VxRail Manager** → **Support → Phone Home**.
2. Click **Enable Phone Home**.
3. Enter SRS gateway details (or use Dell's cloud SRS endpoint if no on-premises SRS gateway is deployed):
   - SRS gateway IP or hostname
   - Proxy settings if required
4. Enter the primary contact email and site ID from the Dell support contract.
5. Click **Test Connection** → confirm successful outbound connectivity to Dell.
6. **Save** — VxRail Manager now transmits heartbeat and telemetry data to Dell Support.
7. Log in to the Dell support portal (`https://www.dell.com/support`) → **My Products** → confirm the VxRail cluster appears by service tag within 15–30 minutes.
8. Raise a test service request from VxRail Manager → **Support → Create Service Request** → verify SR is created in the Dell support portal and Dell acknowledges receipt.
9. Document the cluster service tags, VxRail Manager URL, vCenter FQDN, and support contract number in the runbook for this deployment.
