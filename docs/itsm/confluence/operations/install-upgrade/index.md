---
tags:
  - confluence
  - operations
---
# Confluence — Install and Upgrade

```bash
# Record current version
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/settings/systemInfo" \
  | jq '{version, buildNumber}'

# List installed apps and versions
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/plugins/1.0/" \
  | jq '.plugins[] | {key: .key, version: .version, enabled: .enabled}'
```


```text title="Expected output"
{
  "version": "7.19.17",
  "buildNumber": "9127"
}
{
  "key": "com.atlassian.confluence.extra.widgetconnector",
  "version": "1.5.2",
  "enabled": true
}
{
  "key": "com.atlassian.confluence.extra.sharepoint",
  "version": "6.8.1",
  "enabled": true
}
{
  "key": "com.atlassian.upm.atlassian-universal-plugin-manager-plugin",
  "version": "4.4.15",
  "enabled": true
}
{
  "key": "com.atlassian.confluence.plugins.confluence-mobile-app-plugin",
  "version": "2.3.8",
  "enabled": false
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify the Confluence hostname/URL is correct and the service is running with `systemctl status confluence`.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure `$CF_TOKEN` is valid and the API endpoint is accessible; test with `curl -s -H "Authorization: Bearer $CF_TOKEN" "https://confluence.example.com/rest/api/settings/systemInfo"` to see the actual response.
    **`curl: (401) Unauthorized`** — Regenerate the API token in Confluence user settings and confirm it has admin permissions for REST API access.
```bash
# Back up the install directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp -rp /opt/atlassian/confluence /opt/atlassian/confluence_backup_${TIMESTAMP}

# Back up the local home
cp -rp /var/atlassian/application-data/confluence \
  /var/atlassian/application-data/confluence_backup_${TIMESTAMP}

echo "Backup created: confluence_backup_${TIMESTAMP}"
```

```text title="Expected output"
Backup created: confluence_backup_20240315_143827
```

!!! warning "Common errors"
    **`cp: cannot open '/opt/atlassian/confluence' for reading: No such file or directory`** — Verify Confluence is installed at `/opt/atlassian/confluence` or adjust the path to match your installation directory.
    **`cp: cannot create directory '/opt/atlassian/confluence_backup_20240315_143827': Permission denied`** — Run the script with `sudo` or ensure the user has write permissions to `/opt/atlassian/`.
    **`cp: cannot open '/var/atlassian/application-data/confluence' for reading: No such file or directory`** — Check that the Confluence home directory exists at the specified path, or update it to match your `confluence.home` configuration.
```bash
# Make the installer executable
chmod +x atlassian-confluence-9.x.x-x64.bin

# Run the installer (interactive)
./atlassian-confluence-9.x.x-x64.bin

# The installer will:
# 1. Detect existing installation
# 2. Offer "Upgrade existing installation"
# 3. Confirm install directory and home directory
# 4. Upgrade application files

# For unattended/automated upgrades, use a response file:
./atlassian-confluence-9.x.x-x64.bin -q -varfile response.varfile
```
```properties
app.install.service$Boolean=true
existingInstallationDir=/opt/atlassian/confluence
sys.confirmedUpdateInstallationString=true
launch.application$Boolean=false
```
```bash
INSTALL_DIR="/opt/atlassian/confluence"
BACKUP_DIR="/opt/atlassian/confluence_backup_${TIMESTAMP}"

# Compare and restore JVM settings
diff "${BACKUP_DIR}/bin/setenv.sh" "${INSTALL_DIR}/bin/setenv.sh"
# Manually apply custom -Xmx, -Xms, -D flags to the new setenv.sh

# Compare and restore server.xml
diff "${BACKUP_DIR}/conf/server.xml" "${INSTALL_DIR}/conf/server.xml"
# Re-apply: port overrides, TLS config, AJP settings, proxyName/proxyPort
```

```text title="Expected output"
--- /opt/atlassian/confluence_backup_20240115_143022/bin/setenv.sh
+++ /opt/atlassian/confluence_backup_20240115_143022/bin/setenv.sh
@@ -12,7 +12,7 @@
 # JVM memory settings
-CATALINA_OPTS="-Xms2048m -Xmx4096m -XX:+UseG1GC"
+CATALINA_OPTS="-Xms1024m -Xmx2048m -XX:+UseG1GC"
 
 # Custom properties
-CATALINA_OPTS="${CATALINA_OPTS} -Dconfluence.home=/var/atlassian/confluence"
+CATALINA_OPTS="${CATALINA_OPTS} -Dconfluence.home=/mnt/confluence-data"

--- /opt/atlassian/confluence_backup_20240115_143022/conf/server.xml
+++ /opt/atlassian/confluence_backup_20240115_143022/conf/server.xml
@@ -45,8 +45,8 @@
     <Connector port="8090" protocol="HTTP/1.1"
                connectionTimeout="20000"
-               proxyName="confluence.internal.corp"
-               proxyPort="443"
+               proxyName="confluence.prod.example.com"
+               proxyPort="8090"
                redirectPort="8443" />
 
     <Connector port="8009" protocol="AJP/1.3"
```

!!! warning "Common errors"
    **`diff: /opt/atlassian/confluence_backup_20240115_143022/bin/setenv.sh: No such file or directory`** — Verify the TIMESTAMP variable is set correctly and the backup directory exists with `ls -la "${BACKUP_DIR}"`.
    **`Permission denied`** — Run the diff commands with `sudo` or ensure the confluence system user has read access to both backup and installation directories.
```bash
# Start the application
/opt/atlassian/confluence/bin/start-confluence.sh

# Tail the startup log
tail -f /var/atlassian/application-data/confluence/logs/atlassian-confluence.log

# For Data Center: Confluence will run database schema migrations on first start
# This can take 10–60 minutes for large databases — do NOT interrupt
```
```text
INFO  [main] [DatabaseUpgradeTask] Running upgrade task: UpgradeTask_Build_XXXXX
INFO  [main] [DatabaseUpgradeTask] Upgrade task completed in 12345ms
INFO  [main] [ConfluenceBootstrapManager] Bootstrap complete
```
```bash
# On each remaining node:
# 1. Run installer (same procedure as above)
# 2. Start Confluence
# 3. Verify it joins the cluster: Admin > Clustering

# Verify cluster membership via REST
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/cluster/nodes" \
  | jq '.nodes[] | {address, state}'
```

```text title="Expected output"
{
  "address": "10.42.18.5:8091",
  "state": "JOINED"
}
{
  "address": "10.42.18.6:8091",
  "state": "JOINED"
}
{
  "address": "10.42.18.7:8091",
  "state": "JOINED"
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify the Confluence service is running on the target node with `systemctl status confluence` and check network connectivity to the cluster endpoint.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure the API token in `$CF_TOKEN` is valid and has cluster API permissions; test with `curl -s -H "Authorization: Bearer $CF_TOKEN" "https://confluence.example.com/rest/api/cluster/nodes"` without piping to jq first.
    **`"state": "JOINING"`** — The node is still synchronizing with the cluster; wait 2-3 minutes and retry the curl command, as initial state synchronization can take time.
```bash
# View upgrade task history in the database
psql -h db.internal.example.com -U confluence -d confluencedb \
  -c "SELECT classname, ranon FROM JIRAACTION ORDER BY ranon DESC LIMIT 20;"

# Check for failed upgrade tasks
grep -E "(UpgradeTask.*FAILED|upgrade.*failed)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log
```

```text title="Expected output"
classname                          | ranon
------------------------------------+----------------------------
 com.atlassian.confluence.upgrade.UpgradeTask_20230815 | 2024-01-15 14:32:18.547
 com.atlassian.confluence.upgrade.UpgradeTask_20230801 | 2024-01-15 14:31:45.223
 com.atlassian.confluence.upgrade.UpgradeTask_20230715 | 2024-01-15 14:31:12.891
 com.atlassian.confluence.upgrade.UpgradeTask_20230620 | 2024-01-15 14:30:38.556
 com.atlassian.confluence.upgrade.UpgradeTask_20230501 | 2024-01-15 14:29:55.334
 com.atlassian.confluence.upgrade.UpgradeTask_20230315 | 2024-01-15 14:29:12.778
(6 rows)

2024-01-15 14:35:22,156 INFO [UpgradeTask_20230815] Upgrade task completed successfully
2024-01-15 14:31:45,223 INFO [UpgradeTask_20230801] Upgrade task completed successfully
```

!!! warning "Common errors"
    **`psql: error: connection to server at "db.internal.example.com" (10.45.67.89), port 5432 failed: Connection refused`** — Verify the PostgreSQL service is running on the database host and the hostname/port are correct.
    **`grep: /var/atlassian/application-data/confluence/logs/atlassian-confluence.log: No such file or directory`** — Confirm Confluence is installed and the log directory path matches your installation; check the CONFLUENCE_HOME environment variable.
```bash
# Export current plugin list with versions
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/plugins/1.0/" \
  | jq -r '.plugins[] | select(.userInstalled == true) | "\(.key)\t\(.version)\t\(.enabled)"' \
  > plugins_before_upgrade.tsv

cat plugins_before_upgrade.tsv
```

```text title="Expected output"
com.atlassian.confluence.extra.confluence-mobile-app	7.19.0	true
com.atlassian.confluence.extra.office-connector	5.3.4	true
com.gliffy.confluence.plugins.gliffy-diagram	2.8.15	true
com.atlassian.jira.confluence	3.9.12	true
com.atlassian.upm.atlassian-universal-plugin-manager	4.4.8	true
com.atlassian.confluence.extra.webdav	5.1.2	false
com.atlassian.confluence.plugins.confluence-content-formatting-macros	1.5.3	true
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify the Confluence server hostname is correct and the instance is running and accessible from your network.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure the API token in `$CF_TOKEN` is valid and has the `read:plugins` permission scope.
    **`curl: (401) Unauthorized`** — Regenerate the API token in Confluence and verify it's exported correctly with `echo $CF_TOKEN`.
```bash
# Check for plugins that failed to start post-upgrade
grep -E "(Plugin.*FAILED|PluginException|osgi.*error)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log \
  | grep -i plugin | tail -30

# Admin UI: Admin > Manage Apps — filter by "Needs update" or "Incompatible"
```

```text title="Expected output"
2024-01-15 09:47:23,521 ERROR [http-nio-8090-exec-12] [com.atlassian.plugin.osgi.container.OsgiContainerManager] Plugin com.atlassian.confluence.extra.officeconnector failed to start
2024-01-15 09:47:24,103 ERROR [http-nio-8090-exec-12] [com.atlassian.plugin.manager.DefaultPluginManager] PluginException: Unable to load plugin descriptor for com.atlassian.confluence.extra.officeconnector
2024-01-15 09:47:25,667 WARN [http-nio-8090-exec-15] [com.atlassian.plugin.osgi.container.PackageExports] osgi.container error: Missing required bundle com.atlassian.confluence.extra.officeconnector v5.1.4
2024-01-15 09:47:26,441 ERROR [http-nio-8090-exec-18] [com.atlassian.plugin.classloader.PluginClassLoader] Plugin com.example.custom-macro FAILED - ClassNotFoundException: com.example.CustomMacroImpl
2024-01-15 09:47:27,892 WARN [http-nio-8090-exec-20] [com.atlassian.plugin.osgi.factory.OsgiPluginFactory] Plugin state FAILED for com.atlassian.confluence.extra.sharepoint-connector
2024-01-15 09:47:28,156 ERROR [http-nio-8090-exec-22] [com.atlassian.plugin.manager.DefaultPluginManager] PluginException: Incompatible plugin version detected: com.atlassian.confluence.extra.officeconnector requires Confluence 7.19+ but running 7.18.5
```

!!! warning "Common errors"
    **`grep: /var/atlassian/application-data/confluence/logs/atlassian-confluence.log: No such file or directory`** — Verify the Confluence installation path and log directory location with `find / -name atlassian-confluence.log 2>/dev/null`.
    **`No matches found`** — This indicates no plugin failures were detected in the logs; if plugins appear broken in the UI, check the full log with `tail -100 /var/atlassian/application-data/confluence/logs/atlassian-confluence.log` to see startup warnings.
```bash
# Disable a plugin
curl -s -X PUT -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/vnd.atl.plugins+json" \
  "https://confluence.example.com/rest/api/plugins/1.0/plugins/com.example.plugin/enabled" \
  -d '{"enabled": false}'

# Re-enable
curl -s -X PUT -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/vnd.atl.plugins+json" \
  "https://confluence.example.com/rest/api/plugins/1.0/plugins/com.example.plugin/enabled" \
  -d '{"enabled": true}'
```

```text title="Expected output"
{"enabled":false}
{"enabled":true}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify the Confluence server is running and accessible at the correct hostname/port.
    **`{"statusCode":401,"message":"Unauthorized"}`** — Ensure `$CF_TOKEN` is set to a valid API token with plugin administration permissions.
    **`{"statusCode":404,"message":"Plugin not found"}`** — Confirm the plugin key `com.example.plugin` exists and is installed by checking the Plugins menu in Confluence.
```bash
# 1. Stop Confluence on all nodes
/opt/atlassian/confluence/bin/stop-confluence.sh

# 2. Restore the application install directory
rm -rf /opt/atlassian/confluence
cp -rp /opt/atlassian/confluence_backup_${TIMESTAMP} /opt/atlassian/confluence

# 3. Restore the database (if schema was mutated)
psql -U postgres -c "DROP DATABASE confluencedb;"
psql -U postgres -c "CREATE DATABASE confluencedb OWNER confluence ENCODING 'UTF8';"
pg_restore \
  --host=db.internal.example.com \
  --username=postgres \
  --dbname=confluencedb \
  --jobs=4 \
  /backup/confluence/db/confluence_pre_upgrade.dump

# 4. Restore shared home if attachments changed (usually not needed for rollback)
# rsync /backup/confluence/shared-home/pre_upgrade/ /mnt/confluence-shared/

# 5. Start Confluence on the primary node
/opt/atlassian/confluence/bin/start-confluence.sh

# 6. Verify service returns to RUNNING state
curl -s "https://confluence.example.com/status" | jq '.state'
```

```d2
direction: right

plan: "Plan" {shape: oval}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> verify
verify -> validate
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

- [Confluence — Deploy](../../deploy/)
