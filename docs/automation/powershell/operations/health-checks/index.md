# PowerShell — Health Checks

## PowerShell Environment Health Check Flow

```mermaid
flowchart TD
    start["Start Health Check"]
    checkVersion["$PSVersionTable\nExpected PS version?"]
    checkPolicy["Get-ExecutionPolicy\nRemoteSigned or better?"]
    checkModules["Required modules\ninstalled at expected versions?"]
    checkWinRM["Test-WSMan target hosts\nWinRM reachable?"]
    checkTasks["Get-ScheduledTask\nAny Disabled that should run?"]
    checkLogs["Get-WinEvent PowerShell/Operational\nErrors in last 24h?"]
    healthy["Status: HEALTHY"]
    alertVersion["Alert: Update\nPowerShell version"]
    alertPolicy["Alert: Fix\nexecution policy"]
    alertModules["Alert: Update-Module\nor Install-Module"]
    alertWinRM["Alert: Enable-PSRemoting\non target hosts"]
    alertLogs["Alert: Review\nPS operational log"]

    start --> checkVersion
    checkVersion -->|OK| checkPolicy
    checkVersion -->|Fail| alertVersion
    checkPolicy -->|OK| checkModules
    checkPolicy -->|Fail| alertPolicy
    checkModules -->|OK| checkWinRM
    checkModules -->|Fail| alertModules
    checkWinRM -->|OK| checkTasks
    checkWinRM -->|Fail| alertWinRM
    checkTasks --> checkLogs
    checkLogs -->|None| healthy
    checkLogs -->|Errors| alertLogs
```
┌───────────────────────────────────── PowerShell — Health Checks ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  PowerShell health checks: verify PS version, remoting, module currency, and script execution │   │
│   │      Check: $PSVersionTable.PSVersion, Test-WSMan, Get-PSRepository, PSScriptAnalyzer run     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Version and Environment            │  │               Remoting Health               │   │
│   │          $PSVersionTable.PSVersion           │  │            Test-WSMan <hostname>            │   │
│   │          Get-Module -ListAvailable           │  │        Test-NetConnection -port 5985        │   │
│   │       Get-InstalledModule (PSGallery)        │  │          Get-PSSessionConfiguration         │   │
│   │          Get-ExecutionPolicy -List           │  │            winrm get winrm/config           │   │
│   │        Invoke-ScriptAnalyzer -Path .         │  │          Check JEA endpoints active         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           $PSVersionTable = hash table with PS version, OS, runtime, and build info           │   │
│   │     Test-WSMan      = validates WinRM connectivity and config on remote host; returns XML     │   │
│   │ExecutionPolicy = check per scope: Process, CurrentUser, LocalMachine; Restricted blocks all .p│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
