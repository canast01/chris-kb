# Commvault — Authentication

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
