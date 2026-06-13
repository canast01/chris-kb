---
tags:
  - operations
---
# Operations

<div class="kb-summary">
Operational procedures, health checks, troubleshooting guides, and runbooks for the virtualization platform.
</div>

```text
┌───────────────────────────────────── VMware Operations Overview ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   VMware Platform Operations                                  │   │
│   │      vCenter: cluster, host, and VM management · Aria Operations: performance dashboards      │   │
│   │         Log Insight / Aria Log Intelligence: log aggregation, search, and correlation         │   │
│   │         CLI: esxcli (host ops) · govc (scripted vCenter tasks) · PowerCLI (automation)        │   │
│   │         vROps capacity analytics: right-sizing, trend forecasting, workload placement         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Management tools cover health monitoring, troubleshooting, and runbook execution                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Health Checks        │  │       Troubleshooting       │  │           Runbooks          │   │
│   │  Cluster capacity headroom  │  │    VM boot failures: logs   │  │    Host maintenance mode    │   │
│   │  vSAN health service check  │  │   Network: vmkping/traffic  │  │   Rolling patch procedure   │   │
│   │  Host connectivity: vCenter │  │   Storage latency: esxtop   │  │    VM snapshot management   │   │
│   │   Alarm: red/yellow review  │  │   ESXi PSOD: vmkernel dump  │  │    Cert renewal workflow    │   │
│   │   Cert expiry + NTP drift   │  │   HA/DRS: config + events   │  │    VDS port group changes   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Health checks prevent outages · troubleshooting resolves them · runbooks standardise ops           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Monitoring         │  │         Maintenance         │  │          Automation         │   │
│   │  vCenter performance charts │  │    Maintenance mode evac    │  │  PowerCLI: Connect-VIServer │   │
│   │    Aria dashboards: vROps   │  │  VUM/LCM: upgrade baseline  │  │  govc: fast CLI operations  │   │
│   │   SNMP traps → monitoring   │  │  Cluster remediation order  │  │   vCenter REST API: HTTPS   │   │
│   │   Log alerts: query+notify  │  │   HA admission control adj  │  │    Event triggers: DRS/HA   │   │
│   │  Capacity: forecast/resize  │  │   DRS migration threshold   │  │    Scheduled tasks: recur   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Monitoring feeds maintenance decisions · automation scales operational repeatability               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      esxcli      │       govc       │      PowerCLI     │     REST API     │       SSH        │   │
│   │  ESXi host ops   │  vCenter tasks   │   vSphere module  │    HTTPS JSON    │   Direct host    │   │
│   │  Namespace cmds  │   VMOMI client   │   Cmdlet syntax   │  OAuth2 bearer   │     Port 22      │   │
│   │  esxcli --help   │   env GOVC_URL   │   Import-Module   │  Postman / curl  │     Auth key     │   │
│   │  sw/network/vm   │   vm.info / ls   │    Get-VM | ...   │   GET/POST/PUT   │   known_hosts    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts · vSAN datastores · vCenter appliance · NSX Managers · Power & Cooling                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter  = VMware vCenter Server; central management platform for hosts and VMs                      │
│  esxcli   = ESXi command-line utility; manages network, storage, and VM kernel modules                │
│  govc     = Go-based open-source vCenter CLI; wraps vSphere API for fast operations                   │
│  PowerCLI = VMware PowerShell module; 700+ cmdlets for full vSphere automation                        │
│  Aria Operations= VMware vROps; ML-based performance analytics and capacity management                │
│  PSOD     = Purple Screen of Death; ESXi kernel panic with vmkernel dump for analysis                 │
│  vSAN     = VMware hyperconverged storage; NVMe/SSD pools forming a cluster datastore                 │
│  DRS      = Distributed Resource Scheduler; auto-migrates VMs to balance CPU/memory                   │
│  HA       = High Availability; restarts VMs on surviving hosts after a host failure                   │
│  VUM      = vSphere Update Manager; baseline-based patching for ESXi hosts                            │
│  LCM      = Lifecycle Manager; successor to VUM; manages vSphere add-on lifecycle                     │
│  vROps    = VMware vRealize Operations; analytics engine in Aria Operations platform                  │
│  VDS      = vSphere Distributed Switch; cluster-level virtual switch managed by vCenter               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Pre- and post-change health checks, daily checks, and validation procedures.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Troubleshooting guides, known issues, and resolution steps across all platforms.</span>
</a>

<a class="kb-card" href="runbooks/">
  <strong>Runbooks</strong>
  <span>Step-by-step operational runbooks for common tasks and incidents.</span>
</a>

</div>

