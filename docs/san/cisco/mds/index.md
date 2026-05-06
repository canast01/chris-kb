# Cisco MDS

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>show zone, flogi database, interfaces, VSANs, trunking, diagnostics, and config backup.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Bash fabric health check, Python FLOGI database report, zoning audit, and Ansible config backup playbook.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily checks, health check, change readiness, incident triage, maintenance window, and post-change validation.</span>
</a>

</div>

## Overview

Cisco MDS switches provide Fibre Channel connectivity for SAN environments.

## Daily Checks

- Verify fabric health
- Check port errors
- Confirm zoning configuration

## Health Commands

```bash
show version
show interface brief
show zone
show fabric status
```

## Upgrade Workflow

1. Back up configuration
2. Verify firmware compatibility
3. Upgrade secondary switch first
