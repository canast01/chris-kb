---
tags:
  - operations
  - tanzu
  - vmware
---
# Tanzu — Install and Upgrade


<div class="kb-summary">
Install and Upgrade reference covering Prerequisites for vSphere with Tanzu (Supervisor), Enable Workload Management on vSphere, Deploy TKG Management Cluster (Standalone), Deploy a TKG Workload Cluster, Harbor Deployment (OVA) and 3 more sections.

*Applies to: Tanzu 3.x*
</div>
```text
┌────────────────────────── Virtualization Vmware Tanzu — Install and Upgrade ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Vmware installation and upgrade: deployment and version management procedures         │   │
│   │         Pre-upgrade: back up configuration, check compatibility, review release notes         │   │
│   │      Upgrade: rolling upgrade preserves service; non-disruptive on dual-controller arrays     │   │
│   │           Post-upgrade: verify all services running; run health check; notify users           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Plan → backup config → upgrade staging → upgrade production → validate                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Tanzu infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Tanzu platform overview and core concepts               │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---


!!! warning "Host enters maintenance mode"
    ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. Confirm DRS is Fully Automated and HA admission control is satisfied before starting.
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

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
