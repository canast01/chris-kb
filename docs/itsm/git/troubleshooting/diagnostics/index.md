---
tags:
  - git
  - troubleshooting
search:
  boost: 1.5
description: "Git diagnostic techniques: enable GIT_TRACE environment variables for protocol-level debug output, verify remote URLs and connectivity with git ls-remote..."
---
# Git — Diagnostics

<div class="kb-summary">
Git diagnostic techniques: enable GIT_TRACE environment variables for protocol-level debug output, verify remote URLs and connectivity with git ls-remote, use ssh -vvvT to diagnose SSH key and host verification failures, check git config for proxy and credential settings, recover lost commits and branches with git reflog, and collect a sanitised diagnostic bundle for escalation.

*Applies to: Git 2.x*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
D: "Check network:\ngit ls-remote origin\nping github.com" {shape: rectangle}
E: "Run git fsck --full" {shape: rectangle}
F: "git config --list --show-origin" {shape: rectangle}
C: "C" {shape: rectangle}
G: "GIT_TRACE_CURL=1 git fetch\nCheck HTTP status code" {shape: rectangle}
H: "ssh -vvvT git@host\nCheck key offered: ssh-add -l" {shape: rectangle}
I: "Token expired or wrong scope\nRotate PAT or re-authenticate" {shape: rectangle}
J: "Check repo permissions\nCheck org SSO enforcement" {shape: rectangle}
K: "Set git config http.proxy\nor http_proxy env var" {shape: rectangle}
L: "git config http.sslVerify\nVerify CA bundle: git config http.sslCAInfo" {shape: rectangle}
M: "M" {shape: rectangle}
N: "ssh-add ~/.ssh/id_ed25519" {shape: rectangle}
O: "Key not registered on platform\nAdd public key to account" {shape: rectangle}
P: "Server key changed or MITM\nVerify fingerprint out-of-band\nssh-keyscan to update known_hosts" {shape: rectangle}
Q: "Firewall blocking port 22 or 443\nTry SSH over HTTPS: ssh -p 443 git@ssh.github.com" {shape: rectangle}
R: "Check /etc/resolv.conf\nnslookup github.com" {shape: rectangle}
S: "CORRUPTION — restore from mirror backup\nContact platform support" {shape: rectangle}
T: "Normal — safe to prune\ngit prune --expire=2.weeks.ago" {shape: rectangle}
U: "git remote set-url origin correct-url" {shape: rectangle}
V: "git mergetool" {shape: rectangle}
W: "Resolved" {shape: rectangle}
X: "Escalate to platform support" {shape: rectangle}
A: "Git command fails" {shape: rectangle}

B -> D
B -> E
B -> F
C -> G
C -> H
G -> I
G -> J
G -> K
G -> L
M -> N
M -> O
H -> P
D -> Q
D -> R
E -> S
E -> T
F -> U
F -> V
I -> W
J -> W
K -> W
L -> W
N -> W
O -> W
P -> W
Q -> W
R -> W
S -> X
T -> W
U -> W
V -> W
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_enable_trace_logging: "Step 1 — Enable trace logging" {shape: rectangle}
step_2_verify_remote_connectivity: "Step 2 — Verify remote connectivity" {shape: rectangle}
step_3_inspect_git_configuration: "Step 3 — Inspect git configuration" {shape: rectangle}
step_4_diagnose_ssh_authentication: "Step 4 — Diagnose SSH authentication" {shape: rectangle}
step_5_diagnose_https_authentication: "Step 5 — Diagnose HTTPS authentication and proxy" {shape: rectangle}
step_6_recover_lost_work: "Step 6 — Recover lost work" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_enable_trace_logging: investigate
symptom -> step_2_verify_remote_connectivity: investigate
symptom -> step_3_inspect_git_configuration: investigate
symptom -> step_4_diagnose_ssh_authentication: investigate
symptom -> step_5_diagnose_https_authentication: investigate
symptom -> step_6_recover_lost_work: investigate
step_1_enable_trace_logging -> resolution
step_2_verify_remote_connectivity -> resolution
step_3_inspect_git_configuration -> resolution
step_4_diagnose_ssh_authentication -> resolution
step_5_diagnose_https_authentication -> resolution
step_6_recover_lost_work -> resolution
```

## Before you begin

- **Access:** terminal access on the affected workstation; SSH key files in `~/.ssh/`; git config at `~/.gitconfig`; admin access to the remote Git platform (GitHub, GitLab, Bitbucket) to verify key registration and permissions
- **Gather first:** the exact error message text, the git command that failed, the remote URL (`git remote -v`), the transport being used (SSH or HTTPS), and whether the issue is repository-specific or affects all repos
- **Scope:** confirm whether the issue is: one command on one repo, all git operations, a specific remote, or a specific user — this determines whether it is a credential, network, or repository-integrity issue
- **Safety:** `GIT_TRACE_CURL` may expose authorization headers; always redact before sharing outputs with support teams

---

## Step 1 — Enable trace logging

Git environment variables activate protocol-level debug output without modifying config files.

```bash
# Basic command trace — shows every git operation step
GIT_TRACE=1 git fetch origin

# Redirect trace output to a log file (useful for long operations)
GIT_TRACE=/tmp/git-trace.log git push origin main
cat /tmp/git-trace.log

# Enable multiple traces simultaneously
GIT_TRACE=1 GIT_TRACE_PERFORMANCE=1 GIT_TRACE_SETUP=1 git status

# Performance profiling — identify slow operations
GIT_TRACE_PERFORMANCE=1 git log --oneline -100 2>&1 | grep "performance"

# Pack protocol trace — for clone/fetch/push object negotiation
GIT_TRACE_PACKET=1 git fetch origin 2>&1 | head -80

# HTTP/HTTPS header trace
GIT_CURL_VERBOSE=1 git fetch 2>&1 | head -60

# Full curl trace including auth headers (redact before sharing)
GIT_TRACE_CURL=1 git fetch 2>&1 | sed 's/Authorization: Basic .*/Authorization: Basic <REDACTED>/'
```


```text title="Expected output"
trace: built-in: git 'fetch' 'origin'
trace: run_command: 'ssh' '-o' 'SendEnv=GIT_PROTOCOL' 'git@github.com' 'git-upload-pack '\''/myorg/myrepo.git'\'''
trace: exec: 'ssh' '-o' 'SendEnv=GIT_PROTOCOL' 'git@github.com' 'git-upload-pack '\''/myorg/myrepo.git'\'''
From github.com:myorg/myrepo
   a3f8c21..9e2d1b4  main       -> origin/main
   5c7a9e1..6d4b2f8  develop    -> origin/develop

trace: performance: 0.042000 s: git command: 'fetch' 'origin'
trace: setup: git_dir: .git
trace: setup: worktree: /home/user/myrepo
trace: setup: cwd: /home/user/myrepo
trace: setup: prefix: (null)

performance: 0.156 s: read-tree
performance: 0.089 s: traverse_trees
performance: 0.034 s: diff-index

* 0000000000000000000000000000000000000000 9e2d1b4f8c3a5d7e1f2b4c6a8d9e1f2b3c4d5e6f refs/heads/main
* 5c7a9e1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f 6d4b2f8a9c1d3e5f7a9b0c1d2e3f4a5b6c7d8e9 refs/heads/develop
```

!!! warning "Common errors"
    **`fatal: could not read Username for 'https://github.com': No such file or directory`** — Configure SSH keys or use a personal access token with `git config --global credential.helper store`.
    **`fatal: The remote end hung up unexpectedly`** — Check network connectivity and SSH key permissions with `ssh -T git@github.com`; increase timeout with `git config --global http.postBuffer 524288000`.
    **`trace: run_command: 'ssh' ... fatal: Could not resolve hostname`** — Verify DNS resolution with `nslookup github.com` and check SSH config in `~/.ssh/config` for correct Host entries.
---

## Step 2 — Verify remote connectivity

```bash
# Show all remotes with fetch and push URLs
git remote -v
# origin  git@github.com:org/repo.git (fetch)
# origin  git@github.com:org/repo.git (push)

# Show full remote configuration
git remote show origin

# Test that the remote is reachable and list its refs (confirms auth + connectivity)
git ls-remote origin

# Check if a specific ref exists on the remote
git ls-remote origin refs/heads/main
git ls-remote origin refs/tags/v1.0.0
```


```text title="Expected output"
origin  git@github.com:acme-corp/infra-automation.git (fetch)
origin  git@github.com:acme-corp/infra-automation.git (push)

* remote origin
  Fetch URL: git@github.com:acme-corp/infra-automation.git
  Push  URL: git@github.com:acme-corp/infra-automation.git
  HEAD branch: main
  Remote branches:
    develop tracked
    main    tracked
    release/v2.1.0 tracked
  Local branches configured for 'git pull':
    main merges with remote main
    develop merges with remote develop
  Local refs configured for 'git push':
    main pushes to main (up to date)
    develop pushes to develop (up to date)

5f8c3a2e9b1d4f6a7c8e9f0a1b2c3d4e5f6a7b8c	HEAD
a9f2e1d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2	refs/heads/develop
7c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d	refs/heads/main
2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a	refs/tags/v1.9.5
9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d	refs/tags/v2.0.0
4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d	refs/tags/v2.1.0

a9f2e1d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2	refs/heads/main

(no output — ref does not exist on remote)
```

!!! warning "Common errors"
    **`fatal: 'origin' does not appear to be a 'git' repository`** — Verify you are in a git repository root directory with `git rev-parse --git-dir`.
    **`Permission denied (publickey). fatal: Could not read from remote repository.`** — Ensure your SSH key is added to the SSH agent with `ssh-add ~/.ssh/id_rsa` and registered in your GitHub account.
    **`fatal: repository not found`** — Confirm the remote URL is correct and you have access to the repository with `git remote set-url origin <correct-url>`.
`git ls-remote origin` is the fastest test — it authenticates and fetches the remote ref list. If this succeeds, the auth and network path are working. If it fails, the error message narrows the problem to DNS, firewall, auth, or permissions.

---

## Step 3 — Inspect git configuration

```bash
# List all effective config (merged: system → global → local → worktree)
git config --list

# Show config with source file for each key
git config --list --show-origin

# Show only local repo config
git config --local --list

# Show only global user config
git config --global --list

# Get a specific key
git config user.email
git config --get remote.origin.url
git config --get core.sshCommand

# Key config items to verify during troubleshooting
git config user.name
git config user.email
git config core.autocrlf
git config http.proxy
git config http.sslVerify
git config credential.helper
git config core.sshCommand

# Safe config dump — redact secrets before sharing
git config --list --show-origin | grep -v -i "password\|secret\|token\|key"
```


```text title="Expected output"
user.name=Alice Chen
user.email=alice.chen@company.com
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=false
core.autocrlf=input
http.sslVerify=true
credential.helper=osxkeychain
remote.origin.url=https://github.com/company/infrastructure.git
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
core.sshCommand=ssh -i ~/.ssh/id_rsa_deploy -o StrictHostKeyChecking=accept-new
branch.main.remote=origin
branch.main.merge=refs/heads/main

file:/etc/gitconfig	core.autocrlf=false
file:/home/alice/.gitconfig	user.name=Alice Chen
file:/home/alice/.gitconfig	user.email=alice.chen@company.com
file:/home/alice/.gitconfig	credential.helper=osxkeychain
file:.git/config	remote.origin.url=https://github.com/company/infrastructure.git
file:.git/config	core.sshCommand=ssh -i ~/.ssh/id_rsa_deploy -o StrictHostKeyChecking=accept-new

user.name=Alice Chen
user.email=alice.chen@company.com
remote.origin.url=https://github.com/company/infrastructure.git
core.sshCommand=ssh -i ~/.ssh/id_rsa_deploy -o StrictHostKeyChecking=accept-new

user.name=Alice Chen
user.email=alice.chen@company.com
credential.helper=osxkeychain

alice.chen@company.com
https://github.com/company/infrastructure.git
ssh -i ~/.ssh/id_rsa_deploy -o StrictHostKeyChecking=accept-new

Alice Chen
alice.chen@company.com
input
(not set)
true
osxkeychain
ssh -i ~/.ssh/id_rsa_deploy -o StrictHostKeyChecking=accept-new

file:/etc/gitconfig	core.autocrlf=false
file:/home/alice/.gitconfig	user.name=Alice Chen
file:/home/alice/.gitconfig	user.email=alice.chen@company.com
file:/home/alice/.gitconfig	credential.helper=osxkeychain
file:.git/config	remote.origin.url=https://github.com/company/infrastructure.git
file:.git/config	core.sshCommand=ssh -i ~/.ssh/id_rsa_deploy -o StrictHostKeyChecking=accept-new
```

!!! warning "Common errors"
    **`error: key does not contain a section: user.email`** — Ensure you're running `git config` inside a valid git repository or use `--global` flag for user-level config.
    **`fatal: not a git repository (or any of the parent directories): .git`** — Navigate to the root of a git repository before running config commands, or use `--global` to query system-wide settings.
---

## Step 4 — Diagnose SSH authentication

```bash
# Basic verbose SSH test to GitHub
ssh -vT git@github.com

# Triple-verbose for full protocol trace
ssh -vvvT git@github.com

# Test to GitLab
ssh -vvvT git@gitlab.example.com

# Test to GitLab on a non-standard port
ssh -vvvT -p 2222 git@gitlab.example.com
```


```text title="Expected output"
OpenSSH_8.2p1 Ubuntu 4ubuntu0.7, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /home/devops/.ssh/config
debug1: No more authentication methods to try.
Permission denied (publickey).

debug1: Authentications that can continue: publickey
debug1: Next authentication method: publickey
debug1: Offering public key: /home/devops/.ssh/id_rsa RSA SHA256:aBcD1234EfGhIjKlMnOpQrStUvWxYz5678+9/0AbCdE
debug1: Server accepted our key
Hi octocat! You've successfully authenticated, but GitHub does not provide shell access.
Connection to github.com closed.

debug1: Reading configuration data /home/devops/.ssh/config
debug1: Authentications that can continue: publickey
debug1: Offering public key: /home/devops/.ssh/id_rsa RSA SHA256:aBcD1234EfGhIjKlMnOpQrStUvWxYz5678+9/0AbCdE
debug1: Server accepted our key
Hi devops-team! You've successfully authenticated, but GitLab does not provide shell access.
Connection to gitlab.example.com closed.

debug1: Connecting to gitlab.example.com [192.168.1.42] port 2222.
debug1: Connection established.
debug1: Authentications that can continue: publickey
debug1: Offering public key: /home/devops/.ssh/id_rsa RSA SHA256:aBcD1234EfGhIjKlMnOpQrStUvWxYz5678+9/0AbCdE
debug1: Server accepted our key
Hi devops-team! You've successfully authenticated, but GitLab does not provide shell access.
Connection to gitlab.example.com port 2222 closed.
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Verify the public key is added to your Git provider account and the private key path in ~/.ssh/config matches your actual key file.
    **`ssh: connect to host gitlab.example.com port 2222: Connection refused`** — Confirm the GitLab SSH service is running on port 2222 and any firewall rules allow outbound connections to that port.
    **`Could not resolve hostname gitlab.example.com: Name or service not known`** — Check DNS resolution with `nslookup gitlab.example.com` and verify the hostname is correct in your SSH config.
Key signatures in `ssh -vvvT` output:

```yaml
# Key being offered
debug1: Offering public key: /Users/user/.ssh/id_ed25519 ED25519
# Platform's response to the offered key:
debug1: Authentications that can continue: publickey
# Successful auth:
debug1: Authentication succeeded (publickey).

# Common failure signatures:
# "Permission denied (publickey)" — key not registered on remote
# "No supported authentication methods available" — server config issue
# "Host key verification failed" — known_hosts mismatch
# "Connection refused" — wrong host/port or firewall block
# "Connection timed out" — firewall or network routing issue
```

```bash
# Check the SSH config being applied
ssh -G git@github.com | grep -E "^(hostname|user|port|identityfile|identitiesonly)"

# List keys currently loaded in the SSH agent
ssh-add -l

# If no agent is running or no keys loaded:
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Test with explicit key (bypass agent)
ssh -i ~/.ssh/id_ed25519 -vT git@github.com

# Check known_hosts
ssh-keygen -F github.com
ssh-keygen -F gitlab.example.com

# Regenerate known_hosts entry if server key changed (after verifying legitimacy)
ssh-keygen -R github.com
ssh-keyscan -H github.com >> ~/.ssh/known_hosts

# Use custom SSH flags for a single git command
GIT_SSH_COMMAND="ssh -vvv -i ~/.ssh/id_ed25519" git fetch origin

# Set permanently in repo config for troubleshooting session
git config core.sshCommand "ssh -vvv -i ~/.ssh/id_ed25519"
# Remember to unset when done
git config --unset core.sshCommand
```


```text title="Expected output"
hostname github.com
user git
port 22
identityfile ~/.ssh/id_ed25519
identitiesonly yes

2048 SHA256:nThbg6kXUpJWGl7E1IGOCspRQsbqNsZc5zcA7xHCVNU git@github.com (RSA)

SSH_AUTH_SOCK=/tmp/ssh-XXXX1a2b3c/agent.12345; export SSH_AUTH_SOCK;
SSH_AGENT_PID=12346; export SSH_AGENT_PID;
Identity added: /home/ubuntu/.ssh/id_ed25519 (user@workstation)

OpenSSH_8.2p1 Ubuntu 4ubuntu0.7, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /home/ubuntu/.ssh/config
debug1: Offering public key: /home/ubuntu/.ssh/id_ed25519 ED25519 SHA256:aBcD1e2fGhIjKlMnOpQrStUvWxYz3a4B5c6DeF7gHiJ
debug1: Server accepts key: /home/ubuntu/.ssh/id_ed25519 ED25519 SHA256:aBcD1e2fGhIjKlMnOpQrStUvWxYz3a4B5c6DeF7gHiJ
debug1: Authentication succeeded (publickey).
Hi username! You've successfully authenticated, but GitHub does not provide shell access.

# github.com:22 SSH-2.0-libssh_0.8.9
github.com found in /home/ubuntu/.ssh/known_hosts:1

gitlab.example.com not found in /home/ubuntu/.ssh/known_hosts

Host key verification changed. Offending RSA key in /home/ubuntu/.ssh/known_hosts:5
/home/ubuntu/.ssh/known_hosts updated successfully.
# github.com:22 SSH-2.0-libssh_0.8.9
github.com|1|AbCdEfGhIjKlMnOpQrStUvWxYz=|1a2b3c4d5e6f7g8h9i0j= ecdsa-sha2-nistp256 AAAA...

remote: Enumerating objects: 42, done.
remote: Counting objects: 100% (42/42), done.
remote: Compressing objects: 100% (28/28), done.
Receiving objects: 100% (42/42), 15.23 KiB | 2.54 MiB/s, done.

(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Verify the private key path is correct and readable (`ls -la ~/.ssh/id_ed25519`), then confirm the public key is added to your Git hosting provider's SSH keys.
    **`Could not open a connection to your authentication agent.`** — Start the SSH agent with `eval "$(ssh-agent -s)"` before running `ssh-add`.
    **`Host key verification failed.`** — Run `ssh-keyscan -H github.com >> ~/.ssh/
---

## Step 5 — Diagnose HTTPS authentication and proxy

```bash
# Show HTTP credential helper in use
git config credential.helper

# Test HTTPS connectivity with full header trace
GIT_TRACE_CURL=1 git ls-remote origin 2>&1 | grep -E "^> |^< HTTP"

# Check if a proxy is set (relevant in corporate environments)
git config http.proxy
echo $http_proxy
echo $https_proxy

# Test HTTPS through a proxy explicitly
git config http.proxy http://proxy.corp.example.com:8080
git ls-remote origin   # test
git config --unset http.proxy   # revert

# SSL verification
git config http.sslVerify       # should be true
git config http.sslCAInfo       # custom CA bundle path if set

# Disable SSL verify temporarily to test if cert is the issue (TESTING ONLY — revert immediately)
git -c http.sslVerify=false ls-remote origin

# Refresh GitHub PAT credential
git credential reject <<'EOF'
protocol=https
host=github.com
EOF
# Next git operation will prompt for new credentials
```


```text title="Expected output"
store
* Connected to github.com (140.82.113.3) port 443 (#0)
> GET /repos/acme-corp/infrastructure.git/info/refs?service=git-upload-pack HTTP/1.1
< HTTP/1.1 200 OK
http://proxy.corp.example.com:8080
http://proxy.corp.example.com:8080
https://proxy.corp.example.com:8080
Fetching refs from origin...
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
true
/etc/ssl/certs/custom-ca-bundle.crt
* Connected to github.com (140.82.113.3) port 443 (#0)
> GET /repos/acme-corp/infrastructure.git/info/refs?service=git-upload-pack HTTP/1.1
< HTTP/1.1 200 OK
```

!!! warning "Common errors"
    **`fatal: unable to access 'https://github.com/...': Could not resolve host: github.com`** — Check DNS resolution with `nslookup github.com` and verify network connectivity; if behind a proxy, ensure `git config http.proxy` is set correctly.
    **`fatal: unable to access 'https://github.com/...': SSL certificate problem: self signed certificate`** — Verify the certificate with `openssl s_client -connect github.com:443` and either update your CA bundle path via `git config http.sslCAInfo /path/to/ca-bundle.crt` or contact your security team if using a corporate proxy.
    **`fatal: unable to access 'https://github.com/...': The requested URL returned error: 401`** — Refresh your GitHub PAT credentials by running the `git credential reject` block above, then retry the operation to be prompted for new credentials.
---

## Step 6 — Recover lost work

### Recover a lost commit

```bash
# See what HEAD was before the reset
git reflog | head -10
# abc1234 HEAD@{0}: reset: moving to HEAD~1
# def5678 HEAD@{1}: commit: Add important feature   <-- this is the lost commit

# Show reflog with timestamps
git reflog --format='%C(auto)%h %gd %gs %cr%Creset' | head -30

# Restore it
git cherry-pick def5678
# or create a branch at that point
git branch recover/lost-commit def5678
```


```text title="Expected output"
abc1234 HEAD@{0}: reset: moving to HEAD~1
def5678 HEAD@{1}: commit: Add important feature
9f2c1e0 HEAD@{2}: commit: Update documentation
4a7b3d2 HEAD@{3}: commit: Fix bug in auth module
8e9f5c1 HEAD@{4}: clone: clone from origin/main
c3d2e1f HEAD@{5}: initial commit

abc1234 HEAD@{0}: reset: moving to HEAD~1 2 minutes ago
def5678 HEAD@{1}: commit: Add important feature 5 minutes ago
9f2c1e0 HEAD@{2}: commit: Update documentation 12 minutes ago
4a7b3d2 HEAD@{3}: commit: Fix bug in auth module 25 minutes ago
8e9f5c1 HEAD@{4}: clone: clone from origin/main 2 hours ago

[main abc1234] Add important feature
 Date: Thu Jan 16 14:32:18 2025 +0000
 2 files changed, 47 insertions(+), 3 deletions(-)
 create mode 100644 src/features/new-feature.py

Branch 'recover/lost-commit' set up to track 'def5678'.
```

!!! warning "Common errors"
    **`fatal: bad revision 'def5678'`** — Verify the commit hash from `git reflog` output is correct and hasn't been garbage collected by running `git gc --aggressive` to preserve reflog entries.
    **`error: commit def5678 is not an ancestor of HEAD`** — Use `git cherry-pick def5678` instead of `git rebase` if the commit is not in the current branch's history.
### Recover a deleted branch

```bash
# Find the commit the branch pointed to
git reflog | grep "checkout: moving from deleted-branch"
# or search by branch name
git reflog --all | grep deleted-branch | head -5

# Recreate the branch
git branch recovered-branch <sha-from-reflog>
git switch recovered-branch
```


```text title="Expected output"
0a1f2c3 HEAD@{0}: checkout: moving from main to deleted-branch
5e7d8b9 HEAD@{1}: checkout: moving from deleted-branch to main
0a1f2c3 HEAD@{2}: commit: Add authentication module
7c4e9f1 HEAD@{3}: commit: Update dependencies
a2b3c4d HEAD@{4}: checkout: moving from deleted-branch to feature/auth

0a1f2c3 deleted-branch@{0}: commit: Add authentication module
5e7d8b9 deleted-branch@{1}: checkout: moving from main to deleted-branch

Created branch 'recovered-branch' based on 0a1f2c3
Switched to branch 'recovered-branch'
```

!!! warning "Common errors"
    **`fatal: your current branch 'deleted-branch' does not have any commits yet`** — Run `git reflog --all` instead of `git reflog` to search across all refs, not just HEAD.
    **`error: pathspec '0a1f2c3' did not match any file(s) known to git`** — Ensure you copied the full SHA from reflog output (at least 7 characters) and use it directly in `git branch recovered-branch <sha>` without quotes or extra whitespace.
### Recover a dropped stash

```bash
# List unreachable commits (includes dropped stashes)
git fsck --unreachable | grep commit | awk '{print $3}' | \
  xargs git log --merges --no-walk --oneline

# Apply a recovered stash by SHA
git stash apply <sha>
```


```text title="Expected output"
commit 3f8a2e1c9d7b4a6f5e2c1a9d8b7f6e5d4c3b2a1f
commit 7e5d4c3b2a1f9e8d7c6b5a4f3e2d1c0b9a8f7e6d
commit 2a1f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2
commit 9d8b7f6e5d4c3b2a1f9e8d7c6b5a4f3e2d1c0b9
commit 5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d7c6b

WIP on develop: 4f3e2d1c Merge pull request #847 from feature/auth-refactor
index 1a2b3c4d..5e6f7g8h 100644
--- a/src/auth.js
+++ b/src/auth.js
@@ -12,3 +12,7 @@ function validateToken(token) {
+  // Recovery successful
```

!!! warning "Common errors"
    **`fatal: Not a valid object name`** — Verify the SHA exists in `git fsck --unreachable` output and copy it exactly without truncation.
    **`No stash entries found`** — Ensure you're using a commit SHA from the unreachable list, not a stash reference; use `git stash apply <sha>` only for stashes recovered via fsck.
### Recover staged content discarded by checkout

```bash
# If content was staged (git add) before checkout:
git fsck --lost-found
ls .git/lost-found/other/   # blobs that were staged but not committed
```


```text title="Expected output"
Checking object database for consistency...
Checking commits...
Checking trees...
Checking blobs...
Checking refs...
dangling blob 3a7f9e2c1b4d8f6a9e2c1b4d8f6a9e2c
dangling blob 5f2e8d1c9b4a7f6e3d2c1b0a9f8e7d6c
dangling blob 8c9b2a1f7e6d5c4b3a2f1e0d9c8b7a6f
ls: cannot access '.git/lost-found/other/': No such file or directory
```

!!! warning "Common errors"
    **`ls: cannot access '.git/lost-found/other/': No such file or directory`** — Run `git fsck --lost-found` first to populate the lost-found directory, or check that you're in the root of a Git repository.
    **`fatal: Not a git repository (or any of the parent directories): .git`** — Navigate to the root directory of your Git repository before running these commands.
---

## Step 7 — Collect diagnostic bundle

Run this script from within the affected repository. Review the output before sharing — it sanitises secrets but verify manually.

```bash
#!/usr/bin/env bash
# collect-git-diagnostics.sh — run from within the affected repository
OUTPUT_FILE="git-diagnostics-$(date +%Y%m%d-%H%M%S).txt"

{
  echo "=== Git Diagnostics ==="
  echo "Collected: $(date -u)"
  echo ""

  echo "--- Git Version ---"
  git version

  echo ""
  echo "--- Config (sanitized) ---"
  git config --list --show-origin | grep -v -iE "password|secret|token|key"

  echo ""
  echo "--- Remote URLs ---"
  git remote -v

  echo ""
  echo "--- Branch Status ---"
  git branch -vv

  echo ""
  echo "--- Last 10 Reflog Entries ---"
  git reflog -10

  echo ""
  echo "--- Object Count ---"
  git count-objects -vH

  echo ""
  echo "--- SSH Config ---"
  ssh -G git@github.com 2>/dev/null | grep -E "^(hostname|user|port|identityfile)"

  echo ""
  echo "--- SSH Keys in Agent ---"
  ssh-add -l 2>&1

  echo ""
  echo "--- Network: github.com ---"
  curl -sv --max-time 10 https://github.com 2>&1 | head -30

} > "$OUTPUT_FILE" 2>&1

echo "Diagnostics written to: $OUTPUT_FILE"
echo "Review before sharing to ensure no secrets are present."
```


```text title="Expected output"
=== Git Diagnostics ===
Collected: 2024-01-15 14:32:47 UTC

--- Git Version ---
git version 2.43.0

--- Config (sanitized) ---
file:/etc/gitconfig	core.editor=vim
file:/home/devops/.gitconfig	user.name=DevOps Team
file:/home/devops/.gitconfig	user.email=devops@company.internal
file:.git/config	remote.origin.url=git@github.com:company/repo.git
file:.git/config	core.bare=false

--- Remote URLs ---
origin	git@github.com:company/repo.git (fetch)
origin	git@github.com:company/repo.git (push)

--- Branch Status ---
* main                    a7f3e2c [origin/main] Merge pull request #847
  develop                 c1b9d44 [origin/develop: ahead 3] Update CI pipeline
  hotfix/sec-patch        8e2f1a9 [origin/hotfix/sec-patch] Security patch for CVE-2024-1234

--- Last 10 Reflog Entries ---
a7f3e2c HEAD@{0}: pull: Fast-forward
c1b9d44 HEAD@{1}: checkout: moving from develop to main
8e2f1a9 HEAD@{2}: rebase -i (finish): returning to refs/heads/develop
...

--- Object Count ---
count: 4521
size: 18.42 MiB
in-pack: 4156
packs: 2
size-pack: 17.89 MiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes

--- SSH Config ---
hostname github.com
user git
port 22
identityfile /home/devops/.ssh/id_rsa
identityfile /home/devops/.ssh/id_ed25519

--- SSH Keys in Agent ---
2048 SHA256:nThgk45Cby5aj8FD3aPEb7W8osSAkNRy2K1Xj9mK4vQ /home/devops/.ssh/id_rsa (RSA)
256 SHA256:jL8nM2pQ9vX3yZ1aBcDeFgHiJkLmNoPqRsTuVwXyZaB /home/devops/.ssh/id_ed25519 (ED25519)

--- Network: github.com ---
*   Trying 140.82.113.3:443...
* Connected to github.com (140.82.113.3) port 443 (#0)
* TLS 1.3 connection using TLS_AES_128_GCM_SHA256
* Server certificate: sha256/WoiWtaLaL7z1yP8IqJ4xwQa307gCHMx3V8zI2fV4ucU=
HTTP/2 200
...

Diagnostics written to: git-diagnostics-20240115-143247.txt
Review before sharing to ensure no secrets are present.
```

!!! warning "Common errors"
    **`fatal: not a git repository (or any of the parent directories): .git`** — Ensure the script is
---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| Trace log | `GIT_TRACE=/tmp/git-trace.log git <cmd>` | Internal operation sequence, timing |
| Curl trace | `GIT_TRACE_CURL=1 git fetch 2>&1` | HTTP status codes, auth headers |
| SSH trace | `ssh -vvvT git@host 2>&1` | Key offered, auth method, host key |
| Pack protocol | `GIT_TRACE_PACKET=1 git fetch 2>&1` | Object negotiation, pack statistics |
| Reflog | `git reflog` | History of all ref movements including lost commits |
| Object store | `git fsck --full` | Missing objects, dangling refs, corrupt packs |
| Config | `git config --list --show-origin` | Proxy, SSL, credential, SSH settings |
| Diagnostic bundle | `collect-git-diagnostics.sh` | All-in-one — attach to support ticket |

---

## See also

- [Git — Common Issues](../common-issues/)
- [Git — Escalation](../escalation/)
- [Git — Health Checks](../../operations/health-checks/)

## Verify resolution

- `git ls-remote origin` succeeds and returns the current ref list with no errors
- `ssh -vT git@github.com` returns `Hi <user>! You've successfully authenticated` (GitHub) or equivalent
- The git command that was failing now completes successfully: `git fetch origin`, `git push origin main`
- `git fsck --full` shows no missing or corrupt objects
- `git config --get remote.origin.url` shows the correct remote URL for the repository
