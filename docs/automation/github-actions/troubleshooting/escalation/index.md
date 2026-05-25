# GitHub Actions — Escalation

> Part of the [GitHub Actions Troubleshooting](../index.md) reference.

---

## GitHub Status and Known Issues

Before escalating, check whether the issue is a platform-wide incident.

```bash
# Check GitHub's status page
open https://githubstatus.com

# Subscribe to status notifications via the GitHub Status API
curl https://www.githubstatus.com/api/v2/status.json | jq '.status'
```
┌───────────────────────────────────── GitHub Actions — Escalation ─────────────────────────────────────┐
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

## Escalation Checklist

- [ ] Confirmed issue is not on the [GitHub Status page](https://githubstatus.com)
- [ ] Captured the full run ID and workflow file name
- [ ] Downloaded run logs: `gh run download RUN_ID --dir ./run-logs`
- [ ] Identified the exact step, error message, and exit code
- [ ] Reproduced the issue or confirmed it is consistent
- [ ] Checked GitHub Community discussions for similar reports
- [ ] Raised a support ticket with run ID, repo name, and log excerpt

```mermaid
flowchart TD
    issue(["Workflow issue\ncannot self-resolve"])
    statusPage["Check githubstatus.com\nPlatform incident?"]
    incident{Platform\nincident?}
    waitResolve["Wait for GitHub\nto resolve"]
    collectData["Collect data\ngh run view RUN_ID --log\ngh run list --workflow ci.yml"]
    community["Search GitHub Community\nDiscussions for similar reports"]
    found{Solution\nfound?}
    openTicket["Open GitHub Support ticket\nRun ID + repo name + log excerpt\nEnterprise plan: SLA-backed"]
    done(["Issue resolved"])

    issue --> statusPage --> incident
    incident -->|Yes| waitResolve --> done
    incident -->|No| collectData --> community --> found
    found -->|Yes| done
    found -->|No| openTicket --> done
```
