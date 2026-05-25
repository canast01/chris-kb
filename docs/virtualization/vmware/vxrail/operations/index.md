# VxRail — Operations

<div class="kb-summary">
Day-to-day operational reference for VxRail in the VMware product context. Covers plugin health, LCM upgrade sequencing, cluster expansion, and SupportAssist automation.
</div>

```text
┌───────────────────────────────────────── VxRail — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         VxRail plugin daily health checks in vCenter; iDRAC hardware alarms monitoring        │   │
│   │        LCM bundle download and pre-check before upgrade; node-by-node upgrade sequence        │   │
│   │            FW + ESXi upgraded together per node in a single LCM operation per node            │   │
│   │        SupportAssist for proactive case creation on hardware alerts from iDRAC or OMIVV       │   │
│   │   Post-upgrade validation: vSAN health, ESXi version, iDRAC FW, and cluster stability checks  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch drift early · lifecycle upgrades per node · automation scales VxRail management    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │       VxRail plugin UI      │  │        LCM bundle DL        │  │        VxRail Mgr API       │   │
│   │         iDRAC alarms        │  │       Pre-check health      │  │         LCM REST API        │   │
│   │        ESXi connected       │  │       Node-by-node upg      │  │        PowerCLI vSAN        │   │
│   │       vSAN resync chk       │  │       FW+ESXi together      │  │       Dell automation       │   │
│   │          LCM status         │  │      Rebalance post-add     │  │        Ansible VxRail       │   │
│   │        SupportAssist        │  │          Post-check         │  │      SupportAssist API      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch issues early · lifecycle upgrades in sequence · automation handles at-scale changes│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │    VxRail API    │  Plugin: green   │    Daily checks   │  LCM bundle DL   │  Config export   │   │
│   │   LCM REST API   │    iDRAC: ok     │    Maint window   │  Pre-check run   │  vSAN config bk  │   │
│   │  PowerCLI vSAN   │  vSAN: resync=0  │     Node maint    │   Node-by-node   │   iDRAC config   │   │
│   │  Ansible VxRail  │ ESXi: connected  │   Expand cluster  │   Post-upg val   │  Restore redep   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · NVMe/SSD/HDD · 25GbE NICs · iDRAC OOB · ToR switches                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VxRail Manager API  = REST API on VxRail Manager VM; used for LCM jobs, health queries, and config   │
│  LCM bundle          = Signed Dell upgrade package; FW + ESXi + vSAN versions tested and bundled      │
│  Pre-check           = Health validation run before LCM upgrade; blocks if vSAN or network issues     │
│  Node-by-node upgrade = LCM puts one node in maintenance, upgrades FW+ESXi, then moves to next node   │
│  SupportAssist       = Dell proactive support; auto-opens cases on hardware alert from iDRAC or OMIVV │
│  iDRAC               = Integrated Dell Remote Access Controller; hardware health, console, and OOB    │
│  OMIVV               = OpenManage Integration for VMware vCenter; shows Dell hardware alarms in       │
│  vSAN rebalance      = Redistributes vSAN objects evenly after a node is added to the cluster         │
│  Maintenance mode    = ESXi state that evacuates VMs via DRS before hardware or upgrade operations    │
│  FW update           = Firmware update applied to iDRAC, BIOS, NICs, and drives as part of LCM bundle │
│  PowerCLI            = VMware PowerShell module; used for vSAN health checks and cluster automation   │
│  Post-upgrade validation = Checks ESXi version, iDRAC FW, vSAN health, and cluster stability after LCM│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Daily Health Checks

| Check | Location | Expected State |
|---|---|---|
| VxRail cluster health | vCenter → VxRail Plugin → Cluster Summary | All green |
| Node health | vCenter → VxRail Plugin → Hosts | All nodes Online |
| vSAN health | vCenter → Cluster → Monitor → vSAN → Health | All checks green |
| vSAN resync bytes | vCenter → Cluster → Monitor → vSAN → Resyncing | 0 bytes resyncing |
| iDRAC hardware alarms | VxRail Plugin → Hardware → iDRAC | No critical alerts |
| ESXi host connection | vCenter → Hosts and Clusters | All hosts Connected |
| LCM status | VxRail Plugin → LCM | No failed tasks |

```bash
# Quick vSAN health check from ESXi host (SSH)
esxcli vsan health cluster get | grep -v "Green\|green"
esxcli vsan debug resync list | grep -E "Total Bytes|Remaining Bytes"

# Via PowerCLI
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" | Select-Object OverallHealth, Description
```

---

## VxRail Manager Operations

### Access VxRail Plugin

1. Log into vCenter with an account that has the VxRail Plugin role
2. **Menu → VxRail** — the plugin opens in the vCenter UI
3. Navigate: **Cluster**, **Hosts**, **LCM**, **Support**

### Change VxRail Manager Admin Password

```bash
# SSH to VxRail Manager VM (default port 22)
ssh mystic@<vxrail-manager-ip>

# Change the local admin password
passwd mystic
```

Also update the password in:
- vCenter credential store (VxRail Plugin → System → vCenter Credentials)
- Secrets vault / password manager

### VxRail Manager API Authentication

```bash
# All API calls use HTTP Basic Auth with the mystic account
# Generate a base64 credential
echo -n "mystic:password" | base64

# Use in API call
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -H "Content-Type: application/json" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/cluster"
```

---

## VxRail Lifecycle Manager (LCM) Upgrades

The VxRail LCM is the only supported method for upgrading a VxRail cluster. It applies a single bundle that includes:

- ESXi patch or upgrade
- vCenter Server patch or upgrade
- vSAN patch
- Node firmware (BIOS, iDRAC, NIC, HBA, disk controller)
- VxRail Manager update

**Never upgrade ESXi, vCenter, or firmware independently** on VxRail nodes — the LCM tracks bundle versions and will block or fail future upgrades if versions are inconsistent.

### LCM Upgrade Workflow

**Step 1 — Obtain the upgrade bundle**

Download the VxRail Upgrade Bundle from Dell's support site:
`https://www.dell.com/support` → Product Support → VxRail → Drivers & Downloads

The bundle is a large `.bin` file (typically 5–20 GB).

**Step 2 — Upload the bundle**

VxRail Plugin → LCM → Upload Bundle → Browse to the `.bin` file

Or use the VxRail Manager API:

```bash
# Upload via API (multipart)
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -F "file=@/tmp/VxRail-7.0.401-bundle.bin" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/lcm/bundle"
```

**Step 3 — Run pre-upgrade checks**

VxRail Plugin → LCM → Pre-Check

The pre-check validates:
- Cluster health is green
- No active resync in vSAN
- All nodes are reachable
- vCenter is reachable and credentials are valid
- Bundle compatibility with current cluster version

```bash
# Check pre-upgrade status via API
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/lcm/precheck/status"
```

**Step 4 — Run the upgrade**

VxRail Plugin → LCM → Upgrade → Start Upgrade

The LCM upgrades one node at a time:
1. Puts node in maintenance mode (DRS migrates VMs)
2. Applies ESXi and firmware updates
3. Reboots the node
4. Exits maintenance mode
5. Waits for vSAN to resync before proceeding to next node

Total duration: 30–120 minutes per node depending on firmware updates and vSAN resync.

**Step 5 — Monitor progress**

VxRail Plugin → LCM → Upgrade Status

Or via API:

```bash
# Poll LCM upgrade status
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/lcm/upgrade" | python3 -m json.tool
```

**Step 6 — Validate post-upgrade**

```bash
# Verify ESXi version on all nodes
Get-VMHost | Select-Object Name,
    @{N="Version"; E={$_.Version}},
    @{N="Build"; E={$_.Build}} | Sort-Object Name

# Verify vSAN health post-upgrade
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" | Select-Object OverallHealth

# Check VxRail Manager version
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/system" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('VxRail Version:', d.get('version','?'))
print('Build Number:', d.get('build_number','?'))
"
```

### LCM Pre-Upgrade Checklist

- [ ] vSAN health is all green — no warnings or errors
- [ ] vSAN resync bytes = 0 (all objects fully synced)
- [ ] All VxRail nodes Online in VxRail Plugin
- [ ] vCenter and VxRail Manager are reachable and healthy
- [ ] Change window approved; storage and application teams notified
- [ ] VxRail Manager backup taken (snapshot the VxRail Manager VM)
- [ ] vCenter file-based backup current
- [ ] Target bundle compatibility confirmed against Dell compatibility matrix
- [ ] DRS configured to Fully Automated — VMs must migrate automatically during node maintenance

---

## Node Expansion (Add a Node)

Adding a node to a VxRail cluster is managed entirely through VxRail Manager.

### Pre-Expansion Requirements

- New node is racked, cabled, and powered on
- iDRAC is accessible and configured with an IP on the OOB management network
- New node's iDRAC credentials are known
- The new node's hardware model is compatible with the existing cluster (VxRail hardware compatibility applies)
- Cluster has an available IP in each required network (management, vMotion, vSAN, vDS)

### Expansion Procedure

**VxRail Plugin → Cluster → Add Node**

1. VxRail Manager discovers the new node via iDRAC
2. Validate node hardware is compatible
3. Configure network settings for the new node (IPs, VLANs)
4. VxRail Manager installs ESXi on the node using Auto Deploy or the cluster's configuration
5. The node joins the vSphere cluster
6. vSAN incorporates the node's disk groups
7. vSAN rebalances data across the expanded cluster

Monitor via: VxRail Plugin → Cluster → Events

```bash
# API — trigger node expansion
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
  "https://<vxrail-manager-ip>/rest/vxm/v1/cluster/expansion"
```

After expansion, check vSAN rebalancing completes before the next operational change:

```bash
esxcli vsan debug resync list | grep -E "Total|Remaining"
# Wait until Remaining Bytes = 0
```

---

## vSAN Operations

### Check vSAN Cluster Health

```bash
# From any ESXi host in the cluster (SSH)
esxcli vsan health cluster get
esxcli vsan health summary get

# Cluster configuration
esxcli vsan cluster get

# Disk group status per node
esxcli vsan storage list

# Object resync status
esxcli vsan debug resync list

# Network test
esxcli vsan debug network test
```

### Monitor vSAN Capacity

```powershell
# PowerCLI — vSAN datastore capacity
Get-Datastore "vsanDatastore" | Select-Object Name,
    @{N="TotalGB"; E={[Math]::Round($_.CapacityGB)}},
    @{N="FreeGB"; E={[Math]::Round($_.FreeSpaceGB)}},
    @{N="UsedPct"; E={[Math]::Round((1 - $_.FreeSpaceGB/$_.CapacityGB)*100,1)}}
```

Alert at 70% used — vSAN performance degrades as capacity fills and rebalancing becomes more frequent.

### vSAN Disk Group Management

```bash
# List disk groups on a node
esxcli vsan storage list | grep -E "Disk Group UUID|Display Name|Is SSD"

# Add a disk to an existing disk group (via vCenter)
# vCenter → Cluster → Configure → vSAN → Disk Management → Add Disk

# Remove a disk from vSAN (causes vSAN to evacuate data first)
# vCenter → Cluster → Configure → vSAN → Disk Management → Remove Disk
# Wait for evacuation to complete before physically removing
```

### Handle a Disk Failure

1. vCenter alarm triggers indicating a vSAN component is degraded/absent
2. Check which disk failed: **vCenter → Cluster → Monitor → vSAN → Physical Disk**
3. If the disk shows `Absent` or `Degraded`, vSAN automatically rebuilds on remaining capacity
4. Replace the failed disk:
   - Put the node in maintenance mode in vCenter
   - Dell iDRAC or onsite support: hot-swap the failed disk
   - On node exit from maintenance mode, vSAN discovers the new disk
5. Add the replacement disk to vSAN: **vCenter → Cluster → Configure → vSAN → Disk Management → Claim Disk**
6. Monitor rebalancing: `esxcli vsan debug resync list`

---

## Hardware Health and iDRAC Operations

VxRail Manager monitors node hardware through iDRAC polling. Hardware alarms surface in the VxRail Plugin.

### Access iDRAC Directly

```bash
# Each node has a dedicated iDRAC IP (configured during VxRail initial setup)
# Access: https://<idrac-ip>  (default: root / Calvin for factory-fresh nodes — change immediately)
```

### iDRAC Useful Commands (via iDRAC CLI / SSH)

```bash
# SSH to iDRAC
ssh root@<idrac-ip>

# Get system event log (hardware faults)
racadm getsysinfo
racadm getsel | tail -20

# Get NIC and HBA info
racadm nicstatistics -n NIC.Integrated.1-1
racadm storagecontroller get

# Power cycle a node (use carefully)
racadm serveraction powercycle

# Get firmware versions
racadm getversion -f bios
racadm getversion -f idrac
```

### ESXCLI Hardware Health

```bash
# On ESXi host (SSH) — hardware sensors
esxcli hardware sensor list --type Temperature
esxcli hardware sensor list --type Fan
esxcli hardware sensor list --type Power

# Platform info
esxcli hardware platform get

# IPMI event log (SEL)
esxcli hardware ipmi sel list | tail -20
```

---

## Backup and Restore

### VxRail Manager VM Backup

VxRail Manager is a VM — back it up like any other critical VM. Use Veeam or your backup tool to back up the VxRail Manager VM.

Frequency: Daily, retained for 14 days.

Before any LCM upgrade: take a snapshot of the VxRail Manager VM (not a long-term replacement for backup — snapshots degrade vSAN performance if left active).

### ESXi Configuration Export

```bash
# Export ESXi host configuration bundle for each VxRail node
Get-VMHostFirmware -VMHost "vxrail-node-01.example.local" \
  -BackupConfiguration -DestinationPath C:\backups\vxrail\
```

### vCenter File-Based Backup

vCenter should be backed up via the VAMI (port 5480): **Backup → Configure → Schedule**. VxRail deployments with embedded vCenter must back up vCenter through the VAMI — VxRail Manager does not handle vCenter backup.

```yaml
VAMI: https://<vcenter-ip>:5480 → Backup → Configure
Protocol: SFTP
Frequency: Daily
Retain: 14 backups
```

---

## Change Readiness Checklist

Before any VxRail maintenance operation (LCM upgrade, node expansion, disk replacement):

- [ ] vSAN health is all green — `esxcli vsan health cluster get`
- [ ] vSAN resync bytes = 0 — `esxcli vsan debug resync list`
- [ ] All nodes Online in VxRail Plugin
- [ ] No active vCenter alarms on cluster or hosts
- [ ] DRS is enabled and fully automated
- [ ] vCenter backup current (VAMI)
- [ ] VxRail Manager VM backup current (Veeam or snapshot)
- [ ] Change window approved; application teams notified
- [ ] Support contract active; Dell SupportAssist enabled on the cluster

### Post-Change Validation

- [ ] All VxRail nodes Online in VxRail Plugin
- [ ] vSAN health all green
- [ ] vSAN resync completed (0 bytes)
- [ ] No new vCenter alarms
- [ ] VMs running normally
- [ ] ESXi version matches expected post-upgrade version
- [ ] iDRAC hardware health: no new faults
