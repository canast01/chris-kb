---
tags:
  - tanzu
  - kubernetes
---
# Tanzu Cheat Sheet

<div class="kb-summary">
Top-10 Tanzu commands for cluster lifecycle, package management, and Kubernetes operations in TKG environments.
</div>
![Tanzu Cheat Sheet](../../assets/reference-cheat-sheets-tanzu.svg)




## Tanzu CLI

```bash
tanzu version                                          # CLI and plugin versions
tanzu plugin list                                      # installed plugins and status
tanzu management-cluster get                           # management cluster status
tanzu cluster list --include-management-cluster        # all clusters

# Cluster lifecycle
tanzu cluster create my-cluster -f cluster.yaml        # create workload cluster
tanzu cluster delete my-cluster                        # delete workload cluster
tanzu cluster scale my-cluster --worker-machine-count 5   # scale workers

# Packages
tanzu package repository list -A                       # package repositories
tanzu package available list -A                        # available packages
tanzu package installed list -A                        # installed packages
tanzu package install cert-manager \
  --package-name cert-manager.tanzu.vmware.com \
  --version 1.7.2+vmware.1 -n tkg-packages            # install a package
```

## TKGs (vSphere with Tanzu — Supervisor kubeconfig)

```bash
# Login to Supervisor (TKGs)
kubectl vsphere login --server <supervisor-ip> --vsphere-username admin@vsphere.local

# Namespace and cluster ops
kubectl get ns                                         # namespaces (vSphere namespaces)
kubectl get tkc -n my-ns                               # TanzuKubernetesCluster objects
```

## See also

- [Tanzu Operations](../../virtualization/vmware/tanzu/operations/procedures/)
- [Tanzu Troubleshooting](../../virtualization/vmware/tanzu/troubleshooting/common-issues/)
