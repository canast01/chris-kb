# Tanzu — Operations

<div class="kb-summary">
Tanzu — Operations reference.
</div>

```text
┌────────────────────────────────────── VMware Tanzu — Operations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Cluster lifecycle: provision, scale, and upgrade workload clusters via kubectl or Tanzu CLI  │   │
│   │      Node pool management: add/remove workers; drain nodes before maintenance operations      │   │
│   │     Supervisor health: check vCenter Workload Management status; validate namespace quotas    │   │
│   │      Image management: scan and promote images in Harbor; enforce OPA/admission policies      │   │
│   │      Tanzu CLI: tanzu cluster create/delete/upgrade/scale; kubeconfig context management      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops manage cluster state · lifecycle upgrades Kubernetes versions                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │        Cluster status       │  │       Cluster upgrade       │  │          Tanzu CLI          │   │
│   │       Node pool scale       │  │       K8s version bump      │  │        kubectl apply        │   │
│   │       Namespace quotas      │  │      Node drain/cordon      │  │       GitOps pipelines      │   │
│   │        Image scanning       │  │        Supervisor upg       │  │        TMC automation       │   │
│   │       Harbor registry       │  │        OVA bundle upg       │  │        Cluster API CR       │   │
│   │       kubeconfig mgmt       │  │        Cert rotation        │  │         Helm deploys        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops check cluster and node health · lifecycle upgrades Kubernetes safely                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  tanzu cluster   │ Cluster: Running │   Scale workers   │ Cluster upgrade  │  kubeconfig bkp  │   │
│   │  kubectl apply   │   Nodes: Ready   │   Add namespace   │  Supervisor upg  │  ETCD snapshot   │   │
│   │  kubectl drain   │    Quotas: ok    │    Update quota   │    OVA bundle    │  Cluster config  │   │
│   │   tanzu login    │ Harbor: healthy  │   Image promote   │   Post-upg val   │  Namespace bkp   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts · RAM DIMMs · Network NICs · vSAN/NFS storage · NSX-T fabric · vCenter appliance          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Tanzu CLI          = kubectl plug-in and tanzu binary for cluster lifecycle and context management   │
│  tanzu cluster      = CLI sub-command for create, scale, upgrade, delete of workload clusters         │
│  Node drain         = kubectl drain removes pods from a node before maintenance or upgrade            │
│  Node pool scaling  = Adding or removing worker VMs in a pool via Cluster API update                  │
│  Supervisor upgrade = vCenter-driven update of the Workload Management control plane version          │
│  OVA bundle         = Tanzu node OS image OVA; uploaded to vCenter content library for upgrades       │
│  kubeconfig         = Kubernetes configuration file with cluster endpoint and credentials for kubectl │
│  Namespace quota    = CPU/memory/storage limits applied to a vSphere namespace; enforced by Supervisor│
│  Cluster API CR     = Custom Resource defining desired cluster state; reconciled by Cluster API       │
│  GitOps pipeline    = Declarative deployment pipeline applying manifests from git to Kubernetes       │
│  Harbor             = VMware OCI-compatible registry; image scanning and replication built-in         │
│  ETCD snapshot      = Backup of Kubernetes cluster state; taken before any major upgrade operation    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Commands, syntax, and quick reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Routine checks, service validation, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Day-to-day operational tasks and how-to guides.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation, upgrade, patching, and decommission.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup configuration, restore procedures, and validation.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and reusable code.</span>
</a>

</div>
