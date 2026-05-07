# Veeam Security
## Role-Based Access Control

Veeam has five built-in roles — assign via AD groups, not individual users:

| Role | Capabilities |
|---|---|
| Veeam Backup Administrator | Full VBR administration — assign sparingly |
| Veeam Backup Operator | Start/stop jobs, perform restores; no configuration changes |
| Veeam Restore Operator | Restore data only — no backup job management |
| Veeam Backup Viewer | Read-only — view jobs, reports, and configuration |
| Veeam Tape Operator | Tape library and vault management |

Configure: VBR console → Users and Roles → Add.

## Immutable Backups

Protect against ransomware by making backup files immutable:

### Linux Hardened Repository

```bash
# Verify immutability is active on backup files
# (Veeam sets this automatically via chattr on the repository)
lsattr /mnt/backup/ | head -20
# Look for 'i' flag: ----i----------- ./backup.vbk

# The VBR service account must be non-root on the hardened repo
# VBR connects with a limited account; root SSH login should be disabled
grep PermitRootLogin /etc/ssh/sshd_config   # Must show: no
```

### S3 Object Lock (SOBR Capacity Tier)

Configure Object Lock in `Compliance` mode:
- VBR console → SOBR → Capacity Tier → Enable immutability
- Set immutability period = retention period + 10 days buffer
- Compliance mode: even bucket owner cannot delete during immutability period

## Backup Encryption

Enable AES-256 encryption per backup job:

```powershell
# VBR console: Job Properties → Storage → Enable backup file encryption
# Enter encryption password — stored in VBR config DB
# Export encryption keys after creation: Main Menu → Manage Passwords → Export
```

**Key management is critical**: loss of the encryption key = unrecoverable backup data.
Store exported keys in CyberArk or an offline safe, separate from the VBR server.

## CyberArk Integration

VBR can retrieve infrastructure credentials from CyberArk at runtime:

1. VBR console → Credentials → Add → CyberArk
2. Configure CCP (Central Credential Provider) URL, application ID, and safe name
3. Credentials retrieved at job runtime — never stored in VBR config DB

## Multi-Factor Authentication

For Veeam Backup Enterprise Manager (if deployed):
- Enable MFA under Settings → Users → configure TOTP or SAML provider
- Require MFA for all administrative accounts

## Audit Log

```powershell
# Audit log location on Windows VBR server
Get-Content "C:\ProgramData\Veeam\Backup\Audit.log" | Select-String "Login|Modify|Delete"

# Review monthly and on any security incident
```

Forward to SIEM using a log forwarder (Filebeat, Splunk UF) on the VBR server. Alert on:
- Failed login attempts
- Job deletion or modification outside maintenance windows
- Encryption key management operations

## Network Security

| Port | Purpose | Restriction |
|---|---|---|
| 9392/TCP | VBR console communication | Restrict to admin management subnets |
| 2500–3300/TCP | Data transfer (proxy) | Open between proxies and repositories only |
| 443/TCP | vCenter API | VBR to vCenter |
| 6160/TCP | Veeam Installer Service | Between VBR server and managed components |

## Security Hardening Checklist

- [ ] RBAC configured with AD groups — no shared admin logins
- [ ] Encryption enabled on all jobs writing to cloud or off-site targets
- [ ] Linux hardened repository deployed for immutable local backups
- [ ] S3 Object Lock in Compliance mode for cloud capacity tier
- [ ] Encryption keys exported and stored in CyberArk/offline vault
- [ ] VBR console port (9392) restricted to admin subnets via firewall
- [ ] CyberArk integration active for infrastructure credentials
- [ ] Audit log forwarded to SIEM; alerts configured
- [ ] Veeam ONE alert for any backup job failing > 2 consecutive times
