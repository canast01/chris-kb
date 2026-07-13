---
tags:
  - github-actions
  - operations
---
# GitHub Actions — Scripts

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
```


```text title="Expected output"
Rotating DEPLOY_SSH_KEY...
  ✓ DEPLOY_SSH_KEY rotated
Rotating AWS_SECRET_ACCESS_KEY...
  ✓ AWS_SECRET_ACCESS_KEY rotated
Rotating SLACK_BOT_TOKEN...
  ✓ SLACK_BOT_TOKEN rotated
All secrets rotated.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error making API request.` | Verify `VAULT_ROLE_ID` and `VAULT_SECRET_ID` environment variables are set and the AppRole auth method is enabled on the Vault instance. |
    | `Error: authentication required` | Ensure you are authenticated to GitHub CLI with `gh auth login` and have `admin:org_hook` permissions on the target repository. |
    | `jq: error (at <stdin>:1): Cannot index null with string "auth"` | Check that the Vault login response is valid JSON; confirm the Vault server is reachable at `VAULT_ADDR` and AppRole credentials are correct. |
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

```text title="Expected output"
Audit written to secret-audit-2025-01-15.csv
201 secret-audit-2025-01-15.csv
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: command not found` | Install the GitHub CLI with `brew install gh` (macOS) or `apt-get install gh` (Linux), then authenticate with `gh auth login`. |
    | `HTTP 403: Resource not accessible by integration` | Ensure your GitHub token has `admin:org_hook` and `repo` scopes by running `gh auth refresh -s admin:org_hook,repo`. |
    | `jq: parse error: Cannot index number with string "name"` | The API response is malformed; add error handling with `| jq -r '.secrets[]? // empty | ...'` to skip empty or non-object responses. |
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

```text title="Expected output"
[
  {
    "name": "build-and-test",
    "id": 8472651293,
    "branch": "main"
  },
  {
    "name": "security-scan",
    "id": 8472598447,
    "branch": "feature/auth-refactor"
  }
]
2 workflow failure(s) in the last 60m on `org/infra`
• build-and-test (main): https://github.com/org/infra/actions/runs/8472651293
• security-scan (feature/auth-refactor): https://github.com/org/infra/actions/runs/8472598447
{"ok":true,"channel":"C04K9QKBLP2","ts":"1699564892.001200","message":{"type":"message","user":"U05LMKQ8Z9P","text":"*2 workflow failure(s) in the last 60m on `org/infra`*\n• build-and-test (main): https://github.com/org/infra/actions/runs/8472651293\n• security-scan (feature/auth-refactor): https://github.com/org/infra/actions/runs/8472598447\n","bot_id":"B05LMKQ8Z9P"}}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: command not found` | Install the GitHub CLI with `brew install gh` (macOS) or `apt-get install gh` (Linux), then authenticate with `gh auth login`. |
    | `"error": "invalid_auth", "ok": false` | Verify the `SLACK_BOT_TOKEN` environment variable is set to a valid token and has `chat:write` scope in Slack workspace settings. |
    | `jq: parse error: Invalid numeric literal at line 1 column 7` | Ensure the GitHub API response is valid JSON by checking that `gh auth status` shows you are authenticated and the repo name is correct. |
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
- [GitHub Actions — CLI Reference](../cli-reference/)
- [GitHub Actions — Health Checks](../health-checks/)
