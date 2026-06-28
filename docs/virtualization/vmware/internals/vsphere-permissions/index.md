---
tags:
  - internals
  - vmware
---
# vSphere Permissions Model — SSO, Roles, Inheritance, and Least Privilege

<div class="kb-summary">
vSphere access control is built on a layered permission model: SSO handles authentication, roles define what actions are allowed, and permissions bind a role to a user or group on a specific inventory object. This page covers the full stack — SSO domains and identity sources, built-in and custom roles, permission inheritance and propagation rules, global permissions, solution user certificates, service account patterns, and practical least-privilege designs for production environments.

*Applies to: vSphere 7.x / 8.x*
</div>

---

## Authentication Layer — SSO and Identity Sources

### vCenter Single Sign-On (SSO)

SSO is the authentication broker for all vSphere components. Every login to vCenter, ESXi (via vCenter), and other VMware products goes through SSO. It issues SAML tokens that components exchange after initial authentication.

**SSO domain:** `vsphere.local` is the default. It contains:

- Built-in administrator account: `administrator@vsphere.local`
- Built-in groups: `Administrators`, `CAAdmins`, `ActAsUsers`, `LicenseService.Administrators`
- Solution users (machine accounts for vCenter services)

> Never use `administrator@vsphere.local` for day-to-day operations. It bypasses AD group policies, its activity does not appear in AD audit logs, and it has no lockout policy by default. Use it only for break-glass recovery.

### Identity Sources

vCenter SSO can authenticate users from multiple identity sources simultaneously:

| Type | Protocol | Use case |
|---|---|---|
| **Active Directory (Integrated Windows Auth)** | Kerberos | vCenter server is domain-joined; recommended for AD environments |
| **Active Directory as LDAP** | LDAP/LDAPS | vCenter is not domain-joined; explicit bind credentials required |
| **OpenLDAP** | LDAP | Non-AD LDAP directories |
| **vsphere.local** | Built-in | Local SSO accounts — break-glass and solution users |

```bash
# List configured identity sources via CLI (vCenter)
/usr/lib/vmware-vmafd/bin/dir-cli sso-config show-identity-sources \
  --login administrator@vsphere.local

# Or via API (useful in automation):
# GET https://vcenter/api/vcenter/identity/providers
```

**LDAP binding account best practice:**

- Create a dedicated read-only AD service account (e.g., `svc-vcenter-bind`)
- Bind with LDAPS (port 636) — never plain LDAP in production
- Grant only `Read` on the Users/Groups OU — no admin rights needed
- Set the account to never expire or manage rotation carefully (connector breaks immediately on password expiry)

### SSO Lockout and Password Policies

SSO has its own lockout policy independent of AD:

```text
Default SSO policies (vsphere.local accounts):
  Password: 8+ chars, 1 upper, 1 lower, 1 digit, 1 special
  Max failures before lockout: 5
  Lockout duration: 300 seconds
  Failed attempt window: 180 seconds

Location in vCenter UI:
  Administration → Single Sign On → Configuration → Local Accounts → Policy
```

---

## The Permission Model

A **permission** in vSphere is a triple: `(user_or_group, role, inventory_object)`. It answers: "Who can do What on Which object."

```text
Permission = Principal + Role + Object

Example:
  Principal:  CORP\vsphere-admins (AD group)
  Role:       VM Power User
  Object:     Folder: Production VMs
  Propagate:  Yes (applies to all child objects)
```

### Object Hierarchy (Inheritance Chain)

Permissions propagate down the inventory tree when **Propagate to children** is checked:

```text
Global (root)
  └── vCenter Server
        └── Datacenter
              ├── Cluster
              │     └── ESXi Host
              │           └── VM
              ├── Datastore
              ├── Network
              └── Folder
                    └── VM
```

A permission set on the Datacenter with propagation enabled applies to all objects within it — clusters, hosts, VMs, datastores, and networks. A permission set at the VM level only applies to that VM.

**Resolution rule:** The most specific permission wins. If a user has `Read Only` on the Datacenter but `VM Power User` on a specific VM, they get `VM Power User` rights on that VM and `Read Only` on everything else.

---

## Built-In Roles

vCenter ships with a fixed set of system roles that cannot be modified or deleted:

| Role | Typical use |
|---|---|
| **No Access** | Explicitly denies all access (overrides inherited permissions) |
| **Read Only** | View objects and their properties — no actions |
| **View** | Browse inventory structure only (see folders, not properties) |
| **Administrator** | Full access to all operations |
| **Virtual Machine Power User** | Start, stop, reset, configure VMs; no provisioning or host access |
| **Virtual Machine User** | Interact with VM console and devices; cannot change VM config |
| **Resource Pool Administrator** | Manage resource pools and VMs within them |
| **VMware Consolidated Backup User** | Permissions required for backup solutions (snapshot operations, datastore browse) |
| **Datastore Consumer** | Allocate space on datastores; used for storage operations |
| **Network Administrator** | Manage virtual networking objects |

### Sample Roles for Common Scenarios

```text
Helpdesk operator — needs VM console access only:
  Role: Virtual Machine User
  Object: Folder containing all user VMs
  Propagate: Yes

Storage admin — manages datastores, no VM access:
  Role: Custom (Datastore: all privileges, VM: none)
  Object: Datacenter (datastores visible at this level)

L1 infrastructure team — power ops, no provisioning:
  Role: Virtual Machine Power User
  Object: Cluster or Datacenter
  Propagate: Yes
```

---

## Custom Roles

Custom roles let you build precisely scoped permission sets from vSphere's ~350 individual privileges.

```powershell
# PowerCLI — create a custom role
New-VIRole -Name "AppTeam-VM-Operator" `
  -Privilege (Get-VIPrivilege `
    -Id VirtualMachine.Interact.PowerOn,
         VirtualMachine.Interact.PowerOff,
         VirtualMachine.Interact.Reset,
         VirtualMachine.Interact.ConsoleInteract,
         VirtualMachine.State.CreateSnapshot,
         VirtualMachine.State.RemoveSnapshot,
         Global.CancelTask)

# Assign the role to a group on a folder
$folder   = Get-Folder "Production-Apps"
$role     = Get-VIRole "AppTeam-VM-Operator"
$principal = "CORP\appteam-ops"
New-VIPermission -Entity $folder -Principal $principal `
  -Role $role -Propagate $true
```

### Privilege Categories to Know

| Category | Key privileges |
|---|---|
| **VirtualMachine.Config** | Add disk, change CPU/memory, rename, annotate |
| **VirtualMachine.Interact** | Power on/off, console, guest OS operations, inject USB |
| **VirtualMachine.Inventory** | Create, register, delete, move VMs |
| **VirtualMachine.Provisioning** | Clone, deploy from template, export |
| **VirtualMachine.State** | Create/remove snapshots, revert |
| **Host.Config** | Network, storage, firmware, advanced settings |
| **Datastore** | Browse, manage files, allocate space |
| **Resource** | Assign VMs to pools, migrate (vMotion) |
| **Sessions** | Validate session, impersonate — rarely granted |

> **Audit shortcut:** Export current role definitions to CSV regularly. Unexpected privilege additions to custom roles are a common audit finding.

```powershell
# Export all roles and privileges to CSV
Get-VIRole | ForEach-Object {
  $role = $_
  $role.PrivilegeList | ForEach-Object {
    [PSCustomObject]@{
      Role      = $role.Name
      Privilege = $_
    }
  }
} | Export-Csv -Path "/tmp/vsphere-roles-audit.csv" -NoTypeInformation
```

---

## Permission Propagation and Inheritance Rules

### How Propagation Works

When you create a permission with **Propagate to children: Yes**, all current and future child objects inherit it. Permissions are not stored on child objects — they are evaluated at access time by walking up the hierarchy.

```text
Permission evaluation for user accessing VM "APP-01":
  1. Check VM "APP-01" — direct permission? → use it
  2. No direct? → check parent folder
  3. No folder permission? → check cluster
  4. No cluster? → check datacenter
  5. No datacenter? → check global (root)
  6. No permission found anywhere → No Access
```

### Blocking Inheritance

To deny access to a subtree while granting access to the parent:

1. Set `No Access` role on the object where you want to block — this is the only way to deny
2. Or: do not propagate the parent permission; grant explicit permissions only on specific child objects

```text
Scenario: AD group "AllEngineers" has Read Only on the Datacenter.
Problem:  Sensitive VM "PAYROLL-01" must not be visible to AllEngineers.
Solution: Assign the "No Access" role to AllEngineers directly on "PAYROLL-01".
          This overrides the inherited Read Only from the Datacenter.
```

### Common Mistakes

| Mistake | Effect |
|---|---|
| Granting permission at vCenter root without checking propagation | Unintentionally grants access to all datacenters and objects |
| Forgetting that `No Access` is an active assignment | Removing a `No Access` permission does not grant access; it restores inherited access |
| Setting permissions on individual VMs instead of folders | Permissions are lost when a VM is moved; folder-based permissions follow automatically |
| Using individual user accounts instead of AD groups | Creates unmanageable permission sprawl; use AD groups |

---

## Global Permissions

Global permissions (set at the **root** of the vSphere inventory) apply across multiple vCenter instances linked via Enhanced Linked Mode. They are evaluated before vCenter-level permissions.

```text
Normal permission: applies to one vCenter's objects
Global permission: applies to all vCenter objects across the linked domain

Use cases for global permissions:
  - SSO administrators who manage identity sources on all vCenters
  - Enterprise monitoring accounts that need read-only access everywhere
  - vCenter-level administrators (need access to the vCenter appliance itself,
    not just inventory objects)
```

**Setting global permissions:**

```text
vSphere Client → Administration → Global Permissions → Add
  Principal: CORP\vcenter-global-admins
  Role: Administrator
  Propagate: Yes
```

> Global permissions are stored in the SSO directory, not in individual vCenter databases. They survive vCenter reinstalls if SSO is preserved. Back up SSO configuration before major vCenter upgrades.

---

## Solution Users and Service Accounts

### Solution Users

Solution users are machine accounts representing vCenter services (vpxd, vsphere-ui, vpxd-extension). They authenticate using X.509 certificates rather than passwords.

```bash
# List solution users on vCenter
/usr/lib/vmware-vmafd/bin/dir-cli service list \
  --login administrator@vsphere.local

# Check certificate expiry for solution users
/usr/lib/vmware-vmafd/bin/vecs-cli entry getcert \
  --store MACHINE_SSL_CERT --alias __MACHINE_CERT | \
  openssl x509 -noout -dates

# Renew all certificates (run as root on VCSA)
/usr/lib/vmware-vmca/bin/certificate-manager
```

**Certificate expiry is a common production incident.** Solution user certificates expire after 2 years by default in some vCenter versions. When they expire, vCenter services cannot communicate internally — symptoms include grey hosts, missing datastores in vCenter UI, and API authentication failures.

### Service Accounts for Automation and Backup

Create dedicated service accounts for each tool that integrates with vCenter:

| Tool type | Recommended role | Scope |
|---|---|---|
| Backup (Veeam, Commvault) | VMware Consolidated Backup User + custom snapshot/datastore privileges | Datacenter or specific folders |
| Monitoring (vROps, Zabbix) | Read Only | vCenter root with propagation |
| Automation (Terraform, Ansible) | Custom role (minimum required privileges) | Per-folder or per-cluster |
| Replication (SRM, vSphere Replication) | Custom SRM role (documented per product) | Datacenter |

```powershell
# PowerCLI — create a read-only monitoring service account permission
$vcUser   = "CORP\svc-vsphere-monitor"
$role     = Get-VIRole "ReadOnly"
$vcRoot   = Get-Folder -Type Datacenter -Name "/"  # root
New-VIPermission -Entity (Get-Datacenter) `
  -Principal $vcUser -Role $role -Propagate $true
```

**Service account hygiene:**

- Never use `administrator@vsphere.local` for automation — rotation is painful and disruption is total
- Document each service account's purpose, owning team, and rotation schedule in CMDB
- Set AD service accounts to not require interactive logon
- Review service account permissions quarterly

---

## Least-Privilege Design Patterns

### Pattern 1 — Tiered Team Access

```text
Tier       | Principal              | Role                    | Object
-----------|------------------------|-------------------------|------------------
L3 vSphere | CORP\vsphere-l3        | Administrator           | Datacenter
L2 infra   | CORP\vsphere-l2        | Virtual Machine Power User | Cluster
L1 ops     | CORP\vsphere-l1        | Virtual Machine User    | Production Folder
App teams  | CORP\<app-team>        | Custom (power + console) | App Folder
Monitoring | CORP\svc-monitor       | Read Only               | vCenter root
Backup     | CORP\svc-backup        | Custom backup role      | Datacenter
```

### Pattern 2 — Folder-Per-Environment Isolation

```text
Datacenter: CORP-DC
  ├── Folder: PRODUCTION           → CORP\vsphere-prod-admins: Administrator
  │     ├── Folder: PROD-DATABASES → CORP\dba-team: Custom (power, console)
  │     └── Folder: PROD-APP       → CORP\app-team: Virtual Machine User
  ├── Folder: DR                   → CORP\vsphere-l3: Administrator
  └── Folder: DEV-TEST             → CORP\devops: Administrator
                                     (limited blast radius — no prod access)
```

### Pattern 3 — Restricting VM Configuration Changes

Grant power operations without allowing configuration changes:

```powershell
# Custom role: allow power ops + console, deny all config changes
$powerOnly = New-VIRole -Name "Power-Only" `
  -Privilege (Get-VIPrivilege -Id `
    VirtualMachine.Interact.PowerOn,
    VirtualMachine.Interact.PowerOff,
    VirtualMachine.Interact.Reset,
    VirtualMachine.Interact.Suspend,
    VirtualMachine.Interact.ConsoleInteract,
    VirtualMachine.State.CreateSnapshot,
    VirtualMachine.State.RemoveSnapshot,
    VirtualMachine.State.RevertToSnapshot,
    Global.CancelTask,
    System.Anonymous,
    System.Read,
    System.View)
```

---

## Auditing and Compliance

### Event Log — Permission Changes

All permission changes are logged in the vCenter events database:

```bash
# PowerCLI — find recent permission change events
Get-VIEvent -MaxSamples 1000 -Type UserLoginSessionEvent, `
  UserLogoutSessionEvent, PermissionAddedEvent, `
  PermissionRemovedEvent, PermissionUpdatedEvent | `
  Where-Object {$_.CreatedTime -gt (Get-Date).AddDays(-7)} | `
  Select-Object CreatedTime, UserName, FullFormattedMessage | `
  Sort-Object CreatedTime -Descending
```

### Quarterly Permission Audit Checklist

```text
[ ] No individual user accounts with Administrator role (must be AD groups)
[ ] administrator@vsphere.local has no non-emergency active sessions
[ ] All service accounts have minimum required privileges documented
[ ] Solution user certificates expire > 60 days out
[ ] No permissions set directly on VMs (must be on folders)
[ ] Global permissions list reviewed — no unexpected principals
[ ] Identity sources use LDAPS (not plain LDAP)
[ ] SSO lockout policy is enabled (max failures ≤ 5)
[ ] vCenter SSL certificate expires > 90 days out
[ ] Inactive user accounts (no login > 90 days) removed from vsphere.local
```

---

## Quick Reference — Key Facts

| Topic | Key fact |
|---|---|
| SSO default domain | `vsphere.local` |
| Break-glass account | `administrator@vsphere.local` — never for daily use |
| Permission resolution | Most specific object wins; `No Access` always wins |
| Inheritance blocking method | Assign `No Access` role on the target object |
| Global permission storage | SSO directory (not vCenter DB) |
| Solution user auth method | X.509 certificates |
| Default certificate lifetime | 2 years (VMCA-signed) |
| Propagate default | Must be explicitly set; not propagated by default |
| Best scope for permissions | Folder or higher — never individual VM |
| AD group vs user account | Always AD groups for operational accounts |

---

## Related Pages

- [vSphere Security — Encryption, Identity, and VM Hardening](../vsphere-security/)
- [Cluster Services — DRS, HA, and vSAN](../cluster-services/)
- [vSphere Lifecycle Management](../vsphere-lifecycle/)
