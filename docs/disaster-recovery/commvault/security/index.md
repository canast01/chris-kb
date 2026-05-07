# CommVault Security
## RBAC Roles

CommVault roles are assigned through User Groups scoped to specific Client Groups, Storage Policies, or Subclients:

| Role | Capabilities |
|---|---|
| Master | Full CommCell administration |
| Tenant Admin | Manage users and jobs within assigned tenant |
| Operator | Start/stop jobs; no configuration changes |
| End User | Self-service restore of own data only |
| View Only | Read-only — view jobs and configuration |

Assign roles in Command Center: Manage → Security → User Groups.

**Never share admin accounts** — create individual named accounts for each operator; map AD groups to CommVault roles.

## Backup Encryption

Configure per Storage Policy (Command Center: Storage → Storage Policies):

| Encryption Option | When to Use |
|---|---|
| Client-side (BlowFish/AES-256) | Maximum protection; CPU overhead on client |
| MediaAgent-side (AES-256) | Off-client encryption; no client CPU impact |
| Storage-level encryption | If storage supports hardware encryption (not CommVault-managed) |

Mandate for:
- [ ] Policies covering PII or regulated data → AES-256, MediaAgent-side minimum
- [ ] Cloud and off-site copy targets → always encrypted
- [ ] DDB encryption: enable for dedup pools storing sensitive workloads

## Linux Hardened Repository (Immutable Backups)

Protect against ransomware using immutability:

```bash
# On Linux hardened repository server
# CommVault sets immutable flag automatically via chattr +i
# Verify:
lsattr /path/to/backup/files | grep '\-i\-'
```

Configure via VBR Repository settings: enable "Immutable" with retention period matching recovery requirements.

## CyberArk Integration

CommVault supports CyberArk Central Credential Provider (CCP) for runtime password retrieval:

1. Command Center: Manage → Security → Credential Manager
2. Add credential → select CyberArk CCP as vault type
3. Configure: CCP URL, app ID, safe name, object name

Service account passwords never stored in CommVault config — retrieved from CyberArk at job runtime.

## Network Security

| Port | Purpose | Restriction |
|---|---|---|
| 8400/TCP | CommServe communication | Restrict to admin management subnets |
| 8403/TCP | MediaAgent data movement | Allow from client subnets to MediaAgent IPs only |
| 443/HTTPS | Command Center web UI | Restrict to admin subnets |

## Two-Factor Authentication

Enable 2FA for Command Center:
- Manage → Security → Identity Providers → configure SAML or TOTP
- Require MFA for all admin-level accounts
- Exempt automated service accounts (use dedicated service account with IP restriction instead)

## Audit Trail

```powershell
# View CommVault audit log
qoperation execscript -sn GetAuditLog -si starttime=<timestamp>
```

Forward audit logs to SIEM via syslog:
- Command Center: Manage → Alerts → configure syslog destination
- Alert on: admin account creation, policy modifications, job deletion, encryption key access

## Security Hardening Checklist

- [ ] RBAC configured — all users assigned to roles via AD groups
- [ ] No shared admin credentials
- [ ] Encryption enabled for all regulated data policies
- [ ] DDB encryption enabled
- [ ] 2FA enabled for Command Center
- [ ] CommServe management ports (8400, 8403) firewall-restricted
- [ ] CyberArk integration active for service account passwords
- [ ] Audit log forwarded to SIEM; alerts configured
- [ ] CommServe OS and SQL Server on supported, patched versions
