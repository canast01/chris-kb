# GitHub Actions — Scripts


<div class="kb-summary">
> Part of the [GitHub Actions Operations](../index.md) reference. Utility scripts for managing GitHub Actions infrastructure — secrets rotation, runner health, artifact cleanup, and workflow monitoring.
</div>

> Part of the [GitHub Actions Operations](../index.md) reference.

Utility scripts for managing GitHub Actions infrastructure — secrets rotation, runner health, artifact cleanup, and workflow monitoring.

## Secret Rotation Script

```bash
#!/bin/bash
# rotate-secrets.sh — Rotate GitHub secrets from HashiCorp Vault
set -euo pipefail

REPO="org/infra"
VAULT_ADDR="https://vault.example.com"

rotate_secret() {
  local secret_name="$1"
  local vault_path="$2"
  local vault_field="$3"

  echo "Rotating $secret_name..."
  NEW_VALUE=$(vault kv get -field="$vault_field" "$vault_path")
  echo "$NEW_VALUE" | gh secret set "$secret_name" --repo "$REPO"
  echo "  ✓ $secret_name rotated"
}

# Login to Vault (AppRole)
vault write auth/approle/login \
  role_id="$VAULT_ROLE_ID" \
  secret_id="$VAULT_SECRET_ID" > /tmp/vault-token.json
export VAULT_TOKEN=$(jq -r .auth.client_token /tmp/vault-token.json)

rotate_secret "DEPLOY_SSH_KEY"       "secret/data/deploy" "ssh_private_key"
rotate_secret "AWS_SECRET_ACCESS_KEY" "secret/data/aws"   "secret_key"
rotate_secret "SLACK_BOT_TOKEN"       "secret/data/slack" "bot_token"

echo "All secrets rotated."
```text
┌────────────────────────────────────── GitHub Actions — Scripts ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Utility scripts for GitHub Actions operations: bulk secret update, runner status report, audit│   │
│   │  Use gh CLI or GitHub REST API (PyGitHub / requests) for scripting GitHub Actions management  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Management Scripts              │  │                Audit Scripts                │   │
│   │             bulk_set_secrets.py              │  │             audit_action_pins.py            │   │
│   │            list_runner_status.py             │  │        check_workflow_permissions.py        │   │
│   │             cancel_stuck_runs.py             │  │          report_billing_minutes.py          │   │
│   │              migrate_secrets.py              │  │           find_unpinned_actions.py          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    PyGitHub       = Python GitHub API client; pip install PyGithub; wraps REST and GraphQL    │   │
│   │         gh api --paginate = fetch all pages of a paginated API response automatically         │   │
│   │    Action audit   = scan all workflow YAML for uses: lines; verify each is pinned to a SHA    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Bulk Secret Audit Script

```bash
#!/bin/bash
# audit-secrets.sh — List all secrets across repos and environments
set -euo pipefail

ORG="myorg"
OUTPUT="secret-audit-$(date +%F).csv"

echo "repo,scope,secret_name" > "$OUTPUT"

# Org-level secrets
gh api orgs/$ORG/actions/secrets | jq -r \
  '.secrets[] | "'$ORG'/org-level,org,\(.name)"' >> "$OUTPUT"

# Repo-level secrets for each repo
gh repo list $ORG --limit 200 --json name -q '.[].name' | \
  while read -r repo; do
    # Repo secrets
    gh api repos/$ORG/$repo/actions/secrets 2>/dev/null | jq -r \
      '.secrets[]? | "'$ORG'/'$repo',repo,\(.name)"' >> "$OUTPUT" || true

    # Environment secrets
    gh api repos/$ORG/$repo/environments 2>/dev/null | \
      jq -r '.environments[]?.name' | \
      while read -r env; do
        gh api repos/$ORG/$repo/environments/$env/secrets 2>/dev/null | jq -r \
          '.secrets[]? | "'$ORG'/'$repo','$env',\(.name)"' >> "$OUTPUT" || true
      done
  done

echo "Audit written to $OUTPUT"
wc -l "$OUTPUT"
```

## Failed Run Notifier (Webhook)

```bash
#!/bin/bash
# notify-failures.sh — Check for recent failures and post to Slack
set -euo pipefail

REPO="org/infra"
SLACK_CHANNEL="#ci-alerts"
LOOKBACK_MINUTES=60

SINCE=$(date -d "$LOOKBACK_MINUTES minutes ago" +%Y-%m-%dT%H:%M:%SZ)

FAILURES=$(gh api "repos/$REPO/actions/runs?status=failure&per_page=10" | \
  jq --arg since "$SINCE" \
    '[.workflow_runs[] | select(.updated_at > $since) | {name: .name, id: .id, branch: .head_branch}]')

COUNT=$(echo "$FAILURES" | jq length)

if [ "$COUNT" -gt 0 ]; then
  MESSAGE="*$COUNT workflow failure(s) in the last ${LOOKBACK_MINUTES}m on \`$REPO\`*\n"
  while IFS= read -r run; do
    name=$(echo "$run" | jq -r .name)
    id=$(echo "$run" | jq -r .id)
    branch=$(echo "$run" | jq -r .branch)
    MESSAGE+="• $name ($branch): https://github.com/$REPO/actions/runs/$id\n"
  done < <(echo "$FAILURES" | jq -c '.[]')

  curl -s -X POST "https://slack.com/api/chat.postMessage" \
    -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"channel\": \"$SLACK_CHANNEL\", \"text\": \"$MESSAGE\"}"
fi
```

## Runner Auto-Registration Script

```bash
#!/bin/bash
# register-runner.sh — Register a new self-hosted runner
set -euo pipefail

REPO="${1:-org/infra}"
RUNNER_NAME="${2:-$(hostname)}"
RUNNER_LABELS="${3:-self-hosted,linux,prod}"
RUNNER_DIR="/home/github-runner/actions-runner"
RUNNER_VERSION="2.319.1"

# Download runner
mkdir -p "$RUNNER_DIR" && cd "$RUNNER_DIR"
curl -O -L "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"
tar xzf "actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"

# Get registration token
REG_TOKEN=$(gh api --method POST repos/$REPO/actions/runners/registration-token | jq -r .token)

# Configure runner
./config.sh \
  --url "https://github.com/$REPO" \
  --token "$REG_TOKEN" \
  --name "$RUNNER_NAME" \
  --labels "$RUNNER_LABELS" \
  --unattended \
  --replace

# Install and start service
sudo ./svc.sh install github-runner
sudo ./svc.sh start github-runner
sudo ./svc.sh status github-runner

echo "Runner $RUNNER_NAME registered and started."
```
