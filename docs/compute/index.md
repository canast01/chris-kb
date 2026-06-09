# Compute

<div class="kb-summary">
Compute platform knowledge base covering Windows Server, Linux, GPU workloads, and local AI (Ollama). Includes architecture references, server build standards, operational procedures, CLI commands, patching and lifecycle management, performance troubleshooting, and security hardening guides.
</div>

```text
┌────────────────────────────────────── Compute Platform Overview ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Compute Infrastructure                                    │   │
│   │         Physical and virtual x86-64 servers running Linux and Windows Server workloads        │   │
│   │           Remote access: SSH port 22 (Linux) · RDP port 3389 / WinRM 5985 (Windows)           │   │
│   │              Out-of-band: Dell iDRAC · HP iLO · IPMI — independent of the host OS             │   │
│   │        Automation: Bash/Python (Linux) · PowerShell/DSC (Windows) · Ansible across both       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Both platforms run on the same physical hardware — differentiated by OS and tooling                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Linux Server                 │  │                Windows Server               │   │
│   │   RHEL · Ubuntu · Debian · Rocky · Alpine    │  │    Server 2019 · Server 2022 · Core mode    │   │
│   │   Kernel: modules, parameters, namespaces    │  │     Hyper-V: built-in Type 1 hypervisor     │   │
│   │     systemd: service management and boot     │  │   Active Directory Domain Services (AD DS)  │   │
│   │   LVM: flexible logical volume management    │  │     NTFS · ReFS: file systems with ACLs     │   │
│   │     Package mgmt: dnf / apt / rpm / dpkg     │  │      Group Policy (GPO): central config     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Linux and Windows share hardware but differ in tooling, auth, and management patterns              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Linux Operations               │  │              Windows Operations             │   │
│   │     SSH remote access and key management     │  │       RDP and WinRM remote management       │   │
│   │     Performance: perf/sar/iostat/vmstat      │  │      Performance Monitor · Get-Counter      │   │
│   │     Security: SELinux/AppArmor · auditd      │  │     Defender AV · Audit Policies · LAPS     │   │
│   │    Logs: journalctl · rsyslog · logrotate    │  │      Event Viewer: logs and diagnostics     │   │
│   │     Automation: Bash/Python · cron jobs      │  │    PowerShell automation · Task Scheduler   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Day-to-day operations use platform-native tools and automation frameworks                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SSH        │       RDP        │       WinRM       │   iDRAC / BMC    │  SNMP / Syslog   │   │
│   │   Linux remote   │  Windows remote  │    PS remoting    │   Out-of-band    │    Monitoring    │   │
│   │   TCP port 22    │  TCP port 3389   │    TCP 5985/86    │   IPMI / REST    │   UDP 161/162    │   │
│   │ Key + cert auth  │  NLA + Kerberos  │   HTTP/S WS-Mgmt  │   DRAC web+CLI   │   MIB + traps    │   │
│   │SCP · SFTP · rsync│ mstsc.exe client │   Invoke-Command  │  Lifecycle Ctrl  │  Nagios/OpenNMS  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 rack servers · NIC teaming · FC HBAs · iDRAC / iLO BMC · Power & Cooling                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  systemd      = Linux PID 1; manages service units, timers, mounts, and boot targets                  │
│  LVM          = Logical Volume Manager; PV → VG → LV abstraction for flexible disk layout             │
│  SELinux      = Security-Enhanced Linux; mandatory access control via kernel labels                   │
│  AD DS        = Active Directory Domain Services; LDAP directory + Kerberos KDC for auth              │
│  GPO          = Group Policy Object; settings pushed to computers and users via LDAP                  │
│  Hyper-V      = Windows built-in Type 1 hypervisor; supports checkpoints and live migration           │
│  NTFS         = New Technology File System; ACLs, compression, encryption, and quotas                 │
│  WinRM        = Windows Remote Management; WS-Management for PowerShell PSRemoting                    │
│  iDRAC        = Dell Integrated Remote Access Controller; out-of-band BMC for server mgmt             │
│  LAPS         = Local Admin Password Solution; rotates local admin passwords stored in AD             │
│  auditd       = Linux audit daemon; logs syscall events for security compliance/forensics             │
│  SNMP         = Simple Network Management Protocol; polls device metrics and receives traps           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="windows-server/"><strong>Windows Server</strong><span>Architecture, standards, lifecycle, operations, CLI, scripts, troubleshooting, and security.</span></a>
<a class="kb-card" href="linux/"><strong>Linux</strong><span>Architecture, standards, lifecycle, operations, CLI, scripts, troubleshooting, and security.</span></a>
<a class="kb-card" href="local-ai/"><strong>Local AI & GPU</strong><span>Run LLMs locally with Ollama and manage GPU workloads — drivers, CUDA, sizing, and performance tuning.</span></a>
</div>
