---
tags:
  - github-actions
  - security
description: "GitHub Actions encryption: encrypted secrets storage, environment-level secret scoping, OIDC token federation for AWS and Azure, and artifact encryption..."
---
# GitHub Actions — Encryption

<div class="kb-summary">
GitHub Actions encryption: encrypted secrets storage, environment-level secret scoping, OIDC token federation for AWS and Azure, and artifact encryption policies.

*Applies to: GitHub Actions*
</div>

---

```d2
direction: down

secrets_management: "Secrets Management" {shape: rectangle}
masking_dynamic_values: "Masking Dynamic Values" {shape: rectangle}

secrets_management -> masking_dynamic_values: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Secrets Management

```d2
direction: right

dev: "Developer\nsets secret" {shape: rectangle}
ghSettings: "GitHub Settings\nRepo / Env / Org" {shape: rectangle}
ghEncrypted: "GitHub Encrypted Store\nLibSodium public key encryption" {shape: rectangle}
wfRun: "Workflow Run\nRunner environment" {shape: rectangle}
step: "Step\nenv: VAR=${{ secrets.X }}" {shape: rectangle}
logs: "Workflow Logs\nValue masked as ***" {shape: rectangle}

dev -> ghSettings
ghSettings -> ghEncrypted
ghEncrypted -> wfRun
wfRun -> step
step -> logs
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

---

## See also

- [GitHub Actions — Hardening](../hardening/)
- [GitHub Actions — Authentication](../authentication/)
- [GitHub Actions — Access Control](../access-control/)
