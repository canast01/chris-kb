---
tags:
  - confluence
  - operations
description: "This page defines the daily health check procedure for Confluence Data Center. Run these checks as part of a morning operational routine or automate them..."
---
# Confluence — Health Checks

<div class="kb-summary">
This page defines the daily health check procedure for Confluence Data Center. Run these checks as part of a morning operational routine or automate them with a monitoring script.

*Applies to: Confluence Cloud / Data Center*
</div>

---

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
health_check_flow: "Health Check Flow" {shape: rectangle}
run_this_routine: "Run This Routine" {shape: rectangle}
2_log_checks: "2. Log Checks" {shape: rectangle}
3_disk_space: "3. Disk Space" {shape: rectangle}
4_database_connectivity_and_latency: "4. Database Connectivity and Latency" {shape: rectangle}
5_search_index_status: "5. Search Index Status" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> health_check_flow
health_check_flow -> run_this_routine
run_this_routine -> 2_log_checks
2_log_checks -> 3_disk_space
3_disk_space -> 4_database_connectivity_and_latency
4_database_connectivity_and_latency -> 5_search_index_status
5_search_index_status -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Health Check Flow

## Run This Routine

1. **Confluence service status** — On Linux run `systemctl status confluence`; on Windows run `net start | findstr /i confluence`; the service must be active and running; if stopped, check `catalina.out` for the last error before restarting.
2. **Cluster health (Data Center)** — Navigate to **Confluence Admin → General Configuration → Clustering**; confirm all expected nodes appear with state `ACTIVE`; a missing or `OFFLINE` node means the cluster is degraded and failover capacity is reduced.
3. **Database connectivity** — Navigate to **Confluence Admin → General Configuration → Troubleshooting and Support → System Information**; confirm the database connection pool shows active connections and no pool exhaustion; alternatively check via `psql -U confluence -d confluencedb -c "SELECT 1;"` from the app server.
4. **Index status** — Navigate to **Confluence Admin → General Configuration → Content Indexing**; confirm the index state is not currently rebuilding and the queue depth is near zero; a persistently growing queue or a stuck reindex will cause search results to be stale or unavailable.
5. **Disk space** — Run `df -h /var/atlassian/application-data/confluence` and also check the shared home mount if Data Center; alert if any volume exceeds 80%; the shared home fills gradually with attachments and backups and is the most common cause of disk-related outages.
6. **Mail server** — Navigate to **Confluence Admin → Mail Servers** and use the **Send Test Email** function; confirm the test email is received; a failing mail server means all Confluence notifications (page watches, mentions, space admin alerts) are silently dropped.
7. **Recent errors** — Run `tail -100 /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | grep -i error`; review any error lines for patterns such as `OutOfMemoryError`, `Could not get JDBC Connection`, or `LuceneIndex`; recurring errors should be opened as incidents rather than ignored.

Response states:

| State | Meaning |
|---|---|
| `RUNNING` | Fully operational |
| `STARTING` | Startup in progress (wait) |
| `STOPPING` | Shutdown in progress |
| `ERROR` | Failed — check logs immediately |
| `FIRST_RUN` | Awaiting setup wizard |

---

## 2. Log Checks

### Log Locations

| Log File | Purpose |
|---|---|
| `<CONFLUENCE_HOME>/logs/atlassian-confluence.log` | Main application log |
| `<INSTALL>/logs/catalina.out` | Tomcat stdout / JVM output |
| `<CONFLUENCE_HOME>/logs/atlassian-confluence-security.log` | Authentication events |
| `<CONFLUENCE_HOME>/logs/atlassian-confluence-index-recovery.log` | Index recovery events |

### Quick Error Scan

```bash
LOG="/var/atlassian/application-data/confluence/logs/atlassian-confluence.log"

# Count errors in the last 24 hours (assumes log rotation daily)
grep -c "ERROR" "$LOG"

# Show the last 20 error lines with timestamp
grep "ERROR" "$LOG" | tail -20

# Look for OOM indicators
grep -E "(OutOfMemoryError|java.lang.OutOfMemory)" "$LOG" | tail -5

# Check for LDAP/login failures
grep -E "(AuthenticationException|CrowdException|LDAP)" "$LOG" | tail -10

# Check for index errors
grep -E "(IndexException|LuceneIndex|index corrupt)" "$LOG" | tail -10
```


```text title="Expected output"
247
2024-01-15 14:32:18,445 ERROR [http-nio-8090-exec-12] com.atlassian.confluence.core.ContentEntityManager - Failed to retrieve page content for space key: PROJ
2024-01-15 14:28:05,221 ERROR [scheduler-3] com.atlassian.confluence.search.v2.ContentIndexer - Error indexing document ID: 12847
2024-01-15 14:15:43,887 ERROR [http-nio-8090-exec-8] com.atlassian.crowd.manager.authentication.AuthenticationManager - Authentication failed for user: jsmith@example.com
2024-01-15 14:02:19,556 ERROR [pool-4-thread-1] com.atlassian.confluence.mail.notification.NotificationQueueProcessor - Mail delivery failed: Connection timeout
2024-01-15 13:58:12,334 ERROR [http-nio-8090-exec-15] com.atlassian.confluence.pages.actions.ViewPageAction - Page rendering exception for pageId: 98765
2024-01-15 13:45:01,112 ERROR [scheduler-1] com.atlassian.confluence.core.persistence.hibernate.HibernateContentDao - Database connection pool exhausted
2024-01-15 13:32:47,998 ERROR [http-nio-8090-exec-22] com.atlassian.confluence.search.v2.ContentIndexer - Lucene index write lock timeout
2024-01-15 13:18:33,445 ERROR [pool-2-thread-3] com.atlassian.confluence.core.ContentEntityManager - Failed to serialize page object
2024-01-15 13:05:22,667 ERROR [http-nio-8090-exec-5] com.atlassian.confluence.security.PermissionManager - Permission check failed for user: alee
2024-01-15 12:52:11,889 ERROR [scheduler-2] com.atlassian.confluence.mail.notification.NotificationQueueProcessor - SMTP server unreachable: mail.corp.local
(no output — no OutOfMemoryError found in recent logs)
2024-01-15 14:15:43,887 ERROR [http-nio-8090-exec-8] com.atlassian.crowd.manager.authentication.AuthenticationManager - Authentication failed for user: jsmith@example.com
2024-01-15 13:42:19,334 ERROR [http-nio-8090-exec-14] com.atlassian.confluence.security.ldap.LdapUserDirectory - LDAP connection refused: ldap://directory.corp.local:389
2024-01-15 12:28:56,112 ERROR [pool-1-thread-2] com.atlassian.crowd.manager.directory.DirectoryManager - CrowdException: Directory sync failed
2024-01-15 11:15:33,998 ERROR [http-nio-8090-exec-19] com.atlassian.confluence.security.ldap.LdapUserDirectory - LDAP bind failed: Invalid credentials for service account
2024-01-15 10:02:44,556 ERROR [scheduler-4] com.atlassian.confluence.security.ldap.Ld
```
---

## 3. Disk Space

```bash
#!/bin/bash
# confluence-disk-check.sh

WARN_THRESHOLD=80
CRIT_THRESHOLD=90
INSTALL_DIR="/opt/atlassian/confluence"
HOME_DIR="/var/atlassian/application-data/confluence"
SHARED_HOME="/mnt/confluence-shared"

check_disk() {
  local path="$1"
  local label="$2"
  local pct
  pct=$(df -h "$path" | awk 'NR==2 {gsub(/%/,"",$5); print $5}')
  if [ "$pct" -ge "$CRIT_THRESHOLD" ]; then
    echo "CRITICAL: $label at ${pct}% ($path)"
  elif [ "$pct" -ge "$WARN_THRESHOLD" ]; then
    echo "WARNING: $label at ${pct}% ($path)"
  else
    echo "OK: $label at ${pct}% ($path)"
  fi
}

check_disk "$INSTALL_DIR"  "Install directory"
check_disk "$HOME_DIR"     "Local home"
check_disk "$SHARED_HOME"  "Shared home (attachments/index)"

# Show largest directories under shared home
echo ""
echo "Top 10 directories in shared home:"
du -sh "${SHARED_HOME}/"* 2>/dev/null | sort -rh | head -10
```


```text title="Expected output"
OK: Install directory at 45% (/opt/atlassian/confluence)
OK: Local home at 62% (/var/atlassian/application-data/confluence)
WARNING: Shared home at 82% (/mnt/confluence-shared)

Top 10 directories in shared home:
18G	/mnt/confluence-shared/attachments
12G	/mnt/confluence-shared/index
4.2G	/mnt/confluence-shared/backups
2.1G	/mnt/confluence-shared/thumbnails
890M	/mnt/confluence-shared/temp
340M	/mnt/confluence-shared/analytics-logs
120M	/mnt/confluence-shared/plugins
45M	/mnt/confluence-shared/export
```

!!! warning "Common errors"
    **`df: '/mnt/confluence-shared': No such file or directory`** — Verify the shared home mount point exists and is mounted with `mount | grep confluence-shared`.
    **`awk: syntax error in regex at or near `%'`** — Ensure the df output format is standard; run `df -h /opt/atlassian/confluence` manually to confirm column 5 contains the percentage value.
    **`du: cannot access '/mnt/confluence-shared/*': Permission denied`** — Run the script with sudo or ensure the executing user has read permissions on the shared home directory.
---

## 4. Database Connectivity and Latency

### Connectivity Test

```bash
# PostgreSQL connectivity from app server
psql -h db.internal.example.com -U confluence -d confluencedb \
  -c "SELECT version();" 2>&1 | grep -E "(PostgreSQL|error|FATAL)"

# Connection count (compare to max_connections)
psql -h db.internal.example.com -U confluence -d confluencedb \
  -c "SELECT count(*) AS active_connections FROM pg_stat_activity WHERE state = 'active';"

# Check max connections setting
psql -h db.internal.example.com -U confluence -d confluencedb \
  -c "SHOW max_connections;"
```


```text title="Expected output"
PostgreSQL 12.14 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 9.3.0, 64-bit
 active_connections
──────────────────
                 42
(1 row)

 max_connections
─────────────────
             200
(1 row)
```

!!! warning "Common errors"
    **`psql: error: could not translate host name "db.internal.example.com" to address: Name or service not known`** — Verify DNS resolution with `nslookup db.internal.example.com` and confirm the hostname is correct in your network configuration.
    
    **`psql: error: FATAL: password authentication failed for user "confluence"`** — Check that the confluence database user password is correct and that the `.pgpass` file (if used) has the right credentials with permissions set to 0600.
    
    **`psql: error: FATAL: remaining connection slots are reserved for non-replication superuser connections`** — Increase the `max_connections` parameter in postgresql.conf and restart PostgreSQL, or reduce active connections by terminating idle sessions.
### Latency Test

```bash
# Simple query latency measurement
time psql -h db.internal.example.com -U confluence -d confluencedb \
  -c "SELECT id, title FROM content WHERE contenttype = 'PAGE' LIMIT 100;" \
  > /dev/null
```


```text title="Expected output"
id  |                           title                            
-----+------------------------------------------------------------
 123 | Home
 124 | Getting Started with Confluence
 125 | Team Processes
 126 | Infrastructure Guidelines
 127 | Disaster Recovery Plan
 128 | API Documentation
 129 | Security Policies
...
(100 rows)

real	0m1.247s
user	0m0.156s
sys	0m0.032s
```

!!! warning "Common errors"
    **`psql: error: could not translate host name "db.internal.example.com" to address: Name or service not known`** — Verify DNS resolution with `ndig db.internal.example.com` or update the hostname to match your actual database server FQDN.
    **`psql: error: FATAL: password authentication failed for user "confluence"`** — Confirm the confluence user password is correct and check that the `.pgpass` file exists with proper permissions (`chmod 600 ~/.pgpass`) or use the `-W` flag to prompt for password.
    **`psql: error: FATAL: database "confluencedb" does not exist`** — Connect to the postgres database first with `-d postgres` and run `\l` to list available databases, then use the correct database name.
| Metric | OK | Warning | Critical |
|---|---|---|---|
| DB connect time | < 100 ms | 100–500 ms | > 500 ms |
| Simple query time | < 200 ms | 200 ms–1 s | > 1 s |
| Active connections | < 70% of max | 70–90% of max | > 90% of max |

---

## 5. Search Index Status

```bash
# REST API — check indexing queue size
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/search/index" | jq '.'

# Admin UI equivalents:
# Admin > General Configuration > Content Indexing
# Admin > General Configuration > Troubleshooting and Support > Index Tracker
```


```text title="Expected output"
{
  "indexQueueSize": 0,
  "indexingEnabled": true,
  "lastIndexTime": "2024-01-15T09:47:32.521Z",
  "indexedContentCount": 18547,
  "pendingUpdates": 0,
  "indexVersion": "8.7.2",
  "status": "IDLE"
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify the Confluence hostname is correct and the instance is running with `curl -I https://confluence.example.com`.
    **`jq: parse error: Invalid JSON text at line 1`** — Check that `$CF_TOKEN` is valid and has API permissions by testing with `curl -s -H "Authorization: Bearer $CF_TOKEN" "https://confluence.example.com/rest/api/user/current" | jq '.'`.
    **`{"statusCode":401,"message":"Unauthorized"}`** — Regenerate the API token in Confluence (Settings > Personal > API tokens) and re-export it as `export CF_TOKEN="your_new_token"`.
Via the admin console, check:

- **Index state**: Should be `CONNECTED` or `NORMAL`
- **Queue size**: Should be near 0 during off-peak; a persistently growing queue indicates the indexer is falling behind
- **Last reindex time**: Should match the last content modification time

### Trigger a Re-index (if needed)

```bash
# Trigger re-indexing via REST
curl -s -X POST -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/search/index/reindex"
```


```text title="Expected output"
{"status":"reindexing","taskId":"task-7f3a9c2e-1b4d-4a8f-9e2c-5d6a1f8b3c4e","message":"Reindexing started successfully","estimatedDuration":"45 minutes"}
```

!!! warning "Common errors"
    **`{"error":"Unauthorized","statusCode":401}`** — Verify the `CF_TOKEN` environment variable is set and contains a valid bearer token with admin permissions.
    **`{"error":"Forbidden","statusCode":403}`** — Ensure the token's associated user account has the "Confluence Administrator" global permission.
    **`curl: (6) Could not resolve host: confluence.example.com`** — Replace `confluence.example.com` with your actual Confluence instance hostname and verify network connectivity.
---

## 6. Cluster Node Status (Data Center)

```bash
# Admin UI: Admin > General Configuration > Clustering

# REST API — cluster node info
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/cluster/nodes" | jq '.'

# Expected output structure:
# {
#   "nodes": [
#     { "id": "...", "address": "10.0.1.11", "state": "ACTIVE", "version": "8.5.4" },
#     { "id": "...", "address": "10.0.1.12", "state": "ACTIVE", "version": "8.5.4" },
#     { "id": "...", "address": "10.0.1.13", "state": "ACTIVE", "version": "8.5.4" }
#   ]
# }
```


```text title="Expected output"
{
  "nodes": [
    {
      "id": "node-a1b2c3d4e5f6",
      "address": "10.0.1.11",
      "state": "ACTIVE",
      "version": "8.5.4"
    },
    {
      "id": "node-f6e5d4c3b2a1",
      "address": "10.0.1.12",
      "state": "ACTIVE",
      "version": "8.5.4"
    },
    {
      "id": "node-9x8y7z6w5v4u",
      "address": "10.0.1.13",
      "state": "ACTIVE",
      "version": "8.5.4"
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify the Confluence server is running and accessible at the specified hostname/port.
    **`{"statusCode":401,"message":"Unauthorized"}`** — Ensure the CF_TOKEN environment variable is set to a valid API token with cluster admin permissions.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl to skip SSL verification, or configure proper certificates in your Confluence instance.
Cluster checks:

| Check | Expected | Alert If |
|---|---|---|
| All nodes present | N nodes active | Any node absent |
| Hazelcast membership | N members | Member count < N |
| Node version | All identical | Version mismatch |
| Cache sync status | In sync | Drift > 1 min |

### Hazelcast Port Connectivity

```bash
# From node-2, verify port 5801 is reachable on node-1
nc -zv 10.0.1.11 5801 && echo "OK" || echo "FAIL"
```


```text title="Expected output"
Connection to 10.0.1.11 5801 port [tcp/*] succeeded!
OK
```

!!! warning "Common errors"
    **`nc: connect to 10.0.1.11 port 5801 (tcp) failed: Connection refused`** — Verify the service listening on port 5801 is running on node-1 with `systemctl status <service-name>`.
    **`nc: getaddrinfo for host "10.0.1.11" port 5801 failed: Name or service not known`** — Confirm the IP address 10.0.1.11 is correct and reachable by pinging it first: `ping -c 1 10.0.1.11`.
    **`nc: connect to 10.0.1.11 port 5801 (tcp) failed: No route to host`** — Check network connectivity and firewall rules between node-2 and node-1; verify the route exists with `ip route show`.
---

## 7. Scheduled Jobs

**Admin > General Configuration > Scheduled Jobs**

Jobs to verify are not failing:

| Job | Default Schedule | Failure Impact |
|---|---|---|
| Send Batch Notification Email | Every 10 min | Delayed email notifications |
| Flush Edit Sessions | Every 30 min | Stale collaborative edits |
| Clean Temporary Directory | Daily 01:00 | Disk fill up |
| Storage Optimisation | Weekly | Increased DB/attachment storage |
| Cluster Safety Check | Every 5 min (DC) | Split-brain risk undetected |

---

## Key Metrics Reference Table

| Metric | Collection Method | Healthy Range | Action if Breached |
|---|---|---|---|
| JVM heap used | JMX / `/status` endpoint | < 80% Xmx | Increase heap or tune |
| GC pause time | GC log / JMX | < 500 ms | Tune G1GC settings |
| HTTP response time | Synthetic monitor | < 3 s (page load) | Investigate DB / plugin |
| DB active connections | `pg_stat_activity` | < 70% of max_connections | Increase pool or max_conn |
| Disk usage (shared home) | `df -h` | < 80% | Archive old content, expand vol |
| Index queue depth | Admin UI | 0–10 (off-peak) | Trigger re-index |
| Cluster nodes active | Admin > Clustering | = expected node count | Investigate offline node |
| Error rate in log | `grep -c ERROR` | 0–5 / hour | Triage each error |
| Mail queue depth | Admin > Mail | 0 (queue clears) | Check SMTP connectivity |

---

## Health Check Script (Automated)

```bash
#!/bin/bash
# confluence-healthcheck.sh — run via cron, output to log / alerting system

CF_URL="https://confluence.example.com"
CF_TOKEN="<PAT>"
REPORT="/var/log/confluence-health-$(date +%Y%m%d).log"
FAILURES=0

check() {
  local label="$1"
  local result="$2"
  local expected="$3"
  if [[ "$result" == *"$expected"* ]]; then
    echo "OK  | $label" | tee -a "$REPORT"
  else
    echo "FAIL| $label — got: $result" | tee -a "$REPORT"
    ((FAILURES++))
  fi
}

# 1. HTTP status
status=$(curl -sf "${CF_URL}/status" | jq -r '.state' 2>/dev/null)
check "HTTP status" "$status" "RUNNING"

# 2. Disk space
disk_pct=$(df /mnt/confluence-shared | awk 'NR==2 {gsub(/%/,"",$5); print $5}')
[ "$disk_pct" -lt 80 ] && check "Disk space (shared home)" "OK" "OK" \
  || check "Disk space (shared home)" "FAIL (${disk_pct}%)" "OK"

# 3. DB connectivity
db_ok=$(psql -h db.internal.example.com -U confluence -d confluencedb \
  -c "SELECT 1;" -t 2>&1 | grep -c "1")
[ "$db_ok" -eq 1 ] && check "DB connectivity" "OK" "OK" \
  || check "DB connectivity" "FAIL" "OK"

# 4. Error count in log
error_count=$(grep -c "ERROR" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log 2>/dev/null)
[ "$error_count" -lt 10 ] && check "Log error count" "OK (${error_count})" "OK" \
  || check "Log error count" "FAIL (${error_count} errors)" "OK"

echo "---" | tee -a "$REPORT"
echo "Health check complete. Failures: $FAILURES" | tee -a "$REPORT"

# Exit non-zero so cron / monitoring detects failures
exit $FAILURES
```


```text title="Expected output"
OK  | HTTP status
OK  | Disk space (shared home)
OK  | DB connectivity
OK  | Log error count (7)
---
Health check complete. Failures: 0
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443`** — Verify CF_URL is correct and Confluence is running; check network connectivity with `ping confluence.example.com`.
    **`psql: error: connection to server at "db.internal.example.com" (10.42.1.15), port 5432 failed`** — Ensure the PostgreSQL host is reachable, credentials in the psql command are correct, and the database user has login privileges.
    **`jq: parse error: Invalid JSON text at line 1`** — Confirm the `/status` endpoint returns valid JSON; test manually with `curl -sf "${CF_URL}/status" | jq .` to see the actual response.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Confluence — Procedures](../procedures/)
- [Confluence — CLI Reference](../cli-reference/)
- [Confluence — Common Issues](../../troubleshooting/common-issues/)
