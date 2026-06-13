---
tags:
  - architecture
---
# OpenShift — Architecture

<div class="kb-summary">
OpenShift control plane, node types, networking model, and storage integration. Covers how etcd, API server, scheduler, and operators interact to manage cluster state.

*Applies to: OpenShift 4.x*
</div>

![OpenShift Architecture Overview](../../../assets/openshift-architecture-overview.svg)

```mermaid
graph LR
    A[OpenShift Architecture] --> B[How It Works]
    A --> C[Design Standards]
    A --> D[Integrations]

    B --> B1[API Request Flow]
    B --> B2[etcd Raft Quorum]
    B --> B3[Operator Pattern]
    B --> B4[OVN-Kubernetes CNI]
    B --> B5[MachineConfig MCO]

    C --> C1[Cluster Sizing Tiers]
    C --> C2[Node Sizing Table]
    C --> C3[Network CIDR Planning]
    C --> C4[StorageClass Standards]
    C --> C5[Infra Node Placement]

    D --> D1[vSphere CCM / CSI]
    D --> D2[LDAP / AD Identity]
    D --> D3[Harbor / Quay Registry]
    D --> D4[cert-manager / Vault]
    D --> D5[ArgoCD / GitOps]

    classDef root fill:#1e3a5f,color:#fff
    classDef section fill:#2563eb,color:#fff
    classDef topic fill:#374151,color:#fff
    class A root
    class B,C,D section
    class B1,B2,B3,B4,B5,C1,C2,C3,C4,C5,D1,D2,D3,D4,D5 topic
```

<div class="kb-grid">
  <a class="kb-card" href="how-it-works/">
    <span class="kb-card-title">How It Works</span>
    <span class="kb-card-desc">Control plane topology, etcd, API server, scheduler, and operator pattern</span>
  </a>
  <a class="kb-card" href="design-standards/">
    <span class="kb-card-title">Design Standards</span>
    <span class="kb-card-desc">Node sizing, MachineSet design, storage class standards, and networking</span>
  </a>
  <a class="kb-card" href="integrations/">
    <span class="kb-card-title">Integrations</span>
    <span class="kb-card-desc">vSphere IPI, AWS IPI, LDAP/AD, Quay, ACM, and storage backends</span>
  </a>
</div>
