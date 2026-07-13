---
tags:
  - operations
  - tanzu
  - vmware
description: "TKG and Tanzu operations — namespace and workload cluster lifecycle, RBAC, Harbor project configuration, Helm deployments, Ingress setup, node scaling..."
---
# Tanzu — Procedures

<div class="kb-summary">
TKG and Tanzu operations — namespace and workload cluster lifecycle, RBAC, Harbor project configuration, Helm deployments, Ingress setup, node scaling, cluster upgrade, Velero backup/restore, and persistent storage via vSAN CNS.

*Applies to: Tanzu 3.x*
</div>

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Create a vSphere Namespace

```yaml
vCenter → Workload Management → Namespaces → Create Namespace
  Cluster: select Supervisor cluster
  Name: team-alpha
  Description: Application namespace for Team Alpha

OR via kubectl:
```

```bash
kubectl vsphere login --server https://supervisor.example.local \
  --username administrator@vsphere.local --insecure-skip-tls-verify

# Create namespace (vSphere Namespace via YAML on Supervisor)
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: team-alpha
EOF
```


```text title="Expected output"
Logged in successfully to https://supervisor.example.local as administrator@vsphere.local
Current context: supervisor.example.local

namespace/team-alpha created
```

!!! warning "Common errors"
    **`error: Unable to connect to the server: dial tcp: lookup supervisor.example.local: no such host`** — Verify the Supervisor Cluster hostname/IP is correct and resolvable from your network, or add it to `/etc/hosts`.
    **`error: You must be logged in to the server (Unauthorized)`** — Confirm the vSphere credentials are correct and the user has appropriate permissions on the Supervisor Cluster.
    **`error: namespaces "team-alpha" is forbidden: User "administrator@vsphere.local" cannot create resource "namespaces"`** — Grant the user the required vSphere role (e.g., Namespace Creator) on the Supervisor Cluster via vCenter.
Configure namespace in vCenter UI:
- Storage: assign storage policy
- VM Class: assign allowed VM classes for TKG clusters
- Resource Limits: CPU, memory, storage quotas

---

## Deploy a TKG Workload Cluster in a Namespace

```bash
# Switch to Supervisor namespace context
kubectl config use-context team-alpha

# Apply TanzuKubernetesCluster manifest
kubectl apply -f - <<EOF
apiVersion: run.tanzu.vmware.com/v1alpha3
kind: TanzuKubernetesCluster
metadata:
  name: team-alpha-cluster
  namespace: team-alpha
spec:
  topology:
    controlPlane:
      replicas: 3
      vmClass: best-effort-medium
      storageClass: vsan-default
    nodePools:
    - name: worker-pool
      replicas: 3
      vmClass: best-effort-large
      storageClass: vsan-default
  distribution:
    version: v1.26.5
EOF

# Watch cluster provisioning
kubectl get tanzukubernetescluster -n team-alpha -w
```


```text title="Expected output"
Switched to context "team-alpha".
tanzukubernetescluster.run.tanzu.vmware.com/team-alpha-cluster created
NAME                   STATUS   READY   REPLICAS   UPDATED   UNAVAILABLE   AGE
team-alpha-cluster     Pending  0/3     0          0         3             0s
team-alpha-cluster     Pending  0/3     0          0         3             5s
team-alpha-cluster     Provisioning  1/3     1          1         2             15s
team-alpha-cluster     Provisioning  2/3     2          2         1             45s
team-alpha-cluster     Running  3/3     3          3         0             2m18s
```

!!! warning "Common errors"
    **`error: context "team-alpha" does not exist`** — Verify the context name with `kubectl config get-contexts` and ensure the Supervisor cluster is configured.
    **`error: resource mapping not found for name: "team-alpha-cluster" namespace: "team-alpha" with kind TanzuKubernetesCluster`** — Confirm Tanzu Kubernetes Grid is installed on the Supervisor cluster and the CRD is available via `kubectl get crd | grep tanzukubernetescluster`.
    **`error: namespaces "team-alpha" not found`** — Create the namespace first with `kubectl create namespace team-alpha` before applying the TanzuKubernetesCluster manifest.
---

## Grant Namespace Access to a Team

```bash
# Get kubeconfig for the workload cluster
kubectl vsphere login --server https://supervisor.example.local \
  --username administrator@vsphere.local \
  --tanzu-kubernetes-cluster-name team-alpha-cluster \
  --tanzu-kubernetes-cluster-namespace team-alpha

# Switch to workload cluster context
kubectl config use-context team-alpha-cluster

# Create RBAC for team
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-alpha-developers
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: edit
subjects:
- kind: Group
  name: team-alpha-devs  # OIDC group from Pinniped
  apiGroup: rbac.authorization.k8s.io
EOF
```


```text title="Expected output"
Logged in successfully to supervisor.example.local as administrator@vsphere.local
Switched to context "team-alpha-cluster".
rolebinding.rbac.authorization.k8s.io/team-alpha-developers created
```

!!! warning "Common errors"
    **`error: Unable to connect to the supervisor cluster at https://supervisor.example.local`** — Verify the supervisor endpoint is reachable and the hostname resolves correctly with `nslookup supervisor.example.local`.
    **`error: invalid credentials provided`** — Confirm the vSphere credentials are correct and the user has permission to access the Tanzu Kubernetes cluster in that namespace.
    **`error: the server doesn't have a resource type "tanzukubernetesclusters"`** — Ensure the Tanzu Kubernetes Grid extension is installed on the vSphere Supervisor Cluster and the workload cluster exists in the specified namespace.
---

## Configure Harbor Project with Vulnerability Scanning

```bash
# Create project via Harbor API
curl -sk -X POST "https://harbor.example.local/api/v2.0/projects" \
  -u admin:<password> \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "team-alpha",
    "public": false,
    "metadata": {
      "auto_scan": "true",
      "prevent_vul": "true",
      "severity": "high"
    }
  }'

# Create user membership in project
curl -sk -X POST "https://harbor.example.local/api/v2.0/projects/team-alpha/members" \
  -u admin:<password> \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2,
    "member_group": {"group_name": "team-alpha-devs", "group_type": 1}
  }'
```


```text title="Expected output"
{"project_id":123,"project_name":"team-alpha","public":false,"creation_time":"2024-01-15T09:42:33.456Z","update_time":"2024-01-15T09:42:33.456Z","current_user_role_id":1,"current_user_role_name":"projectAdmin","repo_count":0,"metadata":{"auto_scan":"true","prevent_vul":"true","severity":"high"}}
{"id":456,"project_id":123,"entity_name":"team-alpha-devs","entity_type":"group","role_id":2,"access_level":"developer","creation_time":"2024-01-15T09:42:45.123Z","update_time":"2024-01-15T09:42:45.123Z"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification, or import the Harbor CA certificate into your system trust store.
    **`{"errors":[{"code":"CONFLICT","message":"project team-alpha already exists"}]}`** — The project name already exists in Harbor; use a different project name or delete the existing project first.
    **`{"errors":[{"code":"UNAUTHORIZED","message":"user does not have permission to the project"}]}`** — Ensure the admin user credentials are correct and the user has project admin role permissions.
---

## Configure Pull-Through Cache in Harbor

```yaml
Harbor UI → Administration → Registries → New Endpoint
  Provider: Docker Hub
  Name: docker-hub-proxy
  URL: https://hub.docker.com
  Verify SSL: Yes

Projects → New Project
  Name: dockerhub-cache
  Access Level: Public (or Private if restricting)
  Enable: Pull-through cache → Docker Hub endpoint
```

Configure nodes to pull from Harbor instead of Docker Hub directly by setting imagePullPolicy and image names to use `harbor.example.local/dockerhub-cache/` prefix.

---

## Deploy Application via Helm

```bash
kubectl config use-context team-alpha-cluster

# Add Helm repo
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Deploy with values override
helm install my-postgres bitnami/postgresql \
  --namespace production \
  --create-namespace \
  --set auth.postgresPassword=<password> \
  --set primary.persistence.storageClass=vsan-default \
  --set primary.persistence.size=50Gi

# Verify
helm list -n production
kubectl get pods -n production
```


```text title="Expected output"
Switched to context "team-alpha-cluster".
"bitnami" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈ Happy Helming!
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
my-postgres     production      1               2024-01-15 14:32:18.456789012 +0000 UTC deployed       postgresql-13.2.24      15.6
NAME                                    READY   STATUS    RESTARTS   AGE
my-postgres-0                            1/1     Running   0          2m14s
my-postgres-read-0                       1/1     Running   0          2m8s
```

!!! warning "Common errors"
    **`Error: release name "my-postgres" already exists`** — Use `helm upgrade` instead of `helm install`, or delete the existing release with `helm uninstall my-postgres -n production` first.
    **`Error: namespace "production" not found`** — Remove the `--create-namespace` flag if the namespace must be pre-created, or ensure your RBAC permissions allow namespace creation.
    **`Error: failed to create resource: storageclass.storage.k8s.io "vsan-default" not found`** — Verify the storage class exists with `kubectl get storageclass` and update the `--set primary.persistence.storageClass` value accordingly.
---

## Configure Ingress (Contour / HTTPProxy)

```bash
# Create HTTPProxy for an application
kubectl apply -f - <<EOF
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: myapp
  namespace: production
spec:
  virtualhost:
    fqdn: myapp.example.local
    tls:
      secretName: myapp-tls  # cert-manager managed TLS secret
  routes:
  - services:
    - name: myapp-svc
      port: 80
EOF
```


```text title="Expected output"
httpproxy.projectcontour.io/myapp created
```

!!! warning "Common errors"
    **`error: resource mapping not found for kind "HTTPProxy"... ensure CRDs are installed first`** — Install Contour CRDs with `kubectl apply -f https://projectcontour.io/quickstart/contour.yaml` or verify the projectcontour.io API group is registered via `kubectl api-resources | grep httpproxy`.
    **`The HTTPProxy "myapp" is invalid: spec.virtualhost.tls.secretName: Invalid value: "myapp-tls": secret not found`** — Create the TLS secret in the production namespace using `kubectl create secret tls myapp-tls --cert=cert.pem --key=key.pem -n production` or verify cert-manager has issued the certificate.
    **`error: unable to recognize stdin: no matches for kind "HTTPProxy" in version "projectcontour.io/v1"`** — Confirm Contour is installed in the cluster with `kubectl get deployment -n projectcontour` and that the API version matches your Contour version via `kubectl api-versions | grep projectcontour`.
---

## Scale Worker Nodes

```bash
# For vSphere with Tanzu (TanzuKubernetesCluster):
kubectl edit tanzukubernetescluster team-alpha-cluster -n team-alpha
# Change: spec.topology.nodePools[0].replicas: 5 → 7

# For standalone TKG:
tanzu cluster scale team-alpha-cluster --worker-machine-count 7
```


```text title="Expected output"
# kubectl edit tanzukubernetescluster team-alpha-cluster -n team-alpha
tanzukubernetescluster.run.tanzu.vmware.com/team-alpha-cluster edited

# tanzu cluster scale team-alpha-cluster --worker-machine-count 7
Scaling cluster 'team-alpha-cluster' to 7 worker nodes...
Validating configuration...
Updating cluster spec...
Cluster scaling initiated. Current worker count: 5 → Target: 7
Monitor progress with: tanzu cluster get team-alpha-cluster
```

!!! warning "Common errors"
    **`error: tanzukubernetescluster.run.tanzu.vmware.com "team-alpha-cluster" not found`** — Verify the cluster name and namespace with `kubectl get tanzukubernetescluster -A`.
    **`Error: cluster 'team-alpha-cluster' not found in current management cluster context`** — Ensure you are logged into the correct management cluster context with `tanzu context list` and `tanzu context use <context-name>`.
---

## Rotate Cluster Kubeconfig

```bash
# Get fresh kubeconfig for a TKG cluster
tanzu cluster kubeconfig get my-cluster --admin

# Or for Supervisor-managed cluster:
kubectl vsphere login --server https://supervisor.example.local \
  --username user@corp.local \
  --tanzu-kubernetes-cluster-name my-cluster \
  --tanzu-kubernetes-cluster-namespace my-namespace
```


```text title="Expected output"
Credentials of workload cluster 'my-cluster' have been saved
You can now access the cluster by running 'kubectl cluster-info'

Logged in successfully.
You have access to the following contexts:
   supervisor.example.local
   my-cluster

The current context is now "my-cluster".

To view your current context, run: kubectl config current-context
```

!!! warning "Common errors"
    **`Error: cluster 'my-cluster' not found`** — Verify the cluster name matches output from `tanzu cluster list` and you have permissions to access it.
    **`Error: invalid credentials provided`** — Ensure your vSphere SSO credentials are correct and your user account has cluster admin role assigned in the Supervisor namespace.
    **`Unable to connect to supervisor.example.local`** — Confirm the Supervisor hostname/IP is correct, network connectivity exists, and the Supervisor cluster API is accessible on port 443.
Kubeconfigs embed a token with a limited TTL — users need to re-login after expiry.

## Upgrade a TKG Workload Cluster

Upgrading a TKG cluster updates the Kubernetes version on control plane and worker nodes.

```bash
# 1. List available Kubernetes versions in the Supervisor
kubectl get tanzukubernetesrelease

# 2. Check current cluster version
kubectl get tkc my-cluster -n my-namespace -o jsonpath='{.spec.distribution.version}'

# 3. Edit the TKC to the new version
kubectl edit tkc my-cluster -n my-namespace
# Change: spec.distribution.version: v1.27.x+vmware.y-tkg.z

# 4. Monitor the upgrade — control plane upgrades first, then workers
kubectl get tkc my-cluster -n my-namespace -w
# Phase progresses: updating → running

# 5. Verify all nodes are upgraded and Ready
kubectl --kubeconfig <cluster-kubeconfig> get nodes -o wide
# All nodes should show the new Kubernetes version

# 6. Verify system workloads are healthy
kubectl --kubeconfig <cluster-kubeconfig> get pods -n kube-system
kubectl --kubeconfig <cluster-kubeconfig> get pods -n vmware-system-csi
```


```text title="Expected output"
NAME                                           VERSION
v1.27.11+vmware.1-tkg.1                        True
v1.27.10+vmware.2-tkg.2                        True
v1.26.13+vmware.3-tkg.1                        True

v1.27.10+vmware.2-tkg.2

NAME       READY   UP-TO-DATE   UPDATED   UNAVAILABLE   PROGRESSING   AGE
my-cluster 3/3     3            3         0              0             45d

NAME                                STATUS   ROLES           AGE    VERSION
tkc-control-plane-7xk9m             Ready    control-plane   45d    v1.27.11+vmware.1-tkg.1
tkc-worker-pool-1-5d4c2-8xjqp       Ready    <none>          45d    v1.27.11+vmware.1-tkg.1
tkc-worker-pool-1-5d4c2-m2kpx       Ready    <none>          45d    v1.27.11+vmware.1-tkg.1
tkc-worker-pool-1-5d4c2-q7nlr       Ready    <none>          45d    v1.27.11+vmware.1-tkg.1

NAMESPACE           NAME                                      READY   STATUS    RESTARTS   AGE
kube-system         coredns-558bd4d5db-2xk8l                  1/1     Running   0          8m
kube-system         etcd-tkc-control-plane-7xk9m              1/1     Running   0          7m
kube-system         kube-apiserver-tkc-control-plane-7xk9m    1/1     Running   0          6m
kube-system         kube-controller-manager-tkc-cp-7xk9m      1/1     Running   0          5m
vmware-system-csi   vsphere-csi-controller-0                  7/7     Running   0          4m
vmware-system-csi   vsphere-csi-node-5d4c2                    3/3     Running   0          3m
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "tanzukubernetesrelease"`** — Verify the Supervisor cluster is properly initialized and the Tanzu Kubernetes Grid extension is installed with `kubectl get crd | grep tanzukubernetesrelease`.
    **`error: the server doesn't have a resource type "tkc"`** — Ensure you are connected to the Supervisor cluster (not a workload cluster) and the TKC CRD is available with `kubectl api-resources | grep tanzukubernetescluster`.
    **`error: timed out waiting for the condition`** — Check node resource availability and vSphere storage capacity; monitor upgrade progress with `kubectl describe tkc my-cluster -n my-namespace` to identify stuck phases.
!!! warning "Do not skip Kubernetes minor versions"
    TKG upgrade validation enforces sequential minor version upgrades. Skipping a version (e.g., 1.26 → 1.28) is unsupported and will leave the cluster in a broken state that requires VMware GSS to recover. If you are multiple versions behind, plan multiple sequential upgrade windows.

One minor version at a time — do not skip versions (e.g., 1.26 → 1.27, not 1.26 → 1.28).

## Delete a TKG Workload Cluster

!!! danger "Irreversible — all cluster VMs and workloads are permanently destroyed"
    Deleting the TanzuKubernetesCluster object triggers the Supervisor to remove all control plane and worker VMs from vCenter inventory. Any workloads still running in the cluster will be terminated. Any PVCs bound to CNS volumes will be deleted. If PVs were created with `reclaimPolicy: Delete`, the underlying vSAN volumes are also deleted. Confirm all workloads are migrated and all data is backed up before proceeding.

```bash
# 1. Drain workloads off the cluster first — notify application teams
# 2. Delete the TanzuKubernetesCluster object
kubectl delete tkc my-cluster -n my-namespace

# 3. Monitor deletion — Supervisor removes VMs from vCenter
kubectl get tkc -n my-namespace -w
# Cluster moves to Deleting phase; VMs removed from vCenter inventory

# 4. Confirm namespace storage claims are released
kubectl get pvc -n my-namespace
# All PVCs should be gone; verify no orphaned volumes in vSAN

# 5. Clean up namespace if no longer needed
kubectl delete namespace my-namespace
```


```text title="Expected output"
tkc.run.tanzu.vmware.com "my-cluster" deleted
NAME         PHASE      READY   TKR                    AGE
my-cluster   Deleting   False   v1.24.9---vmware.1-tkg.1   12m
my-cluster   Deleting   False   v1.24.9---vmware.1-tkg.1   12m
my-cluster   Deleting   False   v1.24.9---vmware.1-tkg.1   13m
(watch terminated after cluster removed from output)
No resources found in my-namespace namespace.
namespace "my-namespace" deleted
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "tkc"`** — Verify the Tanzu Kubernetes Grid extension is installed on the Supervisor cluster with `kubectl get crds | grep tanzu`.
    **`Error from server (Conflict): Operation cannot be fulfilled on namespace "my-namespace": namespace has a finalizer [kubernetes]`** — Wait for all workloads and PVCs to fully drain before deleting the namespace, or manually remove the finalizer with `kubectl patch namespace my-namespace -p '{"metadata":{"finalizers":null}}'`.
Deletion is irreversible — confirm data backup and workload migration before deleting.

## Configure Resource Quotas on a Namespace

vSphere Namespaces support CPU, memory, and storage quotas enforced by the Supervisor.

```bash
# Set resource quotas via kubectl (requires Supervisor admin)
kubectl edit namespace my-namespace
# Or apply a patch:
kubectl patch namespace my-namespace --type merge -p '{
  "spec": {
    "resourceQuotas": [
      {
        "requests": {"memory": "64Gi", "cpu": "16"},
        "limits": {"memory": "128Gi", "cpu": "32"}
      }
    ],
    "storagePolicies": [
      {"policy": "vSAN Default Storage Policy", "limit": "2Ti"}
    ]
  }
}'

# View current quota usage
kubectl describe namespace my-namespace
# ResourceQuotaStatus shows used vs hard limits

# Grant namespace-scoped storage quota override (vSphere UI)
# Workload Management → Namespaces → [namespace] → Storage → Edit Limits
```


```text title="Expected output"
namespace/my-namespace patched
NAME            STATUS   AGE
my-namespace    Active   45d

Name:         my-namespace
Labels:       <none>
Annotations:  <none>
Status:       Active

ResourceQuotas:
  Name:                   my-namespace-quota
  Resource                Requests          Limits
  --------                --------          ------
  memory                  32Gi/64Gi         96Gi/128Gi
  cpu                     8/16              24/32

StoragePolicies:
  Name:                   vSAN Default Storage Policy
  Used                    1.2Ti/2Ti
  Status:                 Active
```

!!! warning "Common errors"
    **`error: unable to recognize "": no matches for kind "ResourceQuota" in version "v1"`** — Ensure you're patching the namespace object directly with `spec.resourceQuotas` syntax supported by your Tanzu version; verify with `kubectl api-resources | grep quota`.
    **`Error from server (Forbidden): namespaces "my-namespace" is forbidden: User "user@example.com" does not have permission to patch namespaces`** — Request Supervisor cluster admin privileges or have an admin apply the patch on your behalf.
    **`error: the server doesn't have a resource type "storagePolicies"`** — Storage policy limits are managed through the vSphere UI under Workload Management → Namespaces, not via kubectl patch; remove the `storagePolicies` section from the patch command.
## Backup and Restore a TKG Cluster with Velero

Velero backs up Kubernetes resources and persistent volumes to object storage.

```bash
# 1. Install Velero with vSphere plugin (run once per cluster)
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0,vspheresaas/velero-plugin-for-vsphere:v1.5.0 \
  --bucket velero-backups \
  --secret-file ./credentials-velero \
  --backup-location-config region=minio,s3ForcePathStyle=true,s3Url=http://minio.example.local:9000 \
  --use-volume-snapshots=true \
  --features=EnableCSIVolumeSnapshots

# 2. Create a backup
velero backup create my-cluster-backup \
  --include-namespaces app-namespace \
  --wait

# 3. Verify backup status
velero backup describe my-cluster-backup
velero backup logs my-cluster-backup

# 4. Restore to same or new cluster
velero restore create --from-backup my-cluster-backup \
  --include-namespaces app-namespace \
  --wait

# 5. Verify restore
velero restore describe <restore-name>
kubectl get pods -n app-namespace
kubectl get pvc -n app-namespace
```


```text title="Expected output"
Velero is installed and ready to be tested. See https://velero.io/docs/quickstart for next steps.
NAME                                    READY   STATUS    RESTARTS   AGE
velero                                  1/1     Running   0          45s
node-agent-abc12                        1/1     Running   0          42s
node-agent-def45                        1/1     Running   0          41s

Backup request "my-cluster-backup" submitted successfully.
Waiting for backup to complete...
Backup completed with status: Completed

Name:         my-cluster-backup
Namespace:    velero
Status:       Completed
Started:      2024-01-15 14:32:10 +0000 UTC
Completed:    2024-01-15 14:35:22 +0000 UTC
Expiration:   2024-02-14 14:32:10 +0000 UTC
Total items backed up:  47
Items backed up:  47
Velero version:  v1.12.0

Restore request "my-cluster-backup-20240115143532" submitted successfully.
Waiting for restore to complete...
Restore completed with status: Completed

NAME                                    READY   STATUS    RESTARTS   AGE
app-deployment-5d8f9c2b4-7x9kl         1/1     Running   0          8s
app-deployment-5d8f9c2b4-m2pqr         1/1     Running   0           7s
cache-pod-8b4c6f1a9-9lmn2              1/1     Running   0          6s

NAME                    STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
app-data-pvc            Bound    pvc-a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6   50Gi       RWO            vsphere-sc     5s
backup-pvc              Bound    pvc-x9y8z7w6-v5u4-43t2-s1r0-q9p8o7n6m5l4   100Gi      RWO            vsphere-sc     4s
```

!!! warning "Common errors"
    **`Error: error getting backup location: BackupStorageLocation default is not available`** — Verify the S3/MinIO credentials in the secret file and ensure the backup location is accessible with `velero backup-location get`.
    **`error: timed out waiting for backup to complete`** — Check cluster resources with `kubectl top nodes` and increase the wait timeout, or review Velero logs with `kubectl logs -n velero deployment/velero` for plugin failures.
    **`Error: error restoring PersistentVolumeClaim: error creating PersistentVolumeClaim: PersistentVolumeClaim "app-data-pvc" is invalid: spec.storageClassName: Invalid value`** — Ensure the storage class referenced in the backup exists on the target cluster, or use `velero restore create --modify-namespace-mappings` to remap storage classes.
## Troubleshoot Node NotReady

```bash
# 1. Identify NotReady node
kubectl get nodes
kubectl describe node <node-name>
# Look for: conditions, events, kubelet status

# 2. SSH to the node (via jumpbox or kubectl debug)
kubectl debug node/<node-name> -it --image=busybox

# On node:
# Check kubelet service
systemctl status kubelet
journalctl -u kubelet -n 100 --no-pager

# Check container runtime
systemctl status containerd
crictl ps

# Check disk pressure (common cause)
df -h
# If disk pressure: remove unused images
crictl rmi --prune

# 3. Check vSphere — confirm VM is powered on and has network
# Supervisor: kubectl get virtualmachine -n my-namespace
```


```text title="Expected output"
NAME                          STATUS   ROLES           AGE     VERSION
supervisor-control-plane-1    Ready    control-plane   45d     v1.27.5
worker-node-01                NotReady worker          12d     v1.27.5
worker-node-02                Ready    worker          12d     v1.27.5

● kubelet.service - kubelet: The Kubernetes Node Agent
     Loaded: loaded (/etc/systemd/system/kubelet.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Thu 2024-01-18 14:32:15 UTC; 8min ago
     Process: 2847 ExecStart=/usr/bin/kubelet (code=exited, status=1/255)

Jan 18 14:32:14 worker-node-01 kubelet[2847]: E0118 14:32:14.521847    2847 server.go:302] "Failed to load kubelet config file" err="open /etc/kubernetes/kubelet/kubelet-config.yaml: no such file or directory"

● containerd.service - containerd container runtime
     Loaded: loaded (/etc/systemd/system/containerd.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 13:45:22 UTC; 27min ago

CONTAINER ID        IMAGE                                    STATE
a7f2c3e1b9d4       registry.tanzu.vmware.com/pause:3.6     Running
c2e8f1a3d5b7       registry.tanzu.vmware.com/coredns:1.9.3  Running

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       50G   48G  1.2G  98% /
/dev/sdb1      100G   45G   55G  45% /var/lib/containerd

Deleted 12 unused images

NAME                    STATUS   POWERSTATE   AGE
tanzu-worker-node-01    True     poweredOn    12d
```

!!! warning "Common errors"
    **`Failed to load kubelet config file: open /etc/kubernetes/kubelet/kubelet-config.yaml: no such file or directory`** — Restore the kubelet config from a backup or redeploy the node using the Tanzu CLI with `tanzu machine delete` and `tanzu machine create`.
    **`disk pressure detected: 98% used`** — Run `crictl rmi --prune` to remove unused images, or expand the root volume in vSphere and resize the filesystem with `growpart /dev/sda 1 && resize2fs /dev/sda1`.
    **`Unable to connect to the server: dial tcp: lookup supervisor-control-plane-1: no such host`** — Verify DNS resolution on the node with `nslookup supervisor-control-plane-1` and check `/etc/resolv.conf` points to the correct cluster DNS server.
!!! warning "--delete-emptydir-data causes data loss for pods using emptyDir volumes"
    The `--delete-emptydir-data` flag silently deletes any data stored in emptyDir volumes on this node — including caches, temporary files, or any workload that incorrectly uses emptyDir for persistent state. Confirm no running pods rely on emptyDir before draining. This flag is only safe to use when you have confirmed all pods are stateless or all stateful pods have been rescheduled.

```bash
# 4. Force node drain and delete if unrecoverable
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data --force
kubectl delete node <node-name>
# TKC controller will provision a replacement node automatically
```


```text title="Expected output"
node/worker-node-03 cordoned
pod/nginx-deployment-7d4f8c6b9-2xk9l evicted
pod/redis-cache-5f8b9c2d-4m7p1 evicted
pod/logging-agent-ds-9k2m1 skipped
Removed taint node.kubernetes.io/unschedulable:NoSchedule from node worker-node-03
node "worker-node-03" drained
node "worker-node-03" deleted
INFO: TKC controller detected node deletion, initiating replacement provisioning
INFO: New node worker-node-03-replacement provisioned with UUID: 550e8400-e29b-41d4-a716-446655440000
```

!!! warning "Common errors"
    **`error: unable to drain node "worker-node-03", aborting command [DaemonSet-managed Pods (use --ignore-daemonsets to ignore)`** — Add the `--ignore-daemonsets` flag to the drain command to skip system pods.
    **`error: node "worker-node-03" not found`** — Verify the exact node name with `kubectl get nodes` before attempting deletion.
    **`error: timed out waiting for pod eviction after 5m0s`** — Increase the timeout with `--timeout=10m` or use `--force` to forcefully terminate stubborn pods.
## Configure Persistent Storage (vSAN CNS/CSI)

TKG uses the vSphere CSI driver to provision persistent volumes backed by vSAN datastores.

```bash
# 1. Verify CSI driver is running
kubectl get pods -n vmware-system-csi
# All pods should be Running

# 2. List available storage classes
kubectl get storageclass
# vSAN storage classes are provisioned by Supervisor automatically

# 3. Create a PVC using a vSAN storage class
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
  namespace: app-namespace
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 50Gi
  storageClassName: wcpglobal-storage-profile
EOF

# 4. Verify PVC is bound
kubectl get pvc app-data -n app-namespace
# STATUS should be Bound; VOLUME shows the CNS volume ID

# 5. Check volume in vSAN (vCenter UI)
# vSAN → Container Volumes → confirm CNS volume listed with correct size and policy
```


```text title="Expected output"
NAME                                             READY   STATUS    RESTARTS   AGE
vsphere-csi-controller-6d8f4c7b9-2kxlm          3/3     Running   0          8d
vsphere-csi-node-4j5nm                          3/3     Running   0          8d
vsphere-csi-node-7p2qr                          3/3     Running   0          8d
vsphere-csi-node-9m8ks                          3/3     Running   0          8d

NAME                                PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE   AGE
wcpglobal-storage-profile           csi.vsphere.vmware.com  Delete          WaitForFirstConsumer 45d
vsan-default-storage-policy         csi.vsphere.vmware.com  Delete          WaitForFirstConsumer 45d

persistentvolumeclaim/app-data created

NAME       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                AGE
app-data   Bound    pvc-a7f2e1c9-3b44-11ed-9c4a-005056a12345   50Gi       RWO            wcpglobal-storage-profile   12s
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "storageclass"`** — Verify you are connected to a Tanzu Supervisor cluster (not a guest cluster) with `kubectl cluster-info`.
    **`PersistentVolumeClaim does not exist`** — Ensure the namespace `app-namespace` exists by running `kubectl create namespace app-namespace` before applying the PVC.
    **`ProvisioningFailed: error getting credentials`** — Confirm the vSAN cluster has network connectivity to the Supervisor control plane and CSI driver credentials are valid in the `vmware-system-csi` namespace.
---

## Enable vSphere with Tanzu on a Cluster (Supervisor)

This procedure activates the Tanzu Supervisor on a vSphere cluster, enabling it to host vSphere Namespaces and TKG workload clusters. This is the initial setup step — run once per cluster.

### Prerequisites

![Prerequisites](../../../../../assets/tanzu-proc-prerequisites.svg)

- vSphere 7.x+ or 8.x with Enterprise Plus license
- vSAN or an external NFS/iSCSI datastore for persistent storage
- NSX-T or VDS-based networking (NSX-T required for pod networking; VDS supported for basic workloads)
- DNS record for the Supervisor Control Plane: `supervisor.example.local → <supervisor-vip>`
- IP ranges reserved for: Supervisor Control Plane VMs (3 IPs), Ingress/Egress, Pods

### Step 1 — Configure Namespace and Network Settings in vCenter

![Step 1 — Configure Namespace and Network Settings in vCenter](../../../../../assets/tanzu-proc-step-1-configure-namespace-and-network-settings-in-vcenter.svg)

1. vCenter → **Workload Management → Enable**
2. Select the target cluster → **Enable Workload Management**
3. In the wizard:
   - **Networking**: choose NSX-T or VDS-based networking
   - **Storage**: assign a storage policy (vSAN Default or custom) for Supervisor VMs and PVCs
   - **Load Balancer**: specify NSX ALB or HA Proxy VIP range for ingress
   - **Workload Network**: define the pod CIDR, service CIDR, and egress CIDRs (must not overlap with physical network)
   - **Control Plane Size**: Tiny/Small/Medium/Large — match to expected workload scale

4. Set the **API Server endpoint** DNS name — must resolve to the VIP from all Kubernetes clients
5. Click **Finish** — vCenter provisions three Supervisor Control Plane VMs and configures the cluster

### Step 2 — Monitor Enablement

![Step 2 — Monitor Enablement](../../../../../assets/tanzu-proc-step-2-monitor-enablement.svg)

```bash
# Monitor from vCenter → Workload Management → Supervisor
# Status progresses: Configuring → Running (typically 10–20 min)

# Or check via kubectl after the supervisor IP is reachable
kubectl get svc -n kube-system --kubeconfig <supervisor-kubeconfig>
```


```text title="Expected output"
NAME                                TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
kube-dns                            ClusterIP      10.96.0.10       <none>        53/UDP,53/TCP            18m
kube-apiserver                      ClusterIP      10.96.0.1        <none>        443/TCP                  18m
etcd                                ClusterIP      10.96.0.13       <none>        2379/TCP                 18m
metrics-server                      ClusterIP      10.96.0.100      <none>        443/TCP                  17m
vmware-system-csi                   ClusterIP      10.96.1.50       <none>        443/TCP                  16m
wcp-webhook-service                 ClusterIP      10.96.2.75       <none>        443/TCP                  15m
```

!!! warning "Common errors"
    **`Unable to connect to the server: dial tcp 192.168.1.200:6443: i/o timeout`** — Verify the supervisor cluster IP is reachable and the kubeconfig points to the correct supervisor endpoint; check network connectivity and firewall rules.
    **`error: the server doesn't have a resource type "svc"`** — Ensure you are using a valid kubeconfig for the supervisor cluster, not a guest cluster kubeconfig.
    **`error: open <supervisor-kubeconfig>: no such file or directory`** — Replace `<supervisor-kubeconfig>` with the actual path to your downloaded supervisor kubeconfig file from vCenter.
### Step 3 — Download the Supervisor kubeconfig

![Step 3 — Download the Supervisor kubeconfig](../../../../../assets/tanzu-proc-step-3-download-the-supervisor-kubeconfig.svg)

1. vCenter → **Workload Management → Supervisors → select the supervisor → Configure → Namespace → Download kubeconfig**
2. Save as `supervisor.kubeconfig`

```bash
kubectl --kubeconfig=supervisor.kubeconfig get nodes
# Expect 3 Supervisor Control Plane nodes in Ready state
```


```text title="Expected output"
NAME                                    STATUS   ROLES                  AGE   VERSION
supervisor-node-01.vmware.local         Ready    control-plane,master   45d   v1.27.11+vmware.2-fips.1
supervisor-node-02.vmware.local         Ready    control-plane,master   45d   v1.27.11+vmware.2-fips.1
supervisor-node-03.vmware.local         Ready    control-plane,master   45d   v1.27.11+vmware.2-fips.1
```

!!! warning "Common errors"
    **`error: unable to access the server: dial tcp: lookup supervisor-node-01.vmware.local: no such host`** — Verify the kubeconfig file points to a valid Supervisor Cluster endpoint and DNS resolution is working from your admin machine.
    **`error: You must be logged in to the server (Unauthorized)`** — Re-authenticate to the Supervisor Cluster using `kubectl vsphere login` with valid vSphere credentials.
    **`NotReady`** — Check node health with `kubectl describe node <node-name>` and review kubelet logs on the affected Supervisor node for resource or networking issues.
### Step 4 — Post-Enablement Validation

![Step 4 — Post-Enablement Validation](../../../../../assets/tanzu-proc-step-4-post-enablement-validation.svg)

- [ ] Supervisor shows **Running** in vCenter → Workload Management
- [ ] Three Supervisor Control Plane VMs visible in vCenter (prefixed `SupervisorControlPlaneVM`)
- [ ] `kubectl get nodes` returns 3 Ready nodes
- [ ] `kubectl get ns` shows `kube-system`, `vmware-system-*` namespaces

---

## Configure Antrea Network Policy (Pod Security)

Antrea is the default CNI plugin for Tanzu workload clusters. Antrea Network Policies restrict traffic between pods and namespaces, implementing micro-segmentation at the Kubernetes layer.

### Kubernetes NetworkPolicy (Standard)

![Kubernetes NetworkPolicy (Standard)](../../../../../assets/tanzu-proc-kubernetes-networkpolicy-standard.svg)

Kubernetes NetworkPolicy objects are namespace-scoped and select pods by label. They define allowed ingress and egress:

```yaml
# Allow only pods with app=backend to receive traffic from app=frontend on port 8080
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  policyTypes:
  - Ingress
```

```bash
kubectl apply -f network-policy.yaml
kubectl get networkpolicy -n prod
```


```text title="Expected output"
networkpolicy.networking.k8s.io/allow-ingress created
networkpolicy.networking.k8s.io/deny-egress created
NAME              POD-SELECTOR       AGE
allow-ingress     app=web            2m
deny-egress       app=database       2m
restrict-traffic  tier=backend       5m
```

!!! warning "Common errors"
    **`error: error validating "network-policy.yaml": error validating data: ValidationError(NetworkPolicy.spec.ingress[0].from[0]): invalid type for io.k8s.api.networking.v1.NetworkPolicyPeer: got "string", expected "object"`** — Verify the YAML indentation and structure of the `from` field, ensuring it contains objects not strings.
    **`Error from server (Forbidden): networkpolicies.networking.k8s.io is forbidden: User "system:serviceaccount:default:deployer" cannot create resource "networkpolicies" in API group "networking.k8s.io" in the namespace "prod"`** — Grant the service account or user the `create` permission for networkpolicies using a ClusterRole or Role binding.
### Antrea ClusterNetworkPolicy (Cluster-Wide, Higher Priority)

![Antrea ClusterNetworkPolicy (Cluster-Wide, Higher Priority)](../../../../../assets/tanzu-proc-antrea-clusternetworkpolicy-cluster-wide-higher-priority.svg)

Antrea ClusterNetworkPolicy (ACNP) applies cluster-wide and takes priority over namespace-scoped NetworkPolicy. Use for enforcing baseline security rules that namespace owners cannot override:

```yaml
# Deny all east-west traffic between namespaces unless explicitly allowed
apiVersion: crd.antrea.io/v1alpha1
kind: ClusterNetworkPolicy
metadata:
  name: deny-cross-namespace-default
spec:
  priority: 5
  appliedTo:
  - namespaceSelector: {}
  ingress:
  - action: Drop
    from:
    - namespaceSelector:
        matchExpressions:
        - key: kubernetes.io/metadata.name
          operator: NotIn
          values: ["kube-system", "vmware-system-csi"]
    # All cross-namespace traffic denied unless a lower-priority NetworkPolicy allows it
```

```bash
kubectl apply -f cluster-network-policy.yaml
kubectl get clusternetworkpolicy
```


```text title="Expected output"
clusternetworkpolicy.networking.tanzu.vmware.com/default-deny created
NAME           AGE
default-deny   2s
```

!!! warning "Common errors"
    **`error: resource mapping not found for name: "clusternetworkpolicy" namespace: "" from "cluster-network-policy.yaml": no matches for kind "ClusterNetworkPolicy" in version "networking.tanzu.vmware.com/v1alpha1"`** — Ensure the Tanzu networking extension is installed on the cluster with `kubectl apply -f https://...tanzu-networking-extension.yaml`.
    **`The ClusterNetworkPolicy "default-deny" is invalid: spec.rules: Invalid value: []uint8(nil): rules must be specified`** — Add at least one ingress or egress rule to the spec.rules field in your YAML manifest.
### Test Policy Enforcement

![Test Policy Enforcement](../../../../../assets/tanzu-proc-test-policy-enforcement.svg)

```bash
# Verify policy is enforced: exec into the frontend pod and test connectivity
kubectl exec -n prod -it <frontend-pod> -- curl http://backend-svc:8080   # should succeed
kubectl exec -n prod -it <frontend-pod> -- curl http://database-svc:5432  # should fail if not allowed

# Antrea provides a traceflow tool for debugging policy drops
kubectl antctl traceflow -S frontend-pod -D backend-pod -n prod
```


```text title="Expected output"
Defaulting container name to frontend-app.
pod/frontend-7d4c9f2b exec session started
<!DOCTYPE html>
<html>
<head><title>200 OK</title></head>
<body>Backend service responding</body>
</html>
command terminated with exit code 1
Defaulting container name to frontend-app.
pod/frontend-7d4c9f2b exec session started
curl: (7) Failed to connect to database-svc port 5432: Connection refused

Traceflow for frontend-pod -> backend-pod (prod namespace):
  Src: 10.244.1.15 (frontend-pod)
  Dst: 10.244.2.8 (backend-pod)
  Protocol: TCP/6
  Phase: Forwarded
  Action: ALLOWED
  Timestamp: 2024-01-15T14:32:18Z
```

!!! warning "Common errors"
    **`error: unable to upgrade connection: container not found ("frontend-app")`** — Specify the correct container name with `-c <container-name>` flag or verify the pod exists with `kubectl get pods -n prod`.
    **`error: unable to find "frontend-pod" in namespace "prod"`** — Use the full pod name from `kubectl get pods -n prod` instead of a partial name; traceflow requires exact pod identifiers.
---

## Decommission a vSphere Namespace

Decommissioning a namespace removes all TKG clusters, PVCs, and Kubernetes objects within it. This is the correct method to fully clean up a namespace and release its IP/storage allocations.

!!! danger "Deleting a namespace is permanent and removes all workloads and data within it"
    All TKG workload clusters, running pods, persistent volumes, and configuration in the namespace are deleted. There is no undo. Ensure all workloads have been migrated or decommissioned and all data backed up before proceeding.

### Step 1 — Delete TKG Workload Clusters First

![Step 1 — Delete TKG Workload Clusters First](../../../../../assets/tanzu-proc-step-1-delete-tkg-workload-clusters-first.svg)

Before deleting the namespace, explicitly delete all TKG clusters it contains:

```bash
# List clusters in the namespace
kubectl get tanzukubernetescluster -n <namespace>

# Delete each cluster
kubectl delete tanzukubernetescluster <cluster-name> -n <namespace>

# Wait for cluster deletion to complete (control plane VMs are deleted from vCenter)
kubectl get tanzukubernetescluster -n <namespace>
# When the namespace returns empty, clusters are gone
```


```text title="Expected output"
NAME                    STATUS   READY   SEVERITY   REASON
prod-cluster-01         Ready    True    Normal     
staging-cluster-02      Ready    True    Normal     
dev-cluster-03          Ready    True    Normal     
tanzukubernetescluster.run.tanzu.vmware.com "prod-cluster-01" deleted
tanzukubernetescluster.run.tanzu.vmware.com "staging-cluster-02" deleted
tanzukubernetescluster.run.tanzu.vmware.com "dev-cluster-03" deleted
NAME                    STATUS           READY   SEVERITY   REASON
prod-cluster-01         Deleting         False   Warning    DeletionInProgress
staging-cluster-02      Deleting         False   Warning    DeletionInProgress
dev-cluster-03          Deleting         False   Warning    DeletionInProgress
(After 2-3 minutes)
No resources found in default namespace.
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "tanzukubernetescluster"`** — Verify the Tanzu operator is installed with `kubectl get deployment -n tanzu-system` and check your cluster has the correct API extensions.
    **`Error from server (NotFound): namespaces "<namespace>" not found`** — Confirm the namespace exists with `kubectl get ns` and use the correct namespace name in the `-n` flag.
    **`error: timed out waiting for the condition`** — If deletion hangs beyond 5 minutes, check vCenter for orphaned VMs and manually remove them, then retry the delete command.
### Step 2 — Release Persistent Volumes

![Step 2 — Release Persistent Volumes](../../../../../assets/tanzu-proc-step-2-release-persistent-volumes.svg)

```bash
# List PVCs in the namespace
kubectl get pvc -n <namespace>

# Delete PVCs — this triggers vSAN CNS volume deletion
kubectl delete pvc --all -n <namespace>
```


```text title="Expected output"
NAME                                       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
tanzu-mysql-data-pvc                       Bound    pvc-a7f3c2e1-9b4d-4f8a-b2c9-1d5e8f9a0b1c   50Gi       RWO            vsan-default   45d
tanzu-etcd-backup-pvc                      Bound    pvc-b8g4d3f2-0c5e-5g9b-c3d0-2e6f9g0b1c2d   100Gi      RWO            vsan-default   32d
tanzu-logging-pvc                          Bound    pvc-c9h5e4g3-1d6f-6h0c-d4e1-3f7g0h1c2d3e   20Gi       RWO            vsan-default   18d
persistentvolumeclaim "tanzu-mysql-data-pvc" deleted
persistentvolumeclaim "tanzu-etcd-backup-pvc" deleted
persistentvolumeclaim "tanzu-logging-pvc" deleted
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "pvc" in API group ""`** — Verify the cluster is running and `kubectl` is configured correctly with `kubectl cluster-info`.
    **`Error from server (Forbidden): persistentvolumeclaims is forbidden: User "system:serviceaccount:default:default" cannot delete resource "persistentvolumeclaims"`** — Ensure your service account or user has RBAC permissions to delete PVCs in the target namespace.
### Step 3 — Delete the Namespace via vCenter

![Step 3 — Delete the Namespace via vCenter](../../../../../assets/tanzu-proc-step-3-delete-the-namespace-via-vcenter.svg)

1. vCenter → **Workload Management → Namespaces** → select the namespace → **Delete**
2. vCenter deregisters the namespace from the Supervisor, removes network and storage allocations
3. The namespace disappears from the Supervisor's namespace list

```bash
# Or via kubectl against the Supervisor
kubectl --kubeconfig=supervisor.kubeconfig delete namespace <namespace>
```


```text title="Expected output"
namespace "workload-prod" deleted
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "namespace"`** — Verify the kubeconfig points to a valid Supervisor cluster and that your user has API server access.
    **`Error from server (NotFound): namespaces "<namespace>" not found`** — Confirm the namespace name is spelled correctly and exists before attempting deletion.
    **`error: unable to read client certificate ... (no such file or directory)`** — Ensure the supervisor.kubeconfig file path is correct and the certificate files it references are accessible.
### Step 4 — Post-Deletion Validation

![Step 4 — Post-Deletion Validation](../../../../../assets/tanzu-proc-step-4-post-deletion-validation.svg)

- [ ] Namespace no longer appears in vCenter → Workload Management → Namespaces
- [ ] `kubectl get ns` on the Supervisor no longer lists the namespace
- [ ] vSAN datastore freed: confirm PVC backing volumes are deleted in vCenter → Storage
- [ ] DNS records for TKG cluster API endpoints removed (if manually created)
- [ ] IP addresses for the namespace's ingress and load balancer VIPs released in IPAM

---

## See also

- [Tanzu — Health Checks](../health-checks/)
- [Virtualization Vmware Tanzu — Common Issues](../../troubleshooting/common-issues/)
- [Tanzu — CLI Reference](../cli-reference/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
