# Cisco MDS

<div class="kb-summary">
Cisco MDS 9000 series switches knowledge base covering fabric architecture, zoning, VSANs, ISLs, CLI references, health checks, scripts, and troubleshooting guides for Fibre Channel SAN environments.
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

Cisco MDS switches provide Fibre Channel connectivity for SAN environments.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Verify fabric health |  |  |
| Check port errors |  |  |
| Confirm zoning configuration |  |  |

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
