---
tags:
  - confluence
  - troubleshooting
search:
  boost: 1.5
---
# Confluence — Common Issues

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


```text title="Expected output"
CATALINA_OPTS="-Xms1024m -Xmx2048m -XX:+UseG1GC"
CATALINA_OPTS="$CATALINA_OPTS -XX:G1HeapRegionSize=16M -XX:InitiatingHeapOccupancyPercent=35"

2024-01-15 14:32:18,445 ERROR [http-nio-8090-exec-12] [confluence.util.ConfluenceUtil] OutOfMemoryError: Java heap space
2024-01-15 14:35:22,891 ERROR [http-nio-8090-exec-8] [confluence.util.ConfluenceUtil] OutOfMemoryError: Java heap space
2024-01-15 14:38:45,123 ERROR [http-nio-8090-exec-15] [confluence.util.ConfluenceUtil] OutOfMemoryError: GC overhead limit exceeded
2024-01-15 15:02:11,456 ERROR [http-nio-8090-exec-3] [confluence.util.ConfluenceUtil] OutOfMemoryError: Java heap space

-rw-r--r-- 1 confluence confluence 1.2G Jan 15 14:35 heap_dump_2024-01-15_14-35-22.hprof
-rw-r--r-- 1 confluence confluence 1.1G Jan 15 14:38 heap_dump_2024-01-15_14-38-45.hprof

  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT
  0.00  12.45  67.89  87.34  92.11  88.76    342   18.234    12    8.567  26.801
  0.00   8.92  71.23  89.12  91.88  87.45    343   18.456    12    8.567  27.023
  0.00  15.67  58.34  91.45  92.34  89.12    344   18.678    13    9.234  27.912
  0.00   6.78  73.45  93.21  93.01  90.23    345   18.901    13    9.234  28.135
  0.00  11.34  69.12  95.67  93.45  91.56    346   19.123    14    9.901  29.024
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /var/atlassian/application-data/confluence/logs/atlassian-confluence.log: No such file or directory` | Verify the Confluence data directory path matches your installation; check `confluence.home` in `confluence.cfg.xml` or use `find / -name atlassian-confluence.log 2>/dev/null`. |
    | `pgrep: command not found` | Install `procps` package (`apt install procps` on Debian/Ubuntu or `yum install procps-ng` on RHEL/CentOS) or replace with `ps aux | grep confluence | grep -v grep | awk '{print $2}'`. |
    | `jstat: command not found` | Ensure the JDK (not just JR |
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

```text title="Expected output"
VACUUM ANALYZE
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: could not translate host name "$DB_HOST" to address: Name or service not known` | Replace `$DB_HOST` with the actual PostgreSQL hostname or IP address (e.g., `psql -h postgres.internal -U confluence_user -d confluence`). |
    | `psql: error: FATAL: role "confluence_user" does not exist` | Verify the database user exists and `$DB_USER` is set correctly; check with `psql -h $DB_HOST -U postgres -c "\du"` to list available roles. |
    | `psql: error: FATAL: database "confluence" does not exist` | Confirm the database name in `$DB_NAME` matches an existing Confluence database; list databases with `psql -h $DB_HOST -U $DB_USER -l`. |
```bash
# Check index errors
grep -E "(IndexException|LuceneIndex|index corrupt|Lucene)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -20

# Check index directory size and modification time
ls -lh /mnt/confluence-shared/index/

# Check available disk space
df -h /mnt/confluence-shared
```

```text title="Expected output"
2024-01-15 14:32:18,456 ERROR [http-nio-8090-exec-12] [com.atlassian.confluence.search.v2.lucene.LuceneIndexAccessor] Index corruption detected in segment_42
2024-01-15 14:32:19,123 WARN [http-nio-8090-exec-15] [com.atlassian.confluence.search.v2.lucene.LuceneIndexAccessor] Lucene IndexWriter lock timeout after 300s
2024-01-15 14:32:22,567 ERROR [scheduler-8] [com.atlassian.confluence.search.v2.lucene.LuceneIndexAccessor] IndexException: write.lock held by another process
2024-01-15 14:32:45,891 ERROR [http-nio-8090-exec-3] [com.atlassian.confluence.search.v2.lucene.LuceneIndexAccessor] Lucene index rebuild required

total 2.8G
drwxr-xr-x 12 confluence confluence 4.0K Jan 15 14:28 .
drwxr-xr-x  5 root      root      4.0K Jan 10 09:15 ..
-rw-r--r--  1 confluence confluence 1.2G Jan 15 14:28 segments_4
-rw-r--r--  1 confluence confluence 847M Jan 15 14:27 segments_3
-rw-r--r--  1 confluence confluence 312M Jan 15 14:26 segments_2
-rw-r--r--  1 confluence confluence  45K Jan 15 14:25 write.lock

Filesystem     Size  Used Avail Use% Mounted on
/mnt/confluence-shared  500G  487G   13G  98% /mnt/confluence-shared
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `IndexException: write.lock held by another process` | Stop the Confluence service, remove `/mnt/confluence-shared/index/write.lock`, then restart the service. |
    | `Filesystem ... 98% /mnt/confluence-shared` | Increase the mount point capacity or archive old index segments to free at least 50GB of space. |
    | `Index corruption detected in segment_42` | Trigger a manual index rebuild via Confluence Administration > Troubleshooting > Rebuild Search Index. |
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

```text title="Expected output"
/mnt/confluence-shared/index_corrupt_20240115
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   342  100   342    0     0   1205      0 --:-- --:-- --:--:--:-- --:--:--
{
  "status": "REBUILDING",
  "progress": 87
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to host.example.com port 8090: Connection refused` | Verify Confluence is running with `systemctl status confluence` and check `CF_URL` environment variable is set correctly. |
    | `jq: parse error: Invalid JSON text at line 1` | Ensure `CF_TOKEN` is valid and has search API permissions; test with `curl -s -H "Authorization: Bearer $CF_TOKEN" "${CF_URL}/rest/api/search/index"` without jq first. |
    | `mv: cannot stat '/mnt/confluence-shared/index': No such file or directory` | Confirm the shared index path matches your Confluence installation; check `confluence.cfg.xml` for the actual `confluence.home` or index location. |
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

```text title="Expected output"
# LDAP search output
dn: CN=testuser,OU=Users,DC=example,DC=com
cn: Test User
mail: testuser@example.com
sAMAccountName: testuser

search result
result: 0 Success
numResponses: 2
numEntries: 1

# Directory sync log grep results
2024-01-15 09:42:13,521 INFO [crowd-sync-scheduler-1] com.atlassian.crowd.directory.RemoteDirectory - Synchronizing directory 'LDAP Directory' (ID: 1)
2024-01-15 09:42:15,847 INFO [crowd-sync-scheduler-1] com.atlassian.crowd.directory.RemoteDirectory - Sync completed in 2326ms
2024-01-15 09:43:22,104 WARN [crowd-sync-scheduler-1] com.atlassian.crowd.directory.RemoteDirectory - Directory sync took longer than expected: 8234ms
2024-01-15 10:15:44,392 ERROR [crowd-sync-scheduler-1] com.atlassian.crowd.manager.CrowdManager - CrowdException: Failed to synchronize directory
2024-01-15 10:15:44,393 ERROR [crowd-sync-scheduler-1] com.atlassian.crowd.manager.CrowdManager - LDAPException: Referral limit exceeded
```

!!! warning "Common errors"
    **`ldapsearch: error code 49 "80090308: LdapErr: DSID-0C090446, comment: AcceptSecurityContext error, data 52e, v3839"` — Verify the service account password is correct and the account is not locked in Active Directory.
    **`ldapsearch: error code 1 "Operations error"` — Confirm the LDAP server hostname resolves correctly and port 636 is open from the Confluence server (test with `nc -zv dc01.example.com 636`).
    **`LDAPException: Referral limit exceeded` — Increase the referral limit in Confluence LDAP configuration or simplify the search base to avoid excessive referral chasing across domain controllers.
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

```text title="Expected output"
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2026 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `connect: Connection refused` | Verify the LDAP server hostname and port 636 are correct, and that the firewall allows outbound connections to that port. |
    | `verify error:num=20:unable to get local issuer certificate` | Import the LDAP server's CA certificate into Confluence's truststore or disable certificate verification if using a self-signed cert in a test environment. |
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

```text title="Expected output"
2024-01-15 14:32:18,445 ERROR [http-nio-8090-exec-12] [com.atlassian.plugins.osgi.factory.OsgiPluginFactory] PluginException: Failed to load plugin descriptor for com.example.problematic-plugin
2024-01-15 14:32:19,102 WARN [PluginEventManager] BundleException: The bundle "com.example.problematic-plugin" could not be resolved
2024-01-15 14:32:20,556 ERROR [OSGi Framework] OSGi bundle com.example.problematic-plugin:2.1.0 has unsatisfied imports: com.atlassian.confluence.api.service.v2
2024-01-15 14:33:45,201 ERROR [http-nio-8090-exec-8] [com.atlassian.plugins.osgi.factory.OsgiPluginFactory] PluginException: Plugin initialization timeout after 30000ms
2024-01-15 14:35:12,889 WARN [PluginEventManager] BundleException: Circular dependency detected in plugin chain
{
  "key": "com.example.problematic-plugin",
  "version": "2.1.0",
  "enabled": true,
  "state": "ERROR"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to confluence.example.com port 443: Connection refused` | Verify the CF_URL environment variable is set correctly and the Confluence instance is running with `systemctl status confluence`. |
    | `jq: parse error: Invalid JSON text at line 1` | Remove the `-s` flag temporarily to see the actual HTTP response, or check that the Bearer token in CF_TOKEN is valid and has API permissions. |
    | `grep: /var/atlassian/application-data/confluence/logs/atlassian-confluence.log: No such file or directory` | Verify the Confluence installation path with `find / -name atlassian-confluence.log 2>/dev/null` or check the CONFLUENCE_HOME environment variable. |
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

```text title="Expected output"
{"enabled": false}
Stopping Confluence...
If you wish to stop Confluence, run this script without any arguments
executing as current user
Waiting for Confluence to stop .... stopped
Confluence stopped successfully
Starting Confluence...
executing as current user
Confluence is starting up. Please wait, this may take a few moments...
Confluence started successfully. You can access it at http://localhost:8090/confluence
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to host` | Verify `$CF_URL` is set correctly and the Confluence instance is reachable on the network. |
    | `Permission denied` | Run the curl command and cache removal as the Confluence service user (typically `confluence`) or with `sudo`. |
    | `{"statusCode":401,"message":"Unauthorized"}` | Ensure `$CF_TOKEN` is a valid bearer token with admin permissions in Confluence. |
```bash
# Check security log for failed auth events
tail -50 /var/atlassian/application-data/confluence/logs/atlassian-confluence-security.log

# Verify the admin account is in the internal directory (failsafe)
# Admin > User Management > Users > search for "admin" → check directory source

# Check for cookie/session issues in Tomcat config
grep -E "(sessionCookieName|sessionCookiePath|secure)" \
  /opt/atlassian/confluence/conf/server.xml
```

```text title="Expected output"
2024-01-15 14:32:18,547 WARN [http-thread-234] [com.atlassian.confluence.user.ConfluenceAuthenticator] Failed login attempt for user 'jsmith' from 192.168.1.105
2024-01-15 14:33:02,891 WARN [http-thread-235] [com.atlassian.confluence.user.ConfluenceAuthenticator] Failed login attempt for user 'admin' from 192.168.1.110
2024-01-15 14:35:41,123 ERROR [http-thread-240] [com.atlassian.confluence.user.ldap.LdapAuthenticator] LDAP connection timeout after 5000ms
2024-01-15 14:36:15,456 WARN [http-thread-241] [com.atlassian.confluence.user.ConfluenceAuthenticator] Failed login attempt for user 'mchen' from 192.168.1.108
2024-01-15 14:37:22,789 INFO [http-thread-242] [com.atlassian.confluence.user.ConfluenceAuthenticator] Successful login for user 'admin' from 192.168.1.102
2024-01-15 14:38:09,234 WARN [http-thread-243] [com.atlassian.confluence.user.ConfluenceAuthenticator] Failed login attempt for user 'jsmith' from 192.168.1.105
...
    <sessionCookieName>JSESSIONID</sessionCookieName>
    <sessionCookiePath>/</sessionCookiePath>
    <sessionCookieSecure>true</sessionCookieSecure>
    <sessionCookieHttpOnly>true</sessionCookieHttpOnly>
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `tail: cannot open '/var/atlassian/application-data/confluence/logs/atlassian-confluence-security.log' for reading: No such file or directory` | Verify the Confluence data directory path with `echo $CONFLUENCE_HOME` and adjust the path accordingly, or check if the security log is in a different location like `/opt/atlassian/confluence/logs/`. |
    | `grep: /opt/atlassian/confluence/conf/server.xml: No such file or directory` | Confirm the Confluence installation directory by running `find / -name server.xml -path "*/confluence/*" 2>/dev/null` and update the path in the grep command. |
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

```text title="Expected output"
$2a$10$kL9mN2pQrStUvWxYzAbCdeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJ
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: connection to server at "db.internal.local" (10.42.1.15), port 5432 failed` | Verify `$DB_HOST`, `$DB_USER`, and `$DB_NAME` environment variables are set correctly and the database is accessible from this host. |
    | `ERROR: column "credential" does not exist` | Confirm the Confluence database schema version; use `\d cwd_user` in psql to verify the correct column name (may be `password_hash` in newer versions). |
    | `ERROR: more than one row returned by subquery used as an expression` | Multiple internal directories exist; specify the exact directory ID in the WHERE clause or filter by `directory_type = 'INTERNAL'`. |
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

```text title="Expected output"
/dev/nfs-server:/export/confluence on /mnt/confluence-shared type nfs4 (rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=10.42.8.15,local_lock=none,addr=10.42.8.10)
Filesystem     Size  Used Avail Use% Mounted on
/dev/nfs-server:/export/confluence  500G  387G  113G  78% /mnt/confluence-shared
Write OK
{
  "attachmentMaxSize": 26214400,
  "attachmentExtensions": {
    "allowed": [
      "pdf",
      "doc",
      "docx",
      "xls",
      "xlsx",
      "ppt",
      "pptx",
      "jpg",
      "png",
      "gif"
    ],
    "banned": [
      "exe",
      "bat",
      "sh",
      "cmd"
    ]
  },
  "enabled": true
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `mount | grep confluence: command not found` | Ensure you're running this on the Confluence server itself, not a client machine; if using a container, verify the NFS mount exists in the pod spec. |
    | `Write FAILED` | Check NFS mount permissions with `ls -ld /mnt/confluence-shared` and verify the Confluence process user (typically `confluence`) has write access via `sudo -u confluence touch /mnt/confluence-shared/test`. |
    | `jq: command not found` | Install jq with `apt-get install jq` (Debian/Ubuntu) or `yum install jq` (RHEL/CentOS), or pipe the curl output to `python3 -m json.tool` instead. |
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

```text title="Expected output"
(no output — command completes silently)
{"success":true,"attachmentSize":209715200}
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to host: Name or service not known` | Verify `$CF_URL` is set correctly and the Confluence server is reachable via `ping` or `curl -v`. |
    | `umount: /mnt/confluence-shared: target is busy` | Close all open files on the mount point with `lsof /mnt/confluence-shared` and kill processes, or use `umount -l` for lazy unmount. |
    | `mount.nfs: access denied by server while mounting nfs-server:/confluence-shared` | Check NFS server exports with `showmount -e nfs-server` and verify the client IP is authorized in `/etc/exports`. |
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

```text title="Expected output"
used | max_conn
------+----------
   42 |      100
(1 row)

 pid  |   duration   | state  |                          query
------+--------------+--------+------------------------------------------------------------
 8472 | 00:02:15.342 | active | SELECT * FROM large_table WHERE id > 1000000 LIMIT 50000;
 9156 | 00:01:47.891 | active | UPDATE inventory SET stock = stock - 1 WHERE sku = $1;
 7823 | 00:00:35.127 | active | VACUUM ANALYZE customer_transactions;
(3 rows)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: connection to server at "db-prod-01.internal" (10.24.8.15), port 5432 failed: Connection refused` | Verify the PostgreSQL service is running on the target host with `systemctl status postgresql` and confirm `$DB_HOST` is correct. |
    | `psql: error: FATAL: Ident authentication failed for user "confluence_user"` | Check that the PostgreSQL `pg_hba.conf` allows the connection method for your user and host, or use password authentication with a `.pgpass` file. |
    | `psql: error: FATAL: database "confluence_prod" does not exist` | Confirm the database name in `$DB_NAME` matches an existing database by running `psql -l` on the target host. |
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

```text title="Expected output"
pg_terminate_backend
─────────────────────
 t
 t
 f
 t
(4 rows)

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: FATAL: Ident authentication failed for user "postgres"` | Ensure the postgres system user can connect without a password by using `sudo -u postgres psql` or configure `.pgpass` with proper permissions (600). |
    | `ERROR: must be superuser to execute ALTER SYSTEM` | Connect as the actual postgres superuser account; if using a service account, grant superuser privileges with `ALTER USER "$DB_USER" SUPERUSER;` or use the postgres system user directly. |
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

```text title="Expected output"
10.0.1.10
10.0.1.11
10.0.1.12
10.0.1.13
Connection to 10.0.1.12 5801 port [tcp/*] succeeded!
OK
2024-01-15 09:42:13,521 INFO [ClusterService] MemberJoined: Member(address=10.0.1.11:5801, uuid=a7f3-4b2c-9e1d)
2024-01-15 09:42:14,105 INFO [Hazelcast] Cluster state: ACTIVE, members: 4
2024-01-15 09:42:15,342 INFO [ClusterService] MemberJoined: Member(address=10.0.1.13:5801, uuid=c2e8-7a1f-5d4a)
2024-01-15 09:43:22,891 WARN [Hazelcast] High memory usage detected: 87%
2024-01-15 09:44:01,567 INFO [ClusterService] Heartbeat received from 10.0.1.10:5801
2024-01-15 09:45:33,219 ERROR [ClusterService] MemberLeft: Member(address=10.0.1.12:5801, uuid=b5d2-3c9f-1e7a) - timeout
2024-01-15 09:45:34,443 INFO [Hazelcast] Cluster state: DEGRADED, members: 3
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to confluence.example.com port 443: Connection refused` | Verify Confluence is running with `systemctl status confluence` and check firewall rules allow port 443 inbound. |
    | `nc: getaddrinfo: Name or service not known` | Ensure the hostname/IP 10.0.1.12 is correct and resolvable; verify network connectivity with `ping 10.0.1.12`. |
    | `grep: /var/atlassian/application-data/confluence/logs/atlassian-confluence.log: No such file or directory` | Confirm the Confluence installation path and log location; check with `find / -name atlassian-confluence.log 2>/dev/null`. |
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

```text title="Expected output"
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
num  target     prot opt source               destination
42   ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:5801

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
num  target     prot opt source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
num  target     prot opt source               destination

/mnt/confluence-shared on /mnt/confluence-shared type nfs4 (rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=10.42.8.15,local_lock=none,addr=10.42.8.10)
/mnt/confluence-shared: mounted successfully
Stopping Confluence...
Confluence stopped.
Starting Confluence...
Confluence started successfully. PID: 8742
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `mount: /mnt/confluence-shared: special device /mnt/confluence-shared does not exist` | Verify the NFS export path exists on the server and check /etc/fstab for correct mount point definition. |
    | `iptables: No chain/target/match by that name` | Ensure iptables is installed and running; on systems using nftables, convert rules or check with `nft list ruleset | grep 5801` instead. |
    | `Connection refused` (when Confluence fails to start)` | Check that port 5801 is not already in use with `lsof -i :5801` and verify sufficient disk space with `df -h /opt/atlassian`. |
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

```text title="Expected output"
{
  "outgoingMail": {
    "absoluteLimit": 1000,
    "currentSize": 47,
    "queue": [
      {
        "id": "msg-8392",
        "recipient": "admin@company.com",
        "subject": "Confluence Notification",
        "timestamp": "2024-01-15T09:23:14Z",
        "status": "PENDING"
      },
      {
        "id": "msg-8391",
        "recipient": "user@company.com",
        "subject": "Page Update Alert",
        "timestamp": "2024-01-15T09:18:47Z",
        "status": "PENDING"
      }
    ]
  },
  "errorQueue": {
    "size": 3,
    "errors": [
      {
        "id": "err-2847",
        "recipient": "invalid@domain.local",
        "reason": "SMTPException: 550 User unknown"
      }
    ]
  }
}
2024-01-15 09:45:22,156 ERROR [mail-sender-1] MailException: Failed to send message to user@oldomain.com - SMTPException: 550 Relay access denied
2024-01-15 09:32:15,423 ERROR [mail-sender-2] JavaMailSender: Connection timeout to smtp.example.com:587 after 30000ms
2024-01-15 08:51:09,891 WARN [mail-queue] SMTPException: 421 Service not available, try again later
SMTP login OK
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `SMTPException: 550 Relay access denied` | Verify the SMTP server allows relay from the Confluence server IP or check authentication credentials in Confluence mail settings. |
    | `Connection timeout to smtp.example.com:587 after 30000ms` | Confirm the SMTP server hostname/port is correct and the firewall allows outbound connections on port 587 from the Confluence server. |
    | `curl: (7) Failed to connect to host` | Ensure `$CF_URL` and `$CF_TOKEN` environment variables are set correctly and the Confluence API is accessible. |
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
R1: "Plugin issues\n— disable suspect plugin via REST API" {shape: rectangle}
R2: "Plugin issues\n— check ac:name in page source" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Search missing pages\n— trigger full reindex from Admin Content Indexing" {shape: rectangle}
R4: "Search missing pages\n— check space permissions for search user" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "Attachment issues\n— increase limit in Admin Further Configuration" {shape: rectangle}
R6: "Attachment issues\n— fix nginx client_max_body_size setting" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "Auth and LDAP\n— trigger manual LDAP sync in User Directories" {shape: rectangle}
R8: "Auth and LDAP\n— check IdP cert expiry in SAML config" {shape: rectangle}
B5: "B5" {shape: rectangle}
R9: "Plugin issues\n— check PDF export plugin version compatibility" {shape: rectangle}
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

- [Confluence — Diagnostics](../diagnostics/)
- [Confluence — Escalation](../escalation/)
- [Confluence — Health Checks](../../operations/health-checks/)
