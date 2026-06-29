---
tags:
  - python
  - troubleshooting
search:
  boost: 1.5
---
# Python Automation — Escalation

<div class="kb-summary">
Python automation escalation: when to file a CPython bug, how to report a library issue, how to respond to CVEs, and the internal escalation path for script failures, dependency vulnerabilities, and production automation outages.

*Applies to: Python 3.x*
</div>

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "On-Call Engineer" as ENG
participant "Python\nSystem" as SYS
participant "Vendor Support" as SUP

ENG -> SYS: Severity Levels (Internal)
SYS --> ENG: Output
ENG -> SYS: Pre-Escalation Triage Checklist
SYS --> ENG: Output
ENG -> SYS: Step-by-Step Data Collection
SYS --> ENG: Output
ENG -> SUP: Escalate with diagnostic bundle
SUP --> ENG: Case / resolution path

@enduml
```

## Before you begin

- **Access:** Access to the script execution environment and its log output; pip/package manager access to check installed versions
- **Gather first:** full Python traceback (not a screenshot), `python3 --version`, the exact command that invokes the failing script, and `pip list` output
- **Scope:** confirm whether the failure is script-specific, environment-specific (one host), or cross-environment (all hosts running the same script)
- **CVE detected:** if the escalation involves a security vulnerability in a dependency, rotate any affected secrets immediately before investigating further
- **Logging:** add `logging.basicConfig(level=logging.DEBUG)` to capture full HTTP request/response detail before reproducing

---

## Severity Levels (Internal)

| Severity | Definition | Escalation Path |
|---|---|---|
| P1 — Critical | Production automation pipeline completely down; secret exposure suspected; data loss | Immediate: on-call engineer + security team (if secret leak) |
| P2 — High | Critical script failing for all runs; external API broken for all operations; CVE in prod dependency | Same day: automation team + infra team |
| P3 — Medium | Single script or function failing; intermittent errors in non-critical automation | Next business day: automation team |
| P4 — Low | Performance concern; code quality issue; dependency update available but not critical | Sprint backlog item |

## Pre-Escalation Triage Checklist

| Check | Command | Expected |
|---|---|---|
| Python version | `python3 --version` | Expected version (3.10+, 3.11+, etc.) |
| Virtual environment active | `which python3` | Points to venv path, not system Python |
| Dependencies installed | `pip check` | `No broken requirements` |
| CVE status of dependencies | `pip-audit` or `safety check` | No known vulnerabilities |
| Script syntax valid | `python3 -m py_compile <script>.py` | No output (success) |
| Network/API reachable | `curl -s https://api.example.com/health` | HTTP 200 |
| SSL cert valid | `python3 -c "import ssl,urllib.request; urllib.request.urlopen('https://api.example.com')"` | No SSL error |
| Secret available | `echo $SECRET_VAR | wc -c` | Non-zero length |

---

## Step-by-Step Data Collection

### 1. Collect environment information

```bash
# Python and package versions
python3 --version > /tmp/py-env.txt
pip list --format=columns >> /tmp/py-env.txt
pip freeze > /tmp/requirements-current.txt

# Identify the virtual environment and interpreter in use
which python3
echo $VIRTUAL_ENV
python3 -c "import sys; print(sys.prefix); print(sys.path)"

# OS and OpenSSL version (for SSL-related issues)
uname -a
python3 -c "import ssl; print(ssl.OPENSSL_VERSION)"
openssl version
```


```text title="Expected output"
Python 3.11.7
Package    Version
---------- -------
pip        24.0
requests   2.31.0
urllib3    2.1.0
certifi    2023.7.22
setuptools 69.0.2
wheel      0.42.0
...
certifi==2023.7.22
charset-normalizer==3.3.2
idna==3.6
requests==2.31.0
urllib3==2.1.0
/usr/local/bin/python3
/home/admin/venv-prod
/home/admin/venv-prod
['/home/admin/venv-prod/lib/python3.11/site-packages', '/usr/lib/python3.11', '/usr/lib/python3.11/lib-dynload']
Linux ip-10-42-8-15 5.15.0-1234-aws #1234-Ubuntu SMP x86_64 GNU/Linux
OpenSSL 3.0.11 19 Sep 2023
OpenSSL 3.0.11 19 Sep 2023
```

!!! warning "Common errors"
    **`which: python3: not found`** — Ensure Python 3 is installed and in PATH, or use the full path to the interpreter (e.g., `/usr/bin/python3`).
    **`$VIRTUAL_ENV: command not found`** — The virtual environment is not activated; run `source /path/to/venv/bin/activate` before executing the script.
    **`ModuleNotFoundError: No module named 'ssl'`** — Reinstall Python with OpenSSL support using your package manager (e.g., `apt-get install python3-dev libssl-dev && python3 -m pip install --upgrade pip`).
### 2. Capture the full traceback

```python
# Add to the failing script before the failing call:
import logging, traceback

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    filename='/tmp/script-debug.log'
)

try:
    # YOUR FAILING CODE HERE
    pass
except Exception as e:
    logging.error("Failure details:\n%s", traceback.format_exc())
    raise
```

```bash
# Or capture all output when running:
python3 -u /path/to/script.py 2>&1 | tee /tmp/script-output-$(date +%F-%H%M%S).log
```


```text title="Expected output"
Starting script execution at 2024-01-15 14:32:18...
Processing configuration from /etc/app/config.yaml
Connected to database: postgres://db-prod-01.internal:5432/maindb
Initializing worker pool with 8 threads
[INFO] Task 1: Completed in 2.341s
[INFO] Task 2: Completed in 1.892s
[INFO] Task 3: Completed in 3.127s
[WARNING] Task 4: Retrying connection (attempt 2/3)
[INFO] Task 4: Completed in 5.614s
Script execution completed successfully
Output saved to /tmp/script-output-2024-01-15-143218.log
```

!!! warning "Common errors"
    **`python3: command not found`** — Install Python 3 or verify it's in your PATH with `which python3`.
    **`/path/to/script.py: No such file or directory`** — Replace `/path/to/script.py` with the actual script path and verify it exists with `ls -la`.
    **`Permission denied`** — Make the script executable with `chmod +x /path/to/script.py` or run with `python3` directly.
### 3. Identify the failing dependency

```bash
# Show full package info for the suspected package
pip show <package-name>

# Check if a newer version is available
pip index versions <package-name>

# Test in isolation with a minimal script
python3 -c "
import <package>
print(<package>.__version__)
# test the specific failing call
"

# Check for known CVEs
pip install pip-audit
pip-audit -r /tmp/requirements-current.txt
```


```text title="Expected output"
Name: requests
Version: 2.28.1
Summary: Python HTTP for Humans.
Home-page: https://requests.readthedocs.io
Author: Kenneth Reitz
Location: /usr/local/lib/python3.9/site-packages
Requires: charset-normalizer, idna, urllib3, certifi
Required-by: boto3, kubernetes

Available versions: 2.28.2, 2.29.0, 2.31.0

2.31.0
Vulnerability found in certifi (2022.12.7):
  ID: GHSA-35m3-r9hj-r8mm
  Fix: Update certifi to 2023.7.22 or later
  Severity: HIGH

1 vulnerability found in /tmp/requirements-current.txt
```

!!! warning "Common errors"
    **`ERROR: No matching distribution found for <package-name>`** — Verify the package name spelling and ensure PyPI is accessible; try `pip search <package-name>` or check https://pypi.org directly.
    **`ModuleNotFoundError: No module named '<package>'`** — Install the package with `pip install <package>` or check that the import name matches the distribution name (they sometimes differ, e.g., `pip install pillow` but `import PIL`).
### 4. For API errors — capture request/response detail

```python
# Enable HTTP debug logging for requests library
import logging
import http.client

http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# For boto3 (AWS SDK)
import boto3
boto3.set_stream_logger(name='botocore', level=logging.DEBUG)
```

### 5. Write the timeline

```text
Python version: 3.11.9
OS: Ubuntu 22.04.3 LTS
Affected script: /opt/automation/sync-inventory.py
Invocation: /usr/bin/python3 /opt/automation/sync-inventory.py --env prod
Cron schedule: */5 * * * * (every 5 minutes)

Issue first observed: 2026-06-15 13:00 UTC
Last successful run: 2026-06-15 12:55 UTC

Error observed:
  Traceback (most recent call last):
    File "sync-inventory.py", line 87, in <function>
      response = session.get(url, timeout=30)
  requests.exceptions.SSLError: HTTPSConnectionPool(host='api.example.com', port=443):
  Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(...)))

Packages relevant:
  requests==2.31.0 (upgraded 2 hours before failure)
  urllib3==2.0.7 (upgraded 2 hours before failure)
  certifi==2024.2.2

Changes in 2h before issue:
  - pip upgrade ran automatically via pre-deploy hook: requests 2.28.2 → 2.31.0, urllib3 1.26.18 → 2.0.7

Blast radius:
  - Inventory sync completely stopped
  - 5 other scripts using the requests library also failing
```

---

## Escalation Path

![Python Automation — Escalation — Diagram](../../../../assets/automation-python-troubleshooting-escalation-diagram.svg)

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Add `verify=False` to requests calls to bypass SSL errors | Disables certificate validation entirely — creates a man-in-the-middle risk in production | Fix the trust store (`certifi`, OS CA bundle) or pin the certificate; never disable verification |
| Use `try: except: pass` to silence the error and continue | Hides the real failure; downstream code runs on invalid or missing data | Log the error and fail explicitly; fix the root cause |
| Run `pip install --upgrade` on a production host without testing | Package upgrades frequently introduce breaking API changes | Use a requirements file with pinned versions; test upgrades in non-production first |
| Commit plaintext secrets to the repository to "fix" the secret access error | Permanent exposure; git history preserves secrets even after deletion | Use environment variables, a secrets manager (Vault, AWS Secrets Manager), or a `.env` file excluded from git |
| Share the full debug log externally without scrubbing | Debug logs often capture HTTP request headers including `Authorization: Bearer <token>` | Scrub all authentication headers and secret values before sharing any log file |

---

## Useful Commands for Case Updates

```bash
# Quick state snapshot — include in every escalation update
python3 --version
pip list --format=columns | head -30
echo "OpenSSL: $(python3 -c 'import ssl; print(ssl.OPENSSL_VERSION)')"

# Reproduce with maximum verbosity and save output
python3 -W all -v /path/to/script.py 2>&1 | tee /tmp/repro-$(date +%F-%H%M%S).log

# Test just the network call in isolation
python3 -c "
import requests, ssl
r = requests.get('https://api.example.com/health', timeout=10)
print(f'Status: {r.status_code}')
print(f'TLS version: {r.raw.version}')
"

# Check if issue is version-specific (install older version in test venv)
python3 -m venv /tmp/test-venv
/tmp/test-venv/bin/pip install requests==2.28.2
/tmp/test-venv/bin/python3 /path/to/script.py 2>&1 | head -20

# CVE scan
pip-audit -r /tmp/requirements-current.txt --format markdown
```


```text title="Expected output"
Python 3.11.8
Package            Version
------------------ -----------
requests           2.31.0
urllib3            2.1.0
certifi            2023.7.22
charset-normalizer 3.3.2
idna                3.6
pip                23.3.1
setuptools         68.2.2
...
OpenSSL: OpenSSL 3.0.12 26 Jan 2024

Verbose output saved to /tmp/repro-2024-01-15-143022.log
Status: 200
TLS version: 12

created virtual environment with 3.11.8 at /tmp/test-venv
Collecting requests==2.28.2
  Downloading requests-2.28.2-py3-none-any.whl (62 kB)
Installing collected packages: requests, urllib3, certifi, charset-normalizer, idna
Successfully installed requests-2.28.2 urllib3-1.26.13 certifi-2022.12.7 charset-normalizer-3.3.2 idna-3.4
Script completed successfully in 2.341s

Auditing dependencies from /tmp/requirements-current.txt
Found 2 vulnerabilities:
| Package | Version | Vulnerability | Severity |
|---------|---------|---|---|
| urllib3 | 2.1.0 | CVE-2023-45803 | Medium |
| certifi | 2023.7.22 | CVE-2023-37920 | Low |
```

!!! warning "Common errors"
    **`ModuleNotFoundError: No module named 'requests'`** — Run `pip install requests` in the active Python environment before executing the script.
    **`requests.exceptions.SSLError: HTTPSConnectionPool(host='api.example.com', port=443): Max retries exceeded`** — Verify SSL certificates are valid with `python3 -c "import certifi; print(certifi.where())"` and check firewall/proxy rules blocking HTTPS.
    **`venv: error: command not found`** — Install the venv module with `apt install python3-venv` (Debian/Ubuntu) or `yum install python3-venv` (RHEL/CentOS).
---

## See also

- [Python — Diagnostics](../diagnostics/)
- [Python — Common Issues](../common-issues/)

---

## Verify resolution

- Confirm the script completes successfully (`exit code 0`) for at least 3 consecutive runs
- Check that all downstream systems received the expected data (inventory synced, API calls succeeded)
- If a package was pinned as a workaround, create a follow-up ticket to upgrade when the fix is released
- If a CVE was involved: confirm patched version is deployed; verify secret rotation is complete
