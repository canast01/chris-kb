# FOD — Access Control


<div class="kb-summary">
Access Control reference covering APEX Console RBAC Roles, API Service Account Configuration, SCG Access Controls, CloudIQ User Roles, General Controls.
</div>

```
┌────────────────────────────────────── Dell FoD — Access Control ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FoD access control: who can purchase keys, download files, apply licenses, and audit     │   │
│   │      Portal access: only named storage leads with MFA-enabled Dell accounts can purchase      │   │
│   │         Array access: only Storage Admin role can import license keys; Operator cannot        │   │
│   │        Vault access: only named engineers can retrieve .lic files; access is MFA-gated        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Purchase (storage lead) → vault store → retrieve (named eng.) → apply (admin role) → logged        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Portal Access        │  │         Array Access        │  │         Vault Access        │   │
│   │       Named leads only      │  │       Admin role only       │  │       Named engineers       │   │
│   │         MFA enforced        │  │        LDAP/AD group        │  │         MFA required        │   │
│   │           Dell SSO          │  │        No shared acct       │  │          Access log         │   │
│   │        Account audit        │  │         CR pre-apply        │  │         Lease expiry        │   │
│   │         IP restrict         │  │       Quarterly review      │  │       Offboard revoke       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    On engineer offboarding: revoke Dell portal access, array RBAC, and vault lease immediately        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      System      │       Who        │    Auth Method    │   Review Freq    │      Owner       │   │
│   │   Dell portal    │  Storage leads   │   Dell SSO + MFA  │    Quarterly     │   Storage lead   │   │
│   │    Array GUI     │   Named admins   │    LDAP + RBAC    │    Quarterly     │   Storage lead   │   │
│   │      Vault       │ Named engineers  │     MFA token     │    Quarterly     │     Sec team     │   │
│   │       CMDB       │     Ops team     │    Service acct   │      Annual      │     Ops lead     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: array GUI RBAC enforced; no direct filesystem or iDRAC access needed for FoD apply       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Portal access  = Access to Dell Licensing Portal; limit to storage leads who handle purchasing     │
│    Admin role     = Array management role with license import rights; separate from Operator          │
│    LDAP group     = Array admin rights controlled via AD group; add/remove via directory              │
│    No shared acct = Each engineer has individual array admin account; shared accounts banned          │
│    CR pre-apply   = ITSM CR must be approved before any engineer retrieves key from vault             │
│    Vault lease    = HashiCorp Vault access token with TTL; expires and must be renewed                │
│    MFA required   = Both Dell portal and vault require MFA; prevents credential-only access           │
│    Account audit  = Quarterly review of Dell portal accounts; remove leavers and excess access        │
│    Quarterly review = Storage lead reviews who has array admin and vault access; remove if not needed │
│    Offboard revoke = Immediate removal from portal, LDAP group, and vault on engineer departure       │
│    IP restrict    = Dell portal can restrict login to corporate IP ranges; reduces phishing risk      │
│    Lease expiry   = Vault lease auto-expires; reduces risk of standing access to .lic files           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── Dell FoD — Access Control ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FoD access control: who can purchase keys, download files, apply licenses, and audit     │   │
│   │      Portal access: only named storage leads with MFA-enabled Dell accounts can purchase      │   │
│   │         Array access: only Storage Admin role can import license keys; Operator cannot        │   │
│   │        Vault access: only named engineers can retrieve .lic files; access is MFA-gated        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Purchase (storage lead) → vault store → retrieve (named eng.) → apply (admin role) → logged        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Portal Access        │  │         Array Access        │  │         Vault Access        │   │
│   │       Named leads only      │  │       Admin role only       │  │       Named engineers       │   │
│   │         MFA enforced        │  │        LDAP/AD group        │  │         MFA required        │   │
│   │           Dell SSO          │  │        No shared acct       │  │          Access log         │   │
│   │        Account audit        │  │         CR pre-apply        │  │         Lease expiry        │   │
│   │         IP restrict         │  │       Quarterly review      │  │       Offboard revoke       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    On engineer offboarding: revoke Dell portal access, array RBAC, and vault lease immediately        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      System      │       Who        │    Auth Method    │   Review Freq    │      Owner       │   │
│   │   Dell portal    │  Storage leads   │   Dell SSO + MFA  │    Quarterly     │   Storage lead   │   │
│   │    Array GUI     │   Named admins   │    LDAP + RBAC    │    Quarterly     │   Storage lead   │   │
│   │      Vault       │ Named engineers  │     MFA token     │    Quarterly     │     Sec team     │   │
│   │       CMDB       │     Ops team     │    Service acct   │      Annual      │     Ops lead     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: array GUI RBAC enforced; no direct filesystem or iDRAC access needed for FoD apply       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Portal access  = Access to Dell Licensing Portal; limit to storage leads who handle purchasing     │
│    Admin role     = Array management role with license import rights; separate from Operator          │
│    LDAP group     = Array admin rights controlled via AD group; add/remove via directory              │
│    No shared acct = Each engineer has individual array admin account; shared accounts banned          │
│    CR pre-apply   = ITSM CR must be approved before any engineer retrieves key from vault             │
│    Vault lease    = HashiCorp Vault access token with TTL; expires and must be renewed                │
│    MFA required   = Both Dell portal and vault require MFA; prevents credential-only access           │
│    Account audit  = Quarterly review of Dell portal accounts; remove leavers and excess access        │
│    Quarterly review = Storage lead reviews who has array admin and vault access; remove if not needed │
│    Offboard revoke = Immediate removal from portal, LDAP group, and vault on engineer departure       │
│    IP restrict    = Dell portal can restrict login to corporate IP ranges; reduces phishing risk      │
│    Lease expiry   = Vault lease auto-expires; reduces risk of standing access to .lic files           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Flex on Demand](../../index.md) reference.

---

## APEX Console RBAC Roles

| Role | Capabilities | Recommended Use |
|---|---|---|
| **Account Admin** | Full subscription management, user provisioning, raise and manage service requests | One or two named storage leads per account |
| **Storage Admin** | View and manage storage resources, view consumption dashboards, acknowledge alerts | Day-to-day storage operations team |
| **Viewer / Monitor** | Read-only access to dashboards, consumption reports, and capacity trends | Capacity monitoring automation accounts, finance teams, auditors |

Assign the Viewer role to any integration or service account that only needs to pull capacity metrics. Write-level access is not required for FOD reporting or chargeback automation.

## API Service Account Configuration

| Control | Detail |
|---|---|
| **One account per integration** | Create a dedicated APEX API service account for each consuming system (e.g., one for CloudIQ, one for chargeback scripts, one for monitoring tooling). Do not share credentials between integrations. |
| **Scope to minimum role** | Bind each service account to the Viewer role unless a specific integration requires write operations. Document any exception. |
| **Credential rotation** | Rotate API client secrets every 90 days. Store credentials in a secrets vault (HashiCorp Vault, AWS Secrets Manager, or equivalent) — never in source code or configuration files. |
| **Token lifetime** | APEX API access tokens are short-lived. Ensure integrations use the OAuth client credentials flow to refresh tokens automatically rather than caching a long-lived token. |

## SCG Access Controls

| Control | Detail |
|---|---|
| **Local admin accounts** | The SCG appliance has a local admin account used during initial registration. Change the default password at deployment and rotate it on the same schedule as other privileged credentials. |
| **Management network access** | Restrict SSH and the SCG management interface to the storage management VLAN. Block access from general-purpose server VLANs. |
| **No inbound connectivity required** | The SCG initiates all outbound connections to Dell's cloud. No inbound firewall rule from the internet to the SCG is needed or should be opened. |
| **Audit log access** | SCG activity is visible in CloudIQ under the gateway events log. Review this log monthly to confirm telemetry delivery and detect unexpected registration or deregistration events. |

## CloudIQ User Roles

| Role | Capabilities |
|---|---|
| **Admin** | Manage users, configure alert policies, view all objects across all registered arrays |
| **Operator** | Acknowledge and manage alerts, view all objects |
| **Read Only** | View dashboards, capacity reports, and health scores; cannot modify any configuration |

Apply the Read Only role to all non-operational accounts. Audit CloudIQ user membership quarterly and remove accounts for personnel who have changed roles or left the organisation.

## General Controls

- Restrict Unisphere access to named storage administrators; do not use shared admin credentials.
- Enforce MFA on the APEX Console for all human users — this is configurable under the account's identity settings.
- Review APEX Console user access quarterly and revoke stale accounts promptly.
