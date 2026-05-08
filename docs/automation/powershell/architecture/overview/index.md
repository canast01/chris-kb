# PowerShell — Architecture Overview

PowerShell is a cross-platform task automation shell built on .NET. Understanding its internals is essential for building reliable, maintainable automation at enterprise scale.

---

## PowerShell Core vs Windows PowerShell

| Attribute | Windows PowerShell | PowerShell Core / PowerShell 7+ |
|---|---|---|
| Runtime | .NET Framework 4.x | .NET 6 / 7 / 8 (cross-platform) |
| Platforms | Windows only | Windows, Linux, macOS |
| Version | 5.1 (final, no new features) | 7.x (active development) |
| Module support | Full Windows module library | Some Windows-only modules unavailable |
| Remoting | WinRM only | WinRM + SSH |
| Release cadence | Security patches only | Active feature releases |
| Config location | `%APPDATA%\Microsoft\Windows\PowerShell` | `~/.config/powershell` |
| `$PSVersionTable.PSEdition` | `Desktop` | `Core` |

Windows PowerShell 5.1 remains the default on all Windows Server versions. PowerShell 7 must be installed separately and runs side-by-side. Always target PowerShell 7 for new automation unless a dependency is hard-bound to Desktop edition.

---

## Execution Engine

The PowerShell execution engine processes input through a well-defined sequence. Each statement passes through the **parser**, is compiled to an **AST (Abstract Syntax Tree)**, and is evaluated by the **runtime** against the active **runspace**.

```mermaid
flowchart LR
    A([Input<br/>stdin / script / command]) --> B[Lexer & Parser]
    B --> C[AST\nAbstract Syntax Tree]
    C --> D[Binder\nType resolution]
    D --> E[Compiled Script Block]
    E --> F{Runspace}
    F --> G[Command Discovery\nAlias → Function → Cmdlet → Native]
    G --> H[Parameter Binding]
    H --> I[Pipeline Processor]
    I --> J[Output / Objects]
    J --> K([stdout / next cmdlet / $null])
    I --> L([Error Stream\n$Error / Write-Error])
    style F fill:#1565c0,color:#fff
    style I fill:#2e7d32,color:#fff
```

### Pipeline Processing

The pipeline is the fundamental unit of composition. Objects flow between cmdlets without serialisation — full .NET objects pass in memory between pipeline stages.

```powershell
# Each stage receives full .NET objects
Get-Process |
    Where-Object { $_.CPU -gt 10 } |
    Select-Object Name, Id, CPU |
    Sort-Object CPU -Descending |
    Export-Csv -Path /tmp/high_cpu.csv -NoTypeInformation
```

Key pipeline mechanics:

- `begin {}` block runs once before pipeline input arrives
- `process {}` block runs once per input object (`$_` / `$PSItem`)
- `end {}` block runs once after all input is consumed
- `$input` automatic variable accumulates all pipeline input in non-pipeline functions

---

## Remoting

### WinRM (Windows Remote Management)

WinRM is the default remoting transport on Windows. It uses HTTP (5985) or HTTPS (5986) and SOAP/WSMan.

```powershell
# Enable WinRM on a target (run as admin on target)
Enable-PSRemoting -Force

# Test connectivity
Test-WSMan -ComputerName srv-prod-01 -Authentication Default

# One-off remote command
Invoke-Command -ComputerName srv-prod-01 -ScriptBlock {
    Get-Service -Name WinRM
}

# Persistent session (reuse for multiple commands)
$session = New-PSSession -ComputerName srv-prod-01 -Credential (Get-Credential)
Invoke-Command -Session $session -ScriptBlock { hostname }
Remove-PSSession $session
```

### SSH Remoting (PowerShell 7+)

SSH remoting works across platforms and does not require WinRM.

```powershell
# Requires PowerShell 7 on both ends; sshd configured with PowerShell subsystem
# /etc/ssh/sshd_config: Subsystem powershell /usr/bin/pwsh -sshs -NoLogo

$session = New-PSSession -HostName linux-host-01 -UserName svcaccount -SSHTransport
Invoke-Command -Session $session -ScriptBlock { uname -a }
```

---

## Module System

Modules are the primary packaging unit. A module is a directory containing a manifest (`.psd1`) and one or more script files (`.psm1`) or binary DLLs (`.dll`).

```
MyModule/
├── MyModule.psd1      # Manifest: metadata, exports, dependencies
├── MyModule.psm1      # Root module: dot-sources private functions
├── Public/            # Exported functions
│   ├── Get-Widget.ps1
│   └── Set-Widget.ps1
└── Private/           # Internal helpers (not exported)
    └── Invoke-WidgetApi.ps1
```

```powershell
# Module discovery paths (ordered)
$env:PSModulePath -split [IO.Path]::PathSeparator

# Install from PSGallery
Install-Module -Name PSFramework -Scope CurrentUser -Repository PSGallery

# Import with explicit version
Import-Module MyModule -RequiredVersion 2.3.1

# Inspect what a module exports
Get-Module MyModule | Select-Object -ExpandProperty ExportedFunctions
```

### Module Manifest Key Fields

```powershell
@{
    ModuleVersion   = '2.3.1'
    GUID            = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    Author          = 'Platform Automation Team'
    Description     = 'Widget management automation'
    PowerShellVersion = '7.2'
    RequiredModules = @('PSFramework')
    FunctionsToExport = @('Get-Widget','Set-Widget','Remove-Widget')
    PrivateData     = @{
        PSData = @{
            Tags = @('Widget','Automation')
        }
    }
}
```

---

## Runspace Model

A **runspace** is an isolated instance of the PowerShell execution environment. Each session has one default runspace. For parallelism, multiple runspaces can be created and managed via runspace pools.

```powershell
# Parallel processing with runspace pool (more efficient than ForEach-Object -Parallel for large sets)
$pool = [RunspaceFactory]::CreateRunspacePool(1, 8)  # min 1, max 8 concurrent
$pool.Open()

$jobs = foreach ($server in $servers) {
    $ps = [PowerShell]::Create()
    $ps.RunspacePool = $pool
    [void]$ps.AddScript({
        param($s)
        Test-Connection -ComputerName $s -Count 1 -Quiet
    }).AddArgument($server)

    [PSCustomObject]@{
        Server    = $server
        PowerShell = $ps
        Handle    = $ps.BeginInvoke()
    }
}

$results = foreach ($job in $jobs) {
    [PSCustomObject]@{
        Server = $job.Server
        Online = $job.PowerShell.EndInvoke($job.Handle)[0]
    }
    $job.PowerShell.Dispose()
}

$pool.Close()
$pool.Dispose()
```

PowerShell 7 also exposes `ForEach-Object -Parallel` as a simpler surface for moderate parallelism:

```powershell
$servers | ForEach-Object -Parallel {
    Test-Connection -ComputerName $_ -Count 1 -Quiet
} -ThrottleLimit 10
```

---

## Key Automatic Variables

| Variable | Description |
|---|---|
| `$_` / `$PSItem` | Current pipeline object |
| `$PSVersionTable` | Runtime version information |
| `$Error` | Array of recent error records (newest at index 0) |
| `$LASTEXITCODE` | Exit code of the last native command |
| `$PSCommandPath` | Full path of the running script file |
| `$PSScriptRoot` | Directory containing the running script |
| `$env:PSModulePath` | Colon/semicolon-separated module search paths |
| `$ConfirmPreference` | Threshold for automatic `-Confirm` prompts |
| `$ErrorActionPreference` | Default action on non-terminating errors |
| `$VerbosePreference` | Controls `Write-Verbose` output |
