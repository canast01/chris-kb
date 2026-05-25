# FOD — Authentication

```text
┌────────────────────────────────────── Dell FoD — Authentication ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       FoD authentication: secure access to Dell portal, array management, and key vault       │   │
│   │         Dell portal: Dell SSO with MFA (TOTP or hardware key); tied to support account        │   │
│   │    Array GUI: local accounts or LDAP/AD integration; Storage Admin role for license import    │   │
│   │      Vault: LDAP or AppRole auth with MFA token; short-lived lease; audit log per access      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Dell portal MFA → download key → vault MFA store → array LDAP auth → import license                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Portal Auth         │  │          Array Auth         │  │          Vault Auth         │   │
│   │           Dell SSO          │  │        Local accounts       │  │         LDAP method         │   │
│   │           TOTP MFA          │  │          LDAP / AD          │  │        AppRole method       │   │
│   │         Hardware key        │  │         SSH key auth        │  │       Short TTL lease       │   │
│   │       Session timeout       │  │       Password policy       │  │         MFA wrapper         │   │
│   │         IP allowlist        │  │       Account lockout       │  │          Access log         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All three systems require individual named accounts; no service accounts for FoD apply             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      System      │      Method      │        MFA        │   Session TTL    │     Lockout      │   │
│   │   Dell portal    │     Dell SSO     │    TOTP/HW key    │   30 min idle    │    5 attempts    │   │
│   │    Array GUI     │    LDAP/local    │   N/A (LDAP MFA)  │   60 min idle    │    5 attempts    │   │
│   │      Vault       │   LDAP/AppRole   │   TOTP required   │   Lease TTL 1h   │   N/A (lease)    │   │
│   │    Array CLI     │     SSH key      │        N/A        │   Session only   │    5 attempts    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: auth tokens never stored on shared systems; personal TOTP app or hardware key only       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dell SSO      = Dell identity provider for support.dell.com and licensing.dell.com                 │
│    TOTP MFA      = Time-based One-Time Password; Google/Microsoft Authenticator app                   │
│    Hardware key  = YubiKey or similar FIDO2 key; strongest MFA option for portal access               │
│    LDAP auth     = Array authenticates engineers via Active Directory; groups control roles           │
│    AppRole       = HashiCorp Vault machine auth method; used by automation scripts                    │
│    Short TTL     = Vault lease expires in 1 hour; engineer must re-auth to retrieve another key       │
│    MFA wrapper   = Vault LDAP auth combined with TOTP second factor; both required                    │
│    SSH key auth  = Array CLI accessed via SSH keypair only; disable password SSH on all arrays        │
│    Password policy = Array local accounts: 12+ chars, complexity, 90-day rotation                     │
│    Account lockout = 5 failed attempts locks account; admin or LDAP reset required                    │
│    IP allowlist  = Dell portal access restricted to corporate egress IP; home access blocked          │
│    Session timeout = Portal and array GUI auto-logout after idle period; re-auth required             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Flex on Demand](../../index.md) reference.

---

FOD metering access is managed through the underlying array management interfaces (Unisphere for PowerMax, PowerStore Manager) and the Dell APEX Console. Authentication follows the same model as those platforms.

- **Unisphere**: local accounts or LDAP/AD integration. Use a dedicated read-only service account for FOD capacity monitoring automation.
- **APEX Console**: Dell account-based authentication with optional SSO/federation via Azure AD or Okta.
- **CloudIQ API**: OAuth2 client credentials for programmatic access to metered usage data.
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
