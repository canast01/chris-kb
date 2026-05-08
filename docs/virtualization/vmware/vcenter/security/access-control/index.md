# vCenter Security — Access Control

## Role-Based Access Control (RBAC)

vCenter uses a privilege-based permission model. Permissions are assigned as: **principal (user/group) + role (privilege set) + inventory object (scope)** + optional propagation to children.

### Built-in Roles

| Role | Description |
|---|---|
| Administrator | Full access to all objects |
| Read-Only | View objects and properties; no configuration changes |
| No Access | Explicitly block access to an object subtree |
| Virtual Machine User | Interact with (console, power on/off) but not configure VMs |
| Virtual Machine Power User | Interact + snapshot + basic reconfiguration |
| Resource Pool Administrator | Manage resource pools and child objects |
| Network Administrator | Manage networks and distributed switches |
| Datastore Consumer | Allocate space from datastores |

### Permission Scopes

- **Global Permission**: Applies across all vCenter instances in the SSO domain; use sparingly
- **Inventory Permission**: Applied at datacenter, cluster, folder, or individual object level
- **Propagation**: Check "Propagate to children" to apply down the hierarchy

### Custom Roles

Create custom roles for least-privilege: **Administration → Roles → New**

Common custom role patterns:
- **Backup Operator**: Snapshot + datastore browse + VM config (VADP minimum)
- **VM Operator**: Power operations + console + snapshot; no host/network/storage access
- **Monitoring Reader**: Read-only + performance counters
- **NSX Integration Service Account**: Specific host/network privileges for NSX compute manager

## SSO Domain and Identity Sources

vCenter ships with a local `vsphere.local` SSO domain. The `administrator@vsphere.local` account is the bootstrap admin. In production:

- Add AD as an identity source
- Grant required AD groups vSphere roles
- Do not use `administrator@vsphere.local` for day-to-day operations
- Rotate `administrator@vsphere.local` password per policy; document in password vault

## Audit Logging — Access Events

### vCenter Events and Tasks

All configuration changes in vCenter generate events viewable at **Monitor → Events**. Events are stored in the PostgreSQL database. Default retention: 30 days for tasks, 30 days for events. Adjust at **Administration → vCenter Server Settings → Statistics**.

### Syslog Forwarding

Forward vCenter audit events to SIEM/syslog aggregator:

```
VAMI (https://<vcenter>:5480) → Syslog → Add Syslog Server
Protocol: TLS (preferred) / UDP / TCP
Port: 514 (UDP), 6514 (TLS)
```

Events forwarded include: login/logout, permission changes, VM creation/deletion, host add/remove.

### Alarms for Security Events

Create vCenter alarms for:
- Failed login attempts (event: `com.vmware.sso.LoginFailure`)
- Permission additions/removals
- Certificate expiry (< 30 days)
- SSH enabled on ESXi host

## PowerCLI — Permission Management

```powershell
# List all permissions
Get-VIPermission

# Permissions for a specific user
Get-VIPermission | Where-Object { $_.Principal -eq "<domain>\<user>" }

# Assign a role
New-VIPermission `
    -Entity (Get-Datacenter "<dc_name>") `
    -Principal "<domain>\<user>" `
    -Role (Get-VIRole "ReadOnly") `
    -Propagate:$true

# Remove a permission
Get-VIPermission -Entity (Get-VM "<vm_name>") |
    Where-Object { $_.Principal -eq "<domain>\<user>" } |
    Remove-VIPermission -Confirm:$false

# Audit: export all permissions to CSV
Get-VIPermission | Select-Object Entity, Principal, Role, IsGroup, Propagate |
    Export-Csv -Path vcenter_permissions.csv -NoTypeInformation

# Identify users with Administrator role
Get-VIPermission | Where-Object { $_.Role -eq "Admin" } |
    Select-Object Entity, Principal, Propagate
```

## vCenter Roles RBAC Reference (from roles-permissions)

vCenter RBAC, roles, groups, permissions, access reviews, and least privilege cleanup.

### Access Review Checklist

| Check | Notes |
|---|---|
| Review active alarms | Identify anomalous activity |
| Check recent failed tasks | Flag permission-related failures |
| Confirm service health | Verify no unauthorised changes |
| Review recent permission or inventory changes | Monitor → Events → filter on permission events |
| Confirm ownership and support notes | Ensure accounts have owners documented |
| Validate dependencies | Confirm service accounts still valid |
