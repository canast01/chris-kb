# Python Automation — Backup & Restore

Automation infrastructure must itself be protected. Loss of virtual environments, configuration, or secrets can halt all automated operations. This page covers what to back up, how, and how to restore quickly.

---

## What to Back Up

| Artifact | Backup method | Priority |
|---|---|---|
| Source code | Git repository | Critical — primary source of truth |
| `requirements.txt` / `poetry.lock` | Committed to Git | Critical — enables venv rebuild |
| Configuration files (non-secret) | Git repository | Critical |
| Secrets and credentials | Secrets manager (Vault, AWS SSM) | Critical — never in Git |
| Virtual environments | Do NOT back up — rebuild from lock file | N/A |
| Output data / reports | Object storage (S3, Azure Blob) or NAS | High |
| Scheduled task / cron definitions | Committed to Git or ITSM | High |

> Virtual environments are **not** backed up. They are ephemeral build artifacts. The lock file is the backup — the venv is always rebuilt from it.

---

## Source Code Backup

All automation code lives in Git. The Git repository is the authoritative backup.

```bash
# Verify all scripts are tracked
git status

# Ensure nothing is untracked that should be committed
git ls-files --others --exclude-standard

# Tag a release before major changes
git tag -a v1.4.2 -m "Pre-maintenance snapshot $(date -I)"
git push origin v1.4.2
```
```

---

## Dependency Backup (`requirements freeze`)

The lock file must always be committed. It is the exact specification needed to recreate the runtime environment.

### `pip` projects

```bash
# Create/update the lock file
pip freeze > requirements.txt

# Verify it captures everything needed
pip install -r requirements.txt --dry-run

# For multi-environment setups
pip freeze > requirements.txt          # production deps
pip freeze > requirements-dev.txt      # includes dev tools
```

### `poetry` projects

```bash
# Lock file is auto-managed — update after dependency changes
poetry lock

# Export to requirements.txt format for Docker or CI
poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry export -f requirements.txt --output requirements-dev.txt --with dev --without-hashes

# Verify lock file is consistent with pyproject.toml
poetry check
poetry lock --check
```

### Offline package cache (air-gapped environments)

```bash
# Download all packages for offline use
pip download -r requirements.txt -d /opt/pip-cache/

# Install from offline cache
pip install --no-index --find-links /opt/pip-cache/ -r requirements.txt
```

---

## Secrets Backup

**Never hardcode secrets in scripts or configuration files.** Secrets must live in a dedicated secrets manager.

### HashiCorp Vault

```bash
# Write a secret
vault kv put secret/automation/widget-api \
    api_key="sk-..." \
    api_url="https://api.example.com"

# Read a secret (use in scripts)
export WIDGET_API_KEY=$(vault kv get -field=api_key secret/automation/widget-api)

# List all secrets (to verify backup completeness)
vault kv list secret/automation/
```

```python
# Reading secrets from Vault in Python
import hvac
import os

client = hvac.Client(url=os.environ["VAULT_ADDR"], token=os.environ["VAULT_TOKEN"])

secret = client.secrets.kv.v2.read_secret_version(
    path="automation/widget-api",
    mount_point="secret",
)
api_key = secret["data"]["data"]["api_key"]
```

### AWS Systems Manager Parameter Store

```python
import boto3

ssm = boto3.client("ssm", region_name="eu-west-1")

def get_secret(name: str) -> str:
    resp = ssm.get_parameter(Name=name, WithDecryption=True)
    return resp["Parameter"]["Value"]

api_key = get_secret("/automation/widget/api_key")
```

### Secrets rotation checklist

- [ ] All secrets have an expiry date set in the secrets manager
- [ ] Rotation procedure documented in runbook
- [ ] Scripts use environment variables or secrets manager — no hardcoded values
- [ ] `.env` files excluded via `.gitignore`
- [ ] `git log --all -p | grep -i 'password\|secret\|api_key\|token'` returns no matches

---

## Configuration Backup

Non-secret configuration is committed to Git alongside code.

```python
# config.py — load from environment with pydantic-settings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    api_url: str = Field(description="Widget API base URL")
    api_key: str = Field(description="Widget API key (from env or secrets manager)")
    log_level: str = Field(default="INFO")
    output_dir: str = Field(default="/opt/automation/output")
    max_retries: int = Field(default=3)

settings = Settings()
```

```ini
# config/production.ini — committed to Git (no secrets)
[api]
url = https://api.example.com
timeout = 30
max_retries = 3

[logging]
level = INFO
format = json

[output]
directory = /opt/automation/output
retention_days = 90
```

---

## Restore Procedure

### Full Automation Infrastructure Restore

Use this procedure when restoring to a new host or recovering from complete failure.

```bash
# Step 1: Install Python (use pyenv for version control)
curl https://pyenv.run | bash
pyenv install 3.12.3
pyenv global 3.12.3
python --version  # Verify

# Step 2: Clone the automation repository
git clone https://github.com/org/platform-automation.git /opt/automation
cd /opt/automation

# Step 3: Restore virtual environment from lock file
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Verify all packages installed correctly
pip check  # Reports any dependency conflicts

# Step 4: Restore secrets (retrieve from Vault or SSM)
export VAULT_ADDR="https://vault.example.com"
export VAULT_TOKEN=$(cat /etc/automation/vault-token)
./scripts/restore-secrets.sh   # Writes .env from Vault

# Step 5: Restore configuration
cp config/production.ini /etc/automation/widget-automation.ini

# Step 6: Restore scheduled tasks
# systemd
sudo cp deploy/systemd/*.service /etc/systemd/system/
sudo cp deploy/systemd/*.timer   /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now widget-sync.timer

# cron (Linux)
crontab -l  # Verify empty
crontab deploy/crontab/automation.crontab

# Step 7: Validate restore
python -m pytest tests/ -x -q             # Run test suite
python -m widget_automation --check        # Application health check
```

### Restore Validation Checklist

- [ ] Python version matches expected (`python --version`)
- [ ] All packages install without errors (`pip install -r requirements.txt`)
- [ ] No dependency conflicts (`pip check`)
- [ ] Test suite passes (`pytest`)
- [ ] Secrets are accessible (spot-check one secret retrieval)
- [ ] Scheduled tasks are registered and enabled
- [ ] First scheduled run completes successfully (check logs)
- [ ] Output directory writable and correctly mounted

---

## Scheduled Job Recovery

When a scheduled automation job fails mid-run, follow this procedure:

```bash
# 1. Identify what ran and what failed
journalctl -u widget-sync.service --since "1 hour ago"

# 2. Check the last successful output
ls -lt /opt/automation/output/ | head -20

# 3. Determine if idempotent re-run is safe
#    (check if script has --resume or --since flags)
python -m widget_automation --help | grep -E 'resume|since|from'

# 4. Re-run with explicit scope if partial run must be recovered
python -m widget_automation sync \
    --since "2026-05-07T00:00:00Z" \
    --until "2026-05-08T00:00:00Z" \
    --dry-run   # Preview first

python -m widget_automation sync \
    --since "2026-05-07T00:00:00Z" \
    --until "2026-05-08T00:00:00Z"

# 5. Verify output completeness
python -m widget_automation verify --date 2026-05-07
```

### Idempotency requirement

All production automation scripts must be idempotent. Running the same script twice must produce the same result without duplication or corruption.

```python
def sync_widget(name: str) -> None:
    """Idempotent widget sync — safe to re-run."""
    existing = get_widget_from_db(name)
    remote = fetch_widget_from_api(name)

    if existing and existing["checksum"] == remote["checksum"]:
        log.info("widget_unchanged", name=name)
        return  # No-op — already up to date

    upsert_widget(name, remote)  # Create or update — not append
    log.info("widget_synced", name=name)
```
