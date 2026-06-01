# Venafi Vendor Support


<div class="kb-summary">
Procedures for raising support cases with Venafi, collecting diagnostic data, and escalating critical incidents.
</div>
```text
┌──────────────────────────── Security Venafi Troubleshooting — Escalation ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Venafi escalation: severity triage, vendor support contact, and required artifacts      │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
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
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Venafi Troubleshooting infrastructure · management network · monitoring         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Venafi             = Security Venafi Troubleshooting platform overview and core concepts           │
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


---
## Support Portal

| Item | Detail |
|---|---|
| Support portal | https://support.venafi.com |
| Knowledge base | https://support.venafi.com/hc/en-us |
| Version compatibility matrix | https://support.venafi.com/hc/en-us/articles/360024789251 |
| EOL / Support lifecycle | https://support.venafi.com/hc/en-us/articles/360024784232 |
| Community forum | https://community.venafi.com |

Log in with your Venafi support account credentials. Support entitlement (Premier, Premier Plus) determines available SLA tiers and access to named technical account managers.

---

## Severity Levels and SLA

| Severity | Description | Initial Response (Premier) |
|---|---|---|
| Sev 1 — Critical | Production TPP down; no certificates can be issued or renewed | 1 hour (phone + portal) |
| Sev 2 — High | Major feature degraded; workaround available | 4 hours |
| Sev 3 — Medium | Non-critical feature impaired | 1 business day |
| Sev 4 — Low | General questions, feature requests, documentation | 2 business days |

For Sev 1: open the portal ticket AND call the Venafi support hotline simultaneously. Phone number is listed in the support portal after authentication.

---

## Pre-Collection Checklist

Collect the following before opening any support case to reduce round-trips:

### TPP Version and Environment

```powershell
# TPP version (run on TPP Policy Server)
Get-ItemProperty "HKLM:\Software\Venafi\Platform" | Select-Object ProductVersion

# Installed hotfixes
Get-WmiObject Win32_QuickFixEngineering | Sort-Object InstalledOn -Descending | Select-Object -First 10

# OS and hardware details
Get-ComputerInfo | Select-Object WindowsProductName, OsVersion, CsProcessors, CsTotalPhysicalMemory
```

### Log Collection

```powershell
# TPP application logs (primary location)
$logPath = "$env:ProgramData\Venafi\log\"
Get-ChildItem $logPath -Filter "VdcLogFile*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# Collect last 24 hours of logs
$cutoff = (Get-Date).AddHours(-24)
Get-ChildItem $logPath -Filter "VdcLogFile*.log" |
  Where-Object { $_.LastWriteTime -gt $cutoff } |
  ForEach-Object { Copy-Item $_.FullName "C:\Temp\VenafiLogs\" }

# Windows Event Log — Application source (Venafi)
Get-WinEvent -FilterHashtable @{ LogName = "Application"; ProviderName = "Venafi*" } -MaxEvents 500 |
  Select-Object TimeCreated, LevelDisplayName, Message |
  Export-Csv "C:\Temp\Venafi_EventLog.csv" -NoTypeInformation
```

### CA Connector Diagnostics

```powershell
# Test CA connector connectivity from TPP server
# For ADCS (CES endpoint):
Invoke-WebRequest -Uri "https://adcs.corp.example.com/ADPolicyProvider_CEP_UsernamePassword/service.svc/CEP" `
  -UseDefaultCredentials

# For external CA (DigiCert, Entrust):
Test-NetConnection -ComputerName "www.digicert.com" -Port 443
```

---

## Required Information for SR

Include all of the following in the initial SR submission:

- TPP version (e.g., `23.4.1.xxx`)
- Windows Server OS version on TPP nodes
- SQL Server version and edition
- CA type and version (e.g., ADCS on Server 2022, DigiCert connector version)
- Approximate total managed certificate count
- Error message with exact timestamp
- Steps to reproduce (if applicable)
- Business impact and affected certificates/services
- Log files from the pre-collection checklist (attach to ticket)

---

## Escalation Path

1. Open portal ticket at support.venafi.com with full pre-collection data.
2. For Sev 1: call support hotline (number in portal after authentication).
3. If no response within SLA: request escalation to Senior Support Engineer via portal.
4. If business-critical escalation needed beyond support: contact your Venafi Technical Account Manager (TAM) or Customer Success Manager (CSM).

## Escalation Decision Flow

```mermaid
flowchart TD
    issue["Venafi issue detected"]
    issue --> severity{"Severity\nassessment"}
    severity -->|"production TPP down\nno certs can issue"| sev1["Sev 1 — Critical"]
    severity -->|"major feature degraded\nworkaround available"| sev2["Sev 2 — High"]
    severity -->|"non-critical feature\nimpaired"| sev3["Sev 3 — Medium"]
    sev1 --> preCollect["Run pre-collection\nchecklist (TPP version, logs, CA diag)"]
    sev2 --> preCollect
    sev3 --> openPortal["Open portal ticket\nsupport.venafi.com"]
    preCollect --> openPortal
    openPortal -->|"Sev 1"| callHotline["Call Venafi support hotline\nsimultaneously"]
    callHotline --> slaCheck{"Response within SLA?"}
    slaCheck -->|"no"| escalateSSE["Request escalation to\nSenior Support Engineer"]
    escalateSSE --> tamEscalate["Contact TAM / CSM\nfor business-critical escalation"]
    slaCheck -->|"yes"| workWithSupport["Work with support engineer\nto resolution"]
```
