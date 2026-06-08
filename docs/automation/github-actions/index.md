# GitHub Actions

<div class="kb-summary">
GitHub Actions knowledge base covering event-driven workflow architecture, runner management, secrets and OIDC authentication, self-hosted runners, concurrency, and CI/CD pipeline design for GitHub-hosted repositories.
</div>

```text
┌────────────────────────────────── GitHub Actions — CI/CD Automation ──────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   GitHub Actions: native CI/CD platform; workflows defined in YAML under .github/workflows/   │   │
│   │   Trigger: push, pull_request, schedule, workflow_dispatch, repository_dispatch, or webhooks  │   │
│   │  Jobs run on runners: GitHub-hosted (ubuntu/windows/macos) or self-hosted (on-prem/cloud VMs) │   │
│   │         Actions marketplace: reusable steps; pin by SHA for security; audit before use        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │    Workflow → job → step    │  │      Runner management      │  │      Secrets management     │   │
│   │         Runner types        │  │     Monitoring job runs     │  │       OIDC cloud auth       │   │
│   │     Environments + gates    │  │     Cache and artifacts     │  │      Branch protection      │   │
│   │       Matrix strategy       │  │     Billing and minutes     │  │        Action pinning       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Workflow       = YAML file in .github/workflows/; defines triggers, jobs, and steps      │   │
│   │   Job            = set of steps that run on a single runner; jobs run in parallel by default  │   │
│   │      Step           = individual task in a job; uses: an action, or run: a shell command      │   │
│   │  Action         = reusable unit of automation; published to GitHub Marketplace or repo-local  │   │
│   │           Runner         = compute that executes jobs; GitHub-hosted or self-hosted           │   │
│   │   Environment    = deployment target with protection rules, secrets, and required reviewers   │   │
│   │   Matrix         = strategy to run a job across multiple variable combinations (OS, version)  │   │
│   │    Artifact       = file uploaded from a job and available for download or subsequent jobs    │   │
│   │    Cache          = store and restore dependencies across runs; keyed by hash of lock file    │   │
│   │     OIDC          = OpenID Connect; GHA requests short-lived cloud tokens without secrets     │   │
│   │      workflow_dispatch= manual trigger with optional input parameters; run from UI or API     │   │
│   │    Concurrency    = group/cancel-in-progress setting to avoid duplicate runs on same branch   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Day-to-day operational tasks, health checks, procedures, and automation scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation procedures.</span>
</a>

</div>
