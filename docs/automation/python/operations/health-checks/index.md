---
tags:
  - operations
  - python
---
# Python Automation — Health Checks

<div class="kb-summary">
Health Checks reference covering Environment Health, Package Management, Scheduled Scripts.

*Applies to: Python 3.x*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
package_management: "Package Management" {shape: rectangle}
scheduled_scripts: "Scheduled Scripts" {shape: rectangle}
python_automation_health_check_flow: "Python Automation Health Check Flow" {shape: rectangle}
incident_triage: "Incident Triage" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> package_management
package_management -> scheduled_scripts
scheduled_scripts -> python_automation_health_check_flow
python_automation_health_check_flow -> incident_triage
incident_triage -> verify
verify -> generate_report
```

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


```text title="Expected output"
Python 3.11.7
pip 23.3.1 from /usr/local/lib/python3.11/site-packages/pip (python 3.11)
total 48
drwxr-xr-x  6 admin admin  4096 Jan 15 10:22 .venv
drwxr-xr-x 18 admin admin  4096 Jan 15 09:45 ..
-rw-r--r--  1 admin admin   102 Jan 15 10:22 pyvenv.cfg
drwxr-xr-x  3 admin admin  4096 Jan 15 10:22 bin
drwxr-xr-x  2 admin admin  4096 Jan 15 10:22 include
drwxr-xr-x  3 admin admin  4096 Jan 15 10:22 lib
requests                      2.31.0
boto3                         1.28.45
azure-common                  1.1.28
vmware-vsphere-automation-sdk 1.82.1
ansible                       2.10.17
paramiko                       3.3.1
No broken requirements found.
OK
0 2 * * * /usr/local/bin/python3 /opt/scripts/health_check.py >> /var/log/health_check.log 2>&1
30 * * * * /usr/local/bin/python3 /opt/scripts/sync_inventory.py
```

!!! warning "Common errors"
    **`pip3: command not found`** — Install Python 3 and pip3 using your system package manager (apt install python3-pip on Ubuntu/Debian).
    **`WARNING: pip is being invoked by an old script wrapper`** — Upgrade pip with `python3 -m pip install --upgrade pip`.
    **`error: externally-managed-environment`** — Use a virtual environment or add `--break-system-packages` flag to pip install commands.
**Check pyenv version (if using pyenv)**

```bash
pyenv version
cat .python-version
```


```text title="Expected output"
3.11.7 (set by /home/devops/.pyenv/versions/3.11.7/bin/python)
3.11.7
```

!!! warning "Common errors"
    **`pyenv: version `3.11.7' is not installed`** — Run `pyenv install 3.11.7` to install the required Python version.
    **`cat: .python-version: No such file or directory`** — Create a `.python-version` file in the project root with `echo "3.11.7" > .python-version`.
The `.python-version` file records the required Python version for the project. `pyenv` activates it automatically when entering the directory.

**Verify virtual environment is active**

```bash
echo $VIRTUAL_ENV
python3 -c "import sys; print(sys.prefix)"
```


```text title="Expected output"
/opt/venv/myapp
/opt/venv/myapp
```

!!! warning "Common errors"
    **`No such file or directory`** — Activate the virtual environment first with `source /path/to/venv/bin/activate`.
    **`ModuleNotFoundError: No module named 'sys'`** — This is extremely rare; reinstall Python with `python3 -m venv /path/to/venv` and reactivate.
If `VIRTUAL_ENV` is empty, activate the venv before running scripts:

```bash
source /opt/automation/venv/bin/activate
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`bash: /opt/automation/venv/bin/activate: No such file or directory`** — Create the virtual environment with `python3 -m venv /opt/automation/venv` or verify the correct path.
    **`bash: source: command not found`** — Use `. /opt/automation/venv/bin/activate` instead, or ensure you're running bash (not sh).
**Check for environment variable completeness**

```bash
python3 -c "import os; print([k for k in ['API_URL','API_TOKEN','LOG_DIR'] if k not in os.environ])"
```


```text title="Expected output"
['API_TOKEN', 'LOG_DIR']
```

!!! warning "Common errors"
    **`ModuleNotFoundError: No module named 'os'`** — This is extremely rare; reinstall Python 3 if it occurs, as `os` is a built-in module.
    **`SyntaxError: invalid syntax`** — Ensure the bash block is copied exactly without line breaks; paste the entire command as a single line or properly escape newlines with backslashes.
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


```text title="Expected output"
Package                    Version
-------------------------- -----------
pip                        23.2.1
setuptools                 68.0.0
wheel                      0.41.2
requests                   2.31.0
paramiko                   3.3.1
pyyaml                     6.0.1
jinja2                     3.1.2
ansible                    2.10.7
prometheus-client          0.17.1

Package                    Version Latest Type
-------------------------- ----------- ----------- -----
pip                        23.2.1      24.0        wheel
setuptools                 68.0.0      69.1.0      wheel
requests                   2.31.0      2.32.1      wheel
paramiko                   3.3.1       3.4.0       wheel
pyyaml                     6.0.1       6.0.2       wheel
```

!!! warning "Common errors"
    **`WARNING: pip is being invoked by an old script wrapper.`** — Upgrade pip with `python3 -m pip install --upgrade pip` to use the current wrapper.
    **`ERROR: Could not find a version that satisfies the requirement`** — Ensure the package name is spelled correctly and the PyPI repository is accessible.
**Check for dependency conflicts**

```bash
pip3 check
```


```text title="Expected output"
WARNING: pip is being invoked by an old script wrapper.
This will fail in a future version of pip.
Please see https://github.com/pip/pip/issues/5599 for advice on fixing the underlying issue.
To avoid this problem you can invoke Python with '-m pip' instead of trying to call pip directly.

(no output — all dependencies are compatible)
```

!!! warning "Common errors"
    **`ERROR: pip's dependency resolver does not currently take into account all the packages that are installed with your project in order to compare their dependency versions.`** — Run `pip3 install --upgrade pip` to update pip to the latest version that fully resolves dependencies.
    **`WARNING: Ignoring invalid distribution -ip`** — Remove corrupted package metadata by running `pip3 install --force-reinstall <package_name>` or clear pip cache with `rm -rf ~/.cache/pip`.
Any output from `pip3 check` indicates a broken dependency graph that must be resolved.

**Audit for known CVEs**

```bash
pip3 install safety
safety check
```


```text title="Expected output"
Collecting safety
  Downloading safety-2.3.5-py2.py3-none-any.whl (33.2 MB)
     |████████████████████████████████| 33.2 MB 2.3 MB/s
Installing collected packages: safety
Successfully installed safety-2.3.5
╒════════════════════════════════════════════════════════════════════════════╕
│                                                                            │
│                       /$$$$$$            /$$                              │
│                      /$$__  $$          | $$                              │
│  /$$$$$$$  /$$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$               │
│ /$$_____/ /$$_____/ | $$$$   /$$__  $$|_  $$_/  | $$  | $$               │
│|  $$$$$$ | $$       | $$_/  | $$  \ $$  | $$    | $$  | $$               │
│ \____  $$| $$       | $$    | $$  | $$  | $$ /$$| $$  | $$               │
│ /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$/  |  $$$$/|  $$$$$$$               │
│|_______/  \_______/|__/     \______/    \___/   \____  $$               │
│                                                  /$$  | $$               │
│                                                 |  $$$$$$/               │
│  by SafetyDB.org                                \______/                │
│                                                                            │
╒════════════════════════════════════════════════════════════════════════════╕

 Safety 2.3.5 is scanning this environment
 Timestamp: 2024-01-15T09:42:33Z

 Found and scanned 47 packages

 No known security vulnerabilities found
```

!!! warning "Common errors"
    **`pip3: command not found`** — Install Python 3 and pip3 using your system package manager (apt-get install python3-pip on Debian/Ubuntu).
    **`safety: command not found`** — Ensure the pip3 installation completed successfully and /usr/local/bin is in your PATH, or use python3 -m safety check instead.
**Export current dependencies (freeze)**

```bash
pip3 freeze > requirements-$(date +%Y%m%d).txt
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`pip3: command not found`** — Install Python 3 and pip3 with `apt-get install python3-pip` (Debian/Ubuntu) or `brew install python3` (macOS).
    **`Permission denied`** — Run the command from a directory where you have write permissions, or use `sudo` if necessary (though this is not recommended for pip operations).
**Install from pinned requirements**

```bash
pip3 install -r requirements.txt
```


```text title="Expected output"
Collecting certifi==2023.7.22
Collecting requests==2.31.0
Collecting pyyaml==6.0.1
Collecting psutil==5.9.5
Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Installing collected packages: certifi, charset-encoder, idna, urllib3, requests, pyyaml, psutil
Successfully installed certifi-2023.7.22 requests-2.31.0 pyyaml-6.0.1 psutil-5.9.5
```

!!! warning "Common errors"
    **`ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`** — Verify you are in the correct directory where requirements.txt is located, or provide the full path to the file.
    **`ERROR: pip's dependency resolver does not currently take into account all the packages that are installed with setuptools==X.X.X`** — This is typically a warning and safe to ignore; if installation fails, upgrade pip with `pip3 install --upgrade pip`.
    **`error: Microsoft Visual C++ 14.0 or greater is required`** — Install the Microsoft C++ Build Tools or ensure a compatible C++ compiler is available on your system.
**Verify a specific critical library is importable**

```bash
python3 -c "import requests; print(requests.__version__)"
python3 -c "import boto3; print(boto3.__version__)"
python3 -c "import paramiko; print(paramiko.__version__)"
```


```text title="Expected output"
2.31.0
1.26.137
3.3.1
```

!!! warning "Common errors"
    **`ModuleNotFoundError: No module named 'requests'`** — Install the missing package with `pip3 install requests`.
    **`ModuleNotFoundError: No module named 'boto3'`** — Install AWS SDK with `pip3 install boto3`.
    **`ModuleNotFoundError: No module named 'paramiko'`** — Install SSH library with `pip3 install paramiko`.
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


```text title="Expected output"
0 2 * * * /usr/bin/python3 /opt/health-checks/system_monitor.py >> /var/log/health-checks.log 2>&1
*/15 * * * * /usr/bin/python3 /opt/health-checks/disk_usage.py --threshold 85
0 */6 * * * /usr/bin/python3 /opt/health-checks/service_status.py --notify admin@company.com
```

!!! warning "Common errors"
    **`no crontab for root`** — Run `sudo crontab -e` to create a crontab entry for the current user or specify the user with `sudo crontab -u username -l`.
    **`command not found: crontab`** — Install cron service with `sudo apt-get install cron` (Debian/Ubuntu) or `sudo yum install cronie` (RHEL/CentOS).
**Check system-wide cron for Python jobs**

```bash
grep -r "python" /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/ /etc/cron.weekly/ 2>/dev/null
```


```text title="Expected output"
/etc/cron.d/python-health-check:*/15 * * * * root /usr/bin/python3 /opt/scripts/health_check.py >> /var/log/health_check.log 2>&1
/etc/cron.d/backup-jobs:0 2 * * * root /usr/bin/python3 /opt/automation/backup.py --full
/etc/cron.daily/system-audit:#!/bin/bash
/usr/bin/python3 /opt/scripts/audit.py --daily
/etc/cron.hourly/metrics-collector:#!/bin/bash
/usr/bin/python3 /opt/monitoring/collect_metrics.py
/etc/cron.weekly/db-maintenance:0 3 * * 0 root /usr/bin/python3 /opt/db/maintenance.py --optimize
```

!!! warning "Common errors"
    **`grep: /etc/cron.hourly/: No such file or directory`** — Create the missing directory with `mkdir -p /etc/cron.hourly/` or remove it from the grep search path if it's not needed.
    **`Permission denied`** — Run the command with `sudo` to access protected cron directories: `sudo grep -r "python" /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/ /etc/cron.weekly/ 2>/dev/null`
**Check cron daemon is running**

```bash
systemctl status cron
# or on RHEL/CentOS:
systemctl status crond
```


```text title="Expected output"
● crond.service - Command Scheduler
     Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:23:47 UTC; 3 days ago
   Main PID: 1247 (crond)
      Tasks: 1 (limit: 2048)
     Memory: 2.1M
        CPU: 15ms
     CGroup: /system.slice/crond.service
             └─1247 /usr/sbin/crond -n

Jan 15 09:23:47 prod-scheduler-01 systemd[1]: Started Command Scheduler.
```

!!! warning "Common errors"
    **`Unit cron.service could not be found.`** — Use `systemctl status crond` on RHEL/CentOS systems instead of `cron`.
    **`System has not been booted with systemd as init system (PID 1). Can't operate.`** — Use `service crond status` or `ps aux | grep crond` on systems without systemd.
**Review recent cron execution log**

```bash
grep CRON /var/log/syslog | tail -50
# or on RHEL/CentOS:
grep CRON /var/log/cron | tail -50
```


```text title="Expected output"
Jan 15 08:15:01 prod-app-01 CRON[2847]: (root) CMD (cd /opt/backup && ./daily-backup.sh)
Jan 15 09:30:02 prod-app-01 CRON[3156]: (postgres) CMD (/usr/local/bin/pg_dump -U postgres maindb > /backups/maindb.sql)
Jan 15 10:45:03 prod-app-01 CRON[3892]: (www-data) CMD (/usr/bin/php /var/www/html/cron/cleanup.php)
Jan 15 12:00:01 prod-app-01 CRON[4521]: (root) CMD (/opt/monitoring/health-check.sh >> /var/log/health-check.log 2>&1)
Jan 15 14:15:02 prod-app-01 CRON[5234]: (root) CMD (find /tmp -type f -mtime +7 -delete)
Jan 15 16:30:01 prod-app-01 CRON[6145]: (syslog) CMD (/usr/sbin/logrotate /etc/logrotate.conf)
Jan 15 18:45:03 prod-app-01 CRON[7089]: (root) CMD (/opt/scripts/sync-ntp.sh)
Jan 15 20:00:02 prod-app-01 CRON[7856]: (backup) CMD (/usr/bin/rsync -av /data /mnt/backup/)
Jan 15 22:15:01 prod-app-01 CRON[8734]: (root) CMD (/opt/monitoring/disk-usage-alert.sh)
Jan 16 00:30:02 prod-app-01 CRON[9521]: (postgres) CMD (VACUUM ANALYZE;)
```

!!! warning "Common errors"
    **`grep: /var/log/syslog: No such file or directory`** — Use the RHEL/CentOS path `/var/log/cron` instead, or check your distro's actual syslog location with `ls /var/log/`.
    **`Permission denied`** — Run the command with `sudo` since cron logs typically require root privileges to read.
**Check systemd timer units (alternative to cron)**

```bash
systemctl list-timers --all | grep python
```


```text title="Expected output"
NEXT                         LEFT     LAST                         PASSED   UNIT                          ACTIVATES
Mon 2024-01-15 14:30:00 UTC  2h 15m   Mon 2024-01-15 12:30:12 UTC  5s       python-health-check.timer    python-health-check.service
Mon 2024-01-15 15:00:00 UTC  2h 45m   Mon 2024-01-15 11:00:08 UTC  1h 30m   python-app-monitor.timer     python-app-monitor.service
Mon 2024-01-15 16:15:00 UTC  3h 59m   Sun 2024-01-14 16:15:22 UTC  22h      python-backup-check.timer    python-backup-check.service

3 timers listed.
```

!!! warning "Common errors"
    **`Failed to get properties: Unit python-health-check.timer not found.`** — Verify the timer unit exists with `systemctl list-unit-files | grep python` and enable it if needed with `systemctl enable python-health-check.timer`.
    **`Failed to list timers: Access denied`** — Run the command with `sudo` or ensure your user is in the `systemd-journal` group.
**Verify script output log (if scripts redirect output)**

```bash
# Example: check last run time and exit status from a log file
tail -20 /var/log/automation/<script-name>.log
```


```text title="Expected output"
2024-01-15 14:32:18 [INFO] Health check started for database-sync
2024-01-15 14:32:22 [INFO] Connected to primary database (host: db-primary-01.internal)
2024-01-15 14:32:25 [INFO] Verified 1,247 records synced successfully
2024-01-15 14:32:26 [INFO] Replication lag: 0.3ms
2024-01-15 14:32:27 [INFO] Health check completed successfully
2024-01-15 14:32:27 [INFO] Exit status: 0
2024-01-15 15:02:18 [INFO] Health check started for database-sync
2024-01-15 15:02:23 [INFO] Connected to primary database (host: db-primary-01.internal)
2024-01-15 15:02:26 [INFO] Verified 1,248 records synced successfully
2024-01-15 15:02:27 [INFO] Replication lag: 0.2ms
2024-01-15 15:02:28 [INFO] Health check completed successfully
2024-01-15 15:02:28 [INFO] Exit status: 0
```

!!! warning "Common errors"
    **`tail: cannot open '/var/log/automation/<script-name>.log' for reading: No such file or directory`** — Replace `<script-name>` with the actual script name and verify the log directory exists.
    **`tail: cannot open '/var/log/automation/database-sync.log' for reading: Permission denied`** — Run the command with `sudo` or ensure your user has read permissions on the log file.
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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Python — Procedures](../procedures/)
- [Python — CLI Reference](../cli-reference/)
- [Python — Common Issues](../../troubleshooting/common-issues/)
