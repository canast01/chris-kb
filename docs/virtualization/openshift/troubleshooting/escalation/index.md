# OpenShift — Escalation

<div class="kb-summary">
Red Hat support escalation process: severity levels, required data for support cases, SOS report generation, and escalation contacts for production-down situations.
</div>

```text
┌──────────────────────────────────── OpenShift Support Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Always attach must-gather to every support case; it is required for Red Hat to assist        │  │
│   │   Severity 1: production down — call Red Hat support immediately after opening case online        │
│   │   If stuck in a loop, request case escalation or a Technical Account Manager (TAM) review      │  │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Severity Levels        │  │      Required Data           │  │      Escalation Path        │ │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  Sev 1: production down     │  │  must-gather bundle          │  │  Open case online           │  │
│   │  Sev 2: major function lost │  │  SOS report from each node   │  │  Sev 1: call immediately   │   │
│   │  Sev 3: non-critical issues │  │  oc get clusterversion -o y  │  │  Escalate if no progress   │   │
│   │  Sev 4: general questions   │  │  Steps to reproduce timeline │  │  Request TAM for critical  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    must-gather  = Required cluster state bundle; run before opening any support case                  │
│    SOS report   = Node-level diagnostic (sosreport via toolbox); separate per affected node           │
│    TAM          = Technical Account Manager; assigned Red Hat contact for premium subscriptions       │
│    CEE          = Customer Engagement Engineer; the Red Hat support engineer assigned to your case    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Severity Levels

| Severity | Definition | Red Hat Response SLA |
|---|---|---|
| Sev 1 | Production system down; business-critical function completely unavailable | 1 hour (24×7) |
| Sev 2 | Major function lost; significant performance degradation in production | 4 business hours |
| Sev 3 | Non-critical failure; workaround available; limited functionality impacted | 1 business day |
| Sev 4 | General question, documentation request, or feature request | 2 business days |

## Pre-Escalation Checklist

```bash
# 1. Capture cluster version and update history
oc get clusterversion -o yaml > /tmp/clusterversion.yaml

# 2. Check all cluster operator statuses
oc get co > /tmp/co-status.txt

# 3. Capture recent events across cluster
oc get events -A --sort-by='.lastTimestamp' > /tmp/events.txt

# 4. Capture node status
oc get nodes -o wide > /tmp/nodes.txt
oc describe nodes > /tmp/nodes-describe.txt

# 5. Collect must-gather bundle (always required)
oc adm must-gather --dest-dir=/tmp/must-gather
tar czf must-gather-$(date +%F-%H%M).tar.gz /tmp/must-gather/

# 6. Note: exact symptoms, when they started, and any recent changes
# (upgrades, config changes, infrastructure changes, cert rotations)
```

## SOS Report (Per Node)

```bash
# Run on each affected node using toolbox (RHCOS nodes don't have sosreport natively)
oc debug node/<node-name>
chroot /host
toolbox

# Inside toolbox container:
sosreport --batch --label openshift-node

# Copy from node to local machine
# From separate terminal:
NODE_POD=$(oc get pods -n openshift-debug -o name | grep <node-name> | head -1)
oc cp <debug-pod>:/host/tmp/sosreport*.tar.xz /tmp/

# Run on multiple nodes in parallel if needed
for node in master-0 master-1 master-2; do
  echo "Starting sosreport on $node"
  oc debug node/$node -- chroot /host bash -c 'toolbox sosreport --batch --label openshift-escalation' &
done
```

## Opening a Support Case

Information to include:
1. **OpenShift version**: `oc get clusterversion -o jsonpath='{.status.desired.version}'`
2. **Infrastructure**: IPI/UPI, cloud/bare-metal/vSphere, network plugin (OVN-K/SDN)
3. **Node count**: control plane + worker count; any infra or storage nodes
4. **Timeline**: when did the issue start? what changed before it started?
5. **Symptoms**: exact error messages, affected components, blast radius
6. **Steps taken**: what you've already tried and the result
7. **Attachments**: must-gather bundle, sosreport(s), any relevant YAML/logs

```bash
# Collect OpenShift version info for case description
oc version
oc get clusterversion -o jsonpath='{.status.desired.version}'
oc get infrastructure cluster -o jsonpath='{.status.platformStatus.type}'
oc get network cluster -o jsonpath='{.spec.networkType}'
```

## Escalation Path

```text
1. Open support case at access.redhat.com with Sev 1/2
   ↓
2. For Sev 1: call Red Hat support phone immediately
   (number on access.redhat.com — varies by region)
   ↓
3. If no progress in 2-4 hours: request case escalation
   → Ask CEE to escalate to team lead or L3 engineering
   ↓
4. If still no progress: contact TAM (Technical Account Manager)
   → TAM can expedite internally and coordinate engineering resources
   ↓
5. For data corruption or security incidents: request Critical Situation (CritSit) team
```

## Useful Commands for Case Updates

```bash
# Verify issue persists (run before each update to RH)
oc get co | grep -v "True.*False.*False"   # operators not fully healthy
oc get nodes | grep -v " Ready "           # nodes not ready

# Snapshot current state with timestamp
oc get co,nodes,pods -A 2>&1 | tee /tmp/state-$(date +%F-%H%M).txt

# Get API server audit logs if authentication/authorization issue
oc adm inspect clusteroperator/kube-apiserver --dest-dir=/tmp/apiserver-inspect
# Includes audit log rotation in the bundle

# etcd health for etcd-related cases
oc get etcd cluster -o yaml | grep -A30 conditions

# Check if any nodes have high resource pressure
oc adm top nodes
oc adm top pods -A | sort -k3 -rn | head -20
```
