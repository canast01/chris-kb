---
tags:
  - networking
description: "A path is a complete end-to-end connection from an HBA port through the fabric to a storage target port."
---
# FC Paths

<div class="kb-summary">
A path is a complete end-to-end connection from an HBA port through the fabric to a storage target port.
</div>

![FC Paths — Diagram](../../../../assets/networking-protocols-fibre-channel-paths-diagram.svg)
Multipath I/O (MPIO) uses multiple paths simultaneously for redundancy and load distribution.

## Path Architecture

```text
Host HBA0 (WWPN-A) → Fabric A → Array Port CT-A0 → LUN
Host HBA1 (WWPN-B) → Fabric B → Array Port CT-B0 → LUN
```

Minimum for production: 2 paths per LUN across independent fabrics.

## Path States

| State | Meaning |
|---|---|
| **Active (I/O)** | Path is in use and carrying I/O |
| **Active (no I/O)** | Path is healthy but standby |
| **Dead / Failed** | Path is down — I/O not possible |
| **Standby** | Path available but not preferred |
| **Transitioning** | Path state changing — transient |

## Checking Paths

### Linux — DM-Multipath

```bash
# Show all paths and their state
multipath -ll

# Show path count per device
multipath -ll | grep -E "^[a-z]|policy|status"

# Path details
dmsetup ls --tree

# Reload multipath config
multipath -r

# Blacklist check
cat /etc/multipath.conf | grep -A5 blacklist
```


```text title="Expected output"
mpatha (360a98000534d41386b6f6e65633a) dm-0 NETAPP,LUN C-Mode
size=500G features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |-+- 2:0:0:0 sda 8:0  active ready running
| `-+- 3:0:0:0 sdb 8:16 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |-+- 4:0:0:0 sdc 8:32 active ready running
  `-+- 5:0:0:0 sdd 8:48 active ready running

mpathb (360a98000534d41386b6f6e65633b) dm-1 NETAPP,LUN C-Mode
size=1T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `-+- 2:0:1:0 sde 8:64 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `-+- 4:0:1:0 sdf 8:80 active ready running

mpatha: 4 paths
mpathb: 2 paths

mpatha (360a98000534d41386b6f6e65633a)
mpathb (360a98000534d41386b6f6e65633b)

(no output — command completes silently)

blacklist {
    devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]*"
    devnode "^hd[a-z]"
    wwn "360a98000534d41386b6f6e65633d"
}
```

!!! warning "Common errors"
    **`multipath: command not found`** — Install device-mapper-multipath package with `yum install device-mapper-multipath` or `apt install multipath-tools`.
    **`device-mapper: reload ioctl failed: Device or resource busy`** — Ensure no processes are accessing the multipath devices and try `multipath -F` to flush before reload.
    **`parse error in /etc/multipath.conf line 42`** — Check multipath.conf syntax with `multipath -t` to identify and fix configuration errors.
### ESXi

```bash
# List all paths for all datastores
esxcli storage core path list

# Paths for a specific device
esxcli storage core path list -d naa.<id>

# Active path count
esxcli storage core path list | grep -c "Active (I/O)"

# Path claim rules
esxcli storage core claimrule list
```


```text title="Expected output"
Name   Device                                    State   PluginName
------  ----------------------------------------  ------  ----------
vmhba2  naa.60001405d1234567890abcdef012345     Active  NMP
vmhba3  naa.60001405d1234567890abcdef012346     Active  NMP
vmhba4  naa.60001405d1234567890abcdef012347     Standby NMP
vmhba5  naa.60001405d1234567890abcdef012348     Active  NMP
vmhba6  naa.60001405d1234567890abcdef012349     Standby NMP

Name   Device                                    State   PluginName
------  ----------------------------------------  ------  ----------
vmhba2  naa.60001405d1234567890abcdef012345     Active  NMP

4

ClaimRule  PluginName  DeviceType  VendorFilter  ModelFilter  Options
---------  ----------  ----------  -----------   -----------  -------
101        NMP         disk        NETAPP        LUN          iops=3
102        NMP         disk        EMC           SYMMETRIX    iops=4
103        NMP         disk        PURE           FlashArray   iops=3
```

!!! warning "Common errors"
    **`Error: Unknown option or set of options: -d`** — Use the correct device identifier format without the `-d` flag; try `esxcli storage core path list | grep naa.<id>` instead.
    **`Error: Unable to find a matching vm kernel nic for the management network`** — Ensure the ESXi host has network connectivity and the management interface is properly configured before running storage commands.
### Windows — MPIO

```powershell
# Show MPIO paths
Get-MSDSMSupportedHW
Get-MPIOAvailableHW

# MPIO disk paths
Get-Disk | Get-MpioDisk | Select-Object -ExpandProperty MpioDeviceAttributes
```

## Path Policies

| Policy | Behaviour | Best for |
|---|---|---|
| **Round Robin** | Distributes I/O across all active paths | Active-active arrays (Pure, VPLEX) |
| **Fixed / Most Recently Used** | Sticks to preferred path; failover on failure | Active-passive arrays |
| **Least Queue Depth** | Sends I/O to path with fewest outstanding requests | High-latency mixed workloads |

## Common Path Issues

| Symptom | Cause | Check |
|---|---|---|
| Single path only | Dual-fabric not configured / zone missing on Fabric B | Verify zoning on both fabrics |
| All paths dead | HBA failure, fabric outage, or storage port down | Check HBA link, `portshow`, storage port state |
| Path flapping | SFP degraded or loose cable | `porterrshow` — look for high CRC or signal loss |
| Paths shown but I/O failing | LUN not mapped in storage host group | Verify LUN masking on array |
| Uneven I/O across paths | Round-robin not configured, using fixed policy | Set multipath policy to round-robin |

## Re-scanning for New Paths

```bash
# Linux — rescan HBAs
echo "- - -" > /sys/class/scsi_host/host0/scan
echo "- - -" > /sys/class/scsi_host/host1/scan
multipath -r

# ESXi — rescan all HBAs
esxcli storage core adapter rescan --all

# Windows
Update-StorageProviderCache -DiscoveryLevel Full
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
mpathb (36001405a1b2c3d4e5f6g7h8i9j0k1l2m) dm-0 NETAPP,LUN C-Mode
mpathc (36001405b2c3d4e5f6g7h8i9j0k1l2m3n4) dm-1 NETAPP,LUN C-Mode
mpatha (36001405c3d4e5f6g7h8i9j0k1l2m3n4o5) dm-2 NETAPP,LUN C-Mode
size=500G features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 2:0:0:0 sdb 8:16 active ready running
  `- 3:0:0:0 sdc 8:32 active ready running

HBA Name    Driver   Link State   Speed
vmhba0      lpfc     Link Up      16 Gbps
vmhba1      lpfc     Link Up      16 Gbps
vmhba2      bnx2fc   Link Up      10 Gbps

(no output — command completes silently)
```

!!! warning "Common errors"
    **`bash: /sys/class/scsi_host/host0/scan: Permission denied`** — Run the command with `sudo` or as root user.
    **`esxcli: command not found`** — Verify you are connected to an ESXi host via SSH; this command only runs on ESXi, not vCenter.
    **`Update-StorageProviderCache : The term 'Update-StorageProviderCache' is not recognized`** — Run PowerShell as Administrator and ensure the Storage module is loaded with `Import-Module Storage`.