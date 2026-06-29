---
tags:
  - confluence
  - troubleshooting
search:
  boost: 1.5
---
# Confluence — Diagnostics

<div class="kb-summary">
Confluence diagnostic commands: check instance health via the /status endpoint, inspect JVM heap with jstat and jmap to identify memory leaks, capture three thread dumps 10 seconds apart to diagnose deadlocks, run PostgreSQL pg_stat_activity and EXPLAIN ANALYZE to identify slow macro and page-render queries, and generate support.zip from Admin for Atlassian escalation.

*Applies to: Confluence Data Center / Cloud*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "Check JVM heap and GC logs\njstat gcutil + jmap histo" {shape: rectangle}
D: "Capture heap dump\njmap dump and analyse with MAT" {shape: rectangle}
E: "Capture thread dumps x3 10s apart\njstack -l CONF_PID" {shape: rectangle}
F: "Check DB query log\npg_stat_activity for long-running queries" {shape: rectangle}
G: "Check app log for exceptions\ngrep Exception atlassian-confluence.log" {shape: rectangle}
H: "H" {shape: rectangle}
I: "Tune G1GC, increase heap in setenv.sh\nReview cache size settings" {shape: rectangle}
J: "Check DB query latency and slow macros\nEXPLAIN ANALYZE suspicious query" {shape: rectangle}
K: "Identify top memory consumers in MAT\nLeak Suspects Report" {shape: rectangle}
M: "Analyse thread states: BLOCKED count\nIdentify deadlock in jstack output" {shape: rectangle}
N: "Identify blocking thread and lock owner\nDisable offending plugin or restart node" {shape: rectangle}
O: "O" {shape: rectangle}
P: "pg_cancel_backend or pg_terminate_backend\nAdd missing index via EXPLAIN ANALYZE" {shape: rectangle}
Q: "Scale DB connection pool in confluence.cfg.xml\nCheck for connection leaks in app log" {shape: rectangle}
R: "Match exception type to known issues\nor disable plugin and retest" {shape: rectangle}
S: "Collect support.zip + thread dump + heap dump\nOpen Atlassian HI ticket" {shape: rectangle}
L: "L" {shape: rectangle}
T: "Provide: instance name, version, node, repro steps\nLog excerpts and support.zip attachment" {shape: rectangle}
A: "Issue Reported" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
H -> I
H -> J
D -> K
E -> M
M -> N
O -> P
O -> Q
G -> R
I -> S
J -> S
L -> S
N -> S
P -> S
Q -> S
R -> S
S -> T
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_instance_health: "Step 1 — Check instance health" {shape: rectangle}
step_2_jvm_heap_analysis: "Step 2 — JVM heap analysis" {shape: rectangle}
step_3_thread_dump_capture_and_analy: "Step 3 — Thread dump capture and analysis" {shape: rectangle}
step_4_database_query_performance: "Step 4 — Database query performance" {shape: rectangle}
step_5_support_zip_collection: "Step 5 — Support ZIP collection" {shape: rectangle}
log_locations: "Log locations" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_instance_health: investigate
symptom -> step_2_jvm_heap_analysis: investigate
symptom -> step_3_thread_dump_capture_and_analy: investigate
symptom -> step_4_database_query_performance: investigate
symptom -> step_5_support_zip_collection: investigate
symptom -> log_locations: investigate
step_1_check_instance_health -> resolution
step_2_jvm_heap_analysis -> resolution
step_3_thread_dump_capture_and_analy -> resolution
step_4_database_query_performance -> resolution
step_5_support_zip_collection -> resolution
log_locations -> resolution
```

## Before you begin

- **Access:** SSH to Confluence server(s) as root or confluence OS user; PostgreSQL admin access; Confluence Admin account for the web UI and support tools
- **Gather first:** the exact error message or slow operation, the Confluence version from Admin > General Configuration > System Information, the number of affected users, and whether the issue started after a specific change (plugin install, upgrade, index rebuild, NFS change)
- **Scope:** confirm whether the issue affects one space, one user, or all users — a single slow space often points to a macro or attachment index issue, while all-user slowness points to JVM or DB saturation

---

## Step 1 — Check instance health

```bash
# Confirm the Confluence application is running
curl -s http://localhost:8090/status
# Expected: {"state":"RUNNING"}

# Recent application errors
LOG="/var/atlassian/application-data/confluence/logs/atlassian-confluence.log"
grep "Exception\|Error" "$LOG" | grep -v "DEBUG" | tail -30

# Slow page render warnings
grep -E "Slow|took [0-9]{4,}ms" "$LOG" | tail -20

# OOM events
grep "OutOfMemoryError" "$LOG"

# Plugin failures
grep -E "(BundleException|PluginException|Failed to start bundle)" "$LOG" | tail -20

# Database errors
grep -E "(JDBCException|SQL.*Exception|cannot acquire.*connection)" "$LOG" | tail -20

# Disk usage
df -h /var/atlassian/application-data/confluence/
ls -lh /var/atlassian/application-data/confluence/attachments/ | tail -5

# System memory
free -h
top -b -n1 | grep java | head -5
```


```text title="Expected output"
{"state":"RUNNING"}
2024-01-15 14:32:18,445 ERROR [http-nio-8090-exec-42] com.atlassian.confluence.pages.actions.ViewPageAction - Exception rendering page: Page ID 98765
java.lang.NullPointerException: Cannot invoke method on null object
	at com.atlassian.confluence.pages.PageManager.getPage(PageManager.java:287)
2024-01-15 14:28:03,221 WARN [scheduler-7] com.atlassian.confluence.search.v2.SearchManager - Error indexing page 54321: timeout after 5000ms
2024-01-15 13:55:42,109 ERROR [http-nio-8090-exec-18] com.atlassian.plugin.manager.DefaultPluginManager - Failed to start bundle: com.example.custom-plugin v2.1.4

2024-01-15 15:01:22,334 WARN [http-nio-8090-exec-51] com.atlassian.confluence.pages.actions.ViewPageAction - Slow page render took 8234ms for page Dashboard
2024-01-15 14:59:18,556 WARN [http-nio-8090-exec-33] com.atlassian.confluence.search.v2.SearchManager - Search query took 6891ms

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda2      500G  387G  113G  78% /var/atlassian/application-data/confluence
-rw-r--r-- 1 confluence confluence 2.3G Jan 15 15:02 page-98765-attachment.pdf
-rw-r--r-- 1 confluence confluence 1.8G Jan 14 22:15 export-backup-20240114.zip
-rw-r--r-- 1 confluence confluence 892M Jan 13 18:44 video-demo.mp4
-rw-r--r-- 1 confluence confluence 567M Jan 12 10:33 archive-2024Q1.tar.gz
-rw-r--r-- 1 confluence confluence 445M Jan 11 09:22 presentation-slides.pptx

               total        used        free      shared  buff/cache   available
Mem:            31Gi       18Gi       4.2Gi       256Mi       8.8Gi       12Gi
java     1847  2.4 58.3 6234568 18234456   ?  Sl   14:22   2:47 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xmx20g -Xms8g
java     1923  0.1  2.1 1024567 678234     ?  Sl   14:25   0:12 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xmx2g
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to localhost port 8090: Connection refused`** — Verify Confluence service is running with `systemctl status confluence` and check if the port binding changed in `confluence.cfg.xml`.
    **`grep: /var/atlassian/application-
---

## Step 2 — JVM heap analysis

### Check current heap usage

```bash
CONF_PID=$(pgrep -f "atlassian-confluence\|confluence\.home" | head -1)

# Summary heap stats (every 5 seconds, 5 samples)
jstat -gcutil "$CONF_PID" 5000 5
# Columns: S0, S1, E (Eden), O (Old), M (Metaspace), YGC, YGCT, FGC, FGCT, GCT
# Alert if O > 90% between GC cycles

# Full GC info
jstat -gc "$CONF_PID" 5000 3
```


```text title="Expected output"
12345
  S0     S1     E      O      M     YGC     YGCT    FGC    FGCT     GCT
  0.00  45.23  78.91  72.34  88.12   1247   156.32    18    45.67  201.99
  0.00  45.23  82.15  72.34  88.12   1247   156.32    18    45.67  201.99
  0.00  45.23  85.42  73.21  88.45   1248   156.89    18    45.67  202.56
  0.00  45.23  12.08  73.21  88.45   1248   156.89    18    45.67  202.56
  0.00  45.23  18.34  73.89  88.67   1249   157.45    18    45.67  203.12

 S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU    YGC     YGCT    FGC    FGCT     GCT
655360 655360      0 296576 5242880 4390912 11010048 8070144 176128 155648 20480 18432   1248  157.45     18   45.67  203.12
655360 655360      0 296576 5242880 4521984 11010048 8070144 176128 155648 20480 18432   1248  157.45     18   45.67  203.12
655360 655360      0 296576 5242880 4653056 11010048 8070144 176128 155648 20480 18432   1249  158.01     18   45.67  203.68
```

!!! warning "Common errors"
    **`12345: No such process`** — Verify Confluence is running with `systemctl status confluence` and check the correct process name with `ps aux | grep confluence`.
    **`jstat: command not found`** — Install the JDK (not just JRE) on the system, as jstat is part of the JDK tools package.
    **`Permission denied`** — Run the command with `sudo` or as the confluence system user to access the JVM process statistics.
### Capture an on-demand heap dump

```bash
CONF_PID=$(pgrep -f "atlassian-confluence\|confluence\.home" | head -1)
DUMP_FILE="/tmp/confluence-heap-$(date +%Y%m%d%H%M).hprof"

jmap -dump:format=b,file="$DUMP_FILE" "$CONF_PID"
echo "Heap dump: $DUMP_FILE ($(du -sh $DUMP_FILE | cut -f1))"
```


```text title="Expected output"
Heap dump: /tmp/confluence-heap-202401151430.hprof (2.3G)
```

!!! warning "Common errors"
    **`jmap: command not found`** — Install the JDK (not just JRE) on the system, as jmap is part of the JDK tools.
    **`Error attaching to process: sun.jvm.hotspot.debugger.DebuggerException: Cannot open socket file`** — Ensure Confluence is running as the same user executing jmap, or run jmap with sudo.
    **`No such file or directory`** — Verify the Confluence PID exists with `pgrep -f "atlassian-confluence"` before running jmap, as the process may have stopped.
### Analyse heap dump with Eclipse MAT

1. Download [Eclipse Memory Analyzer (MAT)](https://www.eclipse.org/mat/)
2. Open the `.hprof` file in MAT
3. Run **Leak Suspects Report** (automatic analysis)
4. Key views:
   - **Dominator tree**: largest retained object graphs
   - **Histogram**: object counts by class
   - **OQL**: query object heap (e.g., `SELECT * FROM com.atlassian.plugin.* WHERE @retainedHeapSize > 1000000`)

Common findings:

| Retained Object | Likely Cause |
|---|---|
| Large `CacheManager` or `EhCache` objects | Cache size misconfigured or unbounded |
| Many `PageImpl` or `ContentEntityObject` | Bulk page render or large export in progress |
| Plugin class instances | Plugin memory leak — disable and retest |
| String arrays > 100 MB | Attachment content loaded into heap |

---

## Step 3 — Thread dump capture and analysis

Thread dumps reveal what all JVM threads are doing at a point in time. Capture 3 dumps 10 seconds apart to identify patterns — stuck threads repeat across dumps; busy threads appear in different states.

### Capture thread dumps

```bash
CONF_PID=$(pgrep -f "atlassian-confluence\|confluence\.home" | head -1)

for i in 1 2 3; do
  DUMP_FILE="/tmp/threaddump_${i}_$(date +%H%M%S).txt"
  jstack -l "$CONF_PID" > "$DUMP_FILE"
  echo "Captured: $DUMP_FILE"
  [ $i -lt 3 ] && sleep 10
done

# Merge for analysis
cat /tmp/threaddump_*.txt > /tmp/threaddump_merged.txt
```


```text title="Expected output"
Captured: /tmp/threaddump_1_143022.txt
Captured: /tmp/threaddump_2_143032.txt
Captured: /tmp/threaddump_3_143042.txt
```

!!! warning "Common errors"
    **`jstack: command not found`** — Install the JDK (not just JRE) on the system, as jstack is only included in JDK distributions.
    **`Could not attach to <PID>: Permission denied`** — Run the script with sudo or as the same user that started the Confluence process (typically the confluence system user).
    **`pgrep: command not found`** — Install the procps package (`apt-get install procps` on Debian/Ubuntu or `yum install procps-ng` on RHEL/CentOS).
### Thread dump quick analysis

```bash
# Count threads by state
grep "java.lang.Thread.State:" /tmp/threaddump_1_*.txt \
  | awk '{print $2}' | sort | uniq -c | sort -rn

# Find all BLOCKED threads
grep -A 10 "java.lang.Thread.State: BLOCKED" /tmp/threaddump_1_*.txt | head -60

# Find all threads waiting on a lock
grep -B 5 "waiting to lock" /tmp/threaddump_1_*.txt | grep "\"" | head -20

# Find deadlocks (jstack outputs these at the end)
grep -A 20 "DEADLOCK" /tmp/threaddump_1_*.txt
```


```text title="Expected output"
245 RUNNABLE
      87 TIMED_WAITING
      42 WAITING
      18 BLOCKED
       3 NEW

java.lang.Thread.State: BLOCKED (on object monitor)
	at com.example.service.DatabasePool.getConnection(DatabasePool.java:156)
	- waiting to lock <0x00007f8c4a2b9f80> (a java.lang.Object)
	at com.example.api.RequestHandler.processQuery(RequestHandler.java:423)
	at java.lang.Thread.run(Thread.java:834)

java.lang.Thread.State: BLOCKED (on object monitor)
	at com.example.cache.CacheManager.invalidate(CacheManager.java:89)
	- waiting to lock <0x00007f8c4a2b9f80> (a java.lang.Object)
	at com.example.service.DataService.refresh(DataService.java:201)
	at java.lang.Thread.run(Thread.java:834)

"http-nio-8080-exec-12" #47 daemon prio=5 os_prio=0 tid=0x00007f8c3e4a2000 nid=0x5f2a waiting to lock <0x00007f8c4a2b9f80> (a java.lang.Object)
"http-nio-8080-exec-15" #50 daemon prio=5 os_prio=0 tid=0x00007f8c3e4a5800 nid=0x5f2d waiting to lock <0x00007f8c4a2b9f80> (a java.lang.Object)
"http-nio-8080-exec-18" #53 daemon prio=5 os_prio=0 tid=0x00007f8c3e4a8c00 nid=0x5f30 waiting to lock <0x00007f8c4a2b9f80> (a java.lang.Object)
"scheduler-pool-1" #61 daemon prio=5 os_prio=0 tid=0x00007f8c3e5b1000 nid=0x5f3e waiting to lock <0x00007f8c4a2b9f80> (a java.lang.Object)
"background-worker-4" #78 daemon prio=5 os_prio=0 tid=0x00007f8c3e6c2400 nid=0x5f55 waiting to lock <0x00007f8c4a2b9f80> (a java.lang.Object)

Found one Java-level deadlock:
=============================
"http-nio-8080-exec-9" #44:
  waiting to lock monitor 0x00007f8c4a2b9f80 (object 0x00007f8c4a2b9f80, a java.lang.Object),
  which is held by "scheduler-pool-2" #62
"scheduler-pool-2" #62:
  waiting to lock monitor 0x00007f8c4a2ba100 (object 0x00007f8c4a2ba100, a java.lang.Object),
  which is held by "http
```
### Thread states reference

| State | Meaning | Normal? |
|---|---|---|
| `RUNNABLE` | Actively executing | Yes |
| `WAITING` | Waiting for notify/join | Yes (idle threads) |
| `TIMED_WAITING` | Sleeping / scheduled wait | Yes |
| `BLOCKED` | Waiting to acquire a monitor lock | Occasional OK; many = problem |
| `DEADLOCK` | Circular lock dependency | Never — immediate action required |

High counts of blocked `http-nio-8090-exec-N` threads indicate HTTP request queue build-up. Root cause is usually DB or lock contention.

---

## Step 4 — Database query performance

### Identify slow queries

```bash
# Enable slow query logging in PostgreSQL (threshold: 500ms)
psql -h "$DB_HOST" -U postgres \
  -c "ALTER SYSTEM SET log_min_duration_statement = '500';"
psql -h "$DB_HOST" -U postgres \
  -c "SELECT pg_reload_conf();"

# View slow queries from pg log
tail -100 /var/log/postgresql/postgresql-*.log | grep "duration:"

# Real-time active query monitoring
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT pid,
             round(extract(epoch from now() - query_start)::numeric, 2) AS elapsed_s,
             state,
             left(query, 100) AS query_snippet
      FROM pg_stat_activity
      WHERE state != 'idle'
        AND query_start < now() - interval '5 seconds'
      ORDER BY elapsed_s DESC;"
```


```text title="Expected output"
ALTER SYSTEM
SELECT 1
2024-01-15 14:23:47.891 UTC [8472] LOG:  duration: 2847.523 ms  statement: SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '30 days';
2024-01-15 14:25:12.445 UTC [8501] LOG:  duration: 1205.678 ms  statement: SELECT COUNT(*) FROM audit_logs WHERE timestamp > NOW() - INTERVAL '1 hour';
2024-01-15 14:27:33.112 UTC [8534] LOG:  duration: 623.891 ms  statement: UPDATE inventory SET stock = stock - 1 WHERE product_id = $1;
2024-01-15 14:29:01.667 UTC [8556] LOG:  duration: 512.234 ms  statement: SELECT * FROM users u JOIN orders o ON u.id = o.user_id LIMIT 1000;

 pid  | elapsed_s |      state      | query_snippet
------+-----------+----------------+----------------------------------------------
 9847 |    18.45  | active         | SELECT * FROM large_transactions WHERE status
 9823 |    12.67  | active         | UPDATE customer_profiles SET last_login = now()
 9801 |     8.34  | active         | INSERT INTO event_log (event_type, timestamp)
(3 rows)
```

!!! warning "Common errors"
    **`psql: error: could not translate host name "$DB_HOST" to address: Name or service not known`** — Replace `$DB_HOST` with the actual PostgreSQL server hostname or IP address, or ensure the environment variable is exported before running the script.
    **`psql: error: FATAL:  Ident authentication failed for user "postgres"`** — Configure PostgreSQL to accept password authentication in `pg_hba.conf` or use a `.pgpass` file with credentials for the postgres user.
    **`tail: cannot open '/var/log/postgresql/postgresql-*.log' for reading: No such file or directory`** — Verify the PostgreSQL log directory path matches your installation (check `log_directory` in `postgresql.conf`) and ensure the user running the command has read permissions.
### Table bloat check

```bash
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT tablename,
             pg_size_pretty(pg_relation_size(tablename::regclass)) AS table_size,
             pg_size_pretty(pg_total_relation_size(tablename::regclass)) AS total_size,
             n_dead_tup AS dead_tuples
      FROM pg_stat_user_tables
      ORDER BY n_dead_tup DESC
      LIMIT 15;"
```


```text title="Expected output"
psql (14.8, server 14.9)
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.

           tablename            | table_size | total_size | dead_tuples
---------------------------------+------------+------------+-------------
 audit_logs                      | 2847 MB    | 3156 MB    |      847293
 user_sessions                   | 1203 MB    | 1456 MB    |      623841
 event_queue                     | 892 MB     | 1087 MB    |      412756
 page_revisions                  | 654 MB     | 891 MB     |      287654
 attachment_metadata             | 423 MB     | 567 MB     |      156432
 workflow_transitions            | 287 MB     | 401 MB     |       98765
 comment_history                 | 156 MB     | 234 MB     |       67543
 notification_log                | 89 MB      | 145 MB     |       34521
 cache_entries                   | 45 MB      | 78 MB      |       12987
 permission_grants               | 34 MB      | 52 MB      |        8234
 label_assignments               | 28 MB      | 41 MB      |        5123
 space_settings                  | 12 MB      | 18 MB      |        1456
 user_preferences                | 8 MB       | 14 MB      |         892
 api_tokens                      | 3 MB       | 5 MB       |         234
 temp_imports                    | 1 MB       | 2 MB       |          45
(15 rows)
```

!!! warning "Common errors"
    **`psql: error: could not translate host name "$DB_HOST" to address: Name or service not known`** — Verify the `$DB_HOST` environment variable is set correctly with `echo $DB_HOST` and confirm the hostname resolves via `nslookup` or `ping`.
    **`psql: error: FATAL: Ident authentication failed for user "$DB_USER"`** — Ensure the PostgreSQL `pg_hba.conf` file permits the connection method for your user and host, or use a `.pgpass` file with proper permissions (600).
    **`ERROR: relation "pg_stat_user_tables" does not exist`** — Confirm you are connecting to the correct database with `-d "$DB_NAME"` and that the PostgreSQL server version supports this system catalog view (available in PostgreSQL 8.4+).
High `dead_tuples` → run `VACUUM ANALYZE <tablename>;`

### EXPLAIN ANALYZE a suspicious query

```sql
-- Prefix the slow query from pg_stat_activity with EXPLAIN (ANALYZE, BUFFERS)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT id, title, version
FROM content
WHERE spacekey = 'OPS'
  AND contenttype = 'PAGE'
  AND prevver IS NULL
ORDER BY title;
```

Look for: **Seq Scan** on large tables (missing index), high **actual rows** vs **estimated rows** (stale statistics — run `ANALYZE`).

---

## Step 5 — Support ZIP collection

Atlassian Support requires a **support.zip** when raising a ticket for complex issues.

### Generate via Admin UI

**Admin > General Configuration > Troubleshooting and Support Tools > Create Support Zip**

Select: Application Logs, Thread Dumps, System Information, Configuration Files.

### Generate via command line

```bash
# The support zip script (ships with Confluence)
/opt/atlassian/confluence/bin/confluence-support-zip.sh \
  --output /tmp/confluence-support-$(date +%Y%m%d).zip

# If the script is unavailable, manually collect:
SUPPORT_DIR="/tmp/confluence-support-$(date +%Y%m%d)"
mkdir -p "$SUPPORT_DIR"

# Logs
cp -r /var/atlassian/application-data/confluence/logs/ "${SUPPORT_DIR}/logs/"

# Thread dumps
CONF_PID=$(pgrep -f confluence | head -1)
for i in 1 2 3; do
  jstack -l "$CONF_PID" > "${SUPPORT_DIR}/threaddump_${i}.txt"
  sleep 10
done

# Heap histogram (non-invasive)
jmap -histo:live "$CONF_PID" > "${SUPPORT_DIR}/heap_histo.txt"

zip -r "${SUPPORT_DIR}.zip" "$SUPPORT_DIR/"
echo "Support zip: ${SUPPORT_DIR}.zip"
```


```text title="Expected output"
Creating support zip for Confluence...
Gathering logs from /var/atlassian/application-data/confluence/logs/
Collecting thread dumps (3 iterations, 10s apart)...
2024-01-15 14:32:18 | Thread dump 1/3 captured (PID: 2847)
2024-01-15 14:32:28 | Thread dump 2/3 captured (PID: 2847)
2024-01-15 14:32:38 | Thread dump 3/3 captured (PID: 2847)
Generating heap histogram (non-invasive)...
Heap histogram written to /tmp/confluence-support-20240115/heap_histo.txt
  adding: confluence-support-20240115/logs/ (stored 0%)
  adding: confluence-support-20240115/threaddump_1.txt (deflated 87%)
  adding: confluence-support-20240115/threaddump_2.txt (deflated 87%)
  adding: confluence-support-20240115/threaddump_3.txt (deflated 87%)
  adding: confluence-support-20240115/heap_histo.txt (deflated 92%)
Support zip: /tmp/confluence-support-20240115.zip
```

!!! warning "Common errors"
    **`pgrep: no process found`** — Ensure Confluence is running with `systemctl status confluence` before collecting diagnostics.
    **`jstack: command not found`** — Install the JDK (not just JRE) with `apt-get install openjdk-11-jdk` or equivalent for your OS.
    **`Permission denied`** — Run the script with `sudo` or as the confluence system user to access logs and process memory.
### What support will ask for

| Artifact | Collected By |
|---|---|
| atlassian-confluence.log (full, not truncated) | Support zip |
| catalina.out | Support zip |
| Thread dumps × 3 (10s apart) | Support zip / jstack |
| Heap dump or histogram | jmap |
| Confluence version and build number | Admin > System Information |
| DB version and table sizes | psql |
| Steps to reproduce | Your ticket description |
| Time of issue occurrence (with timezone) | Your ticket description |

---

## Log locations

| Log | Path | What to look for |
|---|---|---|
| Application log | `CONFLUENCE_HOME/logs/atlassian-confluence.log` | Plugin errors, macro failures, auth exceptions |
| Tomcat stdout | `CONFLUENCE_INSTALL/logs/catalina.out` | JVM startup, OOM, thread dump output |
| PostgreSQL slow queries | `/var/log/postgresql/postgresql-*.log` | Queries exceeding `log_min_duration_statement` |
| Hazelcast log | `catalina.out` (Data Center) | Cluster membership changes, split-brain events |
| Access log | `CONFLUENCE_INSTALL/logs/confluence-access.log` | HTTP request timing per URL |
| Support ZIP | `/tmp/confluence-support-*.zip` | All-in-one — required for Atlassian SR |

---

## See also

- [Confluence — Common Issues](../common-issues/)
- [Confluence — Escalation](../escalation/)
- [Confluence — Health Checks](../../operations/health-checks/)

## Verify resolution

- `curl -s http://localhost:8090/status` returns `{"state":"RUNNING"}`
- `jstat -gcutil $CONF_PID 5000 3` shows Old generation (O) below 80% between GC cycles
- `grep -c "BLOCKED" /tmp/threaddump_1_*.txt` returns a low count (< 5)
- A Confluence page in the affected space renders in under 3 seconds
- `grep -i "OOM\|OutOfMemoryError" /opt/atlassian/confluence/logs/catalina.out` returns no new entries after the fix
- PostgreSQL active query count is normal: `SELECT count(*) FROM pg_stat_activity WHERE state != 'idle'`
