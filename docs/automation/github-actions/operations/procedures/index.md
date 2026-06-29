---
tags:
  - github-actions
  - operations
---
# GitHub Actions — Procedures

<div class="kb-summary">
GitHub Actions procedures: creating workflows, configuring environments, managing self-hosted runners, rotating secrets, and monitoring job execution in the Actions console.

*Applies to: GitHub Actions*
</div>

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Workflows

```d2
direction: right

trigger: "Trigger Event\npush / pull_request\nschedule / workflow_dispatch" {shape: rectangle}
runner: "Runner\nubuntu-24.04\nself-hosted" {shape: rectangle}
jobA: "Job: build\nCheckout → Install → Test → Build" {shape: rectangle}
jobB: "Job: test\nmatrix: OS × Python version" {shape: rectangle}
artifacts: "Artifacts\ndist/ packages\ntest reports" {shape: rectangle}
jobC: "Job: publish\nneeds: build\nenvironment: pypi" {shape: rectangle}
deploy: "Deploy\n./deploy.sh\nor OIDC cloud publish" {shape: rectangle}

trigger -> runner
runner -> jobA
runner -> jobB
jobA -> artifacts
artifacts -> jobC
jobB -> jobC
jobC -> deploy
```

```bash
# .github/workflows/main.yml (calling workflow)
jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
    secrets:
      deploy_key: ${{ secrets.STAGING_DEPLOY_KEY }}
```

### Concurrency Control

Prevent duplicate workflow runs for the same branch or PR.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true   # cancel older runs when a new one starts

# Per-job concurrency
jobs:
  deploy:
    concurrency:
      group: deploy-${{ github.ref }}
      cancel-in-progress: false  # queue deploys rather than cancel
```

### workflow_dispatch and Manual Triggers

```yaml
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy'
        required: true
        type: string
      dry_run:
        description: 'Perform a dry run'
        required: false
        type: boolean
        default: false
      environment:
        description: 'Target environment'
        type: choice
        options: [staging, production]
        default: staging

jobs:
  deploy:
    runs-on: ubuntu-24.04
    steps:
      - run: |
          echo "Deploying version ${{ inputs.version }}"
          echo "Dry run: ${{ inputs.dry_run }}"
          echo "Target: ${{ inputs.environment }}"
```

```bash
# Trigger manually via gh CLI
gh workflow run deploy.yml \
  --field version=1.2.3 \
  --field environment=staging \
  --field dry_run=false
```

### Workflow Feature Reference

| Feature | Syntax | Purpose |
|---|---|---|
| Job dependency | `needs: [build, test]` | Run after listed jobs succeed |
| Conditional | `if: github.ref == 'refs/heads/main'` | Skip job/step conditionally |
| Timeout | `timeout-minutes: 15` | Kill if job runs too long |
| Continue on error | `continue-on-error: true` | Mark step failure as warning |
| Strategy | `strategy.matrix` | Fan out across value combinations |
| Outputs | `outputs.key: ${{ steps.id.outputs.key }}` | Pass data between jobs |
| Composite action | `using: composite` | Bundle steps into a reusable action |

### Composite Actions

```yaml
# .github/actions/setup-env/action.yml
name: Setup Environment
description: Install tools and cache dependencies

inputs:
  python-version:
    description: Python version
    default: '3.12'

runs:
  using: composite
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}
        cache: pip
    - run: pip install -r requirements.txt
      shell: bash
```

## Builds

### Workflow Triggers

Workflows are triggered by events defined under the `on:` key.

```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'tests/**'
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1-5'   # weekdays at 06:00 UTC
  workflow_dispatch:          # manual trigger
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: staging
        type: choice
        options: [staging, production]
```

### Jobs and Steps

```yaml
jobs:
  build:
    name: Build application
    runs-on: ubuntu-24.04
    timeout-minutes: 30

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest tests/ -v --tb=short

      - name: Build package
        run: python -m build
```

### Artifacts

Upload build outputs to persist them between jobs or download after a workflow run.

```yaml
      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist-packages
          path: dist/
          retention-days: 7
          if-no-files-found: error

  deploy:
    needs: build
    runs-on: ubuntu-24.04
    steps:
      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist-packages
          path: dist/
```

### Matrix Builds

```mermaid
flowchart LR
    trigger(["push to main"])
    matrixJob["Job: test\nstrategy.matrix"]

    subgraph "ubuntu-24.04"
        u310["Python 3.10"]
        u311["Python 3.11"]
        u312["Python 3.12"]
    end
    subgraph "windows-latest"
        w311["Python 3.11"]
        w312["Python 3.12"]
    end
    subgraph "macos-latest"
        m311["Python 3.11"]
        m312["Python 3.12"]
    end

    trigger --> matrixJob
    matrixJob --> u310
    matrixJob --> u311
    matrixJob --> u312
    matrixJob --> w311
    matrixJob --> w312
    matrixJob --> m311
    matrixJob --> m312
```

Matrix strategy runs the same job across multiple combinations of parameters.

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-24.04, windows-latest, macos-latest]
        python: ['3.10', '3.11', '3.12']
        exclude:
          - os: macos-latest
            python: '3.10'

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install -r requirements.txt && pytest
```

### Key Build Concepts

| Concept | Description |
|---|---|
| `needs` | Job dependency — wait for listed jobs to succeed |
| `if` | Conditional job/step execution |
| `timeout-minutes` | Kill job if it exceeds this duration |
| `continue-on-error` | Mark step failure as non-fatal |
| `env` | Environment variables for the job or step |
| `outputs` | Pass values from one job to another |

### Passing Outputs Between Jobs

```yaml
jobs:
  build:
    runs-on: ubuntu-24.04
    outputs:
      version: ${{ steps.get_version.outputs.version }}
    steps:
      - name: Get version
        id: get_version
        run: echo "version=$(cat VERSION)" >> "$GITHUB_OUTPUT"

  deploy:
    needs: build
    runs-on: ubuntu-24.04
    steps:
      - name: Use version
        run: echo "Deploying version ${{ needs.build.outputs.version }}"
```

## Publishing

### PyPI Publishing

Publish Python packages to PyPI using OIDC trusted publishing — no long-lived tokens required.

```yaml
# .github/workflows/publish-pypi.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install build && python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish:
    needs: build
    runs-on: ubuntu-24.04
    environment: pypi
    permissions:
      id-token: write   # required for OIDC
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - uses: pypa/gh-action-pypi-publish@release/v1
```

### Docker Hub Publishing

```yaml
# .github/workflows/docker-publish.yml
name: Build and Push Docker Image

on:
  push:
    tags: ['v*.*.*']

jobs:
  docker:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myorg/myapp
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### GitHub Packages (Container Registry)

```yaml
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push to GHCR
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### Release Workflows

Automate GitHub Release creation including changelog generation.

```yaml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-24.04
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses: orhun/git-cliff-action@v3
        with:
          config: cliff.toml
          args: --current --strip header

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.content }}
          files: dist/*
          draft: false
          prerelease: ${{ contains(github.ref, '-rc') || contains(github.ref, '-beta') }}
```

### Publishing Target Comparison

| Target | Auth method | Trigger | Key action |
|---|---|---|---|
| PyPI | OIDC trusted publishing | Release published | `pypa/gh-action-pypi-publish` |
| Docker Hub | Username + access token secret | Tag push | `docker/build-push-action` |
| GHCR | `GITHUB_TOKEN` (built-in) | Tag push | `docker/build-push-action` |
| GitHub Release | `GITHUB_TOKEN` with `contents: write` | Tag push | `softprops/action-gh-release` |
| npm | `NODE_AUTH_TOKEN` secret | Release published | `npm publish` in run step |

## Validation

### Linting Workflow Files with actionlint

`actionlint` is a static analysis tool for GitHub Actions workflow YAML files.

```bash
# Install actionlint (macOS)
brew install actionlint

# Lint all workflows in the current repository
actionlint

# Lint a specific file
actionlint .github/workflows/ci.yml

# Output as JSON for integration with other tools
actionlint -format '{{json .}}'

# Ignore a specific rule
actionlint -ignore 'expression syntax error'

# Run inside a Docker container (no install required)
docker run --rm -v "$(pwd):/repo" --workdir /repo \
  rhysd/actionlint:latest
```

### Schema Validation

VS Code and JetBrains IDEs provide schema-based validation when the schema URL is declared.

```yaml
# Add to the top of any workflow file for IDE validation
# yaml-language-server: $schema=https://json.schemastore.org/github-workflow.json
---
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
```

```bash
# Validate using ajv-cli against the schema
npm install -g ajv-cli
ajv validate \
  -s https://json.schemastore.org/github-workflow.json \
  -d .github/workflows/ci.yml
```

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

## Configure a Self-Hosted Runner

Settings → Actions → Runners → New self-hosted runner → choose OS → follow registration commands → verify runner shows Online.

```bash
# Example registration (Linux)
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.x.x.tar.gz -L https://github.com/actions/runner/releases/download/v2.x.x/actions-runner-linux-x64-2.x.x.tar.gz
tar xzf ./actions-runner-linux-x64-2.x.x.tar.gz

# Configure the runner (token from Settings → Actions → Runners → New runner)
./config.sh --url https://github.com/OWNER/REPO --token <REGISTRATION_TOKEN>

# Start as a service
sudo ./svc.sh install
sudo ./svc.sh start

# Verify runner status in Settings → Actions → Runners (should show Online)
```

| Step | Command / Location |
|---|---|
| Get registration token | Settings → Actions → Runners → New self-hosted runner |
| Configure | `./config.sh --url <repo-url> --token <token>` |
| Install as service | `sudo ./svc.sh install && sudo ./svc.sh start` |
| Verify | Settings → Actions → Runners → runner shows **Online** |

## Set Up Environment Protection Rules

Settings → Environments → New environment → add required reviewers → configure wait timer → restrict to specific branches.

```bash
# Configure via gh CLI
gh api --method PUT /repos/OWNER/REPO/environments/production \
  --input - <<'EOF'
{
  "wait_timer": 10,
  "reviewers": [
    {"type": "User", "id": 12345}
  ],
  "deployment_branch_policy": {
    "protected_branches": true,
    "custom_branch_policies": false
  }
}
EOF
```

```yaml
# Reference the environment in a workflow job
jobs:
  deploy:
    environment:
      name: production
      url: https://example.com
    runs-on: ubuntu-24.04
    steps:
      - run: ./deploy.sh
```

| Setting | Purpose |
|---|---|
| Required reviewers | Named users or teams must approve before the job runs |
| Wait timer | Delay (minutes) between approval and job start |
| Branch restrictions | Only allow deployments from protected branches or named patterns |

## Debug a Failing Workflow

Actions → select failed run → expand failing step → review logs → add `ACTIONS_STEP_DEBUG: true` secret for verbose output → re-run.

```bash
# Enable debug logging via gh CLI (set as a secret)
gh secret set ACTIONS_STEP_DEBUG --body "true"
gh secret set ACTIONS_RUNNER_DEBUG --body "true"

# Re-run only the failed jobs (preserves passing jobs)
gh run rerun <run-id> --failed

# Stream live logs for a running workflow
gh run watch <run-id>

# Download logs for offline inspection
gh run download <run-id> --dir ./run-logs
```

```yaml
# Add temporary debug step to a failing job
- name: Debug environment
  run: |
    echo "Runner OS: ${{ runner.os }}"
    echo "GitHub ref: ${{ github.ref }}"
    env | sort
```

| Debug technique | When to use |
|---|---|
| `ACTIONS_STEP_DEBUG: true` secret | Need verbose runner and step output |
| `ACTIONS_RUNNER_DEBUG: true` secret | Diagnose runner-level connectivity issues |
| `env | sort` step | Confirm environment variables are set correctly |
| Re-run failed jobs | Isolate transient vs. consistent failures |

## Cache Dependencies for Faster Builds

Add `actions/cache` step before dependency install → set key based on lock file hash → verify cache hit/miss in logs.

```yaml
jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: pip install -r requirements.txt

      # For Node.js projects
      - name: Cache node_modules
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-
```

```yaml
# actions/setup-python has built-in caching (preferred for Python)
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: pip                # handles cache key automatically
```

| Cache field | Description |
|---|---|
| `key` | Exact cache key; cache is restored only on exact match |
| `restore-keys` | Fallback prefixes tried in order if exact key is not found |
| `path` | Directory or file to cache |
| Cache hit | Logged as `Cache restored from key: …` in the step output |
| Cache miss | Logged as `Cache not found`; cache is saved at end of job |

## Schedule a Recurring Workflow

Add `on: schedule: - cron: '0 6 * * 1'` trigger → verify next run time in Actions → Scheduled tab.

```yaml
on:
  schedule:
    - cron: '0 6 * * 1-5'   # weekdays at 06:00 UTC
    - cron: '0 0 1 * *'     # first day of every month at 00:00 UTC

jobs:
  weekly-report:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - name: Run scheduled task
        run: python scripts/weekly_report.py
```

```bash
# Trigger a scheduled workflow manually for testing
gh workflow run scheduled-report.yml

# List upcoming scheduled runs (shows next trigger time)
gh workflow list --all

# View run history for a specific workflow
gh run list --workflow=scheduled-report.yml --limit 10
```

| Cron field order | `minute hour day-of-month month day-of-week` |
|---|---|
| `0 6 * * 1` | Every Monday at 06:00 UTC |
| `0 0 * * *` | Every day at midnight UTC |
| `*/15 * * * *` | Every 15 minutes |
| `0 9 1 * *` | First of every month at 09:00 UTC |

Note: GitHub Actions schedules run in UTC. Scheduled workflows may be delayed by up to 15 minutes under high load.

---

## Verify

- Workflow run appears in Actions tab with green checkmark (not red X)
- Workflow logs show all steps completed without errors
- Scheduled workflows trigger at the expected time (allow up to 15 min delay under load)
- Secrets referenced in the workflow are resolved — no `Context access might be invalid` warnings

---

## See also

- [GitHub Actions — Health Checks](../health-checks/)
- [GitHub Actions — CLI Reference](../cli-reference/)
- [GitHub Actions — Common Issues](../../troubleshooting/common-issues/)
