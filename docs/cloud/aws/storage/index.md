---
tags:
  - aws
description: "AWS storage covers three models: EBS block volumes for EC2 boot and data disks, S3 object storage for backups and static assets, and EFS/FSx file storage..."
---
# AWS Storage

<div class="kb-summary">
AWS storage covers three models: EBS block volumes for EC2 boot and data disks, S3 object storage for backups and static assets, and EFS/FSx file storage for shared Linux and Windows workloads. Lifecycle policies automate tiering; snapshots and cross-region replication underpin DR.

*Applies to: AWS*
</div>

![AWS Storage — Diagram](../../../assets/cloud-aws-storage-diagram.svg)

![AWS Storage Architecture](../../../assets/aws-storage-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="ebs/">
  <strong>EBS</strong>
  <span>Block storage, volume types, performance, encryption, and expansion.</span>
</a>

<a class="kb-card" href="ebs-snapshots/">
  <strong>EBS Snapshots</strong>
  <span>Snapshot protection, retention, copy, restore, and lifecycle tasks.</span>
</a>

<a class="kb-card" href="s3/">
  <strong>S3</strong>
  <span>Object storage, buckets, permissions, lifecycle, replication, and encryption.</span>
</a>

<a class="kb-card" href="s3-lifecycle/">
  <strong>S3 Lifecycle</strong>
  <span>Lifecycle policies, transitions, expiration, and storage class control.</span>
</a>

<a class="kb-card" href="s3-replication/">
  <strong>S3 Replication</strong>
  <span>Cross-region replication, same-region replication, and validation.</span>
</a>

<a class="kb-card" href="efs/">
  <strong>EFS</strong>
  <span>Managed NFS storage, mount targets, throughput, and access points.</span>
</a>

<a class="kb-card" href="fsx/">
  <strong>FSx</strong>
  <span>Managed file systems, Windows, Lustre, NetApp ONTAP, and OpenZFS notes.</span>
</a>

</div>
