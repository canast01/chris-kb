---
tags:
  - jira
  - troubleshooting
search:
  boost: 1.5
---
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


```text title="Expected output"
2024-01-15 14:32:18.567 [http-nio-8080-exec-42] ERROR o.a.j.util.JiraUtils - OutOfMemoryError: Java heap space
2024-01-15 14:32:19.234 [GC-Thread-1] WARN c.a.j.startup.LaunchingContext - GC overhead limit exceeded
2024-01-15 14:33:02.891 [catalina-exec-18] ERROR - Exception in thread "http-nio-8080-exec-51": java.lang.OutOfMemoryError: Java heap space
2024-01-15 14:35:44.156 [GC-Thread-2] INFO - Heap dump initiated by OutOfMemoryError hook
2024-01-15 15:12:33.445 [http-nio-8080-exec-7] ERROR - OutOfMemoryError: Java heap space at java.util.Arrays.copyOf

2024-01-15 14:32:18.891: [Pause Full (G1 Evacuation Pause) 2847M->1923M(4096M), 3.247 secs]
2024-01-15 14:33:02.156: [Pause Full (G1 Evacuation Pause) 3156M->2104M(4096M), 2.891 secs]
2024-01-15 14:35:44.723: [Pause Full (G1 Evacuation Pause) 3892M->2567M(4096M), 4.112 secs]
2024-01-15 14:38:19.445: [Pause Full (G1 Evacuation Pause) 4012M->2891M(4096M), 3.556 secs]

 garbage-first heap   total 4096M, used 3247M [0x0000000080000000, 0x0000000180000000)
  region size 2M, 1247 young (2494M), 89 survivors (178M)
 Metaspace       used 287M, committed 294M, reserved 1024M
  class space    used 31M, committed 33M, reserved 256M
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `pgrep: command not found` | Install procps-ng package with `apt-get install procps-ng` or `yum install procps-ng`. |
    | `jcmd: command not found` | Ensure JAVA_HOME is set correctly and jcmd is in PATH; typically found in `$JAVA_HOME/bin/jcmd`. |
    | `Permission denied` | Run the commands as the jira user or with sudo: `sudo -u jira jcmd <PID> GC.heap_info`. |
```bash
# Add to setenv.sh JVM_SUPPORT_RECOMMENDED_ARGS
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+ExplicitGCInvokesConcurrent
-XX:G1HeapRegionSize=16m
-XX:G1ReservePercent=20
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `setenv.sh: No such file or directory` | Verify the JIRA installation path and ensure you're editing the correct setenv.sh file in `$JIRA_HOME/bin/` or `$CATALINA_HOME/bin/`. |
    | `Permission denied` | Run the editor with appropriate permissions (sudo or as the jira service user) to modify setenv.sh. |
    | `JVM_SUPPORT_RECOMMENDED_ARGS: command not found` | Ensure you're appending these values to the existing variable using `JVM_SUPPORT_RECOMMENDED_ARGS="$JVM_SUPPORT_RECOMMENDED_ARGS -XX:+UseG1GC ..."` rather than treating it as a shell command. |
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

```text title="Expected output"
# LDAP Search Results
dn: CN=testuser,OU=Users,DC=example,DC=com
displayName: Test User
mail: testuser@example.com

# Jira Log Errors
2024-01-15 09:42:33,521 WARN [http-nio-8080-exec-12] [com.atlassian.crowd.directory.ldap.LDAPDirectory] LDAP connection pool exhausted, retrying...
2024-01-15 09:43:15,847 ERROR [scheduler_Worker-3] [com.atlassian.crowd.directory.ldap.LDAPDirectory] Failed to sync LDAP directory: javax.naming.CommunicationException: ad.example.com:636
2024-01-15 09:44:02,123 WARN [http-nio-8080-exec-5] [com.atlassian.jira.user.util.UserUtil] User directory synchronization failed for directory ID 10001
2024-01-15 09:45:33,456 ERROR [scheduler_Worker-7] [com.atlassian.crowd.directory.ldap.LDAPDirectory] LDAP bind failed: Invalid credentials for CN=svc-jira,OU=ServiceAccounts,DC=example,DC=com
2024-01-15 09:46:10,789 WARN [http-nio-8080-exec-8] [com.atlassian.crowd.directory.cwd.CrowdDirectory] Directory sync timeout after 30000ms
2024-01-15 09:47:22,234 ERROR [scheduler_Worker-2] [com.atlassian.jira.user.util.UserUtil] CWD operation failed: Connection refused to LDAP server
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ldapsearch: No such file or directory` | Install ldap-utils package with `apt-get install ldap-utils` (Debian/Ubuntu) or `yum install openldap-clients` (RHEL/CentOS). |
    | `ldapsearch: error code 49 - 80090308: LdapErr: DSID-0C090446, comment: AcceptSecurityContext error, data 52e, v3839 ref` | Verify the service account password in `${LDAP_PASSWORD}` is correct and the account is not locked in Active Directory. |
    | `javax.naming.CommunicationException: ad.example.com:636` | Check network connectivity to the LDAP server with `telnet ad.example.com 636` and verify firewall rules allow port 636 from the Jira app server. |
```bash
keytool -importcert \
  -alias ldap-server \
  -file /tmp/ldap-server.crt \
  -keystore "${JAVA_HOME}/lib/security/cacerts" \
  -storepass changeit
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `keytool error: java.lang.Exception: Input not an X.509 certificate` | Verify the certificate file is in PEM or DER format and not corrupted by running `openssl x509 -in /tmp/ldap-server.crt -text -noout`. |
    | `keytool error: java.io.FileNotFoundException: /usr/lib/jvm/java-11-openjdk-amd64/lib/security/cacerts (No such file or directory)` | Confirm `$JAVA_HOME` is set correctly with `echo $JAVA_HOME` and points to a valid JDK installation. |
    | `Certificate already exists with alias <ldap-server>` | Remove the existing certificate first with `keytool -delete -alias ldap-server -keystore "${JAVA_HOME}/lib/security/cacerts" -storepass changeit`, or use a different alias name. |
```bash
# Check workflow for issue type
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/transitions" | python3 -m json.tool

# Check Jira log for validator errors during transition
grep -A5 "WorkflowException\|transition.*fail\|validator" \
  /opt/atlassian/jira/logs/atlassian-jira.log | tail -40
```

```text title="Expected output"
{
  "expand": "transitions",
  "transitions": [
    {
      "id": "11",
      "name": "In Progress",
      "to": {
        "self": "https://jira.example.com/rest/api/2/status/3",
        "description": "This issue is being actively worked on.",
        "iconUrl": "https://jira.example.com/images/icons/statuses/inprogress.png",
        "name": "In Progress",
        "id": "3"
      }
    },
    {
      "id": "21",
      "name": "Done",
      "to": {
        "self": "https://jira.example.com/rest/api/2/status/10000",
        "description": "Work has finished on this issue.",
        "iconUrl": "https://jira.example.com/images/icons/statuses/done.png",
        "name": "Done",
        "id": "10000"
      }
    }
  ]
}
2024-01-15 09:42:17,234 ERROR [jira.workflow.WorkflowException] Transition validation failed for issue PROJ-123
2024-01-15 09:42:17,245 ERROR [jira.workflow.validator] Required field 'Resolution' is missing
2024-01-15 09:42:17,256 WARN [jira.workflow.transition] User admin attempted transition to Done but validator rejected
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to jira.example.com port 443: Connection refused` | Verify the JIRA_URL environment variable is correct and the Jira server is running and accessible from this host. |
    | `jq: command not found` | Install jq (`apt-get install jq` or `yum install jq`) or use `python3 -m json.tool` as shown in the example. |
    | `grep: /opt/atlassian/jira/logs/atlassian-jira.log: No such file or directory` | Confirm the Jira installation path and check the actual log location with `find /opt/atlassian -name "atlassian-jira.log"`. |
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

```text title="Expected output"
{
  "baseUrl": "https://jira.company.internal",
  "title": "Company JIRA Instance",
  "mailServers": [
    {
      "name": "Default SMTP",
      "host": "smtp.example.com",
      "port": 587,
      "username": "jira-notifications@company.com",
      "protocol": "smtp"
    }
  ],
  "notificationScheme": "Default Notification Scheme"
}
Trying 192.0.2.45...
Connected to smtp.example.com.
Escape character is '^]'.
220 smtp.example.com ESMTP ready
^]
quit
221 2.0.0 closing connection
2024-01-15 14:32:18,456 WARN [mail.outgoing.MailQueue] Failed to send notification to user admin: Connection timeout to smtp.example.com:587
2024-01-15 14:33:02,123 ERROR [mail.outgoing.MailQueue] SMTP authentication failed for jira-notifications@company.com: Invalid credentials
2024-01-15 14:35:45,789 WARN [notification.DefaultNotificationService] Email notification skipped: Mail server not configured
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to jira.example.com port 443: Connection refused` | Verify `${JIRA_URL}` is correct and Jira service is running with `systemctl status jira`. |
    | `telnet: Unable to connect to remote host: Connection timed out` | Check firewall rules allow outbound traffic on port 587 and SMTP server hostname is resolvable with `nslookup smtp.example.com`. |
    | `grep: /opt/atlassian/jira/logs/atlassian-jira.log: No such file or directory` | Confirm Jira installation path and check actual log location with `find /opt/atlassian -name "atlassian-jira.log" 2>/dev/null`. |
```bash
# Check index errors in log
grep -i "IndexException\|CorruptIndexException\|LockObtainFailedException" \
  /opt/atlassian/jira/logs/atlassian-jira.log | tail -20

# Check index directory size and permissions
ls -la /var/atlassian/application-data/jira/caches/indexes/
du -sh /var/atlassian/application-data/jira/caches/indexes/*
```

```text title="Expected output"
2024-01-15 14:32:18,445 ERROR [http-nio-8080-exec-12] [com.atlassian.jira.index.DefaultIndexManager] CorruptIndexException: _0.cfs (No such file or directory)
2024-01-15 14:32:19,102 ERROR [http-nio-8080-exec-15] [org.apache.lucene.index.IndexWriter] LockObtainFailedException: Lock held by another process: /var/atlassian/application-data/jira/caches/indexes/write.lock
2024-01-15 14:32:45,667 WARN [scheduler_Worker-11] [com.atlassian.jira.index.DefaultIndexManager] IndexException: Error occurred while indexing issue PROJ-1234

total 48
drwxr-xr-x  8 jira jira  4096 Jan 15 14:28 .
drwxr-xr-x 12 jira jira  4096 Jan 15 14:15 ..
drwxr-xr-x  2 jira jira  4096 Jan 15 14:28 issue
drwxr-xr-x  2 jira jira  4096 Jan 15 14:28 comment
drwxr-xr-x  2 jira jira  4096 Jan 15 14:28 change_history
-rw-r--r--  1 jira jira    128 Jan 15 14:28 write.lock

2.3G	/var/atlassian/application-data/jira/caches/indexes/issue
1.8G	/var/atlassian/application-data/jira/caches/indexes/comment
456M	/var/atlassian/application-data/jira/caches/indexes/change_history
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `LockObtainFailedException: Lock held by another process` | Stop the JIRA service, remove `/var/atlassian/application-data/jira/caches/indexes/write.lock`, then restart the service. |
    | `CorruptIndexException: _0.cfs (No such file or directory)` | Delete the corrupted index directory and trigger a full re-index via JIRA Administration > System > Indexing > Re-Index All Issues. |
    | `Permission denied` when listing indexes directory` | Ensure the jira user owns the indexes directory with `sudo chown -R jira:jira /var/atlassian/application-data/jira/caches/indexes/`. |
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

```text title="Expected output"
$ systemctl stop jira
$ rm -rf /var/atlassian/application-data/jira/caches/indexes/*
$ systemctl start jira
$ curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
>   "${JIRA_URL}/rest/api/2/reindex?type=FOREGROUND"
{
  "currentIndex": 12847,
  "currentIndexPercentage": 0,
  "description": "Reindexing Jira",
  "entityCount": 12847,
  "progressUrl": "/secure/admin/IndexProgress.jspa"
}
$ watch -n30 "curl -s -u ${JIRA_USER}:${JIRA_TOKEN} \
>   ${JIRA_URL}/rest/api/2/reindex | python3 -m json.tool"
Every 30.0s: curl -s -u admin:****** http://jira.internal:8080/rest/api/2/reindex | python3 -m json.tool
{
  "currentIndex": 3421,
  "currentIndexPercentage": 26,
  "description": "Reindexing Jira",
  "entityCount": 12847,
  "progressUrl": "/secure/admin/IndexProgress.jspa"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to jira.internal port 8080: Connection refused` | Wait 30–60 seconds for Jira to fully start before triggering reindex; check `systemctl status jira` to confirm the service is running. |
    | `error: JIRA_USER or JIRA_TOKEN not set` | Export the environment variables before running the curl commands: `export JIRA_USER="admin" JIRA_TOKEN="your-api-token"`. |
    | `"errorMessages": ["You do not have permission to administer Jira"]` | Ensure the JIRA_USER account has Jira System Administrator permissions in the user directory. |
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

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "Workflow stuck\n— check conditions in Project Workflows" {shape: rectangle}
R2: "Workflow stuck\n— fix required fields or disable validator" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Project permission\n— add user to project role in settings" {shape: rectangle}
R4: "Project permission\n— check permission scheme for action" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "Search stale\n— trigger full reindex from Admin Indexing" {shape: rectangle}
R6: "JQL query\n— verify JQL syntax and field names" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "Attachments 404\n— remount NFS JIRA_HOME" {shape: rectangle}
R8: "Attachments 404\n— check attachment size limit in config" {shape: rectangle}
B5: "B5" {shape: rectangle}
R9: "Plugin issues\n— disable suspect plugin via REST API" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "B4" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
D4 -> R7
D4 -> R8
B5 -> R9
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
