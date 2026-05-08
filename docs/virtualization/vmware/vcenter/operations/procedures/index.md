# vCenter — Procedures

## Incident Triage

Use this checklist at the start of any vCenter-related incident to establish scope before taking action.

- [ ] Check vCenter services via VAMI → Services — identify any stopped or failed services
- [ ] Check SSO / PSC health — authentication failures often root-cause in SSO component
- [ ] Review vCenter logs: `/var/log/vmware/vpxd/vpxd.log` on VCSA for errors at incident time
- [ ] Check database health — VCSA embedded Postgres: `service-control --status vmware-vpostgres`
- [ ] Review vCenter events for the affected objects: `Get-VIEvent -Entity <cluster/host/vm> -MaxSamples 200`
- [ ] Check certificate validity — expired cert causes cascading authentication and agent failures
- [ ] Verify network connectivity to VCSA — DNS resolution, vCenter FQDN reachable from hosts
- [ ] Escalate to VMware Support if VPXD service cannot be restarted or database corruption suspected

| Question | Answer |
|---|---|
| Which VCSA services are stopped? | VAMI → Services — identify failed service |
| Is SSO/PSC healthy? | VAMI → SSO, or check `lookupservice` log |
| What does vpxd.log show? | `/var/log/vmware/vpxd/vpxd.log` at incident time |
| Are certificates valid? | VAMI → Certificate Management — check expiry |
| Can hosts connect to vCenter? | Host agent log: `/var/log/vmware/hostd.log` on ESXi |

---

## Maintenance Window Procedure

### Pre-Maintenance Steps

1. Take a VCSA backup via VAMI → Backup, or confirm last backup is current (< 24 hours old)
2. Snapshot the VCSA VM if running virtualised on a separate vCenter (do not use as primary recovery method)
3. Confirm no active DRS migrations or critical tasks running in vCenter
4. Notify all teams that vCenter will be unavailable during maintenance — **workloads continue running on ESXi** even when vCenter is down
5. Check disk space on VCSA before any change:
   ```bash
   df -h
   ```
6. Confirm HA admission control has capacity for the window:
   ```powershell
   Get-Cluster | Select-Object Name, HAEnabled, HAAdmissionControlEnabled
   ```

### During Maintenance

- If performing VCSA update: use VAMI → Update; do not interrupt mid-update
- Restart services one at a time where possible; use `--all` only when necessary
- Monitor `/var/log/vmware/vpxd/vpxd.log` during any service restarts

### Post-Maintenance Validation

- [ ] All VCSA services running: VAMI → Services shows all Started
- [ ] All ESXi hosts Connected:
  ```powershell
  Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"}
  ```
  Result should be empty.
- [ ] DRS and HA active on all clusters:
  ```powershell
  Get-Cluster | Select-Object Name, DrsEnabled, HAEnabled
  ```
- [ ] No critical unacknowledged alarms in vCenter
- [ ] PowerCLI connection successful:
  ```powershell
  Connect-VIServer -Server <vcenter>
  ```
- [ ] vCenter REST API responding:
  ```bash
  curl -sk -u 'administrator@vsphere.local:<password>' \
    -X POST https://<vcenter>/api/session
  # then:
  curl -sk -H "vmware-api-session-id: <token>" \
    https://<vcenter>/api/vcenter/health/system
  ```
  Expected response: `"GREEN"`
- [ ] No new vpxd.log errors introduced by the change
- [ ] Close change ticket with VAMI service status screenshot and PowerCLI connection confirmation

---

## Restarting Services Safely

Only restart services after checking disk space and reviewing recent changes. A full partition causes vpxd or postgres to fail immediately after restart.

```bash
# Check disk space first — /storage/db and /storage/log are the critical ones
df -h

# Check which service is stopped
service-control --status --all

# Restart one service at a time where possible
service-control --restart vpxd
service-control --restart vmware-vpostgres

# Restart a specific service with dependency awareness
service-control --stop vpxd
service-control --start vpxd

# Full restart (causes brief vCenter unavailability — typically 3–5 minutes)
service-control --stop --all
service-control --start --all

# Verify after restart
service-control --status --all
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

Add-VMHost -Name "esxi-05.corp.local" -Location $cluster -User root -Password $cred.GetNetworkCredential().Password -Force
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
$vmhost = Get-VMHost -Name "esxi-01.corp.local"
Set-VMHost -VMHost $vmhost -State Maintenance -Evacuate

# Wait for maintenance mode to be accepted
do {
    Start-Sleep -Seconds 10
    $vmhost = Get-VMHost -Name "esxi-01.corp.local"
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
Set-VMHost -VMHost (Get-VMHost "esxi-01.corp.local") -State Connected
```

---

## vMotion — Migrating a VM

```powershell
# Live vMotion (compute only — same storage)
Move-VM -VM "app-server-01" -Destination (Get-VMHost "esxi-02.corp.local")

# Storage vMotion (same host, different datastore)
Move-VM -VM "app-server-01" -Datastore (Get-Datastore "DS-VMFS-PURE01-02")

# Full migration (compute + storage)
Move-VM -VM "app-server-01" `
    -Destination (Get-VMHost "esxi-02.corp.local") `
    -Datastore (Get-Datastore "DS-VMFS-PURE01-02")

# Bulk evacuate all VMs from a host
$sourceHost = Get-VMHost "esxi-01.corp.local"
$targetHost = Get-VMHost "esxi-02.corp.local"
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
(Get-VMHost "esxi-01.corp.local").ExtensionData.ReconnectHost_Task($null)
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
    -VMHost (Get-VMHost "esxi-01.corp.local") `
    -Datastore (Get-Datastore "DS-VMFS-PURE01-01") `
    -ResourcePool (Get-ResourcePool "RP-PROD-STANDARD")
```

Best practices:
- Publish a single library from a central vCenter; subscribe from spoke vCenters (Linked Mode or subscribed library)
- Keep templates on a dedicated datastore separate from production VM storage
- Update templates monthly — patch, update VMware Tools, then convert back to template
