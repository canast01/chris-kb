# EC2 — Images, Volumes & Snapshots


<div class="kb-summary">
EC2 — Images, Volumes & Snapshots reference.
</div>

```text
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
┌──────────────────────────────────────── AWS CLI — EC2 Storage ────────────────────────────────────────┐
│                                                                                                       │
│  EBS volume and snapshot CLI commands for provisioning, attaching, and DR operations.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Volume Operations               │  │              Volume Inspection              │   │
│   │           create-volume: provision           │  │            describe-volumes: list           │   │
│   │         attach-volume: mount to EC2          │  │            describe-volume-status           │   │
│   │            detach-volume: unmount            │  │          describe-volume-attribute          │   │
│   │          modify-volume: resize/type          │  │        describe-volumes-modifications       │   │
│   │            delete-volume: remove             │  │          enable-volume-io: recover          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Volumes created and attached; modify-volume resizes without downtime on Nitro                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Snapshot Operations              │  │                  Encryption                 │   │
│   │        create-snapshot: point-in-time        │  │          create-volume --encrypted          │   │
│   │           describe-snapshots: list           │  │         copy-snapshot: encrypt copy         │   │
│   │         copy-snapshot: cross-region          │  │        modify-ebs-default-encryption        │   │
│   │            delete-snapshot: purge            │  │          --kms-key-id: specify CMK          │   │
│   │         restore-snapshot-tier: thaw          │  │       describe-ebs-encryption-default       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  EBS storage hardware · Nitro hypervisor · KMS HSM · S3 (snapshot storage)                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  EBS             = Elastic Block Store; persistent block storage for EC2                              │
│  modify-volume   = Online resize or type change; no detach needed on Nitro instances                  │
│  enable-volume-io= Re-enables I/O on a volume after a potential data inconsistency                    │
│  Snapshot        = Incremental backup of EBS volume stored in S3                                      │
│  copy-snapshot   = Copies snapshot to another region for DR                                           │
│  restore-snapshot-tier= Restores archived snapshot from S3 Glacier to standard tier                   │
│  CMK             = Customer-Managed Key in KMS; used to encrypt EBS volumes                           │
│  modify-ebs-default-encryption= Sets account-level default to encrypt all new volumes                 │
│  Volume type     = gp3 (general), io2 (IOPS), st1 (throughput), sc1 (cold)                            │
│  gp3             = Default SSD volume; baseline 3000 IOPS, 125 MB/s throughput                        │
│  io2             = High-performance SSD; up to 64,000 IOPS; provisioned IOPS                          │
│  Nitro           = AWS hypervisor; allows online volume modifications without reboot                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
