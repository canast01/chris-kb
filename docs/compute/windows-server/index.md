# Windows Server

<div class="kb-summary">
Windows Server 2019/2022/2025 infrastructure — Active Directory DS, DNS, SMB file services, Hyper-V, WSUS patch management, and PowerShell remoting for enterprise server workloads.
</div>

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


```text
┌──────────────────────────────── Windows Server — Deployment Sequence ─────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Hardware Readiness                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  BIOS/firmware at current vendor-recommended level  ·  update from iDRAC/iLO before OS                │
│  BIOS: VT-x on  ·  VT-d on  ·  Secure Boot on (or off if driver signing issues)                       │
│  TPM 2.0 chip present and enabled (required for BitLocker and Credential Guard)                       │
│  NIC: OEM driver available for target OS version  ·  check Windows Server HCL                         │
│  DNS: A+PTR records created before install  ·  hostname resolves before domain join                   │
│                                                                                                       │
│                                        │  install OS                                                  │
│                                        ▼                                                              │
│  Step 2 · OS Installation                                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Boot from ISO  ·  select Windows Server Datacenter or Standard (Desktop or Core)                     │
│  Custom install  ·  create partitions: 100 MB EFI + 128 MB MSR + OS partition                         │
│  Set local admin password  ·  activate Windows (KMS or MAK key) post-install                          │
│  Windows Update: install all updates before domain join and role deployment                           │
│  Configure hostname: Rename-Computer -NewName <hostname>  ·  reboot to apply                          │
│                                                                                                       │
│                                        │  configure network and domain                                │
│                                        ▼                                                              │
│  Step 3 · Network & Domain Join                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Set static IP: New-NetIPAddress  ·  set DNS to domain controller IPs                                 │
│  Test name resolution: Resolve-DnsName <domain>  ·  Resolve-DnsName <dc-fqdn>                         │
│  Domain join: Add-Computer -DomainName <domain> -Credential <admin>  ·  reboot                        │
│  Verify Kerberos: klist  ·  verify GPO applies: gpresult /r                                           │
│  NIC teaming if redundancy needed: New-NetLbfoTeam  ·  set LACP or switch-independent                 │
│                                                                                                       │
│                                        │  install roles and features                                  │
│                                        ▼                                                              │
│  Step 4 · Roles & Features                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  AD DS: Install-WindowsFeature AD-Domain-Services -IncludeManagementTools                             │
│  Hyper-V: Install-WindowsFeature Hyper-V -IncludeManagementTools  ·  requires reboot                  │
│  File Services: Install-WindowsFeature FS-FileServer FS-DFS-Namespace FS-DFS-Replication              │
│  IIS: Install-WindowsFeature Web-Server -IncludeAllSubFeature                                         │
│  Configure role-specific settings after feature install  ·  verify service started                    │
│                                                                                                       │
│                                        │  apply security baseline                                     │
│                                        ▼                                                              │
│  Step 5 · Security Hardening                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Apply CIS or STIG GPO baseline  ·  audit policy: success and failure on logon/logoff                 │
│  Enable Windows Defender  ·  configure exclusions for installed roles only                            │
│  Disable unused services: Print Spooler, WinRM (if not needed), NetBIOS over TCP/IP                   │
│  LAPS: verify local admin password managed  ·  check LAPS GUI or AD attribute                         │
│  Enable BitLocker on OS drive (servers with TPM)  ·  store recovery key in AD                         │
│                                                                                                       │
│                                        │  configure monitoring and backup                             │
│                                        ▼                                                              │
│  Step 6 · Monitoring & Backup                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  WSUS: configure Automatic Updates Group Policy  ·  point to WSUS server                              │
│  Windows Admin Center: deploy WAC gateway  ·  add server to managed list                              │
│  Deploy monitoring agent: Aria Ops  ·  SCOM  ·  or log analytics agent                                │
│  Configure Windows event forwarding (WEF) to central log collector or SIEM                            │
│  Backup: configure Windows Server Backup  ·  or deploy Veeam/Commvault agent                          │
│  Test restore  ·  document recovery procedure  ·  confirm alerts reach on-call                        │
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
