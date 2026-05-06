# RDS

> Part of the AWS CLI Reference.

---

```bash
# Instances
aws rds describe-db-instances
aws rds describe-db-instances --db-instance-identifier <id>

# Start / stop
aws rds start-db-instance --db-instance-identifier <id>
aws rds stop-db-instance --db-instance-identifier <id>
aws rds reboot-db-instance --db-instance-identifier <id>

# Snapshots
aws rds describe-db-snapshots
aws rds create-db-snapshot --db-instance-identifier <id> --db-snapshot-identifier <snap_name>
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier <new_id> --db-snapshot-identifier <snap_name>
```
