# Git — Encryption

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

```text
┌────────────────────────────────────────── Git — Encryption ───────────────────────────────────────────┐
│                                                                                                       │
│  Encryption in transit (TLS/SSH), commit signing (GPG/SSH), and encrypted secret storage.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Transport Encryption             │  │             Commit Signing (GPG)            │   │
│   │       SSH: encrypted transport default       │  │     gpg --gen-key (RSA 4096 or Ed25519)     │   │
│   │         HTTPS: TLS 1.2/1.3 enforced          │  │       git config user.signingkey <id>       │   │
│   │       Verify cert: no --insecure flag        │  │            git commit -S / tag -s           │   │
│   │         Proxy: use CONNECT over TLS          │  │      Upload pub key to GitHub settings      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    All Git traffic encrypted in transit; signing provides author authenticity                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             SSH Signing (modern)             │  │                Secret Storage               │   │
│   │          git config gpg.format ssh           │  │         Never commit secrets to repo        │   │
│   │          gpg.ssh.allowedSignersFile          │  │       Use git-secret or SOPS for files      │   │
│   │         Reuses existing SSH key pair         │  │       GitHub Secrets for CI variables       │   │
│   │        Simpler key management vs GPG         │  │        Vault agent: inject at runtime       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab TLS termination · GPG keyserver · Vault · CI secret store                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GPG signing  = commit signed with private key; verified by public key on GitHub                      │
│  SSH signing  = use SSH key for commits; simpler than GPG; supported since git 2.34                   │
│  signingkey   = config option pointing to GPG key ID or SSH public key file                           │
│  git commit -S= sign commit with configured key; -s (lowercase) adds Signed-off-by                    │
│  allowedSigners= file listing trusted SSH public keys for signature verification                      │
│  git-secret   = GPG-based tool encrypting files stored in repo; decrypts for users                    │
│  SOPS         = Mozilla secret management tool; encrypts YAML/JSON with KMS/PGP                       │
│  GitHub Secrets= encrypted vars in repo/org settings; injected into Actions workflows                 │
│  Vault agent  = HashiCorp Vault sidecar; injects secrets to app at pod startup                        │
│  TLS 1.3      = current recommended TLS version; enforced by GitHub/GitLab                            │
│  CONNECT proxy= HTTP CONNECT tunnel; forwards SSH/HTTPS through corporate proxy                       │
│  No --insecure= never disable TLS cert verification; risk of MITM attack                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```nginx
# Minimum TLS 1.2; prefer TLS 1.3
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305';
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```
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
```bash
# Generate an Ed25519 GPG key
gpg --expert --full-generate-key
# Select: (9) ECC (sign and encrypt) → (1) Curve 25519

# Export public key for GitHub/GitLab upload
gpg --armor --export <KEY_ID>

# Backup private key (store offline/in secrets manager)
gpg --armor --export-secret-keys <KEY_ID> > gpg_private_backup.asc
```
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
