# FOD — Authentication

> Part of the [Flex on Demand](../../) reference.

---

FOD metering access is managed through the underlying array management interfaces (Unisphere for PowerMax, PowerStore Manager) and the Dell APEX Console. Authentication follows the same model as those platforms.

- **Unisphere**: local accounts or LDAP/AD integration. Use a dedicated read-only service account for FOD capacity monitoring automation.
- **APEX Console**: Dell account-based authentication with optional SSO/federation via Azure AD or Okta.
- **CloudIQ API**: OAuth2 client credentials for programmatic access to metered usage data.
