# CloudIQ Security
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
CloudIQ portal > Settings > Identity Providers > Add
- IdP Metadata URL or upload XML
- Attribute mapping:
  - email → CloudIQ username
  - role attribute → Admin or Viewer (via IdP group claim)
- Enable Just-in-Time (JIT) provisioning if supported
```

### API Token Rotation

```text
Rotation procedure (annual schedule):
1. CloudIQ portal > Settings > API Clients > [Client] > Rotate Secret
2. Update the new secret in the team secrets manager
3. Redeploy/restart all dependent scripts and integrations
4. Verify API calls return HTTP 200 after rotation
5. Log the rotation date and next due date in the credential register
```

## SCG Certificate Security

The SCG uses TLS certificates for:
- HTTPS communication to Dell cloud (uses Dell trusted root CA — pre-configured)
- HTTPS communication to array management interfaces

Ensure the SCG clock is NTP-synchronised to avoid certificate validation failures:

```text
SCG admin UI > System Settings > Date/Time > NTP Configuration
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
