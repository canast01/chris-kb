# S3

> Part of the AWS CLI Reference.

---

```bash
# Buckets
aws s3 ls
aws s3 ls s3://<bucket>/
aws s3 mb s3://<bucket>
aws s3 rb s3://<bucket> --force

# Objects
aws s3 cp <local_file> s3://<bucket>/<key>
aws s3 cp s3://<bucket>/<key> <local_file>
aws s3 mv s3://<bucket>/<key> s3://<bucket>/<new_key>
aws s3 rm s3://<bucket>/<key>
aws s3 rm s3://<bucket>/<prefix>/ --recursive

# Sync
aws s3 sync <local_dir> s3://<bucket>/<prefix>
aws s3 sync s3://<bucket>/<prefix> <local_dir>
aws s3 sync --delete s3://<source> s3://<dest>

# S3 API (for policy/lifecycle/versioning)
aws s3api get-bucket-versioning --bucket <bucket>
aws s3api put-bucket-versioning --bucket <bucket> --versioning-configuration Status=Enabled
aws s3api get-bucket-policy --bucket <bucket>
aws s3api list-object-versions --bucket <bucket>
aws s3api put-bucket-lifecycle-configuration --bucket <bucket> --lifecycle-configuration file://lifecycle.json
```
