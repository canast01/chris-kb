# Windows Server

<div class="kb-summary">
Windows Server knowledge base covering server operations, Active Directory, Group Policy, DNS, DHCP, SMB, and host management. Includes architecture references, operational procedures, CLI commands, patching, and troubleshooting guides.
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

Windows Server provides core operating system services for enterprise workloads, including Active Directory, file services, DNS, DHCP, IIS, application hosting, and infrastructure management.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review Event Viewer critical and error logs |  |  |
| Check disk capacity |  |  |
| Verify Windows services are running |  |  |
| Confirm backup status |  |  |
| Review patch compliance |  |  |

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
