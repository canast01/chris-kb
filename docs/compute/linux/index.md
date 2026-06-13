---
tags:
  - linux
---
# Linux Server

<div class="kb-summary">
Linux server infrastructure running RHEL and Ubuntu — systemd service management, LVM2 storage, LACP bonded networking, SELinux/AppArmor security, and Ansible-driven automation for enterprise workloads.
</div>

```text
┌────────────────────────────────────── Linux — Platform Overview ──────────────────────────────────────┐
│                                                                                                       │
│  Linux is the primary OS for compute workloads: servers, containers, and automation.                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      Kernel + userspace     │  │       Day-2 procedures      │  │        Access control       │   │
│   │       Distro selection      │  │       Backup & restore      │  │        Authentication       │   │
│   │      Integration model      │  │        Health checks        │  │          Encryption         │   │
│   │       Design standards      │  │       Install/upgrade       │  │          Hardening          │   │
│   │         How it works        │  │        Scripts & CLI        │  │      Audit & compliance     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 / ARM64 servers · NIC · SAN/NAS storage · network switches · power & cooling                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  kernel      = Core of the OS; manages CPU, memory, devices, and system calls                         │
│  userspace   = Everything outside the kernel: daemons, shells, applications                           │
│  distro      = Linux distribution: kernel + package manager + default tooling                         │
│  RHEL        = Red Hat Enterprise Linux; subscription-based, enterprise-grade OS                      │
│  Ubuntu      = Debian-based distro popular for cloud and development workloads                        │
│  systemd     = Init system and service manager; PID 1 on modern Linux distros                         │
│  cgroups     = Kernel feature to limit and isolate CPU/memory per process group                       │
│  namespace   = Kernel isolation for PID, network, mount, UTS, IPC, user scopes                        │
│  SELinux     = Mandatory access control framework built into the Linux kernel                         │
│  PAM         = Pluggable Authentication Modules; flexible auth stack for Linux                        │
│  LVM         = Logical Volume Manager; flexible disk/volume abstraction layer                         │
│  LUKS        = Linux Unified Key Setup; standard for block-device encryption                          │
│  rpm / dpkg  = Package managers for RHEL/Debian families respectively                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
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

<a class="kb-card" href="mysql/"><strong>MySQL / MariaDB</strong><span>Database architecture, installation, replication, backup, and performance tuning.</span></a>
<a class="kb-card" href="postgresql/"><strong>PostgreSQL</strong><span>Database architecture, installation, replication, backup, and performance tuning.</span></a>
<a class="kb-card" href="directory-integration/"><strong>Directory Integration</strong><span>LDAP/AD authentication, SSSD, Kerberos, and sudo integration for Linux hosts.</span></a>

</div>
