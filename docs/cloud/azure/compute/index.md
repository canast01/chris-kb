# Azure Compute

<div class="kb-summary">
Azure Compute articles, operational checks, troubleshooting notes, and references.
</div>

```
┌─────────────────────────────────────── Azure Compute Overview ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Azure Compute — Virtual Machines, Scale Sets, Availability, and Fleet Management       │   │
│   │   Virtual Machines: Windows and Linux VMs; 800+ sizes; Availability Zones for HA deployment   │   │
│   │VM Scale Sets: auto-scaling fleet; uniform or flexible orchestration; custom or platform images│   │
│   │    Availability: Zones (physically isolated) and Sets (fault/update domains) for redundancy   │   │
│   │  Fleet ops: Azure Update Manager (patching) · Extensions (monitoring, DSC) · Boot diagnostics │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VMs provide compute · Scale Sets enable elasticity · Availability features ensure HA deployments   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Virtual Machines      │  │         Availability        │  │       Fleet Management      │   │
│   │   Sizes: B/D/E/F families   │  │    Availability Zones: 3    │  │    Update Manager: patch    │   │
│   │   OS disk: managed Premium  │  │   Availability Sets: FD/UD  │  │   Extensions: agent+script  │   │
│   │    Image: custom gallery    │  │     VM Scale Sets: VMSS     │  │   Boot diagnostics: serial  │   │
│   │  Identity: managed identity │  │    Zone: PPG for low lat    │  │     Serial console: OOB     │   │
│   │  Resize: without data loss  │  │    VMSS: instance refresh   │  │  Inventory: ASC + Defender  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    VMs provide individual compute · Availability features distribute load                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Virtual Machines │   Avail. Sets    │    Avail. Zones   │    Scale Sets    │     Patching     │   │
│   │  Start/stop VM   │  FD: 2-3 racks   │     Zone 1/2/3    │  Min/max count   │  Update Manager  │   │
│   │  Resize: portal  │   UD: rolling    │    Zone balance   │ Scale rule: CPU  │  Patch schedule  │   │
│   │  Image: capture  │   Use: SAP/SQL   │   Use: web tier   │ Rolling upgrade  │    Compliance    │   │
│   │  Boot diag: log  │   SLA: 99.95%    │    SLA: 99.99%    │ Instance refresh │  Reboot: sched   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure host servers · Availability Zones (physical DCs) · Managed Disk storage fabric                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Availability Set  = Groups VMs across fault domains (rack) and update domains (patch group)          │
│  Availability Zone = Physically separate DC in a region; each with independent power, cooling, network│
│  VM Scale Set      = VMSS; fleet of identical VMs with auto-scaling; uniform or flexible orchestration│
│  Managed Identity  = Auto-managed service principal for a VM; used to authenticate to Azure services  │
│  Proximity Placement Group= PPG; co-locates VMs in same data centre for lowest latency between VMs    │
│  Fault Domain      = Rack-level isolation in an Availability Set; typically 2 or 3 per set            │
│  Update Domain     = Rolling maintenance group; Azure updates one UD at a time during planned         │
│  Boot Diagnostics  = Captures VM serial console log and screenshot; diagnoses non-booting VMs         │
│  Serial Console    = Out-of-band console access to VM; works when SSH/RDP unreachable                 │
│  Azure Update Manager= Replaces Azure Automation Update Management; patches VMs on schedule at scale  │
│  VM Extension      = Agent-based add-ons; installs monitoring agents, DSC, custom scripts on VMs      │
│  Shared Image Gallery= Azure Compute Gallery; stores versioned custom VM images shared across         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────── Azure Compute Overview ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Azure Compute — Virtual Machines, Scale Sets, Availability, and Fleet Management       │   │
│   │   Virtual Machines: Windows and Linux VMs; 800+ sizes; Availability Zones for HA deployment   │   │
│   │VM Scale Sets: auto-scaling fleet; uniform or flexible orchestration; custom or platform images│   │
│   │    Availability: Zones (physically isolated) and Sets (fault/update domains) for redundancy   │   │
│   │  Fleet ops: Azure Update Manager (patching) · Extensions (monitoring, DSC) · Boot diagnostics │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VMs provide compute · Scale Sets enable elasticity · Availability features ensure HA deployments   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Virtual Machines      │  │         Availability        │  │       Fleet Management      │   │
│   │   Sizes: B/D/E/F families   │  │    Availability Zones: 3    │  │    Update Manager: patch    │   │
│   │   OS disk: managed Premium  │  │   Availability Sets: FD/UD  │  │   Extensions: agent+script  │   │
│   │    Image: custom gallery    │  │     VM Scale Sets: VMSS     │  │   Boot diagnostics: serial  │   │
│   │  Identity: managed identity │  │    Zone: PPG for low lat    │  │     Serial console: OOB     │   │
│   │  Resize: without data loss  │  │    VMSS: instance refresh   │  │  Inventory: ASC + Defender  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    VMs provide individual compute · Availability features distribute load                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Virtual Machines │   Avail. Sets    │    Avail. Zones   │    Scale Sets    │     Patching     │   │
│   │  Start/stop VM   │  FD: 2-3 racks   │     Zone 1/2/3    │  Min/max count   │  Update Manager  │   │
│   │  Resize: portal  │   UD: rolling    │    Zone balance   │ Scale rule: CPU  │  Patch schedule  │   │
│   │  Image: capture  │   Use: SAP/SQL   │   Use: web tier   │ Rolling upgrade  │    Compliance    │   │
│   │  Boot diag: log  │   SLA: 99.95%    │    SLA: 99.99%    │ Instance refresh │  Reboot: sched   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure host servers · Availability Zones (physical DCs) · Managed Disk storage fabric                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Availability Set  = Groups VMs across fault domains (rack) and update domains (patch group)          │
│  Availability Zone = Physically separate DC in a region; each with independent power, cooling, network│
│  VM Scale Set      = VMSS; fleet of identical VMs with auto-scaling; uniform or flexible orchestration│
│  Managed Identity  = Auto-managed service principal for a VM; used to authenticate to Azure services  │
│  Proximity Placement Group= PPG; co-locates VMs in same data centre for lowest latency between VMs    │
│  Fault Domain      = Rack-level isolation in an Availability Set; typically 2 or 3 per set            │
│  Update Domain     = Rolling maintenance group; Azure updates one UD at a time during planned         │
│  Boot Diagnostics  = Captures VM serial console log and screenshot; diagnoses non-booting VMs         │
│  Serial Console    = Out-of-band console access to VM; works when SSH/RDP unreachable                 │
│  Azure Update Manager= Replaces Azure Automation Update Management; patches VMs on schedule at scale  │
│  VM Extension      = Agent-based add-ons; installs monitoring agents, DSC, custom scripts on VMs      │
│  Shared Image Gallery= Azure Compute Gallery; stores versioned custom VM images shared across         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="availability-sets/">
  <strong>Availability Sets</strong>
  <span>Fault domain and update domain grouping to protect VMs from planned and unplanned downtime.</span>
</a>

<a class="kb-card" href="availability-zones/">
  <strong>Availability Zones</strong>
  <span>Physically separate datacenter zones within an Azure region for high-availability deployments.</span>
</a>

<a class="kb-card" href="boot-diagnostics/">
  <strong>Boot Diagnostics</strong>
  <span>Screenshot and serial log capture for diagnosing VMs that won't boot or are unresponsive.</span>
</a>

<a class="kb-card" href="extensions/">
  <strong>Extensions</strong>
  <span>VM agent extensions for monitoring, antimalware, DSC, custom scripts, and diagnostics.</span>
</a>

<a class="kb-card" href="images/">
  <strong>Images</strong>
  <span>Custom and marketplace VM images, shared image gallery, and image lifecycle management.</span>
</a>

<a class="kb-card" href="patching/">
  <strong>Patching</strong>
  <span>Azure Update Manager and maintenance configurations for OS patch scheduling and compliance.</span>
</a>

<a class="kb-card" href="serial-console/">
  <strong>Serial Console</strong>
  <span>Out-of-band text console access to VMs and VMSS without needing network connectivity.</span>
</a>

<a class="kb-card" href="virtual-machines/">
  <strong>Virtual Machines</strong>
  <span>VM lifecycle management, sizing, availability, monitoring, and operational runbooks.</span>
</a>

<a class="kb-card" href="vm-scale-sets/">
  <strong>VM Scale Sets</strong>
  <span>Auto-scaling VM groups with uniform or flexible orchestration for stateless workloads.</span>
</a>
</div>
