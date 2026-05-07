# NTP


<div class="kb-grid kb-grid-1">

  <div class="kb-card">
    <h3><a href="firewalls/">Firewalls</a></h3>
    <p>Firewalls notes, checks, commands, and references.</p>
  </div>

  <div class="kb-card">
    <h3><a href="sync-state/">Sync State</a></h3>
    <p>Sync State notes, checks, commands, and references.</p>
  </div>

  <div class="kb-card">
    <h3><a href="validation/">Validation</a></h3>
    <p>Validation notes, checks, commands, and references.</p>
  </div>

</div>
## Overview

NTP keeps infrastructure time synchronized. Time drift can break authentication, certificates, logging, replication, clustering, and audit trails.

## Daily Checks

- Confirm time source is reachable
- Check drift offset
- Validate domain time hierarchy
- Review time sync errors

## Health Commands

```bash
ntpq -p
chronyc sources
timedatectl status
w32tm /query /status
```

## Upgrade Workflow

1. Confirm authoritative time sources
2. Update NTP or chrony configuration
3. Restart time service
4. Validate offset and synchronization
5. Monitor logs for drift warnings
