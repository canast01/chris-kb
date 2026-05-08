# NetBackup — Encryption

## Backup Data Encryption

Enable encryption at the policy level:

```bash
# Create an encryption key file
nbkm -createKey -keyGroupName backupkeys

# Enable encryption in policy (Admin Console):
# Policy Attributes → Use Encryption → select key group
```

| Encryption Mode | Location | CPU Impact |
|---|---|---|
| Client-side | Client host | High (on production server) |
| Media server-side | Media server | Low (off client) |
| Storage-level | Array/appliance | None (hardware) |

Mandate client-side or media-server-side encryption for all policies covering PII or regulated data.
