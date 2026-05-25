# GitHub Actions — Common Issues

> Part of the [GitHub Actions Troubleshooting](../index.md) reference.

---

## Common Failures

```mermaid
flowchart TD
    failure(["Workflow failure\nor unexpected behaviour"])
    noTrigger{"Did the workflow\ntrigger at all?"}
    checkPaths["Check on.paths filter\nDoes it match the changed files?"]
    stepFail{"Which step\nfailed?"}
    permErr["Resource not accessible\n→ Add permissions: block to job"]
    ctxErr["Context access invalid\n→ Fix ${{ }} expression syntax"]
    exitErr["Exit code 1\n→ Check step output in logs"]
    secretErr["Secret is empty\n→ Check repo vs env vs org scope"]
    wdErr["No such file\n→ Add working-directory: or cd"]

    failure --> noTrigger
    noTrigger -->|No| checkPaths
    noTrigger -->|Yes| stepFail
    stepFail --> permErr
    stepFail --> ctxErr
    stepFail --> exitErr
    stepFail --> secretErr
    stepFail --> wdErr
```

| Error | Cause | Fix |
|---|---|---|
| `Context access might be invalid` | Wrong expression syntax | Check `${{ }}` vs `$( )` usage |
| `Resource not accessible by integration` | `GITHUB_TOKEN` lacks permission | Add `permissions:` block to job |
| `No such file or directory` | Working directory wrong | Add `working-directory:` or `cd` in run |
| `Process completed with exit code 1` | Command failed | Check step output; add `set -e` or `|| true` |
| Workflow not triggering | `on:` path filter too restrictive | Verify paths match changed files |
| Secret shows as `***` but is empty | Secret not set in correct scope | Check env vs repo vs org secret scopes |

## Permissions Issues

```yaml
# Minimal permissions — grant only what's needed
permissions:
  contents: read
  packages: write
  id-token: write

# Per-job override
jobs:
  release:
    permissions:
      contents: write
      discussions: write
```

```bash
# Check if GITHUB_TOKEN can push to a protected branch
# Protected branch rules must explicitly allow Actions
# Settings → Branches → Branch protection → Allow GitHub Actions to bypass
```

## Caching and Stale State

```yaml
# Clear a cache by key via CLI
gh cache delete --repo owner/repo "pip-cache-key-abc123"

# List all caches
gh cache list --repo owner/repo

# Force cache miss by varying the key
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('**/requirements.txt') }}-${{ github.run_id }}
```
