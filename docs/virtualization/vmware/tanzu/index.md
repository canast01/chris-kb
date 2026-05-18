# Tanzu

<div class="kb-summary">
Tanzu knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```
┌──────────────────── VMware Tanzu: Developer to Pod ────────────────────────────┐
│                                                                                 │
│  Developer                                                                      │
│      │  tanzu CLI / kubectl vsphere login                                       │
│      ▼                                                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐     │
│  │  Tanzu Hub / vCenter Workload Management (Supervisor)                 │     │
│  │  vSphere Namespaces │ resource quotas │ VM classes │ content library  │     │
│  └────────────────────────────┬──────────────────────────────────────────┘     │
│                                │ provision TanzuKubernetesCluster               │
│  ┌─────────────────────────────▼──────────────────────────────────────────┐    │
│  │  TKG Workload Cluster (Kubernetes)                                     │    │
│  │  ┌───────────────┐   ┌───────────────────────────────────────────────┐│    │
│  │  │ Control Plane │   │  Worker Nodes                                 ││    │
│  │  │ (3 VMs)       │   │  ┌──────────┐ ┌──────────┐ ┌──────────┐     ││    │
│  │  │ etcd/API Srv  │   │  │  Node-01 │ │  Node-02 │ │  Node-03 │     ││    │
│  │  └───────────────┘   │  │  Pods►   │ │  Pods►   │ │  Pods►   │     ││    │
│  │                       │  └──────────┘ └──────────┘ └──────────┘     ││    │
│  │                       └───────────────────────────────────────────────┘│    │
│  │  vSphere CSI ► vSAN PVCs │ NSX/AVI ► LoadBalancer │ Harbor ► images   │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                Pinniped ► OIDC ► kubeconfig                     │
└────────────────────────────────────────────────────────────────────────────────┘
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
