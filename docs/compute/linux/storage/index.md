# Linux Storage

Disk, LVM, filesystem, and mount management on RHEL and Ubuntu.
## Disk and Block Device Overview

```bash
# List all block devices with sizes and mount points
lsblk
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,UUID

# Disk details and partition table
fdisk -l /dev/sdb
parted /dev/sdb print

# Identify device by serial number / WWN (useful for SAN)
lsblk -o NAME,SERIAL,WWN,SIZE
udevadm info /dev/sdb | grep -E "ID_SERIAL|ID_WWN"
```

## LVM — Physical Volumes

```bash
# List PVs
pvdisplay
pvs

# Create PV on a new disk
pvcreate /dev/sdb

# Remove PV (after moving data off)
pvremove /dev/sdb
```

## LVM — Volume Groups

```bash
# List VGs
vgdisplay
vgs

# Create VG
vgcreate vg_data /dev/sdb /dev/sdc

# Extend VG with a new disk
vgextend vg_data /dev/sdd

# Check free space in VG
vgs -o name,size,free
```

## LVM — Logical Volumes

```bash
# List LVs
lvdisplay
lvs

# Create LV
lvcreate -L 50G -n lv_app vg_data

# Create LV using percentage of free VG space
lvcreate -l 80%FREE -n lv_app vg_data

# Extend LV and filesystem in one step
lvextend -L +20G /dev/vg_data/lv_app
xfs_growfs /dev/vg_data/lv_app     # XFS — online resize
resize2fs /dev/vg_data/lv_app      # ext4 — online resize

# Remove LV
lvremove /dev/vg_data/lv_app
```

## Filesystem Operations

```bash
# Format
mkfs.xfs /dev/vg_data/lv_app       # XFS (default on RHEL)
mkfs.ext4 /dev/vg_data/lv_app      # ext4

# Mount temporarily
mount /dev/vg_data/lv_app /opt/app

# Persistent mount in /etc/fstab
echo "/dev/vg_data/lv_app  /opt/app  xfs  defaults,nofail  0  2" >> /etc/fstab
mount -a    # Test fstab without reboot

# Check filesystem
xfs_repair /dev/vg_data/lv_app    # XFS (must be unmounted)
e2fsck -f /dev/vg_data/lv_app     # ext4 (must be unmounted)
```

## Disk Usage

```bash
# Filesystem usage summary
df -h

# Directory sizes (find large consumers)
du -sh /var/log/* 2>/dev/null | sort -h | tail -10
du -sh /home/* 2>/dev/null | sort -h | tail -10

# Find files larger than 1 GB
find / -xdev -size +1G -type f 2>/dev/null

# Find files modified in the last 24 hours
find /var/log -newer /tmp -type f 2>/dev/null | head -20
```

## Multipath (SAN LUNs)

```bash
# List multipath devices
multipath -ll

# Check path states
multipath -ll | grep -E "status|running|active|failed"

# Reload multipath config
systemctl reload multipathd

# Add a new LUN (after SAN zoning/mapping)
rescan-scsi-bus.sh       # Install: sg3_utils
echo "- - -" > /sys/class/scsi_host/host*/scan
multipath

# Verify device is visible
lsblk | grep dm-
```

## iSCSI

```bash
# Discover targets
iscsiadm -m discovery -t sendtargets -p <iscsi-target-ip>

# Login to target
iscsiadm -m node --login

# Check session status
iscsiadm -m session

# Persistent login (survive reboot)
iscsiadm -m node -o update -n node.startup -v automatic
```

## NFS Mounts

```bash
# Mount NFS share
mount -t nfs 10.0.0.5:/export/data /mnt/data

# Persistent NFS mount (with timeout options)
echo "10.0.0.5:/export/data  /mnt/data  nfs  defaults,_netdev,timeo=30,retrans=3  0  0" >> /etc/fstab

# Check NFS mount stats
nfsstat -m

# Show NFS exports from server
showmount -e 10.0.0.5
```

## Disk I/O Performance

```bash
# I/O statistics per device — extended
iostat -xz 1 5

# Key columns: %util (saturation), await (ms latency), r/s w/s (IOPS)
# %util > 80% = busy; await > 20ms = latency concern

# Per-process I/O (requires iotop)
iotop -o -P

# Disk read/write speed test (non-destructive — writes to tmpfs)
dd if=/dev/zero of=/tmp/testfile bs=1G count=1 oflag=direct
```

## Swap

```bash
# Check swap usage
free -h
swapon --show

# Add swap space (temporary — file-based)
dd if=/dev/zero of=/swapfile bs=1G count=4
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Persistent — add to /etc/fstab
echo "/swapfile  none  swap  sw  0  0" >> /etc/fstab

# Check swappiness
cat /proc/sys/vm/swappiness
# Set lower value for server workloads (10 recommended)
echo "vm.swappiness=10" >> /etc/sysctl.d/99-sysctl.conf
sysctl -p
```
