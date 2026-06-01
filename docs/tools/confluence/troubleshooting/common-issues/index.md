# Confluence — Common Issues


<div class="kb-summary">
Reference table of the most frequent Confluence operational problems, with root causes and resolution steps. Each issue includes the exact commands or UI steps needed to resolve it.
</div>

---

## Issue Index

| # | Issue | Primary Symptom |
|---|---|---|
| 1 | [Out of Memory (OOM)](#1-out-of-memory) | `OutOfMemoryError` in logs; service crash |
| 2 | [Slow Page Performance](#2-slow-page-performance) | Pages take > 5 s to load |
| 3 | [Search Index Failure](#3-search-index-failure) | Search returns no results or stale results |
| 4 | [LDAP Sync Issues](#4-ldap-sync-issues) | Users cannot log in; directory sync fails |
| 5 | [Plugin Conflicts](#5-plugin-conflicts) | Plugin throws errors; breaks pages |
| 6 | [Login Failures](#6-login-failures) | Users cannot authenticate |
| 7 | [Attachment Upload Failures](#7-attachment-upload-failures) | Upload errors; files not accessible |
| 8 | [Database Connection Exhaustion](#8-database-connection-exhaustion) | Errors acquiring DB connection |
| 9 | [Cluster Split-Brain (DC)](#9-cluster-split-brain-data-center) | Nodes out of sync; conflicting caches |
| 10 | [Mail Notification Failures](#10-mail-notification-failures) | Users not receiving email alerts |

---

## 1. Out of Memory

**Symptoms**

- `java.lang.OutOfMemoryError: Java heap space` in `atlassian-confluence.log`
- `java.lang.OutOfMemoryError: GC overhead limit exceeded`
- Confluence becomes unresponsive; Tomcat auto-restarts (if configured)
- JVM heap dump written to disk if `-XX:+HeapDumpOnOutOfMemoryError` is set

**Root Causes**

- Heap (`-Xmx`) sized too small for the current load or content volume
- Memory leak in a Marketplace plugin
- Excessive concurrent users or large page exports triggering bulk object allocation
- Large attachments or office document conversions exhausting memory

**Diagnosis**

```bash
# Check heap size in setenv.sh
grep -E "(Xmx|Xms)" /opt/atlassian/confluence/bin/setenv.sh

# Look for OOM events in logs
grep "OutOfMemoryError" /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -10

# Identify heap dump files
ls -lh /var/atlassian/application-data/confluence/dumps/*.hprof 2>/dev/null

# Live heap usage via JMX (requires jconsole or jstat)
CONF_PID=$(pgrep -f confluence | head -1)
jstat -gcutil "$CONF_PID" 5000 5   # 5 samples, 5-second interval
# "O" column = Old generation %. Alert if > 90% consistently
```
```
┌───────────────────────────────────── Confluence — Common Issues ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Confluence Frequent Issue Patterns                              │   │
│   │           OOM crash: heap too small; increase -Xmx; check for memory-leaking plugins          │   │
│   │         Slow pages: DB slow queries or GC pressure; check pg_stat_activity and GC log         │   │
│   │     Search broken: Lucene index stale; trigger full reindex from Admin > Content Indexing     │   │
│   │           Auth fails: LDAP sync failure or SAML cert expired; check directory config          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Most Confluence issues fall into four categories: memory, performance, search, auth                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                    Issue                     │  │                  Resolution                 │   │
│   │                 OOM / crash                  │  │         Increase -Xmx; check plugins        │   │
│   │               Slow page loads                │  │              DB index; tune GC              │   │
│   │             Search missing pages             │  │           Full reindex from admin           │   │
│   │               SAML login fails               │  │            Check IdP cert expiry            │   │
│   │               Attachments 404                │  │             Remount NFS home dir            │   │
│   │             DB connection errors             │  │              Increase pool size             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Confluence VMs · PostgreSQL · NFS home · IdP (Okta/ADFS) · load balancer                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  -Xmx         = JVM max heap; set in setenv.sh; increase if OOM crashes occur frequently              │
│  GC pressure  = garbage collection running too frequently; indicates heap too small                   │
│  Reindex      = Admin > Content Indexing > Rebuild Index; fixes stale Lucene search                   │
│  SAML cert    = IdP signing cert; expires on a schedule; update in SAML config                        │
│  NFS remount  = umount then mount; or systemctl restart nfs-client.target                             │
│  DB pool      = JDBC connection pool; increase maxPoolSize in dbconfig.xml                            │
│  GC log       = JVM GC log; enable with -Xlog:gc* in JVM args; shows pause durations                  │
│  Plugin leak  = some Confluence plugins have memory leaks; disable to test                            │
│  LDAP sync    = Admin > User Management > User Directories; trigger manual sync                       │
│  pg_stat_activity = PostgreSQL view; shows running queries; find slow or blocked queries              │
│  Content index = Lucene index managed by Confluence; stored in CONFLUENCE_HOME/index                  │
│  Attachment 404 = attachment served from NFS; NFS unavailable = 404 for all attachments               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

**Fix**

```bash
# 1. Run VACUUM ANALYZE on the Confluence database
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "VACUUM ANALYZE;"

# 2. Rebuild the search index (reduces DB fallback queries)
# Admin > General Configuration > Content Indexing > Rebuild

# 3. Disable profiling macro or limit results in Jira Issues macros
# Edit affected pages: reduce JQL result counts, add caching

# 4. Enable macro performance warnings
# Admin > General Configuration > Logging > 
#   com.atlassian.confluence.macro = WARN
```

---

## 3. Search Index Failure

**Symptoms**

- Search returns "No results found" for known content
- `lucene` or `IndexException` errors in logs
- Admin > Content Indexing shows stuck queue or error state

**Root Causes**

- Index corruption (power loss, NFS interruption, abrupt JVM kill)
- Insufficient disk space on the shared home
- Index rebuild interrupted mid-run
- Shared home NFS mount timeout causing incomplete writes

**Diagnosis**

```bash
# Check index errors
grep -E "(IndexException|LuceneIndex|index corrupt|Lucene)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -20

# Check index directory size and modification time
ls -lh /mnt/confluence-shared/index/

# Check available disk space
df -h /mnt/confluence-shared
```

**Fix**

```bash
# Option A: Partial re-index (faster; recovers without full rebuild)
# Admin > General Configuration > Content Indexing > Re-index

# Option B: Full index rebuild (use when corruption suspected)
# 1. Stop Confluence (or put in maintenance mode)
# 2. Rename or delete the corrupt index:
mv /mnt/confluence-shared/index /mnt/confluence-shared/index_corrupt_$(date +%Y%m%d)
# 3. Start Confluence — it will auto-detect missing index and start rebuild
# 4. Monitor: Admin > Content Indexing
# Note: Confluence is usable but search is degraded during rebuild

# Check rebuild progress via REST
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/search/index" | jq '{status, progress}'
```

---

## 4. LDAP Sync Issues

**Symptoms**

- New AD users cannot log in to Confluence
- Directory sync shows errors in Admin > User Directories
- `CrowdException` or `AuthenticationException` in logs

**Root Causes**

- Bind service account password expired or changed
- AD group membership filter too restrictive
- Network timeout reaching domain controller
- Nested group depth limit exceeded

**Diagnosis**

```bash
# Enable LDAP debug logging
# Admin > Logging and Profiling:
#   com.atlassian.confluence.user.crowd = DEBUG
#   com.atlassian.crowd = DEBUG

# Test LDAP connectivity from the Confluence server
ldapsearch -H ldaps://dc01.example.com:636 \
  -D "CN=svc-confluence,OU=Services,DC=example,DC=com" \
  -w "<password>" \
  -b "DC=example,DC=com" \
  "(sAMAccountName=testuser)" \
  cn mail sAMAccountName

# Check the directory sync log
grep "CrowdException\|LDAPException\|directory.*error" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -20
```

**Fix**

```bash
# 1. Update bind account password in Confluence:
# Admin > User Management > User Directories > [Directory] > Edit
# Update the "Password" field with the new service account password

# 2. Test connection using the "Test Connection" button in the directory config

# 3. Trigger manual sync:
# Admin > User Directories > [Directory] > Synchronise

# 4. If nested groups cause issues — flatten or enable nested group support:
# Admin > User Directories > [Directory] > Enable nested groups

# 5. Verify LDAP TLS cert if using ldaps://
openssl s_client -connect dc01.example.com:636 -showcerts 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## 5. Plugin Conflicts

**Symptoms**

- Pages with a specific macro fail to render (white page or macro error placeholder)
- `PluginException` or `OSGi bundle` errors in logs
- Admin > Manage Apps shows plugin in `Disabled` or `Error` state

**Root Causes**

- Plugin version incompatible with current Confluence version
- Two plugins exporting conflicting OSGi packages
- Plugin upgrade left orphaned resources

**Diagnosis**

```bash
# Find plugin errors in the log
grep -E "(PluginException|BundleException|OSGi)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -20

# Identify which macros are on a broken page:
# - View page source → search for "ac:name" attributes

# Check plugin state via REST
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/plugins/1.0/plugins/com.example.problematic-plugin" \
  | jq '{key, version, enabled, state}'
```

**Fix**

```bash
# Disable the conflicting plugin via REST
curl -s -X PUT \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/vnd.atl.plugins+json" \
  "${CF_URL}/rest/api/plugins/1.0/plugins/com.example.problematic-plugin/enabled" \
  -d '{"enabled": false}'

# Clear OSGi cache (requires restart)
rm -rf /mnt/confluence-shared/plugins-osgi-cache/*
/opt/atlassian/confluence/bin/stop-confluence.sh
/opt/atlassian/confluence/bin/start-confluence.sh

# Update plugin to latest compatible version via Admin > Manage Apps
```

---

## 6. Login Failures

**Symptoms**

- Users receive "Invalid username or password"
- Admin account locked out
- Confluence shows login page in a redirect loop

**Root Causes**

- Incorrect password or account locked in LDAP/Crowd
- Session cookie mismatch after restart (stale `JSESSIONID`)
- Internal user directory password cache stale
- Reverse proxy stripping `X-Forwarded-For` or mangling cookies

**Diagnosis**

```bash
# Check security log for failed auth events
tail -50 /var/atlassian/application-data/confluence/logs/atlassian-confluence-security.log

# Verify the admin account is in the internal directory (failsafe)
# Admin > User Management > Users > search for "admin" → check directory source

# Check for cookie/session issues in Tomcat config
grep -E "(sessionCookieName|sessionCookiePath|secure)" \
  /opt/atlassian/confluence/conf/server.xml
```

**Fix**

```bash
# Reset admin password via database (emergency access)
# 1. Generate a bcrypt hash of the new password
python3 -c "
import bcrypt
pw = b'NewAdminPass123!'
hashed = bcrypt.hashpw(pw, bcrypt.gensalt(rounds=10))
print(hashed.decode())
"

# 2. Update in the database
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "UPDATE cwd_user SET credential = '\$2a\$10\$...<hash>...'
      WHERE user_name = 'admin'
      AND directory_id = (
        SELECT id FROM cwd_directory WHERE directory_name = 'Confluence Internal Directory'
      );"

# 3. For reverse proxy login loops — ensure these headers are set:
# X-Forwarded-Proto: https
# X-Forwarded-Host: confluence.example.com
# And server.xml has: proxyName="confluence.example.com" proxyPort="443" scheme="https"
```

---

## 7. Attachment Upload Failures

**Symptoms**

- "Could not save attachment" error when uploading files
- Upload appears to succeed but file is not accessible
- Error: "The file size exceeds the allowed limit"

**Root Causes**

- Attachment size limit exceeded (default 100 MB)
- Shared home NFS mount is read-only or disconnected
- Disk full on shared home
- Reverse proxy request body size limit (nginx `client_max_body_size`)

**Diagnosis**

```bash
# Check NFS mount status
mount | grep confluence
df -h /mnt/confluence-shared

# Test write access to attachments directory
touch /mnt/confluence-shared/attachments/test_write_$(date +%s) && \
  echo "Write OK" || echo "Write FAILED"

# Check attachment size limit
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/settings/attachmentSettings" | jq '.'
```

**Fix**

```bash
# 1. Increase attachment size limit
# Admin > General Configuration > Further Configuration > Attachment Size

# Or via REST:
curl -s -X PUT -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  "${CF_URL}/rest/api/settings/attachmentSettings" \
  -d '{"attachmentSize": 209715200}'  # 200 MB in bytes

# 2. Fix nginx body size limit (nginx.conf or site config)
# client_max_body_size 250m;
# Then: nginx -s reload

# 3. Re-mount NFS if disconnected
umount /mnt/confluence-shared
mount -t nfs nfs-server:/confluence-shared /mnt/confluence-shared
```

---

## 8. Database Connection Exhaustion

**Symptoms**

- `Unable to acquire JDBC Connection` in logs
- Confluence responds slowly or returns 503
- `pg_stat_activity` shows connections at `max_connections`

**Root Causes**

- JDBC connection pool too small for peak load
- Long-running queries holding connections open
- Connection leak in a plugin
- `max_connections` on PostgreSQL too low

**Diagnosis**

```bash
# Current connection count vs maximum
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT count(*) AS used,
             (SELECT setting::int FROM pg_settings WHERE name='max_connections') AS max_conn
      FROM pg_stat_activity;"

# Identify long-running queries
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT pid, now() - query_start AS duration, state, query
      FROM pg_stat_activity
      WHERE state != 'idle'
      AND query_start < now() - interval '30 seconds'
      ORDER BY duration DESC;"
```

**Fix**

```bash
# 1. Kill long-running/stuck queries
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT pg_terminate_backend(pid)
      FROM pg_stat_activity
      WHERE state != 'idle'
      AND query_start < now() - interval '5 minutes';"

# 2. Increase connection pool in confluence.cfg.xml
# <property name="hibernate.c3p0.max_size">60</property>
# <property name="hibernate.c3p0.min_size">20</property>
# (requires restart)

# 3. Increase PostgreSQL max_connections (requires DB restart)
psql -h "$DB_HOST" -U postgres \
  -c "ALTER SYSTEM SET max_connections = 300;"
# Then restart PostgreSQL
```

---

## 9. Cluster Split-Brain (Data Center)

**Symptoms**

- Users on different nodes see different content
- Admin > Clustering shows fewer nodes than expected
- `HazelcastException` or `ClusterException` in logs

**Root Causes**

- Hazelcast port 5801 blocked between nodes (firewall rule change)
- NFS shared home mount unavailable on one node
- Node isolation during a network partition

**Diagnosis**

```bash
# Check cluster membership on each node
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/cluster/nodes" | jq '.nodes[].address'

# Test Hazelcast port reachability between nodes
nc -zv 10.0.1.12 5801 && echo "OK" || echo "BLOCKED"

# Check Hazelcast-specific logs
grep -E "(Hazelcast|ClusterService|MemberLeft|MemberJoined)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -20
```

**Fix**

```bash
# 1. Confirm firewall rules allow TCP 5801 between all cluster node IPs
iptables -L -n | grep 5801

# 2. Recheck NFS mount on isolated node
mount | grep /mnt/confluence-shared
# Remount if stale:
umount -l /mnt/confluence-shared && mount /mnt/confluence-shared

# 3. Restart the isolated node after fixing connectivity
/opt/atlassian/confluence/bin/stop-confluence.sh
/opt/atlassian/confluence/bin/start-confluence.sh

# 4. After node rejoin, verify cluster in Admin > Clustering
# 5. Flush caches: Admin > Cache Management > Flush All Caches
```

---

## 10. Mail Notification Failures

**Symptoms**

- Users not receiving comment/page/mention notifications
- Admin > Mail > Mail Error Queue contains failed messages
- `MailException` or `SMTPException` in logs

**Root Causes**

- SMTP credentials expired or incorrect
- SMTP server rejecting connections (IP allowlist, TLS cert)
- Confluence mail queue paused (can happen after upgrades)
- Invalid recipient addresses (e.g., deactivated user still subscribed)

**Diagnosis**

```bash
# Check mail queue and error queue
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/admin/mail/queue" | jq '.'

# Check logs for mail errors
grep -E "(MailException|SMTPException|JavaMailSender)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -10

# Test SMTP from the server
python3 -c "
import smtplib
s = smtplib.SMTP('smtp.example.com', 587)
s.starttls()
s.login('user@example.com', 'password')
print('SMTP login OK')
s.quit()
"
```

**Fix**

```bash
# 1. Flush the error queue
# Admin > Mail > Mail Error Queue > Resend All

# 2. Restart mail queue if paused
curl -s -X DELETE -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/admin/mail/queue"  # Flushes queue

# 3. Update SMTP credentials
# Admin > General Configuration > Mail Servers > Edit

# 4. Send test email from admin UI
# Admin > General Configuration > Mail Servers > Send Test Email
```
