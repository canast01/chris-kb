# Horizon — Access Control


<div class="kb-summary">
Access Control reference covering Pool-Level Admin Delegation, Desktop Pool Entitlements, App Volumes Permission Model, UAG Access Control, Service Account for vCenter and 1 more sections.
</div>

  RBAC: AD Groups → Entitlements → Pools
```text
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
┌─────────────────────────────────── VMware Horizon — Access Control ───────────────────────────────────┐
│                                                                                                       │
│  Horizon access control uses AD groups for pool entitlements, Horizon admin roles                     │
│  for management, and UAG for external session access control.                                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Admin Roles                  │  │              Pool Entitlements              │   │
│   │         Administrators: full control         │  │          Entitle: AD user or group          │   │
│   │          Local role: per pod scope           │  │             Per-pool entitlement            │   │
│   │          Custom roles: limited ops           │  │           Global entitlement: CPA           │   │
│   │           Read-only: helpdesk role           │  │             No direct VM access             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Entitlements control who gets a desktop; admin roles control who manages Horizon.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              UAG Access Control              │  │              Audit & Compliance             │   │
│   │         Allowlist: source IP filter          │  │          Events DB: log all logins          │   │
│   │        Authentication: MFA via RADIUS        │  │            Horizon reports: usage           │   │
│   │             SAML: forward to CS              │  │          Review: admin roles qtrly          │   │
│   │         DMZ rules: only 443 inbound          │  │            Alert: login failures            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  UAG sits in DMZ with firewall rules; internal network only allows CS management;                     │
│  desktop VLAN isolated from management network.                                                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Entitlement    = AD user/group assigned to pool; grants access                                       │
│  Admin role     = Horizon admin privilege set; applied to AD group                                    │
│  Custom role    = restricted admin role; e.g., helpdesk only                                          │
│  Global entitlement= Cloud Pod Architecture; cross-pod pool access                                    │
│  CPA            = Cloud Pod Architecture; multi-site/pod federation                                   │
│  UAG allowlist  = IP source filtering on external UAG                                                 │
│  RADIUS         = MFA backend; UAG proxies auth before CS                                             │
│  SAML           = UAG passes assertion to Connection Server                                           │
│  Events DB      = SQL DB; Horizon audit log; login/logoff events                                      │
│  Read-only role = view sessions and machines; no changes                                              │
│  DMZ firewall   = only port 443 inbound to UAG from internet                                          │
│  Qtrly review   = audit Horizon admin role assignments                                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

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
