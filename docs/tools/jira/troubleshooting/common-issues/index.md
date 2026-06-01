# Jira — Common Issues


<div class="kb-summary">
Common Issues reference covering Quick Reference Table, OutOfMemoryError (OOM), Slow Board Loading, LDAP Sync Failures, Workflow Transition Failures and 3 more sections.
</div>

## Quick Reference Table

| Issue | Symptom | Primary Cause | First Action |
|---|---|---|---|
| OutOfMemoryError | JVM crash, slow response, catalina.out error | Heap too small / memory leak | Increase heap, analyse heap dump |
| Slow board loading | Boards take > 10s | JQL complexity, large sprints, index stale | Optimise board filter, reindex |
| LDAP sync failure | Users can't log in, sync errors in admin | LDAP connectivity / schema mismatch | Check LDAP connectivity from app server |
| Workflow transition failure | "Transition not available" errors | Validator failure, screen misconfiguration | Check workflow conditions and validators |
| Email notification failure | No emails sent | SMTP misconfiguration, SMTP server down | Test SMTP from admin UI |
| Search index corruption | Missing search results, index errors | Unclean shutdown, disk issue | Force full reindex |
| Plugin failures | App disabled after upgrade | Compatibility mismatch | Check Marketplace compatibility, update app |
| High DB connection usage | "Unable to get JDBC connection" | Pool exhausted, long-running queries | Increase pool size, kill blocking queries |
| Attachment upload failure | Error on file attach | Shared home full or permissions | Check disk space and file permissions |
| Cluster node missing | Node absent from Admin → Clustering | Node crash, network partition | Check heartbeat, restart node |

---

## OutOfMemoryError (OOM)

### Symptoms

- Jira becomes unresponsive
- `catalina.out` contains `java.lang.OutOfMemoryError: Java heap space`
- Frequent full GC events in GC log
- Jira spontaneously restarts

### Diagnosis

```bash
# Check for OOM events in the last 24h
grep -i "OutOfMemoryError\|Java heap space\|GC overhead\|heap dump" \
  /opt/atlassian/jira/logs/catalina.out | tail -30

# Check GC log for frequent full GC
grep "Pause Full" /opt/atlassian/jira/logs/gc.log | tail -20

# Current heap usage (if Jira is running)
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)
jcmd "${JIRA_PID}" GC.heap_info
```
┌──────────────────────────────────────── Jira — Common Issues ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Jira Frequent Issue Patterns                                 │   │
│   │         OOM crash: heap too small; increase -Xmx in setenv.sh; check for plugin leaks         │   │
│   │          Slow issues: DB slow queries or GC pressure; check pg_stat_activity + GC log         │   │
│   │         Search broken: Lucene index stale; trigger full reindex from Admin > Indexing         │   │
│   │         Workflow stuck: check conditions/validators; view workflow in project settings        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Most Jira issues: memory, performance, search, workflow, or authentication                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                    Issue                     │  │                  Resolution                 │   │
│   │                 OOM / crash                  │  │         Increase -Xmx; check plugins        │   │
│   │               Slow page loads                │  │              DB index; tune GC              │   │
│   │                 Search stale                 │  │           Full reindex from admin           │   │
│   │                Workflow stuck                │  │         Check conditions/validators         │   │
│   │               SAML login fails               │  │            Check IdP cert expiry            │   │
│   │               Attachments 404                │  │            Remount NFS JIRA_HOME            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Jira VMs · PostgreSQL · NFS home · IdP (Okta/ADFS) · load balancer                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  -Xmx         = JVM max heap; set in JIRA_INSTALL/bin/setenv.sh                                       │
│  GC pressure  = excessive garbage collection; heap too small; increase -Xmx                           │
│  Full reindex = Admin > System > Indexing > Full Re-Index; fixes search issues                        │
│  Condition    = workflow transition prerequisite; check in Project > Workflows                        │
│  Validator    = field check before transition; fix fields or disable validator                        │
│  SAML cert    = IdP signing certificate; expires on schedule; update in SAML config                   │
│  NFS remount  = umount && mount JIRA_HOME; or restart nfs-client.target                               │
│  DB index     = PostgreSQL indexes on jiraissue; check with EXPLAIN ANALYZE                           │
│  Plugin leak  = disable suspect plugin to confirm memory leak                                         │
│  LDAP sync    = Admin > User Management > User Directories > Synchronise                              │
│  Indexing     = Admin > System > Indexing; check index status and last run time                       │
│  GC log       = enable -Xlog:gc* in JVM_SUPPORT_RECOMMENDED_ARGS for analysis                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Restart Jira to apply.

**2. Capture Heap Dump for Root Cause**

```bash
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)
jmap -dump:format=b,live,file=/tmp/jira-heap.hprof "${JIRA_PID}"
```

Analyse with Eclipse Memory Analyser Tool (MAT) to identify leaking object graph.

**3. Check for Plugin Memory Leaks**

Temporarily disable recently installed or updated plugins:
`Admin → Manage Apps → [plugin] → Disable`

**4. GC Tuning**

```bash
# Add to setenv.sh JVM_SUPPORT_RECOMMENDED_ARGS
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+ExplicitGCInvokesConcurrent
-XX:G1HeapRegionSize=16m
-XX:G1ReservePercent=20
```

---

## Slow Board Loading

### Symptoms

- Scrum or Kanban boards take > 5–10 seconds to load
- High CPU on app node during board load
- Database slow query log shows board-related JQL

### Diagnosis

```bash
# Check DB slow queries during board load (enable slow query log first)
psql -h "${JIRA_DB_HOST}" -U jira -d jiradb -c "
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
WHERE query ILIKE '%jiraissue%' OR query ILIKE '%customfieldvalue%'
ORDER BY mean_exec_time DESC
LIMIT 20;"

# Check board filter JQL (get board ID from URL)
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/agile/1.0/board/42/configuration" | python3 -m json.tool
```

### Common Causes and Fixes

| Cause | Fix |
|---|---|
| Board filter returns too many issues | Narrow JQL — exclude `Done` issues older than 1 sprint |
| Missing DB indexes | Run `Admin → System → Database → Re-index DB` |
| Stale search index | `Admin → System → Indexing → Full Re-index` |
| Board has too many columns or swimlanes | Simplify board configuration |
| Large number of sub-tasks | Aggregate at Story level, reduce sub-task display |
| Custom field loaded on board | Remove unnecessary custom fields from board card display |

**Optimise Board Filter JQL:**

```jql
-- Before (returns ALL issues including resolved)
project = PROJ

-- After (only active work)
project = PROJ AND (
  sprint in openSprints()
  OR (status != Done AND updated >= -14d)
)
```

---

## LDAP Sync Failures

### Symptoms

- Users cannot log in despite valid AD credentials
- `Admin → User Management → [Directory]` shows sync errors
- Log entries: `LDAP: error code 49`, `CommunicationException`, `TimeLimitExceededException`

### Diagnosis

```bash
# Test LDAP connectivity from app server
ldapsearch -H ldaps://ad.example.com:636 \
  -D "CN=svc-jira,OU=ServiceAccounts,DC=example,DC=com" \
  -w "${LDAP_PASSWORD}" \
  -b "DC=example,DC=com" \
  "(sAMAccountName=testuser)" displayName mail

# Check Jira logs for LDAP errors
grep -i "ldap\|cwd\|crowd\|directory" \
  /opt/atlassian/jira/logs/atlassian-jira.log | grep -i "error\|warn\|fail" | tail -30
```

### Common Error Codes

| LDAP Error Code | Meaning | Fix |
|---|---|---|
| 49 | Invalid credentials | Reset service account password in Jira config |
| 32 | No such object | Base DN incorrect |
| 52e | Invalid credentials (AD-specific) | Account locked, password expired |
| 701 | Account expired | Renew service account expiry in AD |
| 773 | Password must be reset | Reset service account password |
| Connection refused | LDAP unreachable | Check firewall, LDAP server status |
| TimeLimitExceededException | LDAP query too slow | Add LDAP-side index, increase Jira timeout |

### Resolution Steps

1. Verify LDAP service account is not locked: check AD account status
2. Re-enter LDAP password in Jira: `Admin → User Management → [Directory] → Edit`
3. Trigger manual sync: `Admin → User Management → [Directory] → Synchronise`
4. If sync still fails, check LDAP server load and connection limits
5. For certificate errors (LDAPS): import LDAP server certificate to Jira JVM truststore:

```bash
keytool -importcert \
  -alias ldap-server \
  -file /tmp/ldap-server.crt \
  -keystore "${JAVA_HOME}/lib/security/cacerts" \
  -storepass changeit
```

---

## Workflow Transition Failures

### Symptoms

- Users see "Transition not available" or transition button missing
- Transition screen does not appear
- Transition succeeds for some users but not others

### Diagnosis

```bash
# Check workflow for issue type
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/transitions" | python3 -m json.tool

# Check Jira log for validator errors during transition
grep -A5 "WorkflowException\|transition.*fail\|validator" \
  /opt/atlassian/jira/logs/atlassian-jira.log | tail -40
```

### Common Causes

| Cause | Symptom | Fix |
|---|---|---|
| Condition not met | Transition not shown to user | Review workflow conditions (e.g., "User is Assignee") |
| Validator failure | Error on transition | Required field empty — check screen fields |
| Post-function error | Transition appears to succeed but state wrong | Check post-functions for script errors |
| Permission missing | Transition hidden for role | Add permission to transition condition |
| Open sub-tasks | "Close issue" blocked | Close all sub-tasks first, or remove validator |

**Inspect Workflow in Admin UI:**

`Admin → Workflows → [Workflow name] → Edit → [Transition] → Conditions / Validators / Post Functions`

---

## Email Notification Failures

### Symptoms

- No email received after issue creation, comment, or transition
- Notification scheme shows expected recipients
- No delivery errors visible in UI

### Diagnosis

```bash
# Check outgoing mail configuration
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/configuration" | python3 -m json.tool

# Test SMTP from server
telnet smtp.example.com 587

# Check Jira mail log
grep -i "mail\|smtp\|notification\|email" \
  /opt/atlassian/jira/logs/atlassian-jira.log \
  | grep -i "error\|warn\|fail" | tail -30
```

### Resolution

1. **Test SMTP via admin UI**: `Admin → System → Outgoing Mail → Test` — check if test email arrives
2. **Verify SMTP credentials**: ensure username/password or API token is current
3. **Check SMTP server logs** for authentication failures or rate limiting
4. **Check mail queue**: `Admin → System → Mail Queue` — items stuck in queue indicate delivery failure
5. **Flush mail queue**: `Admin → System → Mail Queue → Flush Queue`
6. **Check user email addresses**: ensure recipient user accounts have valid email set
7. **Check notification scheme**: `Admin → Notification Schemes → [scheme] → [event]` — verify recipients

---

## Search Index Corruption

### Symptoms

- JQL searches return no results for known issues
- `Text ~ "keyword"` returns nothing
- Log contains `IndexException`, `CorruptIndexException`
- Reindex fails mid-way

### Diagnosis

```bash
# Check index errors in log
grep -i "IndexException\|CorruptIndexException\|LockObtainFailedException" \
  /opt/atlassian/jira/logs/atlassian-jira.log | tail -20

# Check index directory size and permissions
ls -la /var/atlassian/application-data/jira/caches/indexes/
du -sh /var/atlassian/application-data/jira/caches/indexes/*
```

### Resolution

```bash
# 1. Stop Jira
systemctl stop jira

# 2. Delete index (safe — regenerated from DB)
rm -rf /var/atlassian/application-data/jira/caches/indexes/*

# 3. Start Jira
systemctl start jira

# 4. Trigger full reindex (foreground for safety)
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
  "${JIRA_URL}/rest/api/2/reindex?type=FOREGROUND"

# Monitor progress
watch -n30 "curl -s -u ${JIRA_USER}:${JIRA_TOKEN} \
  ${JIRA_URL}/rest/api/2/reindex | python3 -m json.tool"
```

A full reindex on a large instance can take 30 minutes to several hours. Schedule during low-traffic periods.

---

## Plugin / App Failures

### Symptoms

- `System error` when accessing plugin-dependent features
- `Admin → Manage Apps` shows app as `Error` state
- Log contains `PluginException`, `UnsatisfiedLinkError`, or `ClassNotFoundException`

### Diagnosis

```bash
# Check plugin-related errors
grep -i "plugin\|app\|addon\|atlassian" \
  /opt/atlassian/jira/logs/atlassian-jira.log \
  | grep -i "error\|fail\|disabled" | tail -30

# List disabled/errored plugins
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/plugins/1.0/plugin" \
  | python3 -c "
import sys, json
for p in json.load(sys.stdin):
    if not p.get('enabled', True):
        print(f\"{p.get('key')} — {p.get('name')} — {p.get('version')}\")
"
```

### Resolution Steps

1. **Check Marketplace compatibility**: Go to Marketplace → find app → check version support for Jira version
2. **Update app**: `Admin → Manage Apps → [app] → Update` (if newer version available)
3. **Disable and re-enable**: `Admin → Manage Apps → [app] → Disable → Enable`
4. **Safe mode**: Start Jira in safe mode to disable all user-installed apps:
   ```bash
   # Add to setenv.sh
   JVM_SUPPORT_RECOMMENDED_ARGS="${JVM_SUPPORT_RECOMMENDED_ARGS} -Dplugin.load.mode=SAFE"
   ```
5. **Reinstall app**: Uninstall and reinstall from Marketplace
6. **Clear plugin cache** (Data Center):
   ```bash
   systemctl stop jira
   rm -rf /var/atlassian/application-data/jira/plugins/.osgi-plugins/
   rm -rf /var/atlassian/application-data/jira/plugins/installed-plugins/
   systemctl start jira
   ```
