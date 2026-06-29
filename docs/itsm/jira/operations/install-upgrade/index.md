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
```bash
NEW_VERSION="9.12.3"
wget "https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-${NEW_VERSION}-x64.bin" \
  -O /tmp/jira-upgrade-${NEW_VERSION}.bin
chmod +x /tmp/jira-upgrade-${NEW_VERSION}.bin
```
```bash
# HAProxy — mark backend server as drain
echo "set server jira_backend/jira-app-01 state drain" \
  | socat stdio /var/run/haproxy/admin.sock

# Wait for active connections to complete (check count)
watch -n5 "echo 'show stat' | socat stdio /var/run/haproxy/admin.sock | cut -d',' -f1,2,8"
```
```bash
systemctl stop jira
# Verify stopped
systemctl status jira
```
```bash
/tmp/jira-upgrade-${NEW_VERSION}.bin -q

# Monitor installer output
tail -f /opt/atlassian/jira/logs/atlassian-jira-software-upgrade-*.log
```
```bash
# Schema upgrade progress (during startup)
tail -f /opt/atlassian/jira/logs/atlassian-jira.log \
  | grep -E "schema|migration|upgrade"
```
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
```bash
echo "set server jira_backend/jira-app-01 state ready" \
  | socat stdio /var/run/haproxy/admin.sock
```
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
