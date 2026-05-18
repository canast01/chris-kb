# Windows Server

<div class="kb-summary">
Windows Server 2019/2022/2025 infrastructure — Active Directory DS, DNS, SMB file services, Hyper-V, WSUS patch management, and PowerShell remoting for enterprise server workloads.
</div>

```
┌──────────────────────────────────────────────────────────┐
│                 Windows Server Stack                     │
├────────────────┬─────────────┬────────────┬─────────────┤
│  AD DS / DNS   │  DHCP       │  IIS       │  Hyper-V     │
│  (DC role)     │             │  (web)     │  (VMs)       │
├────────────────┴─────────────┴────────────┴─────────────┤
│          SMB / File Services  │  WinRM / PowerShell      │
├──────────────────────────────────────────────────────────┤
│                  Windows Server Core                     │
│   Services (SCM)  │  Event Log  │  Registry              │
│   WMI / CIM       │  Task Scheduler                      │
├──────────────────────────────────────────────────────────┤
│  Management: RSAT │ WSUS │ Windows Admin Center          │
├────────────────────────────┬─────────────────────────────┤
│  Storage: NTFS / ReFS      │  Network: NIC Team/VLAN     │
│  iSCSI / SMB shares        │  Windows Firewall           │
└────────────────────────────┴─────────────────────────────┘
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
