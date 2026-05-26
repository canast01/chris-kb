# Veeam — Encryption

## Backup Encryption

Enable AES-256 encryption per backup job:

```powershell
# VBR console: Job Properties → Storage → Enable backup file encryption
# Enter encryption password — stored in VBR config DB
# Export encryption keys after creation: Main Menu → Manage Passwords → Export
```
```

### S3 Object Lock (SOBR Capacity Tier)

Configure Object Lock in `Compliance` mode:
- VBR console → SOBR → Capacity Tier → Enable immutability
- Set immutability period = retention period + 10 days buffer
- Compliance mode: even bucket owner cannot delete during immutability period
