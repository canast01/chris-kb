# ServiceNow — Lifecycle Management

<div class="kb-summary">
System onboarding, upgrade readiness, migration, post-upgrade validation, rollback, and decommission procedures.
</div>

```text
┌──────────────────────────────────────── Lifecycle Management ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         System lifecycle: plan → onboard → operate → upgrade → migrate → decommission         │   │
│   │        Each phase documented; no phase skipped without CAB approval and risk assessment       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Procure → build → onboard → BAU → upgrade readiness → migration → decommission                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Onboard           │  │      Operate / Upgrade      │  │            Retire           │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       System readiness      │  │      Upgrade readiness      │  │      Decommission plan      │   │
│   │          CMDB entry         │  │      Upgrade execution      │  │        Data migration       │   │
│   │       Monitoring setup      │  │      Post-upgrade check     │  │       Backup retention      │   │
│   │       Runbook creation      │  │        Rollback path        │  │        Asset disposal       │   │
│   │       Handover to ops       │  │        Migration plan       │  │         CMDB retire         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Onboarding    = Process of introducing a new system into BAU operations with documentation         │
│    Decommission  = Formal retirement of a system; data migration, backup, and asset recovery          │
│    CMDB          = Configuration Management Database; track system attributes through lifecycle       │
│    Upgrade window= Scheduled maintenance period for OS/firmware/software upgrades                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<!-- diagram:lifecycle -->

<div class="kb-grid">
  <a class="kb-card" href="system-onboarding/">
    <span class="kb-card-title">System Onboarding</span>
    <span class="kb-card-desc">Onboard new systems and services into the environment</span>
  </a>
  <a class="kb-card" href="upgrade-readiness/">
    <span class="kb-card-title">Upgrade Readiness</span>
    <span class="kb-card-desc">Pre-upgrade checklist and environment validation</span>
  </a>
  <a class="kb-card" href="migration-procedure/">
    <span class="kb-card-title">Migration Procedure</span>
    <span class="kb-card-desc">Step-by-step system migration process</span>
  </a>
  <a class="kb-card" href="post-upgrade-validation/">
    <span class="kb-card-title">Post-Upgrade Validation</span>
    <span class="kb-card-desc">Validate system health and functionality after upgrades</span>
  </a>
  <a class="kb-card" href="rollback-procedure/">
    <span class="kb-card-title">Rollback Procedure</span>
    <span class="kb-card-desc">Rollback steps when an upgrade or migration fails</span>
  </a>
  <a class="kb-card" href="system-decommission/">
    <span class="kb-card-title">System Decommission</span>
    <span class="kb-card-desc">Safe decommission checklist for retiring systems</span>
  </a>
</div>
