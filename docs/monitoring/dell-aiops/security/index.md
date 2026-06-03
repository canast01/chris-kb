# Dell AIOps Security

<div class="kb-summary">
Dell AIOps Security reference covering Access Control (RBAC), SSO Integration, Audit Logging, Data Sovereignty, Network Security and 1 more sections.
</div>

## Access Control (RBAC)

Dell AIOps access control inherits from CloudIQ RBAC. Roles are assigned per user in the CloudIQ portal.

| Role | Capabilities |
|---|---|
| Admin | Full access: recommendations, configuration, notification rules, user management, API client management |
| Viewer | Read-only access to recommendations, anomalies, health data, and capacity trends |

User management: **CloudIQ portal > Settings > User Management**

Apply the principle of least privilege. Operations staff reviewing dashboards and recommendations should be Viewers. Admins should be limited to designated platform administrators.

## SSO Integration

Dell AIOps authentication is handled through CloudIQ SSO, which supports SAML 2.0 integration with enterprise IdPs.

```text
┌──────────────────────────────────────── Dell AIOps — Security ────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Access Control                │  │           Network & Data Security           │   │
│   │              Local admin + LDAP              │  │              TLS 1.2 all comms              │   │
│   │             RBAC: role per team              │  │                Mgmt VLAN only               │   │
│   │               Service accounts               │  │             Custom cert replace             │   │
│   │               MFA on admin UI                │  │              Audit log retained             │   │
│   │             Annual access review             │  │                Syslog to SIEM               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AIOps VMs on management cluster · data encrypted at rest · outbound only TCP 443                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RBAC = Role-Based Access Control; Admin/Operator/Viewer roles with different permissions             │
│  Service account = Non-personal credential for adapter authentication to infrastructure               │
│  MFA = Multi-factor authentication on AIOps admin UI; reduces credential theft risk                   │
│  Custom cert = CA-signed certificate replacing self-signed; applied to AIOps HTTPS                    │
│  Audit log = Record of logins, config changes, and alert actions in AIOps                             │
│  Syslog = Forwarding AIOps audit events to SIEM (Splunk, Elastic) for correlation                     │
│  Mgmt VLAN = AIOps on isolated management network; no direct access from user VLANs                   │
│  Data at rest = AIOps time-series DB and config encrypted on disk                                     │
│  Annual review = Yearly audit of AIOps user list; remove departed staff accounts                      │
│  Credential rotation = Changing adapter service account passwords per security policy                 │
│  TLS 1.2 = Minimum transport encryption for all AIOps connections                                     │
│  Least privilege = Adapter accounts have read-only access to infrastructure APIs                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── Dell AIOps — Security ────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Access Control                │  │           Network & Data Security           │   │
│   │              Local admin + LDAP              │  │              TLS 1.2 all comms              │   │
│   │             RBAC: role per team              │  │                Mgmt VLAN only               │   │
│   │               Service accounts               │  │             Custom cert replace             │   │
│   │               MFA on admin UI                │  │              Audit log retained             │   │
│   │             Annual access review             │  │                Syslog to SIEM               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AIOps VMs on management cluster · data encrypted at rest · outbound only TCP 443                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RBAC = Role-Based Access Control; Admin/Operator/Viewer roles with different permissions             │
│  Service account = Non-personal credential for adapter authentication to infrastructure               │
│  MFA = Multi-factor authentication on AIOps admin UI; reduces credential theft risk                   │
│  Custom cert = CA-signed certificate replacing self-signed; applied to AIOps HTTPS                    │
│  Audit log = Record of logins, config changes, and alert actions in AIOps                             │
│  Syslog = Forwarding AIOps audit events to SIEM (Splunk, Elastic) for correlation                     │
│  Mgmt VLAN = AIOps on isolated management network; no direct access from user VLANs                   │
│  Data at rest = AIOps time-series DB and config encrypted on disk                                     │
│  Annual review = Yearly audit of AIOps user list; remove departed staff accounts                      │
│  Credential rotation = Changing adapter service account passwords per security policy                 │
│  TLS 1.2 = Minimum transport encryption for all AIOps connections                                     │
│  Least privilege = Adapter accounts have read-only access to infrastructure APIs                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Key events to review in audit log:
- User login/logout (especially failed logins or logins from unexpected locations)
- API client creation, modification, and secret rotation
- Notification rule changes
- Recommendation acknowledgement and dismissal

**Retention**: Export audit logs monthly to SIEM for long-term retention beyond CloudIQ's on-platform retention window.

## Data Sovereignty

AIOps telemetry is processed entirely in Dell's cloud infrastructure.

| Consideration | Detail |
|---|---|
| Data type | Storage performance metrics, capacity data, hardware health — not customer data or PII |
| Processing location | Dell cloud (confirm EU region for GDPR compliance if required) |
| Retention in Dell cloud | Per Dell's data retention policy — review Dell's privacy documentation |
| Local SCG buffer | SCG stores a short-term telemetry buffer on disk — ensure SCG VM disk is on an encrypted datastore |

## Network Security

| Control | Implementation |
|---|---|
| SCG egress | TCP 443 outbound only to Dell cloud endpoints; no inbound rules required |
| SCG management UI access | Restrict to ops management subnet via firewall rule (TCP 9443) |
| Array credentials on SCG | Use dedicated read-only service accounts per array; store in SCG credential store |

## Security Hardening Checklist

- [ ] SSO enabled; local accounts disabled for non-break-glass users
- [ ] Admin role limited to designated platform administrators
- [ ] API clients scoped to minimum required permissions
- [ ] API secrets stored in secrets manager; not in scripts or repos
- [ ] API secret rotation on 90-day schedule; rotation dates tracked
- [ ] SCG management UI access restricted to ops subnet
- [ ] SCG VM disk on encrypted datastore
- [ ] NTP configured on SCG (prevents certificate validation failures)
- [ ] Audit log exported to SIEM monthly
- [ ] Annual review of user accounts — remove stale accounts
