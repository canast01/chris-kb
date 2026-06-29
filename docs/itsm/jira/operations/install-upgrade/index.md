---
tags:
  - jira
  - operations
---
# Jira — Install and Upgrade

```bash
# List all installed apps and versions
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/plugins/1.0/plugin" \
  | python3 -c "
import sys, json
plugins = json.load(sys.stdin)
for p in plugins:
    print(f\"{p.get('key','')}\t{p.get('version','')}\t{p.get('name','')}\")
" | sort > /tmp/jira-plugins-before.txt

cat /tmp/jira-plugins-before.txt
```


```text title="Expected output"
com.atlassian.jira.plugins.jira-development-panel	1.4.8	Jira Development Panel
com.atlassian.servicedesk.servicedesk-plugin	5.11.2	Atlassian Service Desk
com.atlassian.plugins.atlassian-nav-links-plugin	5.9.14	Atlassian Navigation Links
com.atlassian.jira.plugins.jira-agile-ob	8.22.5	Jira Software
com.onresolve.jira.groovy.groovyrunner	3.3.14	ScriptRunner for Jira
com.atlassian.jira.plugins.automation	6.8.1	Automation for Jira
com.atlassian.plugins.atlassian-whitelist-api	1.2.3	Atlassian Whitelist API
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Verify JIRA_URL is correct and the Jira instance is running and accessible from this host.
    **`jq: parse error: Invalid JSON at line 1`** — Confirm JIRA_USER and JIRA_TOKEN are valid; invalid credentials may return an HTML error page instead of JSON.
    **`python3: No module named 'json'`** — Install python3-minimal or ensure python3 is properly configured on the system.
```bash
# Download installer (replace version as appropriate)
JIRA_VERSION="9.12.0"
wget "https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-${JIRA_VERSION}-x64.bin" \
  -O /tmp/jira-installer.bin

chmod +x /tmp/jira-installer.bin

# Run installer (interactive)
/tmp/jira-installer.bin

# Or with response file for silent install:
cat > /tmp/jira-response.varfile << 'EOF'
#install4j response file
sys.adminRights$Boolean=true
app.jiraHome=/var/atlassian/application-data/jira
app.install.service$Boolean=true
portChoice=default
EOF

/tmp/jira-installer.bin -q -varfile /tmp/jira-response.varfile
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jira-database-config>
  <name>defaultDS</name>
  <delegator-name>default</delegator-name>
  <database-type>postgres72</database-type>
  <schema-name>public</schema-name>
  <jdbc-datasource>
    <url>jdbc:postgresql://db.example.com:5432/jiradb</url>
    <driver-class>org.postgresql.Driver</driver-class>
    <username>jira</username>
    <password>strong-password-here</password>
    <pool-min-size>20</pool-min-size>
    <pool-max-size>100</pool-max-size>
    <pool-max-wait>30000</pool-max-wait>
    <pool-max-idle>20</pool-max-idle>
    <validation-query>select 1</validation-query>
    <min-evictable-idle-time-millis>60000</min-evictable-idle-time-millis>
    <time-between-eviction-runs-millis>300000</time-between-eviction-runs-millis>
  </jdbc-datasource>
</jira-database-config>
```
```properties
jira.node.id=jira-app-01
jira.shared.home=/var/atlassian/application-data/jira/shared
ehcache.peer.discovery=default
ehcache.listener.hostName=10.0.1.10
ehcache.listener.port=40001
ehcache.object.port=40011
```
```bash
systemctl start jira
# Complete setup wizard via browser: http://<node-ip>:8080
```
```d2
direction: right

BACKUP: "Take Backup" {shape: rectangle}
DRAIN: "Drain Node 1\nfrom LB" {shape: rectangle}
STOP1: "Stop Jira\nNode 1" {shape: rectangle}
UPGRADE1: "Upgrade\nNode 1" {shape: rectangle}
START1: "Start\nNode 1" {shape: rectangle}
POOL1: "Return Node 1\nto LB" {shape: rectangle}
NEXT: "Repeat for\nNodes 2, 3..." {shape: rectangle}
DONE: "All Nodes\nUpgraded" {shape: rectangle}
ROLLBACK: "Rollback\nNode 1" {shape: rectangle}

BACKUP -> DRAIN
DRAIN -> STOP1
STOP1 -> UPGRADE1
UPGRADE1 -> START1
POOL1 -> NEXT
NEXT -> DONE
```
```bash
# Database backup
PGPASSWORD="${JIRA_DB_PASSWORD}" pg_dump \
  -h db.example.com -U jira -Fc jiradb \
  -f /backup/jira/db/jira_pre_upgrade_$(date +%Y%m%d).pgdump

# Shared home backup
rsync -av /var/atlassian/application-data/jira/shared/ \
  /backup/jira/shared-pre-upgrade-$(date +%Y%m%d)/
```

```text title="Expected output"
pg_dump: [client_min_messages=warning] 
pg_dump: dumping database "jiradb" schema public
pg_dump: dumping database "jiradb" schema public table "cwd_user"
pg_dump: dumping database "jiradb" schema public table "jira_issue"
pg_dump: dumping database "jiradb" schema public table "jira_worklog"
pg_dump: dumping database "jiradb" schema public table "ao_60db71_board"
pg_dump: dumping database "jiradb" schema public table "ao_60db71_sprint"
sending incremental file list
shared/
shared/plugins/
shared/plugins/installed-plugins/
shared/plugins/installed-plugins/jira-misc-workflow-extensions-6.4.3.jar
shared/plugins/installed-plugins/tempo-timesheets-17.8.0.jar
shared/plugins/plugins-osgi-container/
shared/caches/
shared/caches/indexing/
shared/caches/indexing/current/
shared/caches/indexing/current/segments_1
shared/caches/indexing/current/segments.gen
sent 2,847,392,156 bytes  received 45,821 bytes  speed 18.5M/s
total size is 2,847,392,156  speedup is 1.00
```

!!! warning "Common errors"
    **`pg_dump: error: connection to server at "db.example.com" (10.45.12.8), port 5432 failed: Connection refused`** — Verify the PostgreSQL server is running and accessible from the Jira host using `psql -h db.example.com -U jira -d jiradb -c "SELECT 1"`.
    **`rsync: change_dir "/var/atlassian/application-data/jira/shared" failed: No such file or directory (2)`** — Confirm the Jira shared home path is correct and mounted; check with `ls -ld /var/atlassian/application-data/jira/shared`.
    **`FATAL: password authentication failed for user "jira"`** — Verify the JIRA_DB_PASSWORD environment variable is set correctly and matches the database user credentials.
```bash
NEW_VERSION="9.12.3"
wget "https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-${NEW_VERSION}-x64.bin" \
  -O /tmp/jira-upgrade-${NEW_VERSION}.bin
chmod +x /tmp/jira-upgrade-${NEW_VERSION}.bin
```

```text title="Expected output"
--2024-01-15 14:32:18--  https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-9.12.3-x64.bin
Resolving www.atlassian.com (www.atlassian.com)... 104.16.132.229, 104.16.133.229
Connecting to www.atlassian.com (www.atlassian.com)|104.16.132.229|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 892547821 (851M) [application/octet-stream]
Saving to: '/tmp/jira-upgrade-9.12.3.bin'

jira-upgrade-9.12.3.bin    45%[=========>          ] 382.4M  8.92MB/s  eta 52s
```

!!! warning "Common errors"
    **`wget: unable to resolve host address 'www.atlassian.com'`** — Verify network connectivity and DNS resolution; check firewall rules blocking outbound HTTPS traffic.
    **`Permission denied`** — Ensure the user running the script has write permissions to `/tmp` directory; check disk space with `df -h /tmp`.
    **`HTTP Error 404 Not Found`** — Verify the exact version number exists on Atlassian's download page and the URL format matches the current release structure.
```bash
# HAProxy — mark backend server as drain
echo "set server jira_backend/jira-app-01 state drain" \
  | socat stdio /var/run/haproxy/admin.sock

# Wait for active connections to complete (check count)
watch -n5 "echo 'show stat' | socat stdio /var/run/haproxy/admin.sock | cut -d',' -f1,2,8"
```

```text title="Expected output"
# First command (no output — command completes silently)

# Second command output (watch refreshes every 5 seconds):
Every 5.0s: echo 'show stat' | socat stdio /var/run/haproxy/admin.sock | cut -d',' -f1,2,8

pxname,svname,scur
jira_backend,jira-app-01,12
jira_backend,jira-app-02,8
jira_backend,jira-app-03,15
jira_backend,BACKEND,35

Every 5.0s: echo 'show stat' | socat stdio /var/run/haproxy/admin.sock | cut -d',' -f1,2,8

pxname,svname,scur
jira_backend,jira-app-01,8
jira_backend,jira-app-02,8
jira_backend,jira-app-03,15
jira_backend,BACKEND,31

Every 5.0s: echo 'show stat' | socat stdio /var/run/haproxy/admin.sock | cut -d',' -f1,2,8

pxname,svname,scur
jira_backend,jira-app-01,0
jira_backend,jira-app-02,8
jira_backend,jira-app-03,15
jira_backend,BACKEND,23
```

!!! warning "Common errors"
    **`socat: E Connection refused`** — Verify HAProxy is running with `systemctl status haproxy` and the admin socket exists at `/var/run/haproxy/admin.sock`.
    **`socat: E Cannot open file "/var/run/haproxy/admin.sock"`** — Ensure HAProxy is configured with `stats socket /var/run/haproxy/admin.sock mode 660 level admin` in the global section and the socket has read permissions.
```bash
systemctl stop jira
# Verify stopped
systemctl status jira
```

```text title="Expected output"
● jira.service - Atlassian JIRA
     Loaded: loaded (/etc/systemd/system/jira.service; enabled; vendor preset: disabled)
     Active: inactive (dead) since Thu 2024-01-18 14:32:15 UTC; 2s ago
    Process: 8847 ExecStart=/opt/jira/bin/start-jira.sh (code=exited, status=0/SUCCESS)
   Main PID: 8847 (code=exited, status=0/SUCCESS)
      Tasks: 0 (limit: 4915)
     Memory: 0B
        CPU: 0s
   CGroup: /system.slice/jira.service

Jan 18 14:31:22 jira-prod-01 systemd[1]: Started Atlassian JIRA.
Jan 18 14:32:15 jira-prod-01 systemd[1]: Stopping Atlassian JIRA...
Jan 18 14:32:15 jira-prod-01 systemd[1]: Stopped Atlassian JIRA.
```

!!! warning "Common errors"
    **`Failed to stop jira.service: Unit jira.service not loaded.`** — Verify the service file exists at `/etc/systemd/system/jira.service` and run `systemctl daemon-reload`.
    **`Failed to stop jira.service: Access denied`** — Run the command with `sudo` or as a user with systemctl privileges.
```bash
/tmp/jira-upgrade-${NEW_VERSION}.bin -q

# Monitor installer output
tail -f /opt/atlassian/jira/logs/atlassian-jira-software-upgrade-*.log
```

```text title="Expected output"
Unpacking JARs
Verifying checksums
Installing JIRA 8.20.6 to /opt/atlassian/jira
Stopping JIRA service
Backing up database to /var/backups/jira-8.20.5.sql
Running database migrations
Migration 1: Adding new columns to issue table... OK
Migration 2: Updating workflow schemes... OK
Migration 3: Indexing custom fields... OK
Starting JIRA service
Installation complete. JIRA 8.20.6 ready at http://localhost:8080
2024-01-15 14:32:18,445 INFO [main] Upgrade finished successfully in 287 seconds
```

!!! warning "Common errors"
    **`Permission denied`** — Run the installer with `sudo` or as the `jira` system user who owns the installation directory.
    **`No space left on device`** — Ensure at least 5GB free disk space in `/opt/atlassian/jira` and `/var/backups` before running the upgrade.
    **`Database connection refused`** — Verify the database service is running and accessible with `systemctl status postgresql` (or your DB engine) before starting the upgrade.
```bash
# Schema upgrade progress (during startup)
tail -f /opt/atlassian/jira/logs/atlassian-jira.log \
  | grep -E "schema|migration|upgrade"
```

```text title="Expected output"
2024-01-15 09:42:17,234 INFO [main] [com.atlassian.jira.upgrade.UpgradeManager] Starting schema upgrade from version 8.19.0 to 8.20.1
2024-01-15 09:42:18,567 INFO [main] [com.atlassian.jira.upgrade.SchemaUpgradeTask] Executing migration: AddColumnToIssueTable
2024-01-15 09:42:22,891 INFO [main] [com.atlassian.jira.upgrade.SchemaUpgradeTask] Migration AddColumnToIssueTable completed in 4324ms
2024-01-15 09:42:23,145 INFO [main] [com.atlassian.jira.upgrade.SchemaUpgradeTask] Executing migration: CreateIndexOnWorkflow
2024-01-15 09:42:31,456 INFO [main] [com.atlassian.jira.upgrade.SchemaUpgradeTask] Migration CreateIndexOnWorkflow completed in 8311ms
2024-01-15 09:42:31,678 INFO [main] [com.atlassian.jira.upgrade.UpgradeManager] Schema upgrade completed successfully in 14442ms
```

!!! warning "Common errors"
    **`tail: cannot open '/opt/atlassian/jira/logs/atlassian-jira.log' for reading: No such file or directory`** — Verify JIRA is installed at `/opt/atlassian/jira` and the logs directory exists, or adjust the path to match your installation.
    **`grep: (standard input): Permission denied`** — Run the command with `sudo` or ensure your user has read permissions on the log file.
```bash
systemctl start jira

# Monitor startup
tail -f /opt/atlassian/jira/logs/catalina.out \
  | grep -E "INFO|ERROR|WARN|started"

# Health check
curl -s https://jira.example.com/status
# {"state":"RUNNING"}

# Version check
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/serverInfo" | python3 -m json.tool
```

```text title="Expected output"
[1] 12345
tail: cannot open '/opt/atlassian/jira/logs/catalina.out' for reading: No such file or directory
2024-01-15 09:42:23,156 INFO [main] atlassian.jira.startup.JiraStartupListener - JIRA started successfully in 45 seconds
2024-01-15 09:42:24,203 INFO [main] atlassian.jira.startup.JiraStartupListener - Jira 8.20.6 started
2024-01-15 09:42:25,891 WARN [main] com.atlassian.jira.upgrade - Running upgrade tasks
2024-01-15 09:42:31,445 INFO [main] atlassian.jira.upgrade - Upgrade completed
{"state":"RUNNING"}
{
  "baseUrl": "https://jira.example.com",
  "version": "8.20.6",
  "versionNumbers": [8, 20, 6, 0],
  "buildNumber": 820061,
  "buildDate": "2023-11-22T00:00:00.000+0000",
  "serverTitle": "JIRA Production",
  "scmInfo": "abc1d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9"
}
```

!!! warning "Common errors"
    **`tail: cannot open '/opt/atlassian/jira/logs/catalina.out' for reading: No such file or directory`** — Check the actual JIRA_HOME location with `find / -name catalina.out 2>/dev/null` and adjust the path accordingly.
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Verify JIRA is fully started with `systemctl status jira` and that the hostname/port in the URL matches your deployment.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl to skip certificate verification, or configure proper SSL certificates in your JIRA server.xml.
```bash
echo "set server jira_backend/jira-app-01 state ready" \
  | socat stdio /var/run/haproxy/admin.sock
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`socat: E connect() failed: No such file or directory`** — Verify HAProxy is running with `systemctl status haproxy` and the admin socket path is correct in `/etc/haproxy/haproxy.cfg`.
    **`socat: E open() failed: Permission denied`** — Run the command with `sudo` or ensure your user is in the `haproxy` group with `usermod -a -G haproxy $USER`.
```bash
# Verify all apps (plugins) re-enabled
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/plugins/1.0/plugin" \
  | python3 -c "
import sys, json
plugins = json.load(sys.stdin)
disabled = [p for p in plugins if not p.get('enabled', True)]
print(f'{len(disabled)} plugin(s) disabled:')
for p in disabled:
    print(f\"  {p.get('key')} — {p.get('name')}\")
"

# Re-index if major version upgrade
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
  "${JIRA_URL}/rest/api/2/reindex?type=BACKGROUND_PREFERRED"
```

```text title="Expected output"
0 plugin(s) disabled:
{"taskId": "AO_12345678_REINDEX_001"}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Verify JIRA_URL is correct and the Jira instance is running with `systemctl status jira` or equivalent.
    **`{"errorMessages":["Authentication failed"]}`** — Confirm JIRA_USER and JIRA_TOKEN are valid and have API access permissions in Jira.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`** — Ensure the Jira REST API endpoint is accessible; check firewall rules and that the `/rest/api/2/plugins/1.0/plugin` path exists in your Jira version.
```bash
# 1. Stop Jira
systemctl stop jira

# 2. Restore application files (installer created backup in .old directory)
mv /opt/atlassian/jira /opt/atlassian/jira-failed
mv /opt/atlassian/jira.old /opt/atlassian/jira

# 3. Restore database (only if DB schema was modified)
psql -h db.example.com -U postgres \
  -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'jiradb';"
psql -h db.example.com -U postgres \
  -c "DROP DATABASE jiradb; CREATE DATABASE jiradb OWNER jira ENCODING 'UTF8';"

PGPASSWORD="${JIRA_DB_PASSWORD}" pg_restore \
  -h db.example.com -U jira -d jiradb --jobs 4 \
  /backup/jira/db/jira_pre_upgrade_$(date +%Y%m%d).pgdump

# 4. Start Jira
systemctl start jira

# 5. Validate
curl -s https://jira.example.com/status
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
WARNING:  terminating connection for user "postgres" auth method md5
       pg_terminate_backend
------------------------
                       t
                       t
                       t
(3 rows)
NOTICE:  database "jiradb" does not exist, skipping
CREATE DATABASE
pg_restore: error: could not execute query: ERROR:  role "jira" does not exist
(no output — command completes silently)
{"state":"RUNNING","buildNumber":8503,"version":"8.20.11","type":"Cloud"}
```

!!! warning "Common errors"
    **`pg_restore: error: could not execute query: ERROR:  role "jira" does not exist`** — Create the jira database role with `psql -h db.example.com -U postgres -c "CREATE ROLE jira WITH LOGIN PASSWORD 'password';"` before restoring.
    **`psql: error: connection to server at "db.example.com" (10.45.12.8), port 5432 failed`** — Verify database connectivity and that `db.example.com` is resolvable; check firewall rules and PostgreSQL service status on the remote host.
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Wait 30–60 seconds for Jira to fully start, then retry the curl command; check `systemctl status jira` and `/opt/atlassian/jira/logs/catalina.out` for startup errors.
## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Jira — Deploy](../../deploy/)
