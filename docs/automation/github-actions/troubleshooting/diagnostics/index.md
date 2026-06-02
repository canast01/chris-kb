# GitHub Actions — Diagnostics


<div class="kb-summary">
> Part of the [GitHub Actions Troubleshooting](../index.md) reference.
</div>

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
┌──────────────────────────────────── GitHub Actions — Diagnostics ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │GitHub Actions diagnostic sequence: enable debug → inspect logs → check runner → verify secrets│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Debug Logging                 │  │                  Log Access                 │   │
│   │         Set ACTIONS_STEP_DEBUG=true          │  │            gh run view --log <id>           │   │
│   │        Set ACTIONS_RUNNER_DEBUG=true         │  │        gh run view --log-failed <id>        │   │
│   │        Re-run with debug enabled (UI)        │  │           Download log ZIP from UI          │   │
│   │        Add: run: env (print env vars)        │  │        API: /repos/.../runs/{id}/logs       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Debug secrets   = ACTIONS_STEP_DEBUG and ACTIONS_RUNNER_DEBUG are set as repo/env secrets   │   │
│   │     Log retention   = 90 days default; configurable per repo; ZIP downloadable for archive    │   │
│   │       run: env      = add as a step to print all env vars; helps trace secret injection       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌──────────────────────────────────── GitHub Actions — Diagnostics ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │GitHub Actions diagnostic sequence: enable debug → inspect logs → check runner → verify secrets│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Debug Logging                 │  │                  Log Access                 │   │
│   │         Set ACTIONS_STEP_DEBUG=true          │  │            gh run view --log <id>           │   │
│   │        Set ACTIONS_RUNNER_DEBUG=true         │  │        gh run view --log-failed <id>        │   │
│   │        Re-run with debug enabled (UI)        │  │           Download log ZIP from UI          │   │
│   │        Add: run: env (print env vars)        │  │        API: /repos/.../runs/{id}/logs       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Debug secrets   = ACTIONS_STEP_DEBUG and ACTIONS_RUNNER_DEBUG are set as repo/env secrets   │   │
│   │     Log retention   = 90 days default; configurable per repo; ZIP downloadable for archive    │   │
│   │       run: env      = add as a step to print all env vars; helps trace secret injection       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
