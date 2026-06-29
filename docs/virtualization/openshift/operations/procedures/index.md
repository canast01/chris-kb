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


```text title="Expected output"
NAME                                       DESIRED   CURRENT   UPDATED   AVAILABLE   AGE
authentication                             1         1         1         1           45d
baremetal                                  1         1         1         1           45d
cloud-credential                           1         1         1         1           45d
cluster-autoscaler                         1         1         1         1           45d
NAME          STATUS   ROLES           AGE   VERSION
worker-01     Ready    worker          30d   v1.27.8+4fab27b
worker-02     Ready    worker          30d   v1.27.8+4fab27b
master-01     Ready    control-plane   45d   v1.27.8+4fab27b
node "worker-01" cordoned
pod "nginx-deployment-66b6c48dd5-7k2m9" evicted
pod "redis-cache-0" evicted
pod "app-backend-5d8f4c2b1-9xqrs" evicted
Drained node worker-01 successfully
NAME                    READY   STATUS    RESTARTS   AGE       IP            NODE        NOMINATED NODE
(no pods remain on worker-01)
node "worker-01" uncordoned
NAME          STATUS   ROLES    AGE   VERSION
worker-01     Ready    worker   30d   v1.27.8+4fab27b
NAME                    READY   STATUS    RESTARTS   AGE       IP             NODE
nginx-deployment-66b6c48dd5-7k2m9     1/1     Running   0          2m        10.128.2.14    worker-01
redis-cache-0                         1/1     Running   0          1m        10.128.2.15    worker-01
```

!!! warning "Common errors"
    **`error: unable to drain node "worker-01", aborting command [DaemonSet-managed Pods (use --ignore-daemonsets to ignore): openshift-sdn/sdn-xxxxx]`** — Add the `--ignore-daemonsets` flag to the drain command to skip DaemonSet pods.
    **`error: cannot delete Pods with local storage (use --delete-emptydir-data to override): [namespace/pod-name]`** — Add the `--delete-emptydir-data` flag to allow eviction of pods using emptyDir volumes.
    **`error: timed out waiting for pod "app-xyz" to be evicted`** — Increase the `--timeout` value (e.g., `--timeout=600s`) or manually delete the problematic pod with `oc delete pod <pod-name> -n <namespace> --grace-period=0 --force`.
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


```text title="Expected output"
NAME                                    DESIRED   CURRENT   READY   UPDATED   AVAILABLE   AGE
worker-us-east-1a                       3         3         3       3         3           45d
worker-us-east-1b                       3         3         3       3         3           45d
worker-us-east-1c                       2         2         2       2         2           45d

machineset.machine.openshift.io/worker-us-east-1a scaled

NAME                                    STATE         TYPE   AGE
worker-us-east-1a-abcd1                 Provisioning  node   12s
worker-us-east-1a-efgh2                 Running       node   45s
worker-us-east-1b-ijkl3                 Provisioned   node   8s

NAME                STATUS   ROLES    AGE   VERSION
worker-1.example   Ready    worker   2m    v1.27.3
worker-2.example   Ready    worker   45d   v1.27.3
worker-3.example   NotReady worker   1m    v1.27.3

system:serviceaccount:openshift-machine-config-operator:default   Pending   1h
system:node:worker-us-east-1a-abcd1                                Pending   45s
system:node:worker-us-east-1a-efgh2                                Pending   30s

certificatesigningrequest.certificates.k8s.io/system:node:worker-us-east-1a-abcd1 approved
certificatesigningrequest.certificates.k8s.io/system:node:worker-us-east-1a-efgh2 approved
certificatesigningrequest.certificates.k8s.io/system:serviceaccount:openshift-machine-config-operator:default approved

machineset.machine.openshift.io/worker-us-east-1a scaled
```

!!! warning "Common errors"
    **`Error from server (NotFound): machinesets.machine.openshift.io "<machineset-name>" not found`** — Replace `<machineset-name>` with an actual MachineSet name from the `oc get machineset` output.
    **`error: no objects passed to approve`** — Ensure pending CSRs exist before running the approve command; check with `oc get csr | grep Pending` first.
    **`Error: unable to drain node "worker-1.example": cannot delete Pods not managed by ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet`** — Add `--ignore-daemonsets --delete-emptydir-data` flags to the drain command if scaling down encounters pod eviction issues.
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


```text title="Expected output"
apiVersion: machine.openshift.io/v1beta1
kind: MachineSet
metadata:
  name: worker-us-east-1a
  namespace: openshift-machine-api
  labels:
    machine.openshift.io/cluster-api-cluster: ocp-prod-4x2k9
spec:
  replicas: 3
  selector:
    matchLabels:
      machine.openshift.io/cluster-api-machineset: worker-us-east-1a
  template:
    metadata:
      labels:
        machine.openshift.io/cluster-api-machineset: worker-us-east-1a
    spec:
      providerSpec:
        value:
          network:
            subnets:
            - id: subnet-0a7f2c8d9e1b4f5a2
machinesets.machine.openshift.io/worker-us-east-1a created
NAME                    DESIRED   CURRENT   READY   AVAILABLE   AGE
worker-us-east-1a       3         3         2       2           45s
worker-us-east-1b       3         3         3       3           8d
worker-us-east-1c       3         3         3       3           8d
```

!!! warning "Common errors"
    **`error: failed to create new MachineSet: machinesets.machine.openshift.io "worker-us-east-1a" already exists`** — Change the metadata.name field in new-ms.yaml to a unique value that doesn't already exist in the cluster.
    **`error validating data: data[spec.selector.matchLabels.machine.openshift.io/cluster-api-machineset]: Invalid value: "worker-us-east-1a": does not match spec.template.metadata.labels`** — Ensure the selector matchLabels and template metadata labels both reference the same MachineSet name.
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


```text title="Expected output"
node/worker-2.infra.example.com labeled
node/worker-2.infra.example.com tainted
ingresscontroller.operator.openshift.io/default patched
configmap/cluster-monitoring-config created
```

!!! warning "Common errors"
    **`error: taint "node-role.kubernetes.io/infra=reserved:NoSchedule" must have one of the following effects: NoSchedule, PreferNoSchedule, NoExecute`** — Change the taint effect to `NoSchedule` (remove `reserved:` prefix, as it is not a valid taint key component).
    **`Error from server (NotFound): ingresscontrollers.operator.openshift.io "default" not found`** — Verify the IngressController exists with `oc get ingresscontroller -n openshift-ingress-operator` and use the correct name.
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


```text title="Expected output"
deployment.apps/api-service scaled
Waiting for deployment spec update to be observed...
Waiting for deployment "api-service" rollout to finish: 1 out of 3 new replicas have updated...
Waiting for deployment "api-service" rollout to finish: 2 out of 3 new replicas have updated...
Waiting for deployment "api-service" rollout to finish: 3 out of 3 new replicas have updated...
Waiting for deployment "api-service" rollout to finish: 1 old replicas are pending termination...
deployment "api-service" successfully rolled out
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
deployment.apps/api-service rolled back to revision 2
deployment.apps/api-service rolled back to revision 2
deployment.apps/api-service paused
deployment.apps/api-service resumed
deployment.apps/api-service restarted
```

!!! warning "Common errors"
    **`Error from server (NotFound): deployments.apps "<name>" not found`** — Verify the deployment name is correct and exists in the specified namespace with `oc get deploy -n <ns>`.
    **`error: the server doesn't have a resource type "deploy"`** — Use the full resource name `deployment` instead of the alias `deploy`, or ensure your OpenShift CLI version supports the shorthand.
    **`Error from server (Forbidden): deployments.apps "<name>" is forbidden: User "<user>" cannot patch resource "deployments" in API group "apps"`** — Ensure your user has sufficient RBAC permissions to modify deployments in the target namespace.
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


```text title="Expected output"
NAME                                READY   STATUS    RESTARTS   AGE
etcd-master-0                       1/1     Running   0          45d
etcd-master-1                       1/1     Running   0          45d
etcd-master-2                       1/1     Running   2          12h

member 3a26a27c936d0971: name=master-2 peerURLs=https://10.0.1.45:2380 clientURLs=https://10.0.1.45:2379 isLeader=false
member 5b8c1d9e2f4a7c63: name=master-0 peerURLs=https://10.0.1.32:2380 clientURLs=https://10.0.1.32:2379 isLeader=true
member 7d4f9a1b5e2c8d34: name=master-1 peerURLs=https://10.0.1.38:2380 clientURLs=https://10.0.1.38:2379 isLeader=false

Member 3a26a27c936d0971 removed

pod "etcd-master-2" deleted

NAME                                READY   STATUS    RESTARTS   AGE
etcd-master-0                       1/1     Running   0          45d
etcd-master-1                       1/1     Running   0          45d
etcd-master-2                       0/1     Pending   0          2s
etcd-master-2                       0/1     ContainerCreating   0          3s
etcd-master-2                       1/1     Running             0          18s

member 5b8c1d9e2f4a7c63: name=master-0 peerURLs=https://10.0.1.32:2380 clientURLs=https://10.0.1.32:2379 isLeader=true
member 7d4f9a1b5e2c8d34: name=master-1 peerURLs=https://10.0.1.38:2380 clientURLs=https://10.0.1.38:2379 isLeader=false
member 9c2e7f3a1d5b4c89: name=master-2 peerURLs=https://10.0.1.45:2380 clientURLs=https://10.0.1.45:2379 isLeader=false
```

!!! warning "Common errors"
    **`Error: context deadline exceeded`** — Increase the timeout with `--command-timeout=30s` flag or verify etcd pod is fully running before executing etcdctl commands.
    **`Error: certificate signed by unknown authority`** — Verify the cacert path is correct and matches the current etcd CA; check `/etc/kubernetes/static-pod-resources/etcd-certs/configmaps/etcd-serving-ca/` exists in the pod.
    **`Error: etcdctl: command not found`** — The etcdctl binary is located at `/usr/bin/etcdctl` in the etcd pod; use the full path or check the pod image version supports the command.
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


```text title="Expected output"
notBefore=Jan 15 08:23:45 2024 GMT
notAfter=Jan 14 08:23:45 2025 GMT
enddate=Jan 14 08:23:45 2025 GMT
notBefore=Feb  1 12:00:00 2024 GMT
notAfter=Feb  1 12:00:00 2025 GMT
enddate=Feb  1 12:00:00 2025 GMT
NAME                                                   AGE     SIGNERNAME                                    REQUESTOR                                        REQUESTEDDURATION   CONDITION
node-csr-abc123def456ghi789jkl012mno345pqr678stu   2m      kubernetes.io/kube-apiserver-client-kubelet   system:serviceaccount:openshift-machine-config-operator:default   <none>              Pending
node-csr-xyz987wvu654tsr321qpo098nml765kji432hgf   1m      kubernetes.io/kube-apiserver-client-kubelet   system:serviceaccount:openshift-machine-config-operator:default   <none>              Pending
certificatesigningrequest.certificates.k8s.io/node-csr-abc123def456ghi789jkl012mno345pqr678stu approved
certificatesigningrequest.certificates.k8s.io/node-csr-xyz987wvu654tsr321qpo098nml765kji432hgf approved
enddate=Jan 14 08:23:45 2026 GMT
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "secret" in API group ""`** — Verify the secret exists in the correct namespace with `oc get secrets -n openshift-config-managed | grep kube-controller-manager`.
    **`unable to load certificate`** — Ensure the base64-decoded output is valid by checking the secret data field contains a properly formatted PEM certificate.
    **`No resources found`** — Run `oc get csr` first to confirm pending CSRs exist before attempting approval with xargs.
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


```text title="Expected output"
Authentication successful

idp-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: idp-admin
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: cluster-admins
secret "kubeadmin" deleted
Error from server (NotFound): secrets "kubeadmin" not found
```

!!! warning "Common errors"
    **`error: unable to read client-cert /home/user/.kube/config from disk`** — Ensure your kubeconfig file exists and is readable with `ls -la ~/.kube/config`.
    **`Error from server (Forbidden): clusterrolebindings.rbac.authorization.k8s.io "cluster-admin" is forbidden: User "idp-admin" cannot get resource "clusterrolebindings"`** — Verify the IDP user has cluster-admin role assigned before attempting deletion by checking `oc describe clusterrolebinding cluster-admin`.
    **`Error from server (Forbidden): secrets is forbidden: User "kubeadmin" cannot delete resource "secrets" in API group "" in the namespace "kube-system"`** — Log in with your IDP admin account instead of kubeadmin; kubeadmin cannot delete itself.
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


```text title="Expected output"
secret/pull-secret data updated
{
  "auths": {
    "cloud.openshift.com": {
      "auth": "b3BlbnNoaWZ0K2NsdXN0ZXI6MjRkMzU2ZjctNWE5Yi00YzAxLWI4ZjItOWU3YzNhYmM0ZDU2",
      "email": "user@example.com"
    },
    "quay.io": {
      "auth": "cXVheS1jbHVzdGVyOmV5SmhiR2NpT2lKSVV6STFOaUo5LkV5SmtiV1Z1SWpwMGNuVmxMQ0psZW1GdGNHeGxJanBiSW1SdmJTSXNJbU55ZGlJNklrRkJRVTVCVFVsUFUwVlNJaXdpWlhobGNtRm5aU0k2SWtGQlFVNUJUVWxQVTBWU0lsMC5zVzFoWjI5dVoyOXZaMnhMYjI1SFlXZGxiV1Z1ZEhNdVkyOXQ=",
      "email": "user@example.com"
    }
  }
}
NAME                                       READY   UPDATED   DEGRADED   UNAVAILABLE
master                                     3       3         0          0
worker                                     5       5         0          0
worker-gpu                                 2       1         0          1
```

!!! warning "Common errors"
    **`error: no objects matched "pull-secret"`** — Verify the secret exists in openshift-config namespace with `oc get secrets -n openshift-config | grep pull-secret`.
    **`command not found: jq`** — Install jq on the bastion host with `sudo yum install -y jq` or use `python3 -m json.tool` instead.
    **`base64: invalid input`** — Ensure the pull-secret file path is correct and the secret data is not corrupted; re-download from console.redhat.com.
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


```text title="Expected output"
notBefore=Jan 15 09:23:45 2024 GMT
notAfter=Jan 14 09:23:45 2025 GMT
secret/router-certs-default patched
NAME                                                    READY   STATUS    RESTARTS   AGE
etcd-ip-10-0-145-87.us-east-2.compute.internal         3/3     Running   0          45d
etcd-ip-10-0-156-203.us-east-2.compute.internal        3/3     Running   0          45d
etcd-ip-10-0-167-41.us-east-2.compute.internal         3/3     Running   0          45d
NAME                                      AGE   SIGNERNAME                                    REQUESTOR                                                         CONDITION
csr-8k4m2                                  2m    kubernetes.io/kube-apiserver-client-kubelet   system:serviceaccount:openshift-machine-config-operator:default   Pending
csr-9p7x1                                  1m    kubernetes.io/kubelet-serving                  system:node:worker-1.us-east-2.compute.internal                  Pending
certificatesigningrequest.certificates.k8s.io/csr-8k4m2 approved
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "secret" in group "core" in the namespace "openshift-kube-apiserver-operator"`** — Verify the secret name matches your cluster version with `oc get secret -n openshift-kube-apiserver-operator | grep signer`.
    **`error: unable to decode base64`** — Ensure the certificate data exists in the secret; if the secret was recently deleted, restore it from etcd backup or re-run the cert rotation procedure.
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


```text title="Expected output"
machineconfig.machineconfiguration.openshift.io/99-worker-custom-kernel-arg created
NAME                                    CONFIG                                   UPDATED   UPDATING   DEGRADED   NODES
master                                  rendered-master-b4c8a2f1e9d7c3k2       True      False      False      3
worker                                  rendered-worker-a7f2e1d9c4b8k5m3       False     True       False      2
NAME                                    STATUS                   ROLES           AGE       VERSION
worker-node-01.ocp.example.com         NotReady,SchedulingDisabled   worker          45d       v1.27.6
worker-node-02.ocp.example.com         Ready                    worker          45d       v1.27.6
worker-node-03.ocp.example.com         Ready                    worker          45d       v1.27.6
master-node-01.ocp.example.com         Ready                    control-plane   45d       v1.27.6
master-node-02.ocp.example.com         Ready                    control-plane   45d       v1.27.6
master-node-03.ocp.example.com         Ready                    control-plane   45d       v1.27.6
```

!!! warning "Common errors"
    **`error: unable to recognize "STDIN": no matches for kind "MachineConfig" in version "machineconfiguration.openshift.io/v1"`** — Verify the Machine Config Operator is installed with `oc get operator machine-config` and check your OpenShift version supports this API.
    **`Error from server (BadRequest): error when creating "STDIN": MachineConfig.machineconfiguration.openshift.io "99-worker-custom-kernel-arg" is invalid: spec.kernelArguments: Invalid value: "hugepagesz=1G": kernel argument format must be key=value`** — Use proper kernel argument syntax; some arguments like hugepagesz require specific formatting or may need to be set via GRUB instead.
    **`The MachineConfigPool "worker" is degraded`** — Check node status with `oc describe node <node-name>` and MCO logs with `oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-operator -f` to identify why the config failed to apply.
---

## See also

- [OpenShift — Health Checks](../health-checks/)
- [OpenShift — Common Issues](../../troubleshooting/common-issues/)
- [OpenShift — CLI Reference](../cli-reference/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
