# Tanzu — Health Checks

```
┌─────────────── Tanzu Health Check Hierarchy ───────────────────────────────────┐
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  1. Supervisor Cluster                                                   │  │
│  │     vCenter ► Workload Management ► Status: Running                     │  │
│  │     kubectl vsphere login ► kubectl get namespaces                      │  │
│  └───────────────────────────────┬──────────────────────────────────────────┘  │
│                                  │ OK                                           │
│  ┌───────────────────────────────▼──────────────────────────────────────────┐  │
│  │  2. TKG Cluster Nodes                                                    │  │
│  │     tanzu cluster list │ kubectl get nodes (STATUS=Ready)                │  │
│  │     kubectl get pods -n kube-system (all Running/Completed)              │  │
│  └───────────────────────────────┬──────────────────────────────────────────┘  │
│                                  │ OK                                           │
│  ┌───────────────────────────────▼──────────────────────────────────────────┐  │
│  │  3. Storage (PVCs)                                                       │  │
│  │     kubectl get pvc -A (all Bound) │ StorageClass present                │  │
│  │     kubectl get pods -n vmware-system-csi (CSI driver Running)           │  │
│  └───────────────────────────────┬──────────────────────────────────────────┘  │
│                                  │ OK                                           │
│  ┌───────────────────────────────▼──────────────────────────────────────────┐  │
│  │  4. Workloads / Services                                                 │  │
│  │     kubectl get pods -A | grep -v Running/Completed                     │  │
│  │     kubectl get svc -A | grep LoadBalancer (EXTERNAL-IP assigned)       │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Supervisor Cluster Health

```
vCenter → Workload Management → Supervisor Clusters
  Status: Running (green checkmark)
  Control Plane VMs: 3 VMs all in "Running" state
  API server reachable: kubectl vsphere login should succeed
```

```bash
# Test Supervisor API reachability
kubectl vsphere login \
  --server https://supervisor.corp.local \
  --username administrator@vsphere.local \
  --insecure-skip-tls-verify

kubectl get namespaces  # Should return list of vSphere Namespaces
```

---

## TKG Cluster Health

```bash
# Check all clusters and status
tanzu cluster list --include-management-cluster

# Check nodes in a workload cluster
kubectl config use-context <cluster-context>
kubectl get nodes
# All nodes should show STATUS=Ready

# Check control plane health
kubectl get pods -n kube-system
# All pods should be Running or Completed

# Check for CrashLoopBackOff or Error pods across all namespaces
kubectl get pods -A | grep -v Running | grep -v Completed
```

---

## Node Resource Utilization

```bash
# Node-level CPU and memory (requires metrics-server)
kubectl top nodes

# Pod-level resource usage
kubectl top pods -A --sort-by=cpu | head -20
kubectl top pods -A --sort-by=memory | head -20

# Check for nodes with high resource pressure
kubectl describe nodes | grep -A 5 "Conditions:"
# Look for: MemoryPressure=True, DiskPressure=True, PIDPressure=True
```

---

## PVC and Storage Health

```bash
# List all PVCs and their status
kubectl get pvc -A
# All PVCs should show STATUS=Bound
# Any Pending PVC means storage class is not provisioning

# Check StorageClass
kubectl get storageclass

# Test PVC provisioning (create a test PVC)
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
  namespace: default
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 1Gi
  storageClassName: <your-storage-class>
EOF

kubectl get pvc test-pvc  # Should become Bound within 30 seconds
kubectl delete pvc test-pvc
```

---

## Load Balancer / Service Health

```bash
# List Services of type LoadBalancer — verify all have EXTERNAL-IP assigned
kubectl get svc -A | grep LoadBalancer

# If EXTERNAL-IP is <pending> for >2 minutes:
# Check NSX/AVI load balancer IP pool capacity
# Check NSX-T or AVI load balancer controller logs
```

---

## Harbor Registry Health

```bash
# Harbor health API (no auth required)
curl -sk https://harbor.corp.local/api/v2.0/health | python3 -m json.tool
# All components should show status: "healthy"

# Check Harbor pods if deployed on Kubernetes
kubectl get pods -n harbor
# All pods should be Running

# Test image push/pull
docker login harbor.corp.local -u admin -p <password>
docker pull busybox && docker tag busybox harbor.corp.local/library/busybox:test
docker push harbor.corp.local/library/busybox:test
docker pull harbor.corp.local/library/busybox:test
```

---

## Certificate Expiry

```bash
# Check Supervisor API server cert
echo | openssl s_client -connect supervisor.corp.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# Check Harbor cert
echo | openssl s_client -connect harbor.corp.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# Check workload cluster API cert
CLUSTER_API=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}' | sed 's|https://||')
echo | openssl s_client -connect $CLUSTER_API 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## CSR and Cert Manager Health

```bash
# Check for pending CertificateSigningRequests in cluster
kubectl get csr
# Approve any pending (if auto-approval is not configured)

# If cert-manager is installed
kubectl get pods -n cert-manager
kubectl get certificates -A   # All should show READY=True
kubectl get certificaterequests -A
```
