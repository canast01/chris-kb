# AKS

> Part of the Azure CLI Reference.

```text
┌───────────────────────────────────────────────────────────┐
│                    AKS CLI Flow                           │
│                                                           │
│  az aks create          ┌─────────────────────────────┐   │
│  ──────────────────────►│  AKS Cluster                │   │
│                         │  (managed control plane)    │   │
│  az aks show            └──────────────┬──────────────┘   │
│  az aks upgrade                        │                  │
│  az aks scale                          ▼                  │
│                         ┌─────────────────────────────┐   │
│  az aks get-credentials │  Node Pool(s)               │   │
│  ──────────────────────►│  (VM scale sets)            │   │
│         │               └─────────────────────────────┘   │
│         │                                                 │
│         ▼                                                 │
│  ~/.kube/config updated                                   │
│         │                                                 │
│         ▼                                                 │
│  kubectl ──────────────► Kubernetes API ──► Workloads     │
└───────────────────────────────────────────────────────────┘
```

---

```bash
# Clusters
az aks list --output table
az aks show --resource-group <rg> --name <cluster>

# Credentials
az aks get-credentials --resource-group <rg> --name <cluster>
az aks get-credentials --resource-group <rg> --name <cluster> --admin

# Scale
az aks scale --resource-group <rg> --name <cluster> --node-count 5

# Upgrade
az aks get-upgrades --resource-group <rg> --name <cluster>
az aks upgrade --resource-group <rg> --name <cluster> --kubernetes-version <version>

# Node pools
az aks nodepool list --resource-group <rg> --cluster-name <cluster>
```
