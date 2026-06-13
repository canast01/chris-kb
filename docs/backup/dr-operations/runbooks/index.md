---
tags:
  - dr
---
# DR Runbooks

<div class="kb-summary">
Step-by-step DR runbooks for failover, failback, and full DR activation. Each runbook includes activation criteria, pre-checks, phased procedures, communication trees, and validation checklists.
</div>

```text
┌────────────────────────────────────── DR Operations — Runbooks ───────────────────────────────────────┐
│                                                                                                       │
│   Three runbooks: DR Activation, Failover procedure, and Failback procedure                           │
│   Each runbook includes activation criteria, pre-checks, phased steps, and sign-off                   │
│   Activation authority: pre-agreed in DR plan; typically CISO + CTO sign-off required                 │
│   RTO and RPO targets drive which runbook to invoke and how fast each phase must complete             │
│                                                                                                       │
│   DR activation runbook                                                                               │
│   Criteria: production site unavailable AND recovery time estimate exceeds RTO threshold              │
│   Communication tree: primary contact → escalation path → vendor support notification                 │
│   Phase 1: activate DR command structure; Phase 2: invoke failover; Phase 3: verify                   │
│   Sign-off checklist: all critical services verified at DR site before standing down                  │
│                                                                                                       │
│   Failover procedure                                                                                  │
│   Pre-checks: confirm replication lag < RPO; verify DR storage and compute capacity                   │
│   Storage cutover: promote replicated volumes / snapshots to read-write at DR site                    │
│   Compute: power on VMs in dependency order (AD/DNS → core services → apps → front-end)               │
│   Network: update DNS, load balancer VIPs, firewall policies to point to DR site IPs                  │
│                                                                                                       │
│   Failback procedure                                                                                  │
│   Prerequisites: production site restored; replication re-established from DR to prod                 │
│   Re-sync data: reverse replication direction; wait for RPO lag to close before cutback               │
│   Cutback: reverse DNS/network changes; migrate workloads back in planned maintenance window          │
│   Post-failback: verify replication health; remove temporary DR-site DNS overrides                    │
│                                                                                                       │
│   Physical infrastructure                                                                             │
│   DR site: separate datacenter or cloud region; connected via replicated storage fabric               │
│   Replication links: SAN-to-SAN or software (Veeam/CommVault); RPO governs lag tolerance              │
│                                                                                                       │
│   Key terms:                                                                                          │
│   RTO          = Recovery Time Objective; max acceptable downtime duration                            │
│   RPO          = Recovery Point Objective; max acceptable data loss measured in time                  │
│   activation criteria = conditions that authorise invoking the DR plan                                │
│   replication lag = time delta between production write and DR copy being current                     │
│   failover     = shifting production workloads from primary to DR site                                │
│   failback     = returning workloads to production site after DR event resolves                       │
│   sign-off     = formal team lead confirmation that each recovery phase is complete                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="dr-runbook/">
  <strong>DR Activation Runbook</strong>
  <span>Full DR site activation — criteria, communication tree, phased recovery, and sign-off checklist.</span>
</a>

<a class="kb-card" href="failover/">
  <strong>Failover Procedure</strong>
  <span>Step-by-step failover to DR site — storage, compute, and network cutover sequence.</span>
</a>

<a class="kb-card" href="failback/">
  <strong>Failback Procedure</strong>
  <span>Return operations to production site after DR event — re-sync, validation, and cutback steps.</span>
</a>

</div>
