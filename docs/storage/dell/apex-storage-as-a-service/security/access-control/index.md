# APEX Storage as a Service — Access Control

> Part of the [APEX Storage as a Service](../../) reference.

---

## APEX Console RBAC Roles

| Role | Capabilities | Recommended Use |
|---|---|---|
| **Account Admin** | Full subscription management, user provisioning, service request creation, billing access | One or two named storage leads per account |
| **Storage Admin** | Manage storage resources, view and acknowledge alerts, access performance and capacity dashboards | Day-to-day storage operations team |
| **Viewer** | Read-only access to dashboards, capacity reports, consumption data, and health summaries | Capacity monitoring automation, finance teams, auditors |

Assign the Viewer role to all non-operational accounts including monitoring integrations. Elevated roles should be assigned to named individuals only — avoid shared or generic accounts.

## API Token Management

| Control | Detail |
|---|---|
| **One service account per integration** | Create a dedicated APEX API service account for each consuming system (monitoring, automation, chargeback reporting). Never share credentials between integrations or teams. |
| **Minimum role assignment** | Bind each service account to the Viewer role unless the integration explicitly requires write operations. Document and justify any service account with Storage Admin or Account Admin rights. |
| **Token lifecycle** | APEX API tokens are short-lived OAuth 2.0 bearer tokens. Integrations must implement the client credentials flow to refresh tokens automatically. Do not cache tokens beyond their expiry. |
| **Client secret rotation** | Rotate API client secrets every 90 days. Store client IDs and secrets in a secrets vault (HashiCorp Vault, AWS Secrets Manager, CyberArk, or equivalent). Never store credentials in source code, config files, or CI/CD environment variables in plaintext. |
| **Revocation on staff change** | Revoke API credentials for service accounts tied to a departing team member's ownership immediately upon offboarding. Reassign ownership documentation to the team. |

## SSO and SAML Integration

APEX Console supports federated authentication via SAML 2.0. When SSO is configured:

| Control | Detail |
|---|---|
| **Identity provider integration** | Configure the APEX Console as a SAML service provider in your IdP (Okta, Azure AD, Ping Identity, etc.). Map IdP groups to APEX Console roles using attribute-based role assignment. |
| **MFA enforcement** | MFA is enforced at the IdP level when SSO is active. Ensure your IdP policy requires MFA for all users accessing APEX. |
| **Local account fallback** | Disable or restrict local (non-SSO) accounts after SSO is configured. Maintain one break-glass local admin account with a complex password stored in the vault, for use only when SSO is unavailable. |
| **Session timeout** | Configure idle session timeout at the IdP to a maximum of 8 hours. APEX Console does not independently manage session lifetime when SSO is active. |

## SCG Access Controls

| Control | Detail |
|---|---|
| **Local admin password** | Change the SCG appliance default admin password at deployment. Rotate on a 90-day cycle aligned with other privileged credentials. |
| **Network access restriction** | Restrict SCG management interface access to the storage management VLAN. The SCG does not require inbound connections from the internet — deny all inbound at the perimeter. |
| **Gateway audit log** | Review SCG and CloudIQ gateway event logs monthly for unexpected registration, deregistration, or failed connectivity events. |

## General Controls

- Audit APEX Console user access quarterly. Remove accounts for personnel who have left or changed roles.
- Enforce MFA for all human user accounts, either via SSO policy or the APEX Console's built-in MFA setting.
- Do not use shared or team-named accounts for APEX Console access — all access should be attributable to a named individual.
- Log and alert on Account Admin role assignment changes.
