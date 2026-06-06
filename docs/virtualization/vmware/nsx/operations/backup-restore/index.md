# NSX — Backup and Restore

```bash
# Configure backup via API
curl -sk -u 'admin:password' \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "backup_config": {
      "backup_enabled": true,
      "remote_file_server": {
        "server": "backup.example.local",
        "port": 22,
        "protocol": {
          "protocol_name": "SFTP",
          "authentication": {
            "authentication_mode": "PASSWORD",
            "username": "nsx-backup",
            "password": "s3cur3P@ss"
          }
        },
        "dir_path": "/backups/nsx/"
      },
      "pass_phrase": "MyVaultStoredPassphrase",
      "backup_schedule": {
        "resource_type": "IntervalBackupSchedule",
        "seconds_between_backups": 86400
      },
      "backup_to_retain": 14
    }
  }' \
  "https://<nsx-manager>/api/v1/cluster/backups/config"
```
```text
┌────────────────────────────────────── NSX — Backup and Restore ───────────────────────────────────────┐
│                                                                                                       │
│  NSX Manager cluster backup via SFTP, scheduling, and full restore procedure.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              NSX Manager Backup              │  │             Backup Configuration            │   │
│   │          Full cluster state backup           │  │             SFTP server required            │   │
│   │          API: POST /api/v1/cluster/          │  │          Passphrase for encryption          │   │
│   │             UI: System > Backup              │  │           Schedule: daily minimum           │   │
│   │         Includes all config + certs          │  │            Retention: 30+ backups           │   │
│   │          Inventory + policy backup           │  │            Test restore quarterly           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Schedule backup → verify SFTP receipt → test restore in non-prod quarterly.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Restore Procedure               │  │              Verification Steps             │   │
│   │           Deploy fresh NSX Manager           │  │             All nodes show green            │   │
│   │             Point to SFTP backup             │  │            Segments/T0/T1 intact            │   │
│   │              Provide passphrase              │  │              DFW rules restored             │   │
│   │          Restore initiates cluster           │  │            Transport nodes synced           │   │
│   │          Reconnect compute manager           │  │            vCenter integration OK           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs on ESXi, vCenter, SFTP backup server, management network                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NSX Manager = 3-node cluster VM; central control/mgmt plane for NSX                                  │
│  SFTP        = SSH File Transfer Protocol; NSX backup destination                                     │
│  Passphrase  = encryption key for NSX backup file; store securely                                     │
│  Compute Mgr = vCenter registered in NSX; must reconnect after restore                                │
│  Transport node = ESXi/Edge with NSX dataplane (N-VDS) installed                                      │
│  DFW         = Distributed Firewall; policy object restored from backup                               │
│  T0 gateway  = Tier-0; north-south routing; restored from backup state                                │
│  T1 gateway  = Tier-1; service gateway; connected to T0 and segments                                  │
│  Cluster restore = NSX API call re-deploying config from SFTP backup                                  │
│  N-VDS       = NSX virtual distributed switch on transport nodes                                      │
│  Inventory   = groups, tags, VMs known to NSX; backed up with config                                  │
│  Policy API  = NSX policy REST API; primary management interface                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
nsxcli
get cluster status
get managers
get services
```
```bash
# Cluster health
get cluster status

# Transport node connectivity (may take 5–10 min to reconnect)
get transport-node-status

# Verify segments are present
nsxcli
get logical-switches

# Verify gateways
get logical-routers

# Check DFW policies restored
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/domains/default/security-policies" | python3 -m json.tool

# Check Edge nodes reconnected
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/edge-clusters"
```
```bash
# Export full policy config as JSON (use before changes for comparison)
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra?filter=Type-SecurityPolicy" \
  > nsx-dfw-export-$(date +%Y%m%d).json

# Export all infra objects
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra" \
  > nsx-full-infra-$(date +%Y%m%d).json
```
```bash
# Query the last successful backup timestamp
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/cluster/backups/history" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
backups = data.get('results', [])
if backups:
    latest = sorted(backups, key=lambda x: x.get('end_time', 0), reverse=True)[0]
    import datetime
    ts = datetime.datetime.fromtimestamp(latest['end_time']/1000)
    print(f'Last backup: {ts}  Status: {latest.get(\"status\",\"?\")}'  )
else:
    print('No backups found')
"
```
