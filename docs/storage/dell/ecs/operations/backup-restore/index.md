# Dell ECS — Backup & Restore

> Backup configuration, restore procedures, and validation for Dell ECS.

## Overview

Dell ECS is an object storage platform. Data protection is primarily delivered through:

- **Geo-replication**: Objects are replicated across VDCs via replication groups. This is the primary mechanism for data durability and site-level recovery.
- **Erasure coding**: Within a VDC, objects are protected against disk and node failure through erasure coding (typically 12+4).
- **S3 Object Lock (WORM)**: Immutable retention for compliance and backup data.

ECS does not have a traditional backup agent. Configuration backup covers the management layer; data is protected by replication and erasure coding.

## Configuration Backup

Back up the following ECS configuration artefacts regularly:

| Artefact | Location | Method |
|---|---|---|
| Replication group topology | ECS Portal → Settings | Document in runbook; export via Management API |
| Namespace and bucket configuration | `ecscli namespace get` / `ecscli bucket get` | Script-based export via REST API |
| IAM users and access keys | ECS Portal → Namespace → IAM Users | Document; keys cannot be retrieved after creation |
| TLS certificates | ECS Portal → Settings → Certificates | Export and store in secrets management |
| Syslog / SNMP configuration | ECS Portal → Settings | Document in runbook |

## Restoring Object Data

Object data restore depends on the failure scenario:

**Node failure (within a VDC):**
- ECS automatically rebuilds erasure coding stripes to surviving nodes
- No manual restore required; monitor rebuild progress in ECS Portal → Hardware → Disks

**VDC failure (geo-replication configured):**
1. Update client S3 endpoints to point to the surviving VDC
2. Confirm data is accessible: `aws s3 ls s3://<bucket>/ --endpoint-url https://<secondary-vdc>`
3. Check replication lag at the time of failure to understand RPO exposure
4. When the failed VDC recovers, re-add it to the replication group and allow data to resync

**Accidental object deletion:**
- If bucket versioning is enabled, restore a previous version via the S3 API:
  ```bash
  # List object versions to find the version to restore
  aws s3api list-object-versions --bucket <bucket> \
    --endpoint-url https://<ecs-endpoint> --no-verify-ssl

  # Copy the desired version back as the current object
  aws s3api copy-object \
    --bucket <bucket> \
    --copy-source "<bucket>/<key>?versionId=<version-id>" \
    --key <key> \
    --endpoint-url https://<ecs-endpoint> --no-verify-ssl
  ```
- If versioning is not enabled, the object is unrecoverable unless present on a remote VDC with lower replication lag

## Validation

After any restore or VDC failover, validate the following:

- [ ] S3 endpoint functional test: `HeadBucket` or `ListBuckets` succeeds
- [ ] `ecscli namespace list` — all expected namespaces present
- [ ] Spot-check a sample of critical objects with `HeadObject` to confirm accessibility
- [ ] Confirm geo-replication is running and lag is at zero between all VDCs
- [ ] Application teams confirm S3 workloads are running normally
