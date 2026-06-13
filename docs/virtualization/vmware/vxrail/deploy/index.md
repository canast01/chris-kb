---
tags:
  - deployment
  - vmware
  - vxrail
search:
  boost: 1.5
---
# VxRail — Deploy

<div class="kb-summary">
End-to-end deployment guide for a new VxRail cluster. Covers pre-deployment readiness, the First Run Wizard, vCenter integration, vSAN validation, OMIVV plugin setup, and Day 1 post-deployment hardening.

*Applies to: VxRail 7.x / 8.x*
</div>

```text
┌─────────────────────────────────── VxRail Cluster Deployment Flow ────────────────────────────────────┐
│                                                                                                       │
│  Phase 1: Physical Readiness                                                                          │
│  Rack + cable nodes  ·  iDRAC IP on each node  ·  DNS A+PTR for all FQDNs  ·  NTP reachable           │
│  Switch VLANs (mgmt/vMotion/vSAN/VM)  ·  MTU 9000 on vSAN + vMotion ports                             │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 2: First Run Wizard                                                                            │
│  Browser to node1 mgmt IP  ·  enter network config  ·  choose vCenter type                            │
│  VxRail Manager VM deploys automatically on node 1  ·  embedded vCenter deploys                       │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 3: vSAN Configuration                                                                          │
│  VxRail Manager claims disks  ·  assigns cache+capacity tiers  ·  health checks green                 │
│  Create SPBM policy RAID-1 FTT=1  ·  verify ESA vs OSA architecture                                   │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 4: Network Validation                                                                          │
│  Verify vmk0/vmk1/vmk2 on all nodes  ·  MTU vmkping test  ·  OMIVV plugin visible                     │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 5: SupportAssist and OMIVV                                                                     │
│  Install OMIVV plugin  ·  enable SupportAssist in VxRail Plugin  ·  configure Dell Connect            │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 6: Post-Deploy Hardening and Baseline                                                          │
│  Change mystic + iDRAC passwords  ·  lockdown mode on  ·  VAMI backup  ·  LCM baseline                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1: Physical Readiness

VxRail nodes ship pre-racked or are racked on-site. Before running the First Run Wizard every prerequisite below must pass — the wizard does not retry failed DNS or NTP lookups gracefully.

**Racking and cabling**

- Follow the Dell VxRail Network Planning Guide for your appliance model (E/P/V/S series)
- Each node needs: 2 × 25GbE (or 100GbE) data NICs to ToR switches + 1 × dedicated iDRAC port
- Dual switch uplinks required for HA — active/standby or LACP (VxRail supports both)
- iDRAC port on a dedicated OOB management VLAN or shared management VLAN (separate from vmk0)

**iDRAC IP assignment per node (DCUI)**

On each node, at the physical console (or iDRAC front-panel LCD):

```text
iDRAC Settings (F2 at POST or iDRAC front panel)
  → Network Settings
    → Static IP: <idrac-ip>
    → Subnet: <mask>
    → Gateway: <gateway>
    → DNS: <dns-server>
```

Verify iDRAC is reachable before proceeding:

```bash
# From jump host on OOB management VLAN
ping -c 3 <node1-idrac-ip>
ping -c 3 <node2-idrac-ip>
ping -c 3 <node3-idrac-ip>
```

**DNS pre-creation**

Create A and PTR records for ALL of the following FQDNs before starting the wizard. Missing DNS records cause wizard failure or post-deploy vCenter join errors.

| Record | Example FQDN | Type |
|---|---|---|
| VxRail Manager | vxrail-manager.example.local | A + PTR |
| vCenter (embedded) | vcenter.example.local | A + PTR |
| Node 01 | vxrail-node-01.example.local | A + PTR |
| Node 02 | vxrail-node-02.example.local | A + PTR |
| Node 03 | vxrail-node-03.example.local | A + PTR |

```bash
# Verify DNS resolves forward and reverse before wizard
nslookup vxrail-manager.example.local
nslookup node-01.example.local

# Verify reverse lookup for vCenter IP
nslookup 10.0.1.20
```

**NTP reachability**

```bash
# From jump host on management VLAN — NTP must be reachable from this VLAN
ntpdate -q ntp1.example.local
ntpdate -q ntp2.example.local
```

**Switch VLAN and MTU configuration**

| Network | VLAN ID | MTU | Notes |
|---|---|---|---|
| Management | 100 | 1500 | vmk0; iDRAC OOB may share or use dedicated VLAN |
| vMotion | 101 | 9000 | vmk1; jumbo frames required |
| vSAN | 102 | 9000 | vmk2; jumbo frames required — verify on both switch ports |
| VM traffic | 200–299 | 1500 | VM port groups; trunk on host uplinks |

Verify MTU is set to 9000 on all switch ports carrying vSAN and vMotion traffic before the wizard runs. Mismatched MTU causes vSAN build failures that are difficult to diagnose post-deploy.

**Exit criterion:** All nodes iDRAC reachable. All FQDNs resolve forward and reverse. NTP reachable. Switch VLANs and MTU confirmed by network team.

---

## Phase 2: First Run Wizard

The First Run Wizard is a browser-based workflow that runs before vCenter exists. It discovers nodes, collects network configuration, deploys VxRail Manager, and (for embedded deployments) deploys the vCenter VCSA — all automatically.

**Access the wizard**

```bash
# Navigate from a browser on the management VLAN
# The wizard is served from the VxRail bootstrap agent on node 1
https://<node1-management-ip>/
```

Accept the self-signed certificate warning. Default credentials at first access: no login required — the wizard prompts for all passwords as part of setup.

**Wizard input sequence**

| Step | Input | Notes |
|---|---|---|
| 1. Welcome | Accept EULA | Review Dell and VMware license agreements |
| 2. Network discovery | Auto-discovers all nodes on management VLAN | Confirm all expected nodes are listed |
| 3. Node network config | Management, vMotion, vSAN IPs per node | Enter static IPs for all VMkernel ports |
| 4. DNS / NTP | VxRail Manager FQDN, DNS servers, NTP servers | Must match pre-created DNS records exactly |
| 5. vCenter type | Embedded or External | See table below |
| 6. SSO domain | e.g. `vsphere.local` | Cannot be changed post-deploy without full reinstall |
| 7. Passwords | vCenter admin, SSO admin, VxRail Manager mystic | Document securely — not recoverable without reset |
| 8. Review + Deploy | Summary screen | Wizard runs 30–60 min unattended |

**Embedded vs External vCenter**

| Factor | Embedded | External |
|---|---|---|
| vCenter location | Deployed inside the VxRail cluster automatically | Pre-existing vCenter you provide FQDN for |
| Use case | Single-cluster or small deployments | Multi-cluster, multi-site, existing vCenter infrastructure |
| Recovery complexity | Higher — vCenter VM is on vSAN it manages | Lower — vCenter is independent of this cluster |
| Supported from | All VxRail versions | VxRail 4.7+ |

**Wizard deploys automatically:**
- VxRail Manager VM on node 1 (4 vCPU, 12 GB RAM, 60 GB disk minimum)
- Embedded vCenter VCSA (if selected)
- Configures all VMkernel ports on all nodes
- Creates the vSphere cluster object with DRS + HA enabled

**Exit criterion:** Wizard completes without errors. VxRail Manager UI accessible at `https://<vxm-ip>`. vCenter accessible at `https://<vcenter-fqdn>`.

---

## Phase 3: vSAN Configuration

VxRail Manager automatically claims disks and configures vSAN during and after the First Run Wizard. Manual disk claiming is not required or recommended on VxRail — the wizard handles it.

**OSA vs ESA architecture**

| Architecture | Cache tier | Capacity tier | Minimum VxRail |
|---|---|---|---|
| OSA (Original Storage Architecture) | NVMe or SSD (10–20% of total) | SSD or HDD | All versions |
| ESA (Express Storage Architecture) | None — single tier | NVMe only | VxRail 8.0+ |

OSA creates disk groups (1 cache device + 1–7 capacity devices per node). ESA uses all NVMe as a single pool with no explicit cache assignment.

**Verify vSAN health post-deploy**

```bash
# From any ESXi node SSH session
esxcli vsan health cluster get

# Summary view — check for any red or yellow items
esxcli vsan health summary get
```

**Create production SPBM policy**

The default vSAN storage policy (FTT=0) provides no redundancy. Always create and apply a production policy before placing any workload VMs.

In vCenter: Policies and Profiles → VM Storage Policies → Create:
- Name: `VxRail-RAID1-FTT1`
- Failures to tolerate: 1
- RAID method: RAID-1 (Mirroring)
- Apply to: VxRail Manager VM, vCenter VM, and all production VMs

**Verify vSAN health via PowerCLI**

```powershell
Connect-VIServer vcenter.example.local
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" | Select-Object OverallHealth
```

Expected output: `green`

**Check VxRail Manager version and cluster status**

```bash
curl -sk -u 'mystic:password' https://<vxm-ip>/rest/vxm/v1/system | python3 -m json.tool
```

**Exit criterion:** vSAN health all green. VxRail Manager reports cluster healthy. Production SPBM policy created and applied to VxRail Manager and vCenter VMs.

---

## Phase 4: Network Validation

VxRail Manager configures VMkernel ports automatically, but you must validate that all ports are present and functioning on every node after the wizard completes.

**Expected VMkernel ports per node**

| VMkernel | Traffic type | VLAN | MTU | Service tag |
|---|---|---|---|---|
| vmk0 | Management | Management VLAN | 1500 | Management |
| vmk1 | vMotion | vMotion VLAN | 9000 | vMotion |
| vmk2 | vSAN | vSAN VLAN | 9000 | vSAN |

**Verify VMkernel ports on all nodes via PowerCLI**

```powershell
Connect-VIServer vcenter.example.local
Get-VMHost -Location (Get-Cluster "VxRail-Cluster") | Select-Object Name, ConnectionState
```

Expected output: all nodes `Connected`.

**Verify all VMkernel IPs from a specific host**

```bash
# SSH to any VxRail node
esxcli network ip interface list
esxcli network ip interface ipv4 get
```

**MTU test on vSAN network**

Run from each node to each peer node vSAN VMkernel IP. All tests must succeed (0% packet loss) before the cluster is considered production-ready.

```bash
# SSH to node 1 — test vSAN MTU to node 2 vSAN VMkernel IP
# 8972 = 9000 MTU minus 28 bytes IP+ICMP header
vmkping -I vmk2 -d -s 8972 <node2-vsan-vmk-ip>

# Repeat for all node pairs
vmkping -I vmk2 -d -s 8972 <node3-vsan-vmk-ip>
```

**Verify OMIVV plugin in vCenter**

After wizard: vCenter → Menu → OpenManage Integration for VMware vCenter should appear. If the plugin is not present, see Phase 5 for manual installation.

**Exit criterion:** All nodes connected in vCenter. vmk0/vmk1/vmk2 present and correct on all nodes. MTU tests pass across all node pairs. OMIVV plugin visible in vCenter menu.

---

## Phase 5: SupportAssist and OMIVV

OMIVV (OpenManage Integration for VMware vCenter) surfaces Dell hardware alerts, firmware inventory, and warranty data directly in vCenter. SupportAssist enables Dell cloud-based proactive diagnostics. Both should be enabled before the cluster goes to production.

**Install OMIVV plugin (if not auto-installed)**

The OMIVV OVA is available from the Dell support portal. Deploy via vCenter:

1. vCenter → Deploy OVF Template → provide OMIVV OVA path
2. Configure OMIVV appliance: IP, hostname, admin password
3. After deploy: navigate to `https://<omivv-ip>` → register with vCenter
4. In vCenter → Menu → OpenManage Integration → Configure → Add vCenter connection

**Enable SupportAssist via VxRail Plugin**

1. vCenter → Menu → VxRail → Support → SupportAssist
2. Enable SupportAssist → enter Dell support account credentials (or create account)
3. Configure contact info and preferred support language
4. Test connection → confirm status shows "Connected"

**Configure Dell Connect (outbound HTTPS only)**

SupportAssist requires outbound HTTPS (port 443) from VxRail Manager to `esrs.emc.com` and `supportassist.emc.com`. No inbound connections are required.

```bash
# Verify outbound connectivity from VxRail Manager VM SSH
curl -sk https://esrs.emc.com
curl -sk https://supportassist.emc.com
```

If a proxy is required, configure it in VxRail Manager: Settings → Network → Proxy.

**Verify hardware monitoring**

In vCenter → Menu → OpenManage Integration → Hosts and Clusters: all nodes should show hardware health green with firmware inventory populated.

**Exit criterion:** OMIVV shows all nodes with green hardware health. SupportAssist shows Connected status. Dell hardware alerts are visible in vCenter alarms.

---

## Phase 6: Post-Deploy Hardening and Baseline

**Change VxRail Manager mystic password**

The `mystic` account is the local service account for VxRail Manager REST API and CLI access. Change the default password immediately after deployment.

In VxRail Manager UI: Settings → System → Change Password (mystic account)

Or via REST API:

```bash
curl -sk -X PUT -u 'mystic:currentpassword' \
  -H "Content-Type: application/json" \
  -d '{"password":"<NewPassword>"}' \
  https://<vxm-ip>/rest/vxm/v1/system/credentials/mystic
```

**Change iDRAC default passwords on all nodes**

Default iDRAC credentials (root / Calvin) must be changed on every node. Do this via RACADM from each node's ESXi SSH session or from a jump host with RACADM installed.

```bash
# Change iDRAC root password via RACADM (run on each node or via iDRAC IP remotely)
racadm set idrac.users.2.password <NewPassword>

# Verify the change took effect
racadm get idrac.users.2.username
```

Alternatively use the iDRAC web UI: iDRAC Settings → User Authentication → Local Users → root → Change Password.

**Enable lockdown mode on all hosts**

```powershell
# Enable normal lockdown on all VxRail nodes via PowerCLI
Connect-VIServer vcenter.example.local
foreach ($h in Get-VMHost -Location (Get-Cluster "VxRail-Cluster")) {
    $view = Get-View $h
    $view.EnterLockdownMode()
    Write-Host "$($h.Name) lockdown enabled"
}
```

**Configure vCenter VAMI file-based backup**

vCenter VCSA (for embedded deployments) should be backed up via the VAMI backup facility.

1. Navigate to `https://<vcenter-fqdn>:5480` → Backup → Configure
2. Backup location: SFTP or FTPS target (not on the vSAN datastore the VCSA manages)
3. Schedule: daily, retain 3 copies minimum
4. Encryption password: set and document securely

**Configure LCM upgrade baseline**

1. vCenter → Menu → Lifecycle Manager → Baselines
2. Create a VxRail-aware upgrade baseline (VxRail Manager integrates with LCM for coordinated upgrades)
3. VxRail upgrades must go through VxRail Manager → not directly through LCM baselines
4. In VxRail Manager UI: LCM → Upload Bundle → initiate from VxRail Manager, not vCenter LCM directly

**Take VxRail Manager VM backup**

```powershell
# Snapshot VxRail Manager VM as a baseline post-deploy snapshot
Connect-VIServer vcenter.example.local
$vm = Get-VM "VxRail-Manager"
New-Snapshot -VM $vm -Name "Post-Deploy-Baseline" -Description "Clean post-deploy state before production use"
```

Also integrate VxRail Manager VM into any existing VM backup solution (Avamar, VBEM, etc.).

**Disable SSH on all ESXi hosts post-hardening**

```bash
# From each ESXi host SSH session
vim-cmd hostsvc/disable_ssh
vim-cmd hostsvc/disable_esx_shell
```

Or via PowerCLI:

```powershell
foreach ($h in Get-VMHost -Location (Get-Cluster "VxRail-Cluster")) {
    Get-VMHostService -VMHost $h | Where-Object {$_.Key -eq "TSM-SSH"} | Stop-VMHostService -Confirm:$false
}
```

**Exit criterion:** All passwords changed. Lockdown mode active on all nodes. SSH disabled. VAMI backup scheduled and tested. VxRail Manager VM snapshot taken.

---

## Post-Deployment Checklist

| Check | Command / Location | Expected |
|---|---|---|
| All nodes connected | vCenter → Hosts and Clusters | Connected |
| vSAN health | `esxcli vsan health cluster get` | All green |
| vSAN MTU test | `vmkping -I vmk2 -d -s 8972 <peer>` | 0% packet loss |
| VMkernel ports present | `esxcli network ip interface list` | vmk0, vmk1, vmk2 on all nodes |
| VxRail Manager accessible | `https://<vxm-ip>` → cluster health | Healthy |
| VxRail Manager version | `curl -sk -u mystic:pw https://<vxm-ip>/rest/vxm/v1/system` | Current release |
| OMIVV hardware health | vCenter → Menu → OpenManage Integration | All nodes green |
| SupportAssist status | vCenter → Menu → VxRail → Support | Connected |
| mystic password changed | VxRail Manager → Settings → Credentials | Non-default |
| iDRAC passwords changed | iDRAC web UI or `racadm get idrac.users.2` | Non-default (not Calvin) |
| Lockdown mode enabled | vCenter → Host → Configure → Security Profile | Normal |
| SSH disabled | vCenter → Host → Configure → Security Profile → Services | Stopped |
| SPBM policy applied | vCenter → Policies and Profiles | RAID-1 FTT=1 on mgmt VMs |
| VAMI backup configured | `https://<vcenter-fqdn>:5480` → Backup | Scheduled, last run success |
| VxRail Manager VM backup | Snapshot or backup job | Post-deploy baseline exists |
| DNS all records resolve | `nslookup <fqdn>` for each component | Forward + reverse match |
| NTP synced on all nodes | `esxcli system ntp get` | NTP enabled, synced |

---

## See also

- [VxRail — How It Works (VMware Platform)](../architecture/how-it-works/)
- [VxRail — Health Checks](../operations/health-checks/)
- [VxRail — Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
