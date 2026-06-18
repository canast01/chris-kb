---
tags:
  - github-actions
  - automation
  - networking
  - firewall
  - ports
  - cicd
---
# GitHub Actions — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for GitHub Actions with self-hosted runners. GitHub-hosted runners run in GitHub's cloud — no on-premise firewall rules needed for those. Self-hosted runners require outbound 443 to github.com and any deployment target ports.

*Applies to: GitHub Actions with self-hosted runners*
</div>

```text
┌─────────────────────────────── Automation Github Actions Architecture ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Github Actions: Automation Github Actions Architecture platform                │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │             Management: Automation Github Actions Architecture management console             │   │
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
│    Physical: Automation Github Actions Architecture infrastructure · management network · monitoring  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Github Actions     = Automation Github Actions Architecture platform overview and core concepts    │
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


## Self-Hosted Runner — Outbound to GitHub

Self-hosted runners connect **outbound** to GitHub — no inbound from GitHub to the runner is required.

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | github.com, api.github.com | Job polling, artifact upload/download, webhook processing |
| 443 | TCP | *.actions.githubusercontent.com | Action runner runtime and caches |
| 443 | TCP | ghcr.io, *.pkg.github.com | GitHub Container Registry (image pull for container jobs) |

## Self-Hosted Runner — Deployment Targets (Job-Specific)

Runners connect to deployment targets during jobs. Open from the runner's IP to each target type:

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 22 | TCP | Linux deployment targets | SSH deployments, Ansible from runner |
| 443 | TCP | vCenter, AWS, Azure, GCP APIs | IaC and cloud deployment |
| 5986 | TCP | Windows deployment targets | WinRM HTTPS — Windows deployment |
| 443 | TCP | Self-hosted GitLab / package registries | Cross-platform integration |
| 443 | TCP | Docker Hub, GHCR, private registry | Container image pull/push |

## Inbound — Webhook Receiver (if repo is self-hosted GitHub Enterprise)

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | GitHub.com or GitHub Enterprise | Webhook delivery to GitHub Enterprise server |
| 22 | TCP | GitHub Enterprise admin | GitHub Enterprise SSH access |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Self-hosted runner | github.com | 443 | Job polling — must be open |
| Self-hosted runner | Deployment targets | 22, 443, 5986 | Job-specific — open per deployment type |
| GitHub (cloud) | GitHub Enterprise | 443 | Webhook delivery (if GHE) |

## Verify

```bash
# From self-hosted runner host — test GitHub connectivity
curl -sk -o /dev/null -w "%{http_code}" https://api.github.com/

# Test runner registration
./config.sh --url https://github.com/<org>/<repo> --token <token> --check

# From runner — test deployment target
nc -zv <linux-deploy-target> 22
```

## See also

- [GitHub Actions — Architecture](how-it-works/)
- [Ansible — Ports](../../ansible/architecture/ports.md)
- [Terraform — Ports](../../terraform/architecture/ports.md)
- [Git — Ports](../../../itsm/git/architecture/ports.md)
