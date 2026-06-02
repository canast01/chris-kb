# Python Automation — Security



<div class="kb-summary">
Python Automation — Security reference.
</div>

```
┌────────────────────────────────────────── Python — Security ──────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Python security: no hardcoded secrets, dependency CVE scanning, input validation, bandit scan │   │
│   │   Secrets: os.environ["KEY"] or SecretManager SDK — never in source or config files in repo   │   │
│   │   Supply chain: pin all dependencies; scan with safety or pip-audit; use trusted index only   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Secrets           │  │        Code Security        │  │         Supply Chain        │   │
│   │    os.environ for secrets   │  │        bandit -r src/       │  │         Pin all deps        │   │
│   │    AWS SecretsManager SDK   │  │      No eval() / exec()     │  │      pip-audit / safety     │   │
│   │  python-dotenv (.env local) │  │      Validate all input     │  │     Only PyPI / internal    │   │
│   │  No secrets in git history  │  │  subprocess: no shell=True  │  │        Dependabot PRs       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  bandit       = security linter; detects hardcoded secrets, SQL injection risks, unsafe calls │   │
│   │          pip-audit    = checks installed packages against OSV vulnerability database          │   │
│   │shell=True   = subprocess with shell=True risks command injection; always use list args instead│   │
│   │            pre-commit   = hooks for bandit/ruff/gitleaks run before each git commit           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>API keys, OAuth, and credential management.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Least privilege, service accounts, and access policies.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Secrets management and encrypted communication.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Secure coding practices and dependency management.</span>
</a>

</div>
