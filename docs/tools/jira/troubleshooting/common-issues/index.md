# Jira — Common Issues

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

```text
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
```
```bash
# Add to setenv.sh JVM_SUPPORT_RECOMMENDED_ARGS
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+ExplicitGCInvokesConcurrent
-XX:G1HeapRegionSize=16m
-XX:G1ReservePercent=20
```
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
```jql
-- Before (returns ALL issues including resolved)
project = PROJ

-- After (only active work)
project = PROJ AND (
  sprint in openSprints()
  OR (status != Done AND updated >= -14d)
)
```
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
```bash
keytool -importcert \
  -alias ldap-server \
  -file /tmp/ldap-server.crt \
  -keystore "${JAVA_HOME}/lib/security/cacerts" \
  -storepass changeit
```
```bash
# Check workflow for issue type
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/transitions" | python3 -m json.tool

# Check Jira log for validator errors during transition
grep -A5 "WorkflowException\|transition.*fail\|validator" \
  /opt/atlassian/jira/logs/atlassian-jira.log | tail -40
```
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
```bash
# Check index errors in log
grep -i "IndexException\|CorruptIndexException\|LockObtainFailedException" \
  /opt/atlassian/jira/logs/atlassian-jira.log | tail -20

# Check index directory size and permissions
ls -la /var/atlassian/application-data/jira/caches/indexes/
du -sh /var/atlassian/application-data/jira/caches/indexes/*
```
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
