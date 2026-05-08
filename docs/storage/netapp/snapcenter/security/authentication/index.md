# SnapCenter — Authentication

> Part of the [SnapCenter Security](../) reference.

---

## Authentication

- SnapCenter GUI and API use local accounts or Active Directory accounts
- Multi-factor authentication (MFA): SnapCenter 6.0+ supports MFA via SAML 2.0 integration with an IdP (AD FS, Okta, Azure AD)
- Service accounts used for ONTAP connections should use dedicated accounts with minimum ONTAP RBAC permissions — not personal admin accounts
- Plugin hosts use OS-level credentials for agent communication; store credentials in SnapCenter Credential Store (Settings → Credentials), not in plaintext scripts
