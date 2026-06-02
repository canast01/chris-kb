# APEX Storage as a Service — Access Control


<div class="kb-summary">
Access Control reference covering APEX Console RBAC Roles, API Token Management, SSO and SAML Integration, SCG Access Controls, General Controls.
</div>

```
┌────────────────────────────────── Dell Apex STaaS — Access Control ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Apex access control: RBAC roles, SSO, API tokens, IP allowlists, Dell support         │   │
│   │       Three portal roles: Account Admin, Storage Admin, Reader; assign via Apex Console       │   │
│   │          API access: OAuth 2.0 tokens scoped to read or read-write; rotate quarterly          │   │
│   │        IP allowlist: restrict Apex Console access to corporate IP ranges or VPN egress        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSO login → RBAC role check → console or API access → action logged → audit reviewed               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Portal Roles        │  │          API Access         │  │         Restrictions        │   │
│   │        Account Admin        │  │       OAuth 2.0 token       │  │         IP allowlist        │   │
│   │        Storage Admin        │  │         Scoped r/rw         │  │         MFA enforce         │   │
│   │            Reader           │  │        Token rotation       │  │         SSO required        │   │
│   │       Least privilege       │  │        API audit log        │  │       Dell break-glass      │   │
│   │       Review quarterly      │  │         Revoke stale        │  │      Customer approves      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Review user list quarterly; revoke inactive accounts and rotate API tokens                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Role       │      Can do      │     Cannot do     │    Assign via    │      Notes       │   │
│   │    Acct Admin    │  Users/billing   │    Storage ops    │   Apex Console   │  Separate duty   │   │
│   │  Storage Admin   │    Vols/snaps    │   Billing/users   │   Apex Console   │    Day-2 ops     │   │
│   │      Reader      │   View metrics   │     Any change    │   Apex Console   │  Audit/reports   │   │
│   │    API token     │    Automation    │    Portal login   │     Apex API     │  Rotate 90 days  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: corporate IdP reachable by Apex Console · VPN for IP allowlist enforcement               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Account Admin  = Top-level Apex Console role; manages subscriptions, billing, and users            │
│    Storage Admin  = Day-to-day storage ops; cannot modify billing or create users                     │
│    Reader         = View-only; suitable for monitoring, auditing, and management review               │
│    Least privilege = Assign minimum role required for job function; review access regularly           │
│    OAuth 2.0      = Token issued by Apex for API clients; set shortest practical expiry               │
│    Token rotation = Replace API tokens quarterly; revoke old token immediately after                  │
│    IP allowlist   = Apex Console setting to permit logins from specified IP ranges only               │
│    MFA enforce    = Require second factor for all console logins; hardware or TOTP                    │
│    Break-glass    = Dell emergency access; customer must grant in Apex Console; audited               │
│    Separation     = Account Admin and Storage Admin roles should be different people                  │
│    Stale tokens   = API tokens from departed staff or unused integrations; revoke promptly            │
│    Quarterly review = Check all active users and API tokens; remove unneeded access                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [APEX Storage as a Service](../../index.md) reference.

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
