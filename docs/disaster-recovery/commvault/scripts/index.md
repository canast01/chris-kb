# CommVault Scripts

CommVault automation scripts use a combination of the `q*` CLI toolkit and the CommVault REST API. Python is the preferred language for REST API integrations; Bash wraps `q*` commands for simpler operational tasks. All scripts should authenticate using a dedicated service account and retrieve credentials from CyberArk at runtime.

| Script | Language | Purpose |
|---|---|---|
| `cv_job_status_report.py` | Python (REST API) | Queries last 24 hours of job history; generates pass/fail summary and emails it |
| `cv_failed_job_alert.py` | Python (REST API) | Polls for failed jobs and creates incidents in ServiceNow |
| `cv_storage_usage.sh` | Bash (`qlist`) | Reports storage policy capacity used vs allocated; alerts at 80% threshold |
| `cv_sla_compliance.py` | Python (REST API) | Checks SLA report for all clients; flags any below threshold |
| `cv_restore_validation.py` | Python (REST API) | Triggers a restore of a test file from each critical subclient; validates file integrity |

**REST API authentication pattern (Python)**

```python
import requests
session = requests.Session()
resp = session.post(
    "https://<CommServe>/webconsole/api/Login",
    json={"username": "svc-cv-api", "password": "<from_vault>"},
    headers={"Accept": "application/json"}
)
token = resp.json()["token"]
session.headers.update({"Authtoken": token})
```
