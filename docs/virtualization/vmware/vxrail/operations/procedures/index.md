# VxRail — Procedures

<div class="kb-summary">
Operational procedures for VxRail cluster administration. Covers node maintenance mode (with vSAN evacuation), node expansion, disk replacement, and the change readiness and post-change validation checklists required before any VxRail maintenance operation.
</div>

```text
┌──────────────────────────────────────── VxRail — Procedures ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Node maintenance mode: vSAN evacuates objects before ESXi maintenance begins                │   │
│   │   Node expansion: VxRail Plugin discovers new node via iDRAC and installs ESXi automatically  │   │
│   │   Disk replacement: identify failed disk · hot-swap · claim in vSAN · monitor rebalance       │   │
│   │   Change readiness: vSAN green + resync=0 + all nodes online required before any change       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Node Maintenance      │  │       Node Expansion        │  │      Disk Replacement       │   │
│   │   1. vSAN full evacuation   │  │   1. Rack + cable + power   │  │   1. Identify failed disk   │   │
│   │   2. vMotion all VMs off    │  │   2. iDRAC IP configured    │  │   2. Node to maintenance    │   │
│   │   3. Perform hardware work  │  │   3. VxRail Plugin: Add Node│  │   3. Hot-swap the disk      │   │
│   │   4. Exit maintenance mode  │  │   4. Wait for vSAN rebalance│  │   4. Claim disk in vSAN     │   │
│   │   5. Wait for vSAN resync   │  │   5. Post-expansion checks  │  │   5. Monitor rebalance      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dell PowerEdge servers · iDRAC OOB port per node · vSAN NVMe/SSD disk groups · 25GbE NICs            │
│                                                                                                       │
│  Key terms:                                                                                           │
│  Maintenance mode = ESXi state that evacuates VMs via DRS and vSAN data before hardware operations    │
│  vSAN evacuation  = vSAN ensures all data objects have a full copy elsewhere before node enters MM    │
│  DRS              = Distributed Resource Scheduler; migrates VMs to other nodes during maintenance    │
│  Disk group       = vSAN unit of storage: one cache device + one or more capacity devices per node    │
│  Rebalance        = vSAN redistributes objects evenly across nodes after a disk or node is added      │
│  iDRAC            = Integrated Dell Remote Access Controller; used for OOB discovery of new nodes     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Change Readiness Checklist

**Run this checklist before any VxRail maintenance operation** (LCM upgrade, node expansion, disk replacement, network changes).

```bash
# 1. Verify vSAN health is all green
esxcli vsan health cluster get

# 2. Confirm resync bytes = 0 (all objects fully synced)
esxcli vsan debug resync list
```

- [ ] vSAN health is all green — `esxcli vsan health cluster get`
- [ ] vSAN resync bytes = 0 — `esxcli vsan debug resync list`
- [ ] All VxRail nodes Online in VxRail Plugin
- [ ] No active vCenter alarms on cluster or hosts
- [ ] DRS is enabled and set to **Fully Automated**
- [ ] vCenter backup current (VAMI: `https://<vcenter>:5480`)
- [ ] VxRail Manager VM backup current (Veeam or equivalent)
- [ ] Change window approved and application teams notified
- [ ] Support contract active; Dell SupportAssist enabled on the cluster

### Post-Change Validation

- [ ] All VxRail nodes Online in VxRail Plugin
- [ ] vSAN health all green
- [ ] vSAN resync completed (0 bytes remaining)
- [ ] No new vCenter alarms
- [ ] VMs running normally
- [ ] ESXi version matches expected version (if upgrade was performed)
- [ ] iDRAC hardware health: no new faults

---

## Node Maintenance Mode Procedure

VxRail nodes use vSAN as the storage layer. Before entering maintenance mode, vSAN must evacuate all data objects from the node so no data is at risk. This is different from standard vSphere maintenance mode — use the **vSAN-aware** maintenance mode option.

### Step 1 — Confirm Pre-Conditions

```bash
# vSAN must be fully synced before entering maintenance
esxcli vsan debug resync list
# Remaining Bytes must be 0 before proceeding
```

- All VMs must be able to vMotion off the node (DRS Fully Automated)
- Sufficient capacity on remaining nodes to hold evacuated vSAN objects

### Step 2 — Enter Maintenance Mode

In vCenter: right-click the host → **Maintenance Mode → Enter Maintenance Mode**

In the dialog, set the **vSAN data migration** option:

| Option | When to Use |
|---|---|
| **Full data migration** | Recommended for hardware work — evacuates all vSAN objects off the node |
| Ensure accessibility | Faster; keeps one copy accessible but doesn't fully evacuate — use only for short reboots |
| No data migration | Only if you have no vSAN objects on the node (not typical) |

Select **Full data migration** for any hardware work or LCM upgrade.

```powershell
# PowerCLI — enter maintenance mode with full vSAN evacuation
$host = Get-VMHost "vxrail-node-01.example.local"
Set-VMHost -VMHost $host -State Maintenance -VsanDataMigrationMode Full -Confirm:$false
```

### Step 3 — Wait for Maintenance Mode to be Active

vCenter shows the host icon with a wrench (maintenance) indicator. This can take 10–30 minutes depending on the amount of data to evacuate.

```bash
# Monitor evacuation progress
esxcli vsan debug resync list
# Watch for Remaining Bytes to count down to 0
```

### Step 4 — Perform Work

With the node in maintenance mode and VMs migrated off:

- Apply hardware changes, replace failed components, or allow LCM to proceed with upgrade
- iDRAC reboot if needed: `racadm serveraction gracereboot`

### Step 5 — Exit Maintenance Mode

In vCenter: right-click the host → **Maintenance Mode → Exit Maintenance Mode**

```powershell
# PowerCLI — exit maintenance mode
Set-VMHost -VMHost (Get-VMHost "vxrail-node-01.example.local") -State Connected -Confirm:$false
```

### Step 6 — Wait for vSAN Resync

After the node rejoins, vSAN resyncs data back to the node. Do not start another maintenance window until resync completes.

```bash
# Poll resync on any cluster node
esxcli vsan debug resync list
# Proceed only when Remaining Bytes = 0
```

---

## Node Expansion Procedure

Adding a node to a VxRail cluster is orchestrated entirely by VxRail Manager. Manual ESXi installation or manual vSphere cluster addition is not supported.

### Pre-Expansion Requirements

- [ ] New node is racked, cabled, and powered on
- [ ] iDRAC is accessible from the management network and configured with a static IP
- [ ] New node's iDRAC credentials are known (root + password)
- [ ] Node hardware model is compatible with the existing cluster (check Dell VxRail Hardware Compatibility Guide)
- [ ] Available IPs exist in each required network: management, vMotion, vSAN, VM network
- [ ] Existing cluster vSAN health is green and resync = 0

### Step 1 — Verify New Node iDRAC Accessibility

```bash
# Ping the new node iDRAC from the management network
ping <new-node-idrac-ip>

# SSH test
ssh root@<new-node-idrac-ip>
racadm getsysinfo
```

### Step 2 — Initiate Expansion via VxRail Plugin

In vCenter: **Menu → VxRail → Cluster → Add Node**

Follow the wizard:

1. VxRail Manager discovers the new node via iDRAC ping
2. Validate the node hardware is compatible with the cluster (model, disk configuration)
3. Configure network settings for the new node: management IP, vMotion IP, vSAN IP
4. Review and confirm — VxRail Manager installs ESXi and joins the node to the cluster automatically

Or trigger via API:

```bash
curl -sk \
  -X POST \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "hosts": [{
      "idrac": {
        "ip": "10.0.100.25",
        "username": "root",
        "password": "CalvinIdrac1!"
      }
    }]
  }' \
  "https://<vxm-ip>/rest/vxm/v1/cluster/expansion"
```

### Step 3 — Monitor Expansion

Monitor via: **VxRail Plugin → Cluster → Events** or vCenter Tasks panel.

Expansion steps performed by VxRail Manager:

1. iDRAC discovery and hardware validation
2. Network IP assignment
3. ESXi installation via Auto Deploy / cluster profile
4. Node joins vSphere cluster
5. vSAN disk groups claimed on new node
6. vSAN rebalancing begins automatically

### Step 4 — Wait for vSAN Rebalance

After the node joins, vSAN redistributes objects across the now-larger cluster. This is not instantaneous.

```bash
# Monitor rebalance on any existing cluster node
esxcli vsan debug resync list | grep -E "Total|Remaining"
# Proceed with no further changes until Remaining Bytes = 0
```

### Step 5 — Post-Expansion Validation

```powershell
# Confirm new node is visible and version matches cluster
Get-VMHost | Select-Object Name, Version, Build, ConnectionState | Sort-Object Name | Format-Table -AutoSize

# vSAN cluster health
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" | Select-Object OverallHealth

# Confirm new node disk groups are in vSAN
# vCenter → Cluster → Configure → vSAN → Disk Management
```

---

## Disk Replacement Procedure

### Step 1 — Identify the Failed Disk

1. A vCenter alarm fires indicating a vSAN component is **Absent** or **Degraded**
2. Navigate to: **vCenter → Cluster → Monitor → vSAN → Physical Disk**
3. Identify the node and disk position of the failed component
4. Confirm in iDRAC: SSH to the node's iDRAC and check the event log

```bash
# iDRAC event log — look for drive fault events
racadm getsel | tail -30

# Physical disk list from iDRAC
racadm storage get pdisks
```

```bash
# ESXi — identify failed disk in vSAN
esxcli vsan storage list | grep -E "Disk Group UUID|Display Name|In Caching Tier|Is SSD"
```

### Step 2 — Assess vSAN Impact

While the disk is failed, vSAN continues to serve data using remaining copies (if FTT > 0 and data is replicated). Check the number of degraded objects:

```bash
esxcli vsan debug resync list
# Note: resync bytes will show active rebuild activity
```

If vSAN shows **no remaining replicas** for any object (FTT exceeded), treat this as a P1 incident and restore immediately.

### Step 3 — Enter Node Maintenance Mode

Before physically replacing the disk, put the node in maintenance mode using **Full data migration** (see [Node Maintenance Mode](#node-maintenance-mode-procedure) above).

If the disk failure has already caused vSAN to begin rebuilding on other nodes, you may be able to hot-swap without full maintenance mode — consult Dell support for guidance on whether in-place hot-swap is safe in your cluster configuration.

### Step 4 — Hot-Swap the Disk

- Dell PowerEdge nodes support hot-swap of SAS/SATA/NVMe drives with the carrier
- The failed drive's LED will be amber on the front panel
- Physically remove the failed drive and insert the replacement in the same slot
- iDRAC will detect the new drive automatically

```bash
# After insertion, verify iDRAC sees the new disk
racadm storage get pdisks
```

### Step 5 — Exit Maintenance Mode and Claim Disk in vSAN

Exit the node from maintenance mode (see Step 5 of the maintenance mode procedure).

Once the node is back Online, claim the new disk in vSAN:

**vCenter → Cluster → Configure → vSAN → Disk Management → Claim Disk**

Select the new unclaimed disk and add it to the existing disk group (or create a new disk group if the cache disk was also replaced).

### Step 6 — Monitor Rebalance and Rebuild

```bash
# Watch vSAN rebalance after disk claim
esxcli vsan debug resync list
# Wait for Remaining Bytes = 0 before declaring the replacement complete
```

Validate in vCenter: **Cluster → Monitor → vSAN → Health** — all checks should return to green.
