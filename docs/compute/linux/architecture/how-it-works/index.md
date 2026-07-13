---
tags:
  - architecture
  - linux
description: "How It Works reference covering Overview, Kernel Subsystem Architecture, LVM Stack, Storage Stack, Network Stack and 1 more sections."
---
# Linux — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Kernel Subsystem Architecture, LVM Stack, Storage Stack, Network Stack and 1 more sections.

*Applies to: RHEL 8.x / 9.x · Ubuntu 22.04 / 24.04*
</div>

## Overview

Linux servers run RHEL, Ubuntu, or SLES as the base OS. All services are managed by **systemd**, storage is managed via **LVM2** (with dm-multipath for SAN), and security is enforced by **SELinux** (RHEL) or **AppArmor** (Ubuntu). Network configuration uses NetworkManager (`nmcli`) on RHEL and Netplan on Ubuntu.

## Kernel Subsystem Architecture

```d2
direction: right

KERNEL: "Linux Kernel\nRHEL / Ubuntu / SLES" {shape: rectangle}
STORAGE: "Storage Stack\nlvm2 · dm-multipath · xfs/ext4" {shape: rectangle}
NET: "Network Stack\nnm · bonding · firewalld" {shape: rectangle}
SVCS: "systemd Services\nsshd · rsyslog · cron" {shape: rectangle}
SEC: "Security\nSELinux / AppArmor · auditd · PAM" {shape: rectangle}
DISK: "Block Devices\n/dev/sd* / /dev/mapper/*" {shape: rectangle}
NIC: "Physical NICs\neth0 / bond0 / enp*" {shape: rectangle}
ADMIN: "Sysadmin" {shape: rectangle}

KERNEL -> STORAGE
KERNEL -> NET
KERNEL -> SVCS
KERNEL -> SEC
STORAGE -> DISK
NET -> NIC
ADMIN -> KERNEL
```

## Storage Stack

```d2
direction: right

appLayer: "Application\n(read/write syscall" {shape: rectangle}
vfsLayer: "VFS\nVirtual File System" {shape: rectangle}
fsLayer: "Filesystem\nxfs / ext4" {shape: rectangle}
blockLayer: "Block Layer\nI/O scheduler" {shape: rectangle}
driverLayer: "Device Driver\nscsi / nvme" {shape: rectangle}
diskLayer: "Physical Disk\nSSD / HDD / SAN LUN" {shape: rectangle}

appLayer -> vfsLayer
vfsLayer -> fsLayer
fsLayer -> blockLayer
blockLayer -> driverLayer
driverLayer -> diskLayer
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


```text title="Expected output"
Connection 'bond0' (12a4c5d8-9f2e-4a2b-8c1f-7e3a2b9d4f6a) successfully added.
Connection 'ethernet-eth0' (3f7b2c1a-5d9e-4a8b-9c2f-1e6a3b8d5f2c) successfully added.
Connection 'ethernet-eth1' (8a2d4f1c-6e3b-5c9a-1d7f-2a9b4e8c3f5d) successfully added.
Connection 'bond0.100' (5c9a1f3e-7b2d-4a8c-6e1b-9f3a2c5d8b7e) successfully added.
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: invalid bond option 'mode=802.3ad,miimon=100': unknown option` | Use `mode=active-backup` or `mode=balance-alb` instead; 802.3ad requires `mode=balance-alb` in nmcli syntax. |
    | `Error: Connection activation failed: Device 'eth0' is already managed by another connection` | Remove conflicting connections with `nmcli con delete ethernet-eth0` before adding to bond. |
    | `Error: unknown or ambiguous command 'ipv4.addresses'` | Use `ipv4.addresses "192.168.1.10/24"` with quotes around the IP/prefix value. |
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


```text title="Expected output"
● nginx.service - The NGINX HTTP and web server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
     Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2 days ago
       Docs: man:nginx(8)
    Process: 8421 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
   Main PID: 8422 (nginx)
      Tasks: 3 (limit: 4915)
     Memory: 12.4M
        CPU: 2min 34.821s
     CGroup: /system.slice/nginx.service
             ├─8422 "nginx: master process /usr/sbin/nginx"
             ├─8423 "nginx: worker process"
             └─8424 "nginx: worker process"

Jan 18 14:32:15 prod-web-01 systemd[1]: Started The NGINX HTTP and web server.

PV         VG       Fmt  Attr PSize   PFree
/dev/sda3  vg_data  lvm2 a--  100.00g 15.23g

VG       #PV #LV #SN Attr   VSize   VFree
vg_data    1   3   0 wz--n- 100.00g 15.23g

LV      VG       Attr       LSize   Pool Origin Data%  Meta%
lv_app  vg_data  -wi-ao---- 50.00g
lv_db   vg_data  -wi-ao---- 30.00g
lv_log  vg_data  -wi-ao----  4.77g

Size of logical volume vg_data/lv_app changed from 50.00 GiB (12800 extents) to 70.00 GiB (17920 extents).
Logical volume vg_data/lv_app successfully resized.
meta-data=/dev/mapper/vg_data-lv_app isize=512    agcount=4, agsize=3276800 blks
data blocks changed from 13107200 to 18350080 blks

NAME    IPADDR/PREFIXLEN
eth0    192.168.1.45/24
eth1    10.0.0.12/24
lo      127.0.0.1/8

default via 192.168.1.1 dev eth0 proto kernel scope link src 192.168.1.45
10.0.0.0/24 dev eth1 proto kernel scope link src 10.0.0.12

LISTEN    USERS      SEQNUM    PID/PROGRAM NAME
tcp       root       0         8422/nginx
tcp       mysql      0         1847/mysqld
tcp       postgres   0         2156/postgres
udp       root       0         945/systemd-resolved

NAME    SIZE TYPE MOUNTPOINT FSTYPE
sda     200G disk
├─sda1    1G part /boot      ext4
├─sda2   98G part            lvm
└─sda3  100G part /opt/app   xfs
sdb     500G disk
```
---

## See also

- [Linux — Design Standards](../design-standards/)
- [Linux — Integrations](../integrations/)
- [Linux — Deploy](../../deploy/)
