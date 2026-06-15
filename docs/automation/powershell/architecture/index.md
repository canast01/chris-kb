---
tags:
  - architecture
  - powershell
---
# PowerShell — Architecture

<div class="kb-summary">
Cross-platform automation shell on .NET; execution engine processes input through parser → AST → runspace → pipeline; remoting via WinRM (5985/5986) or SSH; module system with PSGallery distribution; runspace pools for parallelism.

*Applies to: PowerShell 7.x*
</div>

```text
┌─────────────────────────── PowerShell Architecture — Pipeline and Remoting ───────────────────────────┐
│                                                                                                       │
│  Cross-platform .NET shell; parser -> AST -> runspace -> pipeline execution;                          │
│  WinRM (5985/5986) or SSH remoting; PSGallery modules; runspace pools.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Execution Engine               │  │                   Remoting                  │   │
│   │            Parser: tokenise input            │  │            WinRM: port 5985 HTTP            │   │
│   │          AST: abstract syntax tree           │  │            WinRM HTTPS: port 5986           │   │
│   │         Runspace: execution context          │  │           SSH: PSRemoting over SSH          │   │
│   │          Pipeline: object streaming          │  │         Enter-PSSession: interactive        │   │
│   │        Cmdlets: verb-noun convention         │  │         Invoke-Command: scriptblock         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Pipeline passes .NET objects between cmdlets — no text parsing needed.                               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Module System                 │  │                Runspace Pools               │   │
│   │          PSGallery: public registry          │  │         RunspacePool: parallel jobs         │   │
│   │         Install-Module: NuGet fetch          │  │        ForEach-Object -Parallel (PS7)       │   │
│   │          PSModulePath: search dirs           │  │         Thread jobs: Start-ThreadJob        │   │
│   │         Private repo: Register-Repo          │  │        ThrottleLimit: max concurrent        │   │
│   │         Module manifest: .psd1 file          │  │         State isolation per runspace        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Windows/Linux host running pwsh; WinRM listener enabled on Windows targets;                          │
│  SSH on Linux targets; PSGallery requires outbound HTTPS to powershellgallery.com.                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cmdlet        = compiled or script function; verb-noun naming convention                             │
│  Pipeline      = | operator; passes objects (not strings) between cmdlets                             │
│  Runspace      = isolated execution context; each session gets one                                    │
│  AST           = Abstract Syntax Tree; parsed representation of script                                │
│  WinRM         = Windows Remote Management; SOAP over HTTP; 5985/5986                                 │
│  PSRemoting    = PowerShell remoting framework; works over WinRM or SSH                               │
│  Execution Policy= controls script loading; Bypass/Unrestricted for automation                        │
│  PSGallery     = public module repository at powershellgallery.com                                    │
│  RunspacePool  = pre-created runspace set; amortises startup cost                                     │
│  -Parallel     = PS7 ForEach-Object parallel; uses thread jobs under the hood                         │
│  Start-Job     = background process job; separate process; higher overhead                            │
│  psd1          = module manifest; declares version, deps, exported names                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![PowerShell Architecture](../../../assets/powershell-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Execution engine, pipeline, remoting (WinRM/SSH), module system, and runspace model.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## PowerShell Core vs Windows PowerShell

| Attribute | Windows PowerShell | PowerShell 7+ |
|---|---|---|
| Runtime | .NET Framework 4.x | .NET 6 / 7 / 8 (cross-platform) |
| Platforms | Windows only | Windows, Linux, macOS |
| Version | 5.1 (final) | 7.x (active development) |
| Remoting | WinRM only | WinRM + SSH |
| Release cadence | Security patches only | Active feature releases |

## Execution Engine

