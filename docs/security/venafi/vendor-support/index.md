# Venafi Vendor Support

Procedures for raising support cases with Venafi, collecting diagnostic data, and escalating critical incidents.

---

```mermaid
flowchart LR
    Vendor_Support["Vendor Support"]
    Vendor_Support --> S0["Support Portal"]
    Vendor_Support --> S1["Severity Levels and SLA"]
    Vendor_Support --> S2["Pre-Collection Checklist"]
    Vendor_Support --> S3["Required Information for SR"]
    Vendor_Support --> S4["Common Issues and First Steps"]
    Vendor_Support --> S5["Escalation Path"]
```

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

### Certificate-Specific Diagnostics

```powershell
# Get details of a specific certificate in Venafi via API
$certDN = "\\VED\\Policy\\Internal\\Production\\Servers\\app01.corp.example.com"
$body   = @{ CertificateDN = $certDN } | ConvertTo-Json

Invoke-RestMethod -Uri "https://venafi.corp.example.com/vedsdk/Certificates/Retrieve" `
  -Headers @{ "X-Venafi-API-Key" = $apiKey } `
  -Method Post -ContentType "application/json" -Body $body
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

## Common Issues and First Steps

| Symptom | First Check |
|---|---|
| Certificate renewal stuck in pending | Check CA connector health; verify CA is reachable; check approval workflow |
| TPP web UI unreachable | Verify IIS app pool running; check SQL connectivity; review VdcLogFile |
| Discovery scan finds no certificates | Check scan range, port list, and Edge Proxy registration |
| LDAP/AD auth failing in Venafi | Test LDAP bind from TPP server; verify service account password not expired |
| Syslog events not appearing in SIEM | Check Log Server service; verify syslog target IP/port; check firewall |

```powershell
# Quick health check: verify core Venafi services are running
Get-Service -Name "Venafi*" | Select-Object Name, Status, StartType

# Verify SQL connectivity
$sql = New-Object System.Data.SqlClient.SqlConnection
$sql.ConnectionString = "Server=sql01.corp.example.com;Database=VenafiDB;Integrated Security=True"
$sql.Open()
Write-Host "SQL connection: $($sql.State)"
$sql.Close()
```

---

## Escalation Path

1. Open portal ticket at support.venafi.com with full pre-collection data.
2. For Sev 1: call support hotline (number in portal after authentication).
3. If no response within SLA: request escalation to Senior Support Engineer via portal.
4. If business-critical escalation needed beyond support: contact your Venafi Technical Account Manager (TAM) or Customer Success Manager (CSM).
