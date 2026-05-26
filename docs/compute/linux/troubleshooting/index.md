# Linux — Troubleshooting


```
┌─────────────────────────────────────── Linux — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│  Linux troubleshooting: system performance, storage, network, and service failures.                   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Performance         │  │           Storage           │  │           Network           │   │
│   │  top / htop: CPU breakdown  │  │   df -h: filesystem usage   │  │      ping / traceroute      │   │
│   │  vmstat / sar: memory trend │  │    iostat: disk I/O stats   │  │    ss -tulpn: open ports    │   │
│   │perf / strace: deep profiling│  │      dmesg: disk errors     │  │   tcpdump: packet capture   │   │
│   │    OOM → dmesg | grep oom   │  │   fsck: filesystem repair   │  │     dig: DNS resolution     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · CPU · RAM · NIC · storage disks                                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vmstat       = virtual memory stats; shows CPU, swap, I/O wait over interval                         │
│  sar          = System Activity Reporter; historical performance data                                 │
│  perf         = Linux performance analysis tool; CPU profiling, tracing                               │
│  strace       = traces syscalls of a process; reveals file/network ops                                │
│  tcpdump      = packet capture; filters by interface, port, host                                      │
│  iostat       = I/O statistics per disk; part of sysstat package                                      │
│  fsck         = filesystem check/repair; run on unmounted filesystem                                  │
│  dmesg        = kernel ring buffer; hardware events, disk errors, OOM kills                           │
│  OOM          = Out of Memory; kernel kills process to free RAM                                       │
│  iowait       = CPU time waiting for I/O; high value = disk bottleneck                                │
│  load average = 1/5/15-min runqueue depth; > nCPU = saturation                                        │
│  tcpdump -nn  = no hostname/port resolution; faster capture output                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
