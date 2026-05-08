# Linux Server

<div class="kb-summary">
Linux server knowledge base covering server operations, storage, networking, security hardening, package management, and host management. Includes architecture references, operational procedures, CLI commands, patching, and troubleshooting guides for RHEL and Ubuntu environments.
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Overview, components, integrations, and standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>

## Overview

Linux servers provide operating system services for applications, databases, automation, web platforms, monitoring tools, and infrastructure services.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Check system load |  |  |
| Review disk usage |  |  |
| Confirm key services are running |  |  |
| Review logs |  |  |
| Validate patch status |  |  |

## Health Commands

```bash
uptime
df -h
free -m
systemctl --failed
journalctl -p err -n 50
```

## Upgrade Workflow

1. Confirm package repositories
2. Verify backup or snapshot
3. Apply updates during maintenance window
4. Reboot if kernel or core packages changed
5. Validate services and logs
