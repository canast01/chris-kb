# CommVault Troubleshooting

CommVault job failures are classified by error code and phase. The first diagnostic step is to open the job detail in the Job Controller and expand the phase-level log — this shows the specific module and error code. Client logs reside on the client under `C:\Program Files\CommVault\ContentStore\Log Files\` (Windows) or `/var/log/commvault/Log_Files/` (Linux). CommServe logs are at the same path on the CommServe host.

| Symptom | Likely Cause | Remediation |
|---|---|---|
| Job fails: network error (phase: backup) | MediaAgent cannot reach client on port 8400 | Check firewall rules; confirm client service is running (`cvd` daemon) |
| Job fails: DDB is offline | DDB disk full or corrupted | Check DDB disk space; run DDB verification; restore DDB from backup if corrupted |
| CommServe SQL errors | SQL Server disk full or SQL service issue | Check SQL Server disk; review SQL Server error log; free space or expand volume |
| Client authentication failure | Certificate mismatch or firewall blocking 8403 | Re-register client certificate; check `cvd` and `cvfwd` ports |
| MediaAgent offline | Service stopped or network issue | Restart CommVault services on MediaAgent; check `CVMA` service status |
| Auxiliary copy stuck | Source copy not pruned or tape library busy | Check tape drive availability; verify source data is not in use |
| DDB corruption | Unexpected shutdown during write | Run `qoperation execscript -sn QS_DDBVerify`; escalate if phase 2 fails |

**Key log locations**

- CommServe: `C:\Program Files\CommVault\ContentStore\Log Files\CommServeDB.log`
- MediaAgent: `C:\Program Files\CommVault\ContentStore\Log Files\CVMA.log`
- Client (Windows): `C:\Program Files\CommVault\ContentStore\Log Files\clBackup.log`
