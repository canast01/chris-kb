---
tags:
  - architecture
  - tanzu
  - vmware
description: "Integrations reference covering vCenter Integration, NSX-T Integration, AVI (NSX Advanced Load Balancer) Integration, vSAN Integration, Active Directory /..."
---
# Tanzu — Integrations

<div class="kb-summary">
Integrations reference covering vCenter Integration, NSX-T Integration, AVI (NSX Advanced Load Balancer) Integration, vSAN Integration, Active Directory / LDAP Integration and 3 more sections.

*Applies to: Tanzu 2.x*
</div>
![Tanzu — Integrations](../../../../../assets/virtualization-vmware-tanzu-architecture-integrations.svg)

## vCenter Integration

Workload Management is a vCenter Server feature. The Supervisor cluster lifecycle — enable, upgrade, configure — is managed entirely through vCenter APIs or the vSphere UI.

### Enable via vCenter UI

**Workload Management → Get Started → vSphere Distributed Switch or NSX-T**

Prerequisites before enabling:
- vSphere 7.0 U1+ or vSphere 8.x
- vCenter and all ESXi hosts on the same major version
- Cluster has at least 3 ESXi hosts (for Supervisor control plane VM anti-affinity)
- vSAN or external shared storage configured
- NSX-T 3.x+ deployed and connected to vCenter, OR AVI Controller deployed
- DNS forward/reverse records for Supervisor control plane VIP
- NTP synchronized across vCenter, ESXi, and NSX/AVI

### Enable via vCenter API

```bash
# Get the cluster MoRef
curl -sk -u administrator@vsphere.local:VMware1! \
  "https://vcenter.example.com/rest/vcenter/cluster" | jq '.value[] | {name,cluster}'

# Enable Workload Management (REST API)
curl -sk -u administrator@vsphere.local:VMware1! \
  -X POST \
  -H "Content-Type: application/json" \
  "https://vcenter.example.com/api/vcenter/namespace-management/clusters/domain-c8:action=enable" \
  -d @enable-wm-payload.json
```

```json
{
  "size_hint": "MEDIUM",
  "network_provider": "NSXT_CONTAINER_PLUGIN",
  "ncp_cluster_network_spec": {
    "pod_cidrs": [{"address": "100.64.0.0", "prefix": 16}],
    "ingress_cidrs": [{"address": "10.50.0.0", "prefix": 24}],
    "egress_cidrs": [{"address": "10.51.0.0", "prefix": 24}],
    "cluster_distributed_switch": "dvs-1",
    "nsx_edge_cluster": "edge-cluster-1"
  },
  "workload_networks_spec": {
    "supervisor_primary_workload_network": {
      "network_provider": "NSXT_CONTAINER_PLUGIN",
      "nsx_network_spec": {
        "vsphere_portgroup_gateways": []
      }
    }
  },
  "service_cidr": {"address": "10.96.0.0", "prefix": 16},
  "master_management_network": {
    "mode": "STATICRANGE",
    "address_range": {
      "starting_address": "10.10.10.20",
      "gateway": "10.10.10.1",
      "subnet_mask": "255.255.255.0",
      "address_count": 5,
      "dns_search_domains": ["example.com"],
      "dns_servers": ["10.10.10.5"]
    },
    "network": "dvportgroup-management"
  },
  "master_ntp_servers": ["10.10.10.5"],
  "master_storage_policy": "vSAN Default Storage Policy",
  "ephemeral_storage_policy": "vSAN Default Storage Policy",
  "login_banner": "Authorized use only",
  "master_dns_servers": ["10.10.10.5"],
  "master_dns_search_domains": ["example.com"]
}
```

---

## NSX-T Integration

NSX-T is the recommended networking provider for vSphere with Tanzu. It supplies both overlay networking and load balancing for the Supervisor and workload clusters.

### Required NSX-T Objects

| Object | Purpose |
|---|---|
| T0 Gateway | North-south routing, BGP to physical network |
| T1 Gateway | Per-namespace or shared L3 gateway |
| Transport Zone (overlay) | Geneve encapsulation domain |
| Uplink Profile | VLAN configuration for physical NICs |
| IP Pool (Supervisor Management) | IPs for Supervisor control plane VMs |
| IP Pool (Ingress) | VIPs for K8s `Service type: LoadBalancer` |
| IP Pool (Egress) | SNAT IPs for pods egressing the cluster |
| Edge Cluster | NSX Edge nodes for N-S traffic and LB |
| Load Balancer Service | NSX-T LB bound to T1, services Supervisor API VIP |

### NSX Container Plugin (NCP)

NCP runs as a pod in the Supervisor cluster (`kube-system` namespace) and bridges K8s and NSX-T:

```bash
# Check NCP status on Supervisor
kubectl get pods -n kube-system | grep ncp

# NCP logs
kubectl logs -n kube-system nsx-ncp-<hash> --tail=100

# NCP ConfigMap
kubectl get configmap -n kube-system nsx-ncp-config -o yaml
```


```text title="Expected output"
nsx-ncp-7d4f2k9m                           1/1     Running   0          12d
nsx-ncp-7d4f2k9m-metrics                   1/1     Running   0          12d

2024-01-15T08:42:33.123Z [INFO] NCP initialized successfully
2024-01-15T08:42:35.456Z [INFO] Connected to NSX Manager at 192.168.1.50:443
2024-01-15T08:42:37.789Z [INFO] Cluster UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
2024-01-15T08:42:40.012Z [INFO] Syncing logical switches for 3 namespaces
2024-01-15T08:42:42.345Z [INFO] Container networking policy enforcement enabled
2024-01-15T08:42:45.678Z [INFO] Health check passed: NSX connectivity OK

apiVersion: v1
kind: ConfigMap
metadata:
  name: nsx-ncp-config
  namespace: kube-system
data:
  ncp.ini: |
    [DEFAULT]
    nsx_api_managers = 192.168.1.50
    nsx_username = admin
    cluster = supervisor-cluster-1
    [coe]
    cluster_name = supervisor-cluster-1
    enable_snat = True
    container_ip_block_id = 550e8400-e29b-41d4-a716-446655440000
```

!!! warning "Common errors"
    **`error: pods "nsx-ncp-<hash>" not found`** — Replace `<hash>` with the actual pod hash from the first command output (e.g., `nsx-ncp-7d4f2k9m`).
    **`Error from server (NotFound): configmaps "nsx-ncp-config" not found`** — Verify NCP is installed in the Supervisor cluster and check the correct namespace with `kubectl get configmap -A | grep ncp`.
NCP translates:
- `NetworkPolicy` → NSX Distributed Firewall rules
- `Service type: LoadBalancer` → NSX Virtual Server + Pool
- `Namespace` creation → NSX Segment + T1 (if namespace isolation enabled)

### NSX-T Load Balancer Sizing

| Size | Virtual Servers | Pools | Members per Pool |
|---|---|---|---|
| Small | 10 | 40 | 40 |
| Medium | 100 | 400 | 400 |
| Large | 1000 | 4000 | 4000 |

The NSX LB size is set when enabling Workload Management (`size_hint` field) and applies per Supervisor cluster.

---

## AVI (NSX Advanced Load Balancer) Integration

AVI is the alternative to NSX-T for environments with standard VDS networking. AVI provides only L4/L7 load balancing — pod networking still uses VDS segments.

### AVI Kubernetes Operator (AKO)

AKO runs in the `avi-system` namespace of each TKG cluster and syncs K8s objects to AVI:

```bash
# Check AKO deployment
kubectl get pods -n avi-system
kubectl logs -n avi-system ako-0 --tail=100

# AKO ConfigMap (key settings)
kubectl get configmap -n avi-system avi-k8s-config -o yaml
```


```text title="Expected output"
NAME                                READY   STATUS    RESTARTS   AGE
ako-0                               1/1     Running   0          45d
avi-controller-0                    1/1     Running   0          45d
avi-controller-1                    1/1     Running   0          45d
avi-controller-2                    1/1     Running   0          45d

2024-01-15T14:32:18.456Z [INFO] AKO initialized successfully
2024-01-15T14:32:19.123Z [INFO] Connected to Avi Controller at 10.50.100.50
2024-01-15T14:32:20.789Z [INFO] Cluster name: tanzu-prod-01
2024-01-15T14:32:21.234Z [INFO] Service Engine Group: Default-Group
2024-01-15T14:32:22.567Z [INFO] Syncing ingress resources from cluster
2024-01-15T14:32:23.891Z [INFO] Registered 3 LoadBalancer services
2024-01-15T14:32:24.445Z [INFO] AKO controller loop running

apiVersion: v1
kind: ConfigMap
metadata:
  name: avi-k8s-config
  namespace: avi-system
data:
  avi_controller: "10.50.100.50"
  avi_username: "admin"
  avi_password: "***"
  cluster_name: "tanzu-prod-01"
  service_engine_group: "Default-Group"
  network_name: "k8s-vip-network"
  subnet_ip: "10.60.0.0"
  subnet_prefix: "24"
  log_level: "INFO"
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "configmap" in API group ""`** — Verify the namespace exists with `kubectl get ns avi-system` and ensure AKO is installed via Helm.
    **`Error from server (NotFound): pods "ako-0" not found`** — Check that the AKO pod is running with `kubectl get pods -n avi-system` and verify the deployment completed successfully.
Key AKO settings:

```yaml
# avi-k8s-config ConfigMap excerpt
controllerIP: "avi-controller.example.com"
serviceEngineGroupName: "Default-Group"
cloudName: "Default-Cloud"
clusterName: "prod-k8s"               # prefix for AVI object names
defaultIngClassAVI: "true"             # AVI handles default IngressClass
l7Settings:
  defaultIngController: true
  serviceType: NodePortLocal           # or ClusterIP with IPVS
networkSettings:
  nodeNetworkList:
  - networkName: "K8s-Nodes-Network"
    cidrs:
    - "10.20.0.0/24"
```

### AVI Service Engine Placement

```text
AVI Controller (VM — 3 nodes for HA)
  └── Service Engine Group
        ├── Service Engine 1 (VM on ESXi host 1)
        ├── Service Engine 2 (VM on ESXi host 2)
        └── Service Engine N
              └── Virtual Services (VIPs mapped to K8s Services)
```

---

## vSAN Integration

vSAN provides the primary storage backing for K8s persistent volumes in most vSphere with Tanzu deployments.

### Storage Policy to StorageClass Mapping

Each vSAN storage policy defined in vCenter can be mapped to a K8s StorageClass:

```yaml
# StorageClass referencing vSAN policy by name
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: vsan-raid1-encrypted
provisioner: csi.vsphere.vmware.com
parameters:
  storagepolicyname: "vSAN RAID-1 Encrypted"
  csi.storage.k8s.io/fstype: ext4
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

### vSAN Storage Policy Design for K8s

| Policy Name | FTT | RAID | Encryption | Use Case |
|---|---|---|---|---|
| vsan-default | 1 | RAID-1 | No | General workloads |
| vsan-ha | 2 | RAID-1 | No | Databases, stateful apps |
| vsan-encrypted | 1 | RAID-1 | Yes (vSAN) | Regulated data |
| vsan-perf | 1 | RAID-5 | No | High IOPS, capacity-efficient |

### CSI Driver Health Check

```bash
# Verify vSphere CSI driver pods
kubectl get pods -n vmware-system-csi

# CSI node driver logs (per node)
kubectl logs -n vmware-system-csi vsphere-csi-node-<hash> -c vsphere-csi-node

# CSI controller logs
kubectl logs -n vmware-system-csi vsphere-csi-controller-<hash> -c vsphere-csi-controller

# Check CSI driver version
kubectl get csidriver csi.vsphere.vmware.com -o jsonpath='{.metadata.annotations}'
```


```text title="Expected output"
NAME                                       READY   STATUS    RESTARTS   AGE
vsphere-csi-controller-0                   6/6     Running   0          14d
vsphere-csi-node-4k8xj                     3/3     Running   2          14d
vsphere-csi-node-7m2pq                     3/3     Running   1          14d
vsphere-csi-node-9n5kr                     3/3     Running   0          14d
vsphere-csi-syncer-0                       1/1     Running   0          14d

I1215 09:42:33.521847       1 utils.go:89] CSI node driver initialized
I1215 09:42:35.234521       1 node.go:156] Node ID: vm-worker-02.corp.local
I1215 09:42:40.891234       1 csi.go:412] Volume attach successful: pvc-a7f3e2c1-9b4d-4e8f-b2a1-5c8d9e3f2a1b
I1215 09:43:12.456789       1 node.go:203] Mount operation completed for /var/lib/kubelet/plugins/csi.vsphere.vmware.com/pv/pvc-a7f3e2c1-9b4d-4e8f-b2a1-5c8d9e3f2a1b

I1215 09:41:22.123456       1 controller.go:78] CSI controller driver initialized
I1215 09:41:25.654321       1 manager.go:234] Syncing volume metadata with vSphere
I1215 09:41:30.987654       1 provisioner.go:445] Volume provisioning request received: size=50Gi, storageClass=vsphere-sc-default
I1215 09:41:35.345678       1 attacher.go:312] Attach operation queued for node: vm-worker-01.corp.local

{"csi.vsphere.vmware.com/version":"v2.7.1","csi.vsphere.vmware.com/build":"20231201.001"}
```

!!! warning "Common errors"
    **`Error from server (NotFound): pods "vsphere-csi-node-<hash>" not found`** — Replace `<hash>` with the actual pod hash from the first command output (e.g., `vsphere-csi-node-4k8xj`).
    **`error: the server doesn't have a resource type "csidriver"`** — Verify the Kubernetes API server supports CSIDriver resources (requires Kubernetes 1.12+) and check RBAC permissions for the current user.
---

## Active Directory / LDAP Integration

### Pinniped — K8s Authentication Federation

Pinniped provides OIDC/LDAP authentication for TKG workload clusters. The Pinniped Supervisor (a separate K8s deployment, often on the management cluster) federates external identity providers and issues cluster-scoped tokens.

```text
User → kubectl → kubeconfig (OIDC issuer = Pinniped Supervisor)
  └── Pinniped Concierge (runs in workload cluster)
        └── Token exchange → Pinniped Supervisor
              └── Dex (OIDC broker)
                    └── LDAP / AD / OIDC IdP
```

### LDAP Configuration via Dex

```yaml
# Dex LDAP connector config (in Pinniped FederationDomain)
connectors:
- type: ldap
  id: ldap
  name: Corporate LDAP
  config:
    host: ldap.example.com:636
    insecureNoSSL: false
    rootCAData: <base64-encoded-CA>
    bindDN: cn=svc-dex,ou=service,dc=example,dc=com
    bindPW: $LDAP_BIND_PW
    usernamePrompt: Username
    userSearch:
      baseDN: ou=users,dc=example,dc=com
      filter: (objectClass=person)
      username: sAMAccountName
      idAttr: DN
      emailAttr: mail
      nameAttr: cn
    groupSearch:
      baseDN: ou=groups,dc=example,dc=com
      filter: (objectClass=groupOfNames)
      userMatchers:
      - userAttr: DN
        groupAttr: member
      nameAttr: cn
```

### OIDCIdentityProvider (Pinniped CRD)

```yaml
apiVersion: idp.supervisor.pinniped.dev/v1alpha1
kind: OIDCIdentityProvider
metadata:
  name: corporate-oidc
  namespace: pinniped-supervisor
spec:
  issuer: https://dex.example.com
  authorizationConfig:
    additionalScopes: [groups, email]
    allowPasswordGrant: false
  claims:
    groups: groups
    username: email
  client:
    secretName: corporate-oidc-client-secret
```

### Supervisor Authentication (vCenter SSO)

The Supervisor cluster API is authenticated via vCenter SSO directly — no Pinniped needed for Supervisor itself:

```bash
kubectl vsphere login \
  --server=https://supervisor-vip.example.com \
  --vsphere-username=administrator@vsphere.local \
  --insecure-skip-tls-verify   # only if cert not trusted locally
```


```text title="Expected output"
Logged in successfully.

Context "supervisor-vip.example.com" created.

You have access to the following contexts:
   supervisor-vip.example.com

Current context is now "supervisor-vip.example.com".
```

!!! warning "Common errors"
    **`error: error validating the path to a credential file`** — Ensure `kubectl vsphere` plugin is installed via `kubectl krew install vsphere` and your kubeconfig directory exists.
    **`error: x509: certificate signed by unknown authority`** — Remove the `--insecure-skip-tls-verify` flag and install the vSphere supervisor cluster's CA certificate in your system trust store, or keep the flag only for non-production testing.
    **`error: invalid credentials`** — Verify the vSphere username and password are correct; use `--password` flag or enter interactively when prompted, and confirm the account has Kubernetes cluster admin permissions.
---

## Harbor Registry Integration

### Pull-Through Cache (Proxy Cache)

Configure Harbor to proxy upstream registries so air-gapped or rate-limited environments can transparently pull images:

```text
Developer/CI pulls: harbor.example.com/dockerhub-proxy/library/nginx:latest
  └── Harbor checks local cache
        ├── Cache hit → serve from Harbor
        └── Cache miss → pull from Docker Hub, cache, serve
```

Configuration:
1. Harbor UI → Administration → Registries → New Endpoint
   - Provider: Docker Hub (or GCR, ECR, Quay, etc.)
   - Name: `docker-hub`
   - Endpoint URL: `https://hub.docker.com`
   - Access credentials (optional, for authenticated pull)
2. Harbor UI → New Project → Check "Proxy Cache" → Select `docker-hub` endpoint
3. Project name becomes the pull path prefix (e.g., `dockerhub-proxy`)

### Vulnerability Scanning with Trivy

```bash
# Harbor 2.x uses Trivy by default
# Enable auto-scan on push: Project → Configuration → "Automatically scan images on push"

# Manual scan trigger via API
curl -u admin:Harbor12345 -X POST \
  "https://harbor.example.com/api/v2.0/projects/myproject/repositories/myapp/artifacts/sha256:abc123/scan"

# Get scan report
curl -u admin:Harbor12345 \
  "https://harbor.example.com/api/v2.0/projects/myproject/repositories/myapp/artifacts/sha256:abc123/additions/vulnerabilities" \
  | jq '.["application/vnd.scanner.adapter.vuln.report.harbor+json; version=1.0"].vulnerabilities[] | select(.severity=="Critical")'
```


```text title="Expected output"
{
  "id": "sha256:abc123",
  "scan_status": "Success",
  "scan_status_code": 200,
  "scan_status_description": "The artifact has been scanned",
  "scan_status_revision": 1
}
{
  "id": "CVE-2024-1234",
  "package": "openssl",
  "package_version": "1.1.1k-1",
  "vulnerability_id": "CVE-2024-1234",
  "severity": "Critical",
  "fixed_version": "1.1.1m-1",
  "description": "Buffer overflow in X.509 certificate parsing"
}
{
  "id": "CVE-2024-5678",
  "package": "glibc",
  "package_version": "2.31-13",
  "vulnerability_id": "CVE-2024-5678",
  "severity": "Critical",
  "fixed_version": "2.31-14",
  "description": "Heap corruption in malloc implementation"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl or import the Harbor CA certificate into your system trust store.
    **`{"errors":[{"code":"UNAUTHORIZED","message":"Unauthorized"}]}`** — Verify Harbor admin credentials are correct and the user has project access; check if the password contains special characters requiring URL encoding.
    **`jq: error (at <stdin>:1): Cannot index object with string "application/vnd.scanner.adapter.vuln.report.harbor+json; version=1.0"`** — Ensure the artifact scan has completed successfully by checking `scan_status` is "Success" before querying vulnerabilities.
### Block Images with Critical CVEs (Replication and Deploy Gate)

```text
Harbor Project → Configuration → Deployment Security → Severity: Critical
→ Prevents images with unscanned or Critical CVEs from being pulled
→ Effective for all users except Project Admin
```

---

## Aria Operations (vROps) Integration for Tanzu

VMware Aria Operations (formerly vROps) can monitor TKG workload clusters via the Kubernetes Management Pack.

### Configure Kubernetes Management Pack

1. Aria Operations → Administration → Repository → Add Management Pack: Kubernetes
2. Add Adapter Instance:
   - Cluster API endpoint: `https://tkc-api.example.com:6443`
   - Service account token: created in workload cluster with cluster-reader role
   - CA certificate of the cluster API

```bash
# Create read-only service account for Aria Operations
kubectl create serviceaccount aria-ops-reader -n kube-system
kubectl create clusterrolebinding aria-ops-reader \
  --clusterrole=view \
  --serviceaccount=kube-system:aria-ops-reader

# Get token (K8s 1.24+)
kubectl create token aria-ops-reader -n kube-system --duration=87600h
```


```text title="Expected output"
serviceaccount/aria-ops-reader created
clusterrolebinding.rbac.authorization.k8s.io/aria-ops-reader created
eyJhbGciOiJIUzI1NiIsImtpZCI6IjEyMzQ1Njc4OTBhYmNkZWYifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZWFjY291bnQubmFtZSI6ImFyaWEtb3BzLXJlYWRlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZWFjY291bnQudWlkIjoiYTJmNDZkYzItNzc5Yi00YzQ1LWI4ZDItOGY5YzFhMmI0ZTU5In0.rZ9KqX_vL2mN8pQ3wT6xY_jK4sA9bC5dE7fG2hI0jL
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "token"`** — Upgrade to Kubernetes 1.24+ or use `kubectl get secret -n kube-system $(kubectl get secret -n kube-system | grep aria-ops-reader-token | awk '{print $1}') -o jsonpath='{.data.token}' | base64 -d` for older versions.
    **`Error from server (AlreadyExists): serviceaccounts "aria-ops-reader" already exists`** — Delete the existing service account with `kubectl delete serviceaccount aria-ops-reader -n kube-system` before recreating it.
Aria Operations collects: node CPU/memory/disk, pod status, PVC usage, K8s events, namespace resource consumption.

---

## Tanzu Observability (Wavefront) Integration

Tanzu Observability (now Aria Operations for Applications / Wavefront) collects metrics from TKG clusters via the Wavefront Proxy:

```bash
# Deploy Wavefront Proxy and Collector via Helm
helm repo add wavefront https://wavefronthq.github.io/helm/
helm repo update

helm install wavefront wavefront/wavefront \
  --namespace wavefront \
  --create-namespace \
  --set wavefront.url=https://longboard.wavefront.com \
  --set wavefront.token=<your-api-token> \
  --set clusterName=prod-k8s \
  --set collector.discovery.enabled=true
```

```yaml
# Wavefront Helm values for full K8s metrics
collector:
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
  discovery:
    enabled: true
    annotationPrefix: "prometheus.io"
    enableRuntimeConfigs: true
proxy:
  replicas: 2
  resources:
    limits:
      cpu: 1000m
      memory: 2Gi
```

Key metrics collected: K8s node CPU/mem/disk, pod resource usage, JVM metrics (via Prometheus annotations), custom app metrics via Prometheus scraping through Wavefront proxy.

## See also

- [Tanzu — How It Works](../how-it-works/)
- [Tanzu — Deploy](../../deploy/)
