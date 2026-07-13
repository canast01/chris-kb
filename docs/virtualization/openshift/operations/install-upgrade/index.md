---
tags:
  - operations
description: "OCP upgrade channels, EUS (Extended Update Support) path, version lifecycle, upgrade prerequisites, pause-worker pattern, multi-hop upgrades, and rollback..."
---
# OpenShift — Install & Upgrade

<div class="kb-summary">
OCP upgrade channels, EUS (Extended Update Support) path, version lifecycle, upgrade prerequisites, pause-worker pattern, multi-hop upgrades, and rollback considerations.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
upgrade_flow: "Upgrade Flow" {shape: rectangle}
channel_selection: "Channel Selection" {shape: rectangle}
upgrade_prerequisites_checklist: "Upgrade Prerequisites Checklist" {shape: rectangle}
standard_upgrade_procedure: "Standard Upgrade Procedure" {shape: rectangle}
upgrade_command_reference: "Upgrade Command Reference" {shape: rectangle}
pause_worker_machineconfigpool: "Pause Worker MachineConfigPool" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> upgrade_flow
upgrade_flow -> channel_selection
channel_selection -> upgrade_prerequisites_checklist
upgrade_prerequisites_checklist -> standard_upgrade_procedure
standard_upgrade_procedure -> upgrade_command_reference
upgrade_command_reference -> pause_worker_machineconfigpool
pause_worker_machineconfigpool -> validate
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Upgrade Flow

## Channel Selection

| Channel | Purpose | Release cadence | Recommended for |
|---------|---------|-----------------|-----------------|
| `stable-4.x` | Production; errata-qualified | ~1–2 weeks after fast | All production clusters |
| `fast-4.x` | Early access; GA but less soak | Days after GA | Dev/staging; risk-tolerant prod |
| `candidate-4.x` | Pre-release RC builds | Continuous | Testing only; not supported in prod |
| `eus-4.x` | Extended Update Support (even minors) | ~18-month support window | Clusters requiring long upgrade windows |

```bash
# Check current channel
oc get clusterversion -o jsonpath='{.items[0].spec.channel}'

# Switch channel
oc adm upgrade channel stable-4.14

# Or via patch
oc patch clusterversion version --type=json \
  -p '[{"op":"add","path":"/spec/channel","value":"stable-4.14"}]'

# List available versions after channel switch
oc adm upgrade
```


```text title="Expected output"
stable-4.13
(no output — command completes silently)
(no output — command completes silently)
Cluster version is 4.13.12
Updates available:
  VERSION     IMAGE
  4.13.13     quay.io/openshift-release-dev/ocp-release@sha256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  4.14.0      quay.io/openshift-release-dev/ocp-release@sha256:f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5
  4.14.1      quay.io/openshift-release-dev/ocp-release@sha256:p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "clusterversion" in group "config.openshift.io" in the namespace "default"` | Ensure you are connected to an OpenShift cluster with `oc login` and have cluster-admin permissions. |
    | `Error from server (Forbidden): clusterversions.config.openshift.io "version" is forbidden: User "system:serviceaccount:default:deployer" cannot patch resource "clusterversions" in API group "config.openshift.io" at the cluster scope` | Run the command as a user with cluster-admin role using `oc adm policy add-cluster-role-to-user cluster-admin <username>`. |
**EUS channels** apply only to even-numbered minor versions (4.10, 4.12, 4.14, 4.16). Subscriptions to an EUS channel unlock the EUS-to-EUS upgrade path; odd-version intermediate releases are not available in EUS channels.

## Upgrade Prerequisites Checklist

All conditions must be true before triggering an upgrade. A single degraded operator blocks the upgrade from completing.

| Check | Command | Pass Condition |
|-------|---------|----------------|
| No degraded operators | `oc get co \| grep -v "True.*False.*False"` | No output |
| All nodes Ready | `oc get nodes \| grep -v " Ready"` | No NotReady nodes |
| MCPs not degraded | `oc get mcp` | All `DEGRADED=False` |
| etcd healthy | `oc rsh -n openshift-etcd etcd-<m0> etcdctl endpoint health --cluster` | All healthy |
| CSVs succeeded | `oc get csv -A \| grep -v Succeeded` | No non-Succeeded CSVs |
| Sufficient PDB budget | `oc get pdb -A` | No PDBs blocking drain |
| etcd backup taken | See backup-restore page | Backup file confirmed |

```bash
# Single-liner health pre-check
oc get co | grep -v "True.*False.*False" | grep -v "^NAME" && \
oc get nodes | grep -v " Ready" | grep -v "^NAME" && \
oc get mcp | grep -v "^NAME" && \
echo "Pre-checks PASSED"
```


```text title="Expected output"
NAME                                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
authentication                             4.12.15   True        False         False      2d
baremetal                                  4.12.15   True        False         False      2d
cloud-credential                           4.12.15   True        False         False      2d
cluster-autoscaler                         4.12.15   True        False         False      2d
Pre-checks PASSED
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "co"` | Ensure you are connected to a valid OpenShift cluster with `oc login` and have sufficient permissions. |
    | `grep: (standard input) is empty` | This occurs when all cluster operators are healthy; add `|| true` at the end of each grep chain to allow the script to continue on empty results. |
## Standard Upgrade Procedure

```bash
# 1. Set channel
oc adm upgrade channel stable-4.14

# 2. Review available versions and recommended path
oc adm upgrade

# 3. Trigger upgrade to specific version (recommended — never use --to-latest in prod)
oc adm upgrade --to=4.14.5

# 4. Monitor ClusterVersion
oc get clusterversion -w
# Progressing=True while upgrading; Progressing=False + version updated = done

# 5. Monitor cluster operators (update sequentially, ~30-60 min total)
oc get co -w

# 6. Monitor node upgrades (MCO drains and reboots)
oc get nodes -w
oc get mcp -w
# MachineConfigPool: UPDATED=True, DEGRADED=False = done

# 7. Confirm completion
oc get clusterversion
# STATUS field: "Cluster version is 4.14.5"
```


```text title="Expected output"
# 1. Set channel
(no output — command completes silently)

# 2. Review available versions and recommended path
Upstream is unset, so the cluster will use an appropriate default.
Channel: stable-4.14
Desired: 4.14.5
Current: 4.14.3
Updates available:
  VERSION     IMAGE
  4.14.4      quay.io/openshift-release-dev/ocp-release@sha256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
  4.14.5      quay.io/openshift-release-dev/ocp-release@sha256:b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a
  4.15.0      quay.io/openshift-release-dev/ocp-release@sha256:c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1b

# 3. Trigger upgrade to specific version
Upgrade initiated to version 4.14.5

# 4. Monitor ClusterVersion
NAME             VERSION   AVAILABLE   PROGRESSING   SINCE   STATUS
version          4.14.3    True        True          2m      Working towards 4.14.5
version          4.14.3    True        True          5m      Working towards 4.14.5
version          4.14.4    True        True          12m     Working towards 4.14.5
version          4.14.5    True        False         18m     Cluster version is 4.14.5

# 5. Monitor cluster operators
NAME                                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE
authentication                             4.14.5    True        False         False      8m
cloud-credential-operator                  4.14.5    True        False         False      7m
cluster-autoscaler                         4.14.5    True        False         False      9m
config-operator                            4.14.5    True        False         False      6m
...

# 6. Monitor node upgrades
NAME                    STATUS   ROLES           AGE    VERSION
worker-0.example.com    Ready    worker          45d    v1.27.6
worker-1.example.com    Ready    worker          45d    v1.27.6
master-0.example.com    Ready    control-plane   45d    v1.27.6
master-1.example.com    Ready    control-plane   45d    v1.27.6
master-2.example.com    Ready    control-plane   45d    v1.27.6

NAME                                    CONFIG                                   UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT   UNAVAILABLEMACHINECOUNT   AGE
master                                  rendered-master-a1b2c3d4e5f6g7h8        True      False      False      3              3                   0
```
## Upgrade Command Reference

| Command | Description |
|---------|-------------|
| `oc adm upgrade` | Show current version, channel, and available upgrades |
| `oc adm upgrade channel <channel>` | Set upgrade channel |
| `oc adm upgrade --to=<version>` | Trigger upgrade to specific version |
| `oc adm upgrade --to-image=<digest>` | Upgrade to specific image hash (multi-hop, disconnected) |
| `oc get clusterversion` | Show version, channel, Progressing/Degraded conditions |
| `oc describe clusterversion` | Full conditions, history, and error messages |
| `oc get co` | All cluster operators with Available/Progressing/Degraded columns |
| `oc get mcp` | MachineConfigPool status — node count, updated count, degraded |
| `oc get nodes -w` | Watch node STATUS during MCO-driven reboots |

## Pause Worker MachineConfigPool

Pausing the worker MCP prevents worker nodes from rebooting during control plane upgrade. Required for EUS-to-EUS; optional for standard upgrades to reduce disruption window.

```bash
# Pause workers before upgrade
oc patch mcp worker --type merge -p '{"spec":{"paused":true}}'

# Verify paused
oc get mcp worker -o jsonpath='{.spec.paused}'    # → true

# Trigger upgrade (only control plane reboots)
oc adm upgrade --to=4.14.5
oc get co -w                          # Wait for all operators to complete

# After control plane done — resume workers
oc patch mcp worker --type merge -p '{"spec":{"paused":false}}'
oc get mcp -w                         # Watch worker pool drain+reboot
```


```text title="Expected output"
machineconfigpool.machineconfigpools.openshift.io/worker patched
true
Updating to 4.14.5
NAME                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE
authentication             4.14.5    True        False         False      2m14s
baremetal                  4.14.5    True        False         False      2m8s
cloud-credential           4.14.5    True        False         False      2m22s
cluster-autoscaler         4.14.5    True        False         False      2m19s
cluster-version            4.14.5    False       True          False      3m1s
console                    4.14.5    True        False         False      2m5s
...
machineconfigpool.machineconfigpools.openshift.io/worker patched
NAME     CONFIG                                 UPDATED   UPDATING   DEGRADED   NODES   READY   UNAVAILABLE   AGE
master   rendered-master-a1b2c3d4e5f6g7h8i     True      False      False      3       3       0             45d
worker   rendered-worker-f8g7h6i5e4d3c2b1a     False     True       False      5       3       2             45d
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "mcp"` | Use the full resource name `machineconfigpool` or ensure the OpenShift CLI is updated to version 4.10+. |
    | `Unable to connect to the server: dial tcp: lookup api.cluster.local on 127.0.0.1:53: no such host` | Verify your kubeconfig is set correctly with `export KUBECONFIG=/path/to/kubeconfig` and the cluster API is reachable. |
> **Warning:** Do not leave worker MCP paused after upgrade completes. Nodes will be out of sync with the cluster config until resumed.

## EUS-to-EUS Upgrade (e.g. 4.12 → 4.14)

```bash
# 1. Switch to EUS channel for source version
oc patch clusterversion version --type=json \
  -p '[{"op":"add","path":"/spec/channel","value":"eus-4.12"}]'

# 2. Pause worker MachineConfigPool
oc patch mcp worker --type=merge -p '{"spec":{"paused":true}}'

# 3. Upgrade to intermediate version (4.13.z) — required even for EUS skip
oc adm upgrade --to=4.13.27          # Check oc adm upgrade for correct z-stream
oc get co -w                          # Wait for operators to complete

# 4. Switch to EUS channel for intermediate
oc patch clusterversion version --type=json \
  -p '[{"op":"add","path":"/spec/channel","value":"eus-4.14"}]'

# 5. Upgrade to 4.14 target
oc adm upgrade --to=4.14.5
oc get co -w

# 6. Unpause workers (they upgrade from 4.12 config directly to 4.14)
oc patch mcp worker --type=merge -p '{"spec":{"paused":false}}'
oc get mcp -w
```


```text title="Expected output"
clusterversion.config.openshift.io/version patched
machineconfigpool.machineconfiguration.openshift.io/worker patched
Updating to version 4.13.27
NAME                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
authentication             4.12.15   True        False         False      10m     
cluster-autoscaler         4.12.15   True        False         False      10m     
cluster-storage-operator   4.12.15   True        False         False      10m     
console                    4.12.15   True        True          False      2m      Working towards 4.13.27
dns                        4.12.15   True        False         False      10m     
etcd                       4.12.15   True        False         False      10m     
...
clusterversion.config.openshift.io/version patched
Updating to version 4.14.5
NAME                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
authentication             4.13.27   True        True          False      1m      Working towards 4.14.5
cluster-autoscaler         4.13.27   True        False         False      8m      
console                    4.13.27   True        True          False      45s     Working towards 4.14.5
...
machineconfigpool.machineconfiguration.openshift.io/worker patched
NAME     CONFIG                                   UPDATED   UPDATING   DEGRADED   UNAVAILABLE   AGE
master   rendered-master-a1b2c3d4e5f6g7h8i9j0   True      False      False      0             45d
worker   rendered-worker-x9y8z7w6v5u4t3s2r1q0   False     True       False      2             45d
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "clusterversion"` | Ensure you are logged in with `oc login` to a valid OpenShift cluster and have cluster-admin permissions. |
    | `Unable to find version 4.13.27 in the available updates` | Run `oc adm upgrade` without arguments to list available versions, then use a valid intermediate z-stream from the output. |
    | `machine-config-daemon on node worker-0 is degraded` | Wait for the worker node to finish applying the paused MachineConfig before unpausing, or check `oc describe node worker-0` for blocking conditions. |
## Multi-Hop Upgrade

OCP upgrade graph enforces version adjacency. Some versions require traversing an intermediate release. The upgrade graph at `access.redhat.com/labs/ocpupgradegraph` shows valid paths.

```bash
# Check if direct path exists
oc adm upgrade
# If desired version not listed, an intermediate hop is required

# Upgrade to intermediate first
oc adm upgrade --to=4.13.27
# Wait for completion, then:
oc adm upgrade --to=4.14.5

# For disconnected (specific image digest)
oc adm upgrade --to-image=quay.local:8443/ocp4/openshift/release:4.14.5-x86_64 \
  --allow-explicit-upgrade
```


```text title="Expected output"
Desired version: 4.14.5
Cluster version: 4.12.8

Available updates:
  VERSION     IMAGE
  4.13.27     quay.io/openshift-release-dev/ocp-release:4.13.27-x86_64
  4.13.28     quay.io/openshift-release-dev/ocp-release:4.13.28-x86_64

Upgrade to intermediate first
Updating to version 4.13.27
Cluster Version Operator is unavailable
Cluster is updating: 4.12.8 -> 4.13.27 (100 of 600 seconds)

Updating to version 4.14.5
Cluster is updating: 4.13.27 -> 4.14.5 (45 of 720 seconds)

Updating to image quay.local:8443/ocp4/openshift/release:4.14.5-x86_64
Cluster is updating: 4.14.5 -> 4.14.5 (disconnected, 12 of 180 seconds)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server has asked for the client to provide credentials` | Ensure your kubeconfig is valid and you are logged in with `oc login` to the cluster. |
    | `error: unable to find image "quay.local:8443/ocp4/openshift/release:4.14.5-x86_64" locally` | Verify the image digest exists in your disconnected registry and the registry hostname/port are accessible from all nodes. |
    | `error: upgrade cannot proceed: DesiredReleaseInvalid` | Confirm the target version exists in the update graph by running `oc adm upgrade` without arguments, or use an intermediate version if a direct path is unavailable. |
## OCP Version Lifecycle

| Version | Type | GA | Full support end | Maintenance end |
|---------|------|----|------------------|-----------------|
| 4.12 | EUS | Jan 2023 | Jan 2024 | Jan 2025 |
| 4.13 | Standard | May 2023 | Nov 2023 | May 2024 |
| 4.14 | EUS | Oct 2023 | Oct 2024 | Oct 2025 |
| 4.15 | Standard | Feb 2024 | Aug 2024 | Feb 2025 |
| 4.16 | EUS | Jun 2024 | Jun 2025 | Jun 2026 |
| 4.17 | Standard | Oct 2024 | Apr 2025 | Oct 2025 |
| 4.18 | EUS | Feb 2025 | Feb 2026 | Feb 2027 |

Current lifecycle: https://access.redhat.com/support/policy/updates/openshift

## Rollback Considerations

OpenShift **does not support automatic rollback** after an upgrade completes. Once the control plane is updated, there is no supported downgrade path.

| Scenario | Recovery Option | Notes |
|----------|----------------|-------|
| Upgrade stalled on degraded CO | Fix CO condition; upgrade resumes automatically | Most common scenario |
| Upgrade stalled on node drain | Fix pod preventing drain (PDB, stuck finalizer) | `oc drain <node> --delete-emptydir-data --ignore-daemonsets` |
| Control plane updated, workers failing | Open RH support; consider etcd restore | Partial upgrade state |
| Catastrophic failure, data loss acceptable | Restore from etcd backup | Loses all post-backup state |
| Catastrophic failure, fresh start | Re-install cluster | Requires full workload re-deploy |

```bash
# Investigate stalled upgrade
oc get clusterversion -o yaml | grep -A30 "conditions:"
oc describe co <degraded-operator>

# Force-resume a stuck operator (use only on RH guidance)
oc patch co <operator> --type=json \
  -p '[{"op":"remove","path":"/status/conditions"}]'

# Check what's blocking a node drain
oc get pods -A --field-selector=spec.nodeName=<node>
oc get pdb -A

# etcd backup restore — see backup-restore page
# etcdctl snapshot restore → re-bootstrap control plane
```


```text title="Expected output"
conditions:
- lastTransitionTime: "2024-01-15T09:23:47Z"
  message: "ClusterOperatorDegraded: operator/kube-apiserver is degraded"
  reason: ClusterOperatorDegraded
  status: "True"
  type: Degraded
- lastTransitionTime: "2024-01-15T09:15:12Z"
  message: "MultipleErrors: etcd quorum lost, 1 of 3 members unavailable"
  reason: MultipleErrors
  status: "True"
  type: Progressing

Name:                  kube-apiserver
Namespace:             openshift-kube-apiserver
Labels:                <none>
Status:                Degraded
Conditions:
  Type                 Status  LastTransitionTime      Reason
  ----                 ------  ------------------      ------
  Degraded             True    2024-01-15T09:23:47Z   NodeInstallerDegraded
  Progressing          True    2024-01-15T09:15:12Z   NodeInstallerProgressing

clusteroperator.config.openshift.io/kube-apiserver patched

NAME                                    READY   STATUS    RESTARTS   AGE     NODE
etcd-member-ip-10-0-1-45.ec2.internal  1/1     Running   0          2d14h   master-0
coredns-7f4d8c9b5d-2k9wx               0/1     Evicted   0          4h12m   worker-1
openshift-sdn-8xjkl                     1/1     Running   0          3d8h    worker-2

NAME                                    MIN AVAILABLE   AGE
poddisruptionbudget-etcd-backup         1               45d
poddisruptionbudget-ingress-controller  2               60d
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "co"` | Use the full resource name `clusteroperator` instead of the alias `co`, or verify the API group with `oc api-resources | grep operator`. |
    | `Error from server (NotFound): clusteroperators.config.openshift.io "<operator>" not found` | Verify the operator name exists with `oc get clusteroperator` and check for typos in the degraded operator name. |
    | `error: unable to patch the resource with name "<operator>"` | Ensure you have cluster-admin privileges with `oc auth can-i patch clusteroperators` and only apply patches on explicit Red Hat support guidance. |
---

## See also

- [OpenShift — Health Checks](../health-checks/)
- [OpenShift — Common Issues](../../troubleshooting/common-issues/)
- [OpenShift — Procedures](../procedures/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
