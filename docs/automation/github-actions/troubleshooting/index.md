# GitHub Actions — Troubleshooting



<div class="kb-summary">
GitHub Actions — Troubleshooting reference.
</div>

```
┌────────────────────────────────── GitHub Actions — Troubleshooting ───────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common GitHub Actions issues: runner offline, job queued but not starting, secret not found  │   │
│   │      Enable debug logging: ACTIONS_RUNNER_DEBUG=true and ACTIONS_STEP_DEBUG=true secrets      │   │
│   │       gh run view --log <run-id> to fetch full log from CLI without opening the browser       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Common Issues                 │  │               Diagnostic Steps              │   │
│   │        Job queued, no runner picks up        │  │          Check runner labels match          │   │
│   │          Secret value empty in step          │  │         Set ACTIONS_STEP_DEBUG=true         │   │
│   │           OIDC token request fails           │  │          Verify cloud trust policy          │   │
│   │       Workflow not triggering on push        │  │         Check on: filter and branch         │   │
│   │          Self-hosted runner offline          │  │        Check service: ./svc.sh status       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         ACTIONS_STEP_DEBUG = secret value true; enables verbose per-step debug logging        │   │
│   │   ACTIONS_RUNNER_DEBUG= runner-level debug; shows runner registration and job pickup detail   │   │
│   │ Runner labels      = self-hosted runner must have all labels listed in runs-on: to pick up job│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────── GitHub Actions — Troubleshooting ───────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common GitHub Actions issues: runner offline, job queued but not starting, secret not found  │   │
│   │      Enable debug logging: ACTIONS_RUNNER_DEBUG=true and ACTIONS_STEP_DEBUG=true secrets      │   │
│   │       gh run view --log <run-id> to fetch full log from CLI without opening the browser       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Common Issues                 │  │               Diagnostic Steps              │   │
│   │        Job queued, no runner picks up        │  │          Check runner labels match          │   │
│   │          Secret value empty in step          │  │         Set ACTIONS_STEP_DEBUG=true         │   │
│   │           OIDC token request fails           │  │          Verify cloud trust policy          │   │
│   │       Workflow not triggering on push        │  │         Check on: filter and branch         │   │
│   │          Self-hosted runner offline          │  │        Check service: ./svc.sh status       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         ACTIONS_STEP_DEBUG = secret value true; enables verbose per-step debug logging        │   │
│   │   ACTIONS_RUNNER_DEBUG= runner-level debug; shows runner registration and job pickup detail   │   │
│   │ Runner labels      = self-hosted runner must have all labels listed in runs-on: to pick up job│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Common workflow failures and resolutions.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Debug logging, runner diagnostics, and analysis.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Escalation paths and GitHub support.</span>
</a>

</div>
