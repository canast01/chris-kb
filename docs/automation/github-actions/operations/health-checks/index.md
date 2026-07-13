---
tags:
  - github-actions
  - operations
description: "Health Checks reference covering Runner Health, Workflow Failures, Secrets and Credentials, Runner Resources."
---
# GitHub Actions — Health Checks

<div class="kb-summary">
Health Checks reference covering Runner Health, Workflow Failures, Secrets and Credentials, Runner Resources.

*Applies to: GitHub Actions*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
workflow_failures: "Workflow Failures" {shape: rectangle}
secrets_and_credentials: "Secrets and Credentials" {shape: rectangle}
runner_resources: "Runner Resources" {shape: rectangle}
daily_checks: "Daily Checks" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> workflow_failures
workflow_failures -> secrets_and_credentials
secrets_and_credentials -> runner_resources
runner_resources -> daily_checks
daily_checks -> verify
verify -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

```bash
# 1. Runner status
gh api /repos/<owner>/<repo>/actions/runners --jq '.runners[] | {name,status,busy}'

# 2. Failed workflows (last 24h)
gh run list --status failure --limit 20

# 3. Pending runs (stuck) — flag if any >30 min old
gh run list --status queued --limit 20

# 4. Secret expiry — review in UI
# Settings → Secrets and variables → Actions → check for expiring credentials

# 5. Runner disk space — SSH to self-hosted runner
df -h /

# 6. Workflow run minutes (billed plan)
gh api /repos/<owner>/<repo>/actions/billing/minutes
```


```text title="Expected output"
name                          status  busy
runner-ubuntu-01              online  false
runner-ubuntu-02              online  true
runner-macos-large            offline false
runner-windows-build-01       online  false

Showing 8 of 12 runs

STATUS  TITLE                              WORKFLOW           BRANCH
failure Deploy to production failed         deploy.yml         main
failure Unit tests timeout                 test.yml           develop
failure Docker build OOM                   build.yml          feature/api-v2

Showing 3 of 3 runs

STATUS  TITLE                              WORKFLOW           BRANCH
queued  Integration tests                  test.yml           main
queued  Security scan                      security.yml       develop

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1      100G   87G   8.2G  92% /

{
  "total_billable_minutes": 1250,
  "total_paid_minutes": 0,
  "ubuntu_minutes": 850,
  "macos_minutes": 400,
  "windows_minutes": 0
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: repository not found` | Replace `<owner>/<repo>` with actual repository path (e.g., `myorg/myrepo`). |
    | `Error: Not Authorized to access this endpoint` | Ensure your GitHub token has `repo` and `admin:repo_hook` scopes via `gh auth refresh -s repo,admin:repo_hook`. |
    | `No space left on device` | Runner disk is critically full at 92%; SSH to the runner and delete old workflow artifacts or increase disk allocation immediately. |
**List runners at the organisation level**

```bash
gh api /orgs/<org>/actions/runners --jq '.runners[] | {name,status,busy}'
```


```text title="Expected output"
{
  "name": "runner-prod-01",
  "status": "online",
  "busy": false
}
{
  "name": "runner-prod-02",
  "status": "online",
  "busy": true
}
{
  "name": "runner-staging-01",
  "status": "offline",
  "busy": false
}
{
  "name": "runner-docker-build-01",
  "status": "online",
  "busy": false
}
{
  "name": "runner-docker-build-02",
  "status": "online",
  "busy": true
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `HTTP 404: Not Found (https://api.github.com/orgs/<org>/actions/runners)` | Replace `<org>` with your actual organization name. |
    | `Must have admin or "manage runners" permissions to access this endpoint` | Ensure your GitHub token has `admin:org_hook` and `admin:org` scopes, or request elevated permissions from an org owner. |
**Check runner version (outdated runners may stop receiving jobs)**

```bash
gh api /repos/<owner>/<repo>/actions/runners --jq '.runners[] | {name,runner_version}'
```


```text title="Expected output"
{
  "name": "runner-ubuntu-01",
  "runner_version": "2.311.0"
}
{
  "name": "runner-ubuntu-02",
  "runner_version": "2.311.0"
}
{
  "name": "runner-macos-01",
  "runner_version": "2.310.2"
}
{
  "name": "runner-windows-01",
  "runner_version": "2.311.0"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: Unauthorized` | Verify your GitHub token has `admin:org_hook` and `repo` scopes by running `gh auth status`. |
    | `HTTP 404: Not Found` | Confirm the owner and repo placeholders are replaced with actual values and the repository exists. |
**Remove a stale offline runner**

```bash
gh api --method DELETE /repos/<owner>/<repo>/actions/runners/<runner-id>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `HTTP 404: Not Found` | Verify the runner ID exists with `gh api /repos/<owner>/<repo>/actions/runners` and confirm the owner and repo names are correct. |
    | `HTTP 403: Forbidden` | Ensure your GitHub token has `admin:org_hook` and `repo` permissions by checking `gh auth status`. |
**Verify runner labels match workflow `runs-on` values**

```bash
# Compare runner labels from API output against runs-on values in workflow files
gh api /repos/<owner>/<repo>/actions/runners --jq '.runners[] | .labels[].name' | sort -u
grep -r "runs-on:" .github/workflows/ | awk '{print $NF}' | sort -u
```


```text title="Expected output"
# First command output (runner labels from API):
ubuntu-latest
ubuntu-20.04
ubuntu-22.04
windows-latest
macos-latest
custom-docker
self-hosted

# Second command output (runs-on values from workflows):
macos-latest
self-hosted
ubuntu-20.04
ubuntu-22.04
ubuntu-latest
windows-latest
custom-docker
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: command not found` | Install the GitHub CLI with `brew install gh` (macOS) or `apt-get install gh` (Linux), then authenticate with `gh auth login`. |
    | `fatal: not a git repository` | Run the commands from the root directory of your cloned repository, or use `cd /path/to/repo` first. |
    | `HTTP 401: Bad credentials` | Re-authenticate with `gh auth logout && gh auth login` and ensure your token has `repo:read` and `admin:org_hook` scopes. |
**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Runner status | `online` | Restart runner service on host |
| Runner busy | Some idle capacity | Add runners if all are perpetually busy |
| Runner version | Current | Update runner application on host |
| Runner labels | Match workflow `runs-on` | Fix labels or update workflow |
| Offline duration | <5 minutes | Investigate host availability |

---

## Workflow Failures

Workflow failures should be investigated promptly. Recurring failures in the same workflow indicate a systemic issue rather than a transient one.

**List recent failed runs**

```bash
gh run list --status failure --limit 20
```


```text title="Expected output"
STATUS  CONCLUSION  NAME                                    WORKFLOW             RUN ID      CREATED AT
failure failure     Deploy to Production                    deploy.yml           8934521098  2024-01-15T14:32:10Z
failure failure     Unit Tests - Python 3.11               test.yml             8934501234  2024-01-15T13:45:22Z
failure failure     Security Scan                          security.yml         8934487654  2024-01-15T12:18:09Z
failure failure     Build Docker Image                     build.yml            8934472891  2024-01-15T11:05:33Z
failure failure     Integration Tests                      integration.yml      8934456723  2024-01-15T09:52:47Z
failure failure     Lint and Format Check                  lint.yml             8934441098  2024-01-15T08:30:15Z
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: command not found` | Install the GitHub CLI with `brew install gh` (macOS) or `apt-get install gh` (Linux), then authenticate with `gh auth login`. |
    | `HTTP 401: Bad credentials` | Re-authenticate with `gh auth login` and ensure your token has `actions:read` permissions. |
    | `HTTP 403: Resource not accessible by integration` | Verify the repository is accessible and your GitHub token has sufficient permissions for the target repository. |
**View details of a specific failed run**

```bash
gh run view <run-id>
```


```text title="Expected output"
✓ COMPLETED in 2m15s
  status: completed
  conclusion: success
  event: push
  branch: main
  commit: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
  author: devops-bot
  created_at: 2024-01-15T09:42:18Z
  updated_at: 2024-01-15T09:44:33Z
  
Jobs:
ID                    NAME                STATUS    CONCLUSION  STARTED             DURATION
1234567890            build-and-test      completed success     09:42:25Z           1m32s
1234567891            deploy-staging      completed success     09:44:01Z           43s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `HTTP 404: Not Found` | Verify the run ID is correct and exists in your repository with `gh run list`. |
    | `Error: no GitHub token found` | Authenticate with `gh auth login` or ensure the `GITHUB_TOKEN` environment variable is set. |
**View logs for a failed run**

```bash
gh run view <run-id> --log-failed
```


```text title="Expected output"
Run <run-id> completed with 1 failure

FAILED ✗ Build and push Docker image
  └─ docker build failed: no space left on device

Log (last 50 lines):
  Step 1/15 : FROM ubuntu:22.04
  Step 2/15 : RUN apt-get update && apt-get install -y curl
  Step 3/15 : COPY . /app
  Step 4/15 : WORKDIR /app
  Step 5/15 : RUN npm install
  Step 6/15 : RUN npm run build
  docker: Error response from daemon: no space left on device
  
Workflow: CI/CD Pipeline
Commit: a3f8e2c1 (main)
Author: devops-team
Created: 2024-01-15T09:42:31Z
Duration: 4m 23s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: the specified run was not found` | Verify the run ID is correct by listing recent runs with `gh run list`. |
    | `Error: authentication required` | Authenticate with GitHub CLI using `gh auth login` and ensure you have access to the repository. |
**List failed runs for a specific workflow**

```bash
gh run list --workflow <workflow-filename.yml> --status failure --limit 20
```


```text title="Expected output"
STATUS  CONCLUSION  NAME                                    WORKFLOW             RUN ID      CREATED AT
failure failure     Deploy to production - retry #3         deploy.yml           1234567890  2024-01-15T14:32:18Z
failure failure     Deploy to production - retry #2         deploy.yml           1234567889  2024-01-15T14:28:45Z
failure failure     Build and test suite                    deploy.yml           1234567888  2024-01-15T14:15:22Z
failure failure     Security scan - timeout                 deploy.yml           1234567887  2024-01-15T13:52:10Z
failure failure     Integration tests failed                deploy.yml           1234567886  2024-01-15T13:41:33Z
failure failure     Docker image push failed                deploy.yml           1234567885  2024-01-15T13:28:19Z
failure failure     Deployment validation error             deploy.yml           1234567884  2024-01-15T13:15:07Z
failure failure     Unit tests - flaky assertion            deploy.yml           1234567883  2024-01-15T12:52:41Z
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: command not found` | Install the GitHub CLI with `brew install gh` (macOS) or `apt-get install gh` (Linux), then authenticate with `gh auth login`. |
    | `HTTP 401: Bad credentials` | Re-authenticate with `gh auth logout && gh auth login` and ensure your token has `actions:read` permissions. |
    | `no workflows found` | Verify the workflow filename matches exactly (case-sensitive) and exists in `.github/workflows/` directory with `gh workflow list`. |
**Check if a workflow is disabled**

```bash
gh workflow list
```


```text title="Expected output"
NAME                                STATE      CREATED             UPDATED
Build and Deploy                    active     2024-01-15 09:23    2024-01-20 14:47
Security Scan                       active     2024-01-10 11:05    2024-01-19 22:31
Unit Tests                          active     2024-01-08 16:42    2024-01-21 08:15
Integration Tests                   active     2024-01-12 13:28    2024-01-20 19:44
Dependency Check                    disabled   2024-01-05 10:11    2024-01-18 15:22
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: command not found` | Install GitHub CLI with `brew install gh` (macOS) or `apt-get install gh` (Linux), then authenticate with `gh auth login`. |
    | `HTTP 401: Unauthorized` | Re-authenticate with `gh auth login` or verify your token has `workflow` scope permissions. |
A workflow marked `disabled` will not trigger. Re-enable with `gh workflow enable <workflow-name>`.

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Failure rate | <5% over 7 days | Investigate recurring failures |
| Queued duration | <5 minutes | Check runner availability |
| Cancelled runs | Occasional (manual) | Investigate if systematic |
| Disabled workflows | None unexpected | Re-enable or document intentional disablement |

---

## Secrets and Credentials

Expired or missing secrets cause silent authentication failures during workflow runs. Secrets should be audited on a regular cadence.

**List secrets configured for a repository**

```bash
gh secret list
```


```text title="Expected output"
NAME                                UPDATED
DOCKER_REGISTRY_PASSWORD            about 2 days ago
DOCKER_REGISTRY_USERNAME            about 2 days ago
SLACK_WEBHOOK_URL                   about 5 days ago
SONARQUBE_TOKEN                     about 1 week ago
AWS_ACCESS_KEY_ID                   about 2 weeks ago
AWS_SECRET_ACCESS_KEY               about 2 weeks ago
GITHUB_TOKEN                        about 3 weeks ago
NPM_REGISTRY_TOKEN                  about 1 month ago
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: command not found` | Install the GitHub CLI with `brew install gh` (macOS) or `apt-get install gh` (Linux), then authenticate with `gh auth login`. |
    | `Error: SilentCommandError` | Ensure you are authenticated by running `gh auth status` and re-authenticate with `gh auth login` if needed. |
This shows secret names only — values are never returned by the API.

**List organisation-level secrets**

```bash
gh secret list --org <org>
```


```text title="Expected output"
NAME                                UPDATED AT
DOCKER_REGISTRY_PASSWORD            2024-01-15T09:32:14Z
SLACK_WEBHOOK_URL                   2024-01-15T08:47:22Z
SONARQUBE_TOKEN                     2024-01-14T16:21:09Z
AWS_ACCESS_KEY_ID                   2024-01-14T14:55:33Z
GITHUB_TOKEN                        2024-01-13T11:03:18Z
NPM_REGISTRY_TOKEN                  2024-01-12T09:18:45Z
DATADOG_API_KEY                     2024-01-11T13:42:07Z
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: HTTP 404: Not Found (https://api.github.com/orgs/<org>/actions/secrets)` | Verify the organization name is correct and you have access to it with `gh auth status`. |
    | `Error: authentication required` | Authenticate with GitHub CLI using `gh auth login` and ensure your token has `admin:org_hook` scope. |
**Check environment secrets**

```bash
gh secret list --env <environment-name>
```


```text title="Expected output"
NAME                                UPDATED AT
DOCKER_REGISTRY_PASSWORD            2024-01-15T09:42:31Z
SLACK_WEBHOOK_URL                   2024-01-15T08:17:22Z
DATABASE_CONNECTION_STRING          2024-01-14T16:53:09Z
KUBE_CONFIG_BASE64                  2024-01-14T11:28:45Z
API_KEY_PRODUCTION                  2024-01-13T14:05:33Z
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: environment not found` | Verify the environment name exists in the repository by running `gh repo view --json environments`. |
    | `Error: authentication required` | Ensure you are authenticated with `gh auth login` and have appropriate permissions for the repository. |
**Identify expiring credentials (manual check)**

Navigate to **Settings → Secrets and variables → Actions** and review each secret's purpose and expected expiry date against your credential rotation schedule.

**Update a secret**

```bash
gh secret set <SECRET_NAME> --body "<new-value>"
```


```text title="Expected output"
✓ Set secret <SECRET_NAME> for repository owner/repo-name
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gh: command not found` | Install GitHub CLI with `brew install gh` (macOS) or `apt-get install gh` (Linux), then authenticate with `gh auth login`. |
    | `HTTP 404: Not Found` | Verify the repository exists and you have push access by running `gh repo view` to confirm your current repository context. |
    | `parsing failed: invalid value for '--body' flag` | Ensure the secret value is properly quoted and doesn't contain unescaped special characters; use single quotes or escape double quotes with backslashes. |
**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Required secrets present | All expected secrets listed | Add missing secrets |
| Credential expiry | >30 days remaining | Rotate and update secret value |
| Scope | Repo or environment scoped | Audit org-level secrets for over-broad access |
| Unused secrets | None | Remove orphaned secrets |

---

## Runner Resources

Self-hosted runner hosts require adequate disk, CPU, and memory. Resource exhaustion causes job failures and may leave workspace directories filling up the disk.

**Check disk space on runner host**

```bash
df -h /
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   32G   18G  64% /
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `df: '/': No such file or directory` | Verify the mount point exists and the filesystem is mounted with `mount | grep " / "`. |
    | `Permission denied` | Run the command with appropriate privileges using `sudo df -h /` if access is restricted. |
Alert if usage exceeds 80%. Runner workspace directories at `_work/` accumulate artefacts from past runs.

**Clean up stale runner workspaces**

```bash
# List workspace directories older than 7 days
find /home/runner/_work -maxdepth 2 -type d -mtime +7

# Remove stale workspaces (run with caution — confirm no active jobs)
find /home/runner/_work -maxdepth 2 -type d -mtime +7 -exec rm -rf {} +
```


```text title="Expected output"
/home/runner/_work/repo-service/repo-service
/home/runner/_work/api-gateway/api-gateway
/home/runner/_work/data-pipeline/data-pipeline
/home/runner/_work/legacy-batch/legacy-batch
/home/runner/_work/monitoring-stack/monitoring-stack
/home/runner/_work/deprecated-tools/deprecated-tools
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `find: '/home/runner/_work/repo-service/repo-service': Permission denied` | Run the command with `sudo` or ensure the runner user has read permissions on all workspace directories. |
    | `rm: cannot remove '/home/runner/_work/api-gateway/api-gateway': Directory not empty` | Verify no active GitHub Actions jobs are using these directories before running the removal command. |
**Check runner service status**

```bash
# systemd-based runner
systemctl status actions.runner.<owner>.<repo>.<runner-name>.service
```


```text title="Expected output"
● actions.runner.acme-corp.deployment-api.runner-01.service - GitHub Actions Runner
     Loaded: loaded (/etc/systemd/system/actions.runner.acme-corp.deployment-api.runner-01.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2 days ago
       Docs: https://github.com/actions/runner
    Process: 8472 ExecStart=/home/runner/actions-runner/run.sh (code=exited, status=0/SUCCESS)
   Main PID: 8473 (Runner.Listener)
      Tasks: 12 (limit: 4096)
     Memory: 287.3M
     CGroup: /system.slice/actions.runner.acme-corp.deployment-api.runner-01.service
             └─8473 /home/runner/actions-runner/bin/Runner.Listener run --startuptype service

Jan 15 14:32:18 runner-host-01 systemd[1]: Started GitHub Actions Runner.
Jan 15 14:35:42 runner-host-01 Runner.Listener[8473]: Current runner version: '2.311.0'
Jan 15 14:35:43 runner-host-01 Runner.Listener[8473]: Runner registration complete
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unit actions.runner.acme-corp.deployment-api.runner-01.service could not be found.` | Verify the service name matches the runner configuration and check `/etc/systemd/system/` for the correct `.service` file. |
    | `Failed to get unit file state for actions.runner.acme-corp.deployment-api.runner-01.service: No such file or directory` | Run `systemctl daemon-reload` after creating or modifying the service file, then retry the status command. |
**Check runner process is active**

```bash
ps aux | grep Runner.Listener
```


```text title="Expected output"
root      12847  0.1  0.3 1245680 98432 ?       Ssl  14:23   0:45 /opt/actions-runner/_work/_tool/Runner.Listener/2.314.1/Runner.Listener run --startuptype service
runner    12891  0.0  0.2 892456 65120 ?        Sl   14:23   0:12 /opt/actions-runner/_work/_tool/Runner.Listener/2.314.1/Runner.Listener
root      13045  0.0  0.0  6408  2104 pts/0    S+   14:28   0:00 grep --color=auto Runner.Listener
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: (standard input): No such device or address` | Ensure the pipe is correctly formed and the `ps` command completes successfully before piping to `grep`. |
    | `No such file or directory` | Verify the GitHub Actions runner is installed at `/opt/actions-runner/` and the Runner.Listener binary exists at the expected version path. |
**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Disk usage | <80% | Clean `_work/` directories or expand disk |
| Runner service | `active (running)` | Restart service; check logs for crash reason |
| CPU during jobs | <90% sustained | Reduce job concurrency or upgrade host |
| Memory | No OOM events | Review job resource requirements |
| Network | Low latency to GitHub | Investigate if jobs are timing out on checkout |

---

## Daily Checks

```bash
# Validate using ajv-cli against the schema
npm install -g ajv-cli
ajv validate \
  -s https://json.schemastore.org/github-workflow.json \
  -d .github/workflows/ci.yml
```


```text title="Expected output"
npm WARN deprecated ajv-cli@5.0.0: ajv-cli is deprecated. Please use ajv package with CLI from ajv/cli
added 47 packages, and audited 48 packages in 2.3s

found 0 vulnerabilities
.github/workflows/ci.yml valid
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ajv: command not found` | Run `npm install -g ajv-cli` before attempting validation, or use `npx ajv` instead. |
    | `.github/workflows/ci.yml invalid` | Review the workflow file for schema violations (missing required fields, incorrect indentation, or unsupported keys) and consult the GitHub Actions workflow syntax documentation. |
### Required Status Checks

Configure branch protection to require workflow jobs to pass before merging.

```bash
# Enable branch protection with required checks via gh CLI
gh api --method PUT /repos/OWNER/REPO/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["build", "test (3.11)", "test (3.12)"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1
  },
  "restrictions": null
}
EOF
```


```text title="Expected output"
{
  "url": "https://api.github.com/repos/acme-corp/deploy-service/branches/main/protection",
  "required_status_checks": {
    "url": "https://api.github.com/repos/acme-corp/deploy-service/branches/main/protection/required_status_checks",
    "strict": true,
    "contexts": [
      "build",
      "test (3.11)",
      "test (3.12)"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "url": "https://api.github.com/repos/acme-corp/deploy-service/branches/main/protection/required_pull_request_reviews",
    "required_approving_review_count": 1
  },
  "restrictions": null
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `HTTP 404: Not Found` | Verify the OWNER and REPO values match your repository path exactly, and that the branch exists. |
    | `HTTP 403: Forbidden` | Ensure your GitHub token has `admin:repo_hook` and `repo` scopes, or use `gh auth login` to re-authenticate with proper permissions. |
    | `HTTP 422: Unprocessable Entity` | Confirm that all status check contexts in the "contexts" array match the exact names of checks configured in your CI/CD workflows. |
### Validating Workflows in CI

Run actionlint automatically as part of the CI pipeline.

```yaml
# .github/workflows/lint-workflows.yml
name: Lint Workflows

on:
  pull_request:
    paths:
      - '.github/workflows/**'

jobs:
  actionlint:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4

      - name: Run actionlint
        uses: rhysd/actionlint@v1
        with:
          fail-on-error: true
```

### Common Validation Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `unexpected key "enviroment"` | Typo in key name | Fix spelling — schema check catches this |
| `expression syntax error` | Malformed `${{ }}` expression | Validate expression brackets and quotes |
| `"on" is required` | Missing trigger | Add `on:` block |
| `job ID must match pattern` | Job name has spaces | Use hyphens: `my-job` not `my job` |
| `uses: action@` missing version | Unpinned action | Append version tag: `@v4` |
| Workflow never runs | `on.paths` filter mismatch | Test with `act` or temporarily broaden filter |

### Pinning Action Versions

```yaml
# Avoid using @main or @master — pin to a specific tag or SHA
steps:
  - uses: actions/checkout@v4           # semver tag (recommended)
  - uses: actions/setup-python@v5

  # For maximum security, pin to the commit SHA
  - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    groups:
      actions:
        patterns: ["*"]
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [GitHub Actions — Procedures](../procedures/)
- [GitHub Actions — CLI Reference](../cli-reference/)
- [GitHub Actions — Common Issues](../../troubleshooting/common-issues/)
