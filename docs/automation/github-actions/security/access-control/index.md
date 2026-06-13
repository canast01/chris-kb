---
tags:
  - github-actions
  - security
---
# GitHub Actions — Access Control

```mermaid
flowchart TD
    wfTrigger(["Workflow triggered"])
    jobCtx["Job context\nenvironment: production"]
    envSecret["Environment secret\nRequired reviewers enforced"]
    repoSecret["Repository secret\nAll workflows in repo"]
    orgSecret["Organisation secret\nGranted repos only"]
    secretCtx["${{ secrets.X }}"]
    step["Step — value masked as *** in logs"]

    wfTrigger --> jobCtx
    jobCtx --> secretCtx
    envSecret --> secretCtx
    repoSecret --> secretCtx
    orgSecret --> secretCtx
    secretCtx --> step
```
```text
┌─────────────────────────────────── GitHub Actions — Access Control ───────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     GitHub Actions access: who can trigger workflows, approve deployments, manage secrets     │   │
│   │    Repo permissions: read (view logs), write (trigger/cancel runs), admin (manage settings)   │   │
│   │  Environment protection: required reviewers, wait timers, branch restrictions for deployments │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Workflow Permissions             │  │              Environment Gates              │   │
│   │         GITHUB_TOKEN scoped per job          │  │          Required reviewers (team)          │   │
│   │        permissions: read-all default         │  │            Wait timer: 10 min min           │   │
│   │         Fork PRs: no secrets access          │  │        Branch restriction: main only        │   │
│   │         workflow_dispatch: user auth         │  │          Deployment logs: auditable         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      CODEOWNERS     = file mapping code paths to review teams; auto-request review on PR      │   │
│   │     Branch protection = require PR + CI pass + review before merge; enforces pipeline gate    │   │
│   │        Deployment review = env requires named team approval; reviewer approves/rejects        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

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
```bash
## Enable secret scanning and push protection via API
gh api --method PATCH repos/ORG/REPO \
  -f 'security_and_analysis[secret_scanning][status]=enabled' \
  -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'

## List alerts
gh api repos/ORG/REPO/secret-scanning/alerts | jq '.[] | {state, secret_type, html_url}'
```
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
