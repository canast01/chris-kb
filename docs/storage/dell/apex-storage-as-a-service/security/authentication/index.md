# APEX Storage as a Service — Authentication

> Part of the [APEX Storage as a Service](../../) reference.

---

- **APEX Console**: Dell account-based authentication with optional SSO/federation via Azure AD or Okta configured under Console Settings
- **APEX REST API**: OAuth2 client credentials (client ID + client secret) generated in APEX Console → Settings → API Keys; access tokens valid for 3600 seconds
- **Underlying platforms**: PowerStore/PowerScale/PowerFlex management authentication is separate and follows each platform's local or LDAP configuration
