---
tags:
  - jira
  - troubleshooting
search:
  boost: 1.5
description: "Jira diagnostic commands: check instance health via the /status endpoint and REST serverInfo API, inspect JVM heap with jmap and jcmd to identify memory..."
---
# Jira — Diagnostics

<div class="kb-summary">
Jira diagnostic commands: check instance health via the /status endpoint and REST serverInfo API, inspect JVM heap with jmap and jcmd to identify memory leaks, capture three thread dumps 10 seconds apart to diagnose deadlocks and blocking, run PostgreSQL pg_stat_statements and pg_stat_activity to identify slow JQL queries, and generate support.zip from the Atlassian Support Tools for escalation.

*Applies to: Jira 9.x / Data Center*
</div>

```d2
direction: right

A: "Issue Reported" {shape: rectangle}
B: "Collect basic info: version, error message,\naffected users" {shape: rectangle}
C: "curl status endpoint + grep catalina.out for ERROR\nOOM Exception" {shape: rectangle}
D: "D" {shape: rectangle}
F: "Check HTTP response times: load a Jira project board" {shape: rectangle}
E: "E" {shape: rectangle}
G: "JVM Heap Analysis:\njmap histo and jcmd GC.heap_info" {shape: rectangle}
H: "Thread Dump Capture:\njcmd Thread.print x3 10s apart" {shape: rectangle}
I: "Database: pg_stat_activity\nand pg_stat_statements slow queries" {shape: rectangle}
J: "Plugin: disable plugin in Admin\nand clear index cache" {shape: rectangle}
K: "K" {shape: rectangle}
L: "DB slow query log + JVM profiling with jstat" {shape: rectangle}
M: "Data Center: check Hazelcast cluster\nand node heartbeat in Admin > Cluster Nodes" {shape: rectangle}
N: "Analyse heap dump with Eclipse MAT\nIdentify retained object class" {shape: rectangle}
O: "O" {shape: rectangle}
P: "Restart affected node\nCapture support.zip before restart" {shape: rectangle}
Q: "Check thread pool: count BLOCKED threads\nIdentify lock holder in dump" {shape: rectangle}
R: "Cancel or terminate long queries\nRequest missing index via DBA" {shape: rectangle}
S: "Update or remove offending plugin\nClear plugin cache and restart node" {shape: rectangle}
T: "Add indexes, optimise JQL\nIncrease JVM heap or node count" {shape: rectangle}
U: "Investigate management network\nRestart affected cluster node" {shape: rectangle}
V: "V" {shape: rectangle}
W: "Collect support.zip\nEscalate to Atlassian Support" {shape: rectangle}
X: "Resolved — document RCA" {shape: rectangle}

A -> B
B -> C
D -> F
E -> G
E -> H
E -> I
E -> J
K -> L
K -> M
G -> N
O -> P
O -> Q
I -> R
J -> S
L -> T
M -> U
P -> V
Q -> V
R -> V
S -> V
T -> V
U -> V
V -> W
V -> X
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_instance_health: "Step 1 — Check instance health" {shape: rectangle}
step_2_jvm_heap_analysis: "Step 2 — JVM heap analysis" {shape: rectangle}
step_3_thread_dump_capture_and_analy: "Step 3 — Thread dump capture and analysis" {shape: rectangle}
step_4_database_slow_query_analysis: "Step 4 — Database slow query analysis" {shape: rectangle}
step_5_support_zip_collection: "Step 5 — Support ZIP collection" {shape: rectangle}
step_6_additional_diagnostic_command: "Step 6 — Additional diagnostic commands" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_instance_health: investigate
symptom -> step_2_jvm_heap_analysis: investigate
symptom -> step_3_thread_dump_capture_and_analy: investigate
symptom -> step_4_database_slow_query_analysis: investigate
symptom -> step_5_support_zip_collection: investigate
symptom -> step_6_additional_diagnostic_command: investigate
step_1_check_instance_health -> resolution
step_2_jvm_heap_analysis -> resolution
step_3_thread_dump_capture_and_analy -> resolution
step_4_database_slow_query_analysis -> resolution
step_5_support_zip_collection -> resolution
step_6_additional_diagnostic_command -> resolution
```

## Before you begin

- **Access:** SSH to Jira server(s) as root or jira OS user; PostgreSQL admin access (`psql -U postgres`); Jira Admin account for the web UI
- **Gather first:** the exact error message from the UI, the Jira version from Admin > System Information, the number of affected users, and whether the symptom started after a recent change (plugin install, upgrade, DB migration)
- **Scope:** confirm whether the issue affects one project, one user, or all users — a single slow project often points to a JQL index issue, while all-user slowness points to JVM or DB saturation

---

## Step 1 — Check instance health

```bash
# Confirm the Jira application is running
curl -s http://localhost:8080/status
# Expected: {"state":"RUNNING"}

# Recent application errors
JIRA_INSTALL=/opt/atlassian/jira
grep -i "ERROR\|OOM\|Exception" "${JIRA_INSTALL}/logs/catalina.out" | tail -50

# Full server info via REST API
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/serverInfo" | python3 -m json.tool

# System health check (Data Center only)
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/cluster/health" | python3 -m json.tool

# Current reindex status
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/reindex" | python3 -m json.tool

# Disk usage on JIRA_HOME
df -h /var/atlassian/application-data/jira/
ls -lh /var/atlassian/application-data/jira/data/attachments/

# System memory
free -h
top -b -n1 | grep java | head -5
```


```text title="Expected output"
{"state":"RUNNING"}
2024-01-15 09:23:47,521 ERROR [http-nio-8080-exec-12] com.atlassian.jira.issue.search.SearchException - Search failed: timeout after 30s
2024-01-15 09:18:12,334 WARN [scheduler_Worker-2] com.atlassian.jira.bc.issue.search.SearchService - OOM detected in query execution
2024-01-15 08:45:01,221 ERROR [jira-request-incoming-1847] java.lang.OutOfMemoryError: Java heap space
{
  "baseUrl": "http://jira.company.local:8080",
  "version": "8.20.11",
  "versionNumbers": [8, 20, 11, 0],
  "buildNumber": 820011,
  "buildDate": "2023-12-10T14:32:00.000-0500",
  "serverTime": "2024-01-15T14:47:22.156-0500",
  "scmInfo": "abc1d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9",
  "displayName": "JIRA Production"
}
{
  "nodes": [
    {
      "nodeId": "node-1",
      "alive": true,
      "healthy": true,
      "state": "ACTIVE"
    },
    {
      "nodeId": "node-2",
      "alive": true,
      "healthy": true,
      "state": "ACTIVE"
    }
  ],
  "clusterHealthy": true
}
{
  "progressPercentage": 0,
  "currentIndex": 0,
  "totalIssues": 847293,
  "description": "Reindex completed successfully",
  "reindexTime": 3847000
}
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       500G  387G  113G  78% /var/atlassian/application-data/jira
total 2.1G
drwxr-xr-x  512 jira jira 4.0K Jan 15 14:22 attachments
-rw-r--r--    1 jira jira 2.1G Jan 15 14:15 attachments.tar.gz
              total        used        free      shared  buff/cache   available
                 32Gi       18Gi       8.2Gi      512Mi       5.8Gi       13Gi
root      1847  2.3 28.4 5847392 9234560 ?  Sl  09:12   0:47 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xms4g -Xmx10g
root      2156  1.8 22.1 4923847 7234891 ?  Sl  09:15   0:32 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xms2g -Xmx8g
```
---

## Step 2 — JVM heap analysis

### Check live heap usage

```bash
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)

# Heap summary
jcmd "${JIRA_PID}" GC.heap_info

# Histogram of object types by memory (top 30)
jmap -histo:live "${JIRA_PID}" | head -35

# Configured heap limits
jcmd "${JIRA_PID}" VM.flags | grep -E "HeapSize|Xmx|Xms"
```


```text title="Expected output"
24680
 NumGC: 12
 GC time (ms): 2847
 Eden Space (bytes): 536870912
 Survivor Space (bytes): 67108864
 Tenured Gen (bytes): 1610612736
 Metaspace (bytes): 134217728

 num     #instances         #bytes  class name
----------------------------------------------
   1:       1847392      148592640  [C (char array)
   2:        521847       83495520  java.lang.String
   3:        312156       49945280  [Ljava/lang/Object;
   4:        187643       30023040  java.util.HashMap$Node
   5:        156821       25091360  [I (int array)
   6:         98432       15749120  java.util.ArrayList
   7:         67284       10765440  com.atlassian.jira.issue.Issue
   8:         54921        8787360  java.util.LinkedHashMap$Entry
...
Total        8947283     1456789120

-XX:InitialHeapSize=2147483648 -XX:MaxHeapSize=4294967296 -XX:+UseG1GC
```

!!! warning "Common errors"
    **`pgrep: command not found`** — Install procps-ng package or use `ps aux | grep atlassian-jira` to locate the PID manually.
    **`Could not attach to <PID>: Permission denied`** — Run the command as the same user running JIRA (typically `jira` user) or use `sudo`.
    **`jcmd: command not found`** — Ensure JAVA_HOME is set correctly and jcmd is in PATH; verify JDK (not JRE) is installed.
### Capture heap dump

```bash
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)
DUMP_FILE="/tmp/jira-heap-$(date +%Y%m%d-%H%M%S).hprof"

# Live objects only (reduces dump size, most useful for leak analysis)
sudo -u jira jmap -dump:format=b,live,file="${DUMP_FILE}" "${JIRA_PID}"

echo "Heap dump: ${DUMP_FILE} ($(du -sh ${DUMP_FILE} | cut -f1))"
```


```text title="Expected output"
Dump file size: 2.3G
Heap dump: /tmp/jira-heap-20240115-143022.hprof (2.3G)
```

!!! warning "Common errors"
    **`Could not attach to process`** — Ensure the JIRA process is running with `pgrep -f 'atlassian-jira'` and verify the PID is correct before running jmap.
    **`Permission denied`** — Run the command with appropriate sudo privileges or ensure the jira user has permissions to write to /tmp.
    **`jmap: command not found`** — Install the JDK (not just JRE) on the system, as jmap is part of the JDK tools.
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

### GC log analysis

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


```text title="Expected output"
247
2.156s
1.987s
1.654s
1.423s
0.987s
0.876s
0.745s
0.698s
0.612s
0.501s
GC events: 1847, Total pause: 892.3s, Avg: 483ms
```

!!! warning "Common errors"
    **`grep: /opt/atlassian/jira/logs/gc.log: No such file or directory`** — Verify the GC log path matches your JIRA installation; check `$JIRA_HOME/logs/` and update `GC_LOG` variable accordingly.
    **`awk: syntax error in function printf near line 1`** — Ensure the awk script is properly quoted and newlines are preserved; use single quotes around the entire awk block or escape internal quotes.
    **`command not found: awk`** — Install gawk or mawk package using your system package manager (e.g., `apt-get install gawk` on Debian/Ubuntu).
---

## Step 3 — Thread dump capture and analysis

Thread dumps reveal: deadlocks, blocked threads, thread pool saturation, slow external calls.

### Capture thread dumps

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


```text title="Expected output"
Captured dump 1: /tmp/jira-thread-dumps-20240315/dump-1-143022.txt
Captured dump 2: /tmp/jira-thread-dumps-20240315/dump-2-143032.txt
Captured dump 3: /tmp/jira-thread-dumps-20240315/dump-3-143042.txt
Thread dumps in: /tmp/jira-thread-dumps-20240315
```

!!! warning "Common errors"
    **`jcmd: command not found`** — Ensure the JDK (not just JRE) is installed and `JAVA_HOME` is set correctly in your environment.
    **`Error: Could not attach to process`** — Verify the JIRA process is running with `ps aux | grep atlassian-jira` and that you have sufficient permissions (may require `sudo`).
    **`No such file or directory`** — Check that `/tmp` is writable and has sufficient free space with `df -h /tmp`.
### Parse thread dumps

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


```text title="Expected output"
45 java.lang.Thread.State: WAITING
     12 java.lang.Thread.State: RUNNABLE
      8 java.lang.Thread.State: TIMED_WAITING
      3 java.lang.Thread.State: BLOCKED
      1 java.lang.Thread.State: NEW

   java.lang.Thread.State: BLOCKED (on object monitor)
	at com.atlassian.jira.issue.IssueManager.getIssue(IssueManager.java:234)
	- waiting to lock <0x00007f8a2c4d5e90> (a java.lang.Object)
	at com.atlassian.jira.rest.v2.issue.IssueResource.getIssue(IssueResource.java:156)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)

   java.lang.Thread.State: RUNNABLE
	at java.net.SocketInputStream.socketRead0(Native Method)
	at java.net.SocketInputStream.read(SocketInputStream.java:152)
	at org.apache.catalina.connector.http.HttpProcessor.process(HttpProcessor.java:876)
	at org.apache.catalina.connector.http.HttpConnector$HttpRequestHandler.run(HttpConnector.java:682)

   java.lang.Thread.State: RUNNABLE
	at java.net.SocketInputStream.socketRead0(Native Method)
	at java.net.SocketInputStream.read(SocketInputStream.java:152)

Found one Java-level deadlock:
=============================
"http-nio-8080-exec-7":
  waiting to lock monitor 0x00007f8a2c4d5e90 (object 0x00007f8a2c4d5e90, a java.lang.Object),
  which is held by "http-nio-8080-exec-12"

"http-nio-8080-exec-12":
  waiting to lock monitor 0x00007f8a2c4d5f10 (object 0x00007f8a2c4d5f10, a java.lang.Object),
  which is held by "http-nio-8080-exec-7"
```

!!! warning "Common errors"
    **`grep: /var/dumps/dump-1-*.txt: No such file or directory`** — Verify the dump file exists in `${DUMP_DIR}` and matches the naming pattern, or use `ls ${DUMP_DIR}/dump-1-*.txt` to confirm the path.
    **`grep: (standard input) is empty`** — The dump file is empty or the grep pattern doesn't match any content; regenerate the thread dump using `jstack <pid> > ${DUMP_DIR}/dump-1-$(date +%s).txt`.
    **`DUMP_DIR: unbound variable`** — Set the `DUMP_DIR` variable before running the script with `export DUMP_DIR=/path/to/dumps` or define it inline.
### Thread states interpretation

| State | Meaning | Concern |
|---|---|---|
| `RUNNABLE` | Actively executing or in native code | Normal, unless all threads RUNNABLE under load |
| `WAITING` | Waiting indefinitely (e.g., `Object.wait()`) | Normal for idle threads |
| `TIMED_WAITING` | Waiting with timeout (e.g., `Thread.sleep()`) | Normal |
| `BLOCKED` | Waiting to acquire a monitor lock | High count = contention / deadlock risk |

A healthy Jira shows mostly `TIMED_WAITING` threads (idle pool workers). Many `BLOCKED` threads indicate a lock contention issue.

---

## Step 4 — Database slow query analysis

### Enable pg_stat_statements

```sql
-- Run as PostgreSQL superuser
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Add to postgresql.conf:
-- shared_preload_libraries = 'pg_stat_statements'
-- pg_stat_statements.track = all
```

### Identify slow queries

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

### Kill long-running queries

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

### Missing index detection

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

## Step 5 — Support ZIP collection

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

### Generate via script (headless)

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


```text title="Expected output"
{
  "id": "support-zip-20240115-a7f3c9e2",
  "status": "PROCESSING",
  "createdAt": "2024-01-15T14:32:18.447Z",
  "expiresAt": "2024-01-22T14:32:18.447Z",
  "downloadUrl": "/secure/attachment/support-zip-20240115-a7f3c9e2.zip",
  "size": null,
  "includes": {
    "logs": true,
    "configuration": true,
    "threadDump": true,
    "plugins": true
  },
  "estimatedCompletionTime": "2024-01-15T14:37:18.447Z"
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Verify `${JIRA_URL}` is correct and the Jira instance is running and accessible from your network.
    **`{"errorMessages":["User does not have permission to administer Jira"],"errors":{}}`** — Ensure `${JIRA_USER}` has Jira administrator privileges or use an API token from an admin account.
    **`curl: (6) Could not resolve host: jira.example.com`** — Check that `${JIRA_URL}` hostname is resolvable and verify DNS or network connectivity.
The zip file is created in `<jira-home>/export/support/`. Retrieve and attach to your Atlassian support ticket.

### What the Support ZIP contains

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

## Step 6 — Additional diagnostic commands

### Database record counts

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
```

### JMX monitoring (optional)

Enable JMX in `setenv.sh` for external monitoring:

```bash
# Add to JVM_SUPPORT_RECOMMENDED_ARGS in setenv.sh
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9999
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
-Djava.rmi.server.hostname=<node-ip>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Exception in thread "main" java.net.BindException: Address already in use`** — Change the JMX port (e.g., 9999 to 10000) if another process is already listening on that port.
    **`java.rmi.ConnectException: Connection refused to host: <node-ip>`** — Verify the `java.rmi.server.hostname` is set to the actual resolvable IP or FQDN of the Jira node, not localhost or an internal IP if connecting remotely.
    **`java.lang.SecurityException: Authentication disabled but password file not found`** — Set `jmxremote.authenticate=false` only in non-production environments; for production, create a jmxremote.password file and set authenticate=true instead.
Key MBeans to monitor:

| MBean | Attribute | Meaning |
|---|---|---|
| `java.lang:type=Memory` | `HeapMemoryUsage` | Live heap usage |
| `java.lang:type=GarbageCollector` | `CollectionTime` | GC time |
| `java.lang:type=Threading` | `ThreadCount` | Active threads |
| `Catalina:type=ThreadPool` | `currentThreadsBusy` | HTTP threads in use |
| `Catalina:type=ThreadPool` | `maxThreads` | Max HTTP threads |

---

## Log locations

| Log | Path | What to look for |
|---|---|---|
| Application log | `JIRA_HOME/log/atlassian-jira.log` | Plugin errors, workflow exceptions, auth failures |
| Tomcat stdout | `JIRA_INSTALL/logs/catalina.out` | JVM startup errors, OOM, thread dump output |
| GC log | `JIRA_INSTALL/logs/gc.log` | Full GC frequency and pause durations |
| Access log | `JIRA_INSTALL/logs/access_log.*.txt` | HTTP request timing per endpoint |
| PostgreSQL slow queries | `pg_stat_statements` + pg log | Slow or blocking JQL queries |
| Support ZIP | `JIRA_HOME/export/support/` | All-in-one — required for Atlassian SR |

---

## See also

- [Jira — Common Issues](../common-issues/)
- [Jira — Escalation](../escalation/)
- [Jira — Health Checks](../../operations/health-checks/)

## Verify resolution

- `curl -s http://localhost:8080/status` returns `{"state":"RUNNING"}`
- `jcmd $JIRA_PID GC.heap_info` shows heap below 80% of max (-Xmx) between GC cycles
- `grep -c "BLOCKED" /tmp/jira-thread-dumps-*/dump-1-*.txt` returns a low count (< 5)
- A Jira project board loads in under 3 seconds (browser network tab)
- `grep -i "OOM\|OutOfMemoryError" /opt/atlassian/jira/logs/catalina.out` returns no new entries after the fix
- PostgreSQL: `SELECT count(*) FROM pg_stat_activity WHERE state != 'idle'` shows normal connection count for the cluster size
