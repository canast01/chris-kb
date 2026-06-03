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

## Process Flow

```text
┌───────────────────────────────── Runbook — Storage Volume Expansion ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Expand storage: grow array LUN → OS rescans → extend filesystem — all online         │   │
│   │           Pre-check: snapshot before expansion; confirm free pool capacity on array           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           1. Array          │  │         2. OS rescan        │  │         3. FS extend        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Expand LUN/vol       │  │      Linux: rescan-scsi     │  │       Linux: resize2fs      │   │
│   │       Verify pool free      │  │      Windows: DiskMgmt      │  │       Windows: Extend       │   │
│   │       Confirm new size      │  │       lsblk / diskpart      │  │     pvresize + lvextend     │   │
│   │        Array CLI/GUI        │  │      ESXi: rescan HBAs      │  │         df -h verify        │   │
│   │        Snapshot first       │  │       Multipath update      │  │      xfs_growfs for XFS     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │     FS type      │   Grow command   │  Partition needed │     Online?      │      Verify      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │       ext4       │ resize2fs /dev/X │   growpart first  │       Yes        │      df -h       │   │
│   │       XFS        │ xfs_growfs /mnt  │   growpart first  │       Yes        │      df -h       │   │
│   │       LVM        │lvextend + resize │  PV extend first  │       Yes        │    lvdisplay     │   │
│   │       NTFS       │  Extend Volume   │      DiskMgmt     │       Yes        │     Explorer     │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    rescan-scsi-bus= Script to trigger OS rescan after LUN resize; alternative: echo 1 > /sys/...      │
│    growpart       = Extends a partition within a disk; required before online FS extend               │
│    pvresize       = LVM: expands physical volume to use new LUN capacity                              │
│    lvextend -r    = LVM: extends logical volume and resizes filesystem in one step                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────── Runbook — Storage Volume Expansion ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Expand storage: grow array LUN → OS rescans → extend filesystem — all online         │   │
│   │           Pre-check: snapshot before expansion; confirm free pool capacity on array           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           1. Array          │  │         2. OS rescan        │  │         3. FS extend        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Expand LUN/vol       │  │      Linux: rescan-scsi     │  │       Linux: resize2fs      │   │
│   │       Verify pool free      │  │      Windows: DiskMgmt      │  │       Windows: Extend       │   │
│   │       Confirm new size      │  │       lsblk / diskpart      │  │     pvresize + lvextend     │   │
│   │        Array CLI/GUI        │  │      ESXi: rescan HBAs      │  │         df -h verify        │   │
│   │        Snapshot first       │  │       Multipath update      │  │      xfs_growfs for XFS     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │     FS type      │   Grow command   │  Partition needed │     Online?      │      Verify      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │       ext4       │ resize2fs /dev/X │   growpart first  │       Yes        │      df -h       │   │
│   │       XFS        │ xfs_growfs /mnt  │   growpart first  │       Yes        │      df -h       │   │
│   │       LVM        │lvextend + resize │  PV extend first  │       Yes        │    lvdisplay     │   │
│   │       NTFS       │  Extend Volume   │      DiskMgmt     │       Yes        │     Explorer     │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    rescan-scsi-bus= Script to trigger OS rescan after LUN resize; alternative: echo 1 > /sys/...      │
│    growpart       = Extends a partition within a disk; required before online FS extend               │
│    pvresize       = LVM: expands physical volume to use new LUN capacity                              │
│    lvextend -r    = LVM: extends logical volume and resizes filesystem in one step                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Dell PowerMax (Solutions Enabler):**
```bash
symconfigure -sid <SID> -cmd "modify dev <DEV_ID>, size=<cylinders>;" commit -noprompt
```

**Dell Unity:**
```bash
uemcli -d <ip> /stor/config/lun -id <lun_id> set -size <new_size_bytes>
```

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

**Linux — no LVM:**
```bash
resize2fs /dev/<device><part>   # ext4
xfs_growfs /mount/point          # xfs
```

## Step 4 — Validate

```bash
df -h                    # confirm new filesystem size
lsblk                    # confirm partition layout
multipath -ll            # confirm all paths still healthy
```

Write a test file to confirm the new space is accessible:
```bash
dd if=/dev/zero of=/mount/point/test.tmp bs=1M count=1024 oflag=direct && rm /mount/point/test.tmp
```

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
