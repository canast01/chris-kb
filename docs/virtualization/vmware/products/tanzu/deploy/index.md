---
tags:
  - deployment
  - tanzu
  - vmware
search:
  boost: 1.5
description: "End-to-end deployment guide for VMware Tanzu Kubernetes Grid on vSphere. Covers Workload Management enablement, Supervisor cluster initialisation, vSphere..."
---
# Tanzu — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Tanzu Kubernetes Grid on vSphere. Covers Workload Management enablement, Supervisor cluster initialisation, vSphere namespace configuration, TKG workload cluster provisioning, Harbor registry setup, and developer onboarding validation.

*Applies to: Tanzu 3.x*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_prerequisites: "Phase 1 — Prerequisites" {shape: rectangle}
phase_2_enable_workload_management_s: "Phase 2 — Enable Workload Management (Supervisor)" {shape: rectangle}
phase_3_vsphere_namespace_configurat: "Phase 3 — vSphere Namespace Configuration" {shape: rectangle}
phase_4_tkg_workload_cluster_provisi: "Phase 4 — TKG Workload Cluster Provisioning" {shape: rectangle}
phase_5_harbor_container_registry: "Phase 5 — Harbor Container Registry" {shape: rectangle}
phase_6_endtoend_validation: "Phase 6 — End-to-End Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_prerequisites
phase_1_prerequisites -> phase_2_enable_workload_management_s
phase_2_enable_workload_management_s -> phase_3_vsphere_namespace_configurat
phase_3_vsphere_namespace_configurat -> phase_4_tkg_workload_cluster_provisi
phase_4_tkg_workload_cluster_provisi -> phase_5_harbor_container_registry
phase_5_harbor_container_registry -> phase_6_endtoend_validation
phase_6_endtoend_validation -> validate
```

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

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


```text title="Expected output"
Server:		10.0.1.53
Address:	10.0.1.53#53

Name:	supervisor.example.local
Address: 10.20.30.40
Address: 10.20.30.41

Server:		10.0.1.53
Address:	10.0.1.53#53
40.30.20.10.in-addr.arpa	name = supervisor.example.local.
41.30.20.10.in-addr.arpa	name = supervisor.example.local.
```

!!! warning "Common errors"
    **`** server can't find supervisor.example.local: NXDOMAIN`** — Add the A-record for supervisor.example.local to your DNS server before enabling Workload Management.
    **`** server can't find 40.30.20.10.in-addr.arpa: NXDOMAIN`** — Create a PTR record in your reverse DNS zone pointing the Supervisor VIP back to supervisor.example.local.
### NTP Verification

```bash
# Verify NTP on each ESXi host (SSH to host)
esxcli system ntp get
esxcli system ntp stats
# Clock offset should be < 1 second
```


```text title="Expected output"
NTP Enabled: true
NTP Servers: 10.20.30.40, 10.20.30.41
NTP Running: true

Remote Server: 10.20.30.40, Stratum: 2, ReferenceID: 192.168.1.1, Synchronized: true, Reachability: 377, Delay(ms): 12.543, Offset(ms): 0.234
Remote Server: 10.20.30.41, Stratum: 2, ReferenceID: 192.168.1.2, Synchronized: true, Reachability: 377, Delay(ms): 14.821, Offset(ms): -0.156
```

!!! warning "Common errors"
    **`Could not connect to the host. The host may not be running, or the login credentials may not be correct.`** — Verify SSH connectivity to the ESXi host and confirm credentials are correct.
    **`NTP Enabled: false`** — Enable NTP with `esxcli system ntp set --enabled=true` and start the service with `esxcli system service start ntpd`.
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


```text title="Expected output"
{
  "kind": "APIGroup",
  "apiVersion": "v1",
  "name": "api",
  "versions": [
    {
      "groupVersion": "v1",
      "version": "v1"
    },
    {
      "groupVersion": "apps/v1",
      "version": "v1"
    }
  ],
  "preferredVersion": {
    "groupVersion": "v1",
    "version": "v1"
  }
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to <supervisor-VIP> port 443: Connection refused`** — Verify the Supervisor VIP is correct and reachable from your workstation by pinging the IP first.
    **`curl: (60) SSL certificate problem: self signed certificate`** — The `-k` flag should bypass SSL verification; if still failing, ensure you're using lowercase `-sk` and not mixing with other curl options.
    **`curl: (6) Could not resolve host`** — Confirm the `<supervisor-VIP>` placeholder was replaced with an actual IP address (e.g., `192.168.1.100`) and is resolvable from your network.
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


```text title="Expected output"
Logged in successfully to 'https://10.42.100.15' as 'administrator@vsphere.local'
The server has a self signed certificate. Proceeding anyway.

CURRENT   NAME                          CLUSTER                       AUTHINFO                      NAMESPACE
*         10.42.100.15                  10.42.100.15                  wcp:10.42.100.15:administrator@vsphere.local   
          tanzu-cli-mc-stg              tanzu-cli-mc-stg              tanzu-cli-mc-stg-user         

NAME              STATUS   AGE
default           Active   45d
kube-node-lease   Active   45d
kube-public       Active   45d
kube-system       Active   45d
workload-prod     Active   38d
workload-staging  Active   22d
...
```

!!! warning "Common errors"
    **`error: Unable to connect to the server: dial tcp: lookup <supervisor-VIP>: no such host`** — Replace `<supervisor-VIP>` with the actual Supervisor Cluster IP address (e.g., `10.42.100.15`).
    **`error: invalid credentials provided`** — Verify the vSphere username and password are correct; use `--vsphere-username` with the full UPN format (e.g., `administrator@vsphere.local`).
    **`error: x509: certificate signed by unknown authority`** — Remove the `--insecure-skip-tls-verify` flag once you have a valid certificate, or ensure your CA certificate is in the system trust store.
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


```text title="Expected output"
Logged in successfully.

The current context is now "team-prod".
```

!!! warning "Common errors"
    **`error: You must be logged in to the server (Unauthorized)`** — Verify the supervisor VIP is correct and the vSphere credentials are valid; check that the user has permission to access the Supervisor Cluster.
    **`error: context "team-prod" does not exist`** — List available contexts with `kubectl config get-contexts` and use the correct namespace name from the output.
### List Available TKG Releases

```bash
# Show available TanzuKubernetesRelease images in the content library
kubectl get tanzukubernetesrelease
# Choose a TKR from this list for the cluster manifest below
```


```text title="Expected output"
NAME                                    VERSION        READY   REASON
v1.24.9---vmware.1-tkg.1-tiny           1.24.9         True    
v1.25.7---vmware.1-tkg.1-small          1.25.7         True    
v1.26.5---vmware.1-tkg.1-medium         1.26.5         True    
v1.27.2---vmware.1-tkg.1-large          1.27.2         True    
v1.28.1---vmware.1-tkg.1-xlarge         1.28.1         False   ImageNotReady
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "tanzukubernetesrelease"`** — Ensure the Tanzu Kubernetes Grid management cluster is properly initialized with `tanzu management-cluster create` and the required CRDs are installed.
    **`No resources found in default namespace.`** — Switch to the correct namespace where TanzuKubernetesRelease objects exist, typically `tkg-system`, using `kubectl config set-context --current --namespace=tkg-system`.
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


```text title="Expected output"
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
tanzukubernetescluster.run.tanzu.vmware.com/prod-cluster created
```

!!! warning "Common errors"
    **`error: unable to recognize "prod-cluster.yaml": no matches for kind "TanzuKubernetesCluster" in version "run.tanzu.vmware.com/v1alpha3"`** — Verify the Tanzu Kubernetes Grid management cluster is properly initialized and the TKG CRDs are installed with `kubectl get crds | grep tanzu`.
    **`The namespace "team-prod" does not exist`** — Create the namespace first with `kubectl create namespace team-prod`.
    **`vmClass "best-effort-medium" not found`** — Verify available VM classes in your Supervisor Cluster with `kubectl get vmclass` and use an existing class name.
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


```text title="Expected output"
NAME           PHASE         READY   TKR NAME                    AGE
prod-cluster   Provisioning  False   v1.27.5---vmware.2-tkg.1    2m
prod-cluster   Provisioning  False   v1.27.5---vmware.2-tkg.1    5m
prod-cluster   Ready         True    v1.27.5---vmware.2-tkg.1    18m

NAME                                    PHASE     VERSION
prod-cluster-control-plane-2xk9f        Running   v1.27.5
prod-cluster-md-0-5d8c4f7b9-lm2pq       Running   v1.27.5
prod-cluster-md-0-5d8c4f7b9-n8qvx       Running   v1.27.5

Logged in successfully to supervisor cluster 10.20.1.50 as administrator@vsphere.local
Switched to context prod-cluster

NAME                             STATUS   ROLES           AGE   VERSION
prod-cluster-control-plane-2xk9f Ready    control-plane   16m   v1.27.5
prod-cluster-md-0-5d8c4f7b9-lm2pq Ready    <none>          14m   v1.27.5
prod-cluster-md-0-5d8c4f7b9-n8qvx Ready    <none>          14m   v1.27.5
```

!!! warning "Common errors"
    **`error: unable to connect to the server: dial tcp 10.20.1.50:6443: i/o timeout`** — Verify the supervisor-VIP is reachable and the vSphere control plane is healthy; check network connectivity and firewall rules.
    **`error: x509: certificate signed by unknown authority`** — Remove the `--insecure-skip-tls-verify` flag once a valid certificate is installed, or ensure your CA bundle is properly configured in kubeconfig.
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


```text title="Expected output"
{"project_id":100,"project_name":"team-prod","public":false,"creation_time":"2024-01-15T09:42:33.521Z","update_time":"2024-01-15T09:42:33.521Z"}
{"id":23,"name":"ci-pipeline","description":"CI push account","secret":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...","creation_time":"2024-01-15T09:43:12.847Z","expires_at":-1}
```

!!! warning "Common errors"
    **`{"errors":[{"code":"CONFLICT","message":"Project name already exists"}]}`** — Check if the project exists with `curl -u admin:<password> https://harbor.example.local/api/v2.0/projects?name=team-prod` and use a different name or delete the existing project first.
    **`{"errors":[{"code":"UNAUTHORIZED","message":"Unauthorized"}]}`** — Verify the admin password is correct and URL is accessible; test connectivity with `curl -k https://harbor.example.local/api/v2.0/health`.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification for self-signed certs, or import the Harbor CA certificate into your system trust store.
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


```text title="Expected output"
Switched to context "prod-cluster".
NAME                    STATUS   ROLES           AGE   VERSION        INTERNAL-IP      EXTERNAL-IP   OS-IMAGE
prod-worker-01          Ready    worker          45d   v1.28.4         10.20.15.42      <none>        VMware Photon OS/Linux
prod-worker-02          Ready    worker          45d   v1.28.4         10.20.15.43      <none>        VMware Photon OS/Linux
prod-worker-03          Ready    worker          44d   v1.28.4         10.20.15.44      <none>        VMware Photon OS/Linux
prod-control-plane-01   Ready    control-plane   45d   v1.28.4         10.20.15.40      <none>        VMware Photon OS/Linux
prod-control-plane-02   Ready    control-plane   45d   v1.28.4         10.20.15.41      <none>        VMware Photon OS/Linux
NAMESPACE     NAME                                    READY   STATUS      RESTARTS   AGE
kube-system   coredns-5d78c0869f-2k8xm               1/1     Completed   0          45d
kube-system   etcd-prod-control-plane-01             1/1     Running     2          45d
```

!!! warning "Common errors"
    **`error: context "prod-cluster" does not exist`** — Run `kubectl config get-contexts` to list available contexts and use the correct name.
    **`Unable to connect to the server: dial tcp 10.20.15.40:6443: connection refused`** — Verify the control plane nodes are running and network connectivity exists; check `kubectl cluster-info` for endpoint status.
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


```text title="Expected output"
persistentvolumeclaim/pvc-test created
NAME       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc-test   Bound    pvc-1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p   5Gi        RWO            vsan-default   2s
persistentvolumeclaim "pvc-test" deleted
```

!!! warning "Common errors"
    **`Error from server (NotFound): error when retrieving current configuration of the object before updating: persistentvolumeclaims "pvc-test" is not found`** — Ensure the namespace is correct and the PVC was successfully created before attempting to delete it.
    **`storageclass.storage.k8s.io "vsan-default" not found`** — Verify the storage class exists in your cluster with `kubectl get storageclass` and update the `storageClassName` field accordingly.
    **`PersistentVolumeClaim is in use by pod`** — Delete any pods using the PVC before attempting to delete the claim, or use `kubectl delete pvc pvc-test --grace-period=0 --force` if necessary.
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


```text title="Expected output"
Login Succeeded
latest: Pulling from library/alpine
Digest: sha256:eece025e432126ce23f223450a0326fbebde39cba518d143f6b05a849d08ce1f
Status: Downloaded newer image for alpine:latest
(no output — command completes silently)
(no output — command completes silently)
The push refers to repository [harbor.example.local/team-prod/alpine]
test: digest: sha256:9c6e40b8664f8e1f4b3d7a2c9e5f1d8a4b6c2e9f1a3d5b7c9e2f4a6b8d0e1f3 size: 528
Digest: sha256:9c6e40b8664f8e1f4b3d7a2c9e5f1d8a4b6c2e9f1a3d5b7c9e2f4a6b8d0e1f3
```

!!! warning "Common errors"
    **`Error response from daemon: Get "https://harbor.example.local/v2/": x509: certificate signed by unknown authority`** — Add Harbor's CA certificate to your Docker daemon trust store or use `--insecure-registry` if testing in non-production.
    **`denied: requested access to the resource is denied`** — Verify the robot account token is correct and has push permissions on the `team-prod` project in Harbor.
    **`Error response from daemon: Get "https://harbor.example.local/v2/team-prod/alpine/manifests/test": unauthorized: unauthorized to access repository`** — Confirm you are logged in with `docker login` and the robot account has the correct role (Developer or higher) assigned to the team-prod project.
### Network Policy Test

```bash
# Confirm Antrea/NSX CNI is running
kubectl get pods -n kube-system | grep -E 'antrea|ncp'

# Verify Supervisor API still reachable from within cluster
kubectl run nettest --image=alpine --restart=Never --rm -it -- \
  wget -qO- https://<supervisor-VIP>:443/api/
```


```text title="Expected output"
NAME                                    READY   STATUS    RESTARTS   AGE
antrea-agent-2k8xj                      2/2     Running   0          14d
antrea-agent-5lmqp                      2/2     Running   0          14d
antrea-agent-9vwkl                      2/2     Running   0          14d
antrea-controller-0                     1/1     Running   0          14d
antrea-controller-1                     1/1     Running   0          14d
antrea-controller-2                     1/1     Running   0          14d
pod/nettest created
{
  "kind": "APIVersions",
  "versions": ["v1"],
  "serverAddressByClientCIDRs": [{"clientCIDR": "0.0.0.0/0", "serverAddress": "192.168.1.50:443"}]
}
pod "nettest" deleted
```

!!! warning "Common errors"
    **`error: no matching resources found`** — Verify Antrea is installed on the cluster with `kubectl get ns kube-system` and check the CNI plugin deployment status.
    **`Connection timed out`** — Confirm the Supervisor VIP is reachable from worker nodes by replacing `<supervisor-VIP>` with the actual IP and testing with `ping` from a node first.
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

---

## See also

- [Tanzu — How It Works](../architecture/how-it-works/)
- [Tanzu — Health Checks](../operations/health-checks/)
- [Virtualization Vmware Tanzu — Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
