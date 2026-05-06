# Object Store (S3)

> Part of the [Pure FlashBlade CLI Reference](../).

---

## Object Store (S3)

```bash
# Buckets
purefb bucket show
purefb bucket create --name <bucket> --account <account>
purefb bucket destroy --name <bucket>
purefb bucket eradicate --name <bucket>

# Accounts
purefb object-store-account show
purefb object-store-account create --name <account>

# Users
purefb object-store-user show
purefb object-store-user create --name <user> --account <account>

# Access keys
purefb object-store-access-key show
purefb object-store-access-key create --user <user>/<account>
```
