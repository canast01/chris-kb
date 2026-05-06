# CloudIQ Security

CloudIQ access is controlled via user roles managed in the CloudIQ console, with SSO via SAML for enterprise identity integration. API client secrets are scoped to service accounts and rotated on the team's standard schedule. Telemetry is processed in Dell's cloud infrastructure, and the SCG certificate must be maintained to ensure encrypted telemetry transport.

| Control | Detail |
|---|---|
| User roles | Admin, Viewer |
| SSO | SAML 2.0 with enterprise IdP |
| API client secret rotation | Every 12 months; stored in secrets manager |
| SCG certificate | Must be current and trusted for encrypted telemetry |
| Audit log | Admin actions logged in CloudIQ audit trail |
| Data sovereignty | Telemetry processed in Dell cloud (check region if required) |
