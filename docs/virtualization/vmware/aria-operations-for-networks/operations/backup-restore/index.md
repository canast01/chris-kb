---
tags:
  - aria-networks
  - operations
  - vmware
---
# vRNI Backup & Restore

```bash
PLATFORM="https://aon.example.local"
TOKEN=$(curl -sk -X POST "${PLATFORM}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
echo "Token: $TOKEN"
```
```text
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
```
```bash
# crontab entry — runs daily at 02:00
0 2 * * * /usr/local/bin/aon-backup.sh >> /var/log/aon-backup.log 2>&1
```
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
```bash
ssh ubuntu@10.10.10.51    # Collector VM

# On Collector VM:
sudo /home/ubuntu/support/pairing.sh
# Enter Platform VM FQDN when prompted
# Enter new pairing key when prompted
```
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

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

