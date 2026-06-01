# Confluence — Install & Upgrade


<div class="kb-summary">
This page covers the end-to-end upgrade procedure for Confluence Data Center, including pre-upgrade preparation, execution, validation, and rollback. Treat every upgrade as a change-controlled activity with a tested rollback path.
</div>

---

## Version Matrix

| Confluence Version | Java Required | PostgreSQL Min | EoL / EoS |
|---|---|---|---|
| 7.x | Java 8 or 11 | 10 | End of Support |
| 8.0–8.4 | Java 11 | 13 | End of Support |
| 8.5 LTS | Java 11 or 17 | 14 | Oct 2026 |
| 8.9 | Java 11 or 17 | 14 | Active |
| 9.0 | Java 17 | 15 | Active |
| 9.x (latest) | Java 17 or 21 | 16 | Active |

> Always upgrade to an **LTS release** for production. Skip LTS-to-LTS where the release notes confirm this is supported.

---

## Pre-Upgrade Checklist

### 14 Days Before Upgrade

- [ ] Review the [Confluence upgrade matrix](https://confluence.atlassian.com/doc/confluence-upgrade-matrix-960695895.html) for your current → target version
- [ ] Check **Marketplace App Compatibility**: Admin > Manage Apps > set "Filter by version" to the target version
- [ ] Review **Known Issues** in the Confluence release notes for the target version
- [ ] Confirm Java version compatibility — upgrade Java separately if needed
- [ ] Confirm PostgreSQL version compatibility
- [ ] Test the upgrade in a **staging environment** that mirrors production

### 48 Hours Before Upgrade

- [ ] Announce maintenance window to users
- [ ] Freeze content changes (optional but recommended for large upgrades)
- [ ] Verify backup is current and has been tested (see [Backup & Restore](../backup-restore/index.md))
- [ ] Document current version: Admin > General Configuration > System Information
- [ ] Export list of installed plugins and their versions
- [ ] Record current heap settings (`setenv.sh`), Tomcat port config (`server.xml`)

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
```
┌────────────────────────────────── Confluence — Install and Upgrade ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Confluence Installation and Upgrade Procedure                         │   │
│   │        Install: JDK 11/17 → download installer → set CONFLUENCE_HOME → run setup wizard       │   │
│   │          DB: create PostgreSQL DB and role → set in setup wizard → apply license key          │   │
│   │          Upgrade: backup DB + home → stop → run new installer → start → verify → test         │   │
│   │          DC node add: install on new VM → point to same DB + NFS → join cluster auto          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Always test upgrade in staging environment before production; keep snapshot for rollback           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Fresh Install Steps              │  │                Upgrade Steps                │   │
│   │              Install JDK 11/17               │  │               Snapshot VM + DB              │   │
│   │              Download installer              │  │                pg_dump backup               │   │
│   │             Set CONFLUENCE_HOME              │  │                Stop all nodes               │   │
│   │             Create PostgreSQL DB             │  │              Run new installer              │   │
│   │               Run setup wizard               │  │               Start and verify              │   │
│   │              Apply license key               │  │              Test key functions             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Fresh VM (RHEL/CentOS) · PostgreSQL VM · NFS datastore · load balancer for DC                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CONFLUENCE_HOME = data directory; set as env var or in confluence-init.properties                    │
│  JDK 11/17    = Confluence 8.x supports JDK 11 and 17; JDK 21 for Confluence 9.x                      │
│  Setup wizard = browser-based initial config: DB, license, admin account, space                       │
│  License key  = Atlassian data center or server license; apply in setup or Admin panel                │
│  pg_dump      = PostgreSQL backup utility; always backup before any upgrade                           │
│  Installer    = Atlassian-provided .bin file for Linux; chmod +x and run as root                      │
│  DC cluster   = second node auto-joins when pointed at same DB and NFS home                           │
│  Snapshot     = VM snapshot before upgrade; revert if upgrade fails                                   │
│  Version check = Confluence upgrade path; some versions require intermediate upgrade steps            │
│  setenv.sh    = JVM argument config; in CONFLUENCE_INSTALL/bin/; set -Xmx here                        │
│  Plugin compat = check app compatibility on upgrade; UPM shows incompatible plugins                   │
│  Rollback     = revert VM snapshot or restore DB dump; re-run previous installer                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

### Step 2 — Back Up Current Installation

```bash
# Back up the install directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp -rp /opt/atlassian/confluence /opt/atlassian/confluence_backup_${TIMESTAMP}

# Back up the local home
cp -rp /var/atlassian/application-data/confluence \
  /var/atlassian/application-data/confluence_backup_${TIMESTAMP}

echo "Backup created: confluence_backup_${TIMESTAMP}"
```

### Step 3 — Run the Installer (Linux)

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

Example `response.varfile` for unattended upgrade:

```properties
app.install.service$Boolean=true
existingInstallationDir=/opt/atlassian/confluence
sys.confirmedUpdateInstallationString=true
launch.application$Boolean=false
```

### Step 4 — Restore Custom Configuration Files

The installer may overwrite `setenv.sh` and `server.xml`. Restore your customizations:

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

### Step 5 — Start Confluence and Monitor

```bash
# Start the application
/opt/atlassian/confluence/bin/start-confluence.sh

# Tail the startup log
tail -f /var/atlassian/application-data/confluence/logs/atlassian-confluence.log

# For Data Center: Confluence will run database schema migrations on first start
# This can take 10–60 minutes for large databases — do NOT interrupt
```

Expected log output during upgrade:

```text
INFO  [main] [DatabaseUpgradeTask] Running upgrade task: UpgradeTask_Build_XXXXX
INFO  [main] [DatabaseUpgradeTask] Upgrade task completed in 12345ms
INFO  [main] [ConfluenceBootstrapManager] Bootstrap complete
```

### Step 6 — Data Center — Rolling Upgrade (remaining nodes)

After the primary node is fully started and the UI is accessible:

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

---

## Database Schema Changes

During major upgrades, Confluence runs **upgrade tasks** that modify the database schema. These are tracked in the `JIRAACTION` / `AO_*` tables and the upgrade log.

```bash
# View upgrade task history in the database
psql -h db.internal.example.com -U confluence -d confluencedb \
  -c "SELECT classname, ranon FROM JIRAACTION ORDER BY ranon DESC LIMIT 20;"

# Check for failed upgrade tasks
grep -E "(UpgradeTask.*FAILED|upgrade.*failed)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log
```

Key schema change points for recent major versions:

| Version Range | Notable Schema Change |
|---|---|
| 7.x → 8.0 | Page storage format migration (XHTML → Fabric) |
| 8.4 → 8.5 | Collaborative editing infrastructure update |
| 8.x → 9.0 | Content model changes; allowlisted macro framework |

---

## Plugin Compatibility Check

### Before Upgrade

```bash
# Export current plugin list with versions
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://confluence.example.com/rest/api/plugins/1.0/" \
  | jq -r '.plugins[] | select(.userInstalled == true) | "\(.key)\t\(.version)\t\(.enabled)"' \
  > plugins_before_upgrade.tsv

cat plugins_before_upgrade.tsv
```

### After Upgrade — Identify Incompatible Plugins

```bash
# Check for plugins that failed to start post-upgrade
grep -E "(Plugin.*FAILED|PluginException|osgi.*error)" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log \
  | grep -i plugin | tail -30

# Admin UI: Admin > Manage Apps — filter by "Needs update" or "Incompatible"
```

### Disable/Re-enable a Plugin via REST

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

---

## Rollback Procedure

If the upgrade fails and the database schema has not been migrated past the point of no return:

### Rollback Steps

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

> If the database migration ran more than ~10 upgrade tasks, a database restore is mandatory. Running the old version against a partially-migrated schema will produce data corruption.

---

## Post-Upgrade Validation Checklist

- [ ] Confluence status endpoint returns `RUNNING`
- [ ] Admin > General Configuration shows the new version number
- [ ] All cluster nodes active (Data Center)
- [ ] Marketplace apps status reviewed — no unexpected failures
- [ ] Search index verified: run a test search for known content
- [ ] User login tested (LDAP/AD sync if applicable)
- [ ] Attachment upload and download tested
- [ ] Email notification tested (Admin > Mail > Send Test Email)
- [ ] Jira application link still active (Admin > Application Links)
- [ ] Run scheduled jobs manually and confirm no failures
- [ ] Performance: compare page load times to pre-upgrade baseline
- [ ] Clear browser caches and communicate maintenance end to users
