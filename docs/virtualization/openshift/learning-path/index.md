# Red Hat OpenShift Container Platform — Learning Path

<div class="kb-summary">
Recommended reading order for OpenShift Container Platform. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture

**Goal**: Understand how OCP components relate — from RHCOS nodes and the control plane to the network overlay and the Operator framework that manages everything.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — control plane internals (kube-apiserver, etcd, scheduler), RHCOS immutable OS model, MachineConfig/MCO lifecycle, and OVN-Kubernetes CNI overlay
- [Design Standards](../architecture/design-standards/) — cluster sizing decisions, node roles (master/worker/infra), topology constraints, and etcd quorum requirements
- [Integrations](../architecture/integrations/) — how OCP connects to identity providers, external registries, storage backends (ODF/CSI), and monitoring stacks

**Why first**: The control plane and operator model are unlike traditional VM infrastructure. Without understanding CVO, cluster operators, and MachineConfig, every operational action feels arbitrary.

---

## Stage 2 — Deployment

**Goal**: Know the two install paths, the bootstrap process, and how to validate a fresh cluster before handing it to workload teams.

**Read**:

- [Deploy](../deploy/) — IPI vs UPI decision matrix, install-config.yaml structure, bootstrap node lifecycle, and post-install validation checklist
- [Install & Upgrade](../operations/install-upgrade/) — cluster version operator (CVO) upgrade channels (stable/fast/eus), upgrade prerequisites, and how to pause MachineConfigPools during rolling upgrades

**Why second**: IPI automation hides many steps that break silently on UPI. Understanding the bootstrap sequence prevents install failures from becoming multi-hour mysteries.

---

## Stage 3 — Operations

**Goal**: Run day-to-day cluster operations confidently — health checks, CLI fluency, patching nodes, and protecting etcd.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers `oc get co`, node status, pending MachineConfigs, and etcd member health
- [CLI Reference](../operations/cli-reference/) — `oc` commands covering project/namespace management, pod debugging, resource editing, and must-gather invocation
- [Procedures](../operations/procedures/) — node drain/cordon, MachineConfigPool pause/resume, certificate rotation, and image pruning
- [Backup & Restore](../operations/backup-restore/) — etcd snapshot backup, restore procedure for control plane failure, and velero-based workload backup
- [Scripts](../operations/scripts/) — automation helpers for certificate expiry checks, node readiness loops, and etcd snapshot scheduling

**Why third**: Operators need CLI and health-check fluency before touching node configuration. A misapplied MachineConfig can render an entire MachineConfigPool unschedulable.

---

## Stage 4 — Security

**Goal**: Lock down cluster access using RBAC and SCCs, enforce authentication, and understand what encryption protects at rest and in transit.

**Read**:

- [Access Control](../security/access-control/) — ClusterRole/Role bindings, service account scoping, and least-privilege project isolation
- [Authentication](../security/authentication/) — identity provider configuration (LDAP/OIDC), OAuth server, kubeadmin removal, and token lifetimes
- [Encryption](../security/encryption/) — etcd encryption at rest, TLS certificate authorities (internal CA, custom ingress certs), and secrets encryption key rotation
- [Hardening](../security/hardening/) — SCC policy (restricted-v2 default), pod security admission, network policies, and audit log configuration

**Why fourth**: Security context constraints are OCP-specific and enforced at admission time — workloads break silently if SCCs are misconfigured. Understand RBAC first so SCC assignments make sense.

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose cluster-level failures systematically using must-gather, operator logs, and event streams before escalating to Red Hat.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — degraded cluster operators, stuck MachineConfigs, image pull failures, and DNS/CNI connectivity problems
- [Diagnostics](../troubleshooting/diagnostics/) — must-gather collection, `oc adm inspect`, etcd leader election checks, and OVN-Kubernetes flow tracing
- [Escalation](../troubleshooting/escalation/) — what to collect before opening a Red Hat support case, sosreport vs must-gather, and severity definitions

**Why last**: Troubleshooting makes most sense once you know the normal operating state and can recognise deviations in operator status, node conditions, and network flows.
