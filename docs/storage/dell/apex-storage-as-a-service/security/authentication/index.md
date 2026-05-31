# APEX Storage as a Service — Authentication

```text
┌────────────────────────────────── Dell Apex STaaS — Authentication ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Apex authentication: SSO/SAML for portal, CHAP for iSCSI, Kerberos for NFS          │   │
│   │          Portal: SSO via SAML 2.0 (Okta, Azure AD, AD FS); MFA required for all users         │   │
│   │         iSCSI: CHAP mutual authentication per initiator; secret stored in Apex Console        │   │
│   │         NFS: Kerberos (sec=krb5) recommended; AUTH_SYS (IP-based) as minimum baseline         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    User → SSO IdP → SAML assertion → Apex Console → RBAC role → storage operation                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Portal Auth         │  │         Storage Auth        │  │           API Auth          │   │
│   │         SAML 2.0 SSO        │  │          iSCSI CHAP         │  │          OAuth 2.0          │   │
│   │        MFA (TOTP/HW)        │  │         NFS Kerberos        │  │         Bearer token        │   │
│   │         Local admin         │  │         FC port sec.        │  │          HTTPS only         │   │
│   │       Session timeout       │  │        Auth_SYS (min)       │  │         Token expiry        │   │
│   │         Audit login         │  │        Initiator IQN        │  │          Rotate 90d         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Always enable CHAP for iSCSI; avoid AUTH_SYS for sensitive NFS shares                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Method      │     Protocol     │       Scope       │   Config path    │      Notes       │   │
│   │     SAML SSO     │     SAML 2.0     │    Portal users   │     Apex>SSO     │   IdP metadata   │   │
│   │       MFA        │    TOTP/FIDO2    │     All users     │  Apex>Security   │    Mandatory     │   │
│   │       CHAP       │    iSCSI CHAP    │     Each host     │    Apex>Hosts    │  Bidirectional   │   │
│   │    OAuth 2.0     │   Bearer token   │    API clients    │  Apex>API keys   │  90-day rotate   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: corporate IdP (Okta/AD FS) · KDC for Kerberos NFS · NTP sync required                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SAML 2.0       = Security Assertion Markup Language; IdP issues signed assertions to Apex          │
│    SSO            = Single Sign-On; user logs in once via IdP; Apex accepts SAML token                │
│    MFA            = Multi-Factor Authentication; TOTP app or hardware key (FIDO2)                     │
│    Local admin    = Fallback Apex account; used only if SSO is unavailable                            │
│    CHAP           = Challenge Handshake; iSCSI host sends hashed secret to authenticate               │
│    Bidirectional CHAP = Both host and array authenticate each other; strongest iSCSI auth             │
│    NFS Kerberos   = sec=krb5 mount option; requires KDC, keytab on NFS client host                    │
│    AUTH_SYS       = NFS trust by UID/GID; no real auth; avoid for sensitive data                      │
│    FC port sec.   = FC switch restricts which pWWNs can login; configured on switch                   │
│    OAuth 2.0      = REST API authentication; scoped bearer token; HTTPS transport only                │
│    Session timeout = Apex Console auto-logs out idle sessions; configure ≤15 min                      │
│    KDC            = Kerberos Key Distribution Centre; required for NFS Kerberos auth                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [APEX Storage as a Service](../../index.md) reference.

---

- **APEX Console**: Dell account-based authentication with optional SSO/federation via Azure AD or Okta configured under Console Settings
- **APEX REST API**: OAuth2 client credentials (client ID + client secret) generated in APEX Console → Settings → API Keys; access tokens valid for 3600 seconds
- **Underlying platforms**: PowerStore/PowerScale/PowerFlex management authentication is separate and follows each platform's local or LDAP configuration
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
