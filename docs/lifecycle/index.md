# Lifecycle

<div class="kb-summary">
Infrastructure lifecycle management covering installation, upgrade, patching, decommission, and EOL tracking across platforms.
</div>

```
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
## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="environment-readiness/">
  <strong>Environment Readiness</strong>
  <span>Pre-deployment checks for infrastructure capacity, dependencies, and configuration baselines.</span>
</a>

<a class="kb-card" href="migration-procedure/">
  <strong>Migration Procedure</strong>
  <span>Step-by-step data, workload, or service migration process with validation checkpoints.</span>
</a>

<a class="kb-card" href="post-upgrade-validation/">
  <strong>Post Upgrade Validation</strong>
  <span>Checks to confirm system health, service availability, and functionality after an upgrade.</span>
</a>

<a class="kb-card" href="rollback-procedure/">
  <strong>Rollback Procedure</strong>
  <span>Steps to revert changes and restore prior state when an upgrade or change fails.</span>
</a>

<a class="kb-card" href="system-decommission/">
  <strong>System Decommission</strong>
  <span>Safe removal of a system including data archival, access revocation, and documentation updates.</span>
</a>

<a class="kb-card" href="system-onboarding/">
  <strong>System Onboarding</strong>
  <span>Steps to register, configure, monitor, and document a new system into the environment.</span>
</a>

<a class="kb-card" href="upgrade-readiness/">
  <strong>Upgrade Readiness</strong>
  <span>Pre-upgrade prerequisites: version compatibility, backup validation, dependency checks, and change approval.</span>
</a>
</div>
