# GitHub Actions Validation

## Linting Workflow Files with actionlint

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

## Schema Validation

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

## Required Status Checks

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

## Validating Workflows in CI

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

## Common Validation Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `unexpected key "enviroment"` | Typo in key name | Fix spelling — schema check catches this |
| `expression syntax error` | Malformed `${{ }}` expression | Validate expression brackets and quotes |
| `"on" is required` | Missing trigger | Add `on:` block |
| `job ID must match pattern` | Job name has spaces | Use hyphens: `my-job` not `my job` |
| `uses: action@` missing version | Unpinned action | Append version tag: `@v4` |
| Workflow never runs | `on.paths` filter mismatch | Test with `act` or temporarily broaden filter |

## Pinning Action Versions

```yaml
# Avoid using @main or @master — pin to a specific tag or SHA
steps:
  - uses: actions/checkout@v4           # semver tag (recommended)
  - uses: actions/setup-python@v5

  # For maximum security, pin to the commit SHA
  - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

```bash
# Use Dependabot to keep pinned actions up to date
# .github/dependabot.yml
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
