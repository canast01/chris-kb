# Git — Security



<div class="kb-summary">
Git security controls — SSH key management, GPG commit signing, repository access control, and secret scanning.
</div>

```text
┌─────────────────────────────────────────── Git — Security ────────────────────────────────────────────┐
│                                                                                                       │
│  Git security: access control, commit signing, secret scanning, and branch protection.                │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │        Commit Signing       │  │       Secret Scanning       │   │
│   │       SSH key per user      │  │    GPG or SSH signing key   │  │   GitHub: native scanning   │   │
│   │     MFA on all accounts     │  │    git config gpg.format    │  │  pre-commit: detect-secrets │   │
│   │ Team-based repo permissions │  │  Verified badge on commits  │  │  BFG: clean leaked secrets  │   │
│   │  Branch protection on main  │  │Require signed: branch policy│  │  Rotate secret immediately  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab · GPG keyserver · pre-commit CI · secret rotation pipelines                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSH key      = ed25519 key pair; public key uploaded to Git host for auth                            │
│  GPG signing  = commit signed with private key; verifiable via public key                             │
│  MFA          = multi-factor authentication; required for all Git host accounts                       │
│  Verified     = GitHub badge confirming commit signed with registered GPG/SSH key                     │
│  detect-secrets= tool that scans diffs for high-entropy strings and known patterns                    │
│  BFG Repo Cleaner= tool to rewrite history, removing files/strings from all commits                   │
│  Branch policy= enforce signing, CI pass, and code review before merge                                │
│  Secret rotation= change leaked credential immediately; assume compromised                            │
│  Team perm.   = grant Read/Write/Admin at team level; avoid direct user grants                        │
│  PAT          = Personal Access Token; use scoped tokens; rotate regularly                            │
│  OIDC         = GitHub Actions can use OIDC to get cloud credentials without secrets                  │
│  Force push   = can overwrite history; restrict via branch protection rules                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSH keys, GPG signing, and credential management.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Repository permissions and branch protection.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Signing commits, tags, and data encryption.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security hardening and secret scanning.</span>
</a>

</div>
