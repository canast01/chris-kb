---
tags:
  - jira
  - troubleshooting
search:
  boost: 1.5
---
# Jira — Common Issues
![Jira — Common Issues](../../../../assets/itsm-jira-troubleshooting-common-issues-index.svg)


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

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1{Workflow transition\nblocked?}
    S --> B2{Project permission\nmissing?}
    S --> B3{JQL returns no\nresults unexpectedly?}
    S --> B4{Attachment upload\nfails?}
    S --> B5{Plugin incompatibility\nafter upgrade?}
    B1 -->|Yes| D1{Validator or\ncondition blocking?}
    D1 -->|Condition| R1[Workflow stuck\n— check conditions in Project Workflows]
    D1 -->|Validator| R2[Workflow stuck\n— fix required fields or disable validator]
    B2 -->|Yes| D2{User in correct\nproject role?}
    D2 -->|No| R3[Project permission\n— add user to project role in settings]
    D2 -->|Yes| R4[Project permission\n— check permission scheme for action]
    B3 -->|Yes| D3{Index stale\nor corrupt?}
    D3 -->|Yes| R5[Search stale\n— trigger full reindex from Admin Indexing]
    D3 -->|No| R6[JQL query\n— verify JQL syntax and field names]
    B4 -->|Yes| D4{NFS home\nmounted?}
    D4 -->|No| R7[Attachments 404\n— remount NFS JIRA_HOME]
    D4 -->|Yes| R8[Attachments 404\n— check attachment size limit in config]
    B5 -->|Yes| R9[Plugin issues\n— disable suspect plugin via REST API]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8,R9 section
    class B1,B2,B3,B4,B5,D1,D2,D3,D4 decision
    class S start
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Jira — Diagnostics](../diagnostics/)
- [Jira — Escalation](../escalation/)
- [Jira — Health Checks](../../operations/health-checks/)
