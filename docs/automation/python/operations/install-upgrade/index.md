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
```text
┌───────────────────────────────────── Python — Install & Upgrade ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Install Python: pyenv for version management; system Python for server automation       │   │
│   │        Upgrade Python version: pyenv install 3.12.3; pyenv local 3.12.3; re-create venv       │   │
│   │       Upgrade packages: pip install -U <pkg>; or poetry update; test after every upgrade      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Python Version Install            │  │               Package Upgrade               │   │
│   │             pyenv install 3.12.3             │  │           pip install -U <package>          │   │
│   │             pyenv global 3.12.3              │  │       pip install -r requirements.txt       │   │
│   │       pyenv local 3.12.3 (per project)       │  │           poetry update <package>           │   │
│   │          rm -rf .venv && re-create           │  │            pip-compile --upgrade            │   │
│   │       pip install -r requirements.txt        │  │           Run pytest after upgrade          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ pyenv        = Python version manager; install multiple versions side-by-side; per-dir version│   │
│   │       EOL tracking = python.org/downloads; upgrade before EOL date; PS 3.8 EOL Oct 2024       │   │
│   │      Re-create venv= after Python upgrade; venv is tied to a specific interpreter binary      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
