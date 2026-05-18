# ESXi

<div class="kb-summary">
Technical and operational reference for VMware ESXi. Covers host architecture, networking, storage paths, patching, security hardening, and troubleshooting for ESXi hosts managed by vCenter.
</div>

```
ESXi Host — Component Overview
┌─────────────────────────────────────────────────────────┐
│  VMkernel (ESXi Hypervisor)                             │
│  ├── CPU Scheduler (NUMA-aware, vCPU scheduling)        │
│  ├── Memory Manager (TPS, balloon, swap hierarchy)      │
│  ├── Storage Stack (NMP, PSP, SATP, VAAI)              │
│  └── Network Stack (vSwitch / vDS, port groups)         │
│                                                         │
│  Management Agents                                      │
│  ├── hostd    ← vSphere API, VM operations              │
│  ├── vpxa     ← vCenter agent (cluster management)      │
│  └── fdm      ← vSphere HA (Fault Domain Manager)       │
│                                                         │
│  Virtual Machines                                       │
│  ├── VM1 (vmx + vCPU + vRAM + vmdk)                   │
│  ├── VM2                                                │
│  └── VM3                                                │
└────────────────┬──────────────┬────────────────────────┘
                 │              │
     ┌───────────▼────┐  ┌──────▼──────────────┐
     │  Storage       │  │  Network             │
     │  FC / iSCSI    │  │  vmnic0 · vmnic1     │
     │  NVMe / NFS    │  │  vmnic2 · vmnic3     │
     │  VMFS / vSAN   │  │  vmk0  vmk1  vmk2   │
     └────────────────┘  └─────────────────────┘
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
