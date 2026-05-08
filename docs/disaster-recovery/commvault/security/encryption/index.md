# Commvault — Encryption

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
