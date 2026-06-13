---
tags:
  - security
---
# Patch Compliance Monitoring

<div class="kb-summary">
Patch Compliance Monitoring reference covering Patch Classification, Windows Patch Compliance, Linux Patch Compliance, SCCM / Endpoint Manager (Windows fleet), Patch Reporting and 2 more sections.
</div>
```text
┌────────────────────────────────────── Security Patch Compliance ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Patch Compliance: Security Patch Compliance platform                     │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Security Patch Compliance management console                   │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Patch Compliance infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Patch Compliance   = Security Patch Compliance platform overview and core concepts                 │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Patch scanning, SLA tracking, WSUS/SCCM management, exception handling</div>
  </a>
</div>

## Patch Classification

| Severity | Definition | Deployment SLA |
|---|---|---|
| Critical | Remote code execution, active exploitation | 15 days |
| Important | Privilege escalation, data exposure | 30 days |
| Moderate | Requires unusual conditions or local access | 90 days |
| Low | Minimal impact | Next scheduled window |

## Windows Patch Compliance

```powershell
# List installed hotfixes sorted by date
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 20

# List missing updates (requires Windows Update module)
$session = New-Object -ComObject Microsoft.Update.Session
$searcher = $session.CreateUpdateSearcher()
$missing = $searcher.Search("IsInstalled=0 and Type='Software'")
$missing.Updates | Select-Object Title, MsrcSeverity | Sort-Object MsrcSeverity

# WSUS — get patch compliance per computer
# Run on WSUS server (requires UpdateServices module)
$wsus = Get-WsusServer -Name wsus01 -PortNumber 8530
$computers = Get-WsusComputer -UpdateServer $wsus -All
$computers | Select-Object FullDomainName, LastSyncTime, @{N='NotInstalled';E={$_.GetUpdateInstallationSummary().NotInstalled}} |
  Sort-Object NotInstalled -Descending | Select-Object -First 20
```

## Linux Patch Compliance

```bash
# RHEL/CentOS — list available security updates
yum updateinfo list security available 2>/dev/null

# Count critical updates
yum updateinfo summary security 2>/dev/null | grep "Critical"

# Ubuntu/Debian — list upgradable security packages
apt list --upgradable 2>/dev/null | grep -i security

# Confirm last update date
rpm -qa --last | head -10          # RHEL
grep "install" /var/log/dpkg.log | tail -10  # Debian

# Check kernel version vs latest available
uname -r
rpm -q kernel | sort -V | tail    # RHEL — latest installed kernel
```

## SCCM / Endpoint Manager (Windows fleet)

```powershell
# Query SCCM database for patch compliance (run on SCCM server)
$query = "SELECT SMS_R_System.Name, SMS_UpdateComplianceStatus.Status FROM SMS_R_System
          INNER JOIN SMS_UpdateComplianceStatus ON SMS_R_System.ResourceID = SMS_UpdateComplianceStatus.MachineID
          WHERE SMS_UpdateComplianceStatus.ArticleID = '<KB-number>'"
```

## Patch Reporting

| Metric | Target |
|---|---|
| Critical patches applied within 15 days | >95% of hosts |
| High patches applied within 30 days | >90% of hosts |
| Systems with no patches >90 days | 0 |
| Unapproved exceptions | Must have documented business justification + compensating control |

## Compliance Checks by Tool

**Qualys / Tenable patch compliance:**
```bash
# Query Tenable.io for patch compliance data
curl -s -H "X-ApiKey: accessKey=<ak>;secretKey=<sk>" \
  "https://cloud.tenable.com/workbenches/assets/vulnerabilities" \
  | jq '.vulnerabilities[] | select(.plugin_family=="Windows : Microsoft Bulletins") | {name,severity,count}'
```

**Azure Update Manager:**
```bash
# List VMs with missing critical updates
az maintenance configuration list -o table

# Check update status for a VM
az maintenance update list -g <rg> --resource-name <vm-name> --resource-type VirtualMachines \
  --provider-name Microsoft.Compute \
  --query '[?properties.maintenanceScope==`InGuestPatch`]'
```

## Exception Handling

When a patch cannot be applied within the SLA:
1. Document the exception with system name, patch, and reason
2. Identify compensating controls (WAF rule, network segmentation, IDS signature)
3. Set review date (maximum 30-day extension for non-critical systems)
4. Obtain security team and management sign-off
5. Track in vulnerability management system
