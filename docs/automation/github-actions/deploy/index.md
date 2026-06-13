---
tags:
  - deployment
  - github-actions
---
# GitHub Actions — Environment Setup

This guide walks through the initial setup of GitHub Actions for a repository: enabling
the feature, creating your first workflow, managing secrets and environments, adding
self-hosted runners, and enforcing status checks on protected branches.

```text
┌───────────────────────────────── GitHub Actions — Environment Setup ──────────────────────────────────┐
│                                                                                                       │
│   GitHub Actions: CI/CD automation built into GitHub; no external CI server needed                    │
│   Workflows triggered by events: push, pull_request, schedule, workflow_dispatch                      │
│   Each workflow has jobs; each job runs on a runner and has a sequence of steps                       │
│   Config lives in .github/workflows/*.yml; multiple workflows per repo allowed                        │
│                                                                                                       │
│   Repository setup                                                                                    │
│   Enable: Settings → Actions → General → Allow all actions and reusable workflows                     │
│   Create .github/workflows/ directory at repo root; add workflow YAML files there                     │
│   First workflow: name, on (trigger), jobs, runs-on, steps with uses or run keys                      │
│                                                                                                       │
│   Secrets and environments                                                                            │
│   Repository secrets: Settings → Secrets and variables → Actions → New repository secret              │
│   Access in workflow: ${{ secrets.MY_SECRET_NAME }} — never echoed in logs                            │
│   Environments: add protection rules (manual approval, deployment branch restrictions)                │
│   Environment secrets override repository secrets when deploying to that environment                  │
│                                                                                                       │
│   Self-hosted runners                                                                                 │
│   Register: Settings → Actions → Runners → New self-hosted runner; follow install script              │
│   Runner labels: assign custom labels; target with runs-on: [self-hosted, linux, prod]                │
│   Runners need outbound TCP 443 to github.com; no inbound ports required                              │
│                                                                                                       │
│   Physical infrastructure                                                                             │
│   GitHub-hosted runners: Ubuntu/Windows/macOS VMs provisioned by GitHub per job                       │
│   Self-hosted runners: on-prem VM or container; persistent; accesses internal networks                │
│                                                                                                       │
│   Key terms:                                                                                          │
│   workflow     = YAML file in .github/workflows/; top-level unit of automation                        │
│   job          = a set of steps running on one runner; jobs run in parallel by default                │
│   step         = single task in a job: a shell command (run:) or an Action (uses:)                    │
│   Action       = reusable workflow component; from GitHub Marketplace or local path                   │
│   runner       = VM or container that executes jobs; GitHub-hosted or self-hosted                     │
│   event        = trigger that starts a workflow (push, PR, schedule, manual dispatch)                 │
│   environment  = named deployment target with protection rules and scoped secrets                     │
│   artifact     = file output of a job; passed between jobs via upload-artifact action                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Enable GitHub Actions on a Repository

1. Open the repository on GitHub.
2. Go to **Settings → Actions → General**.
3. Under **Actions permissions**, select **Allow all actions and reusable workflows**.
4. Click **Save**.

For organisations, the same policy is set at **Org Settings → Actions → Policies**.
Repository-level settings cannot exceed org-level permissions, so configure the org
policy first if individual repos appear locked.

---

## Create the Workflow Directory

GitHub Actions looks for workflow definitions in `.github/workflows/` at the root of
the repository. Create the directory and an initial workflow file:

```bash
mkdir -p .github/workflows
touch .github/workflows/ci.yml
```

Commit and push the directory. GitHub will begin scanning it for valid YAML files on
every push once at least one workflow file is present.

---

## Write a Basic CI Workflow

Paste the following into `.github/workflows/ci.yml` as a starting point:

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: echo "add your test command here"
```

Key fields to customise:

| Field | Purpose |
|---|---|
| `on` | Events that trigger the workflow (push, PR, schedule, etc.) |
| `runs-on` | Runner image (`ubuntu-latest`, `windows-latest`, `macos-latest`) |
| `uses` | Reusable action reference (org/repo@version) |
| `run` | Shell command executed on the runner |

Replace the `echo` line with your actual test or build command once the workflow
structure is confirmed working.

---

## Set Up Repository Secrets

Secrets are encrypted values injected into workflows at runtime. They are never
exposed in logs.

1. Go to **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Enter a name (e.g. `DOCKER_PASSWORD`) and the value.
4. Click **Add secret**.

Reference secrets in a workflow using the `secrets` context:

```yaml
- name: Log in to registry
  run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u myuser --password-stdin
```

Common secrets to add at this stage: container registry credentials, cloud provider
API keys, SSH deploy keys, and notification webhook URLs.

---

## Configure Environments (Prod/Staging)

Environments let you add approval gates and environment-scoped secrets for sensitive
deployment targets.

1. Go to **Settings → Environments → New environment**.
2. Name the environment (`production`, `staging`, etc.).
3. Add **protection rules**:
   - **Required reviewers** — one or more GitHub users must approve before the job runs.
   - **Deployment branch filter** — restrict to `main` or a release pattern.
4. Add **environment secrets** that override or supplement repository secrets for
   this target.

Reference an environment in a workflow job:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./deploy.sh
```

The job will pause and request reviewer approval before executing.

---

## Set Up a Self-Hosted Runner

Use a self-hosted runner when you need access to internal network resources,
specific hardware, or a locked-down OS image.

1. Go to **Settings → Actions → Runners → New self-hosted runner**.
2. Select the target OS and architecture.
3. Follow the displayed registration commands on the target machine:

```bash
# Example for Linux x64
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.x.x.tar.gz -L https://github.com/actions/runner/releases/download/...
tar xzf ./actions-runner-linux-x64-2.x.x.tar.gz
./config.sh --url https://github.com/ORG/REPO --token <TOKEN>
./run.sh
```

4. Return to the **Runners** page and confirm the runner shows status **Idle**.

To run the runner as a service so it survives reboots:

```bash
sudo ./svc.sh install
sudo ./svc.sh start
```

Label runners (e.g. `self-hosted`, `linux`, `gpu`) and reference them in workflows
with `runs-on: [self-hosted, linux]`.

---

## Configure Branch Protection with Status Checks

Require that CI passes before any pull request can be merged.

1. Go to **Settings → Branches → Add rule** (or edit an existing rule for `main`).
2. Enable **Require status checks to pass before merging**.
3. Search for and select the workflow job names you want to enforce (e.g. `build`).
4. Enable **Require branches to be up to date before merging** to prevent stale
   merges.
5. Optionally enable **Require a pull request before merging** and set a minimum
   reviewer count.
6. Click **Save changes**.

Status check names must match exactly. Run the workflow at least once so GitHub
registers the job names before you can add them as required checks.

---

## Validate the Pipeline

1. Push a commit (or open a pull request) to the repository.
2. Click the **Actions** tab on the repository page.
3. Locate the triggered workflow run and open it.
4. Verify each job and step completes with a green tick.
5. If a step fails, expand its log output to read the error message.
6. On a protected branch, confirm the pull request shows the required status check
   as passing before the merge button becomes active.

Common first-run issues:

| Symptom | Likely cause |
|---|---|
| Workflow not triggered | YAML syntax error or wrong trigger event |
| Secret not found | Secret name mismatch or wrong scope (repo vs environment) |
| Runner offline | Runner service not started or network blocked |
| Status check missing | Workflow never ran; push a commit to register the check name |

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation
