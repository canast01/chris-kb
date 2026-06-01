# Windows Server — Architecture

<div class="kb-summary">
Windows Server 2019/2022/2025 infrastructure — Active Directory DS, DNS, SMB file services, Hyper-V, WSUS, and PowerShell-based management. Available in Standard and Datacenter editions with Server Core (recommended) or Desktop Experience installation.
</div>

```
┌──────────────────────────────────── Windows Server — Architecture ────────────────────────────────────┐
│                                                                                                       │
│  Windows Server architecture: kernel, services, Active Directory, and Hyper-V integration.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               OS Architecture                │  │               Active Directory              │   │
│   │         NT kernel: HAL + kernel mode         │  │          Forest → Domain → OU tree          │   │
│   │          Win32 subsystem: user mode          │  │          DC: LDAP + Kerberos + DNS          │   │
│   │            Services: SCM-managed             │  │       SYSVOL: GPO + script replication      │   │
│   │            Registry: config store            │  │           Trust: cross-domain auth          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    OS layer provides platform; AD provides identity; Hyper-V provides virtualisation                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Hyper-V Architecture             │  │                  Networking                 │   │
│   │         Parent partition: management         │  │      Virtual switch: external/int/priv      │   │
│   │          Child partition: VM guest           │  │           NIC teaming: LBFO / SET           │   │
│   │           VMBus: hypercall channel           │  │         SMB Direct: RDMA file access        │   │
│   │             Synthetic NIC / SCSI             │  │         Windows Firewall + GPO rules        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical server · CPU virtualization extensions · NIC · storage SAN/NAS                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HAL          = Hardware Abstraction Layer; isolates kernel from hardware                             │
│  SCM          = Service Control Manager; manages Windows service lifecycle                            │
│  Registry     = hierarchical configuration database; HKLM and HKCU hives                              │
│  SYSVOL       = shared folder replicated to all DCs; holds GPOs and scripts                           │
│  Trust        = cross-domain auth relationship; one-way or two-way                                    │
│  VMBus        = high-speed communication channel between parent and child partitions                  │
│  Synthetic NIC= Hyper-V virtual NIC using VMBus; requires integration services                        │
│  NIC teaming  = LBFO or Switch Embedded Teaming (SET); redundancy + bandwidth                         │
│  SMB Direct   = SMB over RDMA; high-throughput low-latency file access                                │
│  Parent partition= Hyper-V management OS; has direct hardware access                                  │
│  Child partition= VM guest; hardware access via VMBus and VSP/VSC model                               │
│  RDMA         = Remote Direct Memory Access; bypasses OS for low-latency IO                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Windows Server Architecture](../../../assets/windows-server-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">How It Works</div>
    <div class="kb-card-desc">Edition and installation types, key server roles, critical services, common ports, event log channels, and PowerShell reference.</div>
  </a>
  <a class="kb-card" href="integrations/">
    <div class="kb-card-icon">🔗</div>
    <div class="kb-card-title">Integrations</div>
    <div class="kb-card-desc">Active Directory, Group Policy, SAN/SMB storage connectivity, Hyper-V, and monitoring via WMI/WinRM.</div>
  </a>
  <a class="kb-card" href="design-standards/">
    <div class="kb-card-icon">📐</div>
    <div class="kb-card-title">Design Standards</div>
    <div class="kb-card-desc">Edition selection criteria, Server Core baseline, patch management policy, and firewall rule standards.</div>
  </a>
</div>

## Editions

| Version | Edition | Key Differentiator |
|---|---|---|
| Windows Server 2019/2022/2025 | Standard | Up to 2 Hyper-V VMs per licence |
| Windows Server 2019/2022/2025 | Datacenter | Unlimited Hyper-V VMs; Storage Spaces Direct, SDN |
| All | Server Core | No GUI; smaller attack surface; recommended for production |
| All | Desktop Experience | Full GUI; required for some legacy management tools |

## Topology


