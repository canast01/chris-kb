# GitHub Actions — Diagnostics

> Part of the [GitHub Actions Troubleshooting](../index.md) reference.

---

## Debug Logging

```mermaid
flowchart TD
    symptom(["Workflow failure\nor unexpected behaviour"])
    uiCheck["GitHub Actions UI\nCheck step logs for error"]
    runLogs["gh run view RUN_ID --log\nFull log download"]
    debugSecrets["Set repo secrets\nACTIONS_RUNNER_DEBUG=true\nACTIONS_STEP_DEBUG=true"]
    rerunDebug["Re-run jobs with\ndebug logging enabled"]
    actLocal["act push --job build\nRun locally in Docker"]
    dumpCtx["Add step: dump github context\ntoJson(github)"]
    identify(["Identify root cause\nFix and re-push"])

    symptom --> uiCheck
    uiCheck -->|"Insufficient detail"| debugSecrets
    debugSecrets --> rerunDebug --> identify
    uiCheck -->|"Need local iteration"| actLocal --> identify
    uiCheck -->|"Context issue"| dumpCtx --> identify
    uiCheck -->|"Logs clear"| runLogs --> identify
```
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
