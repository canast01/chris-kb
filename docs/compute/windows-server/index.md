# Windows Server

<div class="kb-summary">
Windows Server 2019/2022/2025 infrastructure — Active Directory DS, DNS, SMB file services, Hyper-V, WSUS patch management, and PowerShell remoting for enterprise server workloads.
</div>

```
┌──────────────────────────────────────── Windows Server Stack ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Windows Server Administration                                 │   │
│   │       Server Manager · PowerShell · Windows Admin Center · Event Viewer · Task Scheduler      │   │
│   │           Remote management: RDP (3389) · WinRM (5985/5986) · PowerShell PSRemoting           │   │
│   │          Monitoring: Performance Monitor · Get-Counter · Resource Monitor · Defender          │   │
│   │          Automation: PowerShell DSC · Scheduled Tasks · Group Policy · Ansible WinRM          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Administration tools span OS architecture, networking, and Active Directory                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Networking         │  │       Active Directory      │   │
│   │      Server 2019 / 2022     │  │    DNS Server: zone mgmt    │  │    AD DS: domain services   │   │
│   │   NTFS · ReFS filesystems   │  │   DHCP Server: IP leasing   │  │      Group Policy (GPO)     │   │
│   │  Registry: config database  │  │   NIC Teaming: LACP bonds   │  │    Kerberos: auth tickets   │   │
│   │   Services: Win32 daemons   │  │    Windows Firewall + WDF   │  │   LDAP: directory queries   │   │
│   │  Hyper-V: Type 1 hypervisor │  │   DFS-N: namespace sharing  │  │  Trusts: cross-domain auth  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    OS architecture, networking, and Active Directory form the Windows platform foundation             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Operations         │  │           Security          │  │       Troubleshooting       │   │
│   │    WSUS: patch management   │  │   BitLocker: drive encrypt  │  │  Event Viewer: logs+alerts  │   │
│   │   WinRM: remote execution   │  │      Defender AV + EDR      │  │  SFC / DISM: system repair  │   │
│   │     IIS: web server mgmt    │  │    JEA: Just Enough Admin   │  │     WinPE: recovery env.    │   │
│   │     Volume Shadow Copies    │  │   Audit Policy: event log   │  │   Process Monitor/Explorer  │   │
│   │    FSRM: quota+screening    │  │    LAPS: local admin pwds   │  │   WMI/CIM: system queries   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Operations, security hardening, and diagnostic tools work across all Windows roles                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       RDP        │       SMB        │       WinRM       │     Kerberos     │   LDAP / LDAPS   │   │
│   │  Remote desktop  │   File sharing   │    PS remoting    │  Authentication  │    Directory     │   │
│   │     TCP 3389     │     TCP 445      │    TCP 5985/86    │    TCP 88/UDP    │   TCP 389/636    │   │
│   │  NLA · TLS 1.2   │  NTLM/Kerberos   │    HTTP · HTTPS   │  KDC ticket srv  │  SSL+SASL bind   │   │
│   │    mstsc.exe     │  net use / UNC   │   Invoke-Command  │   Ticket + PAC   │ ADSI/RSAT tools  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 rack servers · NIC teaming · iDRAC/iLO BMC · Windows licensing · Power & Cooling              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AD DS    = Active Directory Domain Services; LDAP directory + Kerberos KDC for Windows auth          │
│  GPO      = Group Policy Object; settings pushed to computers and users via LDAP queries              │
│  WinRM    = Windows Remote Management; WS-Management for PowerShell PSRemoting                        │
│  Kerberos = Ticket-based authentication protocol; default for all AD domain accounts                  │
│  NTFS     = New Technology File System; supports ACLs, compression, and EFS encryption                │
│  Hyper-V  = Windows Type 1 hypervisor; VM checkpoints and live migration built in                     │
│  BitLocker= Full-volume encryption using AES; TPM-backed key storage for boot protection              │
│  LAPS     = Local Admin Password Solution; rotates local admin passwords stored in AD                 │
│  JEA      = Just Enough Administration; limits PS remoting to specific command sets                   │
│  WSUS     = Windows Server Update Services; internal patch distribution server                        │
│  SFC      = System File Checker; scans and repairs corrupt Windows system files                       │
│  DISM     = Deployment Image Servicing; manages Windows images and component packages                 │
│  DFS-N    = Distributed File System Namespace; virtual UNC namespace across share paths               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── Windows Server Stack ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Windows Server Administration                                 │   │
│   │       Server Manager · PowerShell · Windows Admin Center · Event Viewer · Task Scheduler      │   │
│   │           Remote management: RDP (3389) · WinRM (5985/5986) · PowerShell PSRemoting           │   │
│   │          Monitoring: Performance Monitor · Get-Counter · Resource Monitor · Defender          │   │
│   │          Automation: PowerShell DSC · Scheduled Tasks · Group Policy · Ansible WinRM          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Administration tools span OS architecture, networking, and Active Directory                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Networking         │  │       Active Directory      │   │
│   │      Server 2019 / 2022     │  │    DNS Server: zone mgmt    │  │    AD DS: domain services   │   │
│   │   NTFS · ReFS filesystems   │  │   DHCP Server: IP leasing   │  │      Group Policy (GPO)     │   │
│   │  Registry: config database  │  │   NIC Teaming: LACP bonds   │  │    Kerberos: auth tickets   │   │
│   │   Services: Win32 daemons   │  │    Windows Firewall + WDF   │  │   LDAP: directory queries   │   │
│   │  Hyper-V: Type 1 hypervisor │  │   DFS-N: namespace sharing  │  │  Trusts: cross-domain auth  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    OS architecture, networking, and Active Directory form the Windows platform foundation             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Operations         │  │           Security          │  │       Troubleshooting       │   │
│   │    WSUS: patch management   │  │   BitLocker: drive encrypt  │  │  Event Viewer: logs+alerts  │   │
│   │   WinRM: remote execution   │  │      Defender AV + EDR      │  │  SFC / DISM: system repair  │   │
│   │     IIS: web server mgmt    │  │    JEA: Just Enough Admin   │  │     WinPE: recovery env.    │   │
│   │     Volume Shadow Copies    │  │   Audit Policy: event log   │  │   Process Monitor/Explorer  │   │
│   │    FSRM: quota+screening    │  │    LAPS: local admin pwds   │  │   WMI/CIM: system queries   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Operations, security hardening, and diagnostic tools work across all Windows roles                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       RDP        │       SMB        │       WinRM       │     Kerberos     │   LDAP / LDAPS   │   │
│   │  Remote desktop  │   File sharing   │    PS remoting    │  Authentication  │    Directory     │   │
│   │     TCP 3389     │     TCP 445      │    TCP 5985/86    │    TCP 88/UDP    │   TCP 389/636    │   │
│   │  NLA · TLS 1.2   │  NTLM/Kerberos   │    HTTP · HTTPS   │  KDC ticket srv  │  SSL+SASL bind   │   │
│   │    mstsc.exe     │  net use / UNC   │   Invoke-Command  │   Ticket + PAC   │ ADSI/RSAT tools  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 rack servers · NIC teaming · iDRAC/iLO BMC · Windows licensing · Power & Cooling              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AD DS    = Active Directory Domain Services; LDAP directory + Kerberos KDC for Windows auth          │
│  GPO      = Group Policy Object; settings pushed to computers and users via LDAP queries              │
│  WinRM    = Windows Remote Management; WS-Management for PowerShell PSRemoting                        │
│  Kerberos = Ticket-based authentication protocol; default for all AD domain accounts                  │
│  NTFS     = New Technology File System; supports ACLs, compression, and EFS encryption                │
│  Hyper-V  = Windows Type 1 hypervisor; VM checkpoints and live migration built in                     │
│  BitLocker= Full-volume encryption using AES; TPM-backed key storage for boot protection              │
│  LAPS     = Local Admin Password Solution; rotates local admin passwords stored in AD                 │
│  JEA      = Just Enough Administration; limits PS remoting to specific command sets                   │
│  WSUS     = Windows Server Update Services; internal patch distribution server                        │
│  SFC      = System File Checker; scans and repairs corrupt Windows system files                       │
│  DISM     = Deployment Image Servicing; manages Windows images and component packages                 │
│  DFS-N    = Distributed File System Namespace; virtual UNC namespace across share paths               │
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
