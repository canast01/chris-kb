# Horizon — Access Control

```text
  RBAC: AD Groups → Entitlements → Pools
┌──────────────┐    ┌───────────────────┐    ┌─────────────────────┐
│ AD Groups    │    │ Horizon Roles      │    │ Desktop Pools /     │
│              │    │                   │    │ Access Groups        │
│ CORP\Horizon─┼───►│ Administrators    │    │                     │
│ -Admins      │    │ (full config)     │    │ ┌─────────────────┐  │
│              │    ├───────────────────┤    │ │ Pool-Win10-Float│  │
│ CORP\Horizon─┼───►│ Help Desk Admin   │    │ │   entitlements  │  │
│ -HelpDesk    │    │ (session mgmt)    │    │ │                 │  │
│              │    ├───────────────────┤    │ │ VDI-LON-KW-     │  │
│ CORP\Horizon─┼───►│ Inventory Admin   │───►│ │ W11-IC-Users    │  │
│ -Pool-Admins │    │ (scoped to group) │    │ └─────────────────┘  │
└──────────────┘    └───────────────────┘    └─────────────────────┘
```

---

## Horizon Admin Roles

| Role | Capabilities |
|---|---|
| Administrators | Full admin access — all configuration and operations |
| Administrators (Read Only) | View all configuration — no changes |
| Help Desk Administrators | Session management, force logoff, reset desktop |
| Inventory Administrators | Manage pools, entitlements, but not global settings |
| Local Application Administrators | Manage published applications only |

---

## Assign Roles to AD Groups

```text
Horizon Console → Settings → Administrators → Add Permission
  Add User or Group: select AD user or group
  Role: select appropriate role
  Access Group: select resource scope (All, or specific pool group)
  → OK
```

Recommended mapping:
| AD Group | Horizon Role |
|---|---|
| `CORP\Horizon-Admins` | Administrators |
| `CORP\Horizon-HelpDesk` | Help Desk Administrators |
| `CORP\Horizon-ReadOnly` | Administrators (Read Only) |

---

## Pool-Level Admin Delegation

Horizon supports scoping admin permissions to specific pools via Access Groups:

```text
Horizon Console → Settings → Administrators → Access Groups → Create Group
  Name: Pool-Win10-Admins
  Assign pools: select specific desktop pools

Settings → Administrators → Add Permission
  Group: CORP\Horizon-Pool-Win10-Admins → Role: Inventory Administrators
  Access Group: Pool-Win10-Admins
```

This limits the admin to only the pools in the assigned Access Group.

---

## Desktop Pool Entitlements

Control which users can access which pool:

```text
Horizon Console → Inventory → Desktops → [pool] → Entitlements
  Add: CORP\Horizon-Pool-Win10 (AD security group)
  Remove users or groups who should no longer have access
```

---

## App Volumes Permission Model

App Volumes AppStacks are assigned to:
- AD Users
- AD Groups (preferred)
- OUs
- Computers

```yaml
App Volumes Manager → AppStacks → [AppStack] → Assignments
  Add Assignment
    Type: Group
    Name: CORP\AppStack-AdobeReader
    Delivery: On Login
```

Writable volumes (user data disks) are assigned per-user or per-group with storage quotas.

---

## UAG Access Control

Restrict external UAG access by source IP (if applicable):

```text
UAG Admin UI (port 9443) → Advanced Settings → Source IP Rules
  Allow: <corporate VPN IP range>
  Deny: All other
```

DMZ firewall rules:
- Internet → UAG: TCP 443, TCP 8443 (Blast), TCP/UDP 4172 (PCoIP)
- UAG → Connection Server: TCP 443 only
- UAG → desktop VMs: TCP/UDP required for tunneled traffic (if tunnel is configured)

---

## Service Account for vCenter

Horizon Connection Server connects to vCenter with a dedicated service account:

```yaml
vCenter → Administration → Global Permissions → Add
  User: svc-horizon-vc@corp.local
  Role: Horizon Administrator (custom role with required privileges)
  Propagate: Yes
```

Required vCenter privileges for Horizon service account: documented in VMware Horizon documentation — covers virtual machine operations, datastore access, and folder management for the pools.

---

## Audit Log Access

```text
Horizon Console → Monitor → Events
  Filter by: Administrator, type: Configuration Change
```

For long-term audit storage, configure an Events database (SQL Server) during Connection Server setup. The embedded H2 database retains only limited history.
