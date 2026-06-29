---
tags:
  - git
  - security
---
# Git — Access Control

<div class="kb-summary">
Access control in Git hosting platforms governs who can read, write, and administer repositories. Poor access control is the primary vector for insider threats and supply-chain attacks in software development.

*Applies to: Git 2.x*
</div>

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Access Control Model Overview

Git platforms implement access control at multiple layers:

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


```text title="Expected output"
{
  "url": "https://api.github.com/repos/acme-corp/platform-api/branches/main/protection",
  "required_status_checks": {
    "url": "https://api.github.com/repos/acme-corp/platform-api/branches/main/protection/required_status_checks",
    "strict": true,
    "contexts": [
      "ci/build",
      "security/sast"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 2
  },
  "required_linear_history": true,
  "required_conversation_resolution": true,
  "required_signatures": true
}
```

!!! warning "Common errors"
    **`HTTP 404: Not Found`** — Verify the org and repo names are correct and that you have admin access to the repository.
    **`HTTP 422: Validation Failed - "required_status_checks.contexts" is not a list of valid status check contexts`** — Ensure the CI context names match exactly what your GitHub Actions workflows or external checks report (check the branch protection UI to see available contexts).
    **`HTTP 403: Resource not accessible by integration`** — Confirm your GitHub token has `admin:repo_hook` and `repo` scopes, or use a PAT with full repo permissions instead of GITHUB_TOKEN.
### GitLab Protected Branches

```bash
# Protect a branch via GitLab API
curl --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.corp.example.com/api/v4/projects/{id}/protected_branches" \
  --data "name=main&push_access_level=0&merge_access_level=40&allow_force_push=false"
```


```text title="Expected output"
{"id":1,"name":"main","push_access_level":0,"merge_access_level":40,"code_owner_approval_required":false,"inherited":false,"allow_force_push":false,"unprotect_access_level":40,"created_at":"2024-01-15T09:42:33.847Z"}
```

!!! warning "Common errors"
    **`{"message":"401 Unauthorized"}`** — Verify the `GITLAB_TOKEN` environment variable is set and contains a valid personal access token with `api` scope.
    **`{"message":"Branch already protected"}`** — The branch protection already exists; use a PATCH request to update it instead, or delete the existing rule first.
    **`{"message":"404 Project Not Found"}`** — Replace `{id}` with the actual numeric project ID or URL-encoded project path (e.g., `group%2Fproject`).
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


```text title="Expected output"
# This is a CODEOWNERS file for the repository
# Format: path/pattern @username @org/team

* @devops-lead @platform/core-team
src/auth/ @security-team @auth-maintainers
docs/ @tech-writers @documentation-team
*.tf @infrastructure-team
.github/workflows/ @devops-lead @ci-cd-team
tests/ @qa-team @testing-leads
```

!!! warning "Common errors"
    **`cat: .github/CODEOWNERS: No such file or directory`** — Verify the CODEOWNERS file exists in the `.github/` directory by running `ls -la .github/` first.
    **`Permission denied`** — Check file permissions with `ls -l .github/CODEOWNERS` and ensure your user has read access; add read permissions with `chmod +r .github/CODEOWNERS` if needed.
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`fatal: not a git repository (or any of the parent directories): .git`** — Run this command from the repository root directory where the `.git` folder exists.
    **`error: pathspec 'CODEOWNERS' did not match any files`** — Save this content to a file named `CODEOWNERS` in the `.github/` directory, not as a standalone script.
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


```text title="Expected output"
acme-corp/terraform-modules
acme-corp/documentation
acme-corp/public-api-client
acme-corp/legacy-scripts
acme-corp/sample-configs
...

(no output — command completes silently)
```

!!! warning "Common errors"
    **`HTTP 404: Not Found`** — Verify the organization name and repository name are correct, and that your GitHub token has `repo` and `admin:org` permissions.
    **`GraphQL: Field 'private' is not defined on type 'Repository'`** — Use the REST API v3 endpoint format `/repos/{owner}/{repo}` with `-f private=true` flag instead of GraphQL syntax.
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


```text title="Expected output"
[
  {
    "id": 78392841,
    "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDx8vK...",
    "url": "https://api.github.com/repos/acme-corp/backend/keys/78392841",
    "title": "CI Deploy Key - 2024-01-15",
    "read_only": true,
    "created_at": "2024-01-15T09:42:18Z"
  },
  {
    "id": 78392842,
    "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC2nPm...",
    "url": "https://api.github.com/repos/acme-corp/backend/keys/78392842",
    "title": "CI Deploy Key - 2024-01-10",
    "read_only": true,
    "created_at": "2024-01-10T14:27:33Z"
  }
]

{
  "id": 78392843,
  "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDm9kL...",
  "url": "https://api.github.com/repos/acme-corp/backend/keys/78392843",
  "title": "CI Deploy Key - 2024-01-20",
  "read_only": true,
  "created_at": "2024-01-20T11:05:47Z"
}

(no output — command completes silently)
```

!!! warning "Common errors"
    **`gh: Repository not found`** — Verify the org and repo names are correct and you have access to the repository.
    **`Error: Key file not found or permission denied while opening 'deploy_key.pub'`** — Ensure the deploy key file exists in the current directory and is readable with `ls -la deploy_key.pub`.
    **`HTTP 422: Validation Failed - Key is already in use`** — Remove the duplicate key first or generate a new SSH key pair before adding it.
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


```text title="Expected output"
"read"
```

!!! warning "Common errors"
    **`gh: Repository not found`** — Replace `{org}` with your actual organization name (e.g., `gh api /orgs/acme-corp/actions/permissions/workflow`).
    **`HTTP 403: Resource not accessible by integration`** — Ensure your GitHub token has `admin:org_hook` or `admin:org` scope by running `gh auth refresh -s admin:org`.
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


```text title="Expected output"
[
  {
    "id": 42,
    "username": "jsmith",
    "name": "John Smith",
    "state": "active",
    "avatar_url": "https://gitlab.corp.example.com/uploads/user/avatar/42/avatar.jpg",
    "web_url": "https://gitlab.corp.example.com/jsmith",
    "last_activity_on": "2024-01-15",
    "membership_type": "group_member",
    "removable": true,
    "created_at": "2023-06-20T09:15:32.123Z",
    "access_level": 30
  },
  {
    "id": 87,
    "username": "mchen",
    "name": "Maria Chen",
    "state": "active",
    "avatar_url": "https://gitlab.corp.example.com/uploads/user/avatar/87/avatar.jpg",
    "web_url": "https://gitlab.corp.example.com/mchen",
    "last_activity_on": "2024-01-18",
    "membership_type": "project_member",
    "removable": true,
    "created_at": "2023-08-10T14:22:05.456Z",
    "access_level": 40
  }
]
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to gitlab.corp.example.com port 443: Connection refused`** — Verify GitLab server is running and accessible; check network connectivity and firewall rules.
    **`{"message":"401 Unauthorized"}`** — Ensure `$GITLAB_TOKEN` is set correctly and has API access permissions; regenerate the token if expired.
    **`{"message":"404 Project Not Found"}`** — Replace `{id}` with the actual numeric project ID or URL-encoded project path (e.g., `group%2Fproject`).
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


```text title="Expected output"
"terraform-infra","alice.chen",true,true
"terraform-infra","bob.martinez",false,true
"terraform-infra","ci-bot-prod",false,true
"api-gateway","alice.chen",true,true
"api-gateway","david.patel",false,false
"api-gateway","security-scanner",false,true
"monitoring-stack","bob.martinez",true,true
"monitoring-stack","eve.thompson",false,true
...
Audit written to repo_access_audit.csv
```

!!! warning "Common errors"
    **`gh: Unauthorized. Ensure that your token has the necessary scopes to access this resource.`** — Regenerate your GitHub CLI token with `admin:org_hook` and `repo` scopes via `gh auth refresh -s admin:org_hook,repo`.
    **`jq: error (at <stdin>:0): Cannot index array with string "repo"`** — Remove the double quotes around `$repo` in the jq filter and use single quotes: `.[] | ["\($repo)", .login, ...]` or move the variable outside the jq expression.
    **`Error: HTTP 404: Not Found`** — Verify the organization name is correct and you have access to it by running `gh org list`.
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

---

## See also

- [Git — Authentication](../authentication/)
- [Git — Hardening](../hardening/)
- [Git — Encryption](../encryption/)
