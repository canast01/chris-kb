# GitHub Actions Troubleshooting

## Debug Logging

Enable additional diagnostic output without modifying workflow files.

```bash
# Set these repository secrets to enable debug logs for the next run
ACTIONS_RUNNER_DEBUG = true
ACTIONS_STEP_DEBUG   = true

# Or pass via workflow_dispatch input / re-run with debug enabled
# In the GitHub UI: Actions → select run → Re-run jobs → Enable debug logging
```

```yaml
# Add a debug step to print all context objects
- name: Dump GitHub context
  env:
    GITHUB_CONTEXT: ${{ toJson(github) }}
  run: echo "$GITHUB_CONTEXT"

- name: Dump runner context
  env:
    RUNNER_CONTEXT: ${{ toJson(runner) }}
  run: echo "$RUNNER_CONTEXT"
```

## Running Workflows Locally with act

`act` runs GitHub Actions locally using Docker, shortening the feedback loop.

```bash
# Install act (macOS)
brew install act

# List available jobs
act --list

# Run the default push event
act push

# Run a specific job
act push --job build

# Run with a specific secret
act push -s MY_SECRET=value

# Use a smaller runner image
act push -P ubuntu-24.04=catthehacker/ubuntu:act-24.04

# Dry-run (no execution)
act --dryrun push
```

## Common Failures

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

## Inspecting Workflow Runs

```bash
# List recent workflow runs
gh run list --repo owner/repo --limit 20

# View a specific run
gh run view 12345678

# Watch a run in real time
gh run watch 12345678

# Download logs from a failed run
gh run download 12345678 --dir ./run-logs

# Re-run only failed jobs
gh run rerun 12345678 --failed

# Cancel a running workflow
gh run cancel 12345678
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
