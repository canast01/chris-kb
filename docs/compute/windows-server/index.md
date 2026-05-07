# Windows Server

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

<a class="kb-card" href="event-logs/">
  <strong>Event Logs</strong>
  <span>Event Logs notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Health check procedures and validation steps.</span>
</a>

<a class="kb-card" href="patching/">
  <strong>Patching</strong>
  <span>Patching notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="performance/">
  <strong>Performance</strong>
  <span>Performance monitoring, tuning, and baselining.</span>
</a>
</div>

## Overview

Windows Server provides core operating system services for enterprise workloads, including Active Directory, file services, DNS, DHCP, IIS, application hosting, and infrastructure management.

## Daily Checks

- Review Event Viewer critical and error logs
- Check disk capacity
- Verify Windows services are running
- Confirm backup status
- Review patch compliance

## Health Commands

```powershell
Get-Service | Where-Object Status -ne Running
Get-EventLog -LogName System -EntryType Error -Newest 20
Get-PSDrive -PSProvider FileSystem
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

## Upgrade Workflow

1. Confirm application compatibility
2. Verify backup and rollback plan
3. Apply patches or upgrade during maintenance window
4. Reboot and validate services
5. Confirm monitoring and backups are healthy
