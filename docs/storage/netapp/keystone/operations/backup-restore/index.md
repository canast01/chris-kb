# NetApp Keystone — Backup & Restore

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

## ONTAP Snapshot Policy Backup

Underlying Keystone storage runs on ONTAP. Back up snapshot policy configurations.

```bash
# Via ONTAP CLI — list snapshot policies
snapshots policy show

# Export volume snapshot configuration for all Keystone volumes
volume show -vserver <keystone-svm> -fields snapshot-policy,space-guarantee

# List scheduled snapshot jobs
job schedule show
```

## SnapMirror Relationship Export

```bash
# List all SnapMirror relationships
snapmirror show -vserver <svm>

# Export to file (run from ONTAP SSH session)
snapmirror show -vserver <svm> > /tmp/snapmirror-$(date +%Y%m%d).txt
```

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
