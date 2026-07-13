---
tags:
  - deployment
  - git
search:
  boost: 1.5
description: "Step-by-step guide to installing Git, configuring global settings, setting up SSH key authentication, and establishing a working local development..."
---
# Git — Environment Setup

<div class="kb-summary">
Step-by-step guide to installing Git, configuring global settings, setting up SSH key authentication, and establishing a working local development environment.

*Applies to: Git 2.x*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
install_git: "Install Git" {shape: rectangle}
configure_global_user_settings: "Configure Global User Settings" {shape: rectangle}
set_up_ssh_key_authentication: "Set Up SSH Key Authentication" {shape: rectangle}
clone_first_repository: "Clone First Repository" {shape: rectangle}
configure_default_editor_and_diff_to: "Configure Default Editor and Diff Tool" {shape: rectangle}
set_up_gitignore: "Set Up .gitignore" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> install_git
install_git -> configure_global_user_settings
configure_global_user_settings -> set_up_ssh_key_authentication
set_up_ssh_key_authentication -> clone_first_repository
clone_first_repository -> configure_default_editor_and_diff_to
configure_default_editor_and_diff_to -> set_up_gitignore
set_up_gitignore -> validate
```

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


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 14 Nov 2024 09:47:22 AM UTC.
Dependencies resolved.
================================================================================
 Package             Arch         Version              Repository        Size
================================================================================
Installing:
 git                 x86_64       2.43.0-1.fc39        fedora           5.2 M

Transaction Summary
================================================================================
Install  1 Package

Total download size: 5.2 M
Installed size: 26 M
Downloading Packages:
git-2.43.0-1.fc39.x86_64.rpm                       100% |████████| 5.2 MB
Running transaction
  Preparing        :                                                    1/1
  Installing       : git-2.43.0-1.fc39.x86_64                          1/1
  Verifying        : git-2.43.0-1.fc39.x86_64                          1/1

Complete!
git version 2.43.0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sudo: command not found` | Install sudo with `dnf install sudo` or run the command as root directly. |
    | `Error: Unable to find a match: git` | Enable the fedora repository with `sudo dnf config-manager --set-enabled fedora` or check your internet connection. |
**Linux (Ubuntu/Debian):**

```bash
sudo apt update && sudo apt install git -y
git --version
```


```text title="Expected output"
Get:1 http://archive.ubuntu.com/ubuntu focal InRelease [265 kB]
Get:2 http://archive.ubuntu.com/ubuntu focal-updates InRelease [114 kB]
Get:3 http://security.ubuntu.com/ubuntu focal-security InRelease [114 kB]
Fetched 493 kB in 2s (246 kB/s)
Reading package lists... Done
Reading state information... Done
git is already the newest version (1:2.34.1-1ubuntu1.10).
0 upgraded, 0 newly installed, 0 removed.
git version 2.34.1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)` | Run the command with `sudo` or ensure your user has passwordless sudo configured. |
    | `E: Unable to locate package git` | Run `sudo apt update` first to refresh the package index before attempting installation. |
**macOS:**

```bash
# Install via Homebrew (recommended — keeps Git updated separately from Xcode)
brew install git
git --version

# Confirm Homebrew git takes precedence over Xcode git
which git  # should return /usr/local/bin/git or /opt/homebrew/bin/git
```


```text title="Expected output"
==> Downloading https://ghcr.io/v2/homebrew/core/git
==> Downloading from https://ghcr.io/v2/homebrew/core/git/blobs/sha256:a1b2c3d4e5f6
######################################################################## 100.0%
==> Pouring git--2.43.0.arm64_sonoma.bottle.tar.gz
🍺  /opt/homebrew/Cellar/git/2.43.0 (1,547 files, 42.3MB)
==> Running `brew link git`
Already linked: /opt/homebrew/opt/git
git version 2.43.0
/opt/homebrew/bin/git
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Could not symlink bin/git` | Run `brew link --overwrite git` to force symlink creation if another git installation is blocking it. |
    | `command not found: brew` | Install Homebrew first by running `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. |
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


```text title="Expected output"
user.name=Jane Smith
user.email=jane.smith@company.local
user.useConfigFile=true
user.signingkey=
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=false
core.precomposeunicode=true
init.defaultbranch=main
pull.rebase=false
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: key does not contain a section: user.name` | Ensure you are using `git config --global` (not `git config`) and that the syntax is exactly `git config --global user.name "Your Name"`. |
    | `fatal: not in a git repository` | The `--global` flag writes to `~/.gitconfig` regardless of location, so this error indicates a syntax issue; verify the command has no typos. |
**Set the default branch name for new repositories:**

```bash
git config --global init.defaultBranch main
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not in a git repository` | This command sets a global Git config and doesn't require a repository; if you see this error, you're likely in a corrupted git directory—try running the command outside any git folder. |
    | `error: key does not contain a section: init.defaultBranch` | Upgrade to Git 2.28 or later, as `init.defaultBranch` is not supported in older versions. |
**Set pull behaviour (rebase recommended for clean history):**

```bash
git config --global pull.rebase true
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: key does not contain a section: pull.rebase` | Upgrade Git to version 2.27 or later, which introduced the `pull.rebase` configuration option. |
    | `fatal: not in a git repository` | Run this command outside of a repository context; use `--global` flag (already present) or navigate into a Git repository and remove `--global` to set local config instead. |
**Confirm the full global config:**

```bash
cat ~/.gitconfig
```


```text title="Expected output"
[user]
	name = John Doe
	email = john.doe@company.com
[core]
	editor = vim
	autocrlf = false
[credential]
	helper = store
[alias]
	st = status
	co = checkout
	br = branch
[push]
	default = simple
[http]
	sslVerify = true
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: /home/username/.gitconfig: No such file or directory` | Run `git config --global user.name "Your Name"` and `git config --global user.email "your@email.com"` to initialize a global config file. |
    | `Permission denied` | Check file permissions with `ls -la ~/.gitconfig` and restore read access using `chmod 644 ~/.gitconfig`. |
---

## Set Up SSH Key Authentication

SSH key authentication is required for push access to GitHub, GitLab, Bitbucket, and most self-hosted Git servers.

**Generate an Ed25519 key pair:**

```bash
# Ed25519 is preferred over RSA for new keys
ssh-keygen -t ed25519 -C "jane.smith@company.local"
```


```text title="Expected output"
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/jane/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/jane/.ssh/id_ed25519
Your public key has been saved in /home/jane/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:kL9mP2xQvR8nJ5bK3cD7eF1gH4iL6mN9oP0sT2uV3wX jane.smith@company.local
The key's randomart image is:
+--[ED25519 256]--+
|        .o.      |
|       o.o .     |
|      . + o .    |
|       o + o     |
|      . S o .    |
+----[SHA256]-----+
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Generating public/private ed25519 key pair. Enter file in which to save the key (/home/jane/.ssh/id_ed25519): Permission denied` | Ensure the `.ssh` directory exists with `mkdir -p ~/.ssh` and has correct permissions `chmod 700 ~/.ssh`. |
    | `Enter passphrase (empty for no passphrase): No such file or directory` | Check that your home directory is accessible and writable; verify with `ls -la ~`. |
When prompted:
- **File location:** press Enter to accept the default (`~/.ssh/id_ed25519`)
- **Passphrase:** enter a passphrase (required for security — use the SSH agent to avoid re-entering it)

**Start the SSH agent and add the key:**

```bash
# Linux/macOS
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```


```text title="Expected output"
Agent pid 42857
Identity added: /home/ubuntu/.ssh/id_ed25519 (ubuntu@deployment-server)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Could not open a connection to your authentication agent.` | Ensure ssh-agent is running by executing `eval "$(ssh-agent -s)"` before attempting ssh-add. |
    | `Permission denied (publickey).` | Verify the private key file has correct permissions with `chmod 600 ~/.ssh/id_ed25519` and that the corresponding public key is authorized on the remote host. |
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


```text title="Expected output"
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKp7vJ8mQ2nRxL9vK4wPmZqT6sB3dN1xY9hJ2kL5mN6oP user@workstation-prod-01
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: /home/user/.ssh/id_ed25519.pub: No such file or directory` | Generate the key pair first with `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519`. |
    | `Permission denied` | Fix permissions on the `.ssh` directory with `chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_ed25519.pub`. |
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


```text title="Expected output"
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
Hi username! Welcome to GitLab, @username!
The authenticity of host 'git.company.local (192.168.1.42)' can't be established.
ECDSA key fingerprint is SHA256:aBcD1234eFgH5678iJkL9012mNoPqRsT.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'git.company.local,192.168.1.42' (ECDSA) to the known_hosts file.
Hi username! You've successfully authenticated to git.company.local.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey).` | Ensure your SSH public key is added to your Git provider's account settings and your SSH agent is running with `ssh-add ~/.ssh/id_rsa`. |
    | `ssh: Could not resolve hostname git.company.local: Name or service not known` | Verify the self-hosted Git server hostname is correct and resolvable via DNS or add it to your `/etc/hosts` file. |
    | `Connection refused` | Confirm the self-hosted Git server is running and SSH is listening on port 22, or use `-p <port>` if it runs on a non-standard port. |
Expected response (GitHub): `Hi jane.smith! You've successfully authenticated, but GitHub does not provide shell access.`

---

## Clone First Repository

**Clone via SSH (recommended after SSH key setup):**

```bash
git clone git@github.com:org/repo-name.git
cd repo-name
```


```text title="Expected output"
Cloning into 'repo-name'...
remote: Enumerating objects: 2847, done.
remote: Counting objects: 100% (2847/2847), done.
remote: Compressing objects: 100% (1203/1203), done.
remote: Receiving objects: 100% (2847/2847), done.
Resolving deltas: 100% (1654/1654), done.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `git@github.com: Permission denied (publickey).` | Ensure your SSH public key is added to your GitHub account and ssh-agent is running with `eval $(ssh-agent -s) && ssh-add ~/.ssh/id_rsa`. |
    | `fatal: could not read Username for 'https://github.com': terminal prompts disabled` | Use SSH URL format (`git@github.com:org/repo-name.git`) instead of HTTPS, or configure a personal access token for HTTPS authentication. |
    | `fatal: destination path 'repo-name' already exists and is not an empty directory.` | Remove or rename the existing `repo-name` directory before cloning, or clone into a different directory with `git clone git@github.com:org/repo-name.git new-dir-name`. |
**Clone via HTTPS (if SSH is not yet set up):**

```bash
git clone https://github.com/org/repo-name.git
cd repo-name
```


```text title="Expected output"
Cloning into 'repo-name'...
remote: Enumerating objects: 2847, done.
remote: Counting objects: 100% (2847/2847), done.
remote: Compressing objects: 100% (1203/1203), done.
remote: Receiving objects: 100% (2847/2847), 18.5 MiB | 12.3 MiB/s, done.
remote: Resolving deltas: 100% (1456/1456), done.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: unable to access 'https://github.com/org/repo-name.git/': Could not resolve host: github.com` | Verify network connectivity and DNS resolution with `ping github.com` or check firewall/proxy settings. |
    | `fatal: repository 'https://github.com/org/repo-name.git/' not found` | Confirm the repository URL is correct and you have access permissions; verify with `git ls-remote https://github.com/org/repo-name.git`. |
    | `fatal: destination path 'repo-name' already exists and is not an empty directory` | Remove or rename the existing directory with `rm -rf repo-name` before cloning. |
**Confirm the remote is set correctly:**

```bash
git remote -v
# Expected:
# origin  git@github.com:org/repo-name.git (fetch)
# origin  git@github.com:org/repo-name.git (push)
```


```text title="Expected output"
origin  git@github.com:org/repo-name.git (fetch)
origin  git@github.com:org/repo-name.git (push)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not a git repository (or any of the parent directories): .git` | Navigate to the root of a cloned git repository before running this command. |
    | `fatal: No remote named 'origin'` | The repository has no configured remote; add one with `git remote add origin <url>`. |
**Verify you can fetch updates:**

```bash
git fetch origin
git status
```


```text title="Expected output"
remote: Enumerating objects: 42, done.
remote: Counting objects: 100% (42/42), done.
remote: Compressing objects: 100% (18/18), done.
remote: Receiving objects: 100% (42/42), 8.92 KiB | 2.97 MiB/s, done.
remote: Resolving deltas: 100% (24/24), done.
From github.com:company/infrastructure
   a3f8c21..7e2d945  main       -> origin/main
   9b1c3e5..4f6a8d2  develop    -> origin/develop
On branch main
Your branch is behind 'origin/main' by 3 commits.
  (use "git pull" to update your branch)
nothing to commit, working tree clean
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not a git repository (or any of the parent directories): .git` | Ensure you are in the root directory of a cloned git repository. |
    | `fatal: unable to access 'https://github.com/company/infrastructure.git': Could not resolve host: github.com` | Verify network connectivity and that the remote URL is correctly configured with `git remote -v`. |
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: pathspec 'code' did not match any files` | Ensure VS Code is installed and in your PATH; run `code --version` to verify, then use the full path if needed (e.g., `/usr/bin/code`). |
    | `fatal: not in a git repository` | These are global config commands that work outside repos, but if you see this error, remove the `--global` flag to set local repo config instead. |
**Set the diff and merge tool:**

```bash
# Use VS Code as the diff and merge tool
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'

git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: could not expand include directive` | Ensure VS Code is installed and accessible in your system PATH; run `code --version` to verify. |
    | `fatal: bad config file at /home/user/.gitconfig` | Check for syntax errors in your `.gitconfig` file by opening it directly with `cat ~/.gitconfig` and ensure no lines are malformed. |
**Test the diff tool:**

```bash
# Make a small change to a tracked file, then run
git difftool HEAD
# VS Code (or the configured tool) should open showing the diff
```


```text title="Expected output"
(no output — command completes silently)
VS Code window opens with a diff view showing:
  Left pane (HEAD): original file content
  Right pane (working directory): modified file content
  Line numbers and syntax highlighting visible
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: no changes added to commit` | Ensure you've actually modified a tracked file; run `git status` to verify changes exist. |
    | `error: external diff tool not found` | Install your configured difftool (e.g., `code`, `vimdiff`) or set it with `git config --global diff.tool <toolname>`. |
    | `fatal: not a git repository` | Run this command from within a git repository root directory. |
**Enable colour output:**

```bash
git config --global color.ui auto
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: key does not contain a section: color.ui` | Use the correct syntax `git config --global color.ui auto` with the section name included (color is the section, ui is the key). |
    | `fatal: unable to write to /home/username/.gitconfig: Permission denied` | Run the command with appropriate permissions or check that your home directory is writable with `ls -ld ~`. |
---

## Set Up .gitignore

**Create a global .gitignore for files that should never be committed on this machine:**

```bash
touch ~/.gitignore_global
git config --global core.excludesfile ~/.gitignore_global
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not in a git repository` | These are global git config commands that work outside a repo; if you see this error, ensure git is installed and in your PATH with `which git`. |
    | `error: could not lock config file /home/user/.gitconfig: Permission denied` | Change permissions on your home directory or `.gitconfig` file with `chmod 644 ~/.gitconfig` and ensure your user owns it. |
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bash: ~/.gitignore_global: Permission denied` | Ensure your home directory is writable with `chmod u+w ~` or check disk space with `df -h`. |
    | `No such file or directory` | Create the parent directory first with `mkdir -p ~/.config/git` if using a non-standard location, or verify `~` expands correctly with `echo ~`. |
**Per-project .gitignore:**

Add a `.gitignore` in the root of each repository for project-specific patterns. Use `gitignore.io` (`https://www.toptal.com/developers/gitignore`) to generate language and framework-specific templates.

---

## Configure Credential Helper

The credential helper stores HTTPS credentials so you are not prompted on every push or fetch.

**macOS — use the Keychain:**

```bash
git config --global credential.helper osxkeychain
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not in a git repository` | This command sets a global Git config and doesn't require a repo; if you see this error, you're likely in a non-git directory, but the command will still succeed—ignore the error or run from any directory. |
    | `xcrun: error: unable to find utility` | The osxkeychain helper requires Xcode Command Line Tools; install them with `xcode-select --install`. |
**Linux — use the libsecret store (GNOME Keyring):**

```bash
sudo apt install libsecret-tools git-credential-libsecret  # Ubuntu
sudo make --directory=/usr/share/doc/git/contrib/credential/libsecret
git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
```


```text title="Expected output"
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  git-credential-libsecret libsecret-tools
0 upgraded, 2 newly installed, 0 removed.
Setting up libsecret-tools (0.20.5-1) ...
Setting up git-credential-libsecret (1:2.34.1-1ubuntu1) ...
make: Entering directory '/usr/share/doc/git/contrib/credential/libsecret'
gcc -o git-credential-libsecret git-credential-libsecret.c `pkg-config --cflags --libs libsecret-1`
make: Leaving directory '/usr/share/doc/git/contrib/credential/libsecret'
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `make: *** No rule to make target 'install'. Stop.` | The libsecret credential helper is pre-built in recent git versions; skip the `make` command and point credential.helper directly to the binary path. |
    | `fatal: not in a git repository` | The git config command succeeded but you're not in a repository; this is expected for `--global` config and does not prevent credential storage from working. |
    | `error: could not lock config file /home/user/.gitconfig: Permission denied` | Run the git config command without `sudo` to write to your user's home directory instead of root's. |
**Linux — cache credentials in memory for 1 hour:**

```bash
git config --global credential.helper 'cache --timeout=3600'
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: key contains invalid characters` | Ensure the timeout value is numeric only; remove any non-digit characters from the `--timeout` parameter. |
    | `fatal: not in a git repository` | This is a global config command that works outside repos, but if you see this error, verify git is installed with `git --version` and your PATH is correct. |
**Windows — use the Windows Credential Manager (set automatically by Git for Windows):**

```bash
git config --global credential.helper manager-core
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not in a git repository` | This command sets a global Git config and doesn't require a repository; if you see this error, you may have a shell alias or wrapper interfering—run the command with the full path `/usr/bin/git config --global credential.helper manager-core` instead. |
    | `error: key does not contain a section: credential.helper` | This indicates a corrupted Git config file; repair it by running `git config --global --unset credential.helper` followed by the original command. |
**GitHub — use the GitHub CLI for credential management:**

```bash
# Install gh CLI, then authenticate
gh auth login
# Follow prompts — select HTTPS, authenticate via browser
# gh configures the credential helper automatically
```


```text title="Expected output"
? What is your preferred protocol for Git operations on github.com? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: F4A2-B8C9
Press Enter to open github.com in your browser...

✓ Authentication complete.
✓ Logged in as: devops-admin
✓ Git credential helper configured for https://github.com
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Could not find git: git is not installed` | Install git first with `apt-get install git` (Ubuntu/Debian) or `brew install git` (macOS) before running `gh auth login`. |
    | `Error: Failed to authenticate: The redirect URI does not match the registered callback URLs` | Ensure you're using the correct GitHub organization/instance URL and that your browser can reach github.com without proxy/firewall blocking. |
    | `Error: authentication failed - could not read Username for 'https://github.com': terminal prompts disabled` | Run `gh auth login` interactively in a terminal (not in a non-interactive script context) or use `gh auth login --with-token` to provide a PAT instead. |
---

## Validate Setup

Run through the following checks to confirm the Git environment is fully configured.

**Identity and config:**

```bash
git config --global user.name    # must return your full name
git config --global user.email   # must return your email
git config --global --list       # review all settings
```


```text title="Expected output"
John Michael Patterson
john.patterson@company.com
user.name=John Michael Patterson
user.email=john.patterson@company.com
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
init.defaultbranch=main
pull.rebase=false
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not in a git repository` | Run these commands outside a repository or ensure git is properly initialized; the `--global` flag should work anywhere, so verify git is installed with `git --version`. |
    | `error: key does not contain a section: user.name` | The config key syntax is incorrect; use `git config --global user.name "Your Name"` to set values, or just `git config --global user.name` to read them. |
**SSH authentication:**

```bash
ssh -T git@github.com            # or your Git server
# Expected: authentication success message
```


```text title="Expected output"
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey).` | Ensure your SSH public key is added to your GitHub account and the private key is loaded in your SSH agent with `ssh-add ~/.ssh/id_rsa`. |
    | `ssh: Could not resolve hostname git@github.com: Name or service not known` | Verify your network connectivity and that DNS resolution is working; check `/etc/ssh/ssh_config` for correct hostname configuration. |
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


```text title="Expected output"
Initialized empty Git repository in /home/ubuntu/git-test/.git/
[master (root-commit) a3f7e2c] Initial commit
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
a3f7e2c Initial commit
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not a git repository (or any of the parent directories): .git` | Run `git init` before attempting to add or commit files. |
    | `*** Please tell me who you are. Run git config --global user.email "you@example.com" git config --global user.name "Your Name"` | Configure your Git identity with `git config --global user.email "your@email.com" && git config --global user.name "Your Name"` before committing. |
**Diff tool:**

```bash
# Modify README.md, then:
git diff README.md
# Output should be colour-formatted
```


```text title="Expected output"
diff --git a/README.md b/README.md
index 4e2c8f1..9a3d5e7 100644
--- a/README.md
+++ b/README.md
@@ -1,6 +1,8 @@
 # Project Documentation
 
-This is the main README file.
+This is the updated README file with new content.
+
+## New Section Added
 
 ## Installation
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not a git repository (or any of the parent directories): .git` | Initialize the repository with `git init` or clone an existing one with `git clone`. |
    | `No such file or directory` | Ensure README.md exists in the current directory; create it with `touch README.md` if needed. |
**Clone over SSH:**

```bash
# Clone a repository you have access to
git clone git@github.com:org/some-repo.git /tmp/clone-test
ls /tmp/clone-test
# Repository contents must be present
```


```text title="Expected output"
Cloning into '/tmp/clone-test'...
remote: Enumerating objects: 1247, done.
remote: Counting objects: 100% (1247/1247), done.
remote: Compressing objects: 100% (892/892), done.
remote: Receiving objects: 100% (1247/1247), done.
Resolving deltas: 100% (634/634), done.
README.md
src/
tests/
.gitignore
.github/
docs/
package.json
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey).` | Ensure your SSH key is added to the SSH agent with `ssh-add ~/.ssh/id_rsa` and that your public key is registered in GitHub. |
    | `fatal: destination path '/tmp/clone-test' already exists and is not an empty directory.` | Remove the existing directory with `rm -rf /tmp/clone-test` before cloning. |
    | `fatal: repository 'git@github.com:org/some-repo.git' not found.` | Verify the repository name and organization are correct, and that your account has access to the repository. |
**Confirm .gitignore is active:**

```bash
touch ~/.DS_Store
git -C ~/git-test status
# .DS_Store must not appear in the untracked files list
```


```text title="Expected output"
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not a git repository (or any of the parent directories): .git` | Initialize the repository first with `git init` or clone an existing repo into `~/git-test`. |
    | `.DS_Store` appears in the untracked files list` | Add `.DS_Store` to `.gitignore` with `echo ".DS_Store" >> ~/.gitignore` to exclude macOS system files from tracking. |
---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation

---

## See also

- [Git — Procedures](../operations/procedures/)
- [Git — Common Issues](../troubleshooting/common-issues/)
- [Git — How It Works](../architecture/how-it-works/)
