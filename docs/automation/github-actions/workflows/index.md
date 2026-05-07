# GitHub Actions Workflows

## Workflow Syntax Overview

Workflows live in `.github/workflows/` and are YAML files with a defined structure.

```yaml
# .github/workflows/ci.yml
name: CI Pipeline          # displayed in the Actions UI

on:                        # event triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:                       # workflow-level environment variables
  NODE_ENV: test

jobs:
  test:                    # job ID (no spaces)
    name: Run Tests        # display name
    runs-on: ubuntu-24.04
    env:
      LOG_LEVEL: debug     # job-level env vars

    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
        env:
          CI: true         # step-level env vars
```

## Reusable Workflows

Reusable workflows reduce duplication by calling one workflow from another.

```yaml
# .github/workflows/reusable-deploy.yml (called workflow)
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-24.04
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh ${{ inputs.environment }}
        env:
          DEPLOY_KEY: ${{ secrets.deploy_key }}
```

```yaml
# .github/workflows/main.yml (calling workflow)
jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
    secrets:
      deploy_key: ${{ secrets.STAGING_DEPLOY_KEY }}
```

## Concurrency Control

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

## workflow_dispatch and Manual Triggers

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

## Workflow Feature Reference

| Feature | Syntax | Purpose |
|---|---|---|
| Job dependency | `needs: [build, test]` | Run after listed jobs succeed |
| Conditional | `if: github.ref == 'refs/heads/main'` | Skip job/step conditionally |
| Timeout | `timeout-minutes: 15` | Kill if job runs too long |
| Continue on error | `continue-on-error: true` | Mark step failure as warning |
| Strategy | `strategy.matrix` | Fan out across value combinations |
| Outputs | `outputs.key: ${{ steps.id.outputs.key }}` | Pass data between jobs |
| Composite action | `using: composite` | Bundle steps into a reusable action |

## Composite Actions

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
