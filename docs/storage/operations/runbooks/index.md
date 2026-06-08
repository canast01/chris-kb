# Storage — Operational Runbooks

<div class="kb-summary">
Storage operational runbooks — LUN provisioning, replication failover, capacity expansion, snapshot management, and host connectivity validation.
</div>

<div class="kb-grid kb-grid-1">
<a class="kb-card" href="storage-volume-expansion/"><strong>Storage Volume Expansion</strong><span>Volume expansion runbook — thin pool extension, host rescan, partition resize, and filesystem grow.</span></a>
</div>

## LUN Provisioning Runbook

```text
1. Confirm capacity available in storage pool
2. Create volume: name = <hostname>_<purpose>_<size>GB (e.g. sql01_data_500GB)
3. Set protection policy (replication, snapshots)
4. Map to host / host group
5. On host: rescan HBAs / iSCSI
   - Linux: echo "- - -" > /sys/class/scsi_host/hostX/scan
   - Windows: Get-Disk; Initialize-Disk
6. Identify new disk, create partition, format, mount
7. Test I/O: fio or diskspd
8. Document in CMDB
```

## Snapshot Schedule Review

```bash
# Pure FlashArray: check snapshot schedules
purenetwork list   # verify array connectivity
pureprotection list schedules   # review snapshot policies

# Dell PowerMax / SRDF: verify snapshots active
symsnap list -sid <sid> -lun <lun>

# Validate latest snapshot is not stale
# Alert if newest snapshot > 2× schedule interval
```

## Replication Failover Runbook (Generic)

```text
PRE-FAILOVER (planned):
1. Quiesce writes to source (stop application, flush I/O)
2. Verify replication in sync (lag = 0)
3. Demote source volume / break replication pair
4. Promote target volume to read-write
5. Mount on DR host
6. Start application at DR site
7. Update DNS/load balancer

UNPLANNED FAILOVER:
1. Confirm source site is unreachable
2. Promote target (may have some lag — document RPO breach)
3. Mount on DR host
4. Start application
5. Post-incident: quantify RPO breach, check data integrity
```

## Capacity Expansion

```bash
# Add capacity to thin pool (Pure/Dell)
# 1. Install additional shelves / drives (hardware team)
# 2. Present new capacity to pool via array GUI
# 3. Verify pool size increased
# 4. No host-side action needed for thin-provisioned volumes

# Expand an existing volume (online)
# Pure FlashArray CLI:
purevol resize --size 2T vol_name

# Linux host: rescan and extend filesystem
echo 1 > /sys/block/sdX/device/rescan
pvresize /dev/sdX
lvextend -l +100%FREE /dev/vg0/lv_data
resize2fs /dev/vg0/lv_data
```

## Host Connectivity Validation

```bash
# List visible storage devices (Linux)
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
multipath -ll   # show multipath device groups

# Test I/O latency
dd if=/dev/zero of=/mnt/data/test bs=4k count=10000 oflag=direct
fio --name=test --rw=randread --bs=4k --ioengine=libaio --iodepth=32 --size=1G --runtime=30 --filename=/mnt/data/fio.tmp
```
