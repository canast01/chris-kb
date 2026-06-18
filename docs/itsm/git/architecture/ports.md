---
tags:
  - git
  - itsm
  - version-control
  - networking
  - firewall
  - ports
---
# Git (Self-Hosted) — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for self-hosted Git platforms (GitLab, Bitbucket Data Center). Covers web/API, SSH Git operations, CI/CD runner connections, and webhook delivery.

*Applies to: GitLab CE/EE 16.x / Bitbucket Data Center 8.x*
</div>

```text
┌──────────────────────────────────────── Itsm Git Architecture ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Git: Itsm Git Architecture platform                              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: Itsm Git Architecture management console                     │   │
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
│    Physical: Itsm Git Architecture infrastructure · management network · monitoring                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Git                = Itsm Git Architecture platform overview and core concepts                     │
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


## Inbound — Client Access

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Developers, CI/CD pipelines, API clients | HTTPS — web UI, REST API, HTTPS Git clone/push/pull |
| 80 | TCP | Clients | HTTP — redirects to 443 |
| 22 | TCP | Developers, CI/CD runners | SSH — Git clone/push/pull via SSH protocol |

## CI/CD Runner to GitLab/Bitbucket

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | GitLab Runner / Bamboo | GitLab / Bitbucket server | Job polling, artifact upload |
| 443 | TCP | GitLab / Bitbucket | Deployment targets (via webhook) | Webhook delivery to external services |

## Database

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 5432 | TCP | PostgreSQL | GitLab primary database |
| 6379 | TCP | Redis | GitLab Sidekiq job queue, caching |

## GitLab Cluster (Gitaly, Praefect)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 8075 | TCP | GitLab app → Gitaly | Gitaly gRPC — Git repository operations |
| 2305 | TCP | Praefect nodes ↔ Praefect nodes | Praefect cluster (HA Gitaly) |

## Outbound — Server to External

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 25 | TCP | SMTP relay | Email notifications (MR, pipeline, issue alerts) |
| 443 | TCP | External webhook receivers, Slack, Jira | Outbound webhooks and integrations |
| 443 | TCP | Container registry (gcr.io, DockerHub) | Pipeline image pulls (if no local registry) |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Developers | Git server | 443, 22 | HTTPS and SSH Git |
| CI/CD runners | Git server | 443 | Job coordination |
| Git server | PostgreSQL | 5432 | Database |
| Git server | Redis | 6379 | Queue and cache |
| Git app | Gitaly | 8075 | Git operations |
| Git server | SMTP | 25 | Email notifications |

## Verify

```bash
# From developer workstation — test HTTPS clone
git clone https://<gitlab-host>/test/repo.git /tmp/test-clone

# From developer workstation — test SSH
ssh -T git@<gitlab-host>

# From CI runner — test API connectivity
curl -sk -o /dev/null -w "%{http_code}" https://<gitlab-host>/api/v4/projects

# From GitLab app server — test Gitaly
nc -zv <gitaly-host> 8075
```

## See also

- [Git — Architecture](how-it-works/)
- [Git — Operations](../operations/)
- [Jira — Ports](../../jira/architecture/ports.md)
- [GitHub Actions — Ports](../../../automation/github-actions/architecture/ports.md)
