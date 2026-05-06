# NetBackup

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>HA topology, components, connectivity, and sizing.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>VMware, backup tools, monitoring, authentication, and API integration.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
</div>

## Overview

NetBackup provides enterprise backup and recovery for servers, databases, virtual machines, and large-scale production environments.

## Daily Checks

- Review failed jobs
- Check storage unit capacity
- Confirm catalog backup status
- Validate media server health
- Review policy schedules

## Health Commands

```bash
bpdbjobs
bppllist
bpstulist
nbemmcmd -listhosts
bperror -backstat -hoursago 24
```

## Upgrade Workflow

1. Confirm master and media server compatibility
2. Back up catalog
3. Upgrade master server first
4. Upgrade media servers and clients
5. Validate backup and restore jobs
