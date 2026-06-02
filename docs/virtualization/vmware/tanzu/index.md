# Tanzu

<div class="kb-summary">
Tanzu knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```text
┌──────────────────────────────────── VMware Tanzu Kubernetes Stack ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        VMware Tanzu — Enterprise Kubernetes on vSphere                        │   │
│   │         Supervisor Cluster: vSphere-integrated Kubernetes control plane on ESXi hosts         │   │
│   │      TKG Workload Clusters: tenant Kubernetes clusters provisioned in vSphere namespaces      │   │
│   │       vSphere Namespace: resource boundary per team with CPU/RAM/storage quotas and RBAC      │   │
│   │       Harbor: private OCI-compliant registry; image scanning, replication, content trust      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Supervisor hosts the control plane · namespaces isolate tenants · TKG runs workload clusters       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │  Supervisor: Kubernetes CP  │  │   Cluster: create+upgrade   │  │  RBAC: namespace + cluster  │   │
│   │   vSphere namespace: quota  │  │   Harbor: image push/pull   │  │    Network policy: pod L4   │   │
│   │  NSX-T CNI: pod networking  │  │     kubectl + tanzu CLI     │  │   PSA: pod security admit   │   │
│   │     Harbor: OCI registry    │  │     Carvel: package mgmt    │  │   Image scan: Trivy/Clair   │   │
│   │   TMC: multi-cluster mgmt   │  │   TMC: policy + lifecycle   │  │    Audit: API server logs   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines the Kubernetes layers · Operations manage clusters                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │Cluster stuck: che│ kubectl describe │Supervisor: healthy│   GSS + bundle   │ tanzu cluster ls │   │
│   │Pod pending: no no│kubectl get events│   Nodes: Ready?   │  TAM escalation  │kubectl get pods -│   │
│   │Image pull: Harbor│Harbor harbor.log │  Harbor: running? │ Collect API logs │ tanzu package ls │   │
│   │NSX CNI not ready │NSX node agent log│ CNI: pods running?│ P1: cluster down │  kubectl get ns  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere + vSAN cluster · NSX-T for pod networking · Harbor VM · management network + workload network│
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Supervisor Cluster= vSphere-integrated Kubernetes control plane running as ESXi kernel components    │
│  TKG           = Tanzu Kubernetes Grid; tenant Kubernetes clusters deployed from Supervisor           │
│  vSphere Namespace= Resource boundary with CPU/RAM/storage quotas; maps to Kubernetes namespace       │
│  Harbor        = VMware open-source OCI registry; image scanning, replication, and content trust      │
│  TMC           = Tanzu Mission Control; SaaS multi-cluster management, policy, and observability      │
│  Carvel        = Tool suite (kapp, ytt, kbld, imgpkg) for Kubernetes packaging and deployment         │
│  PSA           = Pod Security Admission; Kubernetes enforcer for restricted/baseline/privileged modes │
│  NSX CNI       = NSX-T container network interface; provides pod networking and policy for TKG        │
│  Content trust = Harbor feature ensuring only signed images can be pulled; uses Notary/cosign         │
│  RBAC          = Kubernetes Role-Based Access Control; ClusterRole, Role, RoleBinding,                │
│  Network policy= Kubernetes L4 firewall rules between pods; enforced by NSX CNI in Tanzu              │
│  tanzu CLI     = kubectl plugin for TKG; cluster create, upgrade, kubeconfig management               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌─────────────────────────── VMware Tanzu Kubernetes — Installation Sequence ───────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Requisites                                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  vSphere 7.0 U2+ or vSphere 8  ·  Enterprise Plus licence (Workload Management)                       │
│  NSX-T deployed OR vSphere Distributed Switch 7.0+ for VDS networking mode                            │
│  Shared storage: vSAN or NFS/iSCSI datastore for supervisor control plane VMs                         │
│  DNS: A-records for Supervisor API server VIP + worker node VMs                                       │
│  NTP: all ESXi hosts and vCenter time-synced  ·  Registry (Harbor) planned                            │
│                                                                                                       │
│                                        │  enable Workload Management (Supervisor)                     │
│                                        ▼                                                              │
│  Step 2 · Enable Workload Management                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  vCenter → Workload Management → Enable  ·  Select cluster                                            │
│  Choose networking: NSX-T (recommended) or VDS with HAProxy                                           │
│  Control Plane VMs: size (tiny/small/medium/large)  ·  3 VMs deployed automatically                   │
│  Ingress/Egress CIDR, Pod CIDRs, Service CIDR: enter non-overlapping ranges                           │
│  Wait for Supervisor Ready state  ·  Control plane VMs healthy in vCenter                             │
│                                                                                                       │
│                                        │  configure namespaces                                        │
│                                        ▼                                                              │
│  Step 3 · vSphere Namespace Configuration                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create vSphere namespace per team or environment                                                     │
│  Resource limits: CPU, memory, storage quotas per namespace                                           │
│  Storage policy: assign vSAN or NFS storage policy for PVC provisioning                               │
│  Network: assign NSX segment or VDS network to namespace                                              │
│  Permissions: assign AD users/groups to namespace with edit/view roles                                │
│                                                                                                       │
│                                        │  deploy Tanzu Kubernetes Grid clusters                       │
│                                        ▼                                                              │
│  Step 4 · TKG Cluster Deployment                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  kubectl vsphere login --server <supervisor-VIP>  ·  Authenticate via AD/SSO                          │
│  Switch context to vSphere namespace  ·  Apply TanzuKubernetesCluster YAML                            │
│  Define control plane + worker node pools  ·  Choose TKR (Kubernetes release)                         │
│  Storage class and CNI (Antrea) applied automatically  ·  Cluster provisions                          │
│  Get kubeconfig  ·  kubectl get nodes  ·  All nodes Ready state confirmed                             │
│                                                                                                       │
│                                        │  deploy Harbor container registry                            │
│                                        ▼                                                              │
│  Step 5 · Harbor Container Registry                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Harbor via Aria Automation, Helm, or as embedded in Supervisor                                │
│  Set admin password  ·  Configure internal CA or upload CA-signed cert                                │
│  Create projects: one per team/namespace  ·  Assign project roles to AD groups                        │
│  Robot accounts: create per CI/CD pipeline  ·  Assign pull/push rights                                │
│  Configure replication: mirror images from Docker Hub / external registry                             │
│                                                                                                       │
│                                        │  developer onboarding                                        │
│                                        ▼                                                              │
│  Step 6 · Developer Onboarding                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Provide kubectl vsphere login command + Supervisor VIP to teams                                      │
│  Namespace RBAC: AD groups mapped to Kubernetes RBAC roles via namespace                              │
│  CI/CD integration: pipeline authenticates to Harbor  ·  Build → push → deploy                        │
│  Resource quotas enforced: pods over quota blocked  ·  Teams manage own limits                        │
│  Monitoring: Aria Operations with Kubernetes MP  ·  Alerts on pod failures                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
