---
tags:
  - storage
  - operations
description: "| Field | Value | |---|---| | Risk | Medium | | Approval | Change ticket required; confirm array pool capacity before expanding | | Estimated time | 20–40..."
---
# Storage Volume Expansion Runbook

<div class="kb-summary">
| Field | Value | |---|---| | Risk | Medium | | Approval | Change ticket required; confirm array pool capacity before expanding | | Estimated time | 20–40 minutes | | Impact | No downtime for online expansion; brief I/O pause during partition resize on some platforms |
</div>

| Field | Value |
|---|---|
| Risk | Medium |
| Approval | Change ticket required; confirm array pool capacity before expanding |
| Estimated time | 20–40 minutes |
| Impact | No downtime for online expansion; brief I/O pause during partition resize on some platforms |

```d2
direction: down

process_flow: "Process Flow" {shape: rectangle}
step_2_rescan_storage_on_the_host: "Step 2 — Rescan Storage on the Host" {shape: rectangle}
step_3a_resize_partition: "Step 3a — Resize Partition" {shape: rectangle}
step_3b_resize_filesystem_lv: "Step 3b — Resize Filesystem / LV" {shape: rectangle}
step_4_validate: "Step 4 — Validate" {shape: rectangle}
rollback: "Rollback" {shape: rectangle}

process_flow -> step_2_rescan_storage_on_the_host: uses
step_2_rescan_storage_on_the_host -> step_3a_resize_partition: uses
step_3a_resize_partition -> step_3b_resize_filesystem_lv: uses
step_3b_resize_filesystem_lv -> step_4_validate: uses
step_4_validate -> rollback: uses
```

## Process Flow

**Dell PowerMax (Solutions Enabler):**
```bash
symconfigure -sid <SID> -cmd "modify dev <DEV_ID>, size=<cylinders>;" commit -noprompt
```


```text title="Expected output"
Symmetrix ID: 000123456789ABC
Symmetrix microcode: 5978.1221.1221
Symmetrix model: VMAX 250F
Symmetrix capacity: 50.2 TB
Device ID: 0ABC
Current size: 10000 cylinders
New size: 15000 cylinders
Size increase: 5000 cylinders
Modification committed successfully.
Job ID: 1234567890
Status: SUCCEEDED
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `SYMCLI_ERROR: Device <DEV_ID> not found in Symmetrix <SID>` | Verify the device ID exists in the target array using `symdevice -sid <SID> list`. |
    | `SYMCLI_ERROR: Insufficient free space in pool` | Check available capacity in the storage pool with `sympools -sid <SID> -pool <POOL_NAME> show` and ensure the requested cylinder count is available. |
    | `SYMCLI_ERROR: Cannot modify device while in use` | Unmount or quiesce the volume on the host before attempting expansion using `umount <MOUNT_POINT>` or application-level pause commands. |
**Dell Unity:**
```bash
uemcli -d <ip> /stor/config/lun -id <lun_id> set -size <new_size_bytes>
```


```text title="Expected output"
The LUN (Logical Unit Number) size has been successfully expanded.
Operation ID: 0x7f3a2c1e
LUN ID: 45
Previous Size: 1099511627776 bytes (1 TB)
New Size: 2199023255552 bytes (2 TB)
Status: COMPLETED
Timestamp: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: The specified LUN is not found or is offline` | Verify the LUN ID is correct and the storage array is reachable by running `uemcli -d <ip> /stor/config/lun list`. |
    | `Error: Insufficient space available on storage pool` | Check available capacity on the pool with `uemcli -d <ip> /stor/config/pool -id <pool_id> show` and reduce the requested size if needed. |
    | `Error: LUN is currently in use by a host` | Ensure the LUN is unmapped from all hosts or quiesced before expansion; use `uemcli -d <ip> /stor/config/lun -id <lun_id> show` to verify current mappings. |
## Step 2 — Rescan Storage on the Host

**Linux:**
```bash
# Rescan all SCSI hosts
for host in /sys/class/scsi_host/host*/; do
    echo "- - -" > "${host}scan"
done

# Or target specific HBA
echo 1 > /sys/class/scsi_device/<H:B:T:L>/device/rescan

# Refresh multipath and confirm new size
multipathd reconfigure
multipath -ll
```


```text title="Expected output"
# Rescan all SCSI hosts
# (no output — command completes silently)

# Or target specific HBA
# (no output — command completes silently)

# Refresh multipath and confirm new size
reconfigure: reconfigured
mpatha (360014056b1e3e8e2b5d4c9a2f8e1b3c4) dm-0 NETAPP,LUN C-Mode
size=2.0T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 4:0:0:0 sda 8:0  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 5:0:0:0 sdb 8:16 active ready running
mpathb (360014056c2f4f9f3c6e5d0b1a9f2c3d5) dm-1 NETAPP,LUN C-Mode
size=1.5T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  `- 6:0:0:0 sdc 8:32 active ready running
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bash: /sys/class/scsi_host/host*/: No such file or directory` | Verify the system has SCSI HBAs present with `ls /sys/class/scsi_host/` before running the rescan loop. |
    | `multipathd: command not found` | Install the device-mapper-multipath package with `apt-get install multipath-tools` or `yum install device-mapper-multipath`. |
    | `multipath: command not found` | Ensure the multipath-tools package is installed and the multipathd daemon is running with `systemctl start multipathd`. |
**Windows:**
```powershell
Update-HostStorageCache
Get-Disk | Where-Object { $_.OperationalStatus -eq 'Online' } | Select Number, Size
```

## Step 3a — Resize Partition

**Linux (if using a raw partition, not LVM):**
```bash
# Identify device
lsblk

# Resize partition (parted)
parted /dev/<device> resizepart <part_number> 100%

# Inform kernel of change
partprobe /dev/<device>
```


```text title="Expected output"
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0  500G  0 disk
├─sda1   8:1    0    1M  0 part
├─sda2   8:2    0   99G  0 part /
└─sda3   8:3    0  400G  0 part /var/data
nvme0n1  259:0  0    2T  0 disk
└─nvme0n1p1 259:1  0    2T  0 part /mnt/storage

(parted) resizepart 3 100%
(parted) quit

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Could not stat device /dev/<device> - No such file or block device.` | Replace `<device>` with the actual device name (e.g., `sda`, `nvme0n1`) shown in lsblk output. |
    | `Error: Partition /dev/<device><part_number> is mounted.` | Unmount the partition with `umount /dev/<device><part_number>` before resizing, or use `resize2fs` after parted if the filesystem supports online resizing. |
    | `Error: Could not refresh the device entry /dev/<device>: Device or resource busy` | Ensure no processes are accessing the device and try `partprobe` again, or reboot the system if the device is the root filesystem. |
**Windows:**
```powershell
$disk = Get-Disk -Number <n>
$part = Get-Partition -DiskNumber $disk.Number -PartitionNumber <pn>
$maxSize = ($part | Get-PartitionSupportedSize).SizeMax
Resize-Partition -DiskNumber $disk.Number -PartitionNumber $part.PartitionNumber -Size $maxSize
```

## Step 3b — Resize Filesystem / LV

**Linux — LVM (most common):**
```bash
# Resize physical volume
pvresize /dev/mapper/<mpathX>

# Extend logical volume to use all free space
lvextend -l +100%FREE /dev/<vg>/<lv>

# Resize filesystem (online, no unmount needed)
resize2fs /dev/<vg>/<lv>       # ext4
xfs_growfs /mount/point         # xfs (use mountpoint, not device)
```


```text title="Expected output"
Physical volume "/dev/mapper/mpatha" changed: 1 physical extent(s) resized / 0 physical extent(s) unused
  Size of logical volume vg_storage/lv_data changed from 500.00 GiB (128000 extents) to 750.00 GiB (192000 extents).
  Logical volume vg_storage/lv_data successfully resized
resize2fs 1.46.2 (28-Feb-2021)
Filesystem at /dev/mapper/vg_storage-lv_data is mounted on /data; on-line resizing required
old_desc_blocks = 64, new_desc_blocks = 96
Performing an on-line resize of /dev/mapper/vg_storage-lv_data to 196608000 (4k) blocks.
The filesystem on /dev/mapper/vg_storage-lv_data is now 196608000 (4k) blocks long.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `resize2fs: Device or resource busy` | Ensure the filesystem is mounted before running resize2fs, or use the device path instead of attempting offline resize. |
    | `xfs_growfs: /dev/mapper/vg_storage-lv_data is not a mount point` | Use the mount point path (e.g., `/data`) instead of the device path for xfs_growfs. |
    | `Physical volume /dev/mapper/mpathX not found` | Verify the multipath device name with `multipath -ll` and confirm the device exists before running pvresize. |
**Linux — no LVM:**
```bash
resize2fs /dev/<device><part>   # ext4
xfs_growfs /mount/point          # xfs
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `resize2fs: Bad magic number in superblock` | Ensure the device is unmounted or use `resize2fs -f` only after confirming the filesystem is ext4 with `blkid`. |
    | `xfs_growfs: /mount/point is not a mounted XFS filesystem` | Verify the mount point exists and the filesystem is mounted with `mount | grep xfs`. |
## Step 4 — Validate

```bash
df -h                    # confirm new filesystem size
lsblk                    # confirm partition layout
multipath -ll            # confirm all paths still healthy
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/mapper/vg0-lv_root   500G  245G  255G  49% /
/dev/mapper/vg0-lv_data   2.0T  1.2T  800G  60% /data
/dev/sda1       1014M  187M  827M  19% /boot
tmpfs           7.8G     0  7.8G   0% /dev/shm

NAME                    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                       8:0    0  500G  0 disk
├─sda1                    8:1    0    1G  0 part /boot
└─sda2                    8:2    0  499G  0 part
  └─vg0-lv_root         253:0    0  500G  0 lvm  /
sdb                       8:16   0    2T  0 disk
└─sdb1                    8:17   0    2T  0 part
  └─vg0-lv_data         253:1    0    2.0T  0 lvm  /data
sdc                       8:32   0    2T  0 disk
└─sdc1                    8:33   0    2T  0 part
  └─vg0-lv_data         253:1    0    2.0T  0 lvm  /data

mpatha (36001405a1b2c3d4e5f6g7h8i9j0k1l2m) dm-0 NETAPP,LUN
size=2.0T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 4:0:0:0 sdb 8:16 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 5:0:0:0 sdc 8:32 active ready running
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `lsblk: command not found` | Install util-linux package with `apt-get install util-linux` or `yum install util-linux`. |
    | `multipath: command not found` | Install device-mapper-multipath with `apt-get install multipath-tools` or `yum install device-mapper-multipath`. |
Write a test file to confirm the new space is accessible:
```bash
dd if=/dev/zero of=/mount/point/test.tmp bs=1M count=1024 oflag=direct && rm /mount/point/test.tmp
```


```text title="Expected output"
1024+0 records in
1024+0 records out
1073741824 bytes (1.1 GB, 1.0 GiB) copied, 2.847 s, 379 MB/s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `dd: failed to open '/mount/point/test.tmp' for writing: No such file or directory` | Verify the mount point exists and is mounted with `mount | grep /mount/point` before running the command. |
    | `dd: error writing '/mount/point/test.tmp': No space left on device` | Reduce the count parameter (e.g., `count=512`) or free up space on the volume before retrying. |
    | `dd: opening '/dev/zero': Permission denied` | Run the command with `sudo` or as root to access `/dev/zero`. |
## Rollback

Online expansion of a LUN/partition/filesystem is **not reversible** without a rebuild. If something goes wrong:

1. Do not attempt to shrink — this risks data corruption
2. If partition resize failed mid-way, run `fsck` before mounting
3. If the filesystem is corrupt after resize, restore from backup

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Rescan shows old size | Multipath not refreshed | Run `multipathd reconfigure` then re-check |
| `pvresize` shows no change | Device path wrong | Verify `/dev/mapper/` path with `multipath -ll` |
| `lvextend` fails — no free space | PV size not updated | Run `pvresize` first |
| XFS won't grow | Mounted read-only | Remount read-write; XFS requires online mount to grow |
| Windows disk shows unallocated space | Partition not extended | Use `Resize-Partition` |

## Checklist

- [ ] Array pool capacity confirmed sufficient
- [ ] Host multipath healthy (all paths)
- [ ] LUN expanded on array
- [ ] Host rescan completed
- [ ] Host sees new raw size
- [ ] Partition resized (if applicable)
- [ ] LV extended (if LVM)
- [ ] Filesystem grown
- [ ] `df -h` shows new capacity
- [ ] Test write successful
- [ ] CMDB / capacity tracking updated
- [ ] Change ticket closed

## See also

- [Storage Runbooks](../index.md)
