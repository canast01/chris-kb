# GitHub Actions — Encryption


<div class="kb-summary">
> Part of the [GitHub Actions Security](../index.md) reference.
</div>

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
```powershell

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
