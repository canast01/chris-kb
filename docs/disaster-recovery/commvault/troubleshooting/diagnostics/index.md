# Commvault — Diagnostics

## Log Locations

Client logs reside on the client under `C:\Program Files\CommVault\ContentStore\Log Files\` (Windows) or `/var/log/commvault/Log_Files/` (Linux). CommServe logs are at the same path on the CommServe host.

- CommServe: `C:\Program Files\CommVault\ContentStore\Log Files\CommServeDB.log`
- MediaAgent: `C:\Program Files\CommVault\ContentStore\Log Files\CVMA.log`
- Client (Windows): `C:\Program Files\CommVault\ContentStore\Log Files\clBackup.log`

## Diagnostic Commands

```bash
# Check DDB status and space
qlist ddb

# Check client connectivity readiness
qoperation execscript -sn QS_CheckReadiness

# Run DDB verification
qoperation execscript -sn QS_DDBVerify

# Check CommServe services
qlist services

# View audit log
qoperation execscript -sn GetAuditLog -si starttime=<timestamp>
```

## Support Bundle Collection

Before opening a support case, collect the support bundle on the CommServe:

```bash
# On CommServe (run as administrator)
qsystem log export -path C:\cv_support_bundle

# Alternatively via Command Center:
# Settings > Support > Generate Support Bundle
```
