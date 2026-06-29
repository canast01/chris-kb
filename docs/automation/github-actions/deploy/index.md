---
tags:
  - deployment
  - github-actions
search:
  boost: 1.5
---
# GitHub Actions — Environment Setup

This guide walks through the initial setup of GitHub Actions for a repository: enabling
the feature, creating your first workflow, managing secrets and environments, adding
self-hosted runners, and enforcing status checks on protected branches.

---

```d2
direction: right

plan: "Plan" {shape: oval}
enable_github_actions_on_a_repositor: "Enable GitHub Actions on a Repository" {shape: rectangle}
create_the_workflow_directory: "Create the Workflow Directory" {shape: rectangle}
write_a_basic_ci_workflow: "Write a Basic CI Workflow" {shape: rectangle}
set_up_repository_secrets: "Set Up Repository Secrets" {shape: rectangle}
configure_environments_prodstaging: "Configure Environments (Prod/Staging)" {shape: rectangle}
set_up_a_selfhosted_runner: "Set Up a Self-Hosted Runner" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> enable_github_actions_on_a_repositor
enable_github_actions_on_a_repositor -> create_the_workflow_directory
create_the_workflow_directory -> write_a_basic_ci_workflow
write_a_basic_ci_workflow -> set_up_repository_secrets
set_up_repository_secrets -> configure_environments_prodstaging
configure_environments_prodstaging -> set_up_a_selfhosted_runner
set_up_a_selfhosted_runner -> validate
```

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


```text title="Expected output"
(no output — commands complete silently)
```

!!! warning "Common errors"
    **`mkdir: cannot create directory '.github/workflows': Permission denied`** — Run the command from a directory where you have write permissions, or use `sudo mkdir -p` if modifying a system directory.
    **`touch: cannot touch '.github/workflows/ci.yml': No such file or directory`** — Ensure the `.github/workflows` directory exists first by running `mkdir -p .github/workflows` before creating the file.
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


```text title="Expected output"
mkdir: created directory 'actions-runner'
  % Total    % Received % Xferd  Average Speed   Time    Current
                                 Dload  Upload   Speed
100   142M  100   142M    0     0  8.2M      0  0:00:17 0:00:17 --:--:-- 8.2M
√ Settings Configured for runner group Default
√ Runner connection is good
√ Runner registered successfully with name 'runner-ubuntu-22-04-001'
√ Current runner version: 2.311.0
√ Started listener process
√ Started running job: deploy-production-v1.2.3
√ Job completed with result: Succeeded
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to github.com port 443: Connection refused`** — Verify network connectivity and that the GitHub API endpoint is reachable from this host.
    **`./config.sh: line 42: ./bin/Runner.Listener: cannot execute binary file: Exec format error`** — Ensure you downloaded the correct runner architecture (x64, arm64, etc.) matching your system with `uname -m`.
    **`Error: Authentication failed. Invalid token or insufficient permissions.`** — Regenerate a new PAT or runner registration token in GitHub with appropriate scopes and pass it to the `--token` parameter.
4. Return to the **Runners** page and confirm the runner shows status **Idle**.

To run the runner as a service so it survives reboots:

```bash
sudo ./svc.sh install
sudo ./svc.sh start
```


```text title="Expected output"
Installing service...
Creating systemd unit file at /etc/systemd/system/github-actions-deploy.service
Reloading systemd daemon
Service installed successfully
Starting service...
Service started successfully
Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2s ago
PID: 8742
```

!!! warning "Common errors"
    **`sudo: ./svc.sh: command not found`** — Ensure you are in the correct directory where svc.sh is located and run `ls -la svc.sh` to verify the file exists.
    **`Permission denied`** — Make the script executable by running `chmod +x svc.sh` before executing it with sudo.
    **`Failed to start service: Unit github-actions-deploy.service failed to load`** — Check that the systemd unit file was created correctly with `sudo systemctl cat github-actions-deploy.service` and verify all paths in the unit file are absolute.
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

---

## See also

- [Github Actions — Procedures](../operations/procedures/)
- [Github Actions — Common Issues](../troubleshooting/common-issues/)
- [Github Actions — How It Works](../architecture/how-it-works/)
