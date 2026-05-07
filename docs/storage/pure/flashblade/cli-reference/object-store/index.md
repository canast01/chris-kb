# Object Store (S3)

> Part of the Pure FlashBlade CLI Reference.
## Buckets

```bash
# List buckets
purefb bucket list
purefb bucket list --all          # includes destroyed

# Create a bucket
purefb bucket create --name <bucket> --account <account>

# Destroy a bucket (must be empty)
purefb bucket destroy --name <bucket>

# Eradicate permanently
purefb bucket eradicate --name <bucket>
```

## Accounts

```bash
# List object store accounts
purefb object-store-account list

# Create an account
purefb object-store-account create --name <account>

# Destroy an account
purefb object-store-account destroy --name <account>
```

## Users

```bash
# List users
purefb object-store-user list

# Create a user under an account
purefb object-store-user create --name <user> --account <account>

# Destroy a user
purefb object-store-user destroy --name <user> --account <account>
```

## Access Keys

```bash
# List all access keys
purefb object-store-access-key list

# Create an access key for a user
purefb object-store-access-key create --user <user>/<account>

# Delete an access key
purefb object-store-access-key destroy --name <key_id>
```

> The secret access key is only shown at creation time — store it securely immediately.

## Bucket Replication

```bash
# List bucket replica links
purefb bucket-replica-link list

# Create a replica link to a remote FlashBlade
purefb bucket-replica-link create \
    --local-bucket <local_bucket> \
    --remote-bucket <remote_bucket> \
    --remote <remote_array_name>
```

## S3 Endpoint

```bash
# Show S3 service endpoint
purefb array | grep s3

# Test S3 connectivity
aws s3 ls --endpoint-url https://<flashblade_s3_vip>/
```
