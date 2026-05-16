# Tanzu — Procedures

---

## Create a vSphere Namespace

```
vCenter → Workload Management → Namespaces → Create Namespace
  Cluster: select Supervisor cluster
  Name: team-alpha
  Description: Application namespace for Team Alpha

OR via kubectl:
```

```bash
kubectl vsphere login --server https://supervisor.corp.local \
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
kubectl vsphere login --server https://supervisor.corp.local \
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
curl -sk -X POST "https://harbor.corp.local/api/v2.0/projects" \
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
curl -sk -X POST "https://harbor.corp.local/api/v2.0/projects/team-alpha/members" \
  -u admin:<password> \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2,
    "member_group": {"group_name": "team-alpha-devs", "group_type": 1}
  }'
```

---

## Configure Pull-Through Cache in Harbor

```
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

Configure nodes to pull from Harbor instead of Docker Hub directly by setting imagePullPolicy and image names to use `harbor.corp.local/dockerhub-cache/` prefix.

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
    fqdn: myapp.corp.local
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
kubectl vsphere login --server https://supervisor.corp.local \
  --username user@corp.local \
  --tanzu-kubernetes-cluster-name my-cluster \
  --tanzu-kubernetes-cluster-namespace my-namespace
```

Kubeconfigs embed a token with a limited TTL — users need to re-login after expiry.
