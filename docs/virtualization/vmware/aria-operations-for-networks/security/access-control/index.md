# Aria Operations for Networks — Access Control

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

```
Settings → Authentication → LDAP → Configure

  Server URL:     ldaps://dc01.corp.local:636
  Base DN:        DC=corp,DC=local
  Bind DN:        CN=svc-vrni,OU=ServiceAccounts,DC=corp,DC=local
  Bind Password:  <service account password>
  User Attribute: sAMAccountName
  Group Attribute: memberOf
  Test Connection → "Connection successful"
```

Map AD groups to roles:

```
Settings → Authentication → Role Mappings → Add Mapping

  CN=vRNI-Admins,OU=Groups,DC=corp,DC=local → Super Admin
  CN=vRNI-NetOps,OU=Groups,DC=corp,DC=local → Network Engineer
  CN=vRNI-SecOps,OU=Groups,DC=corp,DC=local → Security Engineer
  CN=vRNI-Audit,OU=Groups,DC=corp,DC=local  → Auditor
```

---

## Local User Management

Local users are managed via UI only (Settings → Users → Add User). The built-in `admin@local` account cannot be deleted.

Change default admin password immediately after deployment:
```
Settings → My Account → Change Password
```

Disable unused local accounts:
```
Settings → Users → [user] → Deactivate
```

---

## API Token Management

Tokens authenticate REST API clients without using user credentials:

```
Settings → API Tokens → Generate Token
  Name:   <descriptive name>
  Role:   <minimum required role>
  Expiry: <explicit date — set a reminder to rotate>
```

Revoke tokens when no longer needed:
```
Settings → API Tokens → [token] → Revoke
```

API usage:
```bash
curl -sk -H "Authorization: NetworkInsight <token>" \
  "https://vrni.corp.local/api/ni/data-sources/vcenters"
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

```
vCenter → Administration → Global Permissions → Add Permission
  User: svc-vrni-vc@corp.local
  Role: Read Only
  Propagate to children: Yes
```

---

## NSX-T Service Account (Minimum Privilege)

```
NSX-T Manager → System → User Management → Add User
  Username: svc-vrni-nsx
  Role: Auditor (read-only)
```

Never use NSX admin credentials — vRNI only reads topology. A separate account with NSX security group write access is needed only if you push microsegmentation recommendations back to NSX.

---

## Audit Logging

All admin actions are logged. Access via:
```
Settings → Audit Logs
```

Forward to SIEM via syslog (Settings → Notifications → Syslog). Alert on:
- Failed login attempts
- Role mapping changes
- Data source deletion
- API token creation / revocation
