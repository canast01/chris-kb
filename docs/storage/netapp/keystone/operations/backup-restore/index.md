# NetApp Keystone — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering Keystone Architecture Context, Keystone Collector Configuration Backup, SnapMirror Relationship Export, Restore Keystone Collector Configuration, Pre-Upgrade Checklist.
</div>

## Keystone Architecture Context

Keystone is a storage-as-a-service subscription — backup/restore covers:
- Keystone Collector configuration backup
- ONTAP volume snapshot and SnapMirror policies (for underlying arrays)
- Keystone portal subscription configuration export

## Keystone Collector Configuration Backup

The Keystone Collector is a VM deployed on-premises that harvests usage data. Back up its configuration before any upgrade.

```bash
# SSH into Keystone Collector VM
ssh admin@<keystone-collector-ip>

# Export current configuration
keystone-config export --output /tmp/ks-config-$(date +%Y%m%d).tar.gz
scp admin@<keystone-collector-ip>:/tmp/ks-config-$(date +%Y%m%d).tar.gz ./

# Verify configuration is parseable
tar -tzf ks-config-<date>.tar.gz
```
┌─────────────────────────── NetApp Keystone — Operations: Backup & Restore ────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Backup: ONTAP Snapshots, SnapVault disk-to-disk, SnapCenter app-consistent          │   │
│   │           Snapshot: instantaneous, space-efficient; RPO minutes; stored in same SVM           │   │
│   │          SnapVault: replicates snapshots to secondary ONTAP; RPO hours; diff cluster          │   │
│   │          Restore: snap restore (volume), snap restore -item (file), SnapCenter clone          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Schedule snapshots -> SnapVault to secondary -> SnapCenter for DB -> restore on demand             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Snapshot          │  │          SnapVault          │  │          SnapCenter         │   │
│   │       Instant capture       │  │         Vault policy        │  │          App plugin         │   │
│   │       Space-efficient       │  │        Secondary vol        │  │        SQL/Oracle/SAP       │   │
│   │          Per-volume         │  │          RPO hours          │  │        App-consistent       │   │
│   │          RPO <5 min         │  │        Long retention       │  │        Clone workflow       │   │
│   │         Max 255/vol         │  │        Throttle xfer        │  │         Report audit        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Test restores quarterly; document RTO targets; validate clone integrity before prod                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Method      │       RPO        │        RTO        │    Retention     │      Notes       │   │
│   │     Snapshot     │      <5 min      │       <1 min      │    30-90 days    │    Local only    │   │
│   │    SnapVault     │      Hours       │     15-30 min     │    1-7 years     │    Secondary     │   │
│   │    SnapCenter    │      <1 min      │       <5 min      │   Policy-based   │   App consist.   │   │
│   │      Object      │      Hours       │     30-60 min     │      Years       │     S3/Grid      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: primary AFF cluster + secondary FAS/AFF cluster different rack or site                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ONTAP Snapshot  = Read-only point-in-time copy; shares blocks with active volume                   │
│    SnapVault       = Disk-to-disk backup replication; vault policy retains snapshots                  │
│    SnapCenter      = NetApp backup server; quiesces apps before snapshot                              │
│    Vault policy    = SnapVault label schedule: hourly/daily/weekly/monthly retention                  │
│    snap restore    = ONTAP CLI: volume snapshot restore; overwrites active volume                     │
│    snap restore -item = Single-file restore from snapshot without rollback                            │
│    Clone           = Writable FlexClone of snapshot; instant; space-efficient                         │
│    RPO             = Recovery Point Objective; max acceptable data loss in time                       │
│    RTO             = Recovery Time Objective; max acceptable downtime for restore                     │
│    App-consistent  = Backup taken with app quiesced (SQL VSS/Oracle RMAN)                             │
│    StorageGRID     = NetApp on-prem S3 object store; long-term vault target                           │
│    FlexClone       = Instant writable clone of volume/snapshot; shares blocks                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

## Restore Keystone Collector Configuration

```bash
# On new or rebuilt Collector VM:
scp ks-config-<date>.tar.gz admin@<new-collector-ip>:/tmp/

ssh admin@<new-collector-ip>
keystone-config import --input /tmp/ks-config-<date>.tar.gz

# Verify after import
keystone-config validate
keystone-collector status
```

## Pre-Upgrade Checklist

- [ ] Export Keystone Collector config to secure location
- [ ] Confirm all SnapMirror relationships are in healthy state
- [ ] Note current Collector version: `keystone-collector version`
- [ ] Download rollback image if upgrading Collector
- [ ] Confirm Keystone portal shows all arrays as healthy before starting
