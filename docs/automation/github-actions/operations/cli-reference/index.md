# GitHub Actions — CLI Reference

> Part of the [GitHub Actions Operations](../index.md) reference.

The `gh` CLI (GitHub CLI) is the primary tool for managing GitHub Actions from the command line.

## Installation

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
```

## Run Management

```bash
# List recent workflow runs
gh run list
gh run list --workflow deploy.yml
gh run list --branch main --limit 20

# View a specific run
gh run view 12345678

# Watch a run in real time
gh run watch 12345678

# View run logs
gh run view 12345678 --log
gh run view 12345678 --log-failed   # only failed job logs

# Download artifacts from a run
gh run download 12345678
gh run download 12345678 --name build-output --dir /tmp/artifacts

# Cancel a running workflow
gh run cancel 12345678

# Re-run failed jobs only
gh run rerun 12345678 --failed

# Re-run entire workflow
gh run rerun 12345678
```

## Secret Management

```bash
# List secrets (names only — values never shown)
gh secret list
gh secret list --env production
gh secret list --org myorg

# Set a secret from stdin
echo "mysecretvalue" | gh secret set MY_SECRET

# Set from a file (SSH key, certificate)
gh secret set DEPLOY_SSH_KEY < ~/.ssh/deploy_ed25519

# Set with explicit value
gh secret set API_TOKEN --body "tok-abc123"

# Set environment secret
gh secret set PROD_DB_PASSWORD --env production

# Set organization secret
gh secret set SHARED_TOKEN --org myorg

# Delete a secret
gh secret delete OLD_TOKEN
gh secret delete STAGING_KEY --env staging
```

## Environment Management

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

## Runner Management

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

## Artifact Management

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

## Cache Management

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

## Usage and Billing

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

## Useful One-Liners

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

## Environment Variables in Workflows

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
