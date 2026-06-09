# Tanzu — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Tanzu Kubernetes Grid on vSphere. Covers Workload Management enablement, Supervisor cluster initialisation, vSphere namespace configuration, TKG workload cluster provisioning, Harbor registry setup, and developer onboarding validation.
</div>

```text
┌────────────────────────────────────── Tanzu — Deployment Phases ──────────────────────────────────────┐
│                                                                                                       │
│  Six phases from licensed vSphere cluster to operational TKG environment. Each phase has a clear      │
│  exit criterion. Do not proceed until the current phase validates clean.                              │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐ │
│   │  Phase 1: Prerequisites     │  │  Phase 2: Workload Mgmt      │  │  Phase 3: vSphere Namespace  │ │
│   │  vSphere 7.0 U2+ / 8.x      │  │  vCenter → Workload Mgmt     │  │  Create namespace per team   │ │
│   │  NSX-T or VDS+HAProxy        │  │  Control plane size select   │  │  CPU/RAM/storage quotas      ││
│   │  DNS for Supervisor VIP      │  │  Pod/service CIDR config     │  │  Storage policy assign       ││
│   │  Content library planned     │  │  Wait for Supervisor Ready   │  │  AD user/group permissions   ││
│   └─────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘ │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐ │
│   │  Phase 4: TKG Cluster       │  │  Phase 5: Harbor Registry    │  │  Phase 6: Validation         │ │
│   │  kubectl vsphere login      │  │  Deploy Harbor OVA           │  │  All cluster nodes Ready     │ │
│   │  Apply TanzuK8sCluster YAML │  │  Configure LDAP/OIDC + TLS   │  │  Harbor: images push/pull    │ │
│   │  Choose TKR release         │  │  Create projects per team    │  │  PVC: CSI provisioning       │ │
│   │  Wait for cluster Ready     │  │  Robot accounts for CI/CD    │  │  Network policy enforced     │ │
│   └─────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘ │
│                                                                                                       │
│  Physical Infrastructure: vSphere cluster (ESXi hosts) · vSAN or NFS datastore · NSX-T fabric         │
│  (or VDS+HAProxy) · management network · DNS/NTP infrastructure · content library datastore.          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Supervisor       = vSphere-integrated Kubernetes control plane running as ESXi kernel components     │
│  TKR              = Tanzu Kubernetes Release; versioned OS+K8s image from content library             │
│  vSphere Namespace= resource boundary with CPU/RAM/storage quotas; maps to K8s namespace              │
│  CAPI/CAPV        = Cluster API / vSphere provider; reconciles TanzuKubernetesCluster CRDs            │
│  Spherelet        = kubelet equivalent running in the ESXi VMkernel; registers host as K8s node       │
│  NCP              = NSX Container Plugin; syncs K8s network objects to NSX-T                          │
│  vSphere CSI      = Container Storage Interface driver; provisions FCD-backed PVCs from vSAN          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Prerequisites

**Exit criterion:** vSphere cluster licensed, NSX-T (or VDS) confirmed, DNS/NTP validated, and content library registered.

### vSphere Requirements

| Requirement | Detail |
|---|---|
| vSphere version | 7.0 U2+ or 8.x (Enterprise Plus licence for Workload Management) |
| Cluster storage | vSAN, NFS, or iSCSI — must support vSphere CSI |
| Networking | NSX-T 3.1+ (recommended) or VDS 7.0+ with HAProxy load balancer |
| ESXi hosts | Minimum 3 hosts in the target cluster; hosts time-synced |
| DNS | A-record for Supervisor API VIP; forward/reverse for all control plane VMs |
| Content library | Tanzu content library subscribed from VMware or local mirror |

### DNS Pre-check

```bash
# Verify Supervisor VIP A-record resolves before enabling Workload Management
nslookup supervisor.example.local
# Confirm PTR record for the Supervisor VIP also exists
nslookup <supervisor-VIP>
```

### NTP Verification

```bash
# Verify NTP on each ESXi host (SSH to host)
esxcli system ntp get
esxcli system ntp stats
# Clock offset should be < 1 second
```

---

## Phase 2 — Enable Workload Management (Supervisor)

**Exit criterion:** Supervisor cluster in Running state; three control plane VMs healthy in vCenter.

### Enable via vSphere Client

```text
vCenter → Workload Management → Get Started → Select vSphere cluster

  Step 1: Cluster         — select the vSphere cluster to host the Supervisor
  Step 2: Control Plane   — size: Tiny (lab) / Small / Medium (production: 4 vCPU, 16 GB RAM)
  Step 3: Storage         — select default storage policy for control plane VMs
  Step 4: Load Balancer   — NSX-T (auto-configured) or AVI (enter AVI controller FQDN + credentials)
  Step 5: Management Net  — select management portgroup; enter IP range for 5 control plane VM IPs
  Step 6: Workload Net    — NSX-T: enter ingress/egress CIDRs, pod CIDR, service CIDR
  Step 7: Content Library — select the Tanzu Kubernetes releases content library
  Step 8: Finish          — deployment takes 30–60 minutes
```

### Monitor Supervisor Status

```bash
# After wizard completes, check Supervisor status
# vCenter → Workload Management → Clusters tab
# Wait for Status: Running (green)

# Verify control plane VMs in vCenter inventory
# Three VMs named: SupervisorControlPlaneVM-0, -1, -2
```

### Post-Enable Checks

```bash
# Retrieve Supervisor API server endpoint
# vCenter → Workload Management → Clusters → click cluster → Control Plane Node IP Address

# Test Supervisor API connectivity from admin workstation
curl -sk https://<supervisor-VIP>:443/api/ | head -5
# Expected: API discovery response
```

---

## Phase 3 — vSphere Namespace Configuration

**Exit criterion:** At least one namespace created with resource limits, storage policy, and AD permissions assigned.

### Create a vSphere Namespace

```text
vCenter → Workload Management → Namespaces → New Namespace
  Cluster: select Supervisor cluster
  Name: team-prod (lowercase, no spaces)
  → Create
```

### Assign Resource Limits

```text
Namespace → Edit → Capacity and Usage
  CPU limit: 64 GHz
  Memory limit: 256 GB
  Storage limit: 2 TB
```

### Assign Storage Policies

```text
Namespace → Edit → Storage → Add Storage
  Select policy: vSAN Default Storage Policy
  Storage limit: 2 TB
  → Add (this creates the StorageClass usable by PVCs in the namespace)
```

### Assign Permissions

```text
Namespace → Edit → Permissions → Add Permission
  Identity source: vsphere.local (or AD domain)
  User/Group: <AD group for namespace owners>
  Role: Edit (for cluster admins) or View (for read-only)
```

### Verify Namespace

```bash
# Authenticate to Supervisor and list namespaces
kubectl vsphere login --server <supervisor-VIP> --vsphere-username administrator@vsphere.local --insecure-skip-tls-verify
kubectl config get-contexts
kubectl get namespaces
```

---

## Phase 4 — TKG Workload Cluster Provisioning

**Exit criterion:** TKG cluster in Ready state with all nodes in Ready status; kubeconfig retrieved successfully.

### Authenticate to Supervisor

```bash
kubectl vsphere login \
  --server <supervisor-VIP> \
  --vsphere-username administrator@vsphere.local \
  --insecure-skip-tls-verify

# Switch context to the target vSphere namespace
kubectl config use-context team-prod
```

### List Available TKG Releases

```bash
# Show available TanzuKubernetesRelease images in the content library
kubectl get tanzukubernetesrelease
# Choose a TKR from this list for the cluster manifest below
```

### Deploy TKG Workload Cluster

```bash
cat > prod-cluster.yaml <<'EOF'
apiVersion: run.tanzu.vmware.com/v1alpha3
kind: TanzuKubernetesCluster
metadata:
  name: prod-cluster
  namespace: team-prod
spec:
  topology:
    controlPlane:
      replicas: 3
      vmClass: best-effort-medium
      storageClass: vsan-default
      tkr:
        reference:
          name: v1.28.8---vmware.1-tkg.2
    nodePools:
    - name: worker-pool-1
      replicas: 5
      vmClass: best-effort-large
      storageClass: vsan-default
      volumes:
      - name: containerd-storage
        mountPath: /var/lib/containerd
        capacity:
          storage: 50Gi
EOF

kubectl apply -f prod-cluster.yaml
```

### Monitor Cluster Provisioning

```bash
# Watch cluster status (takes 10–20 minutes)
kubectl get tanzukubernetescluster prod-cluster -w

# Check individual machine objects
kubectl get machines -n team-prod

# Once cluster Ready, retrieve kubeconfig
kubectl vsphere login \
  --server <supervisor-VIP> \
  --vsphere-username administrator@vsphere.local \
  --tanzu-kubernetes-cluster-name prod-cluster \
  --tanzu-kubernetes-cluster-namespace team-prod \
  --insecure-skip-tls-verify

kubectl config use-context prod-cluster
kubectl get nodes
# Expected: all nodes in Ready state
```

---

## Phase 5 — Harbor Container Registry

**Exit criterion:** Harbor running, CA-signed certificate installed, projects and robot accounts created, Trivy scanner enabled.

### Deploy Harbor OVA

```text
vCenter → Deploy OVF Template → Harbor-<version>.ova
  Network:   Management portgroup
  Storage:   vSAN or NFS datastore (all images stored here; size appropriately)
  Customize: Set FQDN, IP, gateway, DNS, NTP, admin password, root password
  → Deploy (takes ~5 minutes)
```

### Initial Harbor Configuration

```bash
# Access Harbor UI at https://harbor.example.local
# Login: admin / <password set at deploy>

# Change default admin password immediately
# Administration → Users → admin → Set Password

# Configure LDAP/OIDC (Administration → Configuration → Authentication)
# Server: ldaps://ad.example.local:636
# Search DN: CN=svc-harbor,OU=Service Accounts,DC=example,DC=local
```

### Install CA-Signed Certificate

```bash
# Upload certificate via Harbor VAMI (port 443 or 8080)
# Administration → Configuration → System Settings
# Registry Root Certificate: paste CA-signed cert PEM
# Registry Certificate: paste server cert PEM
# Registry Certificate Key: paste private key PEM
# → Save
```

### Create Projects and Robot Accounts

```bash
# Create project via Harbor API
curl -u admin:<password> -X POST \
  -H "Content-Type: application/json" \
  -d '{"project_name":"team-prod","public":false}' \
  https://harbor.example.local/api/v2.0/projects

# Create robot account for CI/CD pipeline
curl -u admin:<password> -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"ci-pipeline","description":"CI push account","permissions":[{"kind":"project","namespace":"team-prod","access":[{"resource":"repository","action":"push"},{"resource":"repository","action":"pull"}]}]}' \
  https://harbor.example.local/api/v2.0/robots

# Enable Trivy vulnerability scanning
# Administration → Interrogation Services → Trivy → Edit → Enable
```

---

## Phase 6 — End-to-End Validation

**Exit criterion:** All checks pass. Hand off to operations team.

### Cluster Node Health

```bash
kubectl config use-context prod-cluster
kubectl get nodes -o wide
# All nodes: Ready, correct Kubernetes version

kubectl get pods -A | grep -v Running | grep -v Completed
# No pods in CrashLoopBackOff or Pending state
```

### PVC Provisioning Test

```bash
cat > pvc-test.yaml <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-test
  namespace: default
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: vsan-default
  resources:
    requests:
      storage: 5Gi
EOF

kubectl apply -f pvc-test.yaml
kubectl get pvc pvc-test
# Expected: STATUS = Bound (CSI provisioning confirmed)
kubectl delete pvc pvc-test
```

### Harbor Push/Pull Test

```bash
# Docker login with robot account credentials
docker login harbor.example.local -u 'robot$ci-pipeline' -p <robot-token>

# Tag and push a test image
docker pull alpine:latest
docker tag alpine:latest harbor.example.local/team-prod/alpine:test
docker push harbor.example.local/team-prod/alpine:test

# Verify image appears in Harbor UI and scan completes
# Harbor → Projects → team-prod → Repositories → alpine → test
```

### Network Policy Test

```bash
# Confirm Antrea/NSX CNI is running
kubectl get pods -n kube-system | grep -E 'antrea|ncp'

# Verify Supervisor API still reachable from within cluster
kubectl run nettest --image=alpine --restart=Never --rm -it -- \
  wget -qO- https://<supervisor-VIP>:443/api/
```

### Post-Deployment Checklist

| Item | Check |
|---|---|
| Supervisor status | Running (green) in Workload Management |
| Control plane VMs | Three SupervisorControlPlaneVM VMs powered on |
| TKG cluster nodes | All nodes in kubectl get nodes show Ready |
| vSAN CSI | PVC bound in < 30 seconds |
| Harbor TLS | Browser shows valid CA-signed certificate |
| Harbor scan | Trivy scan completes on pushed image |
| AD authentication | AD users can log in to namespace via kubectl vsphere login |
| Content library | TKR images available and up to date |
| DNS | Supervisor VIP and control plane VM FQDNs resolve |
| NTP | All ESXi hosts and vCenter drift < 1 second |
