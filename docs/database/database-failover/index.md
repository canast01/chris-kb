# Database Failover Procedure

Promote a standby/replica database to primary when the primary becomes unavailable. Follow the appropriate section for each platform.

```
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌─────────────────┐
│ Primary Fails    │   │ Replica Promoted │   │  DNS Updated     │   │ App Reconnects  │
│                  │   │                  │   │                  │   │                 │
│ Confirm failure  │   │ pg_ctl promote   │   │ CNAME / VIP /    │   │ Connection pool │
│ from multiple    │──►│ RESET SLAVE ALL  │──►│ ProxySQL backend │──►│ flush / bounce  │
│ paths; check lag │   │ AG FAILOVER      │   │ updated to new   │   │ App health chk  │
│                  │   │ Patroni failover │   │ primary host     │   │ returns 200     │
└──────────────────┘   └──────────────────┘   └──────────────────┘   └─────────────────┘
                                                                               │
                                                                      ┌────────┘
                                                                      ▼
                                                             ┌────────────────┐
                                                             │ Rebuild old    │
                                                             │ primary as new │
                                                             │ replica        │
                                                             └────────────────┘
```

## Pre-Failover Checklist

- [ ] Primary failure confirmed (not a network partition — verify from multiple paths)
- [ ] Standby replication lag checked — data loss risk understood
- [ ] Application teams notified (DBA lead, app owners, on-call)
- [ ] DNS / VIP failover method identified and ready
- [ ] Rollback path documented (if primary recovers)

## PostgreSQL — Streaming Replication Failover

```bash
# On STANDBY — check replication lag before promoting
psql -U postgres -c "SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"

# Promote standby to primary
pg_ctl promote -D /var/lib/postgresql/data
# or PostgreSQL 12+:
touch /var/lib/postgresql/data/promote_standby

# Verify promotion
psql -U postgres -c "SELECT pg_is_in_recovery();"  # should return 'f' (false)
psql -U postgres -c "SELECT now() AS current_time;"

# Update application connection string / DNS to point at new primary
```

### PostgreSQL — Patroni (HA cluster)

```bash
# View cluster state
patronictl -c /etc/patroni/config.yml list

# Manual failover to specific member
patronictl -c /etc/patroni/config.yml failover <cluster-name> --master <old-primary> --candidate <new-primary>

# Switchover (graceful — zero data loss)
patronictl -c /etc/patroni/config.yml switchover <cluster-name>
```

## MySQL / MariaDB — Replica Promotion

```bash
# On REPLICA — stop replication and capture position
mysql -u root -e "STOP SLAVE;"
mysql -u root -e "SHOW SLAVE STATUS\G"  # note Exec_Master_Log_Pos

# Reset replica to become new primary
mysql -u root -e "RESET SLAVE ALL;"
mysql -u root -e "RESET MASTER;"

# Enable writes (if read_only was set)
mysql -u root -e "SET GLOBAL read_only = OFF;"
mysql -u root -e "SET GLOBAL super_read_only = OFF;"

# Re-point application connection (update DNS / HAProxy / ProxySQL backend)
```

### MySQL — MHA (Master High Availability)

```bash
# Automatic failover — check MHA status
masterha_check_repl --conf=/etc/mha/app.conf

# Manual failover
masterha_master_switch --conf=/etc/mha/app.conf --master_state=dead --new_master_host=<replica-host>
```

## SQL Server — Always On Availability Group

```sql
-- Check AG health before failover
SELECT ag.name, ar.replica_server_name, rs.role_desc, rs.synchronization_health_desc
FROM sys.dm_hadr_availability_replica_states rs
JOIN sys.availability_replicas ar ON rs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id;

-- Manual failover to synchronous replica (no data loss)
ALTER AVAILABILITY GROUP [AG_Name] FAILOVER;

-- Forced failover (async replica — possible data loss; only if synchronous unavailable)
ALTER AVAILABILITY GROUP [AG_Name] FORCE_FAILOVER_ALLOW_DATA_LOSS;
```

## SQL Server — Failover Cluster Instance (FCI)

```powershell
# Check cluster node status
Get-ClusterNode

# Move SQL Server resource group to another node
Move-ClusterGroup -Name "SQL Server (MSSQLSERVER)" -Node <target-node>

# Verify
Get-ClusterGroup -Name "SQL Server (MSSQLSERVER)" | Select-Object Name, OwnerNode, State
```

## Post-Failover Validation

```bash
# Verify new primary accepting writes
psql -h <new-primary> -U appuser -c "INSERT INTO health_check(ts) VALUES (now());"
mysql -h <new-primary> -u appuser -e "INSERT INTO health_check(ts) VALUES(now());"

# Application connectivity
curl -sf https://<app-endpoint>/health && echo "OK"

# Check for open transactions / locks
# PostgreSQL
psql -c "SELECT pid, state, wait_event_type, query FROM pg_stat_activity WHERE state != 'idle';"
# SQL Server
SELECT session_id, blocking_session_id, wait_type, wait_time FROM sys.dm_exec_requests WHERE blocking_session_id != 0;
```

## Post-Failover Actions

1. Notify application teams: new primary host and connection string
2. Update DNS / load balancer / connection pool to point at new primary
3. Monitor for 30 min — error rate, query latency, connection count
4. Re-establish replication (old primary → new primary) once old primary recovers
5. Document failover in ITSM; link to root cause problem ticket

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Standby not promoting | Trigger file permissions / Patroni state | Check `pg_ctl promote` error; check Patroni logs |
| Split-brain (two primaries) | Both nodes think they are primary | Immediately fence the old primary; force-stop one; rebuild replication |
| High replication lag | Standby behind before failover | Assess data loss risk; decide to wait or accept data loss and proceed |
| Application can't connect after failover | DNS TTL / connection pool | Flush DNS cache; bounce connection pool; update app config |
