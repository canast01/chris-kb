# vCenter — Procedures


<div class="kb-summary">
Procedures reference covering Pre-Maintenance Steps, Restarting Services Safely, Adding an ESXi Host to vCenter, Placing a Host in Maintenance Mode, vMotion — Migrating a VM and 6 more sections.
</div>

```text
VCSA Procedure Flow — Maintenance Window
════════════════════════════════════════════════════════

  Pre-Maintenance                During              Post-Validation
  ┌───────────────────┐         ┌──────────┐         ┌─────────────────┐
  │ 1. VCSA backup    │         │ Perform  │         │ services OK?    │
  │    (VAMI→Backup)  │         │ change   │         │ hosts Connected?│
  │                   │         │          │         │ DRS/HA active?  │
  │ 2. Check df -h    │────────▶│ Monitor  │────────▶│ API responding? │
  │                   │         │ vpxd.log │         │ no new errors?  │
  │ 3. HA admission   │         │          │         │ close ticket    │
  │    capacity check │         │          │         └─────────────────┘
  │                   │         └──────────┘
  │ 4. Notify teams   │
  └───────────────────┘

  Service Restart Order (dependency chain)
  ┌──────────────────────────────────────────────────┐
  │                                                  │
  │  vmware-vpostgres  ←── must start first (DB)     │
  │         │                                        │
  │         ▼                                        │
  │  vmware-stsd       ←── SSO token service         │
  │         │                                        │
  │         ▼                                        │
  │  vmware-sts-idmd   ←── identity daemon           │
  │         │                                        │
  │         ▼                                        │
  │  vpxd              ←── core vCenter daemon       │
  │         │                                        │
  │         ▼                                        │
  │  vsphere-ui        ←── HTML5 client              │
  │  vmware-eam        ←── ESX Agent Manager         │
  │                                                  │
  └──────────────────────────────────────────────────┘
```
```
┌───────────────────────────────── vCenter Server — Common Procedures ──────────────────────────────────┐
│                                                                                                       │
│  Routine vCenter procedures: certificate renewal, host add/remove, cluster                            │
│  configuration, permissions management, and licence assignment.                                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Procedures            │  │               Host Procedures               │   │
│   │           Renew machine cert: VAMI           │  │          Add host: Hosts & Clusters         │   │
│   │          Replace cert: certmgr CLI           │  │            Enter maintenance mode           │   │
│   │          STS cert: scripted renewal          │  │           Remove host: disconnect           │   │
│   │        Renew all: certificate-manager        │  │          Reconnect: fix vpxa creds          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Certificate procedures require SSO admin; host procedures require host permissions.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Permissions & Licences            │  │              Cluster Procedures             │   │
│   │         Assign role at object level          │  │           Enable DRS: auto/manual           │   │
│   │            SSO groups: AD mapped             │  │          Enable HA: configure slots         │   │
│   │         Licence: Administration tab          │  │           vSAN: create diskgroups           │   │
│   │         Global perm: cross-DC roles          │  │            EVC: set CPU baseline            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  All procedures run over vCenter management network; certificate operations                           │
│  cause brief service interruption (~2 min) during VCSA service restart.                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  certificate-manager = VCSA interactive script; renews/replaces all certs                             │
│  certmgr       = low-level cert tool; used for individual cert replacement                            │
│  STS cert      = Security Token Service cert; 2-year validity; manual renew                           │
│  VAMI          = Appliance Management; port 5480; auto-renew machine cert                             │
│  Maintenance mode= drain host of VMs before patching or removal                                       │
│  vpxa creds    = host agent credentials; reconnect if changed via VC UI                               │
│  EVC           = Enhanced vMotion Compatibility; CPU instruction masking                              │
│  DRS slots     = admission control slots; HA reserves resources per policy                            │
│  Global perm   = permission applies to all objects in all datacentres                                 │
│  Role          = named permission set; e.g., Administrator, ReadOnly                                  │
│  Licence key   = applied per product; vSAN, DRS, HA all need VC licence                               │
│  Diskgroup     = vSAN storage unit; one cache tier + capacity tier per host                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Service restart order for manual recovery:
1. `vmware-vpostgres` — database must be running before vpxd
2. `vmware-stsd` — SSO token service
3. `vpxd` — core vCenter service
4. `vsphere-ui` — vSphere Client (if needed)

---

## Adding an ESXi Host to vCenter

```powershell
# Via PowerCLI
$dc = Get-Datacenter -Name "DC-LON"
$cluster = Get-Cluster -Name "CL-LON-PROD"
$cred = Get-Credential   # ESXi root credentials

Add-VMHost -Name "esxi-05.example.local" -Location $cluster -User root -Password $cred.GetNetworkCredential().Password -Force
```

Via UI: **vCenter → Datacenter or Cluster → Actions → Add Host**. Enter FQDN, root credentials, and accept the host thumbprint.

Post-add checks:
- Host shows Connected state
- VMs on host visible in inventory
- Host belongs to correct cluster (DRS/HA active)
- Host NTP, DNS, and syslog confirmed configured

---

## Placing a Host in Maintenance Mode

```powershell
# PowerCLI — maintenance mode with vMotion evacuation
$vmhost = Get-VMHost -Name "esxi-01.example.local"
Set-VMHost -VMHost $vmhost -State Maintenance -Evacuate

# Wait for maintenance mode to be accepted
do {
    Start-Sleep -Seconds 10
    $vmhost = Get-VMHost -Name "esxi-01.example.local"
    Write-Host "State: $($vmhost.State)"
} until ($vmhost.State -eq "Maintenance")
```

```bash
# From ESXi shell (if vCenter unavailable)
esxcli system maintenanceMode set --enable true
esxcli system maintenanceMode get
```

Exit maintenance mode:
```powershell
Set-VMHost -VMHost (Get-VMHost "esxi-01.example.local") -State Connected
```

---

## vMotion — Migrating a VM

```powershell
# Live vMotion (compute only — same storage)
Move-VM -VM "app-server-01" -Destination (Get-VMHost "esxi-02.example.local")

# Storage vMotion (same host, different datastore)
Move-VM -VM "app-server-01" -Datastore (Get-Datastore "DS-VMFS-PURE01-02")

# Full migration (compute + storage)
Move-VM -VM "app-server-01" `
    -Destination (Get-VMHost "esxi-02.example.local") `
    -Datastore (Get-Datastore "DS-VMFS-PURE01-02")

# Bulk evacuate all VMs from a host
$sourceHost = Get-VMHost "esxi-01.example.local"
$targetHost = Get-VMHost "esxi-02.example.local"
Get-VM -Location $sourceHost | Move-VM -Destination $targetHost
```

vMotion requirements:
- Shared storage visible to both hosts (for compute-only vMotion)
- vMotion VMkernel on both hosts (same layer-2 or routed vMotion network)
- Compatible CPU features (use EVC cluster mode to align CPU generations)

---

## Snapshot Management

Snapshots consume datastore space equal to the delta from the base disk. Stale snapshots degrade I/O performance and fill datastores.

```powershell
# Find all snapshots older than 7 days across all VMs
Get-VM | Get-Snapshot |
    Where-Object { $_.Created -lt (Get-Date).AddDays(-7) } |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB, 2)}},
    @{N="AgeDays";E={[math]::Round(((Get-Date) - $_.Created).TotalDays, 0)}} |
    Sort-Object AgeDays -Descending

# Remove a specific snapshot
Remove-Snapshot `
    -Snapshot (Get-Snapshot -VM "app-server-01" -Name "pre-patch-2026-04-01") `
    -Confirm:$false

# Remove ALL snapshots for a VM (consolidate)
Get-Snapshot -VM "app-server-01" | Remove-Snapshot -RemoveChildren -Confirm:$false

# Find VMs needing disk consolidation (snapshot files remain after removal)
Get-VM | Where-Object { $_.ExtensionData.Runtime.ConsolidationNeeded } |
    Select-Object Name, @{N="Host";E={$_.VMHost.Name}}
```

Consolidation via UI: right-click VM → **Snapshots → Consolidate**. This removes orphaned delta files without removing a snapshot from the tree.

---

## Inventory Hygiene Tasks

Run these weekly or include in the daily check script.

```powershell
# Find orphaned / unexpectedly powered-off VMs
Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" } |
    Select-Object Name, @{N="Host";E={$_.VMHost.Name}},
    @{N="LastChange";E={$_.ExtensionData.Config.ChangeVersion}}

# VMs not assigned to any resource pool (using cluster root directly)
Get-VM | Where-Object { $_.ResourcePool.Name -eq (Get-Cluster).Name } |
    Select-Object Name, PowerState

# VMs with VMware Tools not running
Get-VM | Where-Object { $_.ExtensionData.Guest.ToolsRunningStatus -ne "guestToolsRunning" } |
    Select-Object Name, PowerState, @{N="ToolsStatus";E={$_.ExtensionData.Guest.ToolsRunningStatus}}

# Export full VM inventory
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB,
    @{N="VMHost";E={$_.VMHost.Name}},
    @{N="Cluster";E={$_.VMHost.Parent.Name}},
    @{N="Datastore";E={($_ | Get-Datastore).Name -join ";"}} |
    Export-Csv -Path vm_inventory.csv -NoTypeInformation
```

---

## Resync Disconnected Host

When a host shows "Not Responding" or "Disconnected":

```bash
# From VCSA SSH — check vpxd log for host connectivity errors
grep "<esxi-hostname>" /var/log/vmware/vpxd/vpxd.log | tail -50
```

```powershell
# PowerCLI — attempt reconnect
(Get-VMHost "esxi-01.example.local").ExtensionData.ReconnectHost_Task($null)
```

```bash
# From ESXi host SSH — restart the vCenter agent (vpxa)
/etc/init.d/vpxa restart
/etc/init.d/hostd restart

# Verify agent is running
/etc/init.d/vpxa status
```

If the host certificate has drifted from vCenter's expected thumbprint, reconnect via UI and accept the new thumbprint, or re-add the host to vCenter after removing it.

---

## Managing vSphere Tags

Tags are used for inventory classification, RBAC scoping, and backup policy targeting.

```powershell
# List all tag categories and tags
Get-TagCategory
Get-Tag

# Assign a tag to a VM
$tag = Get-Tag -Name "prod" -Category "env"
New-TagAssignment -Tag $tag -Entity (Get-VM "app-server-01")

# List all VMs with a specific tag
Get-TagAssignment -Tag (Get-Tag -Name "prod" -Category "env") |
    Select-Object -ExpandProperty Entity |
    Where-Object { $_ -is [VMware.VimAutomation.ViCore.Types.V1.Inventory.VirtualMachine] } |
    Select-Object Name, PowerState

# Bulk tag assignment
$tag = Get-Tag -Name "gold" -Category "tier"
Get-VM -Location (Get-Cluster "CL-LON-PROD") | ForEach-Object {
    New-TagAssignment -Tag $tag -Entity $_ -ErrorAction SilentlyContinue
}

# Export tag assignments to CSV
Get-TagAssignment | Select-Object `
    @{N="Entity";E={$_.Entity.Name}}, `
    @{N="Category";E={$_.Tag.Category.Name}}, `
    @{N="Tag";E={$_.Tag.Name}} |
    Export-Csv -Path tag_assignments.csv -NoTypeInformation
```

---

## Reconfiguring vSphere HA

After adding or removing hosts, or after host failures, HA may need reconfiguration:

```powershell
# Check HA state on all clusters
Get-Cluster | Select-Object Name, HAEnabled, HAAdmissionControlEnabled, HAFailoverLevel

# Reconfigure HA on a specific cluster (resolves most config warnings)
$cluster = Get-Cluster -Name "CL-LON-PROD"
$clusterView = $cluster | Get-View
$clusterView.ReconfigureComputeResource_Task($clusterView.ConfigurationEx, $true)
```

Via UI: right-click cluster → **Reconfigure for vSphere HA**. This re-evaluates all hosts and resolves most "HA configuration issues" warnings without disrupting running VMs.

---

## Content Library Management

Content Libraries store VM templates, OVF/OVA templates, and ISO images centrally.

```powershell
# List content libraries
Get-ContentLibrary

# Get items in a library
Get-ContentLibrary -Name "Templates-LON" | Get-ContentLibraryItem

# Deploy a VM from a template in the content library
$template = Get-ContentLibraryItem -Name "RHEL9-Gold" -ContentLibrary "Templates-LON"
New-VM -Name "new-vm-01" -ContentLibraryItem $template `
    -VMHost (Get-VMHost "esxi-01.example.local") `
    -Datastore (Get-Datastore "DS-VMFS-PURE01-01") `
    -ResourcePool (Get-ResourcePool "RP-PROD-STANDARD")
```

Best practices:
- Publish a single library from a central vCenter; subscribe from spoke vCenters (Linked Mode or subscribed library)
- Keep templates on a dedicated datastore separate from production VM storage
- Update templates monthly — patch, update VMware Tools, then convert back to template
