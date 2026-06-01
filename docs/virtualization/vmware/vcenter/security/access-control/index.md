# vCenter Security — Access Control


<div class="kb-summary">
Access Control reference covering Built-in Roles, Custom Roles, SSO Domain and Identity Sources, Audit Logging — Access Events, PowerCLI — Permission Management and 3 more sections.
</div>

```text
RBAC Permission Model
════════════════════════════════════════════════════════

  vCenter Inventory Hierarchy (permission scope)
  ┌─────────────────────────────────────────────────────┐
  │  Global Permission  ← applies to ALL vCenters       │
  │  (use sparingly)                                     │
  └───────────────────────────┬─────────────────────────┘
                              │ propagates down
                    ┌─────────▼──────────┐
                    │  vCenter            │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  Datacenter (DC-X)  │ ← assign most roles here
                    └─────────┬──────────┘
                              │
               ┌──────────────┼─────────────────┐
               │              │                 │
      ┌────────▼──────┐ ┌─────▼──────┐ ┌───────▼─────┐
      │  Cluster      │ │  Folder    │ │  Host       │
      │  (CL-X-PROD)  │ │            │ │  (esxi-01)  │
      └───────┬───────┘ └────────────┘ └─────────────┘
              │
     ┌────────▼────────┐
     │  VM             │  ← No Access here overrides Admin above
     │  (app-server-01)│
     └─────────────────┘

  Permission Assignment = Principal + Role + Scope
  ┌───────────────────────────────────────────────────┐
  │  CORP\grp-vcenter-ops  +  VM Operator  +  DC-LON  │
  │  svc-veeam-backup      +  BackupOp     +  DC-LON  │
  │  svc-nsx-compute       +  NSX-Integration + DC-LON│
  │  svc-aria-ops          +  Read-Only    +  Root     │
  └───────────────────────────────────────────────────┘
```
┌─────────────────────────────────── vCenter Server — Access Control ───────────────────────────────────┐
│                                                                                                       │
│  vCenter access control uses SSO for authentication and a role-based permission                       │
│  system applied at inventory object level for authorisation.                                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Role-Based Access               │  │            Permission Inheritance           │   │
│   │           Roles: built-in + custom           │  │            Propagate to children            │   │
│   │         Admin / ReadOnly / NoAccess          │  │           Override at child object          │   │
│   │           Privilege sets per role            │  │             Global perm: all DCs            │   │
│   │           Apply role to user/group           │  │         No propagate: exact obj only        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Assign minimum roles at highest useful object; propagate down the hierarchy.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Identity Sources               │  │           Admin Lockout Prevention          │   │
│   │               SSO local domain               │  │      Always keep administrator@vsphere      │   │
│   │           Active Directory joined            │  │         Break-glass: local SSO user         │   │
│   │            LDAP: OpenLDAP support            │  │        Audit: review perms quarterly        │   │
│   │          AD groups mapped to roles           │  │         Log: all permission changes         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SSO identity store traffic goes over LDAP/LDAPS to AD DCs on management network.                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSO           = Single Sign-On; vCenter identity service; issues SAML tokens                         │
│  Role          = named collection of privileges; applied to user+object pair                          │
│  Privilege     = atomic permission; e.g., VirtualMachine.Power.On                                     │
│  Propagate     = permission flows to all child objects in hierarchy                                   │
│  Global perm   = permission applied at root level across all datacentres                              │
│  administrator@vsphere.local= built-in SSO admin; never remove                                        │
│  Break-glass   = local SSO account for use when AD/LDAP is down                                       │
│  Identity source= AD, LDAP, or local domain; multiple sources allowed                                 │
│  AD group      = Active Directory security group mapped to vCenter role                               │
│  NoAccess role = explicitly blocks access at that object level                                        │
│  Audit         = review all admin-role assignments at least quarterly                                 │
│  Hierarchy     = DC → cluster → host → VM; permissions flow downward                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**VM Operator** — day-to-day VM management without storage or host access:
```text
VirtualMachine.Interact.PowerOn
VirtualMachine.Interact.PowerOff
VirtualMachine.Interact.Reset
VirtualMachine.Interact.ConsoleInteract
VirtualMachine.GuestOperations.*
VirtualMachine.State.CreateSnapshot
VirtualMachine.State.RemoveSnapshot
```

**Read-Only + Performance** — monitoring access including performance counters:
```text
System.Read
System.Anonymous
System.View
Performance.ModifyIntervals (optional, for custom stat intervals)
```

**NSX Integration Service Account**:
```text
Host.Config.Network
Host.Config.Patch
Host.Inventory.EditCluster
Network.*
VirtualMachine.Config.Network
```

---

## SSO Domain and Identity Sources

vCenter ships with a local `vsphere.local` SSO domain. The `administrator@vsphere.local` account is the bootstrap admin.

### Production Identity Source Configuration

Navigate to **Administration → Single Sign On → Configuration → Identity Sources → Add**:

| Field | Value |
|---|---|
| Type | Active Directory (Integrated Windows Authentication) or LDAP |
| Domain name | `corp.example.com` |
| Domain alias | `CORP` |
| LDAP URL | `ldaps://dc01.corp.example.com:636` |
| Base DN (users) | `DC=corp,DC=example,DC=com` |
| Base DN (groups) | `DC=corp,DC=example,DC=com` |
| Username | `svc-vcenter-ldap@corp.example.com` |
| Password | (service account password) |

Always use LDAPS (port 636) rather than LDAP (port 389) to encrypt credentials and directory queries in transit.

### Service Account Best Practices

The LDAP bind account needs only read-only access to AD:
```powershell
# Create a restricted service account in AD (PowerShell on DC)
New-ADUser -Name "svc-vcenter-ldap" -SamAccountName "svc-vcenter-ldap" `
    -UserPrincipalName "svc-vcenter-ldap@corp.example.com" `
    -Path "OU=Service Accounts,DC=corp,DC=example,DC=com" `
    -AccountPassword (ConvertTo-SecureString "P@ssw0rd123!" -AsPlainText -Force) `
    -Enabled $true -PasswordNeverExpires $true

# Deny all group memberships except Domain Users
# Delegate only Read to the Users OU
```

### Administrator@vsphere.local

- Do **not** use for day-to-day operations — use named AD accounts
- Rotate the password quarterly; store in password vault with break-glass procedure
- Monitor for any logins using this account (set SIEM alert on principal = `administrator@vsphere.local`)
- The account cannot be deleted; it is the last-resort access when AD integration fails

---

## Audit Logging — Access Events

### vCenter Events and Tasks

All configuration changes in vCenter generate events viewable at **Monitor → Events**. Events are stored in the PostgreSQL database. Default retention: 30 days for tasks, 30 days for events.

Adjust retention at **Administration → vCenter Server Settings → Statistics**:
- Maximum event age: 90 days (recommended for audit purposes)
- Maximum task age: 90 days

### Syslog Forwarding to SIEM

Forward vCenter audit events to SIEM/syslog aggregator:

```text
VAMI (https://<vcenter>:5480) → Syslog → Add Syslog Server
Protocol: TLS (preferred) / UDP / TCP
Port: 514 (UDP), 6514 (TLS)
```

Events forwarded include: login/logout, permission changes, VM creation/deletion, host add/remove, task success/failure.

Key event types for SIEM alerting:

| Event | Description |
|---|---|
| `com.vmware.sso.LoginFailure` | Failed SSO login attempt |
| `com.vmware.sso.LoginSuccess` | Successful login |
| `vim.event.UserLoginSessionEvent` | User session established |
| `vim.event.PermissionAddedEvent` | Permission granted |
| `vim.event.PermissionRemovedEvent` | Permission revoked |
| `vim.event.RoleAddedEvent` | New role created |
| `vim.event.VMPoweredOffEvent` | VM powered off |
| `vim.event.HostRemovedEvent` | Host removed from inventory |

### Alarms for Security Events

Create vCenter alarms for:
- Failed login attempts (event: `com.vmware.sso.LoginFailure`)
- Permission additions/removals
- Certificate expiry (< 30 days)
- SSH enabled on ESXi host

---

## PowerCLI — Permission Management

```powershell
# List all permissions in the environment
Get-VIPermission

# Permissions for a specific user or group
Get-VIPermission | Where-Object { $_.Principal -eq "CORP\jsmith" }
Get-VIPermission | Where-Object { $_.Principal -match "vsphere.local" }

# Assign a role to a user at the datacenter level (propagates to all children)
New-VIPermission `
    -Entity (Get-Datacenter "DC-LON") `
    -Principal "CORP\grp-vcenter-ops" `
    -Role (Get-VIRole "VM Operator") `
    -Propagate:$true

# Assign a role to a group at cluster scope only
New-VIPermission `
    -Entity (Get-Cluster "CL-LON-PROD") `
    -Principal "CORP\grp-app-team" `
    -Role (Get-VIRole "Virtual Machine User") `
    -Propagate:$true

# Remove a permission
Get-VIPermission -Entity (Get-Datacenter "DC-LON") |
    Where-Object { $_.Principal -eq "CORP\jsmith" } |
    Remove-VIPermission -Confirm:$false

# Create a custom role with specific privileges
$privs = Get-VIPrivilege -Id "VirtualMachine.Interact.PowerOn",
    "VirtualMachine.Interact.PowerOff",
    "VirtualMachine.State.CreateSnapshot",
    "VirtualMachine.State.RemoveSnapshot"
New-VIRole -Name "VM-Operator-Custom" -Privilege $privs

# Audit: export all permissions to CSV
Get-VIPermission | Select-Object Entity, Principal, Role, IsGroup, Propagate |
    Export-Csv -Path vcenter_permissions_$(Get-Date -Format yyyyMMdd).csv -NoTypeInformation

# Identify all principals with Administrator role
Get-VIPermission | Where-Object { $_.Role -eq "Admin" } |
    Select-Object Entity, Principal, IsGroup, Propagate |
    Format-Table -AutoSize

# Identify users with global permissions
Get-VIPermission -Global | Select-Object Principal, Role, IsGroup
```

---

## Service Account Inventory

Maintain a registry of all service accounts that have vCenter permissions:

| Account | Purpose | Role | Scope | Owner | Review Date |
|---|---|---|---|---|---|
| `svc-vcenter-ldap` | AD identity source bind | None (read-only AD) | AD only | Platform team | Quarterly |
| `svc-veeam-backup` | Veeam VADP backup | Backup Operator (custom) | Datacenter | Backup team | Quarterly |
| `svc-nsx-compute` | NSX compute manager | NSX Integration (custom) | Datacenter | Network team | Quarterly |
| `svc-aria-ops` | Aria Operations adapter | Read-Only | Root | Platform team | Quarterly |
| `svc-ansible` | Automation | VM Operator (custom) | Specific clusters | Automation team | Quarterly |

Review service account access quarterly. Disable accounts for decommissioned services immediately.

---

## Access Review Procedure

Run quarterly or after any team change, project completion, or security incident.

```powershell
# Export current permission state
Get-VIPermission | Select-Object Entity, Principal, Role, IsGroup, Propagate |
    Export-Csv -Path vcenter_permissions_review_$(Get-Date -Format yyyyMMdd).csv -NoTypeInformation

# Find any non-group (individual user) permissions — should be rare in production
Get-VIPermission | Where-Object { -not $_.IsGroup } |
    Select-Object Entity, Principal, Role, Propagate

# Find permissions at VM level (overly specific, usually a mistake)
Get-VM | ForEach-Object {
    Get-VIPermission -Entity $_ | Where-Object { $_.Principal -notmatch "SYSTEM" }
} | Select-Object Entity, Principal, Role

# Check for stale permissions from deprovisioned accounts
# Compare against current AD group members
```

Access review checklist:

| Check | Action |
|---|---|
| All Administrator-role holders | Verify each is still current staff and still needs admin |
| Service accounts | Verify each account is active and used by its documented system |
| Global permissions | Verify none added without approval; remove any that can be scoped |
| No Access roles | Verify intent — remove if no longer needed |
| Permissions on individual VMs | Consolidate to folder or cluster level |
| AD groups | Verify group membership is current; remove departed staff |

---

## Lockout and Break-Glass

If `administrator@vsphere.local` is locked out:

```bash
# SSH to VCSA as root
/usr/lib/vmware-vmafd/bin/dir-cli user unlock \
    --account administrator \
    --domain vsphere.local \
    --password <vmdir-admin-password>
```

If the root password is unknown, use the VCSA VM console (via ESXi DCUI) to boot into single-user mode and reset it — documented in VMware KB 2069041.

Store the break-glass password for `administrator@vsphere.local` in an offline vault (e.g., printed and sealed, or HSM-backed secrets manager) separate from the primary password manager. The break-glass procedure must be documented and tested annually.
