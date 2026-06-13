---
tags:
  - operations
  - python
---
# Python Automation — Health Checks


<div class="kb-summary">
Health Checks reference covering Environment Health, Package Management, Scheduled Scripts.
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

```bash
# 1. Python version
python3 --version && pip3 --version

# 2. Virtual environment status
ls -la ~/.venv/ 2>/dev/null || echo "No default venv"

# 3. Installed packages — key automation libraries
pip3 list | grep -E "requests|boto3|azure|vmware|ansible|paramiko"

# 4. Dependency conflicts
pip3 check

# 5. Script syntax check (sample)
python3 -m py_compile <script.py> && echo "OK"

# 6. Cron / scheduled script health — verify expected jobs present
crontab -l | grep python
```
```text
┌─────────────────────────────────────── Python — Health Checks ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Python health checks: verify interpreter version, venv, dependency currency, test pass rate  │   │
│   │      CI pipeline is the primary health gate: ruff + mypy + bandit + pytest must all pass      │   │
│   │             Dependency audit: pip list --outdated; safety check; monthly CVE scan             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Environment Checks              │  │                Quality Checks               │   │
│   │          python3 --version (>=3.11)          │  │           pytest (all tests pass)           │   │
│   │             pip list --outdated              │  │          ruff check . (zero errors)         │   │
│   │           safety check (CVE scan)            │  │           mypy src/ (zero errors)           │   │
│   │           python -c "import <lib>"           │  │          bandit -r src/ (zero high)         │   │
│   │         Check .python-version match          │  │            Coverage report >= 80%           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   safety check   = queries PyPI advisory database; reports known CVEs in installed packages   │   │
│   │    .python-version= pyenv file; records required Python version; auto-activates with pyenv    │   │
│   │        Dependabot     = GitHub service; auto-creates PRs to update dependencies weekly        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Check pyenv version (if using pyenv)**

```bash
pyenv version
cat .python-version
```

The `.python-version` file records the required Python version for the project. `pyenv` activates it automatically when entering the directory.

**Verify virtual environment is active**

```bash
echo $VIRTUAL_ENV
python3 -c "import sys; print(sys.prefix)"
```

If `VIRTUAL_ENV` is empty, activate the venv before running scripts:

```bash
source /opt/automation/venv/bin/activate
```

**Check for environment variable completeness**

```bash
python3 -c "import os; print([k for k in ['API_URL','API_TOKEN','LOG_DIR'] if k not in os.environ])"
```

Replace the list with the environment variables your scripts require.

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Python version | Matches `.python-version` or runbook spec | Install correct version via pyenv or package manager |
| Virtual environment | Active and matches project | Recreate venv if dependencies are mismatched |
| `sys.prefix` | Points to project venv | Deactivate global pip installs; use venv |
| Required env vars | All present | Set missing variables in systemd unit or cron environment |

---

## Package Management

Package version drift causes subtle breakage when an upstream library changes its API. Conflicts between installed packages can cause import failures that only surface at runtime.

**List installed packages**

```bash
pip3 list
pip3 list --outdated
```

**Check for dependency conflicts**

```bash
pip3 check
```

Any output from `pip3 check` indicates a broken dependency graph that must be resolved.

**Audit for known CVEs**

```bash
pip3 install safety
safety check
```

**Export current dependencies (freeze)**

```bash
pip3 freeze > requirements-$(date +%Y%m%d).txt
```

**Install from pinned requirements**

```bash
pip3 install -r requirements.txt
```

**Verify a specific critical library is importable**

```bash
python3 -c "import requests; print(requests.__version__)"
python3 -c "import boto3; print(boto3.__version__)"
python3 -c "import paramiko; print(paramiko.__version__)"
```

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| `pip3 check` output | Empty (no conflicts) | Resolve conflicts by adjusting pinned versions |
| CVE scan | Zero known vulnerabilities | Upgrade affected packages |
| Outdated packages | None critical | Schedule controlled upgrades |
| `requirements.txt` present | Yes, committed to VCS | Freeze and commit current state |

---

## Scheduled Scripts

Python automation scripts commonly run on a schedule via cron or systemd timers. Silent failures in scheduled scripts are a frequent source of undetected automation gaps.

**List all cron jobs running Python scripts**

```bash
crontab -l | grep python
```

**Check system-wide cron for Python jobs**

```bash
grep -r "python" /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/ /etc/cron.weekly/ 2>/dev/null
```

**Check cron daemon is running**

```bash
systemctl status cron
# or on RHEL/CentOS:
systemctl status crond
```

**Review recent cron execution log**

```bash
grep CRON /var/log/syslog | tail -50
# or on RHEL/CentOS:
grep CRON /var/log/cron | tail -50
```

**Check systemd timer units (alternative to cron)**

```bash
systemctl list-timers --all | grep python
```

**Verify script output log (if scripts redirect output)**

```bash
# Example: check last run time and exit status from a log file
tail -20 /var/log/automation/<script-name>.log
```

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Expected cron entries present | All jobs in `crontab -l` | Re-add missing entries |
| Cron daemon status | `active (running)` | Restart and investigate stop reason |
| Last run time | Within expected schedule interval | Check for silent failures in log |
| Script exit code in log | `0` | Debug with manual run; check tracebacks |
| Log file growth | Normal, not zero-length | Confirm output redirection in cron entry |

---

## Python Automation Health Check Flow
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
