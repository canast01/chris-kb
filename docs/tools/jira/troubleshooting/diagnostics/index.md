# Jira — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Diagnostic Flow, JVM Heap Analysis, Thread Dump Capture and Analysis, Database Slow Query Analysis, Support ZIP Collection and 1 more sections.
</div>

## Diagnostic Flow

```mermaid
flowchart TD
    ISSUE([Issue Reported]) --> BASIC[Collect Basic Info\nversion, error message, affected users]

    BASIC --> LOGS[Review Application Logs\natlassian-jira.log, catalina.out]

    LOGS --> LOG_FINDING{Error found\nin logs?}

    LOG_FINDING -- Yes --> CLASSIFY{Error type?}
    LOG_FINDING -- No --> HTTP[Check HTTP\nResponse Times]

    CLASSIFY -- OOM/Heap --> HEAP[JVM Heap Analysis\njmap / heap dump]
    CLASSIFY -- Thread deadlock/hang --> THREAD[Thread Dump\nAnalysis]
    CLASSIFY -- DB error --> DB[Database Diagnostics\npg_stat_activity, slow queries]
    CLASSIFY -- Plugin error --> PLUGIN[Plugin Diagnostics\nDisable/enable, cache clear]

    HTTP --> HTTP_SLOW{Response\n> 3s?}
    HTTP_SLOW -- Yes --> PROFILE[DB slow query log\nJVM profiling]
    HTTP_SLOW -- No --> CLUSTER[Check Cluster\nHeartbeat & Hazelcast]

    HEAP --> ANALYSE[Analyse with MAT\nIdentify leak]
    THREAD --> DEADLOCK{Deadlock\ndetected?}
    DEADLOCK -- Yes --> RESTART[Restart affected node\nCapture support.zip]
    DEADLOCK -- No --> POOL[Check thread pool\nconfiguration]
    DB --> FIX_DB[Resolve DB issue\nkill long queries, tune config]
    PLUGIN --> FIX_PLUGIN[Update or remove\noffending plugin]
    PROFILE --> FIX_PERF[Add indexes, optimise JQL\nincrease resources]
    CLUSTER --> FIX_CLUSTER[Investigate network\nrestart node]

    ANALYSE --> SUPPORT{Issue resolved?}
    RESTART --> SUPPORT
    FIX_DB --> SUPPORT
    FIX_PLUGIN --> SUPPORT
    FIX_PERF --> SUPPORT
    FIX_CLUSTER --> SUPPORT

    SUPPORT -- No --> ESCALATE[Collect support.zip\nEscalate to L3/Atlassian]
    SUPPORT -- Yes --> DONE([Resolved — Document RCA])

    style DONE fill:#2d8a4e,color:#fff
    style ESCALATE fill:#c0392b,color:#fff
```
```text
┌───────────────────────────────────────── Jira — Diagnostics ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    Jira Diagnostic Runbook                                    │   │
│   │            Step 1: curl -s http://localhost:8080/status — confirm state is RUNNING            │   │
│   │                 Step 2: grep -i "ERROR|OOM|Exception" catalina.out | tail -100                │   │
│   │              Step 3: psql -U jira -c "SELECT count(*) FROM jiraissue;" — DB alive             │   │
│   │             Step 4: df -h $JIRA_HOME — check disk; ls $JIRA_HOME/data/attachments             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Stop at first anomaly and remediate before continuing to next diagnostic step                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Application Diagnostics            │  │             Infrastructure Diag             │   │
│   │            curl /status endpoint             │  │               df -h JIRA_HOME               │   │
│   │              grep catalina.out               │  │               mount | grep nfs              │   │
│   │             Thread dump: kill -3             │  │               pg_stat_activity              │   │
│   │              Heap: jmap -histo               │  │              netstat open ports             │   │
│   │             Admin > System Info              │  │                top / free -h                │   │
│   │              support-zip export              │  │              journalctl -u jira             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SSH to Jira VMs · PostgreSQL admin access · NFS mount visibility                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  kill -3 PID    = sends SIGQUIT to JVM; thread dump printed to catalina.out                           │
│  jmap -histo    = histogram of JVM heap; lists top objects by class name                              │
│  pg_stat_activity = PostgreSQL running queries; find blocking and long-running SQL                    │
│  catalina.out   = Tomcat stdout log; JIRA_INSTALL/logs/catalina.out                                   │
│  atlassian-jira.log = Jira application log; JIRA_HOME/log/atlassian-jira.log                          │
│  support-zip    = Admin > System > Troubleshooting; bundles logs and thread dumps                     │
│  top            = real-time process monitor; watch java process CPU and memory                        │
│  netstat        = open port check; confirm 8080 (Jira) and 5432 (PG) listening                        │
│  mount          = list mounted filesystems; verify NFS home mount present                             │
│  journalctl     = systemd log reader; use if Jira runs as systemd service                             │
│  free -h        = system memory; check if OS is swapping under memory pressure                        │
│  df -h          = disk usage; alert if JIRA_HOME volume exceeds 80% full                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

---

## JVM Heap Analysis

### Check Live Heap Usage

```bash
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)

# Heap summary
jcmd "${JIRA_PID}" GC.heap_info

# Histogram of object types by memory (top 30)
jmap -histo:live "${JIRA_PID}" | head -35

# Configured heap limits
jcmd "${JIRA_PID}" VM.flags | grep -E "HeapSize|Xmx|Xms"
```

### Capture Heap Dump

```bash
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)
DUMP_FILE="/tmp/jira-heap-$(date +%Y%m%d-%H%M%S).hprof"

# Live objects only (reduces dump size, most useful for leak analysis)
sudo -u jira jmap -dump:format=b,live,file="${DUMP_FILE}" "${JIRA_PID}"

echo "Heap dump: ${DUMP_FILE} ($(du -sh ${DUMP_FILE} | cut -f1))"
```

### Analyse with Eclipse MAT

1. Download [Eclipse Memory Analyser Tool (MAT)](https://eclipse.dev/mat/)
2. Open the `.hprof` file
3. Run **Leak Suspects Report**
4. Look for classes with large retained heap (> 20% of total)
5. Common Jira leak sources:
   - `JiraIssue` cache not evicting
   - Plugin holding references to closed sessions
   - Lucene IndexSearcher not closed
   - Scheduled tasks accumulating results

### GC Log Analysis

```bash
GC_LOG=/opt/atlassian/jira/logs/gc.log

# Count full GC events (expensive, stop-the-world)
grep -c "Pause Full" "${GC_LOG}"

# Show full GC pause durations
grep "Pause Full" "${GC_LOG}" | awk '{print $NF}' | sort -rn | head -10

# GC throughput summary
grep "Pause" "${GC_LOG}" | awk '{
  sum += $NF
  count++
} END {
  printf "GC events: %d, Total pause: %.1fs, Avg: %.0fms\n",
    count, sum/1000, sum/count
}'
```

---

## Thread Dump Capture and Analysis

Thread dumps reveal: deadlocks, blocked threads, thread pool saturation, slow external calls.

### Capture Thread Dumps

```bash
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)
DUMP_DIR="/tmp/jira-thread-dumps-$(date +%Y%m%d)"
mkdir -p "${DUMP_DIR}"

# Capture 3 dumps 10 seconds apart (standard for hang analysis)
for i in 1 2 3; do
  DUMP_FILE="${DUMP_DIR}/dump-${i}-$(date +%H%M%S).txt"
  jcmd "${JIRA_PID}" Thread.print > "${DUMP_FILE}"
  echo "Captured dump ${i}: ${DUMP_FILE}"
  [ "${i}" -lt 3 ] && sleep 10
done

echo "Thread dumps in: ${DUMP_DIR}"
```

### Parse Thread Dumps

```bash
DUMP_FILE="${DUMP_DIR}/dump-1-*.txt"

# Count thread states
grep -E "^   java.lang.Thread.State:" "${DUMP_FILE}" \
  | sort | uniq -c | sort -rn

# Find threads blocked on locks
grep -A5 "BLOCKED" "${DUMP_FILE}" | head -50

# Find long HTTP request threads
grep -B2 "http-nio-8080" "${DUMP_FILE}" | grep "Thread.State: RUNNABLE"

# Detect deadlocks
grep -A10 "Found.*deadlock" "${DUMP_FILE}"
```

### Thread States Interpretation

| State | Meaning | Concern |
|---|---|---|
| `RUNNABLE` | Actively executing or in native code | Normal, unless all threads RUNNABLE under load |
| `WAITING` | Waiting indefinitely (e.g., `Object.wait()`) | Normal for idle threads |
| `TIMED_WAITING` | Waiting with timeout (e.g., `Thread.sleep()`) | Normal |
| `BLOCKED` | Waiting to acquire a monitor lock | High count = contention / deadlock risk |

A healthy Jira shows mostly `TIMED_WAITING` threads (idle pool workers). Many `BLOCKED` threads indicate a lock contention issue.

---

## Database Slow Query Analysis

### Enable pg_stat_statements

```sql
-- Run as PostgreSQL superuser
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Add to postgresql.conf:
-- shared_preload_libraries = 'pg_stat_statements'
-- pg_stat_statements.track = all
```

### Identify Slow Queries

```sql
-- Top 20 slowest queries by average execution time
SELECT
  LEFT(query, 100) AS query,
  calls,
  ROUND(total_exec_time::numeric, 2) AS total_ms,
  ROUND(mean_exec_time::numeric, 2)  AS avg_ms,
  ROUND(max_exec_time::numeric, 2)   AS max_ms
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_%'
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Currently running queries > 10 seconds
SELECT pid, now() - query_start AS duration, state,
       LEFT(query, 150) AS query
FROM pg_stat_activity
WHERE datname = 'jiradb'
  AND state != 'idle'
  AND query_start < now() - interval '10 seconds'
ORDER BY duration DESC;

-- Blocking queries (lock wait chains)
SELECT
  blocked.pid AS blocked_pid,
  blocked.query AS blocked_query,
  blocking.pid AS blocking_pid,
  blocking.query AS blocking_query
FROM pg_stat_activity AS blocked
JOIN pg_stat_activity AS blocking
  ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE blocked.datname = 'jiradb';
```

### Kill Long-Running Queries

```sql
-- Cancel query (graceful)
SELECT pg_cancel_backend(pid)
FROM pg_stat_activity
WHERE datname = 'jiradb'
  AND state != 'idle'
  AND query_start < now() - interval '5 minutes';

-- Terminate session (hard)
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'jiradb'
  AND pid != pg_backend_pid()
  AND query_start < now() - interval '10 minutes';
```

### Missing Index Detection

```sql
-- Tables with high sequential scan count (candidates for indexing)
SELECT schemaname, relname, seq_scan, idx_scan,
       ROUND(100.0 * seq_scan / (seq_scan + idx_scan + 1), 1) AS seq_pct
FROM pg_stat_user_tables
WHERE schemaname = 'public'
  AND seq_scan > 1000
ORDER BY seq_pct DESC
LIMIT 20;
```

---

## Support ZIP Collection

The Jira `support.zip` bundles all diagnostic information needed for Atlassian support escalation.

### Generate via Admin UI

`Admin → System → Atlassian Support Tools → Create Support Zip`

Options to include (recommended set):

- [x] Application logs (last 3 days)
- [x] Application properties
- [x] Thread dumps (auto-captured at generation time)
- [x] Jira configuration
- [x] Plugin information
- [ ] Attachments (usually too large)

### Generate via Script (Headless)

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  "${JIRA_URL}/rest/api/2/plugins/1.0/resource/com.atlassian.support.stp%3Asupport-tools-plugin/data" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "supportZip",
    "options": {
      "logs": true,
      "configuration": true,
      "threadDump": true,
      "plugins": true
    }
  }' | python3 -m json.tool
```

The zip file is created in `<jira-home>/export/support/`. Retrieve and attach to your Atlassian support ticket.

### What the Support ZIP Contains

| Included File | Purpose |
|---|---|
| `atlassian-jira.log` (last 3 days) | Application events |
| `catalina.out` | JVM/Tomcat output |
| `thread-dump-*.txt` | Live thread dumps |
| `system-info.txt` | JVM args, OS info, Jira version |
| `application-properties.txt` | Jira configuration (sanitised) |
| `installed-plugins.txt` | Plugin list with versions |
| `database-statistics.txt` | DB table sizes and connection info |

---

## Additional Diagnostic Commands

### Jira Instance Information

```bash
# Full server info
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/serverInfo" | python3 -m json.tool

# System health check (Data Center)
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/cluster/health" | python3 -m json.tool

# Check current index status
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/reindex" | python3 -m json.tool
```

### Database Record Counts

```sql
-- Issue count by project
SELECT p.pkey, COUNT(i.id) AS issue_count
FROM project p
LEFT JOIN jiraissue i ON i.project = p.id
GROUP BY p.pkey
ORDER BY issue_count DESC
LIMIT 20;

-- Attachment count and total size
SELECT COUNT(*) AS attachments,
       pg_size_pretty(SUM(filesize)) AS total_size
FROM fileattachment;

-- Comment count
SELECT COUNT(*) FROM jiraaction WHERE actiontype = 'comment';
```

### JMX Monitoring (Optional)

Enable JMX in `setenv.sh` for external monitoring:

```bash
# Add to JVM_SUPPORT_RECOMMENDED_ARGS in setenv.sh
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9999
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
-Djava.rmi.server.hostname=<node-ip>
```

Connect with JConsole or VisualVM:
```text
jconsole <node-ip>:9999
```

Key MBeans to monitor:

| MBean | Attribute | Meaning |
|---|---|---|
| `java.lang:type=Memory` | `HeapMemoryUsage` | Live heap usage |
| `java.lang:type=GarbageCollector` | `CollectionTime` | GC time |
| `java.lang:type=Threading` | `ThreadCount` | Active threads |
| `Catalina:type=ThreadPool` | `currentThreadsBusy` | HTTP threads in use |
| `Catalina:type=ThreadPool` | `maxThreads` | Max HTTP threads |
