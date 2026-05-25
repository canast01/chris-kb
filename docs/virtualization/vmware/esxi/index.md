---
title: ESXi
---

# ESXi

<div class="kb-summary">
Technical and operational reference for VMware ESXi. Covers host architecture, networking, storage paths, patching, security hardening, and troubleshooting for ESXi hosts managed by vCenter.
</div>

```
┌─────────────────────────────────────────── ESXi Host Stack ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    VMware ESXi — Type-1 Bare-Metal Hypervisor (VMkernel OS)                   │   │
│   │       VMkernel: micro-kernel manages CPU/memory/storage/network for all VMs on the host       │   │
│   │    VMkernel ports: Management · vMotion · vSAN · NFC · Replication — each on separate VLAN    │   │
│   │       Storage: local VMFS, SAN (FC/iSCSI/NVMe), NFS — all via storage adapters and PSPs       │   │
│   │          Networking: vSS or vDS; uplink teaming; port groups per workload or function         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VMkernel is the host foundation · networking and storage connect VMs                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │   VMkernel: CPU+RAM sched   │  │   DCUI: local console mgmt  │  │  Lockdown mode: strict/norm │   │
│   │   vSwitch/vDS: port groups  │  │     Patching: VUM / LCM     │  │   Firewall: service rules   │   │
│   │     HBAs: FC/iSCSI/NVMe     │  │  Host profiles: enforce std │  │   Secure boot: TPM verify   │   │
│   │ NIC teaming: active/standby │  │  esxcli: config + diagnose  │  │  SSH/Shell: disabled by std │   │
│   │  VMkernel ports: VMk0-VMkN  │  │    esxtop: real-time perf   │  │  Syslog: to vRLI or syslog  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines the host stack · Operations maintain health · Security hardens the hypervisor │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │PSOD: check vmkern│vm-support bundle │ Host conn: green? │GSS: support bundl│  esxcli system   │   │
│   │NFS unmount: check│esxcli storage lis│ HBA: link state OK│  TAM escalation  │  esxcli network  │   │
│   │vMotion fail: VMk │  esxtop -b -n 5  │ vSAN health: green│ Log bundle + vmx │  vmkfstools -i   │   │
│   │ HA agent restart │/var/log/vmkernel │   Uptime + tasks  │P1: production dow│  vim-cmd vmsvc   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server · CPUs (Intel/AMD) · RAM DIMMs · PCIe HBAs and NICs · SAS/NVMe disks · Power & Cooling    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VMkernel      = ESXi micro-kernel OS; manages CPU scheduling, memory balloon, and device I/O         │
│  DCUI          = Direct Console User Interface; local text console on ESXi host physical screen       │
│  VMkernel port = VMk NIC; carries management, vMotion, vSAN, NFC, or replication traffic              │
│  Lockdown mode = Host setting that prevents direct access; all management via vCenter only            │
│  Host Profile  = Saved configuration template applied to hosts for consistency enforcement            │
│  PSP           = Path Selection Policy; controls multipath selection: MRU, Fixed, or RR               │
│  vDS           = vSphere Distributed Switch; cluster-level virtual switch managed by vCenter          │
│  esxcli        = ESXi CLI framework; namespaces: system, network, storage, vm, software               │
│  esxtop        = ESXi real-time performance monitor; CPU/memory/disk/network counters per VM          │
│  vmkfstools    = CLI for VMDK operations: clone, resize, inflate, import/export                       │
│  PSOD          = Purple Screen of Death; ESXi kernel panic; check vmkernel log for cause              │
│  LCM           = Lifecycle Manager; patching engine in vCenter for ESXi host baselines                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────── ESXi Host Stack ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    VMware ESXi — Type-1 Bare-Metal Hypervisor (VMkernel OS)                   │   │
│   │       VMkernel: micro-kernel manages CPU/memory/storage/network for all VMs on the host       │   │
│   │    VMkernel ports: Management · vMotion · vSAN · NFC · Replication — each on separate VLAN    │   │
│   │       Storage: local VMFS, SAN (FC/iSCSI/NVMe), NFS — all via storage adapters and PSPs       │   │
│   │          Networking: vSS or vDS; uplink teaming; port groups per workload or function         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VMkernel is the host foundation · networking and storage connect VMs                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │   VMkernel: CPU+RAM sched   │  │   DCUI: local console mgmt  │  │  Lockdown mode: strict/norm │   │
│   │   vSwitch/vDS: port groups  │  │     Patching: VUM / LCM     │  │   Firewall: service rules   │   │
│   │     HBAs: FC/iSCSI/NVMe     │  │  Host profiles: enforce std │  │   Secure boot: TPM verify   │   │
│   │ NIC teaming: active/standby │  │  esxcli: config + diagnose  │  │  SSH/Shell: disabled by std │   │
│   │  VMkernel ports: VMk0-VMkN  │  │    esxtop: real-time perf   │  │  Syslog: to vRLI or syslog  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines the host stack · Operations maintain health · Security hardens the hypervisor │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │PSOD: check vmkern│vm-support bundle │ Host conn: green? │GSS: support bundl│  esxcli system   │   │
│   │NFS unmount: check│esxcli storage lis│ HBA: link state OK│  TAM escalation  │  esxcli network  │   │
│   │vMotion fail: VMk │  esxtop -b -n 5  │ vSAN health: green│ Log bundle + vmx │  vmkfstools -i   │   │
│   │ HA agent restart │/var/log/vmkernel │   Uptime + tasks  │P1: production dow│  vim-cmd vmsvc   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server · CPUs (Intel/AMD) · RAM DIMMs · PCIe HBAs and NICs · SAS/NVMe disks · Power & Cooling    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VMkernel      = ESXi micro-kernel OS; manages CPU scheduling, memory balloon, and device I/O         │
│  DCUI          = Direct Console User Interface; local text console on ESXi host physical screen       │
│  VMkernel port = VMk NIC; carries management, vMotion, vSAN, NFC, or replication traffic              │
│  Lockdown mode = Host setting that prevents direct access; all management via vCenter only            │
│  Host Profile  = Saved configuration template applied to hosts for consistency enforcement            │
│  PSP           = Path Selection Policy; controls multipath selection: MRU, Fixed, or RR               │
│  vDS           = vSphere Distributed Switch; cluster-level virtual switch managed by vCenter          │
│  esxcli        = ESXi CLI framework; namespaces: system, network, storage, vm, software               │
│  esxtop        = ESXi real-time performance monitor; CPU/memory/disk/network counters per VM          │
│  vmkfstools    = CLI for VMDK operations: clone, resize, inflate, import/export                       │
│  PSOD          = Purple Screen of Death; ESXi kernel panic; check vmkernel log for cause              │
│  LCM           = Lifecycle Manager; patching engine in vCenter for ESXi host baselines                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
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
