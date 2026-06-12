# OpenShift — Architecture

<div class="kb-summary">
OpenShift control plane, node types, networking model, and storage integration. Covers how etcd, API server, scheduler, and operators interact to manage cluster state.
</div>

![OpenShift Architecture Overview](../../../assets/openshift-architecture-overview.svg)

```text
┌─────────────────────────────────────── OpenShift Architecture ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                OpenShift Architecture Overview                                │   │
│   │   Three sub-sections: How It Works (internals), Design Standards (sizing/CIDR), Integrations  │   │
│   │       Control plane: etcd quorum + API server + controller-manager + scheduler on RHCOS       │   │
│   │  Operator pattern: platform components self-manage via Cluster Operators (CO reconciliation)  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                 ▼                               ▼                                 ▼                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌───────────────────────────────┐   │
│   │        How It Works        │  │      Design Standards      │  │          Integrations         │   │
│   │        etcd I/O path       │  │      Node sizing rules     │  │           vSphere IPI         │   │
│   │       OVN-K data path      │  │        CIDR planning       │  │          LDAP identity        │   │
│   │       Operator pattern     │  │         StorageClass       │  │          Quay registry        │   │
│   │      MachineSet scaling    │  │      MachineSet config     │  │            ACM / ODF          │   │
│   └────────────────────────────┘  └────────────────────────────┘  └───────────────────────────────┘   │
│                                                                                                       │
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
