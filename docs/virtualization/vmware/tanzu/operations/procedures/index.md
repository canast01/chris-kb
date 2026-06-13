---
tags:
  - operations
  - tanzu
  - vmware
---
# Tanzu — Procedures


<div class="kb-summary">
TKG and Tanzu operations — namespace and workload cluster lifecycle, RBAC, Harbor project configuration, Helm deployments, Ingress setup, node scaling, cluster upgrade, Velero backup/restore, and persistent storage via vSAN CNS.

*Applies to: Tanzu 3.x*
</div>
```text
┌──────────────────────── Virtualization Vmware Tanzu — Operational Procedures ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Vmware operational procedures: standard tasks for day-2 administration            │   │
│   │           Covers: provisioning, expansion, maintenance, DR testing, and decommission          │   │
│   │           Pre/post checks required for all maintenance activities affecting storage           │   │
│   │            All procedures require approved change management tickets in production            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Open change → pre-check → execute → verify → post-check → close                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Procedure     │    Pre-check     │       Steps       │      Verify      │    Post-check    │   │
│   │    Provision     │  Capacity free?  │   Create volume   │   Host access    │   Monitor I/O    │   │
│   │      Expand      │   Pool space?    │    Grow volume    │    FS resize     │   Verify size    │   │
│   │     Snapshot     │   Policy set?    │   Take snapshot   │   Snap listed    │   Consistency    │   │
│   │     Failover     │  Repl. in sync?  │    Break repl.    │    App online    │    Verify RTO    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Tanzu infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Tanzu platform overview and core concepts               │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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

---

## Scale Worker Nodes

```bash
# For vSphere with Tanzu (TanzuKubernetesCluster):
kubectl edit tanzukubernetescluster team-alpha-cluster -n team-alpha
# Change: spec.topology.nodePools[0].replicas: 5 → 7

# For standalone TKG:
tanzu cluster scale team-alpha-cluster --worker-machine-count 7
```

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

One minor version at a time — do not skip versions (e.g., 1.26 → 1.27, not 1.26 → 1.28).

## Delete a TKG Workload Cluster

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

# 4. Force node drain and delete if unrecoverable
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data --force
kubectl delete node <node-name>
# TKC controller will provision a replacement node automatically
```

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

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
