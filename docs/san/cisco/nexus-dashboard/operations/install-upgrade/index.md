# Nexus Dashboard — Install & Upgrade

> Part of the [Nexus Dashboard](../../) reference.

---

## Overview

Nexus Dashboard is deployed as a 3-node or 5-node cluster. This page covers fresh installation (OVA on VMware) and in-place cluster upgrades. Application upgrades (NDFC, NDI) are a separate step performed after the ND platform upgrade.

---

## Pre-Installation Requirements

### Per Node (3-Node Cluster, OVA)

| Requirement | Value |
|---|---|
| Hypervisor | VMware ESXi 7.0+ or 8.x |
| vCPU | 16 (24 for NDFC + NDI) |
| RAM | 64 GB (128 GB for NDFC + NDI) |
| Storage | 500 GB thick provisioned (1 TB for NDFC + NDI) |
| NICs | 3 vNICs on separate port groups (mgmt, data, app) |
| NTP | All 3 nodes must reach the same NTP servers |
| DNS | Forward and reverse DNS for each node's mgmt IP |

### Network Prerequisites

- Management network: routed from client workstations; TCP 443 and SSH 22 reachable
- Data network: routed to switch management IPs and APIC/NDFC-managed fabric
- App/cluster network: L2 adjacency between all nodes (low-latency; < 5ms RTT)

Download the ND OVA from Cisco Software Download Center. Verify SHA-512 checksum before deployment.

---

## Fresh Installation — VMware OVA (3-Node Cluster)

### Step 1: Deploy Three OVAs

Deploy three identical OVA instances. In vCenter for each node:

1. **Actions > Deploy OVF Template**
2. Select the ND OVA file
3. VM name: `nd-dc1-1`, `nd-dc1-2`, `nd-dc1-3`
4. Select datastore with sufficient space (thick provisioning)
5. Map OVA networks to your port groups:
   - `mgmt` → Management VLAN port group
   - `data` → SAN/Fabric data port group
   - `app` → Cluster internal port group
6. On **Customize Template**, set for each node:
   - Management IP / mask / gateway
   - Data IP / mask
   - App IP / mask
   - DNS servers
   - NTP servers
   - Hostname (e.g. `nd-dc1-1.corp.example.com`)
   - Initial admin password
7. Do not power on yet.

### Step 2: Power On and Initialize Cluster

Power on all three nodes. Wait 10 minutes for initial startup.

```bash
# SSH to node 1 (the designated primary)
ssh ndadmin@nd-dc1-1.corp.example.com

# Initialize the cluster from node 1
acs cluster init \
  --name nd-dc1 \
  --primary-ip 10.10.5.21 \
  --node-ips 10.10.5.22,10.10.5.23 \
  --app-ips 192.168.100.1,192.168.100.2,192.168.100.3

# Monitor cluster formation (takes 10-20 minutes)
acs health
# Wait until all nodes show Healthy
```

### Step 3: Access the UI and Initial Configuration

Open a browser to `https://nd-dc1-1.corp.example.com` (or the cluster VIP once configured) and log in as `admin`.

**Initial configuration checklist:**

1. **Admin Console > System > NTP** — verify NTP is synchronized on all nodes
2. **Admin Console > Security > Certificates** — replace the default self-signed certificate with a corporate CA certificate
3. **Admin Console > Security > Authentication** — configure LDAP or TACACS+
4. **Admin Console > Operations > Backup** — configure backup schedule and remote target
5. **Admin Console > Infrastructure > Cluster Configuration** — confirm all three nodes are healthy

### Step 4: Install Applications

Navigate to **Admin Console > Apps** to install NDFC and/or NDI:

1. Click **Install App**
2. Upload the NDFC or NDI application image (`.tar.gz`)
3. Click **Install** and wait for deployment (5-10 minutes per app)
4. After installation, the app appears in the ND left navigation

For NDFC SAN deployment:
- Select persona: **SAN Controller**
- Configure seed switches for fabric discovery after installation

---

## In-Place Upgrade

### Pre-Upgrade Checklist

- [ ] Review ND Release Notes and compatibility matrix for the target version
- [ ] Confirm target ND version is compatible with currently installed app versions (NDFC, NDI)
- [ ] Take a full ND cluster backup: **Admin Console > Operations > Backup > Backup Now**
- [ ] Take VM snapshots of all three cluster nodes in vCenter
- [ ] Export NDFC zone databases for all fabrics
- [ ] Confirm no critical NDFC alarms are active
- [ ] Confirm all ND cluster nodes are healthy: `acs health`
- [ ] Schedule a maintenance window (ND UI unavailable for 30-60 minutes during upgrade)
- [ ] Notify stakeholders

### Upgrade Procedure

#### Option A: GUI Upgrade

1. Navigate to **Admin Console > System > Software Update**.
2. Click **Upload** and select the ND upgrade image (`.iso` or upgrade bundle).
3. Click **Upgrade**. The cluster upgrades nodes sequentially (rolling upgrade).
4. During the upgrade, the UI may be intermittently unavailable.
5. After completion, verify: **Admin Console > System > About** — shows new platform version.

#### Option B: CLI Upgrade

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Transfer upgrade image to the cluster
acs upgrade upload /path/to/aci-nd-dk9.3.1.1.ova

# Start the upgrade
acs upgrade start --version 3.1.1

# Monitor upgrade progress
acs upgrade status
# Shows progress per node (each node is upgraded sequentially)

# After completion:
acs health
# All nodes should return to Healthy
```

### Post-Upgrade Validation

```bash
# Verify cluster health
acs health

# Verify all nodes at new version
acs nodes list | grep version

# Verify all apps are Running
acs apps status

# Verify NDFC fabric connectivity
# UI: NDFC > Fabrics — all switches should reconnect within 5 minutes

# Verify NDI telemetry resumed (if installed)
# UI: NDI > Dashboard — anomaly data should appear within 15 minutes
```

After a 48-hour validation window with no issues: delete the VM snapshots taken before the upgrade.

---

## Upgrade Applications (NDFC, NDI)

After the ND platform upgrade is confirmed healthy, upgrade installed applications:

1. Navigate to **Admin Console > Apps**.
2. Select the application (NDFC or NDI).
3. Click **Upgrade**.
4. Upload the new application image.
5. Click **Start Upgrade**. The application is briefly unavailable during the upgrade.
6. After upgrade: confirm app version and validate core functionality.

Upgrade NDFC before NDI. Validate NDFC functionality (fabric discovery, zone operations) before proceeding to NDI upgrade.

---

## Rollback

If a ND platform upgrade causes a cluster-breaking issue:

1. Power off all three ND VMs in vCenter.
2. Revert all three VMs to the pre-upgrade snapshot simultaneously.
3. Power on all three VMs.
4. Verify cluster reforms: `acs health` (takes 5-10 minutes).
5. Confirm NDFC and NDI are running.

**Note:** Snapshot revert restores the full VM state including the database. Any zone changes made after the snapshot (before rollback) will be lost. Ensure pre-upgrade zone exports are available to re-apply if needed.

---

## Adding a Node to an Existing Cluster

To scale a 3-node cluster to 5 nodes:

```bash
# Deploy two additional OVA nodes as per Step 1 above
# Configure their IPs but do not initialize them

# From the primary node, add the new nodes
acs cluster add-node --node-ip 10.10.5.24 --app-ip 192.168.100.4
acs cluster add-node --node-ip 10.10.5.25 --app-ip 192.168.100.5

# Monitor cluster expansion (takes 20-40 minutes)
acs health
acs nodes list
```

---

## Decommission

To decommission a Nexus Dashboard cluster:

1. Export all NDFC zone databases and device alias databases.
2. Take a final full backup.
3. Remove all registered sites and managed fabrics from NDFC to clean up switch-side references:
   - Remove NDFC service accounts from managed switches
   - Remove NDFC as SNMP trap destination on managed switches
4. Power off all three ND cluster VMs.
5. Delete VMs from vCenter.
6. Remove DNS entries.
