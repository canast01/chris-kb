# Tanzu — Install and Upgrade

```text
┌──────────────── Tanzu Upgrade Sequence ────────────────────────────────────────┐
│                                                                                 │
│  Step 1: vCenter upgrade (if upgrading vSphere)                                │
│      │                                                                          │
│      ▼                                                                          │
│  Step 2: Supervisor upgrade                                                     │
│          (auto-managed by vCenter Lifecycle Manager after vCenter upgrade)      │
│      │                                                                          │
│      ▼                                                                          │
│  Step 3: TKG Management Cluster                                                 │
│          tanzu management-cluster upgrade                                        │
│      │                                                                          │
│      ▼                                                                          │
│  Step 4: TKG Workload Clusters (one at a time, rolling)                         │
│          tanzu cluster upgrade <name>                                            │
│          ┌──────────────────────────────────────────────────┐                  │
│          │ control plane nodes upgrade ► worker nodes roll  │                  │
│          │ (one node: cordon ► drain ► upgrade ► uncordon)  │                  │
│          └──────────────────────────────────────────────────┘                  │
│      │                                                                          │
│      ▼                                                                          │
│  Step 5: Harbor — redeploy from new OVA (preserve external DB + storage)        │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites for vSphere with Tanzu (Supervisor)

| Requirement | Detail |
|---|---|
| vSphere | 7.0 U3+ or 8.x |
| Storage | vSAN, NFS, or vSphere CSI-compatible storage |
| Networking | NSX-T 3.1+ OR AVI (NSX Advanced Load Balancer) |
| DNS | Forward/reverse DNS for Supervisor API VIP and control plane VMs |
| NTP | All hosts synchronized |
| License | vSphere with Tanzu license or Tanzu Standard/Advanced |

---

## Enable Workload Management on vSphere

```text
vCenter → Workload Management → Get Started
  Step 1: Select Cluster (must be vSAN cluster or have compatible storage)
  Step 2: Control Plane Size: Tiny/Small/Medium/Large
    (for production: Medium — 4 vCPU, 16 GB RAM per control plane VM)
  Step 3: Storage: select default storage policy for Supervisor
  Step 4: Load Balancer: NSX-T (auto-config) or AVI (enter AVI controller FQDN)
  Step 5: Management Network: select portgroup, enter IP range for control plane VMs
  Step 6: Workload Network: select NSX-T network or portgroup range
  Step 7: TKG Service Content Library: register Tanzu content library
  Step 8: DNS, NTP → confirm → Finish

Deployment takes 30-60 minutes. Monitor progress in Workload Management.
```

---

## Deploy TKG Management Cluster (Standalone)

For TKG deployed outside of vSphere with Tanzu:

```bash
# Create cluster config YAML
cat > mgmt-cluster-config.yaml <<EOF
CLUSTER_NAME: mgmt-cluster
CLUSTER_PLAN: prod
INFRASTRUCTURE_PROVIDER: vsphere
VSPHERE_SERVER: vcenter.example.local
VSPHERE_USERNAME: administrator@vsphere.local
VSPHERE_PASSWORD: <password>
VSPHERE_DATACENTER: /DC01
VSPHERE_RESOURCE_POOL: /DC01/host/Cluster01/Resources/TKG
VSPHERE_DATASTORE: /DC01/datastore/vsan-ds
VSPHERE_FOLDER: /DC01/vm/TKG
VSPHERE_NETWORK: TKG-Management
VSPHERE_SSH_AUTHORIZED_KEY: <ssh-public-key>
CONTROL_PLANE_MACHINE_COUNT: 3
WORKER_MACHINE_COUNT: 3
ENABLE_AUDIT_LOGGING: true
EOF

tanzu management-cluster create --file mgmt-cluster-config.yaml -v 6
```

---

## Deploy a TKG Workload Cluster

```bash
cat > workload-cluster.yaml <<EOF
CLUSTER_NAME: prod-workload-01
CLUSTER_PLAN: prod
NAMESPACE: production
VSPHERE_SERVER: vcenter.example.local
VSPHERE_USERNAME: administrator@vsphere.local
VSPHERE_PASSWORD: <password>
VSPHERE_DATACENTER: /DC01
VSPHERE_RESOURCE_POOL: /DC01/host/Cluster01/Resources/TKG
VSPHERE_DATASTORE: /DC01/datastore/vsan-ds
VSPHERE_FOLDER: /DC01/vm/TKG
VSPHERE_NETWORK: TKG-Workloads
VSPHERE_SSH_AUTHORIZED_KEY: <ssh-public-key>
CONTROL_PLANE_MACHINE_COUNT: 3
WORKER_MACHINE_COUNT: 5
KUBERNETES_VERSION: v1.26.5+vmware.2
EOF

tanzu cluster create --file workload-cluster.yaml
```

---

## Harbor Deployment (OVA)

```text
vCenter → Deploy OVF Template → Harbor-<version>.ova
  Network: Management network
  Storage: shared NFS or vSAN datastore (images stored here)
  
Post-deploy — configure via HTTPS on port 443:
  Admin password → change from Harbor12345 default
  Configure LDAP/OIDC
  Configure S3 or NFS for image storage
  Enable vulnerability scanning (Trivy)
```

---

## Upgrade Order

Strict upgrade sequence:

1. **vCenter** (if upgrading vSphere)
2. **Supervisor** — upgrades automatically after vCenter upgrade (managed by vCenter lifecycle manager)
3. **TKG management cluster:**
   ```bash
   tanzu management-cluster upgrade
   ```
4. **TKG workload clusters** — one at a time:
   ```bash
   tanzu cluster list  # check current versions
   tanzu cluster upgrade <cluster-name>
   # Upgrades control plane first, then workers (rolling)
   ```
5. **Harbor** — OVA-based; redeploy from new OVA preserving external DB and storage

---

## Upgrade a TKG Workload Cluster

```bash
# Check available Kubernetes versions for upgrade
tanzu kubernetes-release get  # or check content library

# Upgrade cluster (rolling — one node at a time)
tanzu cluster upgrade prod-workload-01 --yes

# Monitor upgrade
tanzu cluster get prod-workload-01
kubectl get nodes -w  # watch node status during rolling upgrade

# Verify after upgrade
kubectl get nodes  # all nodes on new version
```

---

## Version Compatibility

Check VMware Tanzu Kubernetes releases compatibility before upgrade:
- https://docs.vmware.com/en/VMware-Tanzu-Kubernetes-Grid/
- Key compat: TKG version ↔ vSphere version ↔ Harbor version ↔ Kubernetes version
