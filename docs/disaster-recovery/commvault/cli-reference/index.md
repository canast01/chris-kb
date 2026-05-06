# CommVault CLI Reference

CommVault provides the `qcommand` CLI toolkit (installed with CommServe and MediaAgent) and a REST API for automation. The `q*` commands connect to the CommServe using the current OS credentials or an explicit login. The REST API base URL is `https://<CommServeHostname>/webconsole/api/` and requires token-based authentication (obtained via `POST /Login`).

| Command | Purpose | Example |
|---|---|---|
| `qlogin` | Authenticate to CommServe | `qlogin -cs <CommServe> -u admin` |
| `qlist jobs` | List recent jobs | `qlist jobs -d 1` (last 1 day) |
| `qoperation backup` | Run backup | `qoperation backup -subclient <name> -backuptype full` |
| `qoperation restore` | Run restore | `qoperation restore -subclient <name> -totime <time>` |
| `qmodify subclient` | Modify subclient | `qmodify subclient -subclient <name> -sp <storagepolicy>` |
| `qdelete job` | Kill a job | `qdelete job -j <jobid>` |
| `qsystem dbbackup` | Trigger CommServe DB backup | `qsystem dbbackup` |
| `qcommit` | Commit configuration changes | `qcommit` |
| `qlist client` | List clients | `qlist client` |
| `qlist storagepolicy` | List storage policies | `qlist storagepolicy` |
| `qlist ddb` | List deduplication databases | `qlist ddb` |
| `qoperation execscript` | Run a script on CommServe | `qoperation execscript -sn QS_CheckReadiness` |
