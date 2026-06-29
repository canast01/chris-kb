---
tags:
  - operations
  - python
---
# Python — Install & Upgrade

```bash
# Install pyenv (Linux/macOS)
curl https://pyenv.run | bash

# Add to shell profile (~/.bashrc or ~/.zshrc)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Reload shell
exec "$SHELL"

# List available Python versions
pyenv install --list | grep '3\.12'

# Install a specific version
pyenv install 3.12.3

# List installed versions
pyenv versions

# Set global default
pyenv global 3.12.3

# Set version for a specific project (writes .python-version)
cd /opt/automation/my-project
pyenv local 3.12.3

# Verify
python --version
which python   # Should point to ~/.pyenv/shims/python
```


```text title="Expected output"
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   270  100   270    0     0    892      0 --:--:-- --:--:-- --:--:-- --:--:--:-- 100%
Cloning into '/home/ubuntu/.pyenv'...
remote: Enumerating objects: 11247, done.
remote: Counting objects: 100% (1234/1234), done.
Receiving objects: 100% (11247/11247), done.
Resolving deltas: 100% (7891/7891), done.

  3.12.0
  3.12.1
  3.12.2
  3.12.3
  3.12.4
  3.12.5
...

Installing Python 3.12.3...
Downloading Python-3.12.3.tar.gz...
######################################################################## 100.0%
Compiling Python 3.12.3...
Installation successful.

  system
  3.11.7
* 3.12.3 (set by /opt/automation/my-project/.python-version)

Python 3.12.3
/home/ubuntu/.pyenv/shims/python
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to pyenv.run port 443: Connection timed out`** — Verify network connectivity and retry, or manually clone pyenv from https://github.com/pyenv/pyenv.git to ~/.pyenv.
    **`pyenv: command not found`** — Ensure the shell profile edits were saved and run `exec "$SHELL"` to reload the shell with updated PATH.
    **`ERROR: The Python ssl extension was not compiled. Missing the OpenSSL lib?`** — Install required build dependencies with `sudo apt-get install libssl-dev libffi-dev python3-dev` (Ubuntu/Debian) or `brew install openssl` (macOS).
```bash
# 1. Inventory all automation using Python on this host
find /opt /home -name "*.py" -not -path "*/.venv/*" -not -path "*/__pycache__/*" 2>/dev/null
find /etc/cron* /etc/systemd/system -name "*.service" -exec grep -l python {} \;

# 2. Document current Python version used by each automation
for venv in /opt/automation/*/venv /opt/automation/*/.venv; do
    echo "=== $venv ==="
    $venv/bin/python --version 2>/dev/null
done

# 3. Check for Python-version-specific packages
pip list | grep -i 'python2\|py2\|six'   # py2 compat libraries signal migration risk

# 4. Test against new Python version before upgrading production
pyenv install 3.12.3
pyenv local 3.12.3
python -m venv /tmp/test-venv-312
source /tmp/test-venv-312/bin/activate
pip install -r requirements.txt
pytest tests/
```

```text title="Expected output"
/opt/automation/backup-tool/backup.py
/opt/automation/deploy-service/main.py
/opt/automation/deploy-service/utils.py
/opt/automation/monitoring/check_health.py
/home/automation/scripts/cleanup.py
/etc/systemd/system/backup-automation.service
/etc/systemd/system/deploy-worker.service
=== /opt/automation/backup-tool/venv ===
Python 3.9.18
=== /opt/automation/deploy-service/.venv ===
Python 3.10.12
=== /opt/automation/monitoring/.venv ===
Python 3.11.7
six                                    1.16.0
python-dateutil                        2.8.2
Downloading pyenv...
Installed python-3.12.3
created virtual environment at /tmp/test-venv-312
Collecting pip==23.3.1 from -r requirements.txt
Successfully installed 100 packages in 2.34s
======================== test session starts =========================
collected 47 tests
tests/unit/test_backup.py ............................ [ 53%]
tests/integration/test_deploy.py ..................... [ 100%]
======================== 47 passed in 8.23s ==========================
```

!!! warning "Common errors"
    **`pyenv: command not found`** — Install pyenv with `curl https://pyenv.run | bash` and add it to your PATH, or use `apt install pyenv` on Debian-based systems.
    **`ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`** — Ensure you are in the correct project directory containing requirements.txt before running pip install.
    **`FAILED tests/integration/test_deploy.py::test_api_connection - ConnectionError: Failed to connect to localhost:8080`** — Start required test services (database, API mock server) or mark integration tests as skipped with `@pytest.mark.skip` before running in isolated environments.
```bash
# Step 1: Install new Python version (alongside existing)
pyenv install 3.12.3  # Does NOT replace existing

# Step 2: Test in a temporary venv
python3.12 -m venv /tmp/upgrade-test
source /tmp/upgrade-test/bin/activate
pip install -r requirements.txt
pytest tests/ -v
deactivate
rm -rf /tmp/upgrade-test

# Step 3: Update .python-version in project
cd /opt/automation/my-project
pyenv local 3.12.3

# Step 4: Recreate the project venv
rm -rf .venv
python -m venv .venv                     # Now uses 3.12.3
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip check                                # Verify no conflicts

# Step 5: Run tests
pytest tests/ -v

# Step 6: Update scheduled task to point to new venv (if absolute path used)
# Check service files
grep -r 'python\|\.venv' /etc/systemd/system/my-automation.service

# Step 7: Restart service
sudo systemctl restart my-automation.service
journalctl -u my-automation.service -f   # Watch logs
```

```text title="Expected output"
Downloading Python-3.12.3... (this may take a minute)
Installing Python-3.12.3... (this may take a few minutes)
Installed Python-3.12.3 to /home/user/.pyenv/versions/3.12.3

collected 47 tests in 0.23s

test_api_endpoints.py::test_health_check PASSED
test_api_endpoints.py::test_user_auth PASSED
test_database.py::test_connection_pool PASSED
...
======================== 47 passed in 2.34s ========================

Setting local Python version to 3.12.3
Collecting pip
Downloading pip-24.0-py3-none-any.whl (1.5MB)
Installing collected packages: pip
Successfully installed pip-24.0

Collecting flask==2.3.2
Downloading Flask-2.3.2-py3-none-any.whl (101kB)
...
Successfully installed flask-2.3.2 requests-2.31.0 sqlalchemy-2.0.15

WARNING: pip-check found 0 broken requirements.

collected 47 tests in 0.25s

test_api_endpoints.py::test_health_check PASSED
test_api_endpoints.py::test_user_auth PASSED
...
======================== 47 passed in 2.41s ========================

ExecStart=/opt/automation/my-project/.venv/bin/python -m my_automation.main

● my-automation.service - My Automation Service
     Loaded: loaded (/etc/systemd/system/my-automation.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 1s ago
   Process: 8742 ExecStart=/opt/automation/my-project/.venv/bin/python -m my_automation.main (code=exited, status=0/SUCCESS)
  Main PID: 8743 (python)
     Tasks: 3 (limit: 2048)
    Memory: 42.3M
```

!!! warning "Common errors"
    **`pyenv: command not found`** — Install pyenv using your package manager (apt install pyenv on Ubuntu, or brew install pyenv on macOS) and add it to your PATH.
    **`ERROR: Could not find a version that satisfies the requirement <package>==X.Y.Z`** — Check requirements.txt for version pins incompatible with Python 3.12; update or remove version constraints and re-run pip install.
    **`ModuleNotFoundError: No module named 'pytest'`** — Add pytest to requirements.txt and re-run pip install -r requirements.txt in the activated venv.
```bash
# pip-audit — checks PyPI advisory database
pip install pip-audit
pip-audit -r requirements.txt

# safety — alternative vulnerability checker
pip install safety
safety check -r requirements.txt

# Output example:
# +===========+==============+==============+============================+
# | package   | version      | vuln_id      | advisory                   |
# +==========+==============+==============+============================+
# | requests  | 2.28.0       | CVE-2023-32681 | Unintended leak via Proxy |
# +===========+==============+==============+============================+
```

```text title="Expected output"
Collecting pip-audit
  Downloading pip_audit-2.6.1-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.2 MB)
Installing collected packages: pip-audit
Successfully installed pip-audit-2.6.1
Auditing /home/devops/app/requirements.txt
Found 3 known security vulnerabilities in 2 packages
  CVE-2023-32681 in requests==2.28.0: Unintended leak via Proxy-Auth header
  CVE-2024-35195 in requests==2.28.0: Potential DoS via malformed URLs
  CVE-2023-27043 in email-validator==1.1.5: ReDoS in email validation regex
Collecting safety
  Downloading safety-3.0.1-py3-none-any.whl (78 kB)
Installing collected packages: safety
Successfully installed safety-3.0.1
+===========+==============+==============+============================+
| package   | version      | vuln_id      | advisory                   |
+===========+==============+==============+============================+
| requests  | 2.28.0       | CVE-2023-32681 | Unintended leak via Proxy |
| requests  | 2.28.0       | CVE-2024-35195 | Potential DoS via URLs    |
| email-val | 1.1.5        | CVE-2023-27043 | ReDoS in regex validation  |
+===========+==============+==============+============================+
```

!!! warning "Common errors"
    **`ERROR: Could not find a version that satisfies the requirement pip-audit`** — Ensure pip is up to date with `pip install --upgrade pip` and check your PyPI index connectivity.
    **`ERROR: pip-audit: command not found`** — Add the pip user bin directory to PATH with `export PATH="$HOME/.local/bin:$PATH"` or reinstall with `pip install --user pip-audit`.
```bash
# Check outdated packages
pip list --outdated

# Upgrade a single package (test before committing)
pip install --upgrade requests
pytest tests/

# Upgrade all packages (risky — test thoroughly)
pip install --upgrade $(pip list --outdated --format=columns | awk 'NR>2 {print $1}')
pytest tests/

# Freeze new versions
pip freeze > requirements.txt

# Review the diff carefully before committing
git diff requirements.txt
```

```text title="Expected output"
Package    Version Latest Type
certifi    2023.7.22 2024.2.2 wheel
requests   2.31.0  2.32.3 wheel
urllib3    2.0.4   2.1.0  wheel
setuptools 68.0.0  69.1.0 wheel

Collecting requests
  Downloading requests-2.32.3-py3-none-any.whl (62 kB)
Installing collected packages: requests
  Attempting uninstall: requests
    Found existing installation: requests 2.31.0
    Uninstalling requests-2.31.0
    Successfully uninstalled requests-2.31.0
  Successfully installed requests-2.32.3

============================= test session starts ==============================
collected 47 items
tests/ PASSED [100%]
============================== 47 passed in 2.34s ===============================

Collecting certifi urllib3 setuptools
  Downloading certifi-2024.2.2-py3-none-any.whl (163 kB)
  Downloading urllib3-2.1.0-py3-none-any.whl (61 kB)
  Downloading setuptools-69.1.0-py3-none-any.whl (819 kB)
Installing collected packages: certifi, urllib3, setuptools
  Successfully installed certifi-2024.2.2 urllib3-2.1.0 setuptools-69.1.0

============================= test session starts ==============================
collected 47 items
tests/ PASSED [100%]
============================== 47 passed in 2.18s ===============================

diff --git a/requirements.txt b/requirements.txt
index 4a2c8f1..9e3d5b2 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -1,8 +1,8 @@
-certifi==2023.7.22
-requests==2.31.0
-urllib3==2.0.4
-setuptools==68.0.0
+certifi==2024.2.2
+requests==2.32.3
+urllib3==2.1.0
+setuptools==69.1.0
```

!!! warning "Common errors"
    **`ERROR: Could not find a version that satisfies the requirement requests==2.32.3`** — Check PyPI connectivity and verify the package version exists with `pip index versions requests`.
    **`FAILED tests/ — AssertionError: expected 200 but got 404`** — Revert the upgrade with `pip install -r requirements.txt.bak` and investigate breaking API changes in the upgraded package.
    **`awk: command not found`** — Install awk with your system package manager (`apt-get install gawk` on Ubuntu or `brew install gawk` on macOS) or use Python's built-in tools instead.
```bash
# Show outdated dependencies
poetry show --outdated

# Update a specific package
poetry update requests

# Update all (within version constraints in pyproject.toml)
poetry update

# Show what would be updated without applying
poetry update --dry-run

# Bump constraint and update (for major version upgrades)
poetry add requests@^2.31
poetry update requests

# After upgrades, run tests and commit the lock file
pytest tests/
git add poetry.lock pyproject.toml
git commit -m "chore: upgrade dependencies May 2026"
```
```yaml
# .github/workflows/security.yml
name: Security Audit
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday 06:00 UTC
  push:
    paths: ['requirements*.txt', 'poetry.lock', 'pyproject.toml']

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install pip-audit
      - run: pip-audit -r requirements.txt --output json > audit-results.json
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: audit-results
          path: audit-results.json
```
```bash
# 2to3 — automated syntax conversion (built-in)
2to3 --list-fixes                        # Show available fixers
2to3 -l -d legacy_script.py             # Diff without modifying
2to3 -w legacy_script.py                # Write converted file (.bak backup created)

# pylint for Python 3 compatibility
pip install pylint
pylint --py3k legacy_script.py

# pyupgrade — modernise Python 3 syntax further
pip install pyupgrade
pyupgrade --py311-plus script.py
```
```python
# six provided Python 2/3 compatibility — remove after full migration to Python 3
import six

# Before (with six)
if six.PY2:
    string_types = (str, unicode)
else:
    string_types = (str,)

# After (Python 3 only)
string_types = (str,)
```
```bash
# WRONG — do not upgrade Python inside an existing venv
# The venv still links to old Python

# CORRECT procedure:
# 1. Deactivate current venv
deactivate

# 2. Remove old venv
rm -rf .venv

# 3. Create new venv with upgraded Python
python3.12 -m venv .venv      # or: pyenv local 3.12.3 && python -m venv .venv

# 4. Install dependencies from lock file
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 5. Verify
pip check
python --version
pytest tests/

# 6. Update any absolute paths in service files
grep -r '/.venv/bin/python' /etc/systemd/system/
# Update to point to new .venv if path changed
sudo systemctl daemon-reload
sudo systemctl restart my-automation.service
```

```d2
direction: right

plan: "Plan" {shape: oval}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> verify
verify -> validate
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Python — Deploy](../../deploy/)
