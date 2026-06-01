# Git — Access Control


<div class="kb-summary">
Access control in Git hosting platforms governs who can read, write, and administer repositories. Poor access control is the primary vector for insider threats and supply-chain attacks in software development.
</div>

---

## Access Control Model Overview

Git platforms implement access control at multiple layers:

```text
Organisation / Instance level
  └── Team / Group level
        └── Repository level
              └── Branch level
                    └── File level (CODEOWNERS)
```
┌──────────────────────────────────────── Git — Access Control ─────────────────────────────────────────┐
│                                                                                                       │
│  GitHub/GitLab access control: SSH keys, PATs, org permissions, and team structures.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Authentication Methods            │  │             Authorisation Model             │   │
│   │         SSH key: ed25519 recommended         │  │         Organisation → Teams → Repos        │   │
│   │           PAT: scoped, expiry set            │  │   Roles: Read/Triage/Write/Maintain/Admin   │   │
│   │        OIDC: keyless CI auth to cloud        │  │       CODEOWNERS: path-level reviewers      │   │
│   │         MFA: mandatory for all users         │  │         Outside collaborators: avoid        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH + MFA for humans; OIDC for machines; team-based grants at org level                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Audit and Review               │  │                 Offboarding                 │   │
│   │      Org audit log: GitHub Security tab      │  │             Remove user from org            │   │
│   │        Review PATs: Settings > Tokens        │  │          Revoke all PATs + SSH keys         │   │
│   │       Inactive users: quarterly review       │  │      Transfer repo ownership if needed      │   │
│   │        Deploy keys: repo-scoped only         │  │         Audit commits signed by user        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab org · SSO IdP · audit log retention · key management                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PAT          = Personal Access Token; scoped (repo/read:org); set expiry                             │
│  OIDC         = OpenID Connect; CI workloads get short-lived tokens, no secrets                       │
│  Deploy key   = SSH key scoped to single repo; read-only preferred                                    │
│  Outside collaborator= non-org member with repo access; harder to audit                               │
│  Maintain role= can manage repo settings but not delete or add admins                                 │
│  Triage role  = can manage issues and PRs but not push code                                           │
│  Org audit log= records all permission changes, invites, deletions                                    │
│  SSO SAML     = GitHub Enterprise + IdP; enforce org access via SSO                                   │
│  Inactive user= member with no commits/PRs in 90 days; review for removal                             │
│  Transfer     = move repo to another user/org; preserves history                                      │
│  Revoke PAT   = Settings → Developer Settings → PATs → Revoke                                         │
│  MFA enforce  = org setting requiring all members to have MFA enabled                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

---

## Branch Protection Rules

Branch protection prevents direct pushes to critical branches (main, release/*) and enforces review requirements.

### GitHub Branch Protection Configuration

Navigate to: Repository → Settings → Branches → Add rule

**Recommended settings for `main`:**

| Setting | Value |
|---|---|
| Require pull request before merging | Enabled |
| Required approvals | 2 (1 minimum) |
| Dismiss stale pull request approvals | Enabled |
| Require review from code owners | Enabled |
| Require status checks to pass | Enabled |
| Require branches to be up to date | Enabled |
| Require signed commits | Enabled |
| Include administrators | Enabled |
| Restrict who can push to matching branches | Enabled |
| Allow force pushes | Disabled |
| Allow deletions | Disabled |

```bash
# Configure branch protection via API
gh api --method PUT \
  /repos/{org}/{repo}/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci/build", "security/sast"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 2
  },
  "restrictions": null,
  "required_linear_history": true,
  "required_conversation_resolution": true,
  "required_signatures": true
}
EOF
```

### GitLab Protected Branches

```bash
# Protect a branch via GitLab API
curl --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.corp.example.com/api/v4/projects/{id}/protected_branches" \
  --data "name=main&push_access_level=0&merge_access_level=40&allow_force_push=false"
```

Access levels: 0=No access, 30=Developer, 40=Maintainer, 60=Admin.

---

## CODEOWNERS

`CODEOWNERS` defines file-level ownership. When a PR modifies owned files, the listed owners must approve.

```bash
# Location options (checked in order)
# CODEOWNERS
# .github/CODEOWNERS
# docs/CODEOWNERS

cat .github/CODEOWNERS
```

**Example CODEOWNERS file:**

```bash
# Default owner for everything
*                          @org/platform-team

# Infrastructure code requires infra team review
/terraform/                @org/infra-team
/ansible/                  @org/infra-team

# Security-sensitive files require security team
/.github/workflows/        @org/security-team
/scripts/deploy.sh         @org/security-team @org/infra-team

# Documentation
/docs/                     @org/docs-team

# Specific file — multiple owners
/config/production.yaml    @alice @bob @org/infra-team
```

**Rules:**
- Last matching pattern wins.
- At least one owner from each required team must approve.
- Combine with "Require review from code owners" branch protection.

---

## Repository Visibility

| Visibility | Access | When to Use |
|---|---|---|
| Private | Invited members only | Default for all internal repos |
| Internal (GitHub Enterprise) | All org members | Shared libraries, inner-source |
| Public | Everyone | Open-source releases only |

```bash
# Audit all public repos in an org
gh api /orgs/{org}/repos --paginate \
  --jq '.[] | select(.private == false) | .full_name'

# Make a repo private
gh api --method PATCH /repos/{org}/{repo} -f private=true
```

---

## Deploy Key Access Control

Deploy keys grant per-repository SSH access to automation systems.

```bash
# List deploy keys on a repo
gh api /repos/{org}/{repo}/keys

# Add a deploy key (read-only)
gh api --method POST /repos/{org}/{repo}/keys \
  -f title="CI Deploy Key - $(date +%Y-%m-%d)" \
  -f key="$(cat deploy_key.pub)" \
  -f read_only=true

# Remove a deploy key by ID
gh api --method DELETE /repos/{org}/{repo}/keys/{key_id}
```

**Controls:**
- One deploy key per pipeline/environment — never share keys across repos.
- Grant read-only unless the pipeline explicitly needs to push.
- Rotate annually or on personnel change.

---

## GitHub Actions Permissions

Constrain what GitHub Actions workflows can do by limiting the default token permissions.

```yaml
# Organisation or repository default: restrict to read-only
# Settings → Actions → General → Workflow permissions → Read repository contents

# Per-workflow explicit permissions (principle of least privilege)
permissions:
  contents: read
  pull-requests: write
  issues: write
  id-token: write     # Required for OIDC cloud auth

jobs:
  build:
    permissions:
      contents: read  # Override at job level — even more restrictive
```

```bash
# Verify org-level workflow permissions via API
gh api /orgs/{org}/actions/permissions/workflow \
  --jq '.default_workflow_permissions'
```

---

## GitLab Group and Project Permissions

```text
Instance level
  └── Group (namespace)
        └── Subgroup
              └── Project (repository)
```

| Role | View code | Push | Merge | Manage members | Admin |
|---|---|---|---|---|---|
| Guest | No | No | No | No | No |
| Reporter | Yes | No | No | No | No |
| Developer | Yes | Yes | Yes | No | No |
| Maintainer | Yes | Yes | Yes | Yes | No |
| Owner | Yes | Yes | Yes | Yes | Yes |

```bash
# List project members
curl --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.corp.example.com/api/v4/projects/{id}/members/all"

# Remove a member from a project
curl --request DELETE \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.corp.example.com/api/v4/projects/{id}/members/{user_id}"
```

---

## Access Review Process

Conduct quarterly access reviews for all repositories.

```bash
#!/bin/bash
# Audit org members and their repo access
ORG="your-org"

# Export all repo collaborators to CSV
gh api /orgs/$ORG/repos --paginate --jq '.[].name' | while read repo; do
  gh api "/repos/$ORG/$repo/collaborators" --paginate \
    --jq ".[] | [\"$repo\", .login, .permissions.admin, .permissions.push] | @csv"
done > repo_access_audit.csv

echo "Audit written to repo_access_audit.csv"
```

**Review checklist:**

- [ ] Remove access for departed employees immediately on offboarding
- [ ] Review and reduce outside collaborator access quarterly
- [ ] Verify no personal repos have org code cloned
- [ ] Audit tokens and deploy keys — remove unused
- [ ] Confirm branch protection is enabled on all default branches

---

## Related Pages

- [Git — Authentication](../authentication/index.md)
- [Git — Encryption](../encryption/index.md)
- [Git — Hardening](../hardening/index.md)
