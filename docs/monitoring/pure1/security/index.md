# Pure1 Security

Pure1 access is controlled via role-based user accounts managed in the Pure1 console, with SSO integration available via SAML 2.0 and SCIM provisioning from enterprise IdPs. API keys are scoped to service accounts and must be rotated on the team's standard annual schedule. Telemetry is read-only from the array's perspective — Pure1 does not write configuration back to arrays.

| Control | Detail |
|---|---|
| User roles | Admin, Read-only |
| SSO | SAML 2.0 / SCIM with enterprise IdP (Okta, Azure AD) |
| API key rotation | Annual rotation; stored in secrets manager |
| Audit log | Admin actions logged in Pure1 audit trail |
| Array write-back | None — telemetry is read-only; Pure1 cannot modify array config |
| Data isolation | Telemetry scoped per customer tenant in Pure cloud |
