# Commvault


<div class="kb-grid kb-grid-2">

  <div class="kb-card">
    <h3><a href="cli-reference/">CLI Reference</a></h3>
    <p>qcommand toolkit, qlist, qoperation, qmedia, CommVault REST API, and job management.</p>
  
  <div class="kb-card">
    <h3><a href="architecture/">Architecture</a></h3>
    <p>Architecture overview, components, and design patterns.</p>
  </div>

  <div class="kb-card">
    <h3><a href="integration/">Integration</a></h3>
    <p>Integration with other systems and platforms.</p>
  </div>

  <div class="kb-card">
    <h3><a href="lifecycle/">Lifecycle</a></h3>
    <p>Installation, upgrades, patching, and decommission.</p>
  </div>

  <div class="kb-card">
    <h3><a href="scripts/">Scripts</a></h3>
    <p>Automation scripts for common tasks and reporting.</p>
  </div>

  <div class="kb-card">
    <h3><a href="security/">Security</a></h3>
    <p>Security configuration, hardening, and access control.</p>
  </div>

  <div class="kb-card">
    <h3><a href="standards/">Standards</a></h3>
    <p>Configuration standards, naming conventions, and baselines.</p>
  </div>

  <div class="kb-card">
    <h3><a href="troubleshooting/">Troubleshooting</a></h3>
    <p>Common issues, diagnostic steps, and resolution guides.</p>
  </div>

  <div class="kb-card">
    <h3><a href="vendor-support/">Vendor Support</a></h3>
    <p>Support bundles, case management, and escalation paths.</p>
  </div>
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
