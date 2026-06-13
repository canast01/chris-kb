---
tags:
  - architecture
  - linux
---
# Linux — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Kernel Subsystem Architecture, LVM Stack, Storage Stack, Network Stack and 1 more sections.

*Applies to: RHEL 8.x / 9.x · Ubuntu 22.04 / 24.04*
</div>

## Overview

Linux servers run RHEL, Ubuntu, or SLES as the base OS. All services are managed by **systemd**, storage is managed via **LVM2** (with dm-multipath for SAN), and security is enforced by **SELinux** (RHEL) or **AppArmor** (Ubuntu). Network configuration uses NetworkManager (`nmcli`) on RHEL and Netplan on Ubuntu.

## Kernel Subsystem Architecture

```mermaid
graph TB
  KERNEL["Linux Kernel\nRHEL / Ubuntu / SLES"]
  KERNEL --> STORAGE["Storage Stack\nlvm2 · dm-multipath · xfs/ext4"]
  KERNEL --> NET["Network Stack\nnm · bonding · firewalld"]
  KERNEL --> SVCS["systemd Services\nsshd · rsyslog · cron"]
  KERNEL --> SEC["Security\nSELinux / AppArmor · auditd · PAM"]
  STORAGE --> DISK[("Block Devices\n/dev/sd* / /dev/mapper/*")]
  NET --> NIC["Physical NICs\neth0 / bond0 / enp*"]
  ADMIN(["Sysadmin"]) -->|"SSH / console"| KERNEL
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef net fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class KERNEL ctrl
  class STORAGE,SVCS,SEC net
  class DISK store
  class NIC,NET net
  class ADMIN host
```
```text
┌──────────────────────────────────────── Linux — How It Works ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                         Boot Sequence                                         │   │
│   │      UEFI/BIOS → GRUB2 bootloader → kernel decompresses into RAM → initramfs mounts root      │   │
│   │       kernel init: detects hardware, loads drivers, mounts real rootfs, exec /sbin/init       │   │
│   │        systemd: reads default.target, activates units in dependency order, starts getty       │   │
│   │      Login: PAM stack authenticates user; bash/zsh shell launched as child of sshd/getty      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Every process originates from PID 1 through fork(); exec() loads new program images                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Syscall & I/O Path              │  │             Scheduling & Memory             │   │
│   │          app calls read() via glibc          │  │       CFS picks next task by vruntime       │   │
│   │         SYSCALL instruction → ring 0         │  │        context switch saves registers       │   │
│   │        VFS dispatches to block layer         │  │       page fault → alloc physical page      │   │
│   │         I/O scheduler (mq-deadline)          │  │        mmap: maps file into VA space        │   │
│   │          NVMe/SCSI driver sends cmd          │  │        OOM: score + kill on pressure        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 CPUs (rings 0/3) · RAM · NVMe/SAS · PCIe bus · iDRAC BMC · Power & Cooling                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GRUB2       = GRand Unified Bootloader v2; presents boot menu and loads kernel + initramfs           │
│  initramfs   = Temporary RAM root used during boot to mount the real root filesystem                  │
│  fork        = Syscall that clones the calling process; child inherits FDs and memory                 │
│  exec        = Syscall family that replaces process image with a new program binary                   │
│  vruntime    = Virtual runtime; CFS metric tracking how much CPU time a task has used                 │
│  context switch= CPU saves registers of running task and loads state of next scheduled task           │
│  page fault  = MMU exception when a virtual address has no mapped physical page yet                   │
│  mmap        = Memory-map syscall; maps files or anonymous memory into a process VAS                  │
│  mq-deadline = Multi-queue deadline I/O scheduler; prioritises read latency over throughput           │
│  ring 0      = CPU privilege level for kernel code; ring 3 is unprivileged userspace                  │
│  PAM         = Pluggable Authentication Modules; configures how login and sudo authenticate           │
│  getty       = Terminal program that presents the login prompt on a virtual console                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Storage Stack

```mermaid
flowchart LR
    appLayer["Application\n(read/write syscall)"]
    vfsLayer["VFS\nVirtual File System"]
    fsLayer["Filesystem\nxfs / ext4"]
    blockLayer["Block Layer\nI/O scheduler"]
    driverLayer["Device Driver\nscsi / nvme"]
    diskLayer["Physical Disk\nSSD / HDD / SAN LUN"]
    appLayer --> vfsLayer --> fsLayer --> blockLayer --> driverLayer --> diskLayer
```

## Network Stack

All production servers require bonded LACP uplinks and separate management/data VLANs:

```bash
# Configure bonded interface with VLAN (RHEL / nmcli)
nmcli con add type bond ifname bond0 bond.options "mode=802.3ad,miimon=100"
nmcli con add type ethernet ifname eth0 master bond0
nmcli con add type ethernet ifname eth1 master bond0
nmcli con add type vlan con-name bond0.100 dev bond0 id 100
nmcli con modify bond0.100 ipv4.addresses <ip>/<prefix> ipv4.gateway <gw> ipv4.method manual
```

## Key CLI Commands

```bash
# Service management (systemd)
systemctl status <service>
journalctl -u <service> -n 100 --no-pager

# Package updates
dnf check-update && dnf upgrade    # RHEL
apt-get update && apt-get upgrade  # Ubuntu

# LVM
pvs && vgs && lvs
lvextend -L +20G /dev/vg_data/lv_app && xfs_growfs /opt/app

# Network
ip -br addr && ip route show
ss -tulnp
ethtool <interface> | grep -E "Link detected|Speed"

# Storage
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE
multipath -ll
df -h && iostat -xz 1 5

# SAN / iSCSI
iscsiadm -m session
rescan-scsi-bus.sh

# Firewall
firewall-cmd --list-all          # RHEL
ufw status verbose               # Ubuntu
```
