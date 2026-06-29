---
tags:
  - aria-networks
  - security
  - vmware
---
# Aria Operations for Networks — Access Control

<div class="kb-summary">
Access Control reference covering Built-in Roles, LDAP / Active Directory Integration, Local User Management, API Token Management, Network-Level Access Control and 3 more sections.

*Applies to: Aria Networks 6.x*
</div>
![Aria Operations for Networks — Access Control](../../../../assets/virtualization-vmware-aria-operations-for-networks-security-.svg)

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

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


```text title="Expected output"
{
  "vcenters": [
    {
      "id": "vcenter-1",
      "name": "vc-prod-01.example.local",
      "ip_address": "192.168.1.45",
      "version": "7.0.3",
      "status": "CONNECTED",
      "last_seen": "2024-01-15T14:32:18Z"
    },
    {
      "id": "vcenter-2",
      "name": "vc-dr-01.example.local",
      "ip_address": "192.168.2.50",
      "version": "6.7.0",
      "status": "CONNECTED",
      "last_seen": "2024-01-15T14:31:45Z"
    }
  ],
  "total_count": 2
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag (already present) or import the CA certificate into your system trust store with `curl -cacert /path/to/ca.pem`.
    **`{"error": "Unauthorized", "message": "Invalid or expired token"}`** — Regenerate the API token in Aria Operations for Networks UI and ensure it's passed correctly in the Authorization header.
    **`curl: (7) Failed to connect to vrni.example.local port 443: Connection refused`** — Verify the VRNI appliance hostname/IP is correct and the management interface is accessible on port 443 using `ping` and `telnet vrni.example.local 443`.
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

## See also

- [Aria Operations for Networks — Authentication](../authentication/)
- [vRNI Security Hardening](../hardening/)
