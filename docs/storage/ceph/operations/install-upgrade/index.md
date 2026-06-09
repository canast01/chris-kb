# Ceph — Lifecycle & Upgrades

<div class="kb-summary">
Ceph cluster upgrades with cephadm: version compatibility, upgrade sequence (MON → MGR → OSD → MDS → RGW), monitoring upgrade progress, and rollback considerations.
</div>

```text
┌───────────────────────────────────── Ceph — Lifecycle & Upgrades ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   cephadm handles upgrade orchestration; upgrades one daemon at a time with health checks     │   │
│   │   Sequence: MON → MGR → OSD → MDS → RGW → RBD mirror; never skip major versions             │     │
│   │   Pre-upgrade: ensure HEALTH_OK + all OSDs up+in + no active recovery                         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Release Calendar

| Release | Status | Notes |
|---|---|---|
| Reef (18) | Current stable | LTS; cephadm default |
| Quincy (17) | Maintenance | LTS; supported until 2024 |
| Pacific (16) | EOL | Upgrade to Reef |
| Octopus (15) | EOL | Last version before cephadm standard |

## Pre-Upgrade Checklist

```bash
# 1. Verify cluster is healthy
ceph health
# Must be HEALTH_OK — do not upgrade a degraded cluster

# 2. Verify all OSDs up+in
ceph osd stat
# Expected: X osds: X up, X in

# 3. Check for any ongoing recovery
ceph -s | grep recovering
# Should show 0 bytes/objects recovering

# 4. Back up cluster config
ceph config-key dump > ceph-config-backup-$(date +%F).json
ceph auth list > ceph-auth-backup-$(date +%F).txt

# 5. Verify mgr module health
ceph mgr module ls | grep -E "enabled|disabled"
```

## Upgrade with cephadm

```bash
# Check current version
ceph version

# List available images
# Ceph container images are at quay.io/ceph/ceph
# Find target version: https://docs.ceph.com/en/latest/releases/

# Pull target image on all nodes
ceph orch upgrade start --image quay.io/ceph/ceph:v18.2.2

# Monitor upgrade progress
watch -n 10 ceph orch upgrade status
# Shows: current component being upgraded, progress percentage, ETA

# What happens during upgrade:
# 1. cephadm upgrades MON daemons one at a time
# 2. Then MGR daemons (active MGR failovers)
# 3. Then all OSD daemons (one at a time; waits for recovery between each)
# 4. Then MDS, then RGW
# Takes: 30-120 min depending on cluster size and OSD rebalancing speed

# Verify after upgrade
ceph versions   # all daemons should report new version
ceph health
```

## Post-Upgrade Validation

```bash
# Verify all daemons updated
ceph versions
# All entries should show the new version

# Run full health check
ceph health detail

# Test I/O (RBD benchmark)
rbd bench --io-type write --io-size 4K --io-threads 16 --io-total 512M rbd/upgrade-test
rbd rm rbd/upgrade-test

# Verify feature flags updated for any new CRUSH or OSD features
ceph osd features
```
