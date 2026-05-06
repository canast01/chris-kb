# Dell CloudIQ Security

## Authentication

CloudIQ uses Dell account-based authentication for portal access. Accounts are managed at [https://myaccount.dell.com](https://myaccount.dell.com).

- **SSO/Federation**: CloudIQ supports identity federation via Azure AD and Okta. Configure federation under **Settings > Identity Provider** in the CloudIQ admin console. With federation enabled, users authenticate via your corporate IdP and CloudIQ accepts the SAML assertion.
- **MFA**: Enforce multi-factor authentication on all Dell accounts that have access to CloudIQ. For federated accounts, MFA enforcement is managed by your IdP. For non-federated Dell accounts, enable MFA in **My Dell Account** settings.
- **Session management**: CloudIQ sessions have a fixed idle timeout; users are required to re-authenticate after inactivity.

## RBAC

CloudIQ provides role-based access control to limit what each user can view and modify.

| Role | Permissions |
|---|---|
| CloudIQ Admin | Full access: manage users, roles, notification rules, API credentials, and all system data |
| System Admin | Manage and view assigned systems; cannot manage users or global settings |
| Viewer | Read-only access to dashboards, health scores, capacity, and alerts; cannot modify settings or acknowledge alerts |

Assign roles under **Settings > Users**. Apply the principle of least privilege — most operational users should be Viewer or System Admin; CloudIQ Admin should be restricted to a small number of named individuals.

## API Security

API client credentials (client ID and client secret) provide programmatic access with the same permissions as the user account that created them.

Best practices:

- **Rotate client secrets every 90 days**. Create the new credential before deleting the old one to avoid automation downtime.
- **Store secrets in a vault**: use CyberArk, HashiCorp Vault, AWS Secrets Manager, or equivalent. Never store client secrets in plaintext configuration files, scripts, or version control.
- **Use separate credentials per integration**: create one client credential per integration (Splunk, Grafana, ServiceNow, etc.) so that a compromised credential can be revoked without affecting other integrations.
- **Scope by use case**: access tokens derived from client credentials inherit the role of the creating account. Create API accounts with the minimum required role (typically Viewer for monitoring integrations).
- **Monitor credential usage**: review the CloudIQ audit log for API calls made with each credential to detect unusual access patterns.

## Data Security

| Layer | Protection |
|---|---|
| Telemetry in transit (SCG to Dell) | TLS 1.2 or higher; certificate-pinned connection from SCG to Dell SRS endpoint |
| Telemetry at rest (Dell cloud) | Encrypted at rest in Dell's cloud infrastructure |
| Portal access | HTTPS (TLS 1.2+); sessions protected by Dell's cloud infrastructure |
| Data content | Telemetry contains configuration metadata and performance statistics only — no user data, file contents, or host data is transmitted |

CloudIQ telemetry does not include: file names, directory paths, user credentials, application data, or any content stored on the managed arrays.

## Audit Log

CloudIQ logs all user actions and API calls in a tamper-evident audit log. Access the audit log under **Admin > Audit Log** in the CloudIQ portal.

Audit events include:

- User logins and logouts (including source IP)
- Changes to notification rules, user roles, and API credentials
- API calls made by integration accounts
- System registration and deregistration events

The audit log can be filtered by date, user, and event type and exported as CSV for SIEM ingestion. Integrate with your SIEM (Splunk, Microsoft Sentinel, etc.) by periodically exporting the audit log via the CloudIQ API or by configuring a scheduled export.

Retain audit log exports for a minimum of 90 days in accordance with your organisation's security policy.
