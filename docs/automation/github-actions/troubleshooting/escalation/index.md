---
tags:
  - github-actions
  - troubleshooting
search:
  boost: 1.5
---
# GitHub Actions — Escalation

<div class="kb-summary">
GitHub Actions escalation: when to escalate to GitHub Enterprise Support, how to collect runner diagnostics, how to open a support case, and internal escalation path for workflow and runner failures.

*Applies to: GitHub Actions (cloud + self-hosted runners)*
</div>

```text
┌───────────────────────────────────── GitHub Actions — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Escalate GitHub Actions issues when: GitHub platform incident, persistent runner failures   │   │
│   │     Check GitHub Status (githubstatus.com) before escalating — may be a platform incident     │   │
│   │          Escalation path: dev team → platform/infra team → GitHub Enterprise support          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │                Info to Gather               │   │
│   │   GitHub platform incident (check status)    │  │             Run ID and full log             │   │
│   │     Self-hosted runner persistent crash      │  │           Runner _diag/ log folder          │   │
│   │      OIDC failing across all workflows       │  │          Cloud trust policy config          │   │
│   │       Secret value corrupted / missing       │  │           GitHub audit log export           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         githubstatus.com = GitHub incident page; check first for platform-wide issues         │   │
│   │         _diag/ folder    = runner diagnostic logs; located in runner install directory        │   │
│   │  GHE Support      = GitHub Enterprise support at support.github.com; requires Enterprise plan │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Repository admin or org owner access; for Enterprise support, account admin access to the GitHub Enterprise contract
- **Gather first:** run ID, workflow name, runner name, and exact error message from the failed job log
- **Scope:** confirm whether the issue affects a single workflow, all workflows on one runner, or all runners org-wide
- **Platform check:** always check `githubstatus.com` before escalating — GitHub incidents account for many runner and API failures
- **Logging:** enable step debug logging first (`ACTIONS_STEP_DEBUG: true` secret) to capture detailed output

---

## Severity Levels

| Severity | Definition | Escalation Path |
|---|---|---|
| Critical | CI/CD completely blocked for production deployments; secret leak suspected | Immediate: platform team + GitHub Enterprise support by phone |
| High | All self-hosted runners offline; OIDC auth broken for all workflows | Same day: platform team → open GitHub Enterprise case |
| Medium | Single runner type failing; specific workflow failing consistently | Next business day: automation team investigation |
| Low | Intermittent runner timeout; occasional step failure with clear retry | Team: investigate with step debug logging |

## Pre-Escalation Triage Checklist

Run through this before opening a GitHub Enterprise support case.

| Check | Command / Action | Expected |
|---|---|---|
| GitHub platform status | `curl https://www.githubstatus.com/api/v2/status.json \| jq '.status'` | `description: "All Systems Operational"` |
| GitHub Actions status | Check githubstatus.com → Actions component | No active incident |
| Issue affects all runners | Test with a minimal workflow on a different runner label | If only one runner, it is a runner issue |
| Minimal workflow reproduces issue | Create a 3-step test workflow and trigger manually | Confirm if issue is workflow-specific or runner-global |
| Runner registration valid | Organization Settings → Actions → Runners | Runner shows "Active" or "Idle" |
| Runner version current | Compare runner version to github.com/actions/runner/releases | Outdated runner versions cause authentication errors |
| OIDC token endpoint reachable | Check workflow has `id-token: write` permission | OIDC requires explicit permission declaration |

---

## Step-by-Step Data Collection

Collect all of the following before opening a support case.

### 1. Get the failing run details

```bash
# Install GitHub CLI if not present: https://cli.github.com/
gh auth login

# View run details and logs for a specific run ID
gh run view <run-id> --log

# Download all logs for a run (saves to ./run-<id>/)
gh run download <run-id> --dir ./run-logs-$(date +%F)

# List recent failed runs for a repository
gh run list --status failure --limit 20
```

### 2. Collect self-hosted runner diagnostics

```bash
# Runner diagnostics are in _diag/ under the runner install directory
ls -la /opt/actions-runner/_diag/

# Collect the most recent runner log files
ls -lt /opt/actions-runner/_diag/ | head -10
cp /opt/actions-runner/_diag/*.log /tmp/runner-diag-$(date +%F)/

# Get runner registration info (includes runner ID and org)
cat /opt/actions-runner/.runner

# Check runner service status (Linux)
sudo systemctl status actions.runner.*.service

# Check runner service status (macOS)
launchctl list | grep actions.runner

# Get runner application version
cat /opt/actions-runner/package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('version','unknown'))"
```

### 3. Collect OIDC configuration (for OIDC/cloud auth issues)

```bash
# Check OIDC subject customization for the repo
gh api /repos/{owner}/{repo}/actions/oidc/customization/sub

# Check org-level OIDC policy
gh api /orgs/{org}/actions/oidc/customization/issuer

# Verify the workflow has correct permissions
grep -A5 'permissions:' .github/workflows/failing-workflow.yml
```

### 4. Export audit log (Enterprise only)

```bash
# Export last 100 audit log entries (requires org admin or enterprise admin)
gh api "/orgs/{org}/audit-log?phrase=action:workflows&per_page=100" \
  --paginate | python3 -c "import sys,json; [print(json.dumps(e)) for e in json.load(sys.stdin)]" \
  > audit-log-$(date +%F).jsonl
```

### 5. Write the timeline

Create a plain text file:

```text
GitHub org / repo: myorg/myrepo
Runner label: self-hosted, linux, x64
Runner hostname: runner-001.example.com
Runner version: 2.314.1

Issue first observed: 2026-06-15 10:30 UTC
Last known good run: 2026-06-15 09:00 UTC
Workflow: deploy-production.yml (Job: build)
Run ID: 9876543210

Error message:
  Error: Process completed with exit code 1
  ##[error]Runner received signal: SIGTERM

Changes in 24h before issue:
  - Runner host OS updated (Ubuntu 22.04 kernel update applied)
  - No workflow changes

Blast radius:
  - All jobs on self-hosted runners are failing
  - GitHub-hosted runner jobs are not affected
```

---

## How to Open a GitHub Enterprise Support Case

1. Go to **support.github.com** and sign in with your Enterprise account.
   - If you cannot access the portal: contact your GitHub account manager to verify your Enterprise entitlement.

2. Click **Open a new ticket**.

3. Under **Product area**, select **Actions** for runner or workflow issues.

4. Under **Priority**, select:
   - **Urgent**: CI/CD completely blocked for production; security incident involving secrets
   - **High**: All runners offline; OIDC broken for the organisation
   - **Normal**: Single workflow or runner type failing
   - **Low**: Questions, feature requests, documentation issues

5. In the **Subject** field, write one sentence: `GitHub Actions self-hosted runner [runner-name] exiting with SIGTERM since [date/time] — all jobs failing`.

6. In the **Description**, paste:
   - GitHub org name and runner hostname
   - Failing run IDs (at least 3 examples)
   - Runner version and OS
   - Timeline (from step 5 above)
   - The `_diag/` log contents

7. Under **Attachments**, upload:
   - Runner diagnostic logs from `_diag/`
   - Workflow YAML file (`failing-workflow.yml`)
   - Run log download from `gh run download`
   - Audit log export (if OIDC or secret issue)

8. Click **Submit**. You will receive a ticket number by email.

---

## Escalation Path

```text
Step 1 — Internal: automation team investigates with step debug logging
         (ACTIONS_STEP_DEBUG: true and ACTIONS_RUNNER_DEBUG: true secrets)
         ↓
Step 2 — If issue is not workflow-specific (affects all runners or all workflows):
         → Platform / infra team: check runner host networking, DNS, TLS, proxy config
         ↓
Step 3 — If platform team cannot resolve: open GitHub Enterprise support case at support.github.com
         → Attach runner diagnostics and failing run logs
         ↓
Step 4 — If GitHub confirms a platform incident affecting your organisation:
         → Follow githubstatus.com for resolution timeline
         → No further escalation needed — GitHub's SRE team is engaged
         ↓
Step 5 — If case is not progressing within SLA:
         → Reply in the support case: "Requesting escalation — impact: [describe production impact]"
         → Contact your GitHub account manager to expedite
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Delete and re-register the runner while jobs are queued | Queued jobs stay assigned to the old runner and will never run | Drain the runner first: disable it in org settings, wait for queue to clear |
| Rotate organisation secrets during an active incident | All in-flight workflows will fail immediately with auth errors | Only rotate after confirming the exact secret affected; communicate the outage window |
| Force-cancel all running jobs without notifying teams | May corrupt state in downstream systems (deployments, database migrations) | Identify which jobs are safe to cancel; cancel only after team review |
| Enable `ACTIONS_STEP_DEBUG` on production workflows permanently | Leaks environment variables and sensitive inputs to logs | Enable only for isolated debug runs; remove the secret immediately after |
| Downgrade the runner binary manually | Unsigned binaries may not authenticate; runner auto-updates will re-upgrade | Pin runner versions at org level through GitHub settings, not manual binary replacement |

---

## Useful Commands for Case Updates

```bash
# Confirm current GitHub platform status (include in every case update)
curl -s https://www.githubstatus.com/api/v2/components.json | \
  python3 -c "import sys,json; [print(f'{c[\"name\"]}: {c[\"status\"]}') for c in json.load(sys.stdin)['components']]"

# Get all failed runs in the last 24 hours across a repository
gh run list --status failure --created ">=2026-06-14" --json databaseId,displayTitle,conclusion,createdAt | \
  python3 -m json.tool

# Check if runner is receiving dispatched jobs
gh api /orgs/{org}/actions/runners --jq '.runners[] | {id, name, status, busy}'

# View specific step failure in a run
gh run view <run-id> --job <job-id> --log | grep -A10 "Error\|##\[error\]"

# Check workflow permissions
gh api /repos/{owner}/{repo}/actions/permissions/workflow

# List org-level secrets (names only, not values)
gh secret list --org {org}
```

---

## See also

- [GitHub Actions — Diagnostics](../diagnostics/)
- [GitHub Actions — Common Issues](../common-issues/)

---

## Verify resolution

- Confirm a re-triggered run on the affected runner completes successfully
- Check `_diag/` logs on the runner — no `Error` or `SIGTERM` entries during the new run
- Verify the specific job that was failing (build, deploy, test) passes end-to-end
- Monitor for 2–3 runs to confirm the fix is stable before removing any workarounds
