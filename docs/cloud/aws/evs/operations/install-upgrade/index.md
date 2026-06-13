---
tags:
  - aws
  - operations
---
# Amazon EVS — Lifecycle & Upgrades

<div class="kb-summary">
VCF upgrades via SDDC Manager, ESXi patching lifecycle, NSX-T and HCX upgrade sequence, pre-upgrade checklist, rollback considerations, and EVS host AMI updates managed through AWS.
</div>

```text
┌────────────────────────────────── Amazon EVS — Lifecycle & Upgrades ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   VCF upgrades: SDDC Manager → Lifecycle Management → Bundle download → Sequential upgrade   │    │
│   │   Upgrade order: SDDC Manager → vCenter → NSX-T → ESXi (one host at a time)                │      │
│   │   Each component must be upgraded before the one it manages — skip order = unsupported       │    │
│   │   Rollback is generally not available for NSX-T or ESXi; snapshot management VMs first      │     │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCF LCM      = Lifecycle Manager in VCF; orchestrates all component upgrades via SDDC Manager        │
│  SDDC Manager = Must be upgraded first in every VCF cycle; before vCenter and NSX-T                   │
│  Upgrade bundle = VCF update package downloaded from VMware depot; contains all installers            │
│  Rolling upgrade = ESXi hosts patched one at a time; vSAN evacuates data before each host             │
│  vLCM         = vSphere Lifecycle Manager in vCenter; manages ESXi image and patch compliance         │
│  Remediation  = vLCM action applying an image to a host; automatically enters maintenance mode        │
│  NSX-T upgrade = Manager → Edge nodes → host transport nodes; never skip order                        │
│  HCX upgrade  = EVS side auto-upgrades; on-prem HCX Manager must be manually upgraded                 │
│  EUS          = Extended Update Support; allows version jumps between select VCF releases             │
│  Pre-check    = SDDC Manager automated compatibility validation run before upgrade starts             │
│  VAMI         = vCenter Appliance Management Interface; used for vCenter backup and OS management     │
│  Brownfield   = Existing EVS environment being upgraded; follow supported upgrade path matrix         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## VCF Upgrade Order

The correct upgrade sequence for VCF on EVS is fixed and must not be changed. Each component must be upgraded before the component it manages — if vCenter is on a newer version than SDDC Manager supports, SDDC Manager cannot perform lifecycle operations. If ESXi is upgraded before NSX-T, the NSX-T host transport node may enter a degraded state.

```text
Required upgrade order:

1. SDDC Manager
   — controls all other component upgrades; must be current before proceeding
   — if SDDC Manager upgrade fails, do not proceed with any other component

2. vCenter Server
   — managed by SDDC Manager lifecycle workflows
   — vCenter must be compatible with the target NSX-T version before NSX-T upgrade

3. NSX-T Manager (3-node cluster)
   — upgraded before Edge nodes and host transport nodes
   — NSX-T upgrade is performed rolling: one manager node at a time

4. NSX-T Edge Nodes
   — upgraded after NSX Manager; before ESXi hosts
   — brief data plane interruption during each Edge node upgrade

5. ESXi Hosts (via vSphere Lifecycle Manager)
   — one host at a time; vSAN data evacuated before each host
   — managed via vLCM in vCenter, not SDDC Manager UI
   — ~30-60 min per host; allow time proportional to host count

6. HCX (if deployed)
   — upgrade last; HCX Cloud (EVS side) upgrades automatically with EVS
   — HCX on-prem Manager must be manually upgraded to match
```

## Pre-Upgrade Checklist

Complete all of these before starting any VCF component upgrade.

**vSAN Health**

```powershell
$cluster = Get-Cluster -Name "EVS-Management-Cluster"
$vsanHealth = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$result = $vsanHealth.QueryVsanClusterHealthSummary($cluster.Id,$null,$null,$true,$null,$null,"defaultView")
$result.Groups | Where-Object { $_.GroupHealth -ne "green" } | Select GroupName, GroupHealth
```

All vSAN health groups must show `green` before proceeding. Any `yellow` or `red` group must be resolved first.

**vSAN Resync**

```powershell
Get-VsanResyncDashboard -Cluster (Get-Cluster "EVS-Management-Cluster") | Select BytesToSync, ActiveTasks
```

BytesToSync must be 0 before upgrading any host.

**NSX-T Stability**

```bash
curl -sk -u "admin:$NSX_PASS" "$NSX_URL/api/v1/cluster/status" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('control_cluster_status',{}).get('status',''))"
```

Expected: `STABLE`. Do not upgrade if NSX-T is in `DEGRADED` or `UNSTABLE` state.

**No Active vMotion Operations**

```powershell
Get-Task | Where-Object { $_.Name -like "*vmotion*" -and $_.State -eq "Running" }
```

Wait for all vMotion tasks to complete before starting an upgrade.

**SDDC Manager Configuration Backup**

Take a manual backup of SDDC Manager configuration before upgrading:

```bash
SDDC_URL="https://sddc-manager.vcf.internal"
TOKEN=$(curl -sk -X POST "${SDDC_URL}/v1/tokens" \
  -H "Content-Type: application/json" \
  -d '{"username":"administrator@vsphere.local","password":"P@ssw0rd"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('accessToken',''))")

curl -sk -X POST -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${SDDC_URL}/v1/backups/tasks" \
  -d '{"elements":[{"resourceType":"SDDC_MANAGER"}]}'
```

**VCF Compatibility Matrix Check**

Before upgrading, verify the target version combination is supported:

- VMware Cloud Foundation Release Notes for the target VCF version
- VMware Product Interoperability Matrix: confirm ESXi, NSX-T, and vCenter version combinations
- Check that the target HCX version is compatible with the target VCF version

## ESXi Upgrade via vSphere Lifecycle Manager

For EVS environments, ESXi upgrades go through vSphere Lifecycle Manager (vLCM) inside vCenter, not SDDC Manager UI directly. SDDC Manager triggers the vLCM workflow as part of the VCF upgrade bundle, but the actual host remediation is visible in vCenter.

**Check current ESXi version across all hosts:**

```powershell
Connect-VIServer -Server vcenter.vcf.internal -User administrator@vsphere.local -Password 'P@ssw0rd'

Get-VMHost | Select Name, Version, Build, `
  @{N="LicenseKey";E={$_.LicenseKey}} | Sort Version
```

**Check vLCM baseline compliance:**

```powershell
$cluster = Get-Cluster -Name "EVS-Management-Cluster"

Get-VMHost -Location $cluster | ForEach-Object {
    $h = $_
    $compliance = ($h | Get-Compliance)
    [PSCustomObject]@{
        Host = $h.Name
        Version = $h.Version
        ComplianceStatus = $compliance.Status
    }
}
```

**Trigger remediation for a host via PowerCLI:**

```powershell
$baseline = Get-Baseline -Name "EVS-ESXi-8.0-U2"
$host = Get-VMHost -Name "evs-host-01.vcf.internal"

Test-Compliance -Entity $host -UpdateType HostPatch
Remediate-Inventory -Entity $host -Baseline $baseline -Confirm:$false
```

SDDC Manager typically invokes remediation automatically as part of the VCF upgrade workflow. Only run manual remediation if directed by SDDC Manager or if a host failed automatic remediation and you need to retry a single host.

## HCX Version Upgrade

HCX Cloud (the EVS-side appliance) upgrades automatically when EVS upgrades the VCF stack. You do not manage HCX Cloud upgrades directly. HCX on-premises Manager must be manually upgraded to match.

**Check current HCX version (both sides):**

```bash
HCX_ONPREM="https://hcx-onprem.corp.local"
HCX_EVS="https://hcx-cloud.vcf.internal"

echo "On-prem HCX:"
curl -sk -u "admin:$HCX_PASS" "${HCX_ONPREM}/hybridity/api/about" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"  Version: {d.get('version','unknown')}\")"

echo "EVS HCX Cloud:"
curl -sk -u "admin:$HCX_PASS" "${HCX_EVS}/hybridity/api/about" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"  Version: {d.get('version','unknown')}\")"
```

Both sides must run the same major HCX version. If EVS has upgraded HCX Cloud automatically, upgrade on-prem HCX Manager before using HCX for migrations.

**Upgrade on-prem HCX Manager:**

1. HCX Manager UI → Summary → Updates → Check for Updates
2. Download and apply the update
3. HCX Manager reboots (~20-30 min)
4. HCX Manager UI → Interconnect → Service Mesh → verify links are green
5. If service mesh appliances need updating: Interconnect → Service Mesh → Update (per mesh)

## SDDC Manager Lifecycle

```bash
# Access SDDC Manager
# URL: https://sddc-manager.vcf.internal
# Credentials: from AWS Secrets Manager /evs/<env-name>/sddc-manager-credentials

# Check for available upgrade bundles
# SDDC Manager UI → Lifecycle Management → Bundle Management → Download Available Bundles

# Trigger upgrade workflow
# SDDC Manager UI → Lifecycle Management → Upgrade
#   Select target VCF version → run precheck → schedule → execute

# Monitor upgrade progress
# SDDC Manager → Lifecycle Management → Upgrade → running workflow task
# Takes: 4-8 hours for full stack (all components)
```

## Rollback Considerations

VCF component upgrades are generally not rollbackable. This applies especially to NSX-T and ESXi upgrades, which modify kernel-level components that cannot be downgraded via software. Plan accordingly:

**Management VM Snapshots (before each component upgrade)**

Before upgrading each component, snapshot the management VMs:

```powershell
$mgmtVMs = @("vcenter", "sddc-manager", "nsx-manager-01", "nsx-manager-02", "nsx-manager-03")

foreach ($vmName in $mgmtVMs) {
    $vm = Get-VM -Name $vmName -ErrorAction SilentlyContinue
    if ($vm) {
        New-Snapshot -VM $vm -Name "pre-upgrade-$(Get-Date -Format yyyy-MM-dd)" `
          -Description "Snapshot before VCF upgrade" -Confirm:$false
        Write-Output "Snapshot created for $vmName"
    }
}
```

Delete snapshots after the upgrade is confirmed successful (snapshots consume vSAN space):

```powershell
Get-VM | Get-Snapshot | Where-Object { $_.Name -like "pre-upgrade-*" } | Remove-Snapshot -Confirm:$false
```

**What can be rolled back:**

- vCenter Server: if snapshot was taken before upgrade, the snapshot can be reverted. Note that reverting vCenter to a snapshot while ESXi hosts are already on a newer version will create a version mismatch — only do this if the ESXi upgrade has not yet started.
- SDDC Manager: can be reverted to snapshot in isolation if the upgrade failed before vCenter began.

**What cannot be rolled back:**

- ESXi: no downgrade path exists once a host has been remediated to a new version. The only recovery for a failed ESXi upgrade is to re-image the host (which requires removing and re-adding the host to the EVS cluster).
- NSX-T: NSX-T provides no in-place downgrade. If a manager upgrade fails mid-way, VMware Support must assist with recovery.

## Version Compatibility Matrix

| VCF Version | ESXi Version | NSX-T Version | vCenter Version |
|---|---|---|---|
| VCF 5.1 | ESXi 8.0 U2 | NSX 4.1 | vCenter 8.0 U2 |
| VCF 5.0 | ESXi 8.0 U1 | NSX 4.0 | vCenter 8.0 U1 |
| VCF 4.5 | ESXi 7.0 U3 | NSX 3.2 | vCenter 7.0 U3 |

Always verify the VMware Product Interoperability Matrix before upgrading EVS components.
