# AWS — Procedures

> Part of the [Operations](../index.md) section.

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
┌─────────────────────────────── AWS Operations — Procedures & Runbooks ────────────────────────────────┐
│                                                                                                       │
│  Standard operating procedures for AWS change management, incident response, and routine ops.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Change Management               │  │              Incident Response              │   │
│   │       RFC: document scope and rollback       │  │        Detect: CloudWatch alarm fires       │   │
│   │        CAB approval for prod changes         │  │      Acknowledge: on-call via PagerDuty     │   │
│   │      Change window: low-traffic period       │  │      Investigate: CloudTrail + CW Logs      │   │
│   │     Pre-change: snapshot + health check      │  │      Contain: isolate affected resource     │   │
│   │      Post-change: validate + close RFC       │  │       Recover: restore from backup/AMI      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SSM Automation documents codify runbooks; OpsCenter tracks operational issues.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Routine Operations              │  │             Post-Incident Review            │   │
│   │     Daily: review CloudWatch dashboards      │  │      Timeline: reconstruct from CT logs     │   │
│   │      Weekly: cost anomaly report review      │  │          Root cause: 5-why analysis         │   │
│   │       Monthly: patch compliance report       │  │      Action items: preventive controls      │   │
│   │         Quarterly: IAM access review         │  │       Document: PIR in Confluence/Jira      │   │
│   │    Annual: DR test + architecture review     │  │     Share: distribute learnings to team     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS regional infrastructure · Multi-AZ service endpoints · CloudTrail audit data                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RFC             = Request for Change; documents scope, risk, and rollback plan                       │
│  CAB             = Change Advisory Board; approves high-risk changes before execution                 │
│  Change window   = Pre-approved time slot for making infrastructure changes                           │
│  Rollback plan   = Documented steps to revert changes if post-change validation fails                 │
│  OpsCenter       = SSM feature that aggregates operational issues with context                        │
│  SSM Automation  = Document-based runbook executed against AWS resources                              │
│  PIR             = Post-Incident Review; blameless analysis after an incident                         │
│  5-why analysis  = Root cause technique: ask why 5 times to find the true cause                       │
│  On-call rotation= Schedule assigning primary/secondary responders for incident alerts                │
│  Runbook         = Step-by-step procedure for a repeatable operational task                           │
│  IAM access review= Periodic audit of unused permissions and inactive access keys                     │
│  DR test         = Disaster recovery test validating RTO/RPO targets are achievable                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
