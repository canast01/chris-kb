# Linux Server

<div class="kb-summary">
Linux server infrastructure running RHEL and Ubuntu — systemd service management, LVM2 storage, LACP bonded networking, SELinux/AppArmor security, and Ansible-driven automation for enterprise workloads.
</div>

```
┌───────────────────────────────────────── Linux Server Stack ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      Linux Administration                                     │   │
│   │        SSH: remote access · systemctl: service management · journalctl: log inspection        │   │
│   │            Package management: dnf (RHEL/Rocky) · apt (Ubuntu/Debian) · rpm / dpkg            │   │
│   │           Performance: perf/sar/iostat/vmstat/top · tracing: strace / ltrace / eBPF           │   │
│   │       Automation: Bash scripting · Python · Ansible: idempotent configuration management      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Administration tools span all subsystems from the kernel to application processes                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Networking         │  │           Storage           │   │
│   │   Linux kernel: monolithic  │  │   ip/ss: iproute2 toolkit   │  │   LVM: PV → VG → LV chain   │   │
│   │    Namespaces: isolation    │  │    iptables/nftables: FW    │  │    XFS · ext4 · Btrfs: FS   │   │
│   │   cgroups: resource limits  │  │    NetworkManager/netplan   │  │   NFS/CIFS: network mounts  │   │
│   │     systemd: PID 1, init    │  │     NIC bonding: 802.3ad    │  │   multipath: I/O failover   │   │
│   │   VFS: unified file layer   │  │   DNS: resolv.conf+systemd  │  │    RAID: md software RAID   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Kernel subsystems provide isolation, networking, and storage to all processes                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Operations         │  │           Security          │  │       Troubleshooting       │   │
│   │   cron/anacron: scheduling  │  │   SELinux: MAC enforcement  │  │   strace: syscall tracing   │   │
│   │    systemd timers: modern   │  │AppArmor: profile confinement│  │   tcpdump: packet capture   │   │
│   │   logrotate: log lifecycle  │  │   sudo/PAM: privilege ctrl  │  │  dmesg: kernel ring buffer  │   │
│   │  tuned: performance tuning  │  │   auditd: syscall auditing  │  │   lsof: open file/port map  │   │
│   │    ulimits: resource caps   │  │     SSH: key auth + MFA     │  │     perf: CPU profiling     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Operations, security, and troubleshooting tools work at the OS and kernel level                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SSH        │    SFTP / SCP    │        NFS        │    SMB / CIFS    │      rsync       │   │
│   │   Secure shell   │  File transfer   │   Unix FS mounts  │  Windows shares  │  Sync + backup   │   │
│   │   TCP port 22    │  SSH subsystem   │    TCP/UDP 2049   │     TCP 445      │     TCP 873      │   │
│   │  PubKey + TOTP   │  sftp/scp cmds   │   exports+fstab   │  smb.conf+fstab  │   rsync daemon   │   │
│   │   sshd_config    │   SFTP server    │     mount.nfs     │    mount.cifs    │   Incremental    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · NIC teaming · FC/iSCSI HBAs · iDRAC/iLO BMC · Power & Cooling                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  systemd  = PID 1 init system; manages service units, timers, mounts, and boot targets                │
│  SELinux  = Security-Enhanced Linux; mandatory access control using kernel labels                     │
│  LVM      = Logical Volume Manager; abstracts physical disks into flexible logical volumes            │
│  iproute2 = Modern Linux networking toolkit; ip, ss, tc replace ifconfig and route                    │
│  iptables = Linux kernel packet-filter firewall; replaced by nftables in newer kernels                │
│  NFS      = Network File System; mounts remote directories over IP using exports/fstab                │
│  cgroups  = Control Groups; kernel feature that limits CPU, memory, and I/O per process               │
│  strace   = System call tracer; shows every kernel call a process makes in real time                  │
│  auditd   = Linux audit daemon; logs syscall events for compliance and forensic analysis              │
│  PAM      = Pluggable Authentication Modules; controls how logins and sudo authenticate               │
│  tuned    = Linux performance daemon; applies OS profiles for different workload types                │
│  multipath= Device mapper feature; aggregates HBA paths to a single block device                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────── Linux Server Stack ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      Linux Administration                                     │   │
│   │        SSH: remote access · systemctl: service management · journalctl: log inspection        │   │
│   │            Package management: dnf (RHEL/Rocky) · apt (Ubuntu/Debian) · rpm / dpkg            │   │
│   │           Performance: perf/sar/iostat/vmstat/top · tracing: strace / ltrace / eBPF           │   │
│   │       Automation: Bash scripting · Python · Ansible: idempotent configuration management      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Administration tools span all subsystems from the kernel to application processes                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Networking         │  │           Storage           │   │
│   │   Linux kernel: monolithic  │  │   ip/ss: iproute2 toolkit   │  │   LVM: PV → VG → LV chain   │   │
│   │    Namespaces: isolation    │  │    iptables/nftables: FW    │  │    XFS · ext4 · Btrfs: FS   │   │
│   │   cgroups: resource limits  │  │    NetworkManager/netplan   │  │   NFS/CIFS: network mounts  │   │
│   │     systemd: PID 1, init    │  │     NIC bonding: 802.3ad    │  │   multipath: I/O failover   │   │
│   │   VFS: unified file layer   │  │   DNS: resolv.conf+systemd  │  │    RAID: md software RAID   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Kernel subsystems provide isolation, networking, and storage to all processes                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Operations         │  │           Security          │  │       Troubleshooting       │   │
│   │   cron/anacron: scheduling  │  │   SELinux: MAC enforcement  │  │   strace: syscall tracing   │   │
│   │    systemd timers: modern   │  │AppArmor: profile confinement│  │   tcpdump: packet capture   │   │
│   │   logrotate: log lifecycle  │  │   sudo/PAM: privilege ctrl  │  │  dmesg: kernel ring buffer  │   │
│   │  tuned: performance tuning  │  │   auditd: syscall auditing  │  │   lsof: open file/port map  │   │
│   │    ulimits: resource caps   │  │     SSH: key auth + MFA     │  │     perf: CPU profiling     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Operations, security, and troubleshooting tools work at the OS and kernel level                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SSH        │    SFTP / SCP    │        NFS        │    SMB / CIFS    │      rsync       │   │
│   │   Secure shell   │  File transfer   │   Unix FS mounts  │  Windows shares  │  Sync + backup   │   │
│   │   TCP port 22    │  SSH subsystem   │    TCP/UDP 2049   │     TCP 445      │     TCP 873      │   │
│   │  PubKey + TOTP   │  sftp/scp cmds   │   exports+fstab   │  smb.conf+fstab  │   rsync daemon   │   │
│   │   sshd_config    │   SFTP server    │     mount.nfs     │    mount.cifs    │   Incremental    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · NIC teaming · FC/iSCSI HBAs · iDRAC/iLO BMC · Power & Cooling                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  systemd  = PID 1 init system; manages service units, timers, mounts, and boot targets                │
│  SELinux  = Security-Enhanced Linux; mandatory access control using kernel labels                     │
│  LVM      = Logical Volume Manager; abstracts physical disks into flexible logical volumes            │
│  iproute2 = Modern Linux networking toolkit; ip, ss, tc replace ifconfig and route                    │
│  iptables = Linux kernel packet-filter firewall; replaced by nftables in newer kernels                │
│  NFS      = Network File System; mounts remote directories over IP using exports/fstab                │
│  cgroups  = Control Groups; kernel feature that limits CPU, memory, and I/O per process               │
│  strace   = System call tracer; shows every kernel call a process makes in real time                  │
│  auditd   = Linux audit daemon; logs syscall events for compliance and forensic analysis              │
│  PAM      = Pluggable Authentication Modules; controls how logins and sudo authenticate               │
│  tuned    = Linux performance daemon; applies OS profiles for different workload types                │
│  multipath= Device mapper feature; aggregates HBA paths to a single block device                      │
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
