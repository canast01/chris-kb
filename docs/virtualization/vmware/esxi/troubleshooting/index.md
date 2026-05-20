# ESXi — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware ESXi. Covers common host failure patterns, diagnostic commands, log collection, and escalation procedures for engaging VMware support.
</div>

```
┌─────────────────────────────────────── ESXi — Troubleshooting ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   ESXi troubleshooting: common failure patterns, diagnostic commands, and escalation process  │   │
│   │ Common issues: PSOD (purple screen), host disconnect from vCenter, storage path loss, vMotion │   │
│   │ Diagnostics: esxcli for live state, esxtop for real-time perf, vmkernel.log for kernel events │   │
│   │      Log collection: vm-support bundle collects all host logs; attach to GSS support case     │   │
│   │    Escalation: P1 for production VMs down; TAM escalation for critical/sustained incidents    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate root cause                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │      PSOD: kernel panic     │  │      esxtop: live perf      │  │      vm-support bundle      │   │
│   │     Host disconnect vCtr    │  │     vmkernel.log events     │  │       GSS: P1/P2 case       │   │
│   │     Storage path failure    │  │     esxcli storage list     │  │        TAM escalation       │   │
│   │     vMotion fail: VMk IP    │  │      esxcli network cmd     │  │       vmx + log bundle      │   │
│   │       HA agent restart      │  │      /var/log/vmkernel      │  │       HCL / BOM match       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics pinpoint root cause                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │   PSOD / panic   │  esxtop -b -n5   │    /var/log/vmk   │  vm-support.tgz  │   reboot host    │   │
│   │ Host disconnect  │  esxcli storage  │   /var/log/hostd  │   GSS P1 case    │  restart hostd   │   │
│   │   Path APD/PDL   │  esxcli network  │   /var/log/vpxa   │   TAM escalate   │   rescan HBAs    │   │
│   │   vMotion fail   │  /var/log/vmkw   │  /var/log/syslog  │   HCL validate   │  HA restart VM   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server · CPUs · RAM DIMMs · PCIe HBAs/NICs · SAS/NVMe disks · iDRAC/iLO OOB console              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PSOD          = Purple Screen of Death; ESXi kernel panic; check /var/log/vmkernel for root cause    │
│  APD           = All Paths Down; storage device unreachable; all paths to LUN failed simultaneously   │
│  PDL           = Permanent Device Loss; storage reports device gone; triggers VM failover if HA       │
│  vm-support    = ESXi log bundle collector; generates .tgz with all host logs for GSS cases           │
│  hostd         = ESXi host agent; handles vCenter communication; restart if host shows disconnected   │
│  vpxa          = vCenter agent on ESXi; proxies vCenter management; restart to fix vCenter disconnect │
│  esxtop        = ESXi real-time monitor; -b batch mode; -n iteration count; CSV output for analysis   │
│  GSS           = Global Support Services; VMware/Broadcom support; P1=production down, P2=degraded    │
│  TAM           = Technical Account Manager; named support resource; escalation for critical incidents │
│  HCL           = Hardware Compatibility List; validates server/driver/firmware combinations for ESXi  │
│  BOM           = Bill of Materials; version matrix for ESXi, FW, and driver compatibility             │
│  vmkfstools    = ESXi VMDK utility: clone, inflate, check, convert disk formats                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
