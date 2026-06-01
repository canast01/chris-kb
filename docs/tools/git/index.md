# Git

<div class="kb-summary">
Git knowledge base covering the distributed object model, GitHub Enterprise and GitLab self-managed architecture, branching workflows, authentication, and troubleshooting.
</div>

```
┌─────────────────────────────────────────── Git — Overview ────────────────────────────────────────────┐
│                                                                                                       │
│  Distributed version control system. Every clone is a full repository; commits are immutable.         │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Core Concepts        │  │       Common Workflows      │  │         Integrations        │   │
│   │  Repository: local + remote │  │ Feature branch → PR → merge │  │ GitHub / GitLab / Bitbucket │   │
│   │    Commit: SHA-1 snapshot   │  │   Rebase for clean history  │  │   CI/CD: Jenkins / Actions  │   │
│   │ Branch: lightweight pointer │  │    Tag: releases + semver   │  │   IaC: Terraform / Ansible  │   │
│   │ Remote: fetch / push / pull │  │   Stash: temp WIP storage   │  │   IDE: VS Code / JetBrains  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Git server (GitHub/GitLab/self-hosted) · developer workstations · CI/CD runners                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SHA-1       = unique hash identifying a commit; immutable content address                            │
│  HEAD        = pointer to current branch or commit; moves with each commit                            │
│  Index       = staging area; git add moves changes here before commit                                 │
│  Remote      = named reference to a remote repository (origin, upstream)                              │
│  Fetch       = download remote objects without merging into working tree                              │
│  Pull        = fetch + merge (or rebase) remote changes into local branch                             │
│  Stash       = temporary storage for uncommitted changes; stack-based                                 │
│  Tag         = named pointer to a commit; annotated tags include metadata                             │
│  Rebase      = re-applies commits on top of another branch; rewrites history                          │
│  Fast-forward= merge when target has no divergent commits; no merge commit                            │
│  Squash      = combine multiple commits into one before merging                                       │
│  Cherry-pick = apply a specific commit from another branch                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────── Git — Overview ────────────────────────────────────────────┐
│                                                                                                       │
│  Distributed version control system. Every clone is a full repository; commits are immutable.         │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Core Concepts        │  │       Common Workflows      │  │         Integrations        │   │
│   │  Repository: local + remote │  │ Feature branch → PR → merge │  │ GitHub / GitLab / Bitbucket │   │
│   │    Commit: SHA-1 snapshot   │  │   Rebase for clean history  │  │   CI/CD: Jenkins / Actions  │   │
│   │ Branch: lightweight pointer │  │    Tag: releases + semver   │  │   IaC: Terraform / Ansible  │   │
│   │ Remote: fetch / push / pull │  │   Stash: temp WIP storage   │  │   IDE: VS Code / JetBrains  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Git server (GitHub/GitLab/self-hosted) · developer workstations · CI/CD runners                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SHA-1       = unique hash identifying a commit; immutable content address                            │
│  HEAD        = pointer to current branch or commit; moves with each commit                            │
│  Index       = staging area; git add moves changes here before commit                                 │
│  Remote      = named reference to a remote repository (origin, upstream)                              │
│  Fetch       = download remote objects without merging into working tree                              │
│  Pull        = fetch + merge (or rebase) remote changes into local branch                             │
│  Stash       = temporary storage for uncommitted changes; stack-based                                 │
│  Tag         = named pointer to a commit; annotated tags include metadata                             │
│  Rebase      = re-applies commits on top of another branch; rewrites history                          │
│  Fast-forward= merge when target has no divergent commits; no merge commit                            │
│  Squash      = combine multiple commits into one before merging                                       │
│  Cherry-pick = apply a specific commit from another branch                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, branching, recovery, and maintenance.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
