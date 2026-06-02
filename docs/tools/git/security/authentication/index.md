# Git — Authentication


<div class="kb-summary">
Authentication in Git controls how users and automation prove identity when accessing repositories. Weak or misconfigured authentication is the most common cause of unauthorised code access and supply-chain incidents.
</div>

---

## Authentication Methods Overview

| Method | Transport | Strength | Recommended Use |
|---|---|---|---|
| SSH key (Ed25519) | SSH | Very High | Developer workstations, CI runners |
| SSH key (RSA 4096) | SSH | High | Legacy systems that cannot use Ed25519 |
| Personal Access Token (PAT) | HTTPS | Medium-High | Automation, API calls, scripts |
| OAuth app token | HTTPS | Medium | Third-party integrations |
| GitHub App installation token | HTTPS | High | CI/CD pipelines, bot accounts |
| GPG-signed commits | Both | Identity proof only | Commit attribution, not transport auth |
| Username + password | HTTPS | Low | Deprecated — disable entirely |
| Deploy keys | SSH | High | Read/write access for single repos |

---

## SSH Key Authentication

### Generating a Strong SSH Key Pair

Always use Ed25519; RSA keys must be at least 4096 bits if Ed25519 is unavailable.

```bash
# Generate Ed25519 key (preferred)
ssh-keygen -t ed25519 -C "user@corp.example.com" -f ~/.ssh/id_ed25519_git

# Generate RSA 4096 (fallback for legacy systems)
ssh-keygen -t rsa -b 4096 -C "user@corp.example.com" -f ~/.ssh/id_rsa_git

# Verify key fingerprint before uploading
ssh-keygen -lf ~/.ssh/id_ed25519_git.pub
```
┌──────────────────────────────────────── Git — Authentication ─────────────────────────────────────────┐
│                                                                                                       │
│  Git authentication: SSH keys, PATs, OIDC for CI, and MFA enforcement.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              SSH Authentication              │  │          HTTPS / PAT Authentication         │   │
│   │       Generate: ssh-keygen -t ed25519        │  │          PAT as password over HTTPS         │   │
│   │         Add pub key to GitHub/GitLab         │  │        Scope: repo + workflow minimum       │   │
│   │         Test: ssh -T git@github.com          │  │            Expiry: 90-day maximum           │   │
│   │        ssh-agent: keyring management         │  │      Credential helper: keychain store      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH preferred for humans; PAT for HTTPS scripts; OIDC for CI pipelines                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                OIDC for CI/CD                │  │               MFA Enforcement               │   │
│   │         No long-lived secrets in CI          │  │           Org setting: require MFA          │   │
│   │       GitHub Actions: id-token: write        │  │           TOTP app or hardware key          │   │
│   │      Cloud provider: OIDC trust policy       │  │        Recovery codes: store offline        │   │
│   │       Short-lived token: < 1 hour TTL        │  │        Enforce SAML SSO in enterprise       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab · CI runner · cloud OIDC provider · MFA authenticator app                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ed25519      = modern elliptic-curve SSH key; shorter and more secure than RSA                       │
│  ssh-agent    = daemon holding decrypted private keys in memory during session                        │
│  PAT scope    = granular permissions (repo, read:org, workflow) on access token                       │
│  Credential helper= caches HTTPS credentials in OS keychain (keychain/libsecret)                      │
│  OIDC         = CI workload requests short-lived token from IdP; no stored secret                     │
│  id-token perm= GitHub Actions permission granting OIDC JWT to the workflow                           │
│  Trust policy = cloud IAM policy allowing GitHub OIDC issuer to assume role                           │
│  TOTP         = time-based one-time password; 6-digit code from authenticator app                     │
│  Recovery codes= backup codes for MFA bypass; store in password manager offline                       │
│  SAML SSO     = enforce org login through enterprise IdP; unlinked users lose access                  │
│  SSH config   = ~/.ssh/config; maps Host to IdentityFile, User, Port                                  │
│  Keychain     = macOS keychain / Windows Credential Manager stores SSH passphrase                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌──────────────────────────────────────── Git — Authentication ─────────────────────────────────────────┐
│                                                                                                       │
│  Git authentication: SSH keys, PATs, OIDC for CI, and MFA enforcement.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              SSH Authentication              │  │          HTTPS / PAT Authentication         │   │
│   │       Generate: ssh-keygen -t ed25519        │  │          PAT as password over HTTPS         │   │
│   │         Add pub key to GitHub/GitLab         │  │        Scope: repo + workflow minimum       │   │
│   │         Test: ssh -T git@github.com          │  │            Expiry: 90-day maximum           │   │
│   │        ssh-agent: keyring management         │  │      Credential helper: keychain store      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH preferred for humans; PAT for HTTPS scripts; OIDC for CI pipelines                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                OIDC for CI/CD                │  │               MFA Enforcement               │   │
│   │         No long-lived secrets in CI          │  │           Org setting: require MFA          │   │
│   │       GitHub Actions: id-token: write        │  │           TOTP app or hardware key          │   │
│   │      Cloud provider: OIDC trust policy       │  │        Recovery codes: store offline        │   │
│   │       Short-lived token: < 1 hour TTL        │  │        Enforce SAML SSO in enterprise       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab · CI runner · cloud OIDC provider · MFA authenticator app                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ed25519      = modern elliptic-curve SSH key; shorter and more secure than RSA                       │
│  ssh-agent    = daemon holding decrypted private keys in memory during session                        │
│  PAT scope    = granular permissions (repo, read:org, workflow) on access token                       │
│  Credential helper= caches HTTPS credentials in OS keychain (keychain/libsecret)                      │
│  OIDC         = CI workload requests short-lived token from IdP; no stored secret                     │
│  id-token perm= GitHub Actions permission granting OIDC JWT to the workflow                           │
│  Trust policy = cloud IAM policy allowing GitHub OIDC issuer to assume role                           │
│  TOTP         = time-based one-time password; 6-digit code from authenticator app                     │
│  Recovery codes= backup codes for MFA bypass; store in password manager offline                       │
│  SAML SSO     = enforce org login through enterprise IdP; unlinked users lose access                  │
│  SSH config   = ~/.ssh/config; maps Host to IdentityFile, User, Port                                  │
│  Keychain     = macOS keychain / Windows Credential Manager stores SSH passphrase                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

`IdentitiesOnly yes` prevents SSH from trying all keys in the agent — critical when managing multiple identities.

### Uploading Public Keys

```bash
# Display public key for upload to GitHub/GitLab/Bitbucket
cat ~/.ssh/id_ed25519_git.pub

# Test connection
ssh -T git@github.com
ssh -T git@gitlab.corp.example.com
```

### Deploy Keys

Deploy keys are repository-specific SSH keys used by CI/CD and automation.

```bash
# Generate a deploy key (no passphrase — stored securely in CI)
ssh-keygen -t ed25519 -C "deploy-key-repo-name" -f ~/.ssh/deploy_key_reponame -N ""
```

- Upload the **public key** to the repository's Deploy Keys settings.
- Store the **private key** in the CI system's secret store (GitHub Actions secrets, GitLab CI variables, Vault).
- Grant read-only access unless the pipeline needs to push.

---

## HTTPS Token Authentication

### Personal Access Tokens (PATs)

PATs replace passwords for HTTPS Git operations. They are scoped and can be revoked individually.

**Minimum required scopes for typical operations:**

| Purpose | Required Scope |
|---|---|
| Clone / pull only | `repo:read` (GitHub), `read_repository` (GitLab) |
| Push code | `repo` (GitHub), `write_repository` (GitLab) |
| Manage webhooks | `admin:repo_hook` |
| Read packages | `read:packages` |

```bash
# Store a PAT securely using Git credential helper
git config --global credential.helper osxkeychain          # macOS
git config --global credential.helper manager              # Windows (Git Credential Manager)
git config --global credential.helper libsecret            # Linux GNOME keyring

# Verify stored credential
git credential fill <<'EOF'
protocol=https
host=github.com
EOF
```

**Never store PATs in:**
- `.git/config` in plaintext
- Shell profile files (`~/.bashrc`, `~/.zshrc`)
- Source code or environment files committed to repos

### Fine-Grained PATs (GitHub)

GitHub fine-grained PATs (2023+) restrict tokens to specific repositories and resource types. Prefer them over classic PATs.

```text
Token expiry: 90 days maximum (enforce via org policy)
Repository access: Selected repositories only
Permissions: Contents: Read and write, Metadata: Read
```

### GitHub Apps vs PATs for Automation

| Criteria | PAT | GitHub App |
|---|---|---|
| Linked to user account | Yes | No |
| Survives user leaving org | No | Yes |
| Fine-grained permissions | Fine-grained PAT only | Yes |
| Rate limit | 5,000 req/hr | 15,000 req/hr |
| Recommended for CI/CD | No | Yes |

---

## GPG Commit Signing

GPG signing authenticates commit authorship (not transport). It does not replace SSH or token auth but proves who created a commit.

```bash
# Generate a GPG key (RSA 4096 or Ed25519)
gpg --full-generate-key
# Choose: (1) RSA and RSA, 4096 bits, 2y expiry

# List keys and get key ID
gpg --list-secret-keys --keyid-format=long

# Configure Git to use the key
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Export public key for upload to GitHub/GitLab
gpg --armor --export <KEY_ID>
```

### Verifying Signed Commits

```bash
# Verify a specific commit
git verify-commit HEAD

# Show signature status in log
git log --show-signature -5

# Verify a signed tag
git verify-tag v1.2.3
```

---

## Two-Factor Authentication (2FA)

Enforce 2FA at the organisation level on all Git hosting platforms.

**GitHub:**
- Organisation Settings → Authentication security → Require two-factor authentication
- Members without 2FA are automatically removed from the org after the grace period

**GitLab:**
- Admin Area → Settings → Sign-in restrictions → Two-factor authentication → Require all users

Supported 2FA methods (in order of security):

| Method | Phishing resistant | Recommended |
|---|---|---|
| Hardware security key (FIDO2/WebAuthn) | Yes | Highest |
| TOTP authenticator app | No | Preferred |
| SMS | No | Avoid |
| Recovery codes | N/A | Backup only |

---

## SSH Certificate Authorities (Enterprise)

Large organisations can issue short-lived SSH certificates instead of distributing individual public keys.

```bash
# Sign a user key with an SSH CA (on the CA host)
ssh-keygen -s /etc/ssh/ca_key \
  -I "user@corp.example.com" \
  -n git \
  -V +8h \
  ~/.ssh/id_ed25519_git.pub

# The resulting certificate is id_ed25519_git-cert.pub
# Configure SSH to present it automatically
# ~/.ssh/config
Host gitlab.corp.example.com
    CertificateFile ~/.ssh/id_ed25519_git-cert.pub
    IdentityFile ~/.ssh/id_ed25519_git
```

Certificates expire automatically — no manual key rotation required.

---

## Credential Rotation and Audit

```bash
# List all SSH keys registered on GitHub via API
gh api /user/keys --jq '.[].title'

# List all PATs (GitHub)
gh api /user/tokens --paginate

# Revoke a PAT by ID
gh api --method DELETE /user/tokens/<token_id>

# Find hardcoded credentials in repo history (use truffleHog)
trufflehog git https://github.com/org/repo.git --only-verified
```

**Rotation schedule:**

| Credential Type | Maximum Age |
|---|---|
| PAT (developer) | 90 days |
| PAT (automation) | 30 days |
| Deploy key | 1 year |
| SSH user key | 2 years |
| GPG signing key | 2 years |

---

## Related Pages

- [Git — Encryption](../encryption/index.md)
- [Git — Access Control](../access-control/index.md)
- [Git — Hardening](../hardening/index.md)
