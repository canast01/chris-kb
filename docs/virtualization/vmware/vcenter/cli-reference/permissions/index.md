# Permissions & Roles

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).
## Roles

```powershell
# List all roles
Get-VIRole

# Role details — privileges assigned
Get-VIRole -Name "ReadOnly" | Select-Object Name, PrivilegeList

# Find roles with a specific privilege
Get-VIRole | Where-Object { $_.PrivilegeList -contains "VirtualMachine.Config.Memory" }
```

## Permissions

```powershell
# All permissions in the inventory
Get-VIPermission

# Permissions for a specific user or group
Get-VIPermission | Where-Object { $_.Principal -eq "<domain>\<user>" }

# Permissions on a specific entity
Get-VIPermission -Entity (Get-VM "<vm_name>")
Get-VIPermission -Entity (Get-Datacenter "<dc_name>")
Get-VIPermission -Entity (Get-Cluster "<cluster_name>")
```

## Assign a Role

```powershell
# Grant a role on a datacenter (propagates to all children)
New-VIPermission `
    -Entity (Get-Datacenter "<dc_name>") `
    -Principal "<domain>\<user>" `
    -Role (Get-VIRole "ReadOnly") `
    -Propagate:$true

# Grant on a specific VM (no propagation needed)
New-VIPermission `
    -Entity (Get-VM "<vm_name>") `
    -Principal "<domain>\<group>" `
    -Role (Get-VIRole "Virtual Machine User") `
    -Propagate:$false
```

## Modify and Remove Permissions

```powershell
# Change role for an existing permission
Set-VIPermission `
    -Permission (Get-VIPermission -Entity (Get-Datacenter "<dc>") | Where-Object { $_.Principal -eq "<domain>\<user>" }) `
    -Role (Get-VIRole "Administrator")

# Remove a permission
Get-VIPermission -Entity (Get-VM "<vm_name>") |
    Where-Object { $_.Principal -eq "<domain>\<user>" } |
    Remove-VIPermission -Confirm:$false
```

## Create a Custom Role

```powershell
# Create a role with specific privileges
New-VIRole -Name "VM-PowerOps" -Privilege (
    Get-VIPrivilege -Name "Power On", "Power Off", "Reset", "Suspend"
)

# Assign custom role
New-VIPermission `
    -Entity (Get-Folder "<folder_name>") `
    -Principal "<domain>\vm-operators" `
    -Role (Get-VIRole "VM-PowerOps") `
    -Propagate:$true
```

## Audit: Permission Report

```powershell
# Export all permissions to CSV
Get-VIPermission | Select-Object Entity, Principal, Role, IsGroup, Propagate |
    Export-Csv -Path vcenter_permissions.csv -NoTypeInformation

# Identify users with Administrator role
Get-VIPermission | Where-Object { $_.Role -eq "Admin" } |
    Select-Object Entity, Principal, Propagate
```

## Common Built-in Roles

| Role | Use Case |
|---|---|
| `Administrator` | Full control — assign sparingly |
| `ReadOnly` | Audit or monitoring accounts |
| `Virtual Machine Power User` | VM console, power ops, snapshots |
| `Virtual Machine User` | VM console and guest interaction only |
| `Resource Pool Administrator` | Manage resource pools within a scope |
| `Network Administrator` | Manage VDS/portgroups |
| `Datastore Consumer` | Browse and allocate datastore space |
