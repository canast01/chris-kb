# Windows Server

<div class="kb-summary">
Windows Server 2019/2022/2025 infrastructure — Active Directory DS, DNS, SMB file services, Hyper-V, WSUS patch management, and PowerShell remoting for enterprise server workloads.
</div>

```
┌────────────────────────────────────── Windows Server — Overview ──────────────────────────────────────┐
│                                                                                                       │
│  Windows Server provides enterprise OS, Active Directory, Hyper-V, and file services.                 │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Core Roles         │  │           Editions          │  │          Management         │   │
│   │    AD DS: domain services   │  │    Standard: 2 VM guests    │  │      Server Manager UI      │   │
│   │       DNS / DHCP / NPS      │  │  Datacenter: unlimited VMs  │  │     Windows Admin Centre    │   │
│   │   Hyper-V: virtualisation   │  │    Core: no GUI, minimal    │  │      PowerShell + WinRM     │   │
│   │      IIS / File / Print     │  │   Essentials: SMB 25 users  │  │      Group Policy (GPO)     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · CPU · RAM · NIC · NTFS/ReFS storage                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AD DS        = Active Directory Domain Services; central identity and policy store                   │
│  Hyper-V      = Microsoft hypervisor built into Windows Server; type-1                                │
│  WinRM        = Windows Remote Management; PS remoting and remote admin                               │
│  GPO          = Group Policy Object; policy applied to OUs in AD                                      │
│  Server Core  = minimal install without GUI; managed remotely via PS/WAC                              │
│  Windows Admin Centre= browser-based GUI for managing servers and clusters                            │
│  NPS          = Network Policy Server; RADIUS for 802.1X / VPN auth                                   │
│  ReFS         = Resilient File System; alternative to NTFS; integrity streams                         │
│  IIS          = Internet Information Services; web/app server role                                    │
│  NTFS         = New Technology File System; default FS with ACLs + journaling                         │
│  SMB          = Server Message Block; file sharing protocol; 3.x on Server 2016+                      │
│  CAL          = Client Access Licence; required per user or device connecting                         │
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
