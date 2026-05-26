# InsightIQ Lifecycle
## Compatibility Validation

Before any InsightIQ upgrade, or before upgrading a monitored OneFS cluster, validate compatibility using the [NetApp Interoperability Matrix Tool (IMT)](https://mysupport.netapp.com/matrix/).

Search for: **InsightIQ** → confirm supported OneFS versions for the target InsightIQ release.

Key compatibility rules:
- InsightIQ 4.x: supports OneFS 7.2, 8.x, and 9.0–9.2
- InsightIQ 4.1+: required for OneFS 9.3+
- Always check IMT before a cluster OS upgrade — a OneFS upgrade may require an InsightIQ upgrade first

## Pre-Upgrade Checklist

```text
1. Check compatibility on NetApp IMT for target InsightIQ and OneFS versions
2. Back up the PostgreSQL database (see Backup section below)
3. Take a VM snapshot of the InsightIQ appliance in vCenter
4. Notify the storage operations team — dashboard access will be unavailable during upgrade
5. Download the InsightIQ upgrade package from the NetApp Support Portal
6. Verify available disk space: InsightIQ requires at least 10 GB free on the OS disk for upgrade staging
```
┌────────────────────────────────── InsightIQ — Lifecycle Management ───────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                    Deploy                    │  │                   Upgrade                   │   │
│   │            Deploy OVA to vCenter             │  │                 Backup first                │   │
│   │              Assign IP and DNS               │  │                 Snapshot VM                 │   │
│   │             Add clusters via UI              │  │              Apply upgrade pkg              │   │
│   │                Configure SMTP                │  │              Verify collection              │   │
│   │             Set retention policy             │  │               Rollback if fail              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  OVA on vSphere management cluster · VM snapshot before upgrade · backup to NFS                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA deployment = Importing InsightIQ as VM; set 4 vCPU, 8 GB RAM, 200+ GB disk                       │
│  Cluster registration = Adding PowerScale cluster in InsightIQ UI with PAPI credentials               │
│  Retention policy = Configured in InsightIQ settings; default 2 years raw data                        │
│  SMTP configuration = InsightIQ settings for email alerts and scheduled reports                       │
│  Upgrade package = Dell-provided upgrade file; applied via iiq_upgrade command                        │
│  Snapshot = VM snapshot taken before upgrade; enables rollback if data is lost                        │
│  Backup = iiq_backup run before upgrade; stored off-VM on NFS                                         │
│  Verify collection = Check InsightIQ is collecting new data after upgrade                             │
│  Rollback = Revert to VM snapshot if upgrade corrupts DB or stops collection                          │
│  Decommission = iiq_backup → save archive → power off VM → remove from vCenter                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Upgrade Procedure (Linux Installer)

```bash
# Stop InsightIQ services
sudo systemctl stop iiq

# Install the upgrade package
sudo rpm -Uvh insightiq-<version>.rpm   # RHEL/CentOS
# or
sudo dpkg -i insightiq-<version>.deb    # Ubuntu

# Start services
sudo systemctl start iiq

# Verify service health
sudo systemctl status iiq
```

## Backup

InsightIQ does not have a native backup tool. Automate database backup with a daily cron job on the appliance.

```bash
# /etc/cron.d/iiq-backup
0 2 * * * root pg_dump -U iiq iiq | gzip > /backup/iiq_$(date +\%Y\%m\%d).sql.gz

# Retain last 14 days of backups
0 3 * * * root find /backup -name 'iiq_*.sql.gz' -mtime +14 -delete
```

Backup files should be replicated to an external backup target (NAS, S3-compatible, or enterprise backup solution).

## Cluster Registration

Adding a new PowerScale cluster to InsightIQ:

```text
1. InsightIQ web UI > Administration > Clusters > Add Cluster
2. Enter:
   - Cluster management IP (SmartConnect zone or management IP)
   - Username: svc-insightiq (read-only OneFS account)
   - Password: from secrets manager
   - Display name: <site>-pscale-<number>
3. Save — InsightIQ will begin collecting within one poll interval (~5 minutes)
4. Verify the cluster appears on the dashboard with throughput data after 15 minutes
```

## Cluster Removal

```text
1. InsightIQ web UI > Administration > Clusters > [Cluster] > Remove
2. Choose whether to retain historical data (recommended: retain for 30 days post-removal for audit)
3. Update any scheduled reports that referenced the removed cluster
```

## EOL Tracking

InsightIQ EOL dates are published on the [NetApp Support Lifecycle page](https://mysupport.netapp.com/site/info/version-support).

- Review EOL status annually
- Plan upgrades to avoid running EOL software in production
- Note: for OneFS 9.5+, evaluate whether native OneFS performance reporting reduces dependency on InsightIQ
