# Brocade Fabric OS

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>switchshow, portshow, zoning, fabricshow, firmware, ISLs, and diagnostics.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Bash fabric health check, Perl port error monitor, Python ISL utilization report, and Ansible config backup.</span>
</a>

</div>

## Overview

Brocade Fabric OS is the operating system for Brocade Fibre Channel SAN switches.

## Daily Checks

- Review switch health
- Check port errors
- Validate zoning configuration
- Confirm fabric membership

## Health Commands

```bash
switchshow
fabricshow
porterrshow
zoneshow
```

## Upgrade Workflow

1. Backup switch configuration
2. Verify upgrade path
3. Upgrade redundant fabric first
4. Validate fabric health
