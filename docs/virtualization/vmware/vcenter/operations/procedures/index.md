---
tags:
  - operations
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter — Procedures


<div class="kb-summary">
Common vCenter procedures — adding and reconnecting ESXi hosts, vMotion and storage migrations, snapshot management, tag management, HA reconfiguration, content library, certificate replacement, file-based backup, roles/permissions, SSO identity sources, alarms, cluster config, and VCSA upgrade.
</div>

```text
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

## Replace vCenter Certificates (VMCA)

vCenter certificate replacement is required when certificates expire, are compromised, or when moving to a custom CA.

```bash
# Method 1: Auto-renew machine SSL cert via VAMI (for VMCA-signed certs)
# https://<vcenter-fqdn>:5480 → Certificate Management → Machine SSL Certificate → Renew

# Method 2: Replace with custom CA cert using certificate-manager
ssh root@<vcenter-fqdn>
/usr/lib/vmware-vmca/bin/certificate-manager
# Option 1: Replace Machine SSL certificate with custom certificate
# Option 6: Replace Solution User certificates with custom certificate
# Provide: root CA cert, signed machine cert, private key

# Method 3: STS certificate renewal (required every 2 years for VMCA-signed)
# STS certs do not auto-renew — check expiry:
python /usr/lib/vmware-vmafd/bin/lstool.py list --url http://localhost:7080/lookupservice/sdk 2>/dev/null | grep -i expire

# Renew STS cert (vSphere 7+):
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store TRUSTED_ROOTS
# Use certificate-manager → Option 8: Reset all certificates
```

Post-replacement validation:

```bash
# Verify new cert is active
echo | openssl s_client -connect <vcenter-fqdn>:443 2>/dev/null | openssl x509 -noout -dates -subject
# Confirm NotAfter shows new expiry

# Verify services are healthy after restart
vmon-cli --status | grep -E "RUNNING|STOPPED"
# All critical services should be RUNNING

# Verify vCenter is accessible from vSphere Client
# Verify ESXi hosts still show Connected
```

## vCenter File-Based Backup

vCenter supports scheduled file-based backups to NFS, SFTP, FTPS, HTTP, or HTTPS locations.

```bash
# Configure backup via VAMI: https://<vcenter-fqdn>:5480
# Backup → Configure → set protocol, location, credentials, schedule, retention

# Trigger manual backup via API
curl -sk -X POST "https://<vcenter-fqdn>/api/vcenter/deployment/backup/schedules?vmw-task=true" \
  -H "vmware-api-session-id: <session-id>" \
  -H "Content-Type: application/json" \
  -d '{
    "location_type": "SFTP",
    "location": "sftp://backup-srv/vcenter-backups",
    "location_user": "vcbackup",
    "location_password": "<password>",
    "parts": ["SEAT"]
  }'

# SEAT = Statistics, Events, Alarms, Tasks (recommended addition to core backup)
```

```powershell
# Monitor backup job status
$headers = @{ "vmware-api-session-id" = $sessionId }
Invoke-RestMethod "https://<vcenter-fqdn>/api/vcenter/deployment/backup/job" -Headers $headers |
  Select-Object id, state, end_time, messages
```

Backup includes: vCenter database, configuration, inventory, and optionally historical data (SEAT). Restore requires the vCenter ISO and backup archive.

---

## Manage Roles and Permissions

vCenter RBAC uses Roles (permission sets) assigned to Principals (users or groups) at a specific inventory object level.

```powershell
# List all roles
Get-VIRole

# Create a custom role with specific privileges
New-VIRole -Name "VM-Operator" -Privilege (Get-VIPrivilege -Id "VirtualMachine.Interact.PowerOn",
    "VirtualMachine.Interact.PowerOff",
    "VirtualMachine.Interact.ConsoleInteract",
    "VirtualMachine.Interact.Suspend")

# Assign role to an AD group at a folder level
$folder = Get-Folder -Name "Production-VMs"
$principal = "DOMAIN\vm-operators"
New-VIPermission -Entity $folder -Principal $principal -Role "VM-Operator" -Propagate:$true

# List permissions on an object
Get-VIPermission -Entity (Get-Folder "Production-VMs")

# Remove a permission
Get-VIPermission -Entity (Get-Folder "Production-VMs") -Principal "DOMAIN\vm-operators" |
    Remove-VIPermission -Confirm:$false
```

**Best practices:**
- Assign permissions at the lowest scope that satisfies the use case (folder/cluster, not root)
- Use AD groups, not individual user accounts
- Never assign Administrator role at root unless required for the admin account
- Audit permissions quarterly: export and review unexpected root-level assignments

---

## Configure SSO Identity Source (Active Directory)

Required before AD accounts/groups can authenticate to vCenter.

1. vCenter → **Administration** → **Single Sign On** → **Configuration** → **Identity Sources**
2. Click **Add Identity Source**
3. Select **Active Directory (Integrated Windows Authentication)** for domain-joined VCSA, or **Active Directory as an LDAP Server** for explicit LDAP binding
4. For LDAP binding:
   - **Domain name**: `EXAMPLE.LOCAL`
   - **Domain alias**: `EXAMPLE`
   - **Base DN for users**: `CN=Users,DC=example,DC=local`
   - **Base DN for groups**: `CN=Users,DC=example,DC=local`
   - **Username / Password**: dedicated service account (e.g., `svc-vcenter-ldap`)
5. Click **Test Connection** → confirm AD is reachable
6. Click **Add** → SSO now resolves AD users
7. Assign vCenter roles to AD groups: Administration → **Access Control** → **Global Permissions** or per-object permissions

```bash
# Verify AD identity source via SSO API
curl -sk -X GET "https://<vcenter-fqdn>/api/vcenter/identity/providers" \
  -H "vmware-api-session-id: <session-id>"
```

---

## Configure a vSphere Alarm

Alarms alert on object state changes or metric threshold violations.

1. vCenter → right-click the target object (cluster, datastore, host) → **Alarms → New Alarm**
2. Set the alarm name and description
3. Under **Triggers**, define the condition:
   - **State trigger**: Host Connection State = Not Responding → trigger after 60 seconds
   - **Metric trigger**: Datastore Free Space < 20% for 5 minutes
4. Under **Actions**, configure what happens when the alarm fires:
   - Send email notification (requires SMTP configured: Administration → SMTP)
   - Run a script
   - Send an SNMP trap
5. Click **OK** — the alarm is immediately active for the selected object and (if checked) its children

```powershell
# List all defined alarms
Get-AlarmDefinition | Select-Object Name, Enabled, Description

# Enable/disable a specific alarm
Get-AlarmDefinition -Name "Host CPU Usage" | Set-AlarmDefinition -Enabled:$false

# Acknowledge an active alarm
Get-AlarmAction | Where-Object { $_.Alarm.Name -eq "Host CPU Usage" }
```

---

## Configure a Cluster (DRS and HA)

When creating or reconfiguring a cluster:

```powershell
# Create a new cluster with DRS and HA
New-Cluster -Name "CL-LON-PROD" -Location (Get-Datacenter "DC-LON") `
    -DrsEnabled:$true -DrsAutomationLevel FullyAutomated `
    -HAEnabled:$true -HAAdmissionControlEnabled:$true

# Configure HA admission control (25% = 1-host failover for a 4-node cluster)
$cluster = Get-Cluster "CL-LON-PROD"
$spec = New-Object VMware.Vim.ClusterConfigSpecEx
$spec.DasConfig = New-Object VMware.Vim.ClusterDasConfigInfo
$spec.DasConfig.AdmissionControlPolicy = New-Object VMware.Vim.ClusterFailoverResourcesAdmissionControlPolicy
$spec.DasConfig.AdmissionControlPolicy.CpuFailoverResourcesPercent = 25
$spec.DasConfig.AdmissionControlPolicy.MemoryFailoverResourcesPercent = 25
($cluster | Get-View).ReconfigureComputeResource_Task($spec, $true)

# Enable EVC (Enhanced vMotion Compatibility) for mixed CPU generations
$clusterView = Get-Cluster "CL-LON-PROD" | Get-View
$evcSpec = New-Object VMware.Vim.EVCMode
$evcSpec.Key = "intel-broadwell"  # set to the lowest CPU generation in cluster
$clusterView.ConfigureEvcMode_Task($evcSpec)
```

Verify cluster health after configuration:

```powershell
# Check HA and DRS configuration
Get-Cluster "CL-LON-PROD" | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel, HAAdmissionControlEnabled, HAFailoverLevel
```

---

## Upgrade vCenter Server (VCSA)

vCenter upgrades use the VCSA installer ISO and run a 2-phase migration: deploy new VCSA then transfer data.

**Pre-upgrade checklist:**
- Snapshot or file-based backup of current VCSA
- Confirm all ESXi hosts are at or below the target vCenter's supported version
- Resolve any existing alarms and health warnings
- Check VMware Interoperability Matrix for NSX/vSAN/Aria compatibility

**Phase 1 — Deploy new VCSA:**
1. Mount the vCenter ISO on a Windows/Linux/macOS machine
2. Run `vcsa-ui-installer/win32/installer.exe` (or `.../lin64/installer` on Linux)
3. Select **Upgrade** → **Install**
4. Enter the source vCenter FQDN and credentials
5. Configure the new VCSA: deployment size, FQDN, IP, NTP, SSO password
6. The installer deploys the new VCSA alongside the existing one — no downtime yet

**Phase 2 — Transfer data:**
1. The installer prompts to switch to the new VCSA
2. vCenter inventory, permissions, and historical data are transferred
3. Source VCSA is powered off after successful transfer
4. Update DNS if using hostname-based access

**Post-upgrade validation:**
```bash
# Verify vCenter version from VAMI
curl -sk "https://<new-vcenter-fqdn>:5480/rest/appliance/system/version" \
  -u "administrator@vsphere.local:<password>"

# Check all services running
ssh root@<new-vcenter-fqdn>
vmon-cli --status | grep -v RUNNING

# Verify ESXi hosts still show Connected in the new vCenter
```
