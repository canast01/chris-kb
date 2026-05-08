# AWS — Procedures

> Part of the [Operations](../) section.

---

## RDS

AWS Relational Database Service — managed database instances, Multi-AZ, snapshots, and performance.

### Supported Engines

| Engine | Use Case |
|---|---|
| MySQL | General-purpose relational |
| PostgreSQL | Advanced SQL, JSON support |
| MariaDB | MySQL-compatible |
| Oracle | Enterprise legacy workloads |
| SQL Server | Windows ecosystem |
| Aurora MySQL / PostgreSQL | High performance, serverless option |

### Common CLI Commands

```bash
# List RDS instances
aws rds describe-db-instances \
  --query 'DBInstances[*].{ID:DBInstanceIdentifier,Engine:Engine,Class:DBInstanceClass,Status:DBInstanceStatus,AZ:AvailabilityZone,MultiAZ:MultiAZ,Endpoint:Endpoint.Address}' \
  --output table

# Describe a specific instance
aws rds describe-db-instances --db-instance-identifier <db-id>

# Create a snapshot
aws rds create-db-snapshot \
  --db-instance-identifier <db-id> \
  --db-snapshot-identifier <snap-name>

# List snapshots
aws rds describe-db-snapshots \
  --db-instance-identifier <db-id> \
  --query 'DBSnapshots[*].{ID:DBSnapshotIdentifier,Status:Status,Created:SnapshotCreateTime,Size:AllocatedStorage}' \
  --output table

# Reboot instance
aws rds reboot-db-instance --db-instance-identifier <db-id>

# Modify instance (example: enable Multi-AZ)
aws rds modify-db-instance \
  --db-instance-identifier <db-id> \
  --multi-az \
  --apply-immediately

# Start / stop instance (for dev/test)
aws rds stop-db-instance --db-instance-identifier <db-id>
aws rds start-db-instance --db-instance-identifier <db-id>
```

### Health Checks

```bash
# Check instance status
aws rds describe-db-instances --db-instance-identifier <db-id> \
  --query 'DBInstances[0].DBInstanceStatus'

# Check recent events
aws rds describe-events \
  --source-identifier <db-id> \
  --source-type db-instance \
  --duration 1440 \
  --query 'Events[*].{Time:Date,Message:Message}' \
  --output table

# CloudWatch — check key metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name FreeStorageSpace \
  --dimensions Name=DBInstanceIdentifier,Value=<db-id> \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average
```

### Key CloudWatch Metrics

| Metric | Warning Threshold | Critical Threshold |
|---|---|---|
| CPUUtilization | >70% | >90% |
| FreeStorageSpace | <20% | <10% |
| ReadLatency / WriteLatency | >10ms | >50ms |
| DatabaseConnections | >80% of `max_connections` | >95% |
| FreeableMemory | <20% | <10% |
| ReplicaLag (read replicas) | >30s | >120s |

### Restore from Snapshot

```bash
# Restore to new instance from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier <new-db-id> \
  --db-snapshot-identifier <snap-id> \
  --db-instance-class db.r6g.large \
  --no-publicly-accessible
```

### Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Connection refused | Security group / subnet group | Verify SG allows inbound on DB port from app subnet |
| High CPU | Slow query log | Enable `slow_query_log`; analyze with EXPLAIN |
| Storage full | `FreeStorageSpace` metric | Modify instance to increase `AllocatedStorage` |
| Multi-AZ failover delay | Event log | Expected: 60–120s for failover; update app retry logic |
| Read replica lagging | `ReplicaLag` metric | Check source instance I/O; consider read replica promotion |
