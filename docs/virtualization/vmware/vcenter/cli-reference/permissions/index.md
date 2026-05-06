# Permissions & Roles

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

---

## Permissions & Roles

```powershell
# Roles
Get-VIRole
Get-VIRole -Name "ReadOnly"

# Permissions
Get-VIPermission
Get-VIPermission | Where-Object { $_.Principal -eq "<domain>\<user>" }

# Assign role
New-VIPermission -Entity (Get-Datacenter <dc>) -Principal "<domain>\<user>" -Role (Get-VIRole "ReadOnly") -Propagate:$true
```
