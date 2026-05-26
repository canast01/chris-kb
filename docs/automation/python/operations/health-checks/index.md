# Python Automation — Health Checks

## Python Automation Health Check Flow

```mermaid
flowchart TD
    start["Start Health Check"] --> checkPython["python3 --version\nExpected version?"]
    checkPython -->|OK| checkVenv["venv intact?\npip check passes?"]
    checkPython -->|Fail| alertPython["Alert: Python version\nmismatch or missing"]
    checkVenv -->|OK| checkImports["Critical packages\nimportable?"]
    checkVenv -->|Fail| alertVenv["Alert: Recreate venv\npip install -r requirements.txt"]
    checkImports -->|OK| checkAPI["Target APIs\nreachable?"]
    checkImports -->|Fail| alertImport["Alert: pip install\nmissing package"]
    checkAPI -->|OK| checkLogs["Error lines in\nrecent logs?"]
    checkAPI -->|Fail| alertAPI["Alert: Network /\nAPI endpoint issue"]
    checkLogs -->|None| healthy["Status: HEALTHY"]
    checkLogs -->|Errors found| alertLogs["Alert: Review\nlog file errors"]
```
```

## Incident Triage

**On alert or issue:**
1. Identify the failing script and the last successful run time — check cron logs (`grep CRON /var/log/syslog`) and script log files
2. Reproduce the failure manually in a test shell to get the full traceback:
   ```bash
   source /opt/automation/venv/bin/activate
   python3 /opt/automation/scripts/failing_script.py 2>&1 | tee /tmp/debug_run.log
   ```
3. Check the error type in the traceback to determine the root cause category
4. Apply the appropriate fix from the triage table below
5. After fixing, run the script manually once and confirm successful output before re-enabling the cron job

| Symptom | Likely Cause | Action |
|---|---|---|
| `ModuleNotFoundError: No module named 'X'` | Package not installed in active venv | `source /opt/automation/venv/bin/activate && pip install <package>` |
| `401 Unauthorized` from API call | Expired or revoked API token | Regenerate token in the target system's API settings, update token in config/secrets store |
| `ConnectionError` or `requests.exceptions.Timeout` | Target API unreachable or network timeout | Confirm API endpoint from automation host: `curl -v <api_url>`; check firewall and proxy settings |
| `JSONDecodeError` or `KeyError` in response parsing | API response format changed | Compare current response against expected schema, update parsing logic, check API changelog |
| `PermissionError` writing output file | File permissions or path issue | Check output directory permissions: `ls -la /path/to/output/`, fix with `chmod` or `chown` |
| Script ran but produced empty or unexpected output | Logic error or upstream data change | Add debug logging and re-run manually; compare against last known good output |
| Cron job not running at all | Cron daemon not running or syntax error in crontab | Check `systemctl status cron`; validate crontab with `crontab -l`; check `/var/log/syslog` for cron errors |
