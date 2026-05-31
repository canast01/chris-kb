# Commvault — Authentication

```text
┌─────────────────────────── Commvault Authentication — Methods and Controls ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Local Authentication      │    AD/LDAP Authentication   │            SAML/SSO            │   │
│   │     CommCell local user DB     │    Bind to AD via LDAP/S    │    SAML 2.0 IdP (ADFS/Okta)    │   │
│   │  Password: 12+ chars complex   │  Kerberos or NTLM fallback  │      SP metadata exchange      │   │
│   │     90-day rotation policy     │     Group sync on login     │        JIT provisioning        │   │
│   │       MFA: TOTP per user       │   Domain join not required  │       Attribute mapping        │   │
│   │     Session timeout 30 min     │     LDAP port 389 / 636     │      Session: 8h default       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Recommendation: integrate AD/LDAP for user lifecycle; enforce MFA for all admins                   │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                       Certificate-Based Authentication (Component Auth)                       │   │
│   │          All CommCell components (CS, MA, client) authenticate with TLS certificates          │   │
│   │            Internal CA (CommServe CA): issues certs automatically at agent install            │   │
│   │               Certificate renewal: automatic 30 days before expiry via CommServe              │   │
│   │             Custom CA: enterprise PKI certs supported; import via CommCell Console            │   │
│   │              CRL/OCSP: revocation check supported for enterprise PKI integration              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AD/LDAP: CommServe needs port 389 (LDAP) or 636 (LDAPS) to domain controller                         │
│  MFA: TOTP secrets stored encrypted in CSDB; no external radius server needed                         │
│  PKI: if using enterprise CA, CommServe must reach CRL/OCSP distribution point                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SAML 2.0       = XML-based SSO standard; Commvault acts as SP; IdP: Okta/ADFS/Ping                   │
│  TOTP           = Time-based One-Time Password (RFC 6238); Google Auth/Microsoft Auth                 │
│  Kerberos       = Windows domain auth protocol used when AD integration is configured                 │
│  JIT Provision  = Just-in-time user creation in CommCell on first SAML login                          │
│  CommServe CA   = Built-in certificate authority issuing component TLS certificates                   │
│  CRL            = Certificate Revocation List; checked to validate cert not revoked                   │
│  OCSP           = Online Certificate Status Protocol; real-time cert revocation check                 │
│  Session Timeout= Idle session limit; default 30 min; configurable per security policy                │
│  LDAP Bind      = CommServe connects to AD using a service account for user searches                  │
│  Attribute Map  = Mapping SAML attributes (email, groups) to CommCell user properties                 │
│  MFA Bypass     = Per-user MFA exception (e.g. service accounts); must be documented                  │
│  PKI            = Public Key Infrastructure; enterprise CA managing component certs                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Two-Factor Authentication

Enable 2FA for Command Center:
- Manage → Security → Identity Providers → configure SAML or TOTP
- Require MFA for all admin-level accounts
- Exempt automated service accounts (use dedicated service account with IP restriction instead)

## CyberArk Integration

CommVault supports CyberArk Central Credential Provider (CCP) for runtime password retrieval:

1. Command Center: Manage → Security → Credential Manager
2. Add credential → select CyberArk CCP as vault type
3. Configure: CCP URL, app ID, safe name, object name

Service account passwords never stored in CommVault config — retrieved from CyberArk at job runtime.
---

## Related Reference

- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
