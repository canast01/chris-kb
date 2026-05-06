# Dell AIOps Security

Dell AIOps access control inherits from CloudIQ RBAC, with Admin and Viewer roles assignable to users via the CloudIQ portal. SSO via CloudIQ supports integration with enterprise identity providers (SAML 2.0). All actions taken on recommendations are logged in the CloudIQ audit trail, which should be reviewed periodically for unauthorised access or unexpected changes. Storage telemetry is processed entirely in Dell's cloud infrastructure — confirm data residency and sovereignty requirements are met for regulated environments. API client credentials (OAuth2) should be rotated regularly and scoped to minimum required permissions.

| Role | Capabilities |
|---|---|
| Admin | Full access to recommendations, configuration, and user management |
| Viewer | Read-only access to recommendations, anomalies, and health data |

- Authentication: SSO via CloudIQ (SAML 2.0 supported)
- Audit log: available in CloudIQ portal; export for SIEM retention
- Data sovereignty: telemetry processed in Dell cloud — review for regulated data
- API credentials: OAuth2 client credentials; rotate every 90 days
- RBAC: assign minimum required role (prefer Viewer for read-only operational users)
