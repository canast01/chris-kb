---
tags:
  - ceph
  - operations
---
# Ceph — Lifecycle & Upgrades

<div class="kb-summary">
Ceph cluster upgrades with cephadm: version compatibility, upgrade sequence (MON → MGR → OSD → MDS → RGW), monitoring upgrade progress, and rollback considerations.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
version_compatibility: "Version Compatibility" {shape: rectangle}
preupgrade_checklist: "Pre-Upgrade Checklist" {shape: rectangle}
upgrade_with_cephadm: "Upgrade with cephadm" {shape: rectangle}
rolling_upgrade_behaviour: "Rolling Upgrade Behaviour" {shape: rectangle}
majorversion_upgrade_requirements: "Major-Version Upgrade Requirements" {shape: rectangle}
postupgrade_validation: "Post-Upgrade Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> version_compatibility
version_compatibility -> preupgrade_checklist
preupgrade_checklist -> upgrade_with_cephadm
upgrade_with_cephadm -> rolling_upgrade_behaviour
rolling_upgrade_behaviour -> majorversion_upgrade_requirements
majorversion_upgrade_requirements -> postupgrade_validation
postupgrade_validation -> validate
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Version Compatibility

| Codename | Major Version | Status | EOL | Kernel RBD Client (min) |
|---|---|---|---|---|
| Squid | 19 | Current development | TBD | kernel 6.x |
| Reef | 18 | Current stable (LTS) | 2026+ | kernel 5.15+ |
| Quincy | 17 | Maintenance (LTS) | 2024 | kernel 5.10+ |
| Pacific | 16 | EOL | 2023 | kernel 5.4+ |
| Octopus | 15 | EOL | 2022 | kernel 4.15+ |

**Rules:**
- Never skip a major version. Pacific → Reef requires an intermediate Quincy upgrade.
- On each OSD node, `ceph osd require-osd-release` must match the current release before starting the next upgrade.
- Client kernels below the minimum may not support RBD features enabled post-upgrade; test before upgrading.

## Pre-Upgrade Checklist

| Check | Command | Required State |
|---|---|---|
| Cluster health | `ceph health` | `HEALTH_OK` |
| OSD in/out ratio | `ceph osd stat` | All OSDs `up` and `in` |
| PG states | `ceph pg stat` | All PGs `active+clean` |
| Recovery | `ceph -s \| grep recover` | 0 bytes recovering |
| Scrub activity | `ceph pg dump \| grep -c scrubbing` | 0 (pause if active) |
| Client compatibility | check kernel/client versions | Above minimum for target release |

```bash
# 1. Verify cluster is healthy — do not upgrade a degraded cluster
ceph health
# Must be HEALTH_OK

# 2. Verify all OSDs are up and in
ceph osd stat
# Expected: X osds: X up, X in

# 3. Check for active recovery (must be zero)
ceph -s | grep recovering
# Should show 0 bytes/objects recovering

# 4. Pause scrubs to reduce I/O contention during upgrade
ceph osd set noscrub
ceph osd set nodeep-scrub

# 5. Back up cluster configuration and auth keys
ceph config-key dump > ceph-config-backup-$(date +%F).json
ceph auth list > ceph-auth-backup-$(date +%F).txt

# 6. Check current version and what require-osd-release is set to
ceph version
ceph osd dump | grep require_osd_release
# These must agree; if not, update require-osd-release first

# 7. Check manager module health
ceph mgr module ls | grep -E "enabled_modules|disabled_modules"
```


```text title="Expected output"
HEALTH_OK
x osds: 12 up, 12 in
recovering 0 B/s, 0 objects/s
noscrub is set
nodeep-scrub is set
dumped all config-keys
exported auth(s)
ceph version 16.2.10 (45ac8adee3d3226cc9dd0850e2cd9150b4d60ed5) pacific (stable)
require_osd_release 16
enabled_modules: [balancer, status, prometheus, pg_stat]
disabled_modules: [dashboard, influx, insights, iostat, nfs, orchestrator, rbd_support, selftest, snap_schedule, telegraf, telemetry, test_orchestrator, volumes]
```

!!! warning "Common errors"
    **`HEALTH_WARN`** — Address the warning with `ceph health detail` and resolve underlying issues (e.g., slow requests, misplaced objects) before proceeding.
    **`error: (2) No such file or directory`** — Verify the Ceph cluster is initialized and the monitor is running with `ceph -s`; check `/etc/ceph/ceph.conf` exists and `CEPH_ARGS` environment variable is not overriding the cluster name.
    **`require_osd_release mismatch detected`** — Set the require-osd-release flag to match the current cluster version with `ceph osd set-require-osd-release <version>` before upgrading OSDs.
## Upgrade with cephadm

### Step 1 — Update cephadm itself

```bash
# Check cephadm version on bootstrap node
cephadm version

# Update cephadm to the latest build for the target release
# Disable and re-enable the mgr module to pick up the new binary
ceph mgr module disable cephadm
cephadm install          # re-downloads and installs latest cephadm binary
ceph mgr module enable cephadm

# Verify the mgr module is running
ceph mgr module ls | grep cephadm
```


```text title="Expected output"
cephadm version 16.2.11.45-1-g1a2b3c4d (octopus)
(no output — command completes silently)
(no output — command completes silently)
cephadm                           on  ceph-mgr.node-01.abc123def456
(no output — command completes silently)
cephadm                           on  ceph-mgr.node-01.abc123def456
```

!!! warning "Common errors"
    **`Error: No module named 'cephadm'`** — Ensure cephadm is installed on the bootstrap node with `curl --silent --remote-name --location https://github.com/ceph/ceph/raw/octopus/src/cephadm/cephadm && chmod +x cephadm`.
    **`Error: mgr module 'cephadm' is not available`** — Verify the Ceph cluster is healthy with `ceph health` and check that the mgr daemon is running with `ceph mgr stat`.
    **`command not found: cephadm`** — Add cephadm to your PATH or use the full path `/usr/sbin/cephadm` if installed via package manager.
### Step 2 — Start the rolling upgrade

```bash
# Specify the exact version or a container image tag
# quay.io/ceph/ceph:vX.Y.Z is the canonical source
ceph orch upgrade start --ceph-version 18.2.4
# Or specify image directly:
# ceph orch upgrade start --image quay.io/ceph/ceph:v18.2.4

# Upgrade daemon order (automatic, orchestrated by cephadm):
#   1. MGR daemons — active MGR fails over; standby becomes active
#   2. MON daemons — one at a time; quorum maintained throughout
#   3. OSD daemons — one at a time; cephadm sets noout automatically
#   4. MDS daemons — active MDS fails over to standby before upgrade
#   5. RGW daemons — rolling restart, gateway remains available
```


```text title="Expected output"
Upgrading to ceph version 18.2.4
Pulling image quay.io/ceph/ceph:v18.2.4
Image pulled successfully
Starting upgrade...
Upgrade started: 6a8f2c1e-9d4b-42f1-8c3a-7b2e5f9d1a4c
Upgrade progress:
  MGR: 2/2 daemons upgraded
  MON: 3/3 daemons upgraded
  OSD: 8/12 daemons upgraded (in progress)
  MDS: 1/1 daemons upgraded
  RGW: 2/2 daemons upgraded
Overall progress: 16/20 daemons complete (80%)
```

!!! warning "Common errors"
    **`Error: invalid ceph version '18.2.4'`** — Use the full semantic version format (e.g., `18.2.4`) or verify the version exists on quay.io/ceph/ceph.
    **`Error: unable to pull image quay.io/ceph/ceph:v18.2.4: connection timeout`** — Ensure the Ceph cluster nodes have outbound HTTPS access to quay.io or use a private registry mirror.
    **`Error: upgrade already in progress`** — Wait for the current upgrade to complete or use `ceph orch upgrade pause` then `ceph orch upgrade resume` to restart.
### Step 3 — Monitor upgrade progress

```bash
# Watch upgrade status — refreshes every 10 s
watch -n 10 ceph orch upgrade status
# Output shows:
#   target_image, progress (%), current daemon type being upgraded

# Secondary view — watch cluster health during upgrade
watch -n 5 "ceph -s | head -20"

# Inspect which daemons are still on the old version
ceph versions
# Example mid-upgrade output:
# {
#   "mon": {"ceph version 18.2.2": 3},
#   "mgr": {"ceph version 18.2.4": 2},
#   "osd": {"ceph version 18.2.2": 9, "ceph version 18.2.4": 3},
#   ...
# }

# Typical duration: 30–120 min depending on OSD count and rebalancing speed
```


```text title="Expected output"
Every 10.0s: ceph orch upgrade status                                                                                                                    Mon Jan 13 14:32:47 2025

TARGET IMAGE: quay.io/ceph/ceph:v18.2.4
PROGRESS: 45%
UPGRADING: osd

Every 5.0s: ceph -s | head -20                                                                                                                          Mon Jan 13 14:32:52 2025

  cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_WARN
            Degraded data redundancy: 156/468 objects degraded (33.3%), 52 pgs degraded
    
  services:
    mon: 3 daemons, quorum ceph-mon-01,ceph-mon-02,ceph-mon-03 (age 2h)
    mgr: 2 daemons, standbys: ceph-mgr-02
    osd: 12 osds: 9 up, 12 in; 45 degraded
    
  data:
    pools:   3 pools, 96 pgs
    objects: 468 objects, 1.2 TiB

{
  "mon": {
    "ceph version 18.2.2": 3
  },
  "mgr": {
    "ceph version 18.2.2": 1,
    "ceph version 18.2.4": 1
  },
  "osd": {
    "ceph version 18.2.2": 9,
    "ceph version 18.2.4": 3
  },
  "rgw": {
    "ceph version 18.2.4": 2
  }
}
```

!!! warning "Common errors"
    **`Error: No orchestrator backend found`** — Ensure Cephadm is deployed with `ceph orch status` and that the mgr orchestrator module is enabled.
    **`Error: upgrade already in progress`** — Wait for the current upgrade to complete or check `ceph orch upgrade pause` to pause and resume safely.
### Step 4 — Pause and resume if needed

```bash
# Pause upgrade (e.g., unexpected HEALTH_WARN during OSD upgrades)
ceph orch upgrade pause

# Check cluster health while paused
ceph health detail
ceph -s

# Resume when cluster is stable
ceph orch upgrade resume

# Stop upgrade entirely (reverts plan but does not downgrade already-upgraded daemons)
ceph orch upgrade stop
```


```text title="Expected output"
Upgrade paused
HEALTH_WARN [WRN] OSD_DOWN: 1 osd(s) down
    osd.3 is down (since 2m)
[WRN] PG_DEGRADED: Degraded data, 128 pg(s) degraded
    128 active+degraded
[WRN] SLOW_OPS: 12 slow ops, oldest one blocked for 45 sec

cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_WARN
    mon: 3 daemons, quorum mon.0,mon.1,mon.2 (age 3h)
    mgr: mgr.host1(active, since 2h), mgr.host2(standby, since 2h)
    osd: 12 osds: 11 up, 1 down; 10 in, 1 out
    data: 2.4 TiB used, 9.6 TiB / 12 TiB avail
    pgs: 256 active+clean; 128 active+degraded

Upgrade resumed
Upgrade stopped
```

!!! warning "Common errors"
    **`Error ENOENT: no upgrade in progress`** — Ensure an upgrade was actually initiated with `ceph orch upgrade start` before attempting to pause or resume.
    **`Error EINVAL: cannot pause: upgrade is already paused`** — Check current upgrade state with `ceph orch upgrade status` before issuing pause/resume commands.
## Rolling Upgrade Behaviour

- cephadm pulls the new container image on each host before restarting the daemon.
- OSDs: cephadm waits for in-flight I/O to drain before killing the OSD process; the `noout` flag is set cluster-wide automatically and unset after all OSDs are upgraded.
- MONs: Ceph requires a quorum of MONs at all times; cephadm never restarts more than one MON simultaneously.
- If a daemon fails to come back after upgrade, cephadm halts and waits; the operator must investigate before the upgrade continues.

## Major-Version Upgrade Requirements

```bash
# After completing all daemon upgrades (e.g., Pacific → Quincy):
# 1. Confirm all daemons are on the new version
ceph versions
# All entries must show the new major version

# 2. Update the OSD release flag to unlock new features
ceph osd require-osd-release quincy
# Replace "quincy" with the codename for your target version

# 3. Enable new CRUSH features (if applicable)
ceph osd set-require-min-compat-client reef
# Only run this if all clients (RBD, CephFS, RGW) support the new release

# 4. Re-enable scrubs
ceph osd unset noscrub
ceph osd unset nodeep-scrub
```


```text title="Expected output"
{
  "mon": [
    {
      "version": "ceph version 17.2.5 (quincy)",
      "release": "quincy",
      "num": 3
    }
  ],
  "mgr": [
    {
      "version": "ceph version 17.2.5 (quincy)",
      "release": "quincy",
      "num": 2
    }
  ],
  "osd": [
    {
      "version": "ceph version 17.2.5 (quincy)",
      "release": "quincy",
      "num": 12
    }
  ],
  "rgw": [
    {
      "version": "ceph version 17.2.5 (quincy)",
      "release": "quincy",
      "num": 2
    }
  ]
}
set require-osd-release to quincy
set-require-min-compat-client reef
noscrub is unset
nodeep-scrub is unset
```

!!! warning "Common errors"
    **`Error EPERM: insufficient caps`** — Run the commands with appropriate admin privileges (e.g., as root or with `sudo ceph`) and ensure your keyring has `osd` capability.
    **`Error EINVAL: invalid release name 'quincy'`** — Verify the release codename matches your target version exactly (e.g., `reef`, `squid`) and that all daemons have already been upgraded to that version.
## Post-Upgrade Validation

| Check | Command | Expected Result |
|---|---|---|
| All daemons on new version | `ceph versions` | Single version entry per daemon type |
| Cluster health | `ceph health` | `HEALTH_OK` |
| PG states | `ceph pg stat` | All PGs `active+clean` |
| OSD feature flags | `ceph osd features` | New release features present |
| Dashboard | `ceph mgr services` | Dashboard URL resolves, shows new version |

```bash
# Verify all daemons report the new version
ceph versions
# All entries must show target version only
# Example: {"mon": {"ceph version 18.2.4": 3}, "osd": {"ceph version 18.2.4": 12}, ...}

# Run full health check
ceph health detail
# Expected: HEALTH_OK

# Confirm PG states recovered
ceph pg stat
# All PGs should be active+clean

# Test I/O — write and read benchmark
rbd create --size 5G rbd/upgrade-test
rbd bench --io-type write --io-size 4K --io-threads 16 --io-total 512M rbd/upgrade-test
rbd bench --io-type read  --io-size 4K --io-threads 16 --io-total 512M rbd/upgrade-test
rbd rm rbd/upgrade-test

# Verify OSD feature flags reflect new release
ceph osd features
# New features should be listed for the target codename

# Check dashboard is accessible and shows correct cluster version
ceph mgr services | grep dashboard
```


```text title="Expected output"
{
  "mon": {
    "ceph version 18.2.4 (3a54dda6149a4ff917b4742500cdb3161b231271)": 3
  },
  "mgr": {
    "ceph version 18.2.4 (3a54dda6149a4ff917b4742500cdb3161b231271)": 2
  },
  "osd": {
    "ceph version 18.2.4 (3a54dda6149a4ff917b4742500cdb3161b231271)": 12
  },
  "mds": {
    "ceph version 18.2.4 (3a54dda6149a4ff917b4742500cdb3161b231271)": 2
  }
}
cluster 8f7a3c2b-1d4e-4a9f-b8c1-5e6d7f9a2c3b
 health HEALTH_OK
 monmap e5: 3 mons at {mon01=10.0.1.10:6789/0,mon02=10.0.1.11:6789/0,mon03=10.0.1.12:6789/0}
 osdmap e847: 12 osds: 12 up, 12 in
 pgmap v2156: 256 pgs: 256 active+clean; 847 GiB data, 2.1 TiB used, 8.9 TiB / 11 TiB avail
 mdsmap e42: 2/2 up {0,1}, 2 up:active
Created image 'upgrade-test' in pool 'rbd'
  sec  Cur ops   ops/sec   ops/sec   bytes/sec   bytes/sec
    1       16    4096.0    4096.0    16.4 MiB   16.4 MiB
    2       16    4088.0    4092.0    16.4 MiB   16.4 MiB
  ...
  128       16    4102.0    4099.2    16.4 MiB   16.4 MiB
Total time run:       128.456 sec
Total ops:            524288
Total bytes:          512 MiB
Bandwidth (MiB/sec):  3.98
Stddev Bandwidth:     0.12
Max bandwidth (MiB/sec): 4.21
Min bandwidth (MiB/sec): 3.76
  sec  Cur ops   ops/sec   ops/sec   bytes/sec   bytes/sec
    1       16    4156.0    4156.0    16.6 MiB   16.6 MiB
  ...
  128       16    4089.0    4098.5    16.4 MiB   16.4 MiB
Total time run:       125.123 sec
Total ops:            524288
Total bytes:          512 MiB
Bandwidth (MiB/sec):  4.09
Stddev Bandwidth:     0.08
Max bandwidth (MiB/sec): 4.31
Min bandwidth (MiB/sec):
```
## Rollback Considerations

Ceph does **not** support automatic rollback. Key points:

- Daemons that have already been upgraded to the new image cannot be automatically reverted without manual intervention.
- If the upgrade is paused or stopped mid-way, the cluster will run a mixed-version state, which is stable for short periods but should be resolved promptly.
- To manually revert a specific daemon to the old image:

```bash
# Pin a specific daemon to an older image (emergency use only)
ceph orch daemon redeploy <daemon-type>.<id> --image quay.io/ceph/ceph:v18.2.2

# Example: revert a specific MGR
ceph orch daemon redeploy mgr.ceph-node1 --image quay.io/ceph/ceph:v18.2.2
```


```text title="Expected output"
Scheduled mgr.ceph-node1 redeploy with image quay.io/ceph/ceph:v18.2.2
```

!!! warning "Common errors"
    **`Error EINVAL: unknown daemon type <daemon-type>`** — Replace `<daemon-type>` with a valid daemon type (mon, mgr, osd, mds, rgw, etc.).
    **`Error: No such daemon mgr.ceph-node1`** — Verify the daemon exists by running `ceph orch ps` and use the correct daemon name from the output.
    **`Error pulling image quay.io/ceph/ceph:v18.2.2: image not found`** — Ensure the image tag exists in the registry and the host has network access to quay.io.
- Major version rollback (e.g., Reef → Quincy) is not supported and will corrupt OSD data if attempted after `ceph osd require-osd-release` has been updated.

---

## See also

- [Ceph — Health Checks](../health-checks/)
- [Ceph — Common Issues](../../troubleshooting/common-issues/)
- [Ceph — Procedures](../procedures/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
