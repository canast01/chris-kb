# Aria Ops for Logs — Backup & Restore


<div class="kb-summary">
Aria Operations for Logs does not include a native configuration backup utility. Recovery relies on: 1. **VM-level backup** of all cluster nodes (primary method for full restoration) 2. **NFS archive** of log data (for long-term log retention, not configuration recovery) 3.
</div>

Aria Operations for Logs does not include a native configuration backup utility. Recovery relies on:
1. **VM-level backup** of all cluster nodes (primary method for full restoration)
2. **NFS archive** of log data (for long-term log retention, not configuration recovery)
3. **Documented configuration** (content packs, alert definitions, user accounts) as a rebuild reference

---

## VM-Level Backup (Primary Method)

Use VADP-compatible backup (Veeam, Commvault, Veritas) for all Aria Ops for Logs nodes.

**Requirements:**
- VMware Tools must be running on all nodes: `vmware-toolsd --version` (from SSH)
- Back up all nodes in the cluster — master and all workers
- Use application-consistent quiesce
- Schedule: nightly full or incremental backups; retain 14 daily restore points minimum

**Pre-backup check:**

```bash
ssh admin@vrli-prod-01.example.local

# Confirm cluster health before backup window
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state}'
# All nodes should show state: "ACTIVE"

# Check disk usage — do not back up a node with >90% disk (indicates ingestion pressure)
df -h /var/log/loginsight
```
```text
┌──────────────────────────── Aria Operations for Logs — Backup and Restore ────────────────────────────┐
│                                                                                                       │
│  Backup vRLI config, dashboards, and alerts; log data is archived separately to NFS/S3.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               What to Back Up                │  │                Backup Methods               │   │
│   │      Config: alerts, dashboards, packs       │  │         vRLI UI: export config JSON         │   │
│   │     Field extractions and custom queries     │  │     REST API: GET /api/v1/config/export     │   │
│   │       Log archive: NFS/S3 (long-term)        │  │         VM snapshot before upgrades         │   │
│   │          TLS certs and LDAP config           │  │      LCM: logscraper for support bundle     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Restore imports config JSON then repoints sources; log data is not restorable from config.           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Restore Sequence               │  │              Restore Validation             │   │
│   │           1. Deploy fresh vRLI OVA           │  │        Import: all dashboards visible       │   │
│   │         2. Import config JSON backup         │  │        Alerts: re-enabled and firing        │   │
│   │         3. Restore LDAP/cert config          │  │          Sources: syslog flowing in         │   │
│   │       4. Repoint ESXi/vCenter sources        │  │            SSO: AD login working            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI Linux VM · NFS/S3 archive storage · vCenter · ESXi syslog config · LCM                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Config export     = vRLI JSON export containing all settings (alerts/dashboards/sources/packs)       │
│  Config import     = vRLI UI or API import of JSON; overwrites current configuration                  │
│  Log archive       = Compressed export of log data to NFS/S3; not part of config backup               │
│  VM snapshot       = vCenter snapshot before vRLI upgrade; fast rollback if upgrade fails             │
│  syslog.global.logHost= Must be re-set on ESXi hosts after vRLI IP changes on restore                 │
│  LDAP restore      = AD directory integration must be reconfigured manually after fresh deploy        │
│  Content pack      = Must be reinstalled from marketplace if not in config export                     │
│  RPO               = Config RPO: ≤24h (daily export); log RPO: archive job interval                   │
│  RTO               = Target: fresh vRLI operational in <2h using config import                        │
│  Alert re-enable   = Imported alerts may be disabled; manually enable after import                    │
│  Source repoint    = Update syslog destination on devices after vRLI IP/FQDN changes                  │
│  LCM logscraper    = Diagnostic tool; not a backup tool; used for support bundles only                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Exporting Configuration Reference (Manual)

Export key configuration elements to documentation files for rebuild reference. This does not replace a full backup but enables faster manual reconstruction if needed.

```bash
BASE="https://vrli-prod-01.example.local"
AUTH="admin:<password>"

# Export alert definitions
curl -sk -u "$AUTH" "$BASE/api/v2/alerts" | jq '.' > vrli-alerts-$(date +%Y%m%d).json

# Export notification channels
curl -sk -u "$AUTH" "$BASE/api/v2/notification" | jq '.' > vrli-notifications-$(date +%Y%m%d).json

# Export agents and agent groups
curl -sk -u "$AUTH" "$BASE/api/v2/agents/groups" | jq '.' > vrli-agent-groups-$(date +%Y%m%d).json

# Export archive configuration
curl -sk -u "$AUTH" "$BASE/api/v2/archiver" | jq '.' > vrli-archiver-$(date +%Y%m%d).json
```

Store these JSON files in version control alongside other infrastructure configuration documentation.

---

## NFS Log Archiving

Long-term log retention beyond the default hot tier is configured via the archive feature. This is not a backup — it archives indexed logs to an NFS share for extended retention and compliance.

```text
Administration → Archiving → Configure → enable NFS archive
```

Provide:
- NFS server: `nas-01.example.local`
- NFS export path: `/exports/vrli-archive`
- Mount options: `nfsvers=3,rw`

Verify archive connectivity:

```bash
# From master node SSH
showmount -e nas-01.example.local
mount -t nfs nas-01.example.local:/exports/vrli-archive /mnt/test-archive
touch /mnt/test-archive/.write-test && echo "OK" && rm /mnt/test-archive/.write-test
umount /mnt/test-archive
```

---

## Restore Procedure

### From VM Backup

1. Power off all Aria Ops for Logs VMs (coordinate — log ingestion will stop during restore)
2. Restore all nodes from backup to the same restore point — restoring nodes from different points causes cluster split-brain
3. Power on the master node first, then workers
4. Verify cluster health:

```bash
ssh admin@vrli-prod-01.example.local
curl -sk -u 'admin:<password>' \
  "https://localhost/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state}'
```

5. Verify log ingestion is active:

```text
Administration → Cluster → each node should show state Active and ingestion rate > 0 events/sec
```

6. Confirm alert definitions and content packs are intact:

```bash
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/alerts" | jq '. | length'
```

7. Re-validate syslog sources are forwarding (check from ESXi hosts, vCenter, and agents)

### Post-Restore Validation Checklist

- [ ] All cluster nodes show ACTIVE state
- [ ] Log ingestion rate is non-zero (visible in Administration → Cluster)
- [ ] Alert definitions present and enabled
- [ ] Content packs installed (vSphere, NSX-T)
- [ ] Notification channels (email, webhook) configured and tested
- [ ] Agent group configurations intact
- [ ] Archive target accessible and writing
