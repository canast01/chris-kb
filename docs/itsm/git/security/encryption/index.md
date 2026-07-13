---
tags:
  - git
  - security
---
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

```text title="Expected output"
[master a3f7e2c] Signed commit
 1 file changed, 2 insertions(+)
Created tag 'v1.2.3'
commit a3f7e2c8b9d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7
gpg: Signature made Wed 15 Jan 2025 14:32:18 UTC using RSA key ID 4A3F8E2D
gpg: Good signature from "DevOps Team <devops@company.internal>"
object a3f7e2c8b9d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7
type commit
tag v1.2.3
tagger DevOps Team <devops@company.internal> Wed 15 Jan 2025 14:32:45 UTC
gpg: Signature made Wed 15 Jan 2025 14:32:45 UTC using RSA key ID 4A3F8E2D
gpg: Good signature from "DevOps Team <devops@company.internal>"
a3f7e2c Signed commit
b2e6d1b Update security policy
c1f5a0e Initial infrastructure setup
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: gpg failed to sign the data` | Ensure GPG is installed (`apt-get install gnupg2`), the key ID is correct, and the GPG agent is running (`gpg-agent --daemon`). |
    | `error: gpg.program not found` | Configure the GPG program path with `git config --global gpg.program /usr/bin/gpg2` if using GPG 2.x. |
    | `error: key <GPG_KEY_ID> does not contain a secret key` | Verify the key exists in your local keyring with `gpg --list-secret-keys` and use the correct 16-character key ID. |
```bash
# Generate an Ed25519 GPG key
gpg --expert --full-generate-key
# Select: (9) ECC (sign and encrypt) → (1) Curve 25519

# Export public key for GitHub/GitLab upload
gpg --armor --export <KEY_ID>

# Backup private key (store offline/in secrets manager)
gpg --armor --export-secret-keys <KEY_ID> > gpg_private_backup.asc
```

```text title="Expected output"
gpg (GnuPG) 2.2.19; Copyright (C) 2019 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) RSA and Elgamal
   (3) DSA and Elgamal
   (4) RSA (sign only)
   (5) DSA (sign only)
   (6) Elgamal (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
   (9) ECC (sign and encrypt)
Your selection? 9
Please select which elliptic curve you want:
   (1) Curve 25519
   (2) Curve 448
   (3) NIST P-256
   (4) NIST P-384
   (5) NIST P-521
Your selection? 1
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 0
Key expires at Thu 01 Jan 2026 00:00:00 UTC
Is this correct? (y/N) y
GnuPG needs to construct a user ID to identify your key.

Real name: DevOps Admin
Email address: admin@company.dev
Comment: Git signing key
You selected this user ID:
    "DevOps Admin <admin@company.dev>"
Change (N)ame, (C)omment or (E)mail (or quit to cancel)? N
We need to generate a lot of random bytes. It is a good idea to perform
some other action (typing, moving the mouse, using the disk) during the
prime generation; this gives the random number generator a better chance
to gain enough entropy.
gpg: key 4F2E8B9C3A1D5E7F marked as ultimately trusted
pub   ed25519 2024-01-15 [SC]
      4F2E8B9C3A1D5E7F2B4A6C8E9D1F3A5B
uid           [ultimate] DevOps Admin <admin@company.dev>
sub   cv25519 2024-01-15 [E]

-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBGXk7pYBCADf8q2N3vK9mL2pQ4rJ8sX5hY3kZ6aB2cD4eF6gH8iJ0kL2mN4o
P6qR8sT0uV2wX4yZ6aB8cD0eF2gH4iJ6kL8mN0oP2qR4sT6uV8wX0yZ2aB4cD8eF8
...
=aBcD
-----END PGP PUBLIC KEY BLOCK-----

gpg: key 4F2E8B9C3A1D5
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

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
commit 7a3f8e2c9b1d4e5f6a7b8c9d0e1f2a3b
Good "git" signature for user@corp.example.com with ED25519 key SHA256:aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcdefghijkl
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: key does not contain a public key` | Ensure the SSH public key file path is correct and the file contains a valid public key (not a private key). |
    | `error: unknown signature type 'ssh'` | Update Git to version 2.34 or later, which added SSH signature support. |
    | `fatal: your current branch 'main' does not have any commits yet` | Create an initial commit before attempting to verify; `git verify-commit HEAD` requires at least one signed commit in history. |
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

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not in a git repository` | Run these commands outside a repo; they set global config in `~/.gitconfig`, not repo-specific settings. |
    | `error: unknown credential helper 'osxkeychain'` | Install Git via Homebrew (`brew install git`) or Xcode Command Line Tools to include the osxkeychain helper. |
    | `error: unknown credential helper '/usr/lib/git-core/git-credential-libsecret'` | Install the libsecret package (`sudo apt install libsecret-1-0 git`) and verify the helper path exists before configuring. |
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

```text title="Expected output"
protocol=https
host=github.com
username=dev-user@company.com
password=ghp_aBcD1234eFgH5678iJkL9012mNoPqRsT
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: cannot run git-credential-osxkeychain: No such file or directory` | Install the credential helper with `git credential-osxkeychain` or use `brew install git-credential-osxkeychain` on macOS. |
    | `grep: /Users/username/.gitconfig: No such file or directory` | Create a basic `.gitconfig` file with `git config --global user.name "Your Name"` or verify the file path is correct for your user. |
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

```text title="Expected output"
Homebrew 4.2.15
==> Downloading https://ghcr.io/v2/homebrew/core/git-crypt/manifests/0.7.0
==> Pouring git-crypt-0.7.0.arm64_darwin.bottle.tar.gz
🍺  /usr/local/opt/git-crypt (8 files, 156KB)
Initialised empty git-crypt repository in /path/to/repo/.git/crypt
[master (root-commit) a7f3e2c] Encrypt secrets with git-crypt
 3 files changed, 3 insertions(+)
 create mode 100644 .gitattributes
 create mode 100644 .git/crypt/keys/default
Repository unlocked. Files decrypted.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not a git repository (or any of the parent directories): .git` | Run `git init` before `git-crypt init`, or ensure you are inside a valid git repository directory. |
    | `gpg: error reading key: No public key` | Verify the GPG_KEY_ID exists locally with `gpg --list-keys` and use the correct key ID format (16-character hex or email). |
    | `git-crypt: error: could not decrypt file` | Ensure the correct decryption key file is provided with `git-crypt unlock` or that your GPG key is available in the local keyring. |
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

```text title="Expected output"
==> Downloading https://ghcr.io/v2/homebrew/core/sops/manifests/3.8.1
==> Downloading https://ghcr.io/v2/homebrew/core/sops/blobs/sha256:a1b2c3d4e5f6
==> Installing sops
==> Pouring sops--3.8.1.monterey.bottle.tar.gz
🍺  /usr/local/Cellar/sops/3.8.1/bin/sops
(no output — command completes silently)
(no output — command completes silently)
sops 3.8.1 (latest)
enc: 0.0.0
gpg: 2.3.11
age: 1.1.1

sops --encrypt secrets/database.yaml > secrets/database.enc.yaml
Encrypting /dev/stdin
sops --decrypt secrets/database.enc.yaml
database:
  host: prod-db-01.internal
  port: 5432
  username: app_user
  password: ENC[AES256_GCM,data:K7x9mP2qL8vN,iv:...]
  sops:
    kms: []
    gcp_kms: []
    azure_kv: []
    hc_vault: []
    age: []
    lastmodified: '2024-01-15T14:32:18Z'
    mac: ENC[AES256_GCM,data:...]
    pgp:
    - created_at: '2024-01-15T14:32:18Z'
      enc: |-
        -----BEGIN PGP MESSAGE-----
        ...
      fp: A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6
    version: 3.8.1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: failed to get the data key [error getting data key from pgp: gpg: no default secret key]` | Ensure your GPG secret key is imported and set as the default key with `gpg --default-key FINGERPRINT`. |
    | `error: failed to encrypt the file [error encrypting with pgp: gpg: no public key]` | Verify the PGP fingerprints in `.sops.yaml` match your imported public keys using `gpg --list-keys`. |
    | `error: failed to open file [permission denied]` | Ensure the secrets directory exists and has write permissions with `mkdir -p secrets && chmod 700 secrets`. |
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

```text title="Expected output"
Endpoint=https://git-lfs.company.internal/storage
Current user: admin@company.com

Locked path/to/large/file.bin

path/to/large/file.bin	admin@company.com	ID: 8f4c2e91-7a3b-4d9e-b2f1-5c8a9d3e7f2a

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Repository or object not found` | Verify the LFS endpoint URL is accessible and the repository exists on the LFS server. |
    | `Error: path/to/large/file.bin is already locked by another user` | Have the other user run `git lfs unlock` first, or contact them to release the lock. |
    | `fatal: Not a git repository` | Run this command from within a Git repository that has LFS initialized with `git lfs install`. |
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

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Git — Hardening](../hardening/)
- [Git — Authentication](../authentication/)
- [Git — Access Control](../access-control/)
