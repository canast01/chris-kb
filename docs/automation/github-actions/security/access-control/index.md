---
tags:
  - github-actions
  - security
---
# GitHub Actions — Access Control

```d2
direction: right

wfTrigger: "Workflow triggered" {shape: rectangle}
jobCtx: "Job context\nenvironment: production" {shape: rectangle}
secretCtx: "${{ secrets.X }}" {shape: rectangle}
envSecret: "Environment secret\nRequired reviewers enforced" {shape: rectangle}
repoSecret: "Repository secret\nAll workflows in repo" {shape: rectangle}
orgSecret: "Organisation secret\nGranted repos only" {shape: rectangle}
step: "Step — value masked as *** in logs" {shape: rectangle}

wfTrigger -> jobCtx
jobCtx -> secretCtx
envSecret -> secretCtx
repoSecret -> secretCtx
orgSecret -> secretCtx
secretCtx -> step
```

```text

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Workflow Permissions

```

```yaml
## Minimal permissions — default deny, grant explicitly
permissions:
  contents: read
  id-token: write    # only for OIDC jobs
  packages: write    # only for jobs pushing to GHCR

## Never use:
## permissions: write-all
```
```yaml
## Workflow — reference environment to trigger protection
jobs:
  deploy-prod:
    environment: production     # triggers protection rules + reviewer gate
    runs-on: ubuntu-24.04
    steps:
      - run: ./deploy.sh
        env:
          DB_PASSWORD: ${{ secrets.PROD_DB_PASSWORD }}
```
```yaml
## Restrict GITHUB_TOKEN to read-only by default (org or repo setting)
## Then grant write only where needed

permissions:
  contents: write       # only for release creation
  pull-requests: write  # only for PR comment bots
  issues: write         # only for issue management workflows
  packages: write       # only for container image publish
```
```bash
## Set default token permissions at org level
gh api --method PATCH orgs/ORG \
  -f members_can_create_repositories=false \
  --field default_workflow_permissions=read
```
```yaml
## Restrict which workflows can use self-hosted runners
## Settings → Actions → Runner groups → Restrict to selected repositories

## In workflow — target runner groups
runs-on:
  group: prod-runners          # named runner group
  labels: [self-hosted, linux]
```
```yaml
## Safe pattern — only run privileged jobs on self-hosted for protected branches
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: [self-hosted, linux, prod]
```
```bash
## Run runner as a dedicated non-root user
useradd -r -s /sbin/nologin -m -d /home/github-runner github-runner

## Ephemeral runners — register, run one job, deregister
./config.sh --ephemeral ...
## Prevents state accumulation between jobs

## Restrict runner network access (only allow required endpoints)
## github.com, api.github.com, objects.githubusercontent.com, *.actions.githubusercontent.com
```

```text title="Expected output"
useradd: warning: home directory '/home/github-runner' already exists and is not empty
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `useradd: user 'github-runner' already exists` | Check existing users with `getent passwd github-runner` and either remove the user with `userdel -r github-runner` or skip user creation if already present. |
    | `./config.sh: command not found` | Ensure you are in the GitHub Actions runner directory (typically `/opt/actions-runner` or similar) where `config.sh` is located, or provide the full path to the script. |
```bash
## Enable secret scanning and push protection via API
gh api --method PATCH repos/ORG/REPO \
  -f 'security_and_analysis[secret_scanning][status]=enabled' \
  -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'

## List alerts
gh api repos/ORG/REPO/secret-scanning/alerts | jq '.[] | {state, secret_type, html_url}'
```

```text title="Expected output"
{
  "state": "open",
  "secret_type": "github_pat",
  "html_url": "https://github.com/ORG/REPO/security/secret-scanning/1"
}
{
  "state": "open",
  "secret_type": "slack_bot_token",
  "html_url": "https://github.com/ORG/REPO/security/secret-scanning/2"
}
{
  "state": "resolved",
  "secret_type": "aws_access_key",
  "html_url": "https://github.com/ORG/REPO/security/secret-scanning/3"
}
{
  "state": "open",
  "secret_type": "private_key",
  "html_url": "https://github.com/ORG/REPO/security/secret-scanning/4"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `HTTP 403: Resource not accessible by integration` | Ensure the GitHub token has `repo` and `security_events:read` scopes, or use a PAT with appropriate permissions. |
    | `jq: parse error: Cannot index string with string "state"` | The API returned an error response instead of JSON array; verify the repository exists and secret scanning is enabled with `gh api repos/ORG/REPO | jq '.security_and_analysis'`. |
    | `HTTP 404: Not Found` | Replace `ORG/REPO` with actual organization and repository names, or verify the repository is accessible to the authenticated user. |
```bash
## Org audit log — all Actions-related events
gh api orgs/ORG/audit-log \
  --paginate \
  -f phrase="action:workflows" \
  -f per_page=100 \
  | jq '.[] | {action, actor, repo, created_at}'

## Filter for secret access events
gh api orgs/ORG/audit-log \
  -f phrase="action:org.actions_secret" \
  | jq '.[] | {action, actor, name: .config.secret_name}'
```
```yaml
## Mask a dynamically generated value
- name: Generate and mask token
  id: auth
  run: |
    TOKEN=$(get-token.sh)
    echo "::add-mask::$TOKEN"
    echo "token=$TOKEN" >> "$GITHUB_OUTPUT"

## Never echo secrets directly — even masked, the pattern is bad
## run: echo ${{ secrets.MY_SECRET }}   # ← avoid

## Use intermediate env vars
- name: Use secret safely
  run: ./script.sh
  env:
    SECRET: ${{ secrets.MY_SECRET }}   # referenced as $SECRET in script
```

---

## See also

- [GitHub Actions — Authentication](../authentication/)
- [GitHub Actions — Hardening](../hardening/)
- [GitHub Actions — Encryption](../encryption/)
