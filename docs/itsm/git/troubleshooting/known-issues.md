---
tags:
  - troubleshooting
  - git
  - gitlab
  - github
  - itsm
  - known-issues
---
# Git / GitLab / GitHub — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Git server bugs, error codes, and workarounds covering GitLab self-managed, Gitaly, and common Git operation failures.

*Applies to: GitLab 16.x / 17.x self-managed; GitHub Enterprise*
</div>

```text
┌────────────────────────────────────── Itsm Git Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Git: Itsm Git Troubleshooting platform                            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Itsm Git Troubleshooting management console                    │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Itsm Git Troubleshooting infrastructure · management network · monitoring                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Git                = Itsm Git Troubleshooting platform overview and core concepts                  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- GitLab errors appear in `Admin → Monitoring → Logs` or `gitlab-ctl tail gitaly`.
- Most push/clone failures are Gitaly, network, or disk space issues.
- `gitlab-rake gitlab:check` runs health check for GitLab self-managed.

## Push / Clone Failures

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `fatal: repository not found` | GitLab 16.x | Repository moved or Gitaly not serving it | Check Gitaly storage: `gitlab-rake gitlab:gitaly:check` | N/A |
| `remote: error: pack-objects died with error` | GitLab 16.x | Repository disk full or Gitaly memory exhaustion | Free disk on Gitaly storage; check Gitaly pod memory | N/A |
| SSH push `Permission denied (publickey)` | All | SSH key not added to user account or wrong key | Verify key in User → SSH Keys; test: `ssh -T git@<gitlab-host>` | N/A |
| HTTPS clone prompting for password on CI | GitLab 16.x | CI job token not configured | Use `CI_JOB_TOKEN`: `git clone https://gitlab-ci-token:$CI_JOB_TOKEN@<repo>` | N/A |

## Gitaly

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Gitaly not reachable` in GitLab health | GitLab 16.x | Gitaly service crashed or TCP 8075 blocked from Workhorse | Restart: `gitlab-ctl restart gitaly`; verify TCP 8075 between GitLab and Gitaly | N/A |
| Gitaly RPC timeout on large repo operations | GitLab 16.x | Gitaly default gRPC timeout too short for large repos | Increase Gitaly timeout in `gitlab.rb`: `gitaly['rpc_timeout'] = '120s'` | N/A |

## GitLab Runner

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Runner `offline` in GitLab | GitLab 16.x | Runner process stopped or TCP 443 to GitLab blocked | Restart: `gitlab-runner restart`; verify TCP 443 from runner to GitLab | N/A |

## See also

- [Git — Common Issues](common-issues.md)
- [Jira — Known Issues](../../jira/troubleshooting/known-issues/)
- [Ansible — Known Issues](../../../automation/ansible/troubleshooting/known-issues/)
