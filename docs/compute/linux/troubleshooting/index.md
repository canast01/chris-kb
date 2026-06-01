# Linux — Troubleshooting



<div class="kb-summary">
Linux — Troubleshooting navigation for Common Issues, Diagnostics, Escalation.
</div>

```
┌────────────────────────────────── Linux — Troubleshooting Overview ───────────────────────────────────┐
│                                                                                                       │
│  Structured approach to Linux problem diagnosis: common issues, diagnostics, escalation.              │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │       Perf degradation      │  │      dmesg / journalctl     │  │        Vendor support       │   │
│   │       Network failures      │  │       strace / ltrace       │  │       Escalation path       │   │
│   │       Disk / FS errors      │  │       perf / bpftrace       │  │        Runbook links        │   │
│   │       Service crashes       │  │        gdb / coredump       │  │         P1 contacts         │   │
│   │        Auth failures        │  │         tcpdump / ss        │  │         RCA template        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · IPMI/iDRAC (OOB access) · console cable · NIC · storage                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  strace      = Traces system calls made by a process; essential for debugging                         │
│  ltrace      = Traces library calls; complements strace for userspace debugging                       │
│  perf        = Linux performance analysis tool; CPU sampling and tracing                              │
│  bpftrace    = eBPF-based tracing tool; powerful kernel and app observability                         │
│  gdb         = GNU debugger; inspects running processes and core dumps                                │
│  coredump    = Memory snapshot of crashed process; analysed with gdb                                  │
│  dmesg       = Kernel ring buffer; first check for hardware/driver errors                             │
│  journalctl  = Query systemd journal; -u for unit, -b for boot, -f follow                             │
│  IPMI        = Out-of-band management; console access even when OS is down                            │
│  RCA         = Root Cause Analysis; post-incident document explaining failure                         │
│  tcpdump     = Packet capture tool; diagnose network-level communication issues                       │
│  OOB         = Out-of-Band; management network separate from production traffic                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
