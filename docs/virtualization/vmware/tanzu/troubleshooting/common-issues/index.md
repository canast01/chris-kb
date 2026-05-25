# Tanzu — Common Issues

```text
┌──────────────── Tanzu Triage: Issue by Layer ──────────────────────────────────┐
│                                                                                 │
│  Supervisor issues                                                              │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Stuck "Configuring" ► DNS/NTP/NSX-T load balancer / content library    │   │
│  │  API unreachable ► check control plane VM IPs and network routing        │  │
│  └───────────────────────────────────────┬──────────────────────────────────┘  │
│                                          │                                      │
│  TKG Cluster issues                      ▼                                      │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Cluster stuck "creating" ► kubectl describe Machine ► image pull/creds  │  │
│  │  Namespace resource quota hit ► vCenter ► Workload Mgmt ► Namespaces    │   │
│  └───────────────────────────────────────┬──────────────────────────────────┘  │
│                                          │                                      │
│  Node / Pod issues                       ▼                                      │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Pod Pending ► kubectl describe: Insufficient cpu/mem │ PVC not bound    │  │
│  │  ImagePullBackOff ► Harbor cert trust │ wrong imagePullSecret            │  │
│  │  LoadBalancer Pending ► NSX/AVI IP pool exhausted                        │  │
│  │  Ingress not routing ► Contour pods │ HTTPProxy Valid condition          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Supervisor Stuck in Configuring State

**Symptoms:** vCenter → Workload Management shows Supervisor as "Configuring" for >30 minutes

**Causes:**

1. **DNS resolution failure**: Supervisor control plane VMs cannot resolve their own FQDN
   ```bash
   # From vCenter shell or ESXi host, test DNS:
   nslookup supervisor.example.local <dns-server>
   # Must resolve to the Supervisor API VIP IP
   ```
   Fix: add A record for Supervisor API VIP in DNS

2. **NTP skew**: Control plane VMs time differs from vCenter by >5 seconds
   ```
   vCenter → Workload Management → Supervisor → Control Plane VMs
   SSH to a control plane VM → check timedatectl
   ```

3. **NSX-T or AVI misconfiguration**: Load balancer not assigning VIP to Supervisor
   ```
   NSX-T → Load Balancing → Virtual Servers → check if VIP created for Supervisor
   ```

4. **Content Library unreachable**: TKG OVA images cannot be downloaded
   ```
   vCenter → Content Libraries → [Tanzu library] → Sync → check sync status
   ```

---

## TKG Cluster Create Fails

**Symptoms:** `tanzu cluster create` returns error or cluster is stuck in "creating" state

1. **Image pull failure** (cannot reach Harbor or content library):
   ```bash
   tanzu cluster get my-cluster -n my-namespace
   # Shows machine status — check Machine objects:
   kubectl get machines -A
   kubectl describe machine <stuck-machine> -n <namespace>
   # Look for: image pull error, bootstrap failure
   ```

2. **vSphere credentials wrong**:
   ```bash
   # Check cluster config credentials by testing vCenter API:
   curl -sk -u "svc-tanzu@corp.local:<password>" \
     "https://vcenter.example.local/rest/com/vmware/cis/session" -X POST
   ```

3. **Insufficient resource quota in Supervisor namespace**:
   ```
   vCenter → Workload Management → Namespaces → [namespace] → Resource Usage
   Verify: CPU/Memory not at limit
   ```

---

## Pod Stuck in Pending

**Symptoms:** Pod stays in Pending state, no events indicating scheduling

1. **Insufficient node resources**:
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   # Look for: "Insufficient cpu" or "Insufficient memory" in Events section
   kubectl top nodes
   # Add more workers or scale up node resources
   ```

2. **PVC not bound** (pod waiting for PVC to be provisioned):
   ```bash
   kubectl get pvc -n <namespace>
   # If PVC is Pending — check storage provisioner:
   kubectl describe pvc <pvc-name> -n <namespace>
   kubectl get pods -n vmware-system-csi  # CSI driver pods must be Running
   ```

3. **No nodes match pod's nodeSelector or taints**:
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   # "0/3 nodes are available: 3 node(s) had untolerated taint"
   kubectl describe nodes | grep -A5 Taints
   ```

---

## ImagePullBackOff

**Symptoms:** Pod events show `ImagePullBackOff` or `ErrImagePull`

1. **Harbor certificate not trusted**:
   ```bash
   # On node: check if harbor cert is in system trust store
   kubectl debug node/<node-name> -it --image=busybox
   # From node shell:
   curl https://harbor.example.local/v2/ -v  # Check TLS error
   ```
   Fix: add Harbor CA cert to cluster trust (cluster config: `TKG_CUSTOM_IMAGE_REPOSITORY_CA_CERTIFICATE`)

2. **Wrong imagePullSecret or credentials expired**:
   ```bash
   kubectl get secret harbor-pull-secret -n production -o yaml | base64 -d
   # Verify credentials are current
   docker login harbor.example.local -u <user> -p <password>  # Test credentials
   ```

---

## Service Type LoadBalancer Pending

**Symptoms:** Service shows `EXTERNAL-IP: <pending>` for >2 minutes

```bash
kubectl describe svc <service-name> -n <namespace>
# Events section will show: "no IPs available in NSX IP pool" or similar

# Check NSX-T load balancer IP pool capacity:
# NSX-T → Networking → Load Balancing → Virtual Servers → check IP usage
# AVI: AVI Controller → Cloud → SE Group → check IP pool capacity
```

Fix: expand the IP pool in NSX-T or AVI, or release unused load balancer IPs.

---

## Ingress Not Routing

**Symptoms:** HTTPProxy or Ingress created but traffic doesn't reach pods

```bash
# Check Contour pods are running:
kubectl get pods -n projectcontour

# Check HTTPProxy status:
kubectl get httpproxy -n production
kubectl describe httpproxy myapp -n production
# Look for: Conditions - Valid

# Check envoy DaemonSet (the data plane):
kubectl get pods -n projectcontour -l app=envoy

# Test: curl the Envoy service directly
kubectl get svc -n projectcontour
curl -k https://<envoy-LB-IP>/ -H "Host: myapp.example.local"
```
