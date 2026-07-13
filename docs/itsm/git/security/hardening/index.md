---
tags:
  - git
  - security
---
# Git — Hardening

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


```text title="Expected output"
Collecting pre-commit
  Downloading pre-commit-3.6.0-py2.py3-none-any.whl (194 kB)
     |████████████████████████████████| 194 kB 2.3 MB/s
Collecting cfgv>=2.4.0
  Downloading cfgv-3.4.0-py2.py3-none-any.whl (7.1 kB)
Collecting identify>=1.0.4
  Downloading identify-2.5.35-py2.py3-none-any.whl (98 kB)
Installing collected packages: cfgv, identify, pre-commit
Successfully installed cfgv-3.4.0 identify-2.5.35 pre-commit-3.6.0
pre-commit installed at .git/hooks/pre-commit
pre-commit installed at .git/hooks/commit-msg
pre-commit installed at .git/hooks/pre-push
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: not a git repository (or any parent up to mount point /)` | Ensure you are in a valid git repository directory before running `pre-commit install`. |
    | `ERROR: Could not find a version that satisfies the requirement pre-commit` | Verify your pip is up to date with `pip install --upgrade pip` and check your internet connection. |
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

```text title="Expected output"
○
    │╲
    │ ○ gitleaks v8.18.2
    │ │
    ○ │ Scanning for secrets...
    │ │
    ○ │ 4 secrets found in git history
    │ │
    ○ │ Findings written to gitleaks-report.json

Scanning commit range HEAD~1..HEAD...
No secrets detected in specified range.

🔍 trufflehog v3.63.0
Loaded 1247 commits from git history
Scanning with verified secrets filter...
Found 0 verified secrets

Secrets baseline created: .secrets.baseline
Baseline contains 0 known secrets
Starting audit mode (press 'q' to quit, 'y' to confirm, 'n' to skip)...
Audit complete. Baseline updated.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gitleaks: command not found` | Install gitleaks with `brew install gitleaks` (macOS) or download from https://github.com/gitleaks/gitleaks/releases. |
    | `Error: failed to create report file: permission denied` | Run the command from a directory where your user has write permissions, or use `sudo` if scanning a restricted repository. |
    | `detect-secrets: command not found` | Install with `pip install detect-secrets` and ensure the installation directory is in your PATH. |
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

```text title="Expected output"
{
  "default_workflow_permissions": "read"
}
actions/checkout@v4
actions/setup-node@v3
actions/upload-artifact@v3
docker/build-push-action@v4
my-org/custom-action@main
security-audit-action@v2.1.0

.github/workflows/deploy.yml:    - uses: actions/checkout@v4
.github/workflows/deploy.yml:    - uses: my-org/custom-action@main
.github/workflows/ci.yml:    - uses: actions/setup-node@v3
.github/workflows/release.yml:    - uses: docker/build-push-action@v4
.github/workflows/security.yml:    - uses: security-audit-action@v2.1.0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not a git repository (or any of the parent directories): .git` | Run the command from the repository root directory where `.github/workflows/` exists. |
    | `gh: repository not found` | Verify the `{org}` and `{repo}` placeholders are replaced with actual values and that your GitHub CLI authentication is valid with `gh auth status`. |
    | `grep: .github/workflows/: No such file or directory` | Ensure the repository contains a `.github/workflows/` directory; create it if workflows haven't been initialized yet. |
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

```text title="Expected output"
✓ Set secret DATABASE_PASSWORD for repository owner/repo
✓ Set secret PROD_API_KEY for environment production in repository owner/repo

NAME                    UPDATED AT
DATABASE_PASSWORD       2024-01-15T09:47:32Z
PROD_API_KEY            2024-01-15T09:48:15Z
STAGING_API_KEY         2024-01-15T08:22:41Z

✓ Deleted secret DATABASE_PASSWORD from repository owner/repo
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: authentication required` | Run `gh auth login` to authenticate with GitHub before managing secrets. |
    | `Error: could not resolve to a repository with the field name of 'owner/repo'` | Ensure you are in a cloned repository directory or specify the repository with `--repo owner/repo` flag. |
    | `Error: secret PROD_API_KEY not found` | Verify the secret name exists in the target environment using `gh secret list --env production` before attempting deletion. |
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

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Git — Authentication](../authentication/)
- [Git — Access Control](../access-control/)
- [Git — Encryption](../encryption/)
