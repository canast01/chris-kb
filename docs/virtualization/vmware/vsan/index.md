# vSAN

<div class="kb-summary">
Technical and operational reference for VMware vSAN. Covers storage policies, disk groups, capacity management, resync operations, health monitoring, and troubleshooting for software-defined storage in vSphere clusters.
</div>

```
vSAN CLUSTER (3-node example, FTT=1 RAID-1)

  vCenter Server
       │  (management plane — policy, health, lifecycle)
       │
  ┌────┴────────────────────────────────────────────────┐
  │                vSAN VMkernel Network                 │
  │                  (dedicated 10/25 GbE)               │
  └────┬──────────────────┬───────────────────┬─────────┘
       │                  │                   │
  ┌────┴───────┐    ┌──────┴──────┐    ┌──────┴──────┐
  │  ESXi-01   │    │  ESXi-02    │    │  ESXi-03    │
  │            │    │             │    │             │
  │ Disk Group │    │ Disk Group  │    │ Disk Group  │
  │ ┌────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │
  │ │Cache   │ │    │ │Cache    │ │    │ │Cache    │ │
  │ │SSD/NVMe│ │    │ │SSD/NVMe │ │    │ │SSD/NVMe │ │
  │ ├────────┤ │    │ ├─────────┤ │    │ ├─────────┤ │
  │ │Cap ×3  │ │    │ │Cap ×3   │ │    │ │Cap ×3   │ │
  │ └────────┘ │    │ └─────────┘ │    │ └─────────┘ │
  └────────────┘    └─────────────┘    └─────────────┘
       │                  │                   │
       └──────────────────┴───────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │    vSAN Datastore     │
              │  (single namespace    │
              │   visible to vCenter) │
              │                       │
              │  VM VMDK Object       │
              │  ├── Component A →    │
              │  │   ESXi-01          │
              │  ├── Component B →    │
              │  │   ESXi-02 (mirror) │
              │  └── Witness →        │
              │      ESXi-03          │
              └───────────────────────┘
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
