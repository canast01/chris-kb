# PowerShell — Troubleshooting


```
┌──────────────────────────────────── PowerShell — Troubleshooting ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   PowerShell troubleshooting: execution errors, remoting failures, module issues, DSC drift   │   │
│   │     Enable verbose output: $VerbosePreference = "Continue"; add -Verbose flag to commands     │   │
│   │            Check $Error[0] for last error; $Error[0].InnerException for root cause            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Common Issues                 │  │             Diagnostic Commands             │   │
│   │        Execution policy blocks script        │  │          Get-ExecutionPolicy -List          │   │
│   │       Module not found on remote host        │  │          $Error[0] | Format-List *          │   │
│   │           WinRM: Access is denied            │  │          Test-WSMan <host> -UseSSL          │   │
│   │     Credential prompt in non-interactive     │  │          Get-PSSessionConfiguration         │   │
│   │           Double-hop auth failure            │  │           Invoke-Command -Verbose           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Double-hop = remoting from host A to B to C; Kerberos fails; use JEA or resource-based KCD  │   │
│   │   KCD        = Kerberos Constrained Delegation; allows service on B to request tickets for C  │   │
│   │           $Error[0]  = most recent error in session; always check before escalating           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Common workflow failures and resolutions.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Debug logging, runner diagnostics, and analysis.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Escalation paths and GitHub support.</span>
</a>

</div>
