# CloudIQ Security

<div class="kb-summary">
CloudIQ Security reference covering Access Control (RBAC), SSO Configuration, SCG Certificate Security, Audit Logging, Data Residency and Privacy and 1 more sections.
</div>

## Access Control (RBAC)

CloudIQ uses role-based access control managed in the CloudIQ portal. Assign the minimum required role to each user.

| Role | Capabilities |
|---|---|
| Admin | Full access: configuration, notifications, user management, API client management |
| Viewer | Read-only access to health scores, capacity, alerts, and system data |

User management: **CloudIQ portal > Settings > User Management**

Principle of least privilege: operations staff monitoring dashboards should be assigned the Viewer role. Admin access should be limited to designated platform administrators.

## SSO Configuration

CloudIQ supports SAML 2.0 SSO integration with enterprise IdPs (Okta, Azure AD, ADFS).

```text
┌───────────────────────────────────────── CloudIQ — Security ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Access Control                │  │                Data Security                │   │
│   │              Dell account + MFA              │  │             TLS 1.2+ in transit             │   │
│   │              RBAC: Admin/Viewer              │  │              Encrypted at rest              │   │
│   │             Service account only             │  │           No config pushed to arr           │   │
│   │             Annual access review             │  │           Telemetry only — no data          │   │
│   │             Audit log in CloudIQ             │  │             Dell SOC2 compliant             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Data stored in Dell cloud datacentres · customer data isolated per tenant · SOC2 Type II             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Dell account MFA = Multi-factor authentication required for cloudiq.dell.com login                   │
│  RBAC = Role-Based Access Control; Admin (full) vs Viewer (read-only) roles                           │
│  Service account = Non-personal account for API access; password rotated per policy                   │
│  Telemetry only = CloudIQ receives metrics and events; does not access user data or files             │
│  No config push = CloudIQ is monitoring-only; it cannot change array configuration                    │
│  TLS 1.2 = Minimum transport encryption for all CloudIQ connections                                   │
│  Encrypted at rest = Telemetry data encrypted in Dell cloud storage                                   │
│  SOC2 Type II = Dell security audit certification; covers data handling and access controls           │
│  Audit log = Record of logins and configuration changes viewable in CloudIQ admin section             │
│  Tenant isolation = Each customer organisation data separated in multi-tenant cloud                   │
│  Annual review = Yearly audit of CloudIQ users; remove stale accounts and inappropriate roles         │
│  API token security = client_id/secret treated as password; never logged or committed to code         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
For internal arrays with self-signed certificates, add them to the SCG trust store:
```text
SCG admin UI > Security > Trusted Certificates > Add Certificate
```

## Audit Logging

CloudIQ logs all administrative actions in an audit trail accessible from the portal.

```text
CloudIQ portal > Settings > Audit Log
- Filter by user, date range, or action type
- Export to CSV for SIEM ingestion
```

Key events to monitor:
- User login/logout (especially failed logins)
- API client creation and secret rotation
- Notification rule changes
- System add/remove events

Audit logs should be exported monthly and forwarded to the SIEM for long-term retention.

## Data Residency and Privacy

Telemetry is processed and stored in Dell's cloud infrastructure.

| Consideration | Detail |
|---|---|
| Data type | Performance metrics, capacity data, hardware health — no customer workload data |
| Residency | Dell cloud (confirm region with Dell for GDPR/data sovereignty requirements) |
| Retention | Dell retains telemetry per their data retention policy — review Dell's privacy policy |
| SCG data at rest | SCG stores a local telemetry buffer — ensure the SCG VM disk is on an encrypted datastore |

## Security Hardening Checklist

- [ ] SSO enabled; local accounts disabled for non-break-glass users
- [ ] API clients scoped to minimum required permissions
- [ ] API secrets stored in secrets manager, not in plain text configs
- [ ] SCG management UI access restricted to ops management subnet (firewall rules)
- [ ] SCG VM disk on encrypted datastore
- [ ] NTP configured on SCG
- [ ] Audit log exported to SIEM monthly
- [ ] API secrets rotated on annual schedule; rotation dates logged
