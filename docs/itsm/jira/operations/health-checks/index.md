---
tags:
  - jira
  - operations
description: "Health Checks reference covering Health Check Overview, 2. Log Review, 3. Disk Space, 4. Database Connectivity, 5. Search Index Status and 3 more sections."
---
# Jira — Health Checks

<div class="kb-summary">
Health Checks reference covering Health Check Overview, 2. Log Review, 3. Disk Space, 4. Database Connectivity, 5. Search Index Status and 3 more sections.

*Applies to: Jira 9.x / Cloud*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
health_check_overview: "Health Check Overview" {shape: rectangle}
run_this_routine: "Run This Routine" {shape: rectangle}
2_log_review: "2. Log Review" {shape: rectangle}
3_disk_space: "3. Disk Space" {shape: rectangle}
4_database_connectivity: "4. Database Connectivity" {shape: rectangle}
5_search_index_status: "5. Search Index Status" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> health_check_overview
health_check_overview -> run_this_routine
run_this_routine -> 2_log_review
2_log_review -> 3_disk_space
3_disk_space -> 4_database_connectivity
4_database_connectivity -> 5_search_index_status
5_search_index_status -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Health Check Overview

## Run This Routine

1. **Jira service status** — Run `systemctl status jira` on the app server; confirm the service is `active (running)`; if not, check the process list with `ps aux | grep jira` and review `catalina.out` for the last recorded error before attempting a restart.
2. **Jira URL health** — Run `curl -sk https://<jira-url>/status`; the response must contain `{"state":"RUNNING"}`; any other state (`STARTING`, `ERROR`, `STOPPING`) indicates Jira is not ready to serve users and requires immediate investigation.
3. **Database connection** — Navigate to **Jira Admin → System → Database → Connection Pool Monitoring**; confirm active connections are below 80% of the pool maximum and the wait count is zero; elevated wait counts indicate connection starvation which causes request queuing and slow page loads.
4. **Index integrity** — Navigate to **Jira Admin → System → Indexing**; confirm no reindex is currently in progress and the last reindex completed successfully; a stale index causes JQL searches to return incorrect or missing results.
5. **Disk space** — Run `df -h /var/atlassian/application-data/jira`; alert if the shared home volume exceeds 80%; also check the app node OS disk and log directory with `du -sh /opt/atlassian/jira/logs/`; attachments accumulate silently and are the most common cause of disk fills.
6. **Mail server** — Navigate to **Jira Admin → System → Outgoing Mail** and use the **Send a Test Email** function; confirm delivery; a failed outgoing mail server means all issue notification emails (assignments, comments, transitions) are queued but not delivered.
7. **Application log errors** — Run `tail -100 /var/atlassian/application-data/jira/log/atlassian-jira.log | grep -iE "error|exception" | tail -20`; review the output for patterns such as `OutOfMemoryError`, `Could not get JDBC Connection`, or `Index is corrupted`; each unique error pattern should be triaged and tracked.

Expected: All nodes show `healthy` / `UP`.

---

## 2. Log Review

### Log Locations

| Log File | Location | Purpose |
|---|---|---|
| Application log | `/opt/atlassian/jira/logs/atlassian-jira.log` | Main Jira application events |
| Catalina log | `/opt/atlassian/jira/logs/catalina.out` | JVM / Tomcat stdout |
| GC log | `/opt/atlassian/jira/logs/gc.log` | Garbage collection events |
| Access log | `/opt/atlassian/jira/logs/localhost_access_log.*.txt` | HTTP request log |
| Audit log | Jira Admin → Audit Log | Admin-action audit trail |

### Log Review Commands

```bash
# Check for ERROR/WARN in last hour
grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2} $(date +%H):" \
  /opt/atlassian/jira/logs/atlassian-jira.log \
  | grep -E "ERROR|WARN" | tail -50

# Check for OutOfMemoryError
grep -i "OutOfMemoryError\|Java heap space\|GC overhead" \
  /opt/atlassian/jira/logs/catalina.out | tail -20

# Check for slow queries
grep -i "slow query\|query took" \
  /opt/atlassian/jira/logs/atlassian-jira.log | tail -20

# Count errors in last 24h
grep "^$(date +%Y-%m-%d)" /opt/atlassian/jira/logs/atlassian-jira.log \
  | grep -c "ERROR"
```


```text title="Expected output"
2024-12-19 14:23:45,123 ERROR [http-nio-8080-exec-42] com.atlassian.jira.issue.search.SearchProvider - Error executing JQL query: Field 'customfield_10042' not found
2024-12-19 14:31:12,456 WARN [scheduler_Worker-2] com.atlassian.jira.service.ServiceManager - Service 'Mail Handler' took 8234ms to execute
2024-12-19 14:45:33,789 ERROR [http-nio-8080-exec-15] com.atlassian.crowd.manager.DirectoryManager - LDAP sync failed: Connection timeout after 30000ms
2024-12-19 14:52:01,234 WARN [http-nio-8080-exec-8] com.atlassian.jira.upgrade.UpgradeTaskManager - Pending upgrade task detected: com.atlassian.jira.upgrade.tasks.UpgradeTask_v8_13_0
2024-12-19 14:58:47,567 ERROR [scheduler_Worker-5] com.atlassian.jira.issue.index.IssueIndexManager - Reindex failed for project KEY-1234: java.io.IOException: Disk space low

2024-12-19 14:15:22.891 [GC (Allocation Failure) 2024-12-19T14:15:22.891+0000: 45.234: [ParNew: 524288K->65536K(589824K), 0.3456789 secs]
2024-12-19 14:42:11.567 [Full GC (System.gc()) 2024-12-19T14:42:11.567+0000: 892.123: [CMS: 1048576K->987654K(1048576K), 2.1234567 secs]

2024-12-19 14:33:44,123 INFO [http-nio-8080-exec-22] com.atlassian.jira.issue.search.SearchProvider - Query took 5432ms: project = PROJ AND status = Open
2024-12-19 14:51:09,456 WARN [http-nio-8080-exec-31] com.atlassian.jira.issue.search.SearchProvider - Slow query detected (8901ms): assignee = currentUser() AND updated >= -7d

342
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /opt/atlassian/jira/logs/atlassian-jira.log: No such file or directory` | Verify JIRA is installed at `/opt/atlassian/jira` or adjust the log path to match your installation directory. |
    | `grep: /opt/atlassian/jira/logs/catalina.out: Permission denied` | Run the command with `sudo` or ensure your user has read permissions on the Tomcat catalina logs. |
    | `date: invalid date format` | Ensure your system's `date` command supports `+%H` and `+%Y-%m-%d` format specifiers (standard on Linux/macOS). |
### Key Error Patterns

| Pattern | Severity | Meaning |
|---|---|---|
| `OutOfMemoryError: Java heap space` | Critical | JVM heap exhausted — increase Xmx or investigate leak |
| `OutOfMemoryError: Metaspace` | Critical | Metaspace exhausted — increase MaxMetaspaceSize |
| `Unable to acquire lock` | High | Distributed lock contention — check cluster health |
| `Could not get JDBC Connection` | High | DB connection pool exhausted |
| `Index is corrupted` | High | Lucene index corruption — reindex required |
| `LDAP: error code 49` | Medium | LDAP bind failure — check service account credentials |
| `SocketTimeoutException` | Medium | Network timeout — check external service connectivity |
| `com.hazelcast.*Exception` | Medium | Cluster communication issue |

---

## 3. Disk Space

```bash
# Check all relevant mount points
df -hT | grep -E "Filesystem|/var/atlassian|/opt/atlassian|/backup"

# Shared home breakdown
du -sh /var/atlassian/application-data/jira/shared/* | sort -hr | head -10

# Find large files
find /var/atlassian/application-data/jira/shared -type f -size +100M \
  | sort -t/ -k1 | head -20

# Log directory size
du -sh /opt/atlassian/jira/logs/
```


```text title="Expected output"
Filesystem     Type     Size  Used Avail Use% Mounted on
/dev/sda1      ext4     500G  385G  115G  77% /
/dev/sdb1      ext4     2.0T  1.8T  200G  90% /var/atlassian
/dev/sdc1      ext4     5.0T  3.2T  1.8T  64% /backup

847G	/var/atlassian/application-data/jira/shared
312G	/var/atlassian/application-data/jira/shared/plugins
156G	/var/atlassian/application-data/jira/shared/export
89G	/var/atlassian/application-data/jira/shared/attachments
34G	/var/atlassian/application-data/jira/shared/index
18G	/var/atlassian/application-data/jira/shared/analytics
12G	/var/atlassian/application-data/jira/shared/logos
8.4G	/var/atlassian/application-data/jira/shared/temp
2.1G	/var/atlassian/application-data/jira/shared/config
...

/var/atlassian/application-data/jira/shared/export/archive-2024-01-15.tar.gz	245M
/var/atlassian/application-data/jira/shared/attachments/proj-KEY-12847-image.zip	187M
/var/atlassian/application-data/jira/shared/plugins/marketplace-bundle-8.9.2.jar	156M
/var/atlassian/application-data/jira/shared/export/backup-full-2024-02-10.tar	134M
/var/atlassian/application-data/jira/shared/attachments/bulk-import-data.csv	118M

23G	/opt/atlassian/jira/logs/
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `find: '/var/atlassian/application-data/jira/shared': No such file or directory` | Verify JIRA installation path with `ls -la /var/atlassian/application-data/` and adjust the path if using a custom installation directory. |
    | `df: /var/atlassian: No such file or directory` | Mount the shared storage volume or check that `/var/atlassian` exists; confirm with `mount | grep atlassian`. |
    | `du: cannot access '/opt/atlassian/jira/logs/': Permission denied` | Run the command with `sudo` or ensure your user has read permissions on the logs directory with `sudo chmod o+rx /opt/atlassian/jira/logs/`. |
### Disk Usage Thresholds

| Mount Point | Warning | Critical | Action |
|---|---|---|---|
| Shared home | 70% | 85% | Archive old exports, purge temp files |
| App node OS disk | 75% | 90% | Rotate logs, clear temp |
| Database volume | 70% | 85% | Archive old audit data, extend volume |
| Backup storage | 80% | 90% | Delete old backups per retention policy |

---

## 4. Database Connectivity

```bash
# Test connection from app node
psql -h db.example.com -U jira -d jiradb -c "\conninfo"

# Check active connections
psql -h db.example.com -U jira -d jiradb \
  -c "SELECT count(*), state FROM pg_stat_activity WHERE datname='jiradb' GROUP BY state;"

# Check for long-running queries (> 30 seconds)
psql -h db.example.com -U jira -d jiradb -c "
SELECT pid, now() - query_start AS duration, state, query
FROM pg_stat_activity
WHERE datname = 'jiradb'
  AND state != 'idle'
  AND query_start < now() - interval '30 seconds'
ORDER BY duration DESC;"

# Check replication lag (if using replica)
psql -h db-replica.example.com -U jira -d jiradb \
  -c "SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"
```


```text title="Expected output"
You are connected to database "jiradb" as user "jira" via socket in "/var/run/postgresql" at port "5432".

 count | state  
-------+--------
    12 | active
    28 | idle
     3 | idle in transaction
(3 rows)

 pid  |   duration   | state  |                          query                           
------+--------------+--------+----------------------------------------------------------
 4521 | 00:01:45.234 | active | SELECT * FROM jira_issue WHERE updated > now() - interval
 4687 | 00:00:52.891 | active | UPDATE jira_worklog SET time_spent = $1 WHERE id = $2 AND
 4702 | 00:00:31.456 | active | INSERT INTO audit_log (event_type, timestamp) VALUES ($1,
(3 rows)

 replication_lag 
-----------------
 00:00:02.341
(1 row)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: could not translate host name "db.example.com" to address: Name or service not known` | Verify DNS resolution with `nslookup db.example.com` or update the hostname in your connection string to match your actual database server. |
    | `psql: error: FATAL: password authentication failed for user "jira"` | Confirm the jira user password is correct and check that the `.pgpass` file has the correct credentials in format `hostname:port:database:username:password`. |
    | `psql: error: FATAL: remaining connection slots are reserved for non-replication superuser connections` | Increase PostgreSQL's `max_connections` parameter or terminate idle connections with `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state='idle' AND query_start < now() - interval '10 minutes'`. |
### Connection Pool Health (via REST)

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/configuration" | python3 -m json.tool
```


```text title="Expected output"
{
  "baseUrl": "https://jira.company.internal",
  "version": "8.20.6",
  "versionNumbers": [
    8,
    20,
    6
  ],
  "deploymentType": "Server",
  "buildNumber": 820006,
  "buildDate": "2023-11-15T09:42:00.000-0500",
  "serverTime": "2024-01-18T14:32:47.123-0500",
  "scmInfo": "abc1d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9",
  "serverTitle": "JIRA Production",
  "licenseVersion": 2
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to jira.company.internal port 443: Connection refused` | Verify the JIRA_URL environment variable is correct and the JIRA instance is running and accessible from this host. |
    | `curl: (401) Unauthorized` | Ensure JIRA_USER and JIRA_TOKEN environment variables are set correctly and the API token has not expired. |
    | `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` | Check that the JIRA REST API endpoint is correct; the response may be HTML error page instead of JSON if the URL path is wrong. |
Via UI: `Admin → System → Database → Connection Pool Monitoring`

| Metric | Warning | Critical |
|---|---|---|
| Active connections | > 80% of pool max | > 95% of pool max |
| Wait count | > 0 persistent | > 5 for > 30s |
| Replication lag | > 30s | > 5 min |

---

## 5. Search Index Status

```bash
# Check index age via REST
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/reindex" | python3 -m json.tool
```


```text title="Expected output"
{
  "currentProgress": 87,
  "currentSubTask": "Indexing issues",
  "description": "Reindex in progress",
  "entityCount": 12847,
  "lastIndexTime": 1704067200000,
  "progressUrl": "/secure/admin/IndexAdmin.jspa?taskId=reindex-1",
  "remainingEstimate": "2m 34s",
  "startTime": 1704067140000,
  "status": "RUNNING"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to jira.example.com port 443: Connection refused` | Verify JIRA_URL is correct and the Jira instance is running and accessible from your network. |
    | `{"errorMessages":["User does not have permission to administer Jira"]}` | Ensure JIRA_USER has the Jira Administrators global permission or System Administrators group membership. |
    | `curl: (6) Could not resolve host: ${JIRA_URL}` | Check that JIRA_URL environment variable is set and contains a valid hostname (e.g., `export JIRA_URL=https://jira.example.com`). |
Expected response when healthy:

```json
{
  "progressUrl": "/rest/api/2/reindex/progress",
  "type": "BACKGROUND_PREFERRED",
  "submittedTime": "2026-05-08T01:00:00.000+0000",
  "startTime": "2026-05-08T01:00:05.000+0000",
  "finishTime": "2026-05-08T01:23:45.000+0000",
  "success": true,
  "currentSubTask": "Completed"
}
```

Check index size on disk:

```bash
du -sh /var/atlassian/application-data/jira/caches/indexes/
```


```text title="Expected output"
2.3G	/var/atlassian/application-data/jira/caches/indexes/
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `du: cannot access '/var/atlassian/application-data/jira/caches/indexes/': Permission denied` | Run the command with `sudo` or as the `jira` user to access the directory. |
    | `du: cannot access '/var/atlassian/application-data/jira/caches/indexes/': No such file or directory` | Verify the JIRA installation path matches your environment; check `$JIRA_HOME` or review the JIRA installation documentation for your version. |
Signs of index problems:

- JQL searches returning 0 results for known issues
- `Index is corrupted` in logs
- Reindex progress stuck at same percentage for > 30 minutes

---

## 6. Cluster Node Status

```bash
# Database-level cluster check
psql -h db.example.com -U jira -d jiradb -c "
SELECT node_id, node_name, status, ip, last_heartbeat,
       EXTRACT(EPOCH FROM (now() - last_heartbeat)) AS seconds_since_heartbeat
FROM clusternodeinfo
ORDER BY last_heartbeat DESC;"
```


```text title="Expected output"
node_id | node_name | status |      ip      |       last_heartbeat       | seconds_since_heartbeat
---------+-----------+--------+--------------+----------------------------+-------------------------
       1 | jira-node-01 | ONLINE | 10.42.18.105 | 2024-01-15 14:23:47.234561 |                       2.1
       2 | jira-node-02 | ONLINE | 10.42.18.106 | 2024-01-15 14:23:45.891234 |                       4.4
       3 | jira-node-03 | ONLINE | 10.42.18.107 | 2024-01-15 14:23:46.567890 |                       3.7
       4 | jira-node-04 | OFFLINE | 10.42.18.108 | 2024-01-15 14:18:12.123456 |                     335.8
(4 rows)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: FATAL: Ident authentication failed for user "jira"` | Verify the `.pgpass` file exists at `~/.pgpass` with correct credentials and permissions (chmod 600), or use password prompt with `-W` flag. |
    | `psql: error: could not translate host name "db.example.com" to address: Name or service not known` | Confirm the database hostname is correct and resolvable by running `nslookup db.example.com` or checking your `/etc/hosts` file. |
    | `ERROR: relation "clusternodeinfo" does not exist` | Verify you are connected to the correct JIRA database and the table name matches your JIRA version (may be `jiraclusternode` in older versions). |
Via UI: `Admin → System → Clustering`

All expected nodes should appear with:
- Status: `ACTIVE`
- Last heartbeat: < 60 seconds ago

Via REST:

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/cluster/nodes" | python3 -m json.tool
```


```text title="Expected output"
{
  "nodes": [
    {
      "nodeId": "node-001",
      "name": "jira-prod-01.internal",
      "state": "ACTIVE",
      "buildNumber": 100156,
      "version": "8.20.11",
      "ipAddress": "10.42.18.45"
    },
    {
      "nodeId": "node-002",
      "name": "jira-prod-02.internal",
      "state": "ACTIVE",
      "buildNumber": 100156,
      "version": "8.20.11",
      "ipAddress": "10.42.18.46"
    },
    {
      "nodeId": "node-003",
      "name": "jira-prod-03.internal",
      "state": "OFFLINE",
      "buildNumber": 100156,
      "version": "8.20.11",
      "ipAddress": "10.42.18.47"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to jira.example.com port 443: Connection refused` | Verify the JIRA_URL environment variable is correct and the Jira instance is running and accessible from your network. |
    | `401 Unauthorized` | Ensure JIRA_USER and JIRA_TOKEN environment variables are set correctly and the API token has not expired. |
    | `json.decoder.JSONDecodeError: Expecting value: line 1 column 1` | Check that the Jira REST API endpoint is correct; the response may be HTML error page instead of JSON if the URL path is wrong. |
---

## 7. Key Metrics Reference

| Metric | Healthy | Warning | Critical | Source |
|---|---|---|---|---|
| HTTP response time (P95) | < 1s | 1–3s | > 3s | LB metrics / APM |
| JVM heap usage | < 70% | 70–85% | > 85% | JMX / `jstat` |
| JVM GC pause (P99) | < 200ms | 200–500ms | > 500ms | GC log |
| DB connection pool used | < 70% | 70–90% | > 90% | Jira admin |
| DB query time (P95) | < 100ms | 100–500ms | > 500ms | pg_stat_statements |
| Disk usage (shared home) | < 70% | 70–85% | > 85% | `df` |
| Cluster heartbeat age | < 30s | 30–60s | > 60s | DB clusternodeinfo |
| Replication lag | < 5s | 5–30s | > 30s | PostgreSQL |
| Active Jira threads | < 100 | 100–200 | > 200 | Thread dump / JMX |
| Error log rate (/hour) | < 10 | 10–100 | > 100 | Log grep |
| Failed logins (/hour) | < 5 | 5–50 | > 50 | Audit log |

---

## 8. Automated Health Check Script

```bash
#!/bin/bash
# jira-health-check.sh — Run daily via cron

JIRA_URL="https://jira.example.com"
JIRA_USER="health-check-svc"
JIRA_TOKEN="${JIRA_HEALTH_TOKEN}"
ALERT_EMAIL="ops-team@example.com"
FAILURES=()

# --- 1. HTTP health endpoint ---
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${JIRA_URL}/status")
if [ "${STATUS}" != "200" ]; then
  FAILURES+=("Jira health endpoint returned HTTP ${STATUS}")
fi

# --- 2. Disk space ---
DISK_PCT=$(df /var/atlassian/application-data/jira/shared \
  | awk 'NR==2{print $5}' | tr -d '%')
if [ "${DISK_PCT}" -gt 85 ]; then
  FAILURES+=("Shared home disk usage at ${DISK_PCT}% — CRITICAL")
elif [ "${DISK_PCT}" -gt 70 ]; then
  FAILURES+=("Shared home disk usage at ${DISK_PCT}% — WARNING")
fi

# --- 3. DB connectivity ---
if ! psql -h db.example.com -U jira -d jiradb -c "SELECT 1" -q > /dev/null 2>&1; then
  FAILURES+=("PostgreSQL connection failed")
fi

# --- 4. Error log check ---
ERROR_COUNT=$(grep "^$(date +%Y-%m-%d)" \
  /opt/atlassian/jira/logs/atlassian-jira.log \
  | grep -c "ERROR" || true)
if [ "${ERROR_COUNT}" -gt 100 ]; then
  FAILURES+=("High error rate: ${ERROR_COUNT} errors today")
fi

# --- 5. Cluster node heartbeat ---
STALE_NODES=$(psql -h db.example.com -U jira -d jiradb -tAc "
  SELECT count(*) FROM clusternodeinfo
  WHERE status = 'ACTIVE'
    AND last_heartbeat < now() - interval '2 minutes'")
if [ "${STALE_NODES}" -gt 0 ]; then
  FAILURES+=("${STALE_NODES} cluster node(s) have stale heartbeat")
fi

# --- Report ---
if [ ${#FAILURES[@]} -gt 0 ]; then
  BODY=$(printf '%s\n' "${FAILURES[@]}")
  echo "${BODY}" | mail -s "[JIRA HEALTH] $(hostname) — $(date)" "${ALERT_EMAIL}"
  echo "HEALTH CHECK FAILED:"
  printf '  - %s\n' "${FAILURES[@]}"
  exit 1
else
  echo "Health check passed: $(date)"
  exit 0
fi
```


```text title="Expected output"
Health check passed: Wed Jan 15 02:30:45 UTC 2025
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: connection to server at "db.example.com" (10.42.8.15), port 5432 failed: Connection refused` | Verify PostgreSQL is running on db.example.com and the network route is accessible; check `psql -h db.example.com -U jira -d jiradb -c "SELECT 1"` manually. |
    | `grep: /opt/atlassian/jira/logs/atlassian-jira.log: No such file or directory` | Confirm the Jira installation path and log file location match your deployment; adjust the path in the script or verify the Jira service is running. |
    | `curl: (7) Failed to connect to jira.example.com port 443: Connection timed out` | Check that the JIRA_URL is correct, the Jira service is running, and firewall/network rules allow outbound HTTPS from the monitoring host. |
Schedule:

```cron
*/15 * * * * jira /opt/scripts/jira-health-check.sh >> /var/log/jira-health.log 2>&1
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Jira — Procedures](../procedures/)
- [Jira — CLI Reference](../cli-reference/)
- [Jira — Common Issues](../../troubleshooting/common-issues/)
