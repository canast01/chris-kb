---
tags:
  - deployment
  - git
---
# Git — Environment Setup

<div class="kb-summary">
Step-by-step guide to installing Git, configuring global settings, setting up SSH key authentication, and establishing a working local development environment.
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Install Git

**Linux (RHEL/CentOS 8+):**

```bash
sudo dnf install git -y
git --version
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update && sudo apt install git -y
git --version
```

**macOS:**

```bash
# Install via Homebrew (recommended — keeps Git updated separately from Xcode)
brew install git
git --version

# Confirm Homebrew git takes precedence over Xcode git
which git  # should return /usr/local/bin/git or /opt/homebrew/bin/git
```

**Windows:**

1. Download the Git for Windows installer from `https://git-scm.com/download/win`.
2. Run the installer and accept the defaults with the following exceptions:
   - **Default editor:** select your preferred editor (VS Code, Vim, Notepad++)
   - **Adjusting PATH:** select **Git from the command line and also from 3rd-party software**
   - **Line ending conversions:** select **Checkout Windows-style, commit Unix-style** (recommended for cross-platform repos)
3. Open Git Bash and confirm: `git --version`

---

## Configure Global User Settings

Set the identity that Git attaches to every commit. These settings are written to `~/.gitconfig`.

```bash
# Set full name
git config --global user.name "Jane Smith"

# Set email address (use the same email as your GitHub/GitLab account)
git config --global user.email "jane.smith@company.local"

# Confirm settings
git config --global --list
```

**Set the default branch name for new repositories:**

```bash
git config --global init.defaultBranch main
```

**Set pull behaviour (rebase recommended for clean history):**

```bash
git config --global pull.rebase true
```

**Confirm the full global config:**

```bash
cat ~/.gitconfig
```

---

## Set Up SSH Key Authentication

SSH key authentication is required for push access to GitHub, GitLab, Bitbucket, and most self-hosted Git servers.

**Generate an Ed25519 key pair:**

```bash
# Ed25519 is preferred over RSA for new keys
ssh-keygen -t ed25519 -C "jane.smith@company.local"
```

When prompted:
- **File location:** press Enter to accept the default (`~/.ssh/id_ed25519`)
- **Passphrase:** enter a passphrase (required for security — use the SSH agent to avoid re-entering it)

**Start the SSH agent and add the key:**

```bash
# Linux/macOS
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**On macOS, add this to `~/.ssh/config` to persist key loading across reboots:**

```text
Host *
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

**Add the public key to your Git server:**

```bash
# Display the public key
cat ~/.ssh/id_ed25519.pub
```

Copy the output and paste it into:
- **GitHub:** Settings → SSH and GPG keys → New SSH key
- **GitLab:** User Settings → SSH Keys → Add key
- **Bitbucket:** Personal settings → SSH keys → Add key
- **Self-hosted Gitea/Gogs:** Profile → Settings → SSH / GPG Keys

**Test the connection:**

```bash
# GitHub
ssh -T git@github.com

# GitLab
ssh -T git@gitlab.com

# Self-hosted
ssh -T git@git.company.local
```

Expected response (GitHub): `Hi jane.smith! You've successfully authenticated, but GitHub does not provide shell access.`

---

## Clone First Repository

**Clone via SSH (recommended after SSH key setup):**

```bash
git clone git@github.com:org/repo-name.git
cd repo-name
```

**Clone via HTTPS (if SSH is not yet set up):**

```bash
git clone https://github.com/org/repo-name.git
cd repo-name
```

**Confirm the remote is set correctly:**

```bash
git remote -v
# Expected:
# origin  git@github.com:org/repo-name.git (fetch)
# origin  git@github.com:org/repo-name.git (push)
```

**Verify you can fetch updates:**

```bash
git fetch origin
git status
```

---

## Configure Default Editor and Diff Tool

**Set the default commit message editor:**

```bash
# VS Code
git config --global core.editor "code --wait"

# Vim
git config --global core.editor "vim"

# Nano
git config --global core.editor "nano"
```

**Set the diff and merge tool:**

```bash
# Use VS Code as the diff and merge tool
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'

git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

**Test the diff tool:**

```bash
# Make a small change to a tracked file, then run
git difftool HEAD
# VS Code (or the configured tool) should open showing the diff
```

**Enable colour output:**

```bash
git config --global color.ui auto
```

---

## Set Up .gitignore

**Create a global .gitignore for files that should never be committed on this machine:**

```bash
touch ~/.gitignore_global
git config --global core.excludesfile ~/.gitignore_global
```

**Recommended global .gitignore entries:**

```bash
cat >> ~/.gitignore_global << 'EOF'
# OS files
.DS_Store
Thumbs.db
desktop.ini

# Editor and IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# Environment files
.env
.env.local
*.env

# Python
__pycache__/
*.pyc
*.pyo
.venv/

# Node
node_modules/

# Build artefacts
dist/
build/
*.o
*.a
EOF
```

**Per-project .gitignore:**

Add a `.gitignore` in the root of each repository for project-specific patterns. Use `gitignore.io` (`https://www.toptal.com/developers/gitignore`) to generate language and framework-specific templates.

---

## Configure Credential Helper

The credential helper stores HTTPS credentials so you are not prompted on every push or fetch.

**macOS — use the Keychain:**

```bash
git config --global credential.helper osxkeychain
```

**Linux — use the libsecret store (GNOME Keyring):**

```bash
sudo apt install libsecret-tools git-credential-libsecret  # Ubuntu
sudo make --directory=/usr/share/doc/git/contrib/credential/libsecret
git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
```

**Linux — cache credentials in memory for 1 hour:**

```bash
git config --global credential.helper 'cache --timeout=3600'
```

**Windows — use the Windows Credential Manager (set automatically by Git for Windows):**

```bash
git config --global credential.helper manager-core
```

**GitHub — use the GitHub CLI for credential management:**

```bash
# Install gh CLI, then authenticate
gh auth login
# Follow prompts — select HTTPS, authenticate via browser
# gh configures the credential helper automatically
```

---

## Validate Setup

Run through the following checks to confirm the Git environment is fully configured.

**Identity and config:**

```bash
git config --global user.name    # must return your full name
git config --global user.email   # must return your email
git config --global --list       # review all settings
```

**SSH authentication:**

```bash
ssh -T git@github.com            # or your Git server
# Expected: authentication success message
```

**Create a test repository and make a commit:**

```bash
mkdir ~/git-test && cd ~/git-test
git init
echo "# Test" > README.md
git add README.md
git commit -m "Initial commit"
git log --oneline
# Expected: one commit entry with your name and email in git log --format=full
```

**Diff tool:**

```bash
# Modify README.md, then:
git diff README.md
# Output should be colour-formatted
```

**Clone over SSH:**

```bash
# Clone a repository you have access to
git clone git@github.com:org/some-repo.git /tmp/clone-test
ls /tmp/clone-test
# Repository contents must be present
```

**Confirm .gitignore is active:**

```bash
touch ~/.DS_Store
git -C ~/git-test status
# .DS_Store must not appear in the untracked files list
```

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation
