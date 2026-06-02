# Windows Server — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Editions and Installation Types, Role Topology.
</div>

## Overview

Windows Server delivers infrastructure services through **Roles** (major functions) and **Features** (supporting components) installed on top of the base OS. The current supported versions are 2019, 2022, and 2025, available in Standard and Datacenter editions. All server administration uses PowerShell, WinRM remoting, or RSAT tools. Server Core (no GUI) is the recommended installation type for security and performance.

## Editions and Installation Types

| Version | Edition | Notes |
|---|---|---|
| Windows Server 2019/2022/2025 | Standard | Up to 2 Hyper-V VMs per licence |
| Windows Server 2019/2022/2025 | Datacenter | Unlimited Hyper-V VMs; Storage Spaces Direct, SDN |
| All | Server Core | No GUI; PowerShell remoting / RSAT; smaller attack surface |
| All | Desktop Experience | Full GUI; larger footprint; required for some legacy tools |

## Role Topology

```mermaid
graph TB
  WS["Windows Server 2019 / 2022"]
  WS --> AD["Active Directory DS\n(DC role)"]
  WS --> DNS_R["DNS Server"]
  WS --> FS["File Server\nSMB · DFS"]
  WS --> IIS["IIS / App Roles"]
  WS --> WSUS["Windows Update\nWSUS / Azure Update Manager"]
  WS --> SEC["Windows Defender\nFirewall · Audit Policy"]
  ADMIN(["Windows Admin"]) -->|"RDP / PowerShell"| WS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class WS ctrl
  class AD,DNS_R,FS,IIS,WSUS,SEC mgmt
  class ADMIN host
```
```
┌──────────────────────────────────── Windows Server — How It Works ────────────────────────────────────┐
│                                                                                                       │
│  Windows Server boot process, service management, and AD authentication flow.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Boot Sequence                 │  │              Kerberos Auth Flow             │   │
│   │             UEFI/BIOS → bootmgr              │  │           User → AS request → TGT           │   │
│   │          winload.exe → kernel load           │  │          TGT → TGS request → ticket         │   │
│   │         Kernel init → HAL → drivers          │  │          Service ticket → resource          │   │
│   │          Session 0: services start           │  │          PAC: user groups in ticket         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Boot completes before user logon; Kerberos tickets cached for session                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Group Policy Processing            │  │            File System Operations           │   │
│   │            Machine GPO at startup            │  │          NTFS: journalled metadata          │   │
│   │              User GPO at logon               │  │          Shadow Copy: VSS snapshots         │   │
│   │           gpupdate /force: reapply           │  │          DFS: distributed namespace         │   │
│   │        Loopback: machine applies user        │  │          BranchCache: WAN optimise          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical server · Domain Controllers · NTP source · storage                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  bootmgr      = Windows Boot Manager; reads BCD store to select OS                                    │
│  winload.exe  = OS loader; loads kernel, HAL, and boot drivers                                        │
│  Session 0    = isolated service session; no interactive user access                                  │
│  TGT          = Ticket Granting Ticket; obtained from KDC at logon                                    │
│  TGS          = Ticket Granting Service; issues service-specific tickets                              │
│  PAC          = Privilege Attribute Certificate; encodes group memberships                            │
│  GPO          = Group Policy Object; settings applied at OU/domain level                              │
│  Loopback     = GPO mode applying machine-linked user policy at logon                                 │
│  VSS          = Volume Shadow Copy Service; creates consistent snapshots                              │
│  DFS          = Distributed File System; namespace + replication for shares                           │
│  BranchCache  = caches remote content at branch office; reduces WAN traffic                           │
│  gpupdate     = triggers immediate GP refresh; /force reapplies all settings                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
