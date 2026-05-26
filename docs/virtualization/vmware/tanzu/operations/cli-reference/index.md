# Tanzu — CLI Reference

---

## tanzu CLI

```bash
# Install tanzu CLI (Linux)
curl -sL https://github.com/vmware-tanzu/tanzu-framework/releases/download/v<version>/tanzu-linux-amd64.tar.gz | tar xz
sudo install tanzu /usr/local/bin/tanzu

# Install required plugins
tanzu plugin sync

# Check version
tanzu version
tanzu plugin list
```

---

## Tanzu Cluster Operations

```bash
# List management clusters
tanzu management-cluster get

# Create a workload cluster (from cluster config YAML)
tanzu cluster create my-workload-cluster --file cluster-config.yaml

# List workload clusters
tanzu cluster list --include-management-cluster

# Get cluster details
tanzu cluster get my-workload-cluster

# Get kubeconfig for a workload cluster
tanzu cluster kubeconfig get my-workload-cluster --admin
# Writes kubeconfig to ~/.kube/config (or merge with KUBECONFIG env var)

# Scale worker nodes
tanzu cluster scale my-workload-cluster --worker-machine-count 5

# Upgrade a workload cluster
tanzu cluster upgrade my-workload-cluster

# Delete a workload cluster
tanzu cluster delete my-workload-cluster --yes
```

---

## kubectl for Supervisor (vSphere with Tanzu)

```bash
# Login to Supervisor cluster
kubectl vsphere login \
  --server https://supervisor.example.local \
  --username administrator@vsphere.local \
  --vsphere-username administrator@vsphere.local \
  --insecure-skip-tls-verify

# List Supervisor namespaces (vSphere Namespaces)
kubectl get namespaces

# Switch context to a Supervisor namespace
kubectl config use-context <namespace>

# List TanzuKubernetesCluster objects in a Supervisor namespace
kubectl get tanzukubernetescluster -n <namespace>

# Deploy a TKG cluster via CRD
kubectl apply -f tkc-cluster.yaml
```

---

## kubectl Workload Cluster Operations

```bash
# Switch context to a workload cluster
kubectl config use-context <workload-cluster-context>

# Get cluster nodes and status
kubectl get nodes -o wide

# Get all pods across all namespaces
kubectl get pods -A

# Check node resource usage (requires metrics-server)
kubectl top nodes
kubectl top pods -A

# Get events sorted by timestamp (useful for debugging)
kubectl get events -A --sort-by='.lastTimestamp'

# Drain a node for maintenance
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Uncordon after maintenance
kubectl uncordon <node-name>
```

---

## Carvel Tools (used by Tanzu)

```bash
# kapp — deploy and track application resources
kapp deploy -a my-app -f ./manifests/ --yes
kapp list
kapp delete -a my-app --yes

# ytt — YAML templating
ytt -f values.yaml -f config/ > rendered.yaml

# imgpkg — package and relocate container images
imgpkg push -b harbor.example.local/tanzu/my-bundle:v1.0 -f ./bundle/
imgpkg pull -b harbor.example.local/tanzu/my-bundle:v1.0 -o ./output/

# vendir — sync external content
vendir sync
```

---

## Harbor CLI

```bash
# Push an image to Harbor
docker login harbor.example.local -u admin -p <password>
docker tag myapp:v1.0 harbor.example.local/myproject/myapp:v1.0
docker push harbor.example.local/myproject/myapp:v1.0

# Pull an image
docker pull harbor.example.local/myproject/myapp:v1.0

# Harbor API — list projects
curl -sk -u admin:<password> \
  "https://harbor.example.local/api/v2.0/projects" | python3 -m json.tool

# Harbor API — list repositories in a project
curl -sk -u admin:<password> \
  "https://harbor.example.local/api/v2.0/projects/myproject/repositories" | python3 -m json.tool
```

---

## Velero CLI (Backup)

```bash
# List backups
velero backup get

# Create on-demand backup
velero backup create my-backup --include-namespaces production

# List restores
velero restore get

# Restore from backup
velero restore create --from-backup my-backup

# Check Velero status
velero version
kubectl get pods -n velero
```
