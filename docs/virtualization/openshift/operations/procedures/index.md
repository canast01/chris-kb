---
tags:
  - operations
---
# OpenShift — Procedures

<div class="kb-summary">
Common operational procedures: node drain and maintenance mode, scaling MachineSets, adding node roles, rotating certificates, etcd member recovery, kubeadmin rotation, and deployment rollout management.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

NM: "Node Maintenance" {shape: rectangle}
C: "1. cordon node" {shape: rectangle}
D: "2. drain --ignore-daemonsets" {shape: rectangle}
V: "3. verify pods migrated" {shape: rectangle}
W: "4. perform maintenance" {shape: rectangle}
U: "5. uncordon" {shape: rectangle}
RD: "6. verify Ready + rescheduled" {shape: rectangle}
OU: "Operator Update" {shape: rectangle}
PM: "pause MachineConfigPool" {shape: rectangle}
UP: "trigger update" {shape: rectangle}
RM: "resume MachineConfigPool" {shape: rectangle}
WC: "watch MCP UPDATED" {shape: rectangle}
CR: "Certificate Rotation" {shape: rectangle}
CE: "check expiry dates" {shape: rectangle}
RN: "renew / approve CSRs" {shape: rectangle}
VR: "verify new cert dates" {shape: rectangle}

NM -> C
C -> D
D -> V
V -> W
W -> U
U -> RD
OU -> PM
PM -> UP
UP -> RM
RM -> WC
CR -> CE
CE -> RN
RN -> VR
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Node Maintenance Procedure

Full sequence for taking a node offline without losing workloads.

```bash
# 1. Pre-check — ensure cluster is healthy before touching any node
oc get co | grep -v "True.*False.*False"
oc get nodes

# 2. Cordon — mark node unschedulable (no new pods land here)
oc adm cordon <node-name>

# 3. Drain — evict all evictable pods
oc adm drain <node-name> \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=60 \
  --timeout=300s
# --ignore-daemonsets: DaemonSet pods are not evicted (they restart on uncordon)
# --delete-emptydir-data: allows pods using emptyDir volumes to be evicted

# 4. Verify — confirm no non-DaemonSet pods remain on the node
oc get pods --all-namespaces -o wide | grep <node-name> | grep -v "DaemonSet\|Completed"

# 5. Perform maintenance (reboot, firmware update, disk swap, etc.)

# 6. Uncordon — allow new scheduling
oc adm uncordon <node-name>

# 7. Verify node returns Ready
oc get node <node-name>

# 8. Verify pods reschedule back if needed
oc get pods --all-namespaces -o wide | grep <node-name>
```

## Scale Workers via MachineSet

```bash
# List MachineSets
oc get machineset -n openshift-machine-api

# Scale up
oc scale machineset <machineset-name> -n openshift-machine-api --replicas=5

# Monitor new machine provisioning
oc get machine -n openshift-machine-api -w
oc get nodes -w

# Approve new worker CSRs (if auto-approval not configured)
oc get csr | grep Pending
oc adm certificate approve <csr-name>
# Approve all pending at once:
oc get csr -o name | xargs oc adm certificate approve

# Scale down (deletes nodes gracefully)
oc scale machineset <machineset-name> -n openshift-machine-api --replicas=3
```

## Add New MachineSet

```bash
# Export existing MachineSet as template
oc get machineset <existing-ms> -n openshift-machine-api -o yaml > new-ms.yaml

# Edit: change name, zone/AZ, and any node-specific settings
# Key fields to update:
#   metadata.name
#   spec.selector.matchLabels.machine.openshift.io/cluster-api-machineset
#   spec.template.metadata.labels.machine.openshift.io/cluster-api-machineset
#   spec.template.spec.providerSpec.value.network (if different)

oc apply -f new-ms.yaml
oc get machineset -n openshift-machine-api
```

## Add Infra Node Role

```bash
# 1. Create infra MachineSet (copy from worker MS, add infra label)
# 2. Label existing or new node
oc label node <node> node-role.kubernetes.io/infra=""

# 3. Taint to prevent regular workloads
oc adm taint node <node> node-role.kubernetes.io/infra=reserved:NoSchedule

# 4. Move router (ingress controller) to infra nodes
oc patch ingresscontroller/default -n openshift-ingress-operator \
  --type=merge \
  -p '{"spec":{"nodePlacement":{"nodeSelector":{"matchLabels":{"node-role.kubernetes.io/infra":""}},"tolerations":[{"key":"node-role.kubernetes.io/infra","effect":"NoSchedule"}]}}}'

# 5. Move monitoring
cat <<EOF | oc apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    prometheusOperator:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: node-role.kubernetes.io/infra
        effect: NoSchedule
    prometheusK8s:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: node-role.kubernetes.io/infra
        effect: NoSchedule
EOF
```

## Scale Deployment and Rollout Management

```bash
# Scale a deployment
oc scale deploy/<name> -n <ns> --replicas=3

# Watch rollout progress
oc rollout status deploy/<name> -n <ns>

# Rollout history
oc rollout history deploy/<name> -n <ns>

# Undo last rollout (revert to previous ReplicaSet)
oc rollout undo deploy/<name> -n <ns>

# Undo to a specific revision
oc rollout undo deploy/<name> -n <ns> --to-revision=2

# Pause / resume a rolling update
oc rollout pause deploy/<name> -n <ns>
oc rollout resume deploy/<name> -n <ns>

# Force a restart of all pods in a deployment (e.g. to pick up new secrets)
oc rollout restart deploy/<name> -n <ns>
```

## Emergency etcd Member Recovery

Use when one etcd member has failed but quorum (2 of 3) is still intact.

```bash
# 1. Check etcd pod status
oc get pods -n openshift-etcd

# 2. Identify failed member — exec into a healthy etcd pod
oc rsh -n openshift-etcd etcd-<healthy-master>
etcdctl member list \
  --endpoints=https://localhost:2379 \
  --cacert=/etc/kubernetes/static-pod-resources/etcd-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
  --cert=/etc/kubernetes/static-pod-resources/etcd-certs/secrets/etcd-all-certs/etcd-peer-<node>.crt \
  --key=/etc/kubernetes/static-pod-resources/etcd-certs/secrets/etcd-all-certs/etcd-peer-<node>.key

# 3. Remove the failed member (using the ID from step 2)
etcdctl member remove <member-id> \
  --endpoints=https://localhost:2379 \
  --cacert=... --cert=... --key=...

# 4. Delete the etcd pod on the failed node — MCO will re-add the member
oc delete pod -n openshift-etcd etcd-<failed-node>

# 5. Monitor new pod starting and member re-joining
oc get pods -n openshift-etcd -w

# 6. Confirm three members
oc rsh -n openshift-etcd etcd-<healthy-master> \
  etcdctl member list --endpoints=https://localhost:2379 ...
```

## Certificate Expiry Check

```bash
# Check kube-controller-manager client cert expiry
oc get secret kube-controller-manager-client-cert-key \
  -n openshift-config-managed \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -dates

# Check all API server certs
oc -n openshift-kube-apiserver-operator get secret kube-apiserver-to-kubelet-signer \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate

# Decode a cert from a file
openssl x509 -in cert.pem -noout -dates

# Check pending CSRs (nodes needing cert approval)
oc get csr
oc get csr | grep Pending

# Approve all pending CSRs
oc get csr -o name | xargs oc adm certificate approve

# After cert rotation: verify new expiry
oc -n openshift-kube-apiserver-operator get secret kube-apiserver-to-kubelet-signer \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate
```

## Rotating kubeadmin

Remove the kubeadmin emergency credential after configuring a proper identity provider with at least one cluster-admin user. This is a one-way operation.

```bash
# 1. Confirm you have cluster-admin access via another identity (NOT kubeadmin)
oc login -u <your-idp-admin> -p <password>
oc whoami    # must NOT be kubeadmin

# 2. Verify the IDP-backed user has cluster-admin
oc get clusterrolebinding cluster-admin -o yaml | grep -A5 subjects

# 3. Delete the kubeadmin secret
oc delete secret kubeadmin -n kube-system

# 4. Verify deletion
oc get secret kubeadmin -n kube-system
# Expected: Error from server (NotFound): secrets "kubeadmin" not found
```

## Image Pull Secret Rotation

```bash
# 1. Obtain new pull secret JSON from console.redhat.com (OpenShift cluster manager)

# 2. Update the global pull secret
oc set data secret/pull-secret \
  -n openshift-config \
  --from-file=.dockerconfigjson=<path-to-new-pull-secret.json>

# 3. Verify the update was applied
oc get secret pull-secret -n openshift-config \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq .

# 4. MCO will roll out the change to all nodes (monitor MCP)
oc get mcp -w
```

## Certificate Rotation

```bash
# Check certificate expiry
oc -n openshift-kube-apiserver-operator get secret kube-apiserver-to-kubelet-signer \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate

# Force ingress cert rotation
oc patch secret router-certs-default -n openshift-ingress --type=json \
  -p='[{"op":"remove","path":"/data/tls.crt"}]'

# Rotate etcd peer certs (if expired)
# Use the etcd-cert-recovery procedure from Red Hat KCS
oc get po -n openshift-etcd | grep etcd

# After cert rotation: approve new CSRs
oc get csr | grep Pending
oc adm certificate approve <csr>
```

## Apply MachineConfig (OS Configuration)

```bash
# Example: add custom kernel argument
cat <<EOF | oc apply -f -
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: worker
  name: 99-worker-custom-kernel-arg
spec:
  kernelArguments:
  - hugepagesz=1G
  - hugepages=16
EOF

# Monitor MCO applying the config (nodes will drain+reboot one by one)
oc get mcp   # MachineConfigPool — watch UPDATED / UPDATING / DEGRADED
oc get nodes -w
```

---

## See also

- [OpenShift — Health Checks](../health-checks/)
- [OpenShift — Common Issues](../../troubleshooting/common-issues/)
- [OpenShift — CLI Reference](../cli-reference/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
