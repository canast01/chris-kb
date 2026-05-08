# Veeam — Authentication

## Multi-Factor Authentication

For Veeam Backup Enterprise Manager (if deployed):
- Enable MFA under Settings → Users → configure TOTP or SAML provider
- Require MFA for all administrative accounts

## CyberArk Integration

VBR can retrieve infrastructure credentials from CyberArk at runtime:

1. VBR console → Credentials → Add → CyberArk
2. Configure CCP (Central Credential Provider) URL, application ID, and safe name
3. Credentials retrieved at job runtime — never stored in VBR config DB
