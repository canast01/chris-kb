# OpenShift — Operations

<div class="kb-summary">
Day-2 operations: oc CLI, health checks, node management, upgrade procedures, etcd backup, and runnable health-check routines.
</div>

```text
┌──────────────────────────────────────── OpenShift Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   OpenShift Day-2 Operations                                  │   │
│   │          Six sub-sections: CLI, Health Checks, Procedures, Upgrades, Backup, Scripts          │   │
│   │           Health baseline: all COs True/False/False; all nodes Ready; etcd 3 members          │   │
│   │               Upgrades: oc adm upgrade → EUS-to-EUS path for minor version jumps              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                 ▼                               ▼                                 ▼                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌───────────────────────────────┐   │
│   │        Daily Health        │  │         Procedures         │  │            Upgrades           │   │
│   │       oc get co,nodes      │  │     Node drain/uncordon    │  │          oc adm upgrade       │   │
│   │     etcd endpoint health   │  │      MachineSet scaling    │  │         EUS channel path      │   │
│   │     cert rotation check    │  │        Cert rotation       │  │        Version lifecycle      │   │
│   └────────────────────────────┘  └────────────────────────────┘  └───────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Backup & Restore               │  │                   Scripts                   │   │
│   │              etcd snapshot backup            │  │                health-check.sh              │   │
│   │             Restore from etcd snap           │  │                 csr-approve.sh              │   │
│   │               OADP / Velero apps             │  │                 node-drain.sh               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="cli-reference/">
    <span class="kb-card-title">CLI Reference</span>
    <span class="kb-card-desc">oc get, describe, logs, exec, adm, debug, and common flags</span>
  </a>
  <a class="kb-card" href="health-checks/">
    <span class="kb-card-title">Health Checks</span>
    <span class="kb-card-desc">Run This Routine — cluster operators, nodes, etcd, and monitoring</span>
  </a>
  <a class="kb-card" href="procedures/">
    <span class="kb-card-title">Procedures</span>
    <span class="kb-card-desc">Scale nodes, drain, add MachineSet, rotate certs, label nodes</span>
  </a>
  <a class="kb-card" href="scripts/">
    <span class="kb-card-title">Scripts</span>
    <span class="kb-card-desc">Health snapshot, node drain, etcd backup, CSR auto-approve</span>
  </a>
  <a class="kb-card" href="install-upgrade/">
    <span class="kb-card-title">Install & Upgrade</span>
    <span class="kb-card-desc">EUS upgrade path, channel selection, and OCP version lifecycle</span>
  </a>
  <a class="kb-card" href="backup-restore/">
    <span class="kb-card-title">Backup & Restore</span>
    <span class="kb-card-desc">etcd backup/restore, OADP for application workloads</span>
  </a>
</div>
