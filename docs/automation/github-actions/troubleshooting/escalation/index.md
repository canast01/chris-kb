# GitHub Actions — Escalation

```bash
# Check GitHub's status page
open https://githubstatus.com

# Subscribe to status notifications via the GitHub Status API
curl https://www.githubstatus.com/api/v2/status.json | jq '.status'
```
```text
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
