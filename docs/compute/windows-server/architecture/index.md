---
tags:
  - architecture
  - windows
---
# Windows Server — Architecture

<div class="kb-summary">
Windows Server 2019/2022/2025 infrastructure — Active Directory DS, DNS, SMB file services, Hyper-V, WSUS, and PowerShell-based management. Available in Standard and Datacenter editions with Server Core (recommended) or Desktop Experience installation.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌─────────────────────────── Windows Server — Platform Architecture Overview ───────────────────────────┐
│                                                                                                       │
│  Microsoft server OS; roles and features architecture; AD DS for identity;                            │
│  Group Policy for management; Hyper-V for virtualisation; WinRM for remote ops.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Core Roles                  │  │               Management Layer              │   │
│   │            AD DS: domain identity            │  │              Group Policy: GPO              │   │
│   │             DNS: name resolution             │  │           WinRM: remote PowerShell          │   │
│   │           DHCP: IP address service           │  │           Server Manager: local UI          │   │
│   │          File Services: SMB shares           │  │            WSUS: patch management           │   │
│   │           Hyper-V: virtualisation            │  │           SCCM/Intune: config mgmt          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Roles are modular; install only what is needed; each role has its own services.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Storage and Networking            │  │             Security Components             │   │
│   │           NTFS: primary filesystem           │  │           Windows Defender: AV/EDR          │   │
│   │          ReFS: resilient filesystem          │  │          Windows Firewall: host FW          │   │
│   │         iSCSI initiator: SAN attach          │  │          BitLocker: disk encryption         │   │
│   │          Failover Clustering: WSFC           │  │           Kerberos: auth protocol           │   │
│   │            SMB 3.0: file sharing             │  │           TLS 1.3: wire encryption          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers; TPM 2.0 required for BitLocker; BIOS/UEFI; NIC team for HA;                          │
│  iDRAC/iLO OOB management; Windows Server requires CAL for each connecting user.                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AD DS          = Active Directory Domain Services; user and computer identity                        │
│  Group Policy   = GPO; domain-wide config pushed to computers and users                               │
│  WinRM          = Windows Remote Management; PowerShell remote sessions                               │
│  Hyper-V        = Windows hypervisor; type-1; VMs run as partitions                                   │
│  WSFC           = Windows Server Failover Cluster; SQL Always On, Hyper-V HA                          │
│  NTFS           = NT File System; permissions, journaling, compression                                │
│  ReFS           = Resilient File System; checksums, no repair needed; Storage Spaces                  │
│  SMB 3.0        = Server Message Block; Windows file sharing protocol                                 │
│  BitLocker      = Microsoft full-disk encryption; requires TPM 2.0                                    │
│  Kerberos       = AD authentication protocol; ticket-based; default in domain                         │
│  WSUS           = Windows Server Update Services; internal patch distribution                         │
│  CAL            = Client Access License; required per user/device connecting                          │
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

