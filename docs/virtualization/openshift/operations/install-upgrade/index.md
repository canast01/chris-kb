# OpenShift — Install & Upgrade

<div class="kb-summary">
OCP upgrade channels, EUS (Extended Update Support) path, version lifecycle, upgrade prerequisites, and step-by-step upgrade procedure with rollback considerations.
</div>

```text
┌─────────────────────────────────────── OpenShift Upgrade Path ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   CVO manages upgrades: downloads release image, updates operators, drains+reboots nodes      │   │
│   │   EUS path: 4.10 → 4.12 → 4.14 (skip minor); requires pause at intermediate EUS version      │    │
│   │   Always: check upgrade paths at access.redhat.com/labs/ocpupgradegraph before proceeding    │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Stable channel → patch → minor version; EUS channel → even minor versions only (4.10, 4.12, 4.14)  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Channels             │  │      Upgrade Steps           │  │       EUS Path              │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  stable-4.x: production     │  │  1. Set channel + version    │  │  4.y.z → 4.y+2.z upgrade    │  │
│   │  fast-4.x: early access     │  │  2. Drain workers (MCO)      │  │  Pause workers at 4.y+1.z  │   │
│   │  candidate-4.x: pre-release │  │  3. Upgrade control plane    │  │  EUS: skip intervening vers │  │
│   │  eus-4.x: even versions     │  │  4. Upgrade workers          │  │  Use eus-4.x channel        │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CVO          = Cluster Version Operator; manages OCP version and drives upgrades                   │
│    EUS          = Extended Update Support; even minor versions (4.10, 4.12) with longer support       │
│    MachineConfigPool= Groups nodes by role; workers upgrade node by node within their pool            │
│    Channel      = Release stream; set in ClusterVersion; determines available upgrades                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Upgrade Prerequisites

```bash
# 1. Check current version and channel
oc get clusterversion

# 2. Verify cluster health — no upgrade if degraded
oc get co | grep -v "True.*False.*False"
oc get nodes | grep -v Ready

# 3. Check available upgrade paths
oc adm upgrade

# 4. Validate upgrade path at:
#    https://access.redhat.com/labs/ocpupgradegraph

# 5. Check operator compatibility
oc get csv --all-namespaces | grep -v Succeeded

# 6. etcd backup (mandatory before upgrade)
# See backup-restore page
```

## Standard Upgrade Procedure

```bash
# Set channel (e.g. moving from fast to stable)
oc patch clusterversion version --type=json \
  -p '[{"op":"add","path":"/spec/channel","value":"stable-4.14"}]'

# Trigger upgrade to specific version
oc adm upgrade --to=4.14.5

# Or upgrade to latest in channel
oc adm upgrade --to-latest

# Monitor upgrade progress
oc get clusterversion -w
oc get co -w          # watch cluster operators update one by one

# Watch node upgrades (MCO drains and reboots nodes)
oc get nodes -w
oc get mcp -w         # MachineConfigPool progress
```

## EUS-to-EUS Upgrade (e.g. 4.12 → 4.14)

```bash
# 1. Switch to EUS channel for source version
oc patch clusterversion version --type=json \
  -p '[{"op":"add","path":"/spec/channel","value":"eus-4.12"}]'

# 2. Pause worker MachineConfigPool (prevent node reboots during control plane upgrade)
oc patch mcp worker --type=merge -p '{"spec":{"paused":true}}'

# 3. Upgrade control plane to 4.14 (skips worker reboots)
oc adm upgrade --to=4.14.5
oc get co -w          # watch control plane operators update

# 4. Switch channel to EUS target
oc patch clusterversion version --type=json \
  -p '[{"op":"add","path":"/spec/channel","value":"eus-4.14"}]'

# 5. Unpause workers (they will now drain+reboot with 4.14 config)
oc patch mcp worker --type=merge -p '{"spec":{"paused":false}}'
oc get mcp -w         # watch worker pool progress
```

## OCP Version Lifecycle

| Version | Type | GA | Full support end | Maintenance end |
|---|---|---|---|---|
| 4.12 | EUS | Jan 2023 | Jan 2024 | Jan 2025 |
| 4.13 | Standard | May 2023 | Nov 2023 | May 2024 |
| 4.14 | EUS | Oct 2023 | Oct 2024 | Oct 2025 |
| 4.15 | Standard | Feb 2024 | Aug 2024 | Feb 2025 |
| 4.16 | EUS | Jun 2024 | Jun 2025 | Jun 2026 |

Check current lifecycle: https://access.redhat.com/support/policy/updates/openshift

## Rollback Considerations

```bash
# OpenShift does NOT support downgrade after upgrade completes
# Options if upgrade fails mid-way:
# 1. Fix the blocking condition (most common — degraded CO)
# 2. Open Red Hat support case with must-gather
# 3. Restore from etcd backup (last resort — loses post-backup state)

# Check what's blocking the upgrade
oc get clusterversion -o yaml | grep -A20 "conditions:"
oc describe co <degraded-operator>
```
