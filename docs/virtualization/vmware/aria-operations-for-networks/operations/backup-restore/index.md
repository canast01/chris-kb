# Aria Operations for Networks — Backup and Restore

## What Is Backed Up

AON does not provide a single-command full backup. Understanding what is and is not included in each backup method is critical.

| Data Type | Config Export (UI) | REST API Export | vSphere Snapshot |
|---|---|---|---|
| Data sources (vCenter, NSX-T, switches) | Yes | Yes | Yes |
| Collector pairings | Yes | Yes | Yes |
| Application definitions | Yes | Yes | Yes |
| Saved searches and pinned alerts | Yes | Yes | Yes |
| User accounts and roles | Yes | Yes | Yes |
| LDAP/AD configuration | Yes | Yes | Yes |
| Notification rules (email, webhook, syslog) | Yes | Yes | Yes |
| SSL certificate (custom) | No — re-import separately | No | Yes |
| Flow data (historical traffic) | **No** | **No** | Yes (if snapshot is consistent) |
| Security recommendations (saved) | Yes | Yes | Yes |
| vSphere snapshot of Platform disk | N/A | N/A | Yes |

**The configuration export is the primary backup artifact** — it is small (typically <10 MB), portable, and captures all operational settings. Flow data is sacrificial: it will be rebuilt over time as new flow data is ingested after a restore.

## Config Export via UI

Settings → Infrastructure → Backup → Download Backup

The download is a `.tar.gz` archive. Store this off the Platform VM immediately after download.

Backup frequency recommendation:
- After any configuration change (data source add/remove, user changes, application definition changes)
- At minimum weekly on a scheduled basis

## Config Export via REST API

Obtain an authentication token first:

```bash
PLATFORM="https://aon.example.local"
TOKEN=$(curl -sk -X POST "${PLATFORM}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
echo "Token: $TOKEN"
```
┌──────────────────────────────────────── vRNI Backup & Restore ────────────────────────────────────────┐
│                                                                                                       │
│  Configuration export via REST API and full restore steps for Aria Operations for Networks.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               What to Back Up                │  │                Backup Method                │   │
│   │         Data source configs (creds)          │  │         REST API: GET /data-sources         │   │
│   │            Alert rule definitions            │  │          REST API: GET /alert-rules         │   │
│   │        Custom dashboards / pinboards         │  │           REST API: GET /pinboards          │   │
│   │       Application definitions (groups)       │  │         REST API: GET /applications         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Export config JSON via REST; snapshot VM for full appliance backup before upgrades.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Restore Procedure               │  │              Appliance Snapshot             │   │
│   │             1. Deploy fresh OVA              │  │          Snapshot VM before upgrade         │   │
│   │          2. POST /data-sources JSON          │  │          Revert snapshot on failure         │   │
│   │          3. POST /alert-rules JSON           │  │         Snapshot: quiesced preferred        │   │
│   │          4. POST /applications JSON          │  │          Flow data: not restorable          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM on vSphere; vSphere snapshots for appliance; S3/NFS for JSON exports                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  REST API            = vRNI northbound API; used for config export and import                         │
│  Data Source         = vRNI connection object (vCenter, NSX, switch) with credentials                 │
│  Alert Rule          = Threshold-based rule triggering notifications on flow anomalies                │
│  Pinboard            = vRNI custom dashboard saved by user; exportable as JSON                        │
│  Application         = Named group of VMs/IPs in vRNI for flow filtering and mapping                  │
│  OVA                 = Open Virtualization Appliance; vRNI deployment package                         │
│  Quiesced Snapshot   = VM snapshot with guest OS file system flushed; preferred for DBs               │
│  Flow Data           = Historical flow records; not included in config backup/restore                 │
│  API Token           = Bearer token used to authenticate REST API backup calls                        │
│  JSON Export         = Machine-readable config dump for data sources, rules, dashboards               │
│  PAK File            = vRNI upgrade bundle; snapshot before applying                                  │
│  Restore Validation  = Post-restore check: data sources green, flows appearing, alerts OK             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Automate with a cron job on a management host:

```bash
#!/bin/bash
# /usr/local/bin/aon-backup.sh
set -euo pipefail

PLATFORM="https://aon.example.local"
USERNAME="svc-aon-backup@local"
PASSWORD="PASSWORD"
BACKUP_DIR="/opt/backups/aon"
RETAIN_DAYS=30

mkdir -p "$BACKUP_DIR"

TOKEN=$(curl -sk -X POST "${PLATFORM}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

OUTFILE="${BACKUP_DIR}/aon-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

curl -sk -X GET "${PLATFORM}/api/ni/settings/backup" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  --output "$OUTFILE"

if [[ -f "$OUTFILE" && $(stat -c%s "$OUTFILE") -gt 10000 ]]; then
  echo "Backup successful: $OUTFILE"
  find "$BACKUP_DIR" -name "aon-backup-*.tar.gz" -mtime "+${RETAIN_DAYS}" -delete
else
  echo "ERROR: Backup file is missing or too small." >&2
  exit 1
fi
```

```bash
# crontab entry — runs daily at 02:00
0 2 * * * /usr/local/bin/aon-backup.sh >> /var/log/aon-backup.log 2>&1
```

## Restore Procedure

### Step 1: Deploy Fresh Platform VM OVA

Deploy the same version of AON Platform OVA as the backup was taken from. Version mismatch during restore is not supported.

Complete the initial setup wizard:
- Configure hostname, IP, gateway, DNS, NTP
- Set admin password
- Do not add any data sources yet

### Step 2: Import Configuration Backup

**UI path:** Settings → Infrastructure → Backup → Restore → Upload Backup File

Select the `.tar.gz` file and click Restore. The platform will:
1. Parse and validate the backup archive
2. Restore data sources, applications, user accounts, notifications
3. Re-generate collector pairing keys (Collectors must re-pair)

Restore via REST API:

```bash
PLATFORM="https://aon-new.example.local"
TOKEN=$(curl -sk -X POST "${PLATFORM}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"NEWPASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -X POST "${PLATFORM}/api/ni/settings/restore" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  -F "file=@/path/to/aon-backup-20260101-020001.tar.gz" \
  -o /tmp/restore-response.json

cat /tmp/restore-response.json
```

### Step 3: Re-Pair Collectors

After a restore to a new Platform VM, all Collectors must re-pair:

1. In the AON UI: Settings → Accounts and Data Sources → Collectors → Select Collector → Get Pairing Key
2. SSH to each Collector VM:

```bash
ssh ubuntu@10.10.10.51    # Collector VM

# On Collector VM:
sudo /home/ubuntu/support/pairing.sh
# Enter Platform VM FQDN when prompted
# Enter new pairing key when prompted
```

3. Verify Collector appears as Connected in the UI within 2–3 minutes.

### Step 4: Verify Data Source Connectivity

After Collectors re-pair, data sources must be verified:

Settings → Accounts and Data Sources → verify each source shows "Connected" and a recent "Last Sync" timestamp.

If a data source shows an error, re-enter credentials (passwords are not stored in the config backup in plaintext and may need to be re-entered depending on the restore path).

## RTO Considerations

| Activity | Estimated Time |
|---|---|
| Deploy Platform OVA | 20–30 minutes |
| Initial setup wizard | 10 minutes |
| Config restore (import) | 5–15 minutes |
| Collector re-pairing (per collector) | 5 minutes |
| First topology sync (per data source) | 10–20 minutes |
| Flow data re-accumulation to baseline | 30 days (for full microsegmentation recommendations) |

**Practical RTO** for configuration and topology: 1–2 hours.
**Flow data RTO**: ongoing — historical flow data is not recoverable without a full disk-level restore.

## vSphere Snapshot Caveats

vSphere snapshots of the Platform VM **can** be used as a recovery point, but with important caveats:

- Snapshots taken while the Platform VM is running are **crash-consistent**, not application-consistent. Cassandra and Elasticsearch may require recovery on first startup after snapshot revert.
- On revert from snapshot, run:

```bash
ssh ubuntu@aon-platform.example.local

# Check Cassandra status
sudo systemctl status cassandra

# If Cassandra failed to start (likely after unclean shutdown):
sudo systemctl stop cassandra
sudo find /var/lib/cassandra -name "*.tmp" -delete
sudo systemctl start cassandra
sudo systemctl status cassandra

# Check all platform services
sudo systemctl status vrni-platform nginx kafka elasticsearch postgres
```

- If services do not recover automatically after snapshot revert, contact VMware Support with the support bundle before attempting further manual recovery.
- Snapshot revert restores flow data as of the snapshot timestamp — data collected between the snapshot and the failure is lost.
- Snapshots should be used as a **short-term safety net before upgrades**, not as the primary backup strategy.

## Backup of Collector VMs

Collector VMs are stateless — **do not back them up**. If a Collector VM is lost, deploy a new OVA and re-pair it. No configuration or flow data is stored on the Collector.
