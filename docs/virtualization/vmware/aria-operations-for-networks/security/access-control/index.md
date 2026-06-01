# Aria Operations for Networks — Access Control


<div class="kb-summary">
Access Control reference covering Built-in Roles, LDAP / Active Directory Integration, Local User Management, API Token Management, Network-Level Access Control and 3 more sections.
</div>

---

## Built-in Roles

| Role | Capabilities | Typical User |
|---|---|---|
| Super Admin | Full access — configuration, users, data sources, all data | Platform admin |
| Network Engineer | View flows, topology, search, alerts — no configuration | Network ops |
| Security Engineer | View flows + microsegmentation recommendations + push to NSX | Security ops |
| Auditor | Read-only — all data, no configuration changes | Compliance |
| Member | Basic search and flow queries | Tier-1 support |

---

## LDAP / Active Directory Integration

```text
Settings → Authentication → LDAP → Configure

  Server URL:     ldaps://dc01.example.local:636
  Base DN:        DC=corp,DC=local
  Bind DN:        CN=svc-vrni,OU=ServiceAccounts,DC=corp,DC=local
  Bind Password:  <service account password>
  User Attribute: sAMAccountName
  Group Attribute: memberOf
  Test Connection → "Connection successful"
```
```powershell
┌───────────────────────────────────────── vRNI Access Control ─────────────────────────────────────────┐
│                                                                                                       │
│  Admin and Member roles, LDAP group mapping, and access control for vRNI.                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Built-in Roles                │  │               Role Permissions              │   │
│   │          Administrator: full access          │  │         Admin: add/edit data sources        │   │
│   │           Member: read-only viewer           │  │            Admin: user management           │   │
│   │           No custom roles in vRNI            │  │           Member: view flows/maps           │   │
│   │         Least privilege: use Member          │  │             Member: run searches            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Two roles only; LDAP groups map to Admin or Member; vIDM SSO extends this.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              LDAP Group Mapping              │  │              API Access Control             │   │
│   │          Settings > Authentication           │  │         API tokens tied to user role        │   │
│   │          Map AD group to Admin role          │  │          Token inherits user perms          │   │
│   │         Map AD group to Member role          │  │          No separate API-only role          │   │
│   │            Test LDAP bind on save            │  │          Rotate tokens periodically         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM; AD/LDAP directory; vIDM optional SSO; network access to LDAP port                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Administrator Role   = Full vRNI access: data sources, users, settings, all queries                  │
│  Member Role          = Read-only: view flows, maps, dashboards; no config changes                    │
│  LDAP Group Mapping   = AD security group assigned to Admin or Member role in vRNI                    │
│  vIDM SSO             = VMware Identity Manager federated login; maps vIDM groups                     │
│  API Token            = Bearer token for REST API; inherits the generating user role                  │
│  Least Privilege      = Grant Member role by default; Admin only for operators                        │
│  LDAP Bind Account    = Service account vRNI uses to query the directory for groups                   │
│  Local Account        = Admin account created during OVA deploy; backup if LDAP fails                 │
│  Group DN             = Distinguished Name of the AD group used in LDAP mapping                       │
│  Token Rotation       = Periodically invalidate and reissue API tokens for security                   │
│  Authentication Test  = vRNI built-in LDAP test button; validates bind and group DN                   │
│  Audit Log            = Records user login, config changes, and data source edits                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

Disable unused local accounts:
```text
Settings → Users → [user] → Deactivate
```

---

## API Token Management

Tokens authenticate REST API clients without using user credentials:

```yaml
Settings → API Tokens → Generate Token
  Name:   <descriptive name>
  Role:   <minimum required role>
  Expiry: <explicit date — set a reminder to rotate>
```

Revoke tokens when no longer needed:
```text
Settings → API Tokens → [token] → Revoke
```

API usage:
```bash
curl -sk -H "Authorization: NetworkInsight <token>" \
  "https://vrni.example.local/api/ni/data-sources/vcenters"
```

---

## Network-Level Access Control

Firewall rules required for vRNI components:

| Source | Destination | Port | Protocol | Purpose |
|---|---|---|---|---|
| Admin workstations | Platform VM | 443 | TCP | UI / API |
| Collector VM | vCenter | 443 | TCP | Inventory polling |
| Collector VM | NSX Manager | 443 | TCP | Topology polling |
| Physical switches | Collector VM | 2055 | UDP | NetFlow / IPFIX |
| Platform VM | Collector VM | 443 | TCP | Collector management |
| Collector VM | Platform VM | 443 | TCP | Data upload |
| Platform VM | LDAP server | 636 | TCP | AD authentication (LDAPS) |

Restrict Platform VM port 443 to management VLAN only — deny direct access from production VLANs.

---

## vCenter Service Account (Minimum Privilege)

```text
vCenter → Administration → Global Permissions → Add Permission
  User: svc-vrni-vc@corp.local
  Role: Read Only
  Propagate to children: Yes
```

---

## NSX-T Service Account (Minimum Privilege)

```text
NSX-T Manager → System → User Management → Add User
  Username: svc-vrni-nsx
  Role: Auditor (read-only)
```

Never use NSX admin credentials — vRNI only reads topology. A separate account with NSX security group write access is needed only if you push microsegmentation recommendations back to NSX.

---

## Audit Logging

All admin actions are logged. Access via:
```text
Settings → Audit Logs
```

Forward to SIEM via syslog (Settings → Notifications → Syslog). Alert on:
- Failed login attempts
- Role mapping changes
- Data source deletion
- API token creation / revocation
