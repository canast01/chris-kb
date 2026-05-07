# GitHub Actions Builds

## Workflow Triggers

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

## Jobs and Steps

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

## Artifacts

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

## Matrix Builds

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

## Key Build Concepts

| Concept | Description |
|---|---|
| `needs` | Job dependency — wait for listed jobs to succeed |
| `if` | Conditional job/step execution |
| `timeout-minutes` | Kill job if it exceeds this duration |
| `continue-on-error` | Mark step failure as non-fatal |
| `env` | Environment variables for the job or step |
| `outputs` | Pass values from one job to another |

## Passing Outputs Between Jobs

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
