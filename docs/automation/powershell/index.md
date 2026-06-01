# PowerShell

<div class="kb-summary">
PowerShell automation knowledge base covering execution engine internals, pipeline model, WinRM and SSH remoting, module development, runspace pools, and scripting patterns for Windows and cross-platform infrastructure automation.
</div>

```powershell
┌───────────────────────────── PowerShell — Shell and Scripting Automation ─────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  PowerShell: Microsoft shell and scripting language; cross-platform since PowerShell 7 (Core) │   │
│   │  Object pipeline: commands pass .NET objects, not text — enables structured data manipulation │   │
│   │  Modules: PSGallery ecosystem; key infra modules: Az, ActiveDirectory, VMware.PowerCLI, Dell  │   │
│   │  PowerShell 5.1 = Windows-only (built-in); PowerShell 7+ = cross-platform (separate install)  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │       Object pipeline       │  │      Script management      │  │       Execution policy      │   │
│   │     Modules + PSGallery     │  │       Remoting (WinRM)      │  │       Constrained lang      │   │
│   │      DSC configuration      │  │       Scheduled tasks       │  │        JEA endpoints        │   │
│   │      PS7 cross-platform     │  │        Error handling       │  │       AMSI integration      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  PowerShell 5.1  = ships with Windows; cannot be updated separately; for Windows-only scripts │   │
│   │       PowerShell 7    = .NET Core-based; install separately; recommended for new scripts      │   │
│   │   PSGallery       = Microsoft-hosted module repository; Install-Module / Install-PSResource   │   │
│   │   DSC             = Desired State Configuration; declarative resource model for node config   │   │
│   │      WinRM           = Windows Remote Management; enables Invoke-Command to remote hosts      │   │
│   │     JEA             = Just Enough Administration; constrained endpoint for delegated admin    │   │
│   │    AMSI            = Antimalware Scan Interface; Windows scans PS scripts before execution    │   │
│   │           PowerCLI        = VMware PowerShell module for vSphere/vSAN/NSX management          │   │
│   │          Az module       = Microsoft Azure PowerShell module; replacement for AzureRM         │   │
│   │          CmdLet          = compiled command implementing Verb-Noun naming convention          │   │
│   │          Pipeline        = | character passes output objects as input to next command         │   │
│   │      ExecutionPolicy = Restricted/AllSigned/RemoteSigned/Unrestricted; per-scope setting      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, scripts, procedures, and health checks.</span>
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
