# Disaster Recovery

<div class="kb-summary">
Disaster recovery knowledge base covering DR design, runbooks, recovery testing, and the Isolated Recovery Environment (IRE) for ransomware vault operations. DR restores service availability after a major disruptive event; backup enables point-in-time data recovery — these are distinct but complementary disciplines.
</div>

```text
┌──────────────────────────────── Disaster Recovery Platform ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Disaster Recovery — Scope and Objectives                             │   │
│   │   DR = restoring service availability after a site-level or major disruptive event            │   │
│   │   RPO = maximum acceptable data loss; RTO = maximum acceptable recovery time                  │   │
│   │   Untested DR is a hypothesis — validated DR requires scheduled tests and runbooks            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         DR Design           │  │         Runbooks            │  │     Recovery Testing        │   │
│   │   RTO/RPO tiers · strat     │  │   Failover · failback       │  │   Tabletop · functional     │   │
│   │   Replication technology    │  │   Step-by-step procedures   │  │   Full DR test · ransomware │   │
│   │   Site topology · network   │  │   Escalation contacts       │  │   Evidence and sign-off     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐                                    │
│   │    Isolated Recovery Env    │  │   Backup Validation         │                                    │
│   │   Air-gap vault · IRE       │  │   Verify restorability      │                                    │
│   │   Clean-room restore        │  │   SureBackup · bpverify     │                                    │
│   │   CyberSense integrity      │  │   Test restore cadence      │                                    │
│   └─────────────────────────────┘  └─────────────────────────────┘                                    │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Production site · DR site · Replication link · Management network · Vault network                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO           = Recovery Point Objective; max acceptable data loss window                            │
│  RTO           = Recovery Time Objective; max acceptable downtime before restore                      │
│  Failover      = activating the DR site; redirecting hosts to replica resources                       │
│  Failback      = returning operations to production site after DR resolved                            │
│  Runbook       = step-by-step documented procedure for a specific DR scenario                         │
│  IRE           = Isolated Recovery Environment; air-gapped clean-room for ransomware recovery         │
│  Clean Room    = isolated vCenter + workstations for cyber recovery validation                        │
│  Air Gap       = network isolation preventing attacker lateral movement to vault                      │
│  CyberSense    = Dell integrity scan engine; detects ransomware indicators in backup data             │
│  Tier 0–4      = service recovery priority tier; Tier 0 = < 15 min RTO / RPO = 0 (sync repl)          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="design/">
  <strong>DR Design</strong>
  <span>RTO/RPO tier matrix, replication strategies, site topology, network design, and recovery objective governance.</span>
</a>

<a class="kb-card" href="runbooks/">
  <strong>Runbooks</strong>
  <span>Step-by-step DR procedures — failover, failback, and full DR activation runbook.</span>
</a>

<a class="kb-card" href="recovery-testing/">
  <strong>Recovery Testing</strong>
  <span>Tabletop exercises, functional tests, full DR failover tests, and ransomware recovery validation.</span>
</a>

<a class="kb-card" href="ire/">
  <strong>Isolated Recovery Environment</strong>
  <span>Air-gapped clean-room for ransomware recovery — isolation, clean-room restore, and CyberSense validation.</span>
</a>

<a class="kb-card" href="backup-validation/">
  <strong>Backup Validation</strong>
  <span>Automated and manual verification that backups are intact and recoverable within defined objectives.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common DR failures — backup job errors, replication lag, failover issues, and IRE connectivity.</span>
</a>

</div>
