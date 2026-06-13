---
tags:
  - powercli
  - troubleshooting
  - vmware
---
# PowerCLI — Troubleshooting

<div class="kb-summary">
Diagnosing and resolving PowerCLI issues: connection failures, module conflicts, API errors, certificate problems, and performance issues with large inventories.
</div>

```text
┌──────────────────────────────── PowerCLI — Troubleshooting Reference ─────────────────────────────────┐
│                                                                                                       │
│   PowerCLI issues fall into three categories: connection, module, and API/performance problems        │
│   Enable verbose output with -Verbose or $VerbosePreference = 'Continue' for immediate diagnosis      │
│   Collect: module version, vCenter version, error message, and ExtensionData trace for escalation     │
│                                                                                                       │
│   Common issues                                                                                       │
│   Certificate error on connect: set InvalidCertificateAction = Ignore (lab) or import CA cert (prod)  │
│   Module not found: run Install-Module VMware.PowerCLI; check PSModulePath includes install dir       │
│   Session expired: check $global:DefaultVIServers.IsConnected; reconnect if $false                    │
│   Cmdlet parameter error: check Get-Help -Full; parameter may not exist on older vCenter API version  │
│                                                                                                       │
│   Diagnostics                                                                                         │
│   Verbose/debug: $VerbosePreference = 'Continue'; add -Verbose to specific cmdlet calls               │
│   API tracing: use $vm.ExtensionData to inspect the raw vSphere API response object properties        │
│   Large inventory performance: use Get-View instead of Get-VM for queries across >500 VMs             │
│                                                                                                       │
│   Escalation                                                                                          │
│   Collect: Get-Module VMware.* output + vCenter version + full error message + minimal repro script   │
│   Check VMware PowerCLI Community (community.vmware.com) before opening a support case                │
│   Escalate to VMware GSS: API returns undocumented error code or cmdlet produces inconsistent output  │
│                                                                                                       │
│   Key terms:                                                                                          │
│   ExtensionData = raw Managed Object Reference from the vSphere API; bypasses the PowerCLI layer      │
│   Get-View      = low-level vSphere API query; significantly faster than Get-VM for large sets        │
│   PSModulePath  = environment variable listing directories where PowerShell searches for modules      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Connection failures, certificate errors, module not found, cmdlet parameter errors, and session timeouts.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Debug mode, API call tracing, performance profiling, and log collection for escalation.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Diagnostic info collection, VMware support case process, API error codes, and community resources.</span>
</a>

</div>
