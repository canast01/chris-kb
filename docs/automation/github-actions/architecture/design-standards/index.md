# GitHub Actions — Standards


<div class="kb-summary">
> Part of the [GitHub Actions Architecture](../index.md) reference.
</div>

## Workflow File Structure

```text
.github/
└── workflows/
    ├── ci.yml          # lint, test, build on every push/PR
    ├── deploy.yml      # deploy to staging/prod on merge to main
    ├── security.yml    # weekly security scans
    └── cleanup.yml     # scheduled resource cleanup
```
┌────────────────────────────────── GitHub Actions — Design Standards ──────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Standards for consistent, secure, maintainable GitHub Actions workflows across repos     │   │
│   │     Security: pin all third-party actions by SHA; avoid GITHUB_TOKEN write-all permission     │   │
│   │    Structure: one workflow per concern; reusable workflows for shared logic; no copy-paste    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Workflow Structure Rules           │  │                Security Rules               │   │
│   │         Name workflows descriptively         │  │           Pin: uses: action@<sha>           │   │
│   │           One workflow per concern           │  │          Minimal GITHUB_TOKEN perms         │   │
│   │       Reusable workflow for shared CI        │  │           OIDC over static secrets          │   │
│   │        Cache keyed on lock file hash         │  │       No secrets in env: at top level       │   │
│   │       Concurrency: cancel-in-progress        │  │       Required reviewers for prod env       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Reusable workflow = workflow called via uses: org/repo/.github/workflows/shared.yml@main   │   │
│   │ SHA pinning       = uses: actions/checkout@<40-char SHA> instead of @v4; prevents tag mutation│   │
│   │ OIDC              = workflow requests short-lived AWS/Azure token; no stored cloud credentials│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

!!! warning "Do not use `permissions: write-all`"
    `write-all` grants excessive access. Set permissions explicitly per job, and only grant what each job needs.

## Reusable Workflows

```yaml
# .github/workflows/reusable-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
    secrets:
      deploy-key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-24.04
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy
        run: ./deploy.sh ${{ inputs.image-tag }}
        env:
          DEPLOY_KEY: ${{ secrets.deploy-key }}
```

```yaml
# Caller workflow
jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      image-tag: ${{ needs.build.outputs.image-tag }}
    secrets:
      deploy-key: ${{ secrets.STAGING_DEPLOY_KEY }}
```

## Composite Actions

```yaml
# .github/actions/setup-python-env/action.yml
name: Setup Python Environment
description: Install Python and project dependencies with caching

inputs:
  python-version:
    required: false
    default: "3.12"

runs:
  using: composite
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}
        cache: pip

    - name: Install dependencies
      shell: bash
      run: pip install -r requirements.txt
```

## Runner Standards

```yaml
# Standard runners by use case
runs-on: ubuntu-24.04      # Linux — prefer specific version over ubuntu-latest
runs-on: windows-2022      # Windows
runs-on: macos-14          # macOS (ARM)

# Self-hosted for resources, VPN access, or large assets
runs-on: [self-hosted, linux, prod]
```

!!! tip "Pin to specific runner versions"
    `ubuntu-latest` changes without notice. Pin to `ubuntu-24.04` in production workflows to avoid unexpected breaks.

## Action Version Pinning

```yaml
# Pin to SHA — most secure (immutable)
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# Pin to major version tag — balance of safety and updates
- uses: actions/checkout@v4         # acceptable for trusted actions

# Never use @main or @master — unpredictable
```

## Caching

```yaml
# Dependency caching
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cache/pip
      ~/.m2/repository
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-deps-

# Docker layer caching
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Job Dependencies and Concurrency

```yaml
jobs:
  build:
    runs-on: ubuntu-24.04
    steps: [...]

  test:
    needs: build
    runs-on: ubuntu-24.04
    steps: [...]

  deploy:
    needs: [build, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04
    steps: [...]

# Prevent concurrent deployments to same environment
concurrency:
  group: deploy-${{ github.ref }}-${{ inputs.environment }}
  cancel-in-progress: false   # queue, don't cancel in-flight deploys
```

## Matrix Strategy

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-24.04, windows-2022]
        python: ["3.11", "3.12"]
        exclude:
          - os: windows-2022
            python: "3.11"
      fail-fast: false     # don't cancel other matrix jobs on failure
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
```

## Artifact Management

```yaml
# Upload build artifacts
- uses: actions/upload-artifact@v4
  with:
    name: build-output-${{ github.sha }}
    path: dist/
    retention-days: 7      # don't keep forever

# Download in subsequent job
- uses: actions/download-artifact@v4
  with:
    name: build-output-${{ github.sha }}
    path: dist/
```

## Notification Standards

```yaml
# Always notify on failure in production deploys
- name: Notify Slack on failure
  if: failure() && github.ref == 'refs/heads/main'
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: "C0123ALERTS"
    slack-message: "Deploy failed: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

## Workflow Checklist

| Standard | Check |
|---|---|
| Explicit permissions set | `permissions:` block present |
| Actions pinned to version | No `@main` or floating tags |
| Secrets not echoed | No `echo ${{ secrets.X }}` |
| `concurrency` on deploy workflows | Prevents race conditions |
| `fail-fast: false` on matrix | Don't hide failures |
| Environment gate on prod deploys | `environment: production` |
| Notifications on failure | Slack / email on `if: failure()` |
| `workflow_dispatch` on all workflows | Manual trigger available |
| Artifact retention set | `retention-days` specified |
