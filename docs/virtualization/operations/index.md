# Operations

Operational procedures, health checks, troubleshooting guides, and runbooks for the virtualization platform.

```
Operations Scope
═══════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────┐
  │                  Daily Operations                   │
  │   Morning health check · Alert triage · Handoff    │
  └──────────────┬──────────────────────┬───────────────┘
                 │                      │
         ┌───────▼──────┐      ┌────────▼───────┐
         │ Health Checks │      │  Runbooks      │
         │               │      │                │
         │ Daily         │      │ Incident       │
         │ Pre-change    │      │ Maintenance    │
         │ Post-change   │      │ Host evac      │
         │ Alert review  │      │ Snapshots      │
         │ Capacity      │      │ VM lifecycle   │
         │ Access check  │      │ Cert renewal   │
         └───────┬───────┘      └────────┬───────┘
                 │                       │
                 └──────────┬────────────┘
                            ▼
                 ┌──────────────────────┐
                 │   Troubleshooting    │
                 │                      │
                 │ Symptom → Category   │
                 │ → Runbook → Resolve  │
                 │                      │
                 │ VM performance       │
                 │ Host disconnected    │
                 │ Datastore issues     │
                 │ Network / cert       │
                 └──────────────────────┘
```

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Pre- and post-change health checks, daily checks, and validation procedures.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Troubleshooting guides, known issues, and resolution steps across all platforms.</span>
</a>

<a class="kb-card" href="runbooks/">
  <strong>Runbooks</strong>
  <span>Step-by-step operational runbooks for common tasks and incidents.</span>
</a>

</div>
