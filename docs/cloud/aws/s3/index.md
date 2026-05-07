# AWS S3

## Overview

AWS S3 is object storage used for backups, logs, application data, static sites, data lakes, and archive workflows.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review bucket access policies |  |  |
| Check lifecycle rules |  |  |
| Confirm replication status |  |  |
| Review storage growth |  |  |
| Validate encryption settings |  |  |

## Health Commands

```bash
aws s3 ls
aws s3api list-buckets
aws s3api get-bucket-encryption --bucket BUCKET_NAME
aws s3api get-bucket-versioning --bucket BUCKET_NAME
```

## Upgrade Workflow

S3 is a managed service. Operational changes usually involve lifecycle, replication, encryption, policy, and logging updates.

1. Export current bucket policy
2. Review access and encryption impact
3. Apply change
4. Validate application access
5. Confirm logging and replication remain healthy
