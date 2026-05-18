# EC2 — Images, Volumes & Snapshots

```
EC2 Storage CLI: AMIs · EBS Volumes · Snapshots
──────────────────────────────────────────────────────────────

  ┌──────────────┐     create-image      ┌──────────────────┐
  │  EC2 Instance│────────────────────► │  AMI             │
  └──────────────┘                      │  describe-images  │
                                        └──────────────────┘
  ┌──────────────┐    create-volume      ┌──────────────────┐
  │  attach-vol  │◄─────────────────────│  EBS Volume      │
  │  (to EC2)    │                      │  describe-volumes │
  │  detach-vol  │                      │  delete-volume    │
  └──────────────┘                      └────────┬─────────┘
                                                 │ create-snapshot
                                                 ▼
                                        ┌──────────────────┐
                                        │  EBS Snapshot    │
                                        │  describe-snaps  │
                                        │  delete-snapshot │
                                        │  copy-snapshot   │
                                        │  (cross-region)  │
                                        └──────────────────┘
```

> Part of the AWS CLI Reference.

---

```bash
# AMIs
aws ec2 describe-images --owners self
aws ec2 create-image --instance-id <id> --name "snapshot-$(date +%F)" --no-reboot

# EBS volumes
aws ec2 describe-volumes
aws ec2 describe-volumes --filters "Name=attachment.instance-id,Values=<id>"
aws ec2 create-volume --availability-zone us-east-1a --size 100 --volume-type gp3
aws ec2 attach-volume --device /dev/xvdf --instance-id <id> --volume-id <vol_id>
aws ec2 detach-volume --volume-id <vol_id>
aws ec2 delete-volume --volume-id <vol_id>

# EBS snapshots
aws ec2 describe-snapshots --owner-ids self
aws ec2 create-snapshot --volume-id <vol_id> --description "backup"
aws ec2 delete-snapshot --snapshot-id <snap_id>
aws ec2 copy-snapshot --source-snapshot-id <snap_id> --source-region us-east-1 --destination-region eu-west-1
```
