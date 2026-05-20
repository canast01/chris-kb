# Tanzu

<div class="kb-summary">
Tanzu knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```
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
│    Architecture defines the Kubernetes layers · Operations manage clusters · Security governs workload│
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
│  RBAC          = Kubernetes Role-Based Access Control; ClusterRole, Role, RoleBinding, ClusterRoleBind│
│  Network policy= Kubernetes L4 firewall rules between pods; enforced by NSX CNI in Tanzu              │
│  tanzu CLI     = kubectl plugin for TKG; cluster create, upgrade, kubeconfig management               │
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
