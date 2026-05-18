# Virtualization

<div class="kb-summary">
Virtualization platform knowledge base covering VMware. Includes architecture references, operational procedures, CLI commands, health checks, lifecycle management, and troubleshooting guides.
</div>

```
VMware Platform Stack
═══════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────┐
  │                   VCF (VMware Cloud Foundation)      │
  │         Lifecycle Management · SDDC Manager         │
  └──────────────────────────┬──────────────────────────┘
                             │ orchestrates
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
  ┌─────────────┐   ┌─────────────────┐   ┌───────────┐
  │   vCenter   │   │      NSX-T      │   │  VxRail   │
  │             │   │ Software-Defined│   │ HCI Node  │
  │ Inventory   │   │   Networking    │   │ Manager   │
  │ HA · DRS    │   │ Firewall · LB   │   └───────────┘
  └──────┬──────┘   └────────┬────────┘
         │                   │
         ▼                   ▼
  ┌─────────────────────────────────────────────────────┐
  │                   ESXi Hosts                        │
  │     Compute · Hypervisor · VMkernel                 │
  │  vmk0(mgmt) · vmk1(vMotion) · vmk2(vSAN) · vmk3   │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │                     vSAN                            │
  │        Distributed Storage · Policy-Driven          │
  │   RAID-1/5/6 · Dedup · Compression · Encryption    │
  └─────────────────────────────────────────────────────┘

  Management Plane:  vCenter → NSX → Aria Ops → Aria Logs
  Data Plane:        ESXi hypervisor → vSAN storage fabric
  Control Plane:     SDDC Manager (VCF) lifecycle control
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="vmware/"><strong>VMware Platform</strong><span>vCenter, ESXi, vSAN, NSX, VCF, VxRail, Aria Suite, Horizon, SRM, and vSphere Replication.</span></a>
</div>
