---
tags:
  - operations
  - tanzu
  - vmware
---
# Tanzu — Health Checks


<div class="kb-summary">
Health Checks reference covering Supervisor Cluster Health, TKG Cluster Health, Node Resource Utilization, PVC and Storage Health, Load Balancer / Service Health and 3 more sections.

*Applies to: Tanzu 3.x*
</div>


## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Supervisor cluster health** — list all namespaces to confirm the Supervisor API is reachable:
   ```bash
   kubectl get namespace --kubeconfig <supervisor-kubeconfig>
   ```
2. **Supervisor control plane VMs** — vCenter → Workload Management → Supervisor Clusters → confirm all 3 supervisor VMs are in **Running** state.
3. **TKG cluster status** — list all workload clusters and their phase:
   ```bash
   kubectl get cluster -A
   ```
   Or with the Tanzu CLI: `tanzu cluster list`
4. **TKG node health** — confirm all nodes are Ready across all clusters:
   ```bash
   kubectl get nodes --all-namespaces
   ```
5. **Supervisor namespace quotas** — check resource usage against configured limits:
   ```bash
   kubectl describe namespace <ns>
   ```
6. **Harbor registry health** (if deployed) — confirm all Harbor pods are Running:
   ```bash
   kubectl get pods -n harbor
   ```
7. **Workload Management status** — vCenter → Workload Management → confirm **Status = Running** for the Supervisor Cluster.
8. **Network health (NSX segments)** — in NSX Manager, verify the supervisor namespace network segments are present and in **Up** state; confirm no segment alarms.
9. **Certificate expiry** — check all certificates managed by cert-manager:
   ```bash
   kubectl get certificate -A
   ```
   All certificates should show `READY=True`; note any approaching expiry dates.
10. **Recent events** — surface any errors or warnings across all namespaces:
    ```bash
    kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20
    ```

---

## Supervisor Cluster Health

![Supervisor Cluster Health](../../../../assets/virtualization-vmware-tanzu-hc-supervisor-cluster-health.svg)

```text
vCenter → Workload Management → Supervisor Clusters
  Status: Running (green checkmark)
  Control Plane VMs: 3 VMs all in "Running" state
  API server reachable: kubectl vsphere login should succeed
```

```bash
# Test Supervisor API reachability
kubectl vsphere login \
  --server https://supervisor.example.local \
  --username administrator@vsphere.local \
  --insecure-skip-tls-verify

kubectl get namespaces  # Should return list of vSphere Namespaces
```

---

## TKG Cluster Health

![TKG Cluster Health](../../../../assets/virtualization-vmware-tanzu-hc-tkg-cluster-health.svg)

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

![Node Resource Utilization](../../../../assets/virtualization-vmware-tanzu-hc-node-resource-utilization.svg)

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

![PVC and Storage Health](../../../../assets/virtualization-vmware-tanzu-hc-pvc-and-storage-health.svg)

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

![Load Balancer / Service Health](../../../../assets/virtualization-vmware-tanzu-hc-load-balancer-service-health.svg)

```bash
# List Services of type LoadBalancer — verify all have EXTERNAL-IP assigned
kubectl get svc -A | grep LoadBalancer

# If EXTERNAL-IP is <pending> for >2 minutes:
# Check NSX/AVI load balancer IP pool capacity
# Check NSX-T or AVI load balancer controller logs
```

---

## Harbor Registry Health

![Harbor Registry Health](../../../../assets/virtualization-vmware-tanzu-hc-harbor-registry-health.svg)

```bash
# Harbor health API (no auth required)
curl -sk https://harbor.example.local/api/v2.0/health | python3 -m json.tool
# All components should show status: "healthy"

# Check Harbor pods if deployed on Kubernetes
kubectl get pods -n harbor
# All pods should be Running

# Test image push/pull
docker login harbor.example.local -u admin -p <password>
docker pull busybox && docker tag busybox harbor.example.local/library/busybox:test
docker push harbor.example.local/library/busybox:test
docker pull harbor.example.local/library/busybox:test
```

---

## Certificate Expiry

![Certificate Expiry](../../../../assets/virtualization-vmware-tanzu-hc-certificate-expiry.svg)

```bash
# Check Supervisor API server cert
echo | openssl s_client -connect supervisor.example.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# Check Harbor cert
echo | openssl s_client -connect harbor.example.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# Check workload cluster API cert
CLUSTER_API=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}' | sed 's|https://||')
echo | openssl s_client -connect $CLUSTER_API 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## CSR and Cert Manager Health

![CSR and Cert Manager Health](../../../../assets/virtualization-vmware-tanzu-hc-csr-and-cert-manager-health.svg)

```bash
# Check for pending CertificateSigningRequests in cluster
kubectl get csr
# Approve any pending (if auto-approval is not configured)

# If cert-manager is installed
kubectl get pods -n cert-manager
kubectl get certificates -A   # All should show READY=True
kubectl get certificaterequests -A
```

---

## See also

- [Virtualization Vmware Tanzu — Common Issues](../troubleshooting/common-issues/)
- [Tanzu — Procedures](procedures/)
- [Tanzu — CLI Reference](cli-reference/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
