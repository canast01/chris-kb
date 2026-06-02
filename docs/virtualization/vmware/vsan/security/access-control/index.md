# vSAN — Access Control


<div class="kb-summary">
vSAN access control is implemented through vCenter's Role-Based Access Control (RBAC) system. There is no separate vSAN permission model — all vSAN management actions require vCenter permissions on the cluster or datacenter objects.
</div>

```text
vSAN RBAC MODEL

  WHO (identity)          ROLE (permissions)        WHERE (scope)
  ──────────────────      ──────────────────────    ────────────────────
  AD Group                Administrator             vCenter Root
  vSAN-Operators  ──────► (full vSAN access)  ───► (KMS config only)
                      │
  AD Group          │   vSAN-StorageOperator        Cluster scope
  vSAN-Operators  ──┼──► (disk groups, health, ───► VSAN-LON-01
                      │   policies, maintenance)      │
  Service Account   │                                 └─► propagates to
  svc-aria-vcenter──┼──► vSAN-Monitor-RO     ─────► hosts + datastore
                      │   (read-only health,
  Service Account   │    capacity, objects)
  svc-veeam     ────┴──► vSAN-PolicyAdmin    ─────► Cluster scope
                          (storage policies           (policy CRUD)
                           create/edit/delete)

  Permission inheritance:
  vCenter Root
       └── Datacenter
               └── Cluster  ◄── assign vSAN roles here
                       ├── Host-01
                       ├── Host-02
                       └── vSAN Datastore  ◄── inherits (propagate=true)
```
```text
┌──────────────────────────────────────── vSAN — Access Control ────────────────────────────────────────┐
│                                                                                                       │
│  vSAN access control is managed through vCenter RBAC; dedicated vSAN admin                            │
│  roles and storage policy permissions control cluster configuration changes.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            vCenter RBAC for vSAN             │  │           vSAN-Specific Privileges          │   │
│   │           Host.Config.Storage priv           │  │          Datastore.Config: required         │   │
│   │           Cluster-level Admin role           │  │            StorageProfile.Update            │   │
│   │        No direct disk access for VMs         │  │          VsanHealth: read-only role         │   │
│   │        Least privilege: read-only ops        │  │          Disk.Configure: only admin         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Restrict disk configuration to cluster admins; storage policy changes to vSAN admins.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               ESXi Host Access               │  │              Audit & Compliance             │   │
│   │         SSH: disable when not needed         │  │           Log: all disk config ops          │   │
│   │           ESXi shell: time-limited           │  │         Review: admin accounts qtrly        │   │
│   │            Lockdown mode: enforce            │  │         Alert: unexpected disk claim        │   │
│   │           Access via vCenter only            │  │         SIEM: forward vCenter events        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical disk access is restricted by ESXi; vSAN manages all disk I/O;                               │
│  no direct block device access from guest VMs.                                                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RBAC          = Role-Based Access Control; vCenter permission model                                  │
│  Privilege     = atomic permission; e.g., Datastore.Config                                            │
│  Lockdown mode = ESXi blocks direct access; all ops via vCenter only                                  │
│  StorageProfile= vCenter storage policy permission set                                                │
│  VsanHealth    = read-only vSAN health monitoring privilege                                           │
│  Disk.Configure= permission to add/remove disks from vSAN                                             │
│  SIEM          = Security Info and Event Mgmt; receives vCenter events                                │
│  SSH disable   = reduce attack surface; enable only for troubleshooting                               │
│  Shell timeout = ESXi shell auto-closes after idle; set to 600s                                       │
│  Cluster admin = role with full vSAN management privileges                                            │
│  Audit log     = vCenter event log; captures all disk/policy changes                                  │
│  Qtrly review  = check admin accounts; remove stale assignments                                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Custom Roles

### vSAN Read-Only Role (Monitoring)

For monitoring systems (Aria Operations, Nagios, custom scripts) that only need to read vSAN status.

```powershell
$monitorPrivileges = @(
    "System.Anonymous", "System.Read", "System.View",
    "VsanHealth.ClusterHealth.Get",
    "StorageProfile.View",
    "Datastore.Browse",
    "Performance.ModifyIntervals",
    "Global.VCServer"
)

New-VIRole -Name "vSAN-Monitor-RO" `
    -Privilege (Get-VIPrivilege -Id $monitorPrivileges)
```

### vSAN Policy Administrator

For users who design and manage storage policies but do not manage physical hardware.

```powershell
$policyAdminPrivileges = @(
    "System.Anonymous", "System.Read", "System.View",
    "StorageProfile.View",
    "StorageProfile.Update",
    "VsanHealth.ClusterHealth.Get",
    "Datastore.Browse",
    "VirtualMachine.Config.ChangeTracking"  # needed to apply policy changes to VMs
)

New-VIRole -Name "vSAN-PolicyAdmin" `
    -Privilege (Get-VIPrivilege -Id $policyAdminPrivileges)
```

---

## Assigning Permissions

### Assign Role to AD Group

Always assign permissions to AD groups, not individual users. This simplifies onboarding and offboarding.

```powershell
# Assign vSAN-StorageOperator role to an AD group on the cluster
New-VIPermission `
    -Entity (Get-Cluster "VSAN-LON-01") `
    -Principal "EXAMPLE\vSAN-Operators" `
    -Role "vSAN-StorageOperator" `
    -Propagate $true

# Assign monitoring role to a service account
New-VIPermission `
    -Entity (Get-Cluster "VSAN-LON-01") `
    -Principal "EXAMPLE\svc-aria-vcenter" `
    -Role "vSAN-Monitor-RO" `
    -Propagate $true
```

**From vCenter UI:**
Cluster → Permissions → Add → select identity source → search for group or user → select role → check Propagate

### Verify Effective Permissions

```powershell
# List all permissions on a cluster
Get-VIPermission -Entity (Get-Cluster "VSAN-LON-01") |
    Select Principal, Role, Propagate |
    Format-Table -AutoSize

# Check what a specific user can do
$cluster = Get-Cluster "VSAN-LON-01"
Get-VIPermission -Entity $cluster | Where-Object { $_.Principal -like "*StorageOps*" }
```

---

## Storage Policy Access Control

Storage policies (SPBM) have their own permission layer within vCenter. Control who can create, edit, and assign policies.

| Privilege | Who Needs It |
|---|---|
| `StorageProfile.View` | All users who provision VMs on vSAN (to select policies) |
| `StorageProfile.Update` | Storage administrators who design and manage policies |
| `StorageProfile.Delete` | Storage administrators only |

```powershell
# Check storage policy permissions
Get-VIPermission -Entity (Get-vCenter) |
    Where-Object { $_.Role -match "PolicyAdmin\|Administrator" }
```

**Protect production policies:** Do not allow VM owners or application teams to modify or create storage policies. Only the storage team should manage the canonical policy set.

---

## vSAN Datastore Access

The vSAN datastore is presented as a single namespace. VM placement on the vSAN datastore is controlled by:

1. **vCenter RBAC:** The user or service account provisioning the VM must have `Datastore.FileManagement` on the vSAN datastore.
2. **Storage Policy compliance:** The vSAN datastore only accepts objects that comply with the assigned storage policy.

**Restrict access to the vSAN datastore by cluster:**

```powershell
# Remove Read-Only access inherited from parent for a non-privileged group
# (Add No Access permission at the datastore level to block inheritance)
$vsanDS = Get-Datastore "vsanDatastore"
New-VIPermission `
    -Entity $vsanDS `
    -Principal "EXAMPLE\AppTeam-NonPrivileged" `
    -Role "NoAccess" `
    -Propagate $false
```

---

## Privileged Access Governance

### Break-Glass Accounts

Maintain documented break-glass procedures for scenarios where AD authentication is unavailable:

- `administrator@vsphere.local` credentials stored in a physical safe or a PAM tool.
- ESXi root credentials stored per host in the PAM tool.
- KMS admin credentials (separate from vCenter access) stored with the same controls.

Review and rotate break-glass credentials at least quarterly.

### Audit Access Reviews

Perform a quarterly review of vCenter permissions:

```powershell
# Export all permissions across the vCenter inventory
$allPerms = @()
$allObjects = Get-View -ViewType All | Where-Object { $_.MoRef.Type -in @("ClusterComputeResource","HostSystem","Datastore","Datacenter") }
foreach ($obj in $allObjects) {
    $perms = Get-VIPermission -Entity (Get-VIObject -MoRef $obj.MoRef) -ErrorAction SilentlyContinue
    $allPerms += $perms
}
$allPerms | Select Entity, Principal, Role, Propagate |
    Export-Csv "vcenter_permissions_$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation
```

Review the export for:
- Accounts that should no longer have access (leavers, role changes).
- Accounts with more privileges than their role requires.
- Service accounts assigned Administrator instead of a minimal role.
- Permissions assigned to individual users instead of groups.

### Separation of Duties

| Function | Responsible Role |
|---|---|
| vSAN hardware configuration (disk groups) | Storage Administrator |
| Storage policy design and approval | Storage Architect |
| VM provisioning (selecting policies) | VM Operator (with View on policies only) |
| Encryption key management | Security / KMS Administrator |
| Backup job configuration | Backup Administrator |
| vCenter and SSO user management | Identity Administrator |

No single person should hold both "Storage Administrator" and "KMS Administrator" roles for production systems.

---

## Access Control for Stretched Clusters

The witness host (vSAN Witness Appliance or physical ESXi) requires:

- Management access from the vCenter managing the production cluster.
- Connectivity on the vSAN witness vmkernel network.
- No production VM workloads running on the witness.

**Restrict witness host access:**

- Assign only `Read Only` vCenter role to operations staff on the witness host.
- Only the vSAN service account and vCenter itself need write access to the witness.
- Do not join the witness host to the same AD OU as production hosts — it is a lower-privilege asset.

```powershell
# Assign read-only access to the witness host for monitoring only
New-VIPermission `
    -Entity (Get-VMHost "vsanwitness-lon.example.com") `
    -Principal "EXAMPLE\vSAN-Operators" `
    -Role "ReadOnly" `
    -Propagate $false
```
