# Tanzu — Integrations


<div class="kb-summary">
Integrations reference covering vCenter Integration, NSX-T Integration, AVI (NSX Advanced Load Balancer) Integration, vSAN Integration, Active Directory / LDAP Integration and 3 more sections.
</div>

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
