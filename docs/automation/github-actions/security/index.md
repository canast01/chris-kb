# GitHub Actions — Security


```
┌────────────────────────────────────── GitHub Actions — Security ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  GitHub Actions security: prevent secret exposure, supply chain attacks, privilege escalation │   │
│   │  Supply chain: pin all third-party actions by full SHA; review action source code before use  │   │
│   │         Secrets: never echo; use ${{ secrets.X }} syntax; masked automatically in logs        │   │
│   │     GITHUB_TOKEN: default permissions read-only; grant write only where explicitly needed     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Supply Chain        │  │       Secrets & Tokens      │  │       Runner Security       │   │
│   │     Pin by SHA, not tag     │  │    OIDC over stored keys    │  │      Ephemeral runners      │   │
│   │     Audit action updates    │  │     Minimal token perms     │  │       Isolated network      │   │
│   │    Allowed action policy    │  │      No secrets in env:     │  │      No shared runners      │   │
│   │    CodeQL for action scan   │  │   Rotate secrets quarterly  │  │    Label per environment    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Allowed actions = org setting; restrict to own, GitHub-verified, or allowed-list only     │   │
│   │     Script injection = fork PR can inject code into ${{ github.event.pull_request.title }}    │   │
│   │ pull_request_target    = runs with write perms even from forks — review carefully before using│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>GitHub tokens, OIDC, and authentication configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Repository permissions, environments, and least privilege.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Secrets management and encrypted communication.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and workflow security practices.</span>
</a>

</div>
