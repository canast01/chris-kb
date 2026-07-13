---
tags:
  - git
  - troubleshooting
search:
  boost: 1.5
---
# Git — Common Issues

```bash
# See which files are conflicted
git status
# "both modified:   src/config.go"

# Show the conflict markers in a file
git diff

# Use a 3-way diff tool
git mergetool
```


```text title="Expected output"
On branch feature/auth-update
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   src/config.go

no changes added to commit but unmerged paths present (in a merge)

diff --cc src/config.go
index 3d4e2a1,7f9c8b2..0000000
--- a/src/config.go
+++ b/src/config.go
@@@ -42,7 -40,9 +42,13 @@@
  	Port: 8080,
  	Debug: true,
++<<<<<<< HEAD
 +	Timeout: 30,
++||||||| merged common ancestor
++	Timeout: 15,
+++=======
+ 	Timeout: 45,
++>>>>>>> feature/auth-update
  }

Merging src/config.go
Normal merge conflict for 'src/config.go':
  {local}: modified file
  {remote}: modified file
Hit return to start merge resolution tool (vimdiff):
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: Your local changes to 'src/config.go' would be overwritten by merge` | Stash or commit your uncommitted changes before attempting the merge with `git stash` or `git add && git commit`. |
    | `fatal: mergetool: tool not found: vimdiff` | Install your preferred merge tool (e.g., `sudo apt-get install vim` on Linux) or configure an alternative with `git config merge.tool <toolname>`. |
```bash
# Enable rerere (re-use recorded resolution)
git config --global rerere.enabled true

# After resolving, rerere records the resolution automatically
# Future identical conflicts are resolved automatically
git rerere
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: not a git repository (or any of the parent directories): .git` | Run this command from within a git repository directory, or initialize one with `git init`. |
    | `error: could not lock config file /home/user/.gitconfig: Permission denied` | Check file permissions with `ls -la ~/.gitconfig` and ensure your user owns the file, or use `sudo` if intentionally configuring system-wide settings. |
```bash
git status
# HEAD detached at a1b2c3d

git log --oneline -5
```

```text title="Expected output"
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
a1b2c3d (HEAD) Fix: update deployment script for prod environment
f4e5d6c Merge pull request #847 from feature/auth-service
7g8h9i0 Refactor: consolidate config management utilities
2j3k4l5 Docs: add troubleshooting guide for git workflows
6m7n8o9 Initial commit with CI/CD pipeline setup
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: your current branch 'main' does not have any commits yet` | Initialize the repository with at least one commit using `git add . && git commit -m "Initial commit"`. |
    | `fatal: not a git repository (or any of the parent directories): .git` | Run `git init` to initialize a git repository in the current directory, or navigate to an existing git project root. |
```bash
# Return to wherever you were before
git switch -
# or
git checkout -
```

```text title="Expected output"
Switched to branch 'feature/auth-refactor'
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: pathspec '-' did not match any file(s) known to git` | You haven't switched branches yet in this session; use `git branch -a` to see available branches and switch to one first. |
    | `fatal: reference is not a tree: -` | Your previous branch was deleted; use `git switch <branch-name>` to switch to an existing branch instead. |
```bash
# Create a new branch at the current (detached) commit
git switch -c feature/save-my-work

# Or attach to an existing branch (only if no new commits were made)
git switch main
```

```text title="Expected output"
Switched to a new branch 'feature/save-my-work'
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: cannot switch branches while carrying a dirty working directory` | Commit or stash your changes with `git stash` before switching branches. |
    | `fatal: reference is not a tree: HEAD` | You are in a corrupted detached HEAD state; use `git reflog` to find a valid commit hash and run `git switch -c feature/save-my-work <commit-hash>`. |
```bash
# Return to main, discarding any uncommitted detached-HEAD changes
git switch main
# Any commits made in detached HEAD state are now unreachable (dangling)
# They will be garbage collected after ~2 weeks
```
```yaml
! [rejected] main -> main (non-fast-forward)
error: failed to push some refs to 'origin'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart.
```
```bash
# Fetch and rebase your commits on top of remote
git pull --rebase origin main

# Resolve any conflicts that arise during rebase
# Then push
git push origin main
```

```text title="Expected output"
remote: Counting objects: 47, done.
remote: Compressing objects: 100% (23/23), done.
remote: Unpacking objects: 100% (47/47), done.
From github.com:company/repo
   a3f8c2e..9d1b4f6  main       -> origin/main
First, rewinding head to replay your commits...
Applying: Add user authentication module
Applying: Update API endpoint documentation
Applying: Fix database connection pooling
Applying: Refactor logging configuration
Successfully rebased and updated refs/heads/main.
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 2.3 KiB | 512.00 KiB/s, done.
Total 8 (delta 5), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (5/5), done.
To github.com:company/repo.git
   9d1b4f6..c7e2a1f  main -> main
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `CONFLICT (content): Merge conflict in src/config.yml` | Manually resolve the conflicted file(s), run `git add <file>`, then execute `git rebase --continue`. |
    | `error: failed to push some refs to 'origin'` | Pull the latest changes with `git pull --rebase origin main` again, resolve any new conflicts, and retry the push. |
    | `fatal: Not a git repository (or any of the parent directories): .git` | Ensure you are in the correct repository directory and have initialized it with `git init` or cloned it with `git clone`. |
```bash
git pull origin main        # creates a merge commit
git push origin main
```

```text title="Expected output"
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (8/8), done.
remote: Unpacking objects: 100% (8/8), done.
From github.com:company/repo
 * branch            main       -> FETCH_HEAD
   a3f8e2c..b7d1f9a  main       -> origin/main
Merge made by the 'recursive' strategy.
 src/config.yaml | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 287 bytes | 287.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), done.
To github.com:company/repo.git
   b7d1f9a..c4e2b1f  main -> main
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: Your local changes to the following files would be overwritten by merge` | Commit or stash your uncommitted changes with `git stash` before pulling. |
    | `fatal: Not a git repository (or any of the parent directories): .git` | Ensure you are in the correct repository directory and it has been initialized with `git init` or cloned. |
```bash
# WARNING: rewrites remote history — never use on shared/protected branches
git push --force-with-lease origin feature/my-branch
# --force-with-lease is safer than --force: fails if someone else pushed since your last fetch
```

```text title="Expected output"
Enumerating objects: 42, done.
Counting objects: 100% (42/42), done.
Delta compression using up to 8 threads
Compressing objects: 100% (28/28), done.
Writing objects: 100% (42/42), 18.5 KiB | 2.3 MiB/s, done.
Total 42 (delta 15), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (15/15), done.
To github.com:myorg/myrepo.git
 + a7f3c9e...b2e1d4f feature/my-branch -> feature/my-branch (forced update)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `remote: error: refusing to allow a forced update of a protected branch` | Remove branch protection rules in your repository settings or push to an unprotected branch instead. |
    | `error: failed to push some refs to 'origin'` | Run `git fetch origin` to sync with remote changes, then rebase your commits and try again. |
    | `fatal: 'origin' does not appear to be a 'git' repository` | Verify your remote URL with `git remote -v` and ensure you have network access to the repository. |
```bash
# Via API — enable branch protection
curl -X POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/:id/protected_branches" \
  --data 'name=main&push_access_level=0&merge_access_level=40&allow_force_push=false'
```
```text
remote: error: File large-binary.bin is 150.00 MB; this exceeds GitHub's file size limit of 100.00 MB.
remote: error: GH001: Large files detected. You may want to try Git Large File Storage.
```
```bash
# Undo the last commit, keep changes staged
git reset --soft HEAD~1

# Remove the large file from staging
git rm --cached path/to/large-binary.bin
echo "path/to/large-binary.bin" >> .gitignore
git add .gitignore

git commit -m "Remove large binary; add to .gitignore"
```

```text title="Expected output"
[main 7a3f2c9] Remove large binary; add to .gitignore
 1 file changed, 1 insertion(+)
 create mode 100644 .gitignore
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: pathspec 'path/to/large-binary.bin' did not match any files` | Verify the exact file path and that the file was actually staged in the previous commit using `git status` or `git diff --cached`. |
    | `fatal: Not a git repository (or any of the parent directories): .git` | Ensure you are in the root directory of the git repository before running these commands. |
```bash
# Using git-filter-repo (recommended over BFG for complex cases)
pip install git-filter-repo
git filter-repo --invert-paths --path path/to/large-binary.bin

# Force push to all remotes (coordinate with team first)
git push --force-with-lease origin main

# --- OR --- using BFG Repo Cleaner (faster for simple cases)
bfg --delete-files large-binary.bin
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force origin main
```

```text title="Expected output"
Collecting git-filter-repo
  Downloading git-filter-repo-2.38.0.tar.gz (55.2 kB)
Installing collected packages: git-filter-repo
Successfully installed git-filter-repo-2.38.0
Parsed 247 commits
New history written in 0.186s; now repacking/cleaning...
Repacking your repo and cleaning out old unneeded objects
Enumerating objects: 1247, done.
Counting objects: 100% (1247/1247), done.
Delta compression using up to 8 threads
Compressing objects: 100% (892/892), done.
Writing objects: 100% (1247/1247), done.
Total 1247 (delta 634), reused 1247 (delta 634), pack-delta compression 9%
Updating refs: 100%
Ref refs/heads/main updated to abc123def456
To github.com:myorg/myrepo.git
 + 8f7a2c9...abc123d main -> main (forced update)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: pathspec 'path/to/large-binary.bin' did not match any files` | Verify the exact file path relative to repository root using `git ls-files | grep binary`. |
    | `! [rejected] main -> main (protected branch)` | Unprotect the branch in your Git hosting platform (GitHub/GitLab/Bitbucket) settings before force-pushing. |
    | `fatal: Not a valid object name` | Ensure you've run `git filter-repo` successfully and the reflog hasn't been pruned; check `git log --oneline | head -5` to confirm history exists. |
```bash
# Install LFS
git lfs install

# Track the file pattern
git lfs track "*.bin"
git lfs track "*.zip"
git add .gitattributes

# Migrate existing history (all branches)
git lfs migrate import --include="*.bin" --everything

git push --force-with-lease origin main
```
```text
remote: HTTP Basic: Access denied
fatal: Authentication failed for 'https://gitlab.example.com/org/repo.git'
```
```bash
# Check which credential store is active
git config --global credential.helper

# List cached credentials (macOS Keychain)
git credential-osxkeychain erase <<EOF
protocol=https
host=github.com
EOF

# Test authentication
curl -sf -u username:TOKEN https://api.github.com/user | jq .login
```

```text title="Expected output"
osxkeychain
(no output — command completes silently)
"octocat"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: could not read Username for 'https://github.com': terminal prompts disabled` | Ensure the credential helper is properly configured with `git config --global credential.helper osxkeychain` and that Keychain access permissions are granted. |
    | `curl: (22) The requested URL returned error: 401 Unauthorized` | Verify the personal access token (TOKEN) is valid, has not expired, and includes the required `user:email` scope for API access. |
    | `jq: parse error: Invalid JSON text at line 1` | Check that the curl request succeeded (remove `-s` flag temporarily to see the actual response) and that the token has sufficient permissions to access `/user` endpoint. |
```bash
# macOS — remove cached entry and let Git re-prompt
git credential-osxkeychain erase <<EOF
protocol=https
host=github.com
EOF
git fetch   # will prompt for new credentials

# Linux (libsecret / GNOME keyring)
git config --global credential.helper libsecret

# Linux (store in plain file — not recommended for production)
git config --global credential.helper store
# Credentials stored in ~/.git-credentials

# Use a new PAT in the URL directly (temporary)
git remote set-url origin https://oauth2:NEW_TOKEN@gitlab.example.com/org/repo.git

# Git Credential Manager (cross-platform)
git credential-manager-core erase
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
Username for 'https://github.com': your_username
Password for 'https://your_username@github.com': 
remote url updated to https://oauth2:NEW_TOKEN@gitlab.example.com/org/repo.git
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: credential-osxkeychain not found` | Install Git via Homebrew (`brew install git`) or Xcode Command Line Tools to include the osxkeychain helper. |
    | `fatal: could not read Username for 'https://github.com': Device not configured` | Ensure the credential helper is properly installed and configured with `git config --global credential.helper <helper-name>`. |
    | `fatal: remote origin already exists` | Use `git remote set-url origin <new-url>` instead of `git remote add` when updating an existing remote. |
```bash
# Verify new token works
curl -H "Authorization: Bearer $NEW_TOKEN" https://api.github.com/user | jq .login

# Update remote URL with new token (use credential store instead when possible)
git remote set-url origin https://github.com/org/repo.git
git config --global credential.helper osxkeychain   # or manager-core
```
```text
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```
```bash
# Test SSH connection with verbose output
ssh -vT git@github.com
ssh -vT git@gitlab.example.com

# Check which key is being offered
ssh-add -l

# Check known_hosts
ssh-keygen -F github.com
```

```text title="Expected output"
OpenSSH_8.2p1 Ubuntu 4ubuntu0.7, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /home/devops/.ssh/config
debug1: Offering public key: /home/devops/.ssh/id_rsa RSA SHA256:aBcD1234efGH5678ijKL9012mnOP3456qrST7890uv
debug1: Server accepts key: perm denied (publickey).
Permission denied (publickey).

OpenSSH_8.2p1 Ubuntu 4ubuntu0.7, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /home/devops/.ssh/config
debug1: Offering public key: /home/devops/.ssh/id_rsa RSA SHA256:aBcD1234efGH5678ijKL9012mnOP3456qrST7890uv
debug1: Server accepts key: perm denied (publickey).
Permission denied (publickey).

2048 SHA256:aBcD1234efGH5678ijKL9012mnOP3456qrST7890uv /home/devops/.ssh/id_rsa (RSA)
4096 SHA256:xYz9876qwERT5432asDF1098lkJH6543mnBV2109cxZ /home/devops/.ssh/id_ed25519 (ED25519)

# Host github.com found in /home/devops/.ssh/known_hosts
|1|G7h3K9mL2pQ8vN5xR4tY6uZ1wA==|aBcD1234efGH5678ijKL9012mnOP3456qrs= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmNzlCYvJxMP7mlG2o29fEHsNvLbwIffqzr2KJYbIW9...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey).` | Verify the public key is added to your Git provider's account settings and the private key has correct permissions (chmod 600). |
    | `Could not open a connection to your authentication agent.` | Start the SSH agent with `eval $(ssh-agent -s)` before running ssh-add. |
    | `Host key verification failed.` | Add the host key to known_hosts by running `ssh-keyscan -H github.com >> ~/.ssh/known_hosts` and retry the connection. |
```bash
# Start agent if not running
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Verify
ssh-add -l

# Persist across reboots (macOS)
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

```text title="Expected output"
Agent pid 42857
Identity added: /Users/admin/.ssh/id_ed25519 (admin@workstation.local)
256 SHA256:aBcD1EfGhIjKlMnOpQrStUvWxYz2345678901234567 /Users/admin/.ssh/id_ed25519 (ED25519)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Could not open a connection to your authentication agent.` | Run `eval "$(ssh-agent -s)"` before attempting to add keys. |
    | `Permission denied (publickey).` | Ensure the private key file has 600 permissions with `chmod 600 ~/.ssh/id_ed25519` and the public key is added to the remote server's `~/.ssh/authorized_keys`. |
    | `The specified item could not be found in the keychain.` | On macOS, the key may not exist at that path; verify with `ls -la ~/.ssh/id_ed25519` and regenerate if needed using `ssh-keygen -t ed25519`. |
```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub via API
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/keys \
  -d "{\"title\":\"$(hostname)\",\"key\":\"$(cat ~/.ssh/id_ed25519.pub)\"}"

# Add to GitLab via API
curl -X POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/user/keys" \
  --data "title=$(hostname)&key=$(cat ~/.ssh/id_ed25519.pub)"
```

```text title="Expected output"
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKp7vN2xQ8mR9jL4kP1sT5uW6yZ3aB9cD2eF4gH5iJ6kL user@workstation
{"id":12847563,"key":"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKp7vN2xQ8mR9jL4kP1sT5uW6yZ3aB9cD2eF4gH5iJ6kL","url":"https://api.github.com/user/keys/12847563","title":"workstation-prod-01","created_at":"2024-01-15T09:23:47Z"}
{"id":5,"key":"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKp7vN2xQ8mR9jL4kP1sT5uW6yZ3aB9cD2eF4gH5iJ6kL","title":"workstation-prod-01","created_at":"2024-01-15T09:24:12Z"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to api.github.com port 443: Connection refused` | Verify network connectivity and that GitHub/GitLab API endpoints are accessible from your environment. |
    | `{"message":"Bad credentials","documentation_url":"https://docs.github.com/rest"}` | Ensure `$GITHUB_TOKEN` or `$GITLAB_TOKEN` environment variables are set with valid, unexpired tokens. |
    | `jq: parse error: Invalid numeric literal at line 1 column 10` | The API response contains an error message instead of JSON; check token permissions include `write:public_keys` scope. |
```bash
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes

Host gitlab.example.com
    HostName gitlab.example.com
    User git
    IdentityFile ~/.ssh/id_ed25519_gitlab
    IdentitiesOnly yes
    Port 22
```
```text
error: Server does not allow request for unadvertised object
fatal: remote error: upload-pack: not our ref
```
```bash
# Initialise and clone all submodules recursively
git submodule update --init --recursive

# Clone with submodules from the start
git clone --recurse-submodules https://github.com/org/repo.git
```

```text title="Expected output"
Cloning into '/path/to/repo'...
remote: Enumerating objects: 4521, done.
remote: Counting objects: 100% (4521/4521), done.
remote: Compressing objects: 100% (2847/2847), done.
remote: Receiving objects: 100% (4521/4521), done.
Resolving deltas: 100% (1674/1674), done.
Submodule 'vendor/lib-core' (https://github.com/org/lib-core.git) registered for path 'vendor/lib-core'
Submodule 'vendor/lib-utils' (https://github.com/org/lib-utils.git) registered for path 'vendor/lib-utils'
Cloning into '/path/to/repo/vendor/lib-core'...
remote: Enumerating objects: 892, done.
remote: Receiving objects: 100% (892/892), done.
Resolving deltas: 100% (421/421), done.
Submodule(s) registered for path 'vendor/lib-utils'
Cloning into '/path/to/repo/vendor/lib-utils'...
remote: Enumerating objects: 1247, done.
remote: Receiving objects: 100% (1247/1247), done.
Resolving deltas: 100% (589/589), done.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: could not read Username for 'https://github.com': No such file or directory` | Ensure SSH keys are configured or use a personal access token in the HTTPS URL format `https://username:token@github.com/org/repo.git`. |
    | `fatal: clone of 'https://github.com/org/repo.git' into submodule path 'vendor/lib-core' failed` | Verify the submodule repository exists and is accessible; check `.gitmodules` file for correct URLs. |
    | `error: Server does not allow request for unadvertised object` | Update Git to the latest version and ensure all submodule commits are pushed to the remote repository. |
```bash
# Check submodule status
git submodule status

# Update all submodules to the commit recorded in the parent repo
git submodule update --recursive

# Update submodule to remote HEAD (use with caution — changes the pinned commit)
git submodule update --remote --merge

# Force-reset a submodule to its recorded commit
git submodule foreach git reset --hard
git submodule update --recursive
```

```text title="Expected output"
a1f2b3c4d5e6f7g8h9i0j1k2l3m4n5o6 submodules/terraform-aws (heads/main)
 b2g3c4d5e6f7g8h9i0j1k2l3m4n5o6p7 submodules/ansible-roles (v2.1.0)
 c3h4d5e6f7g8h9i0j1k2l3m4n5o6p7q8 submodules/monitoring-stack (detached HEAD)
Entering 'submodules/terraform-aws'
Entering 'submodules/ansible-roles'
Entering 'submodules/monitoring-stack'
Updating submodule 'submodules/terraform-aws'
Updating submodule 'submodules/ansible-roles'
Updating submodule 'submodules/monitoring-stack'
HEAD is now at a1f2b3c Update provider versions
HEAD is now at b2g3c4d Bump role dependencies
HEAD is now at c3h4d5e Add Prometheus scrape configs
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: No url found for submodule path 'submodules/terraform-aws' in .gitmodules` | Verify the submodule entry exists in `.gitmodules` and run `git submodule sync` to refresh the configuration. |
    | `error: Your local changes to the following files would be overwritten by merge` | Commit or stash uncommitted changes in the submodule directory before running `git submodule update --remote --merge`. |
```bash
# Check what changed
git submodule foreach git status
git submodule foreach git diff

# Fix file mode differences
git submodule foreach git config core.fileMode false

# Reset silently modified submodule
git submodule foreach git checkout -- .
```

```text title="Expected output"
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
Entering 'vendor/logging'
On branch v2.3.1
HEAD detached at a1f2e9c
nothing to commit, working tree clean

Entering 'vendor/auth-service'
On branch main
HEAD detached at 3c4d8b7
Changes not staged for commit:
  modified:   src/handler.go
  modified:   config/defaults.yaml

Entering 'vendor/logging'
diff --git a/src/logger.go b/src/logger.go
index 4a2c8e1..7f3d9c2 100644
--- a/src/logger.go
+++ b/src/logger.go
@@ -12,3 +12,5 @@ func Init() {
   fmt.Println("Logger initialized")
 }

Entering 'vendor/auth-service'
(no output — command completes silently)

Entering 'vendor/logging'
(no output — command completes silently)

Entering 'vendor/auth-service'
Updated 2 paths from the index
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: No submodules found in .gitmodules` | Verify submodules are initialized with `git submodule update --init --recursive` before running foreach commands. |
    | `error: pathspec '.' did not match any files` | Ensure you are in the repository root directory and submodules are properly cloned with `git submodule update --init`. |
```bash
# Proper removal — three steps required
git submodule deinit -f path/to/submodule
git rm -f path/to/submodule
rm -rf .git/modules/path/to/submodule
git commit -m "Remove submodule path/to/submodule"
```

```text title="Expected output"
Cleared directory path/to/submodule
Rm 'path/to/submodule'
rm: removing directory '.git/modules/path/to/submodule'
[main a7f3c2e] Remove submodule path/to/submodule
 1 file changed, 4 deletions(-)
 delete mode 160000 path/to/submodule
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: No submodule mapping found in .gitmodules for path 'path/to/submodule'` | Verify the exact submodule path with `git config --file .gitmodules --name-only --get-regexp path` before running deinit. |
    | `error: the following file has staged content different from both the file and the working tree: path/to/submodule` | Run `git reset HEAD path/to/submodule` before attempting `git rm -f` to unstage the submodule entry. |
```bash
# Show full config (effective, merged from all scopes)
git config --list --show-origin

# Show all remotes
git remote -v

# Show current branch tracking info
git branch -vv

# Show reflog (last 20 operations — useful for recovery)
git reflog -20

# Show what changed between local and remote
git fetch origin
git log origin/main..HEAD --oneline    # commits you have, remote doesn't
git log HEAD..origin/main --oneline    # commits remote has, you don't
git diff origin/main...HEAD            # diff of diverged changes
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "Push rejected\n— git pull --rebase then push" {shape: rectangle}
R2: "Push rejected\n— git push --force-with-lease" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Merge conflict\n— git mergetool for interactive resolution" {shape: rectangle}
R4: "Merge conflict\n— edit conflict markers then git add" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "Detached HEAD\n— git switch -c new-branch to save work" {shape: rectangle}
R6: "Detached HEAD\n— git switch main to return to branch" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "SSH auth\n— ssh-add key then verify with ssh -T" {shape: rectangle}
R8: "SSH auth\n— check public key added to remote host" {shape: rectangle}
B5: "B5" {shape: rectangle}
R9: "Submodule issues\n— git submodule update --init --recursive" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "B4" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
D4 -> R7
D4 -> R8
B5 -> R9
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Git — Diagnostics](../diagnostics/)
- [Git — Escalation](../escalation/)
- [Git — Health Checks](../../operations/health-checks/)
