# Venafi

<div class="kb-grid kb-grid-14">
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

<a class="kb-card" href="automation/">
  <strong>Automation</strong>
  <span>Automation notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="inventory/">
  <strong>Inventory</strong>
  <span>Inventory notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="policy/">
  <strong>Policy</strong>
  <span>Policy notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="reporting/">
  <strong>Reporting</strong>
  <span>Reporting notes, checks, commands, and references.</span>
</a>
</div>
## Overview

Venafi manages machine identities and automates certificate lifecycle management across infrastructure and applications.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review certificate expiration alerts |  |  |
| Check trust store synchronization |  |  |
| Validate automated certificate renewals |  |  |
| Monitor integration status |  |  |

## Health Commands

```bash
vcert list
vcert status
vcert renew
```

## Upgrade Workflow

1. Backup configuration and databases
2. Confirm system requirements
3. Apply software upgrade
4. Validate certificate provisioning
