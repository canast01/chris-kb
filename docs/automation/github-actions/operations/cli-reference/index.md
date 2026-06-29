---
tags:
  - github-actions
  - operations
---
# GitHub Actions — CLI Reference

```bash
# macOS
brew install gh

# RHEL / Rocky / Fedora
dnf install gh

# Ubuntu / Debian
type -p curl >/dev/null || apt install curl -y
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
apt update && apt install gh -y

# Verify
gh --version
gh auth login
```


```text title="Expected output"
# macOS
Homebrew 4.2.15
Installing gh...
==> Downloading https://ghcr.io/v2/homebrew/core/gh/manifests/2.48.0
==> Pouring gh--2.48.0.arm64_sonoma.bottle.tar.gz
🍺  /usr/local/Cellar/gh/2.48.0: 100 files, 48.2MB

# RHEL / Rocky / Fedora
Dependencies resolved.
Installing:
 gh                                x86_64    2.48.0-1.el9    fedora    18 MB
Transaction Summary
Install  1 Package
Total download size: 18 MB
Installed size: 48 MB
Complete!

# Ubuntu / Debian
Reading package lists... Done
Get:1 https://cli.github.com/packages InRelease [4,892 B]
Get:2 https://cli.github.com/packages/stable/main amd64 Packages [8,234 B]
Fetched 13.1 kB in 2s (6.2 kB/s)
Reading package lists... Done
Setting up gh (2.48.0) ...

# Verify
gh version 2.48.0 (2024-01-15)
https://github.com/cli/cli/releases/tag/v2.48.0

? What is your preferred protocol for Git operations on this host? [Use arrows to move, select with Enter]
> HTTPS
  SSH
  Leave my Git credentials alone
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to cli.github.com port 443: Connection refused`** — Verify network connectivity and check if the GitHub CLI repository is accessible from your environment.
    **`E: Unable to locate package gh`** — Run `apt update` before `apt install gh` to refresh the package cache.
    **`error: failed to authenticate git credential`** — Complete `gh auth login` with valid GitHub credentials before attempting to use authenticated git operations.
```bash
# List environments
gh api repos/OWNER/REPO/environments | jq '.environments[].name'

# Create environment
gh api --method PUT repos/OWNER/REPO/environments/staging

# Create with wait timer (in minutes)
gh api --method PUT repos/OWNER/REPO/environments/production \
  --field wait_timer=5

# View environment details
gh api repos/OWNER/REPO/environments/production | jq .
```

```text title="Expected output"
"development"
"staging"
"testing"
(no output — command completes silently)
(no output — command completes silently)
{
  "id": 398432891,
  "node_id": "MDExOkVudmlyb25tZW50Mzk4NDMyODkx",
  "name": "production",
  "url": "https://api.github.com/repos/acme-corp/deploy-service/environments/production",
  "state": "available",
  "created_at": "2024-01-15T09:22:14Z",
  "updated_at": "2024-01-15T09:22:14Z",
  "protection_rules": [
    {
      "id": 5891234,
      "type": "wait_timer",
      "wait_timer": 5
    }
  ],
  "deployment_branch_policy": null
}
```

!!! warning "Common errors"
    **`HTTP 404: Not Found`** — Verify OWNER and REPO values match your GitHub repository path exactly (case-sensitive).
    **`HTTP 403: Forbidden`** — Ensure your GitHub token has `repo` scope and admin access to the target repository.
    **`parse error: Cannot index number with string "environments"`** — The API response is not an array; check that the endpoint returns an object with an `environments` key, or remove the array indexing from the jq filter.
```bash
# List runners
gh api repos/OWNER/REPO/actions/runners | jq '.runners[] | {id, name, status, labels}'
gh api orgs/ORG/actions/runners | jq '.runners[]'

# Get runner registration token
gh api --method POST repos/OWNER/REPO/actions/runners/registration-token \
  | jq -r .token

# Get runner removal token
gh api --method POST repos/OWNER/REPO/actions/runners/remove-token \
  | jq -r .token

# List runner groups (org)
gh api orgs/ORG/actions/runner-groups | jq '.runner_groups[] | {id, name, visibility}'

# Delete an offline runner
RUNNER_ID=123
gh api --method DELETE repos/OWNER/REPO/actions/runners/$RUNNER_ID
```

```text title="Expected output"
{
  "id": 456,
  "name": "ubuntu-runner-01",
  "status": "online",
  "labels": [
    {
      "id": 1,
      "name": "self-hosted",
      "type": "read-only"
    },
    {
      "id": 2,
      "name": "linux",
      "type": "read-only"
    }
  ]
}
{
  "id": 789,
  "name": "macos-runner-02",
  "status": "offline",
  "labels": [...]
}
...

ghs_16M4v9kL2pQr8xYzAbCdEfGhIjKlMnOpQrStUvWxYz

ghr_1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0T

{
  "id": 1,
  "name": "Default",
  "visibility": "all",
  "allows_public_repositories": true
}
{
  "id": 2,
  "name": "Private-Only",
  "visibility": "private",
  "allows_public_repositories": false
}

(no output — command completes silently)
```

!!! warning "Common errors"
    **`HTTP 404: Not Found (repository.actions.disabled)`** — Enable GitHub Actions in the repository settings under Actions > General.
    **`HTTP 401: Unauthorized`** — Ensure your GitHub CLI token has `admin:org` or `repo` scope by running `gh auth status` and re-authenticating with `gh auth login`.
    **`jq: error (at <stdin>:0): Cannot index null with string "runners"`** — Verify OWNER/REPO/ORG values are correct and the runner exists before querying.
```bash
# List artifacts for a run
gh api repos/OWNER/REPO/actions/runs/RUN_ID/artifacts | jq '.artifacts[]'

# Download artifact
gh run download RUN_ID --name artifact-name --dir /tmp/

# Delete artifact
gh api --method DELETE repos/OWNER/REPO/actions/artifacts/ARTIFACT_ID

# List and delete expired artifacts (bulk cleanup)
gh api repos/OWNER/REPO/actions/artifacts | \
  jq -r '.artifacts[] | select(.expired == true) | .id' | \
  while read id; do
    gh api --method DELETE repos/OWNER/REPO/actions/artifacts/$id
    echo "Deleted artifact $id"
  done
```

```text title="Expected output"
{
  "id": 1847293847,
  "node_id": "MDg6QXJ0aWZhY3QxODQ3MjkzODQ3",
  "name": "build-output",
  "size_in_bytes": 2457600,
  "url": "https://api.github.com/repos/acme-corp/deploy-service/actions/artifacts/1847293847",
  "archive_download_url": "https://api.github.com/repos/acme-corp/deploy-service/actions/artifacts/1847293847/zip",
  "expired": false,
  "created_at": "2024-01-15T09:42:31Z",
  "updated_at": "2024-01-15T09:42:31Z",
  "expires_at": "2024-04-14T09:42:31Z"
}
{
  "id": 1847293848,
  "name": "test-reports",
  "size_in_bytes": 512000,
  "expired": true,
  "created_at": "2023-12-01T14:22:15Z",
  "expires_at": "2024-01-14T14:22:15Z"
}
Downloading artifact-name to /tmp/
artifact-name (2.3 MB) downloaded
Deleted artifact 1847293848
Deleted artifact 1847293849
```

!!! warning "Common errors"
    **`HTTP 404: Not Found`** — Verify OWNER, REPO, and RUN_ID are correct and the run exists in your repository.
    **`gh: could not authenticate`** — Ensure you are logged in with `gh auth login` and have `repo` scope permissions.
```bash
# List caches
gh cache list
gh cache list --sort size --order desc

# Delete a specific cache
gh cache delete CACHE_KEY

# Delete all caches for a branch
gh cache delete --all --branch feature/my-branch

# View cache usage
gh api repos/OWNER/REPO/actions/cache/usage | jq .
```

```text title="Expected output"
gh cache list
NAME                                    ID                      CREATED_AT          LAST_ACCESSED_AT     SIZE_BYTES
node_modules-ubuntu-22.04-main          C:a1b2c3d4e5f6g7h8     2024-01-15T09:23Z    2024-01-18T14:52Z    524288000
build-artifacts-v2-main                 C:x9y8z7w6v5u4t3s2     2024-01-14T16:41Z    2024-01-17T11:30Z    314572800
pip-cache-python3.11-main               C:m1n2o3p4q5r6s7t8     2024-01-12T13:15Z    2024-01-16T08:22Z    209715200

gh cache list --sort size --order desc
NAME                                    ID                      CREATED_AT          LAST_ACCESSED_AT     SIZE_BYTES
node_modules-ubuntu-22.04-main          C:a1b2c3d4e5f6g7h8     2024-01-15T09:23Z    2024-01-18T14:52Z    524288000
build-artifacts-v2-main                 C:x9y8z7w6v5u4t3s2     2024-01-14T16:41Z    2024-01-17T11:30Z    314572800
pip-cache-python3.11-main               C:m1n2o3p4q5r6s7t8     2024-01-12T13:15Z    2024-01-16T08:22Z    209715200

gh cache delete C:a1b2c3d4e5f6g7h8
✓ Deleted cache node_modules-ubuntu-22.04-main

gh cache delete --all --branch feature/my-branch
✓ Deleted 3 caches for branch feature/my-branch

gh api repos/OWNER/REPO/actions/cache/usage | jq .
{
  "total_cache_size_bytes": 1048576000,
  "total_count": 8
}
```

!!! warning "Common errors"
    **`gh: resource not found`** — Verify the CACHE_KEY exists by running `gh cache list` and use the exact ID from the output.
    **`gh: authentication required`** — Ensure you are authenticated with `gh auth login` and have `repo` scope permissions.
```bash
# Check Actions minutes usage (org)
gh api orgs/ORG/settings/billing/actions | jq '{
  total_minutes_used,
  included_minutes,
  total_paid_minutes_used
}'

# Per-repo usage
gh api repos/OWNER/REPO/actions/cache/usage | jq .
```

```text title="Expected output"
{
  "total_minutes_used": 4827,
  "included_minutes": 3000,
  "total_paid_minutes_used": 1827
}
{
  "full_cache_usage_bytes": 5368709120,
  "full_cache_usage_gb": 5.0,
  "full_cache_size_bytes": 10737418240,
  "full_cache_size_gb": 10.0,
  "active_cache_entries_count": 42,
  "active_cache_size_bytes": 3221225472,
  "active_cache_size_gb": 3.0
}
```

!!! warning "Common errors"
    **`HTTP 404: Not Found (https://api.github.com/orgs/ORG/settings/billing/actions)`** — Replace `ORG` with your actual organization name and verify you have admin permissions on that org.
    **`HTTP 403: Resource not accessible by integration`** — Ensure your GitHub token has `admin:org_hook` and `read:org` scopes, or use `gh auth login` to re-authenticate with proper permissions.
```bash
# Find all failed runs in the last 7 days
gh run list --status failure --json databaseId,name,createdAt \
  | jq --arg cutoff "$(date -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)" \
    '.[] | select(.createdAt > $cutoff)'

# Trigger deploy workflow for current branch
gh workflow run deploy.yml --ref "$(git branch --show-current)"

# Watch most recent run until completion
gh run watch $(gh run list --limit 1 --json databaseId -q '.[0].databaseId')

# Bulk re-run all failed jobs across recent runs
gh run list --status failure --json databaseId -q '.[].databaseId' | \
  xargs -I{} gh run rerun {} --failed

# List workflow files that haven't run in 30 days (candidates for cleanup)
gh workflow list --json name,state,updatedAt | \
  jq --arg cutoff "$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)" \
    '.[] | select(.updatedAt < $cutoff) | .name'
```
```yaml
# Workflow-level env
env:
  NODE_ENV: production
  APP_VERSION: ${{ github.sha }}

jobs:
  deploy:
    env:
      DEPLOY_TARGET: prod-cluster   # job-level override

    steps:
      - name: Set dynamic variable
        run: echo "TIMESTAMP=$(date +%s)" >> "$GITHUB_ENV"

      - name: Use it in next step
        run: echo "Built at $TIMESTAMP"

      - name: Set step output
        id: build
        run: echo "image-tag=ghcr.io/org/app:${{ github.sha }}" >> "$GITHUB_OUTPUT"

      - name: Use step output
        run: docker pull ${{ steps.build.outputs.image-tag }}
```

```d2
direction: down

verify: "Verify" {shape: rectangle}

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

- [GitHub Actions — Procedures](../procedures/)
- [GitHub Actions — Scripts](../scripts/)
- [GitHub Actions — Health Checks](../health-checks/)
