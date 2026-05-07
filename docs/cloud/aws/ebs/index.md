# EBS

AWS Elastic Block Store — block storage volumes, snapshots, performance, and lifecycle management.

## Volume Types

| Type | Use Case | Max IOPS | Max Throughput |
|---|---|---|---|
| gp3 | General purpose (default) | 16,000 | 1,000 MB/s |
| gp2 | General purpose (legacy) | 16,000 | 250 MB/s |
| io2 Block Express | High-performance databases | 256,000 | 4,000 MB/s |
| io1 | High IOPS workloads | 64,000 | 1,000 MB/s |
| st1 | Throughput-intensive (big data, log processing) | 500 | 500 MB/s |
| sc1 | Cold workloads, infrequently accessed | 250 | 250 MB/s |

## Common CLI Commands

```bash
# List volumes in a region
aws ec2 describe-volumes \
  --query 'Volumes[*].{ID:VolumeId,Type:VolumeType,Size:Size,State:State,IOPS:Iops,AZ:AvailabilityZone}' \
  --output table

# List volumes attached to an instance
aws ec2 describe-volumes \
  --filters "Name=attachment.instance-id,Values=<instance-id>" \
  --query 'Volumes[*].{ID:VolumeId,Device:Attachments[0].Device,Size:Size,Type:VolumeType}' \
  --output table

# Create snapshot
aws ec2 create-snapshot \
  --volume-id <vol-id> \
  --description "Pre-maintenance snapshot $(date +%Y-%m-%d)"

# List snapshots
aws ec2 describe-snapshots --owner-ids self \
  --query 'Snapshots[*].{ID:SnapshotId,Volume:VolumeId,Size:VolumeSize,State:State,Start:StartTime}' \
  --output table

# Modify volume — increase size or change type (no downtime)
aws ec2 modify-volume \
  --volume-id <vol-id> \
  --size 500 \
  --volume-type gp3 \
  --iops 6000 \
  --throughput 300

# Check modification progress
aws ec2 describe-volumes-modifications --volume-ids <vol-id>
```

## Resize Filesystem After Volume Modification

```bash
# After expanding an EBS volume — extend partition and filesystem on Linux
# Check device name
lsblk

# Grow partition (if partition exists)
sudo growpart /dev/xvda 1

# Resize filesystem
sudo resize2fs /dev/xvda1     # ext4
sudo xfs_growfs /             # xfs (provide mount point)
```

## Snapshots and AMIs

```bash
# Delete old snapshots (older than 30 days) — use with caution
aws ec2 describe-snapshots --owner-ids self \
  --query 'Snapshots[?StartTime<=`2026-04-01`].SnapshotId' \
  --output text | tr '\t' '\n' | while read snap; do
    echo "Deleting $snap"
    aws ec2 delete-snapshot --snapshot-id "$snap"
done

# Copy snapshot to another region
aws ec2 copy-snapshot \
  --source-region us-east-1 \
  --source-snapshot-id <snap-id> \
  --destination-region eu-west-1 \
  --description "Cross-region copy"
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| High latency / low IOPS | Volume type and provisioned IOPS | Switch to gp3 or io2 and increase IOPS |
| Volume stuck modifying | `describe-volumes-modifications` | Wait — large volumes take time; contact AWS Support if stuck >24h |
| Filesystem not expanded after resize | `lsblk` vs `df -h` | Run `growpart` + `resize2fs`/`xfs_growfs` |
| Snapshot failing | Available capacity in account | Check EBS snapshot limits; request limit increase if needed |
