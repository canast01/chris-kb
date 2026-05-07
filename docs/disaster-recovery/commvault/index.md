# Commvault


<div class="kb-grid kb-grid-1">

  <div class="kb-card">
    <h3><a href="cli-reference/">CLI Reference</a></h3>
    <p>qcommand toolkit, qlist, qoperation, qmedia, CommVault REST API, and job management.</p>
  </div>

</div>

## Overview

Commvault provides enterprise backup, recovery, replication, archive, and data protection management.

## Daily Checks

- Review failed jobs
- Check storage policy capacity
- Confirm client connectivity
- Validate deduplication database health
- Review restore readiness

## Health Commands

```bash
qoperation execute -af jobsummary.xml
qlist client
qlist storagepolicy
qoperation execscript -sn QS_CheckReadiness
```

## Upgrade Workflow

1. Confirm CommServe backup
2. Verify client and media agent compatibility
3. Upgrade CommServe
4. Upgrade media agents
5. Validate backup and restore operations
