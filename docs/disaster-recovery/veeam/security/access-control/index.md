# Veeam — Access Control

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
