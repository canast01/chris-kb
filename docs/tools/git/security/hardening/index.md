# Git — Hardening


<div class="kb-summary">
Hardening Git and its hosting platform closes the attack surface around the version control system — the most critical asset in software development pipelines.
</div>

---

## Pre-Commit Hooks

Pre-commit hooks run before each commit is created. They are the first line of defence against secrets, bad code, and policy violations.

### Installing pre-commit Framework

```bash
# Install pre-commit
pip install pre-commit
# or
brew install pre-commit

# Install hooks into the repository
cd /path/to/repo
pre-commit install

# Also install for commit-msg and push hooks
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```
┌─────────────────────────────────────────── Git — Hardening ───────────────────────────────────────────┐
│                                                                                                       │
│  Hardening Git: branch protection, dependency scanning, server-side hooks, and audit logging.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Branch Protection Rules            │  │             Dependency Scanning             │   │
│   │         Require pull request reviews         │  │        Dependabot: auto security PRs        │   │
│   │        Require status checks to pass         │  │        npm audit / pip-audit / trivy        │   │
│   │            Require linear history            │  │       SBOM: software bill of materials      │   │
│   │         Restrict force push + delete         │  │       Renovate: automated dep upgrades      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Branch rules prevent history rewrite; scanning catches vulnerable dependencies                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Server-Side Hooks               │  │                Audit Logging                │   │
│   │       pre-receive: block secrets push        │  │       Org audit log: 90-day retention       │   │
│   │        update: enforce naming policy         │  │          Stream to SIEM via webhook         │   │
│   │         post-receive: notify + scan          │  │       Alert on admin permission grant       │   │
│   │        GHE: custom pre-receive hooks         │  │      Alert on outside collaborator add      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab server · SIEM · Dependabot · secret scanning engine · hooks                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Branch protection= GitHub/GitLab rule set; enforces review, CI, and push restrictions                │
│  Linear history   = requires rebase/squash merge; no merge commits on protected branch                │
│  Dependabot       = GitHub bot; opens PRs for vulnerable dependency updates                           │
│  SBOM             = software bill of materials; lists all dependencies and versions                   │
│  Renovate         = open-source dependency update bot; alternative to Dependabot                      │
│  pre-receive hook = runs on server before refs update; blocks push on failure                         │
│  update hook      = per-ref variant of pre-receive; granular branch-level control                     │
│  post-receive     = runs after successful push; async scan or notification                            │
│  GHE hooks        = GitHub Enterprise custom pre-receive hooks via admin console                      │
│  Audit log webhook= sends org events (push/access change) to SIEM in real time                        │
│  npm audit        = checks package.json deps against known vulnerability database                     │
│  trivy            = container + filesystem vulnerability scanner; works on Git repos                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────────────── Git — Hardening ───────────────────────────────────────────┐
│                                                                                                       │
│  Hardening Git: branch protection, dependency scanning, server-side hooks, and audit logging.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Branch Protection Rules            │  │             Dependency Scanning             │   │
│   │         Require pull request reviews         │  │        Dependabot: auto security PRs        │   │
│   │        Require status checks to pass         │  │        npm audit / pip-audit / trivy        │   │
│   │            Require linear history            │  │       SBOM: software bill of materials      │   │
│   │         Restrict force push + delete         │  │       Renovate: automated dep upgrades      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Branch rules prevent history rewrite; scanning catches vulnerable dependencies                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Server-Side Hooks               │  │                Audit Logging                │   │
│   │       pre-receive: block secrets push        │  │       Org audit log: 90-day retention       │   │
│   │        update: enforce naming policy         │  │          Stream to SIEM via webhook         │   │
│   │         post-receive: notify + scan          │  │       Alert on admin permission grant       │   │
│   │        GHE: custom pre-receive hooks         │  │      Alert on outside collaborator add      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab server · SIEM · Dependabot · secret scanning engine · hooks                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Branch protection= GitHub/GitLab rule set; enforces review, CI, and push restrictions                │
│  Linear history   = requires rebase/squash merge; no merge commits on protected branch                │
│  Dependabot       = GitHub bot; opens PRs for vulnerable dependency updates                           │
│  SBOM             = software bill of materials; lists all dependencies and versions                   │
│  Renovate         = open-source dependency update bot; alternative to Dependabot                      │
│  pre-receive hook = runs on server before refs update; blocks push on failure                         │
│  update hook      = per-ref variant of pre-receive; granular branch-level control                     │
│  post-receive     = runs after successful push; async scan or notification                            │
│  GHE hooks        = GitHub Enterprise custom pre-receive hooks via admin console                      │
│  Audit log webhook= sends org events (push/access change) to SIEM in real time                        │
│  npm audit        = checks package.json deps against known vulnerability database                     │
│  trivy            = container + filesystem vulnerability scanner; works on Git repos                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Secret Scanning

### Repository-Level Scanning

```bash
# Scan full history with gitleaks
gitleaks detect \
  --source . \
  --report-format json \
  --report-path gitleaks-report.json \
  --log-level debug

# Scan a single commit
gitleaks detect --log-opts "HEAD~1..HEAD"

# Scan with truffleHog (verified secrets only)
trufflehog git file://. --only-verified --json

# Initialise detect-secrets baseline (mark known false positives)
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

### GitHub Advanced Security — Secret Scanning

Enabled at the organisation level:

1. Organisation Settings → Code security and analysis → Secret scanning → Enable all
2. Enable **Push protection** to block commits containing detected secrets

```bash
# Check if secret scanning is enabled on a repo
gh api /repos/{org}/{repo} --jq '.security_and_analysis.secret_scanning.status'

# Enable secret scanning via API
gh api --method PATCH /repos/{org}/{repo} \
  --field security_and_analysis='{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}'

# List detected secrets
gh api /repos/{org}/{repo}/secret-scanning/alerts \
  --jq '.[] | [.secret_type, .state, .html_url] | @tsv'
```

---

## `.gitattributes` Security Controls

```gitattributes
# .gitattributes

# Enforce LF line endings (prevent CRLF injection)
* text=auto eol=lf

# Mark binary files as binary (prevent diff poisoning)
*.png binary
*.jpg binary
*.pdf binary
*.zip binary
*.exe binary

# Encrypt sensitive files with git-crypt
secrets/**         filter=git-crypt diff=git-crypt
*.pem              filter=git-crypt diff=git-crypt
*.pfx              filter=git-crypt diff=git-crypt
.env               filter=git-crypt diff=git-crypt
config/prod*.yaml  filter=git-crypt diff=git-crypt

# Export-ignore (exclude from git archive)
.github/           export-ignore
tests/             export-ignore
Makefile           export-ignore
```

---

## `.gitignore` Hardening

```gitignore
# .gitignore — security-critical entries

# Secret files
.env
.env.*
*.pem
*.key
*.pfx
*.p12
*.jks
*.keystore
id_rsa
id_ed25519
*.gpg
secrets/
vault-token

# Credentials and config with secrets
.aws/credentials
.aws/config
.kube/config
kubeconfig
terraform.tfstate
terraform.tfstate.backup
*.tfvars
.terraform/

# IDE and OS files that can leak paths/config
.idea/
.vscode/settings.json
.DS_Store
Thumbs.db

# Build artefacts with embedded secrets
*.log
*.dump
core.*
```

---

## CI/CD Pipeline Security

### GitHub Actions Hardening

```yaml
# .github/workflows/build.yml
name: Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Restrict default token permissions — least privilege
permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # Only if OIDC auth needed

    steps:
      # Pin actions to full commit SHA — not mutable tags
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
        with:
          persist-credentials: false  # Don't persist GitHub token

      # Use OIDC instead of long-lived credentials for cloud auth
      - name: Configure AWS credentials via OIDC
        uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502  # v4.0.2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: eu-west-1

      - name: Run security scan
        run: |
          # Never print secrets even in debug mode
          set +x
          echo "Build step"
```

```bash
# Audit GitHub Actions workflow permissions
gh api /repos/{org}/{repo}/actions/permissions/workflow \
  --jq '.default_workflow_permissions'

# List third-party actions used across workflows
grep -r "uses:" .github/workflows/ | awk '{print $2}' | sort -u

# Identify actions not pinned to a commit SHA
grep -r "uses:" .github/workflows/ | grep -v "@[0-9a-f]\{40\}"
```

### Secrets Management in Pipelines

```bash
# Store a secret in GitHub Actions
gh secret set DATABASE_PASSWORD --body "$(cat /dev/stdin)" <<< "$SECRET_VALUE"

# List secrets (names only — values never shown)
gh secret list

# Remove a secret
gh secret delete DATABASE_PASSWORD

# Environment-scoped secret (only available in specific environments)
gh secret set PROD_API_KEY --env production --body "$SECRET_VALUE"
```

**Rules:**
- Never echo or print secrets in workflow logs.
- Use `::add-mask::` to mask dynamic values:
  ```bash
  echo "::add-mask::$DYNAMIC_SECRET"
  ```
- Use environment-scoped secrets for production credentials.
- Rotate secrets immediately when a pipeline is compromised.

---

## Repository Hygiene

### Audit Repository Settings

```bash
#!/bin/bash
ORG="your-org"

# Check security settings for all repos
gh api /orgs/$ORG/repos --paginate --jq '
  .[] | {
    name,
    private,
    delete_branch_on_merge,
    allow_force_pushes: .allow_force_pushes,
    vulnerability_alerts: .has_vulnerability_alerts
  }
'

# Enable vulnerability alerts and auto-security fixes
for repo in $(gh api /orgs/$ORG/repos --paginate --jq '.[].name'); do
  gh api --method PUT /repos/$ORG/$repo/vulnerability-alerts
  gh api --method PUT /repos/$ORG/$repo/automated-security-fixes
done
```

### Dependency Security (Dependabot)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "security"
      - "dependencies"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

---

## Hardening Checklist

| Control | Scope | Status |
|---|---|---|
| Branch protection on main/release/* | Repository | Check |
| Require signed commits | Repository | Check |
| Require PR reviews (min 2) | Repository | Check |
| CODEOWNERS file in place | Repository | Check |
| pre-commit hooks installed | Developer | Check |
| Secret scanning + push protection | Organisation | Check |
| Actions pinned to commit SHAs | Workflows | Check |
| Default workflow permissions: read | Organisation | Check |
| Dependabot enabled | Repository | Check |
| Force-push disabled | Repository | Check |
| Outside collaborators audited quarterly | Organisation | Check |
| Deploy keys rotated annually | Repository | Check |
| 2FA required for all members | Organisation | Check |
| Repo visibility audit (no accidental public) | Organisation | Check |
| `.gitignore` covers secrets and config | Repository | Check |

---

## Incident Response — Exposed Secret

```bash
# Step 1: Immediately revoke the exposed credential
# (GitHub PAT, AWS key, etc.) — do this BEFORE anything else

# Step 2: Determine blast radius
git log --all --oneline | head -20
trufflehog git file://. --only-verified

# Step 3: Remove from history with git-filter-repo
pip install git-filter-repo
git filter-repo --path path/to/secret-file --invert-paths

# Step 4: Force-push rewritten history
# Coordinate with all repository users — they must re-clone
git push --force-with-lease origin --all

# Step 5: Invalidate all clones
# Notify team to delete local clones and re-clone from remote

# Step 6: Add file to .gitignore and pre-commit hooks
echo "path/to/secret-file" >> .gitignore
git add .gitignore && git commit -m "Prevent re-commit of secret file"
```

---

## Related Pages

- [Git — Authentication](../authentication/index.md)
- [Git — Access Control](../access-control/index.md)
- [Git — Encryption](../encryption/index.md)
