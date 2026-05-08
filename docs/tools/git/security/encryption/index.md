# Git — Encryption

Git itself stores content as objects — commits, trees, blobs — without native encryption. Encryption is applied at the transport layer (SSH/TLS), at the signing layer (GPG/SSH signatures), and optionally at rest through credential helpers and storage-layer controls.

---

## Transport Encryption

### SSH Transport

SSH is the preferred transport for Git. Modern Git SSH uses:

- **Key exchange:** `curve25519-sha256` (ECDH on Curve25519)
- **Host authentication:** `ssh-ed25519` (server host key)
- **Encryption:** `chacha20-poly1305@openssh.com` or `aes256-gcm@openssh.com`
- **MAC:** Authenticated encryption (AEAD, no separate MAC needed)

```bash
# Verify SSH cipher negotiated for a Git host
ssh -vvv git@github.com 2>&1 | grep -E "kex|cipher|mac"

# Restrict ciphers to strong options only (~/.ssh/config)
Host github.com gitlab.corp.example.com
    KexAlgorithms curve25519-sha256,ecdh-sha2-nistp521
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
    MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
    HostKeyAlgorithms ssh-ed25519,rsa-sha2-512
```

```bash
# Verify a Git remote is using SSH (not HTTPS or insecure)
git remote -v

# Check the host key fingerprint matches the expected value
ssh-keyscan github.com 2>/dev/null | ssh-keygen -lf -
# Expected: SHA256:uNiVztksCsDhcc0u9e8BujQXVUpKZIDTMczCvj3tD2s (github.com)
```

### HTTPS/TLS Transport

When SSH is not available, HTTPS must be enforced — plain HTTP must never be used.

```bash
# Force HTTPS instead of HTTP globally
git config --global url."https://".insteadOf "http://"

# Force SSH instead of HTTPS for GitHub
git config --global url."git@github.com:".insteadOf "https://github.com/"

# Verify TLS certificate validation is enabled (should be true by default)
git config --global http.sslVerify
# Returns: true (or empty — also means true)

# Never disable TLS verification in production
# BAD: git config --global http.sslVerify false
```

**TLS version enforcement** (server-side, nginx/Apache reverse proxy in front of GitLab):

```nginx
# Minimum TLS 1.2; prefer TLS 1.3
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305';
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

---

## Commit and Tag Signing

### GPG Signing

GPG signing creates a cryptographic proof of commit authorship. It does not encrypt content but provides integrity and non-repudiation.

```bash
# Configure Git to sign all commits with GPG
git config --global user.signingkey <GPG_KEY_ID>
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Sign a commit manually (overrides global setting)
git commit -S -m "Signed commit"

# Create a signed tag
git tag -s v1.2.3 -m "Release 1.2.3"

# Verify a signed commit
git verify-commit HEAD

# Verify a signed tag
git verify-tag v1.2.3

# Show signatures in log
git log --show-signature --oneline -10
```

**GPG key requirements:**

| Setting | Recommended Value |
|---|---|
| Algorithm | Ed25519 or RSA 4096 |
| Expiry | 2 years maximum |
| Passphrase | Required |
| Subkey for signing | Yes (keep master offline) |

```bash
# Generate an Ed25519 GPG key
gpg --expert --full-generate-key
# Select: (9) ECC (sign and encrypt) → (1) Curve 25519

# Export public key for GitHub/GitLab upload
gpg --armor --export <KEY_ID>

# Backup private key (store offline/in secrets manager)
gpg --armor --export-secret-keys <KEY_ID> > gpg_private_backup.asc
```

### SSH Commit Signing (Git 2.34+)

Git 2.34 introduced SSH key signing — simpler than GPG for teams already using SSH.

```bash
# Use the same SSH key for transport and signing
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519_git.pub
git config --global commit.gpgsign true

# Configure allowed signers for verification
mkdir -p ~/.config/git
echo "user@corp.example.com $(cat ~/.ssh/id_ed25519_git.pub)" \
  >> ~/.config/git/allowed_signers
git config --global gpg.ssh.allowedSignersFile ~/.config/git/allowed_signers

# Verify a commit signed with SSH
git verify-commit HEAD
```

---

## Credential Encryption

Git credentials (tokens, passwords) must never be stored in plaintext.

### OS Keychain Integration

```bash
# macOS — store in Keychain
git config --global credential.helper osxkeychain

# Windows — Git Credential Manager (encrypted in Windows Credential Store)
git config --global credential.helper manager

# Linux — GNOME Keyring (libsecret)
git config --global credential.helper /usr/lib/git-core/git-credential-libsecret

# Linux — pass (GPG-encrypted password store)
git config --global credential.helper /usr/share/doc/git/contrib/credential/gnome-keyring/git-credential-gnome-keyring
```

### Auditing Stored Credentials

```bash
# List credentials currently stored by the helper
git credential-osxkeychain get <<'EOF'
protocol=https
host=github.com
EOF

# Remove a stored credential
git credential-osxkeychain erase <<'EOF'
protocol=https
host=github.com
EOF

# Verify no plaintext credentials in global git config
grep -i "password\|token\|secret" ~/.gitconfig
```

---

## Encrypting Sensitive Files in Repositories

### git-crypt

`git-crypt` transparently encrypts specific files using GPG or a shared symmetric key.

```bash
# Install
brew install git-crypt   # macOS
apt-get install git-crypt  # Debian/Ubuntu

# Initialise in a repository
cd /path/to/repo
git-crypt init

# Add a GPG user who can decrypt
git-crypt add-gpg-user <GPG_KEY_ID>

# Export a symmetric key (for CI systems)
git-crypt export-key /path/to/git-crypt-key

# Define which files to encrypt (.gitattributes)
echo "secrets/** filter=git-crypt diff=git-crypt" >> .gitattributes
echo ".env filter=git-crypt diff=git-crypt" >> .gitattributes
echo "*.pem filter=git-crypt diff=git-crypt" >> .gitattributes
git add .gitattributes
git commit -m "Encrypt secrets with git-crypt"

# Unlock repository (after clone)
git-crypt unlock /path/to/git-crypt-key
# or with GPG:
git-crypt unlock
```

### SOPS (Secrets OPerationS)

SOPS is preferred over git-crypt for structured files (YAML, JSON) and integrates with cloud KMS.

```bash
# Install
brew install sops

# Create SOPS config (.sops.yaml in repo root)
cat > .sops.yaml <<'EOF'
creation_rules:
  - path_regex: secrets/.*\.yaml$
    pgp: "FINGERPRINT1,FINGERPRINT2"
    aws_profile: default
  - path_regex: config/.*\.env$
    pgp: "FINGERPRINT1"
EOF

# Encrypt a file
sops --encrypt secrets/database.yaml > secrets/database.enc.yaml

# Decrypt and edit in place
sops secrets/database.enc.yaml

# Decrypt to stdout
sops --decrypt secrets/database.enc.yaml
```

---

## LFS (Large File Storage) Security

Git LFS stores large binary files on a separate server. Ensure the LFS endpoint uses HTTPS with valid certificates.

```bash
# Verify LFS endpoint
git lfs env | grep Endpoint

# Lock a file to prevent concurrent writes
git lfs lock path/to/large/file.bin

# List locked files
git lfs locks

# Unlock a file
git lfs unlock path/to/large/file.bin
```

---

## Detecting Secrets in History

Even after removing a secret from the current branch, it remains in Git history.

```bash
# Scan entire history with truffleHog
trufflehog git file://. --only-verified

# Scan with gitleaks
gitleaks detect --source . --report-format json --report-path gitleaks-report.json

# If secrets are found — rewrite history with git filter-repo
pip install git-filter-repo
git filter-repo --path secrets/old-secret.env --invert-paths

# Force-push rewritten history (coordinate with all users)
git push --force-with-lease origin main
```

---

## Related Pages

- [Git — Authentication](../authentication/index.md)
- [Git — Access Control](../access-control/index.md)
- [Git — Hardening](../hardening/index.md)
