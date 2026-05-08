# Veeam — Encryption

## Backup Encryption

Enable AES-256 encryption per backup job:

```powershell
# VBR console: Job Properties → Storage → Enable backup file encryption
# Enter encryption password — stored in VBR config DB
# Export encryption keys after creation: Main Menu → Manage Passwords → Export
```

**Key management is critical**: loss of the encryption key = unrecoverable backup data.
Store exported keys in CyberArk or an offline safe, separate from the VBR server.

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
