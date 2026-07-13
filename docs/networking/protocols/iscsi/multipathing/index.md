---
tags:
  - networking
description: "iSCSI multipathing uses multiple network paths between initiator and target for redundancy and load distribution."
---
# iSCSI Multipathing

<div class="kb-summary">
iSCSI multipathing uses multiple network paths between initiator and target for redundancy and load distribution.
</div>

        iSCSI MULTIPATH TOPOLOGY

On Linux, DM-Multipath handles this; on Windows, MPIO; on ESXi, NMP with PSP.

```d2
direction: down

recommended_network_layout: "Recommended Network Layout" {shape: rectangle}
linux_dmmultipath: "Linux — DM-Multipath" {shape: rectangle}
windows_mpio: "Windows — MPIO" {shape: rectangle}
vmware_esxi_nmp: "VMware ESXi — NMP" {shape: rectangle}
load_balance_policies: "Load Balance Policies" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

recommended_network_layout -> linux_dmmultipath: uses
linux_dmmultipath -> windows_mpio: uses
windows_mpio -> vmware_esxi_nmp: uses
vmware_esxi_nmp -> load_balance_policies: uses
load_balance_policies -> common_issues: uses
```

## Recommended Network Layout

```text
Server NIC0 → Storage VLAN A (10.10.1.x) → Array Port A
Server NIC1 → Storage VLAN B (10.10.2.x) → Array Port B
```

Use separate NICs and separate switches (or VLANs at minimum) for each path. Never share iSCSI with management traffic.

## Linux — DM-Multipath

```bash
# Install
dnf install device-mapper-multipath

# Enable and start
systemctl enable --now multipathd

# View all multipath devices and path state
multipath -ll

# Sample output interpretation:
# mpatha (360000000000000) dm-0 PURE,FlashArray
# size=100G features='0' hwhandler='1 alua' wp=rw
# |-+- policy='service-time 0' prio=50 status=active
# | |- 33:0:0:1  sdb 8:16 active ready running
# | |- 34:0:0:1  sdd 8:48 active ready running
# +-+- policy='service-time 0' prio=10 status=enabled
#   |- 33:0:1:1  sdc 8:32 active ready running
#   |- 34:0:1:1  sde 8:64 active ready running

# Reload path config after changes
multipath -r

# Show multipath topology
multipath -t
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 19 Dec 2024 14:22:18 UTC.
Dependencies resolved.
================================================================================
 Package                    Architecture  Version          Repository     Size
================================================================================
Installing:
 device-mapper-multipath    x86_64        0.9.4-3.el9      baseos        521 k

Transaction Summary
================================================================================
Install  1 Package

Total download size: 521 k
Installed size: 1.2 M
Downloading Packages:
[100%] device-mapper-multipath-0.9.4-3.el9.x86_64.rpm
Running transaction
Preparing        :                                                        1/1
Installing       : device-mapper-multipath-0.9.4-3.el9.x86_64            1/1
Verifying        : device-mapper-multipath-0.9.4-3.el9.x86_64            1/1

Created symlink /etc/systemd/system/multi-user.target.wants/multipathd.service → /etc/systemd/system/multipathd.service.
mpatha (360014056d2a1234567890abcdef) dm-0 PURE,FlashArray//E
size=100G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 33:0:0:1  sdb 8:16  active ready running
| |- 34:0:0:1  sdd 8:48  active ready running
+-+- policy='service-time 0' prio=10 status=enabled
  |- 33:0:1:1  sdc 8:32  active ready running
  |- 34:0:1:1  sde 8:64  active ready running

mpathb (360014056d2a9876543210fedcba) dm-1 PURE,FlashArray//E
size=50G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 35:0:0:2  sdf 8:80  active ready running
+-+- policy='service-time 0' prio=10 status=enabled
  |- 35:0:1:2  sdg 8:96  active ready running

(no output — command completes silently)
mpatha: 2 path groups with 2 active, 2 enabled paths
mpathb: 2 path groups with 1 active, 1 enabled paths
```

!!! warning "Common errors"
    **`multipathd.service is not running`** — Run `systemctl start multipathd` to start the service immediately.
    **`multipath: command not found`** — Verify the device-mapper-multipath package installed successfully with `rpm -q device-mapper-multipath`.
    **`No multipath output (empty result)`** — Ensure iSCSI targets are discovered and connected with `iscsiadm -m session` before multipath can detect devices.
### /etc/multipath.conf — Key Settings

```conf
defaults {
    find_multipaths  yes
    user_friendly_names yes
}

blacklist {
    devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]*"
    devnode "^hd[a-z]"
    devnode "^sda$"   # local OS disk — always blacklist
}
```

Most major arrays (Pure, NetApp, Dell) have well-known hardware handlers — use vendor-recommended multipath.conf from their support portal.

## Windows — MPIO

```powershell
# Install MPIO feature
Install-WindowsFeature -Name Multipath-IO

# Add iSCSI device support to MPIO
New-MSDSMSupportedHW -VendorId PURE -ProductId FlashArray

# View MPIO paths
Get-MpioDisk
Get-MpioAvailableDriveLetters

# Set load balance policy
Set-MSDSMGlobalDefaultLoadBalancePolicy -Policy RR   # Round Robin
```

## VMware ESXi — NMP

```bash
# Show PSP (path selection policy) per datastore
esxcli storage nmp device list

# Change PSP for a device
esxcli storage nmp device set \
  -d naa.<id> \
  --psp VMW_PSP_RR

# View active paths
esxcli storage core path list -d naa.<id>

# Set Round Robin I/O operations limit (default 1000)
esxcli storage nmp psp roundrobin deviceconfig set \
  -d naa.<id> --type iops --iops 1
```


```text title="Expected output"
naa.6001405abc123def4567890123456789
   Runtime Name: vmhba0:C0:T0:L0
   Device Display Name: NETAPP LUN (naa.6001405abc123def4567890123456789)
   Aliases: NETAPP-LUN-001
   Partition Table Type: gpt
   Devfs Path: /vmfs/devices/disks/naa.6001405abc123def4567890123456789
   Current Path Selection Policy: VMW_PSP_MRU
   Path Selection Policy Device Config: {policy:iops,iops:1000}

naa.6001405xyz789abc1234567890abcdef
   Runtime Name: vmhba1:C0:T1:L0
   Device Display Name: PURE STORAGE FlashArray (naa.6001405xyz789abc1234567890abcdef)
   Current Path Selection Policy: VMW_PSP_FIXED

(no output — command completes silently)

Name: vmhba0:C0:T0:L0
   Runtime Name: naa.6001405abc123def4567890123456789
   Device: naa.6001405abc123def4567890123456789
   State: active
   Transport: SAS
   Adapter: vmhba0  Channel: 0  Target: 0  LUN: 0

Name: vmhba1:C0:T0:L0
   Runtime Name: naa.6001405abc123def4567890123456789
   Device: naa.6001405abc123def4567890123456789
   State: active
   Transport: SAS
   Adapter: vmhba1  Channel: 0  Target: 0  LUN: 0

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unknown device naa.6001405abc123def4567890123456789`** — Verify the NAA ID is correct by running `esxcli storage nmp device list` and copy the exact device identifier.
    **`Error: Unknown PSP VMW_PSP_RR`** — Use the correct PSP name `VMW_PSP_RR` (Round Robin) or verify available policies with `esxcli storage nmp psp list`.
## Load Balance Policies

| Policy | Linux | Windows | ESXi | Best for |
|---|---|---|---|---|
| Round Robin | `round-robin 0` | `RR` | `VMW_PSP_RR` | Active-active arrays |
| Least Queue | `queue-length 0` | `LQD` | — | Mixed latency |
| Fixed / MRU | `failover` | `FO` | `VMW_PSP_MRU` | Active-passive arrays |

## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| Single path only | Second NIC not bound to iSCSI | Verify both NICs have iSCSI sessions established |
| All paths failed | Network outage or array port down | `multipath -ll` — check path states |
| I/O pinned to one path | Round robin not configured | Set PSP to RR on ESXi; `multipath -ll` policy on Linux |
| Device shows as `dm-N` but no multipath | OS disk accidentally included | Add to `blacklist` in multipath.conf |
