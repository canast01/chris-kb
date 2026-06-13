---
tags:
  - troubleshooting
  - windows
search:
  boost: 1.5
---
# Windows Server — Troubleshooting



<div class="kb-summary">
Diagnosing Windows Server failures — services, event logs, WMI errors, performance degradation, and common boot issues.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌────────────────────────────── Windows Server — Troubleshooting Overview ──────────────────────────────┐
│                                                                                                       │
│  Structured troubleshooting: common issues first, diagnostics second, escalation when needed.         │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │ Service failures + restarts │  │  Event Viewer: Sys+App logs │  │      Vendor TAC engage      │   │
│   │   Performance degradation   │  │   Perfmon: counters + logs  │  │      MS Premier support     │   │
│   │    AD replication errors    │  │   WinRM test connectivity   │  │     Dump analysis (.dmp)    │   │
│   │  Network connectivity loss  │  │   netsh trace capture pkt   │  │    Kernel debugger attach   │   │
│   │      Boot/BSOD failures     │  │     WER reports analysis    │  │      SysInternals tools     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Start with Event Viewer and Perfmon; escalate with dump files and SysInternals traces.               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Log Sources         │  │          CLI Tools          │  │       Escalation Packs      │   │
│   │   System / Application log  │  │    Get-EventLog/wevtutil    │  │    memory.dmp (full/mini)   │   │
│   │      Security audit log     │  │      netstat / tcpview      │  │       procmon boot log      │   │
│   │        DNS debug log        │  │      repadmin / dcdiag      │  │       netsh trace ETL       │   │
│   │        DHCP audit log       │  │     ipconfig / nslookup     │  │      PsInfo + autoruns      │   │
│   │      Hyper-V event log      │  │     diskmgmt + diskpart     │  │     sfc /scannow + dism     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · iDRAC/iLO OOB console · crash dump storage · network tap                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Event Viewer   = MMC snap-in; shows System, Application, Security, custom logs                       │
│  Perfmon        = Performance Monitor; tracks CPU/RAM/disk/network counters over time                 │
│  WER            = Windows Error Reporting; collects crash and hang data for analysis                  │
│  netsh trace    = packet and event tracing; outputs .etl file for Network Monitor                     │
│  WinRM          = Windows Remote Management; Test-WSMan verifies connectivity                         │
│  repadmin       = AD replication diagnostics; /replsummary + /showrepl                                │
│  dcdiag         = Domain Controller diagnostic tool; tests DNS, replication, services                 │
│  SysInternals   = Microsoft tools: procmon, procexp, autoruns, pstools, tcpview                       │
│  memory.dmp     = full kernel crash dump; written to %SystemRoot% on BSOD                             │
│  BSOD           = Blue Screen of Death; kernel panic; error code in minidump                          │
│  sfc            = System File Checker; verifies and repairs protected OS files                        │
│  dism           = Deployment Image Servicing; repairs Windows component store                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known failure modes, symptoms, causes, and fixes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>What to collect before opening a support case and how to engage vendor support.</span>
</a>

</div>

