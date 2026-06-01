# Jira — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering Backup Strategy Overview, XML Backup / Restore (Admin UI), File Storage Backup, Data Center Backup Best Practices, Restore Procedure and 1 more sections.
</div>

## Backup Strategy Overview

Jira requires three independent backup components for a complete recovery:

| Component | What it covers | Recommended method |
|---|---|---|
| **Database** | All issue data, users, configurations, workflows | PostgreSQL `pg_dump` |
| **Shared Home** | Attachments, avatars, logos, plugin data | Filesystem snapshot / rsync |
| **Local Home** | Per-node config (`dbconfig.xml`, `cluster.properties`) | Filesystem copy |
| **XML Export** | Lightweight instance backup (not for large instances) | Jira Admin UI / REST API |

!!! warning "XML Backup Limitations"
    The built-in XML backup is unsuitable for instances with >10 GB of data or >1 million issues. It does not include attachments. Use database-level backups for production.

---

## XML Backup / Restore (Admin UI)

### Create XML Backup

`Admin → System → Backup System`

Options:

| Option | Default | Notes |
|---|---|---|
| Include attachments | Off | Significantly increases backup size |
| Backup path | `<jira-home>/export/` | Must be writable by the Jira process user |

The output is a `.zip` file containing `entities.xml` and optionally an `attachments/` directory.

### Automate XML Backup via REST

```bash
#!/bin/bash
# xml-backup.sh — Trigger Jira XML backup via REST API
JIRA_URL="https://jira.example.com"
USER="admin"
TOKEN="your-api-token"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

curl -s -u "${USER}:${TOKEN}" \
  -X POST \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/plugins/1.0/resource/com.atlassian.jira.ext.backup%3AbackupService/data" \
  --data '{"cbAttachments": "false", "exportToCloud": "false"}' \
  -o /dev/null -w "%{http_code}\n"

echo "XML backup triggered at ${TIMESTAMP}"
```
```
┌────────────────────────────────────── Jira — Backup and Restore ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Jira Backup and Restore Strategy                               │   │
│   │            Backup: pg_dump nightly + tar JIRA_HOME/data/attachments + push off-site           │   │
│   │             Restore: stop Jira → restore DB → restore home → start Jira → reindex             │   │
│   │          XML backup: Admin > Backup System; not for production restores; content only         │   │
│   │              RTO target: 4 hours; RPO target: 24 hours (nightly backup interval)              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Always restore DB before home directory; reindex after any restore                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Backup Strategy                │  │              Restore Procedure              │   │
│   │             DB: pg_dump nightly              │  │              Stop Jira service              │   │
│   │              Home: tar nightly               │  │              Drop + recreate DB             │   │
│   │              Off-site: S3 copy               │  │               pg_restore dump               │   │
│   │             Verify backup daily              │  │               Restore home dir              │   │
│   │             XML: weekly (small)              │  │                  Start Jira                 │   │
│   │           Test restore: quarterly            │  │             Trigger full reindex            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Jira app VMs · PostgreSQL DB with SSD · NFS/SAN for JIRA_HOME · S3 off-site storage                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  pg_dump      = PostgreSQL backup; use --format=custom for parallel pg_restore                        │
│  pg_restore   = restore custom-format pg_dump; use -j for parallel job count                          │
│  JIRA_HOME    = Jira data directory; contains attachments, indexes, plugins, and config               │
│  XML backup   = Jira built-in export; useful for small instances or content migration only            │
│  Off-site     = backup copy to secondary site or S3; required for DR compliance                       │
│  Reindex      = always reindex after restore; DB and index must be in sync                            │
│  RTO          = Recovery Time Objective; target restore completion time                               │
│  RPO          = Recovery Point Objective; maximum acceptable data loss                                │
│  Quarterly test = restore to isolated test environment; verify data integrity                         │
│  Tar archive  = tar -czf jira_home_$(date +%Y%m%d).tar.gz JIRA_HOME/                                  │
│  Drop+recreate = DROP DATABASE jira; CREATE DATABASE jira; before pg_restore                          │
│  Verify       = compare row counts: SELECT count(*) FROM jiraissue;                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

Run this as a cron job:

```cron
# /etc/cron.d/jira-backup
0 1 * * * jira /opt/scripts/pg-backup-jira.sh >> /var/log/jira-backup.log 2>&1
```

### Backup Retention Policy

| Retention | Policy |
|---|---|
| Daily backups | Keep 7 days |
| Weekly backups (Sunday) | Keep 4 weeks |
| Monthly backups (1st of month) | Keep 12 months |
| Off-site / object storage copy | Keep 90 days |

---

## File Storage Backup

### Shared Home Backup

```bash
#!/bin/bash
# filesystem-backup.sh
SHARED_HOME="/var/atlassian/application-data/jira/shared"
BACKUP_DIR="/backup/jira/filesystem"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "${BACKUP_DIR}"

# Incremental rsync to staging area
rsync -av --delete \
  --link-dest="${BACKUP_DIR}/latest" \
  "${SHARED_HOME}/" \
  "${BACKUP_DIR}/${TIMESTAMP}/"

# Update "latest" symlink
ln -snf "${BACKUP_DIR}/${TIMESTAMP}" "${BACKUP_DIR}/latest"

# Create a compressed archive for off-site transfer
tar -czf "${BACKUP_DIR}/jira_fs_${TIMESTAMP}.tar.gz" \
  -C "${BACKUP_DIR}" "${TIMESTAMP}"

echo "Filesystem backup complete: ${BACKUP_DIR}/${TIMESTAMP}"
```

### What to Include

```text
/var/atlassian/application-data/jira/shared/
├── attachments/          ← INCLUDE (primary data)
├── avatars/              ← INCLUDE
├── logos/                ← INCLUDE
├── export/               ← OPTIONAL (regeneratable)
├── plugins/              ← INCLUDE
└── data/                 ← INCLUDE

# Per-node (back up once — same on all nodes):
/var/atlassian/application-data/jira/
├── dbconfig.xml          ← INCLUDE
├── cluster.properties    ← INCLUDE
└── jira-config.properties ← INCLUDE
```

---

## Data Center Backup Best Practices

### Backup Window

For Data Center with rolling upgrades, a backup of a running instance is possible but requires care:

1. **Database**: Use `pg_dump` — PostgreSQL MVCC ensures a consistent snapshot without locking
2. **Filesystem**: Use LVM snapshot or storage array snapshot for consistency with the DB point-in-time
3. **Coordination**: Snapshot the filesystem and database at the same point in time to avoid referential inconsistency

### Snapshot-Based Backup (Recommended for DC)

```bash
#!/bin/bash
# snapshot-backup.sh — Coordinated LVM snapshot backup

DB_HOST="db.example.com"
LV_PATH="/dev/vg_jira/lv_shared"
SNAP_NAME="lv_shared_snap"
SNAP_SIZE="50G"
MOUNT_POINT="/mnt/jira-snap"

# 1. Create DB backup (consistent point-in-time)
PGPASSWORD="${JIRA_DB_PASSWORD}" pg_dump \
  -h "${DB_HOST}" -U jira -Fc jiradb \
  -f /backup/jira/db/jira_$(date +%Y%m%d).pgdump &
DB_PID=$!

# 2. Create LVM snapshot (near-instant)
lvcreate -L "${SNAP_SIZE}" -s -n "${SNAP_NAME}" "${LV_PATH}"

# 3. Wait for DB dump to complete
wait "${DB_PID}"

# 4. Mount snapshot and archive
mkdir -p "${MOUNT_POINT}"
mount "/dev/${VG}/${SNAP_NAME}" "${MOUNT_POINT}"
tar -czf "/backup/jira/fs/jira_fs_$(date +%Y%m%d).tar.gz" \
  -C "${MOUNT_POINT}" .

# 5. Clean up snapshot
umount "${MOUNT_POINT}"
lvremove -f "/dev/${VG}/${SNAP_NAME}"
```

---

## Restore Procedure

### Full Restore (Database + Filesystem)

!!! danger "Production Restore Checklist"
    Before restoring, confirm: backup file integrity, target environment specs, DNS/load balancer is pointing away from the target instance, all cluster nodes are stopped.

#### Step 1 — Stop Jira

```bash
# All nodes
systemctl stop jira

# Verify no Jira processes remain
ps aux | grep -i jira | grep -v grep
```

#### Step 2 — Restore Database

```bash
# Drop and recreate the database
psql -h db.example.com -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'jiradb';"
psql -h db.example.com -U postgres -c "DROP DATABASE jiradb;"
psql -h db.example.com -U postgres -c "CREATE DATABASE jiradb OWNER jira ENCODING 'UTF8';"

# Restore from custom-format dump
PGPASSWORD="${JIRA_DB_PASSWORD}" pg_restore \
  -h db.example.com \
  -U jira \
  -d jiradb \
  --jobs 4 \
  --no-acl \
  --no-owner \
  /backup/jira/db/jira_db_20260101-010000.pgdump
```

#### Step 3 — Restore Filesystem

```bash
# Clear existing shared home
rm -rf /var/atlassian/application-data/jira/shared/*

# Restore from archive
tar -xzf /backup/jira/fs/jira_fs_20260101.tar.gz \
  -C /var/atlassian/application-data/jira/shared/

# Fix ownership
chown -R jira:jira /var/atlassian/application-data/jira/shared/
```

#### Step 4 — Start and Validate

```bash
# Start first node only
systemctl start jira

# Monitor startup logs
tail -f /opt/atlassian/jira/logs/catalina.out
```

Expected startup log entries:

```text
INFO  [main] Jira starting up...
INFO  [main] Jira has been successfully started
```

#### Step 5 — Rebuild Search Index

```bash
curl -u admin:token -X POST \
  "https://jira.example.com/rest/api/2/reindex" \
  -H "Content-Type: application/json" \
  -d '{"type": "FOREGROUND"}'
```

Or via UI: `Admin → System → Indexing → Full Re-index`

#### Step 6 — Validate

```bash
# Check cluster node registration
psql -h db.example.com -U jira -d jiradb \
  -c "SELECT node_id, node_name, status, last_heartbeat FROM clusternodeinfo;"

# Verify issue count matches backup
psql -h db.example.com -U jira -d jiradb \
  -c "SELECT COUNT(*) FROM jiraissue;"

# Health endpoint
curl -s https://jira.example.com/status | python3 -m json.tool
```

#### Step 7 — Bring Up Remaining Nodes

```bash
# Start additional nodes after primary is healthy
systemctl start jira   # on jira-app-02, jira-app-03
```

---

## Restore Validation Checklist

| Check | Command / Method | Expected |
|---|---|---|
| Jira starts | `systemctl status jira` | Active (running) |
| Health endpoint | `GET /status` | `{"state":"RUNNING"}` |
| Issue browse | Open any known issue in browser | Issue loads correctly |
| Attachments | Open issue with known attachment | File downloads |
| User login | Log in as test user | Successful |
| Workflow | Transition a test issue | Transition succeeds |
| Email | Trigger notification | Email received |
| Reindex complete | `Admin → Indexing` | No pending reindex |
| Cluster nodes | Admin → Clustering | All expected nodes shown |
