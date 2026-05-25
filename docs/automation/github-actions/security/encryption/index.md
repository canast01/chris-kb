# GitHub Actions — Encryption

> Part of the [GitHub Actions Security](../index.md) reference.

---

## Secrets Management

```mermaid
flowchart LR
    dev(["Developer\nsets secret"])
    ghSettings["GitHub Settings\nRepo / Env / Org"]
    ghEncrypted["GitHub Encrypted Store\nLibSodium public key encryption"]
    wfRun["Workflow Run\nRunner environment"]
    step["Step\nenv: VAR=${{ secrets.X }}"]
    logs["Workflow Logs\nValue masked as ***"]

    dev --> ghSettings --> ghEncrypted
    ghEncrypted -->|"injected at runtime\nnot stored on disk"| wfRun
    wfRun --> step --> logs
```
┌───────────────────────────────────── GitHub Actions — Encryption ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    GitHub Actions encrypts secrets at rest and in transit; secrets masked in all log output   │   │
│   │       Secrets: stored encrypted in GitHub; decrypted only during job execution on runner      │   │
│   │                Transport: all API calls and runner communication over TLS 1.2+                │   │
│   │     Avoid: do not base64-encode secrets to work around masking — GitHub masks decoded too     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Secret Handling                │  │          Encryption Best Practices          │   │
│   │         AES-256-GCM at rest (GitHub)         │  │        OIDC eliminates stored secrets       │   │
│   │           Masked in all log output           │  │           Rotate secrets quarterly          │   │
│   │          ${{ secrets.X }} injection          │  │           Env scope: job not step           │   │
│   │         Never printed: echo $SECRET          │  │         Audit secret access in logs         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Secret masking  = GitHub scans all log output and replaces secret values with ***       │   │
│   │    add-mask        = ::add-mask::<value> step command; register dynamic values for masking    │   │
│   │    Env scope       = set secret as env var at job level; available to all steps in that job   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Managing secrets via `gh` CLI:

```bash
# Set a repository secret
gh secret set DEPLOY_SSH_KEY < ~/.ssh/deploy_key

# Set from a value
echo "mytoken123" | gh secret set API_TOKEN

# List all secrets (names only — values are never shown)
gh secret list

# Delete a secret
gh secret delete OLD_TOKEN

# Set an organisation-level secret
gh secret set SHARED_TOKEN --org myorg
```

## Secret Types and Scopes

| Scope | Where set | Accessible by |
|---|---|---|
| Repository secret | Repo Settings → Secrets | All workflows in that repo |
| Environment secret | Repo Settings → Environments | Jobs targeting that environment |
| Organisation secret | Org Settings → Secrets | Repos granted access |
| `GITHUB_TOKEN` | Auto-generated per run | All jobs, scoped to the run |

## Secret Scanning and Rotation

GitHub automatically scans pushed commits for common secret patterns and alerts when found.

```bash
# Enable secret scanning via CLI
gh api --method PATCH /repos/OWNER/REPO \
  -f security_and_analysis.secret_scanning.status=enabled \
  -f security_and_analysis.secret_scanning_push_protection.status=enabled

# List secret scanning alerts
gh api /repos/OWNER/REPO/secret-scanning/alerts
```

## Masking Dynamic Values

```yaml
# Mask a dynamically generated value in logs
- name: Get token
  id: auth
  run: |
    TOKEN=$(get-token.sh)
    echo "::add-mask::$TOKEN"
    echo "token=$TOKEN" >> "$GITHUB_OUTPUT"

# Never echo a secret directly — it will appear as ***
# but the pattern is still bad practice:
# run: echo ${{ secrets.MY_SECRET }}  # avoid this
```
