---
tags:
  - git
  - operations
---
# Git — Operations Procedures

```bash
# Common prefixes
feature/  — New functionality (feature/add-login-page)
fix/      — Bug fixes (fix/null-pointer-on-startup)
chore/    — Maintenance, deps, config (chore/upgrade-node-18)
docs/     — Documentation changes (docs/update-api-reference)
hotfix/   — Urgent production fixes (hotfix/payment-timeout)
release/  — Release preparation (release/v2.4.0)
```


```text title="Expected output"
(no output — command completes silently)
```
```bash
# Set upstream when pushing for the first time
git push -u origin feature/PLAT-42-s3-lifecycle

# Check tracking relationships
git branch -vv

# Change the upstream for an existing branch
git branch --set-upstream-to=origin/main feature/PLAT-42-s3-lifecycle

# Push to a differently named remote branch
git push origin local-branch:remote-branch
```

```text title="Expected output"
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (12/12), 2.3 KiB | 2.3 MiB/s, done.
Total 12 (delta 5), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (5/5), done.
remote: Create a pull request for 'feature/PLAT-42-s3-lifecycle' on GitHub by visiting:
remote: https://github.com/acme-corp/infrastructure/pull/new/feature/PLAT-42-s3-lifecycle
To github.com:acme-corp/infrastructure.git
 * [new branch]      feature/PLAT-42-s3-lifecycle -> feature/PLAT-42-s3-lifecycle
Branch 'feature/PLAT-42-s3-lifecycle' set up to track remote branch 'feature/PLAT-42-s3-lifecycle' from 'origin'.

* feature/PLAT-42-s3-lifecycle 4a7c9e2 [origin/feature/PLAT-42-s3-lifecycle] Add S3 lifecycle policy for archive tier
  main                           c2f1b8d [origin/main: ahead 3] Merge pull request #847 from ops/hotfix-vpc
  develop                        8e3a5f1 [origin/develop: behind 2] Update terraform modules

Branch 'feature/PLAT-42-s3-lifecycle' set to track remote branch 'main' from 'origin'.

Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:acme-corp/infrastructure.git
 + 4a7c9e2...c2f1b8d feature/PLAT-42-s3-lifecycle -> remote-branch (forced update)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: The current branch feature/PLAT-42-s3-lifecycle has no upstream branch.` | Run `git push -u origin feature/PLAT-42-s3-lifecycle` to set the upstream before pushing. |
    | `error: src refspec local-branch does not match any file or directory` | Verify the local branch exists with `git branch -a` and use the correct branch name in the push command. |
```bash
# Merge feature into main (creates merge commit)
git switch main
git merge feature/PLAT-42-s3-lifecycle

# Rebase feature branch onto updated main
git switch feature/PLAT-42-s3-lifecycle
git rebase main

# Interactive rebase to squash last 3 commits
git rebase -i HEAD~3

# Abort a rebase in progress
git rebase --abort
```

```text title="Expected output"
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
Merge made by the 'recursive' strategy.
 src/lifecycle/policy.py | 42 ++++++++++++++++++++++++++++++++++++------
 src/lifecycle/config.yaml | 8 ++++++++
 2 files changed, 44 insertions(+), 2 deletions(-)
Switched to branch 'feature/PLAT-42-s3-lifecycle'
Your branch is behind 'main' by 2 commits, and can be diverged by 3 commits.
Successfully rebased and updated refs/heads/feature/PLAT-42-s3-lifecycle.
pick 7a3c9e1 Add S3 lifecycle policy parser
pick 8f2d1b4 Implement retention rules
pick 9c4e6d2 Add unit tests for lifecycle

# Rebase in progress; onto 8a1f5c3
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the message
# s, squash <commit> = use commit, but meld into previous
# f, fixup <commit> = like "squash", but discard this commit's log message
# d, drop <commit> = remove commit
# e, edit <commit> = use commit, but stop for amending

Current branch feature/PLAT-42-s3-lifecycle is up to date with 'main'.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: Your local changes to the following files would be overwritten by merge: src/lifecycle/policy.py` | Commit or stash uncommitted changes with `git stash` before switching branches. |
    | `error: cannot rebase: You have unstaged changes.` | Stage all changes with `git add .` and commit them before rebasing. |
    | `error: could not apply 7a3c9e1... Add S3 lifecycle policy parser` | Resolve merge conflicts in the affected files, then run `git rebase --continue` to resume the rebase. |
```bash
# Find branches with no commits ahead of main
git branch --merged main

# Find branches with no recent activity (older than 90 days)
git for-each-ref --sort=committerdate refs/heads/ \
  --format='%(committerdate:short) %(refname:short)' \
  | awk '$1 < "'$(date -v-90d +%Y-%m-%d)'"'
```

```text title="Expected output"
develop
  feature/auth-redesign
  feature/logging-improvements
  hotfix/security-patch
  release/v2.1.0

2024-08-15 legacy/old-dashboard
2024-07-22 feature/deprecated-api
2024-06-10 bugfix/mysql-timeout
2024-05-30 experimental/ml-pipeline
2024-04-18 archive/payment-v1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: your current branch 'main' does not have any commits yet` | Initialize main with at least one commit before running branch merge checks. |
    | `date: illegal time format` | Use `date -d "90 days ago" +%Y-%m-%d` on Linux or `date -v-90d +%Y-%m-%d` on macOS; adjust syntax for your OS. |
```bash
# View full reflog
git reflog

# View reflog for a specific branch
git reflog show feature/my-branch

# Reflog with timestamps
git reflog --date=iso

# Find the commit hash before a bad reset
git reflog | grep "before reset"
```

```text title="Expected output"
e2a4f9c HEAD@{0}: reset: moving to HEAD~3
7b1d2e8 HEAD@{1}: commit: Fix authentication bug in login module
a9c3f1b HEAD@{2}: commit: Add user validation checks
5d6e7a2 HEAD@{3}: merge: Merge branch 'hotfix/security-patch'
c4b8f9e HEAD@{4}: checkout: moving from main to feature/my-branch
2f1a3d7 HEAD@{5}: commit: Update API documentation
8e9c2b1 HEAD@{6}: reset: moving to HEAD~1

e2a4f9c HEAD@{0}: reset: moving to HEAD~3
7b1d2e8 HEAD@{1}: commit: Fix authentication bug in login module
a9c3f1b HEAD@{2}: commit: Add user validation checks

e2a4f9c 2024-01-15T14:32:18+00:00 HEAD@{0}: reset: moving to HEAD~3
7b1d2e8 2024-01-15T14:28:45+00:00 HEAD@{1}: commit: Fix authentication bug in login module
a9c3f1b 2024-01-15T14:15:22+00:00 HEAD@{2}: commit: Add user validation checks
5d6e7a2 2024-01-15T13:52:09+00:00 HEAD@{3}: merge: Merge branch 'hotfix/security-patch'

5d6e7a2 merge: Merge branch 'hotfix/security-patch'
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: your current branch 'feature/my-branch' does not have any commits yet` | Ensure you're in a repository with commit history; initialize the repo and make at least one commit first. |
    | `fatal: bad revision 'feature/my-branch'` | Verify the branch name exists by running `git branch -a` and use the correct branch name in the reflog command. |
```bash
# Soft reset — keep changes staged
git reset --soft HEAD~1

# Mixed reset (default) — keep changes unstaged
git reset HEAD~1

# Hard reset — discard all changes (destructive)
git reset --hard HEAD~1

# Reset to a specific commit hash
git reset --hard a1b2c3d4

# Undo a reset using reflog
git reset --hard HEAD@{3}
```

```text title="Expected output"
Unstaged changes after reset:
M  src/config.yaml
M  docs/README.md
D  legacy/old-script.sh

HEAD is now at 7f9e8d2 Merge pull request #445 from feature/auth-overhaul
HEAD is now at a1b2c3d4 Fix database connection pooling
HEAD is now at 5c4b3a2 Initial commit
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: ambiguous argument 'HEAD@{3}': unknown revision or malformed revision` | Check available reflog entries with `git reflog` and use a valid index (e.g., `HEAD@{0}`, `HEAD@{1}`). |
    | `error: Your local changes to the following files would be overwritten by merge: src/config.yaml` | Stash uncommitted changes with `git stash` before running the hard reset, or use `git reset --mixed` to preserve them unstaged. |
```bash
# Revert the most recent commit
git revert HEAD

# Revert a specific commit
git revert a1b2c3d4

# Revert a range of commits (oldest first)
git revert a1b2c3d4..e5f6g7h8

# Revert without auto-committing (batch multiple reverts)
git revert -n a1b2c3d4
git revert -n b2c3d4e5
git commit -m "revert: undo broken deployment commits"

# Revert a merge commit (specify parent branch)
git revert -m 1 <merge-commit-hash>
```

```text title="Expected output"
[main a1b2c3d] Revert "Deploy v2.3.1 to production"
 1 file changed, 12 deletions(-)
[main e5f6g7h] Revert "Fix database migration script"
 1 file changed, 8 insertions(+), 5 deletions(-)
[main f7g8h9i] Revert "Add broken feature flag"
 1 file changed, 3 deletions(-)
[main g8h9i0j] revert: undo broken deployment commits
 2 files changed, 15 deletions(-)
[main h9i0j1k] Revert "Merge pull request #847 from feature/auth-redesign"
 4 files changed, 42 deletions(-)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: commit a1b2c3d4 is a merge but no -m option was given.` | Add the `-m 1` or `-m 2` flag to specify which parent branch to revert to. |
    | `error: could not apply a1b2c3d4... <commit message>` | Resolve the merge conflict manually in your editor, then run `git revert --continue` to complete the revert. |
```bash
# Step 1: find the tip commit of the deleted branch in reflog
git reflog | grep "branch-name"

# Step 2: recreate the branch at that commit
git switch -c recovered-branch a1b2c3d4

# Alternative: search all unreachable commits
git fsck --lost-found
ls .git/lost-found/commit/
```

```text title="Expected output"
a1b2c3d4 HEAD@{12}: checkout: moving from main to branch-name
7f8e9d0c HEAD@{13}: commit: Fix authentication module
2k3l4m5n HEAD@{14}: checkout: moving from branch-name to main

Switched to a new branch 'recovered-branch'

.git/lost-found/commit/:
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7
c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: pathspec 'a1b2c3d4' did not match any file(s) known to git` | Verify the commit hash exists in reflog output and copy it exactly, including all characters. |
    | `fatal: A branch named 'recovered-branch' already exists.` | Use a different branch name or delete the existing branch first with `git branch -D recovered-branch`. |
```bash
# Find dangling commits (not reachable from any ref)
git fsck --no-reflogs | grep "dangling commit"

# Inspect a dangling commit
git show <dangling-commit-hash>

# Recover by creating a branch
git switch -c recovery-branch <dangling-commit-hash>

# If you know the commit was recent, check reflog
git reflog --all | head -30
```

```text title="Expected output"
dangling commit 7a3f9c2e1b4d6f8a9c0e1d2f3a4b5c6d7e8f9a0b
dangling commit 2f4e8d1c9b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e
commit 7a3f9c2e1b4d6f8a9c0e1d2f3a4b5c6d7e8f9a0b
Author: devops-team <devops@company.internal>
Date:   Wed Mar 15 14:32:18 2024 +0000

    WIP: database migration rollback script

    - Added connection pooling logic
    - Reverted schema changes for v2.1.0

7a3f9c2e1b4d6f8a9c0e1d2f3a4b5c6d7e8f9a0b HEAD@{0}: commit: WIP: database migration rollback script
4f2e1d8c9b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e HEAD@{1}: reset: moving to main
9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b HEAD@{2}: commit: Add monitoring alerts
2f4e8d1c9b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e HEAD@{3}: checkout: switching from feature/auth to main
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: bad revision '<dangling-commit-hash>'` | Replace the placeholder with an actual commit hash from the fsck output (e.g., `git show 7a3f9c2e1b4d6f8a9c0e1d2f3a4b5c6d7e8f9a0b`). |
    | `fatal: A branch named 'recovery-branch' already exists.` | Use a unique branch name or delete the existing branch first with `git branch -D recovery-branch`. |
```bash
# List all stashes
git stash list

# Apply a specific stash without removing it
git stash apply stash@{2}

# Drop a stash after applying
git stash drop stash@{2}

# Find stashes lost after git stash drop
git fsck --no-reflogs | grep "dangling commit" | awk '{print $3}' | \
  xargs -I{} git stash show {}
```


```text title="Expected output"
stash@{0}: WIP on main: a3f2e1c Update deployment config
stash@{1}: WIP on develop: 7b9c4d2 Fix database connection pool
stash@{2}: WIP on hotfix/auth: 2e1f8a9 Revert SSL certificate change
stash@{3}: On main: 1c5d3e7 Temporary logging changes

On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

dangling commit 4f2a8e1b3c5d9e7f6a2b1c3d4e5f6a7b
 app/config.py | 12 ++++++++----
 services/auth.py | 8 +-------
 2 files changed, 8 insertions(+), 12 deletions(-)

dangling commit 9e7f6a2b1c3d4e5f6a7b8c9d0e1f2a3b
 database/migrations.sql | 45 +++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 45 insertions(+)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: Your local changes to the following files would be overwritten by merge:` | Commit or stash your current working changes before applying a stash. |
    | `error: No stash entries found.` | Verify the stash index exists with `git stash list` before referencing it. |
---

```d2
direction: right

create_a_repository: "Create a Repository" {shape: rectangle}
clone_a_repository: "Clone a Repository" {shape: rectangle}
create_and_switch_branches: "Create and Switch Branches" {shape: rectangle}
commit_and_push_changes: "Commit and Push Changes" {shape: rectangle}
create_a_merge_request_pull_request: "Create a Merge Request / Pull Request" {shape: rectangle}
resolve_a_merge_conflict: "Resolve a Merge Conflict" {shape: rectangle}

create_a_repository -> clone_a_repository
clone_a_repository -> create_and_switch_branches
create_and_switch_branches -> commit_and_push_changes
commit_and_push_changes -> create_a_merge_request_pull_request
create_a_merge_request_pull_request -> resolve_a_merge_conflict
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Create a Repository

Set up a new repository in the UI or locally and connect to a remote.

GitLab/GitHub UI: navigate to **New Repository** → set name, visibility (public / private / internal), optionally initialise with a README → copy the clone URL.

CLI (local init then push):

```bash
git init <name>
cd <name>
git remote add origin <url>
git add README.md
git commit -m "init"
git push -u origin main
```


```text title="Expected output"
Initialized empty Git repository in /home/user/myproject/.git/
On branch main

No commits yet

nothing to commit (create/create files and then "git commit")
[main (root-commit) a3f8e2c] init
 1 file changed, 5 insertions(+)
 create mode 100644 README.md
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 279 bytes | 279.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (0/0), done.
To github.com:username/myproject.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: pathspec 'README.md' did not match any files` | Create the README.md file before running `git add README.md`. |
    | `fatal: 'origin' does not appear to be a 'git' repository` | Verify the remote URL is correct and accessible with `git remote -v`. |
    | `error: src refspec main does not match any branch` | Ensure your default branch matches the remote (check with `git branch` and verify remote branch name). |
---

## Clone a Repository

Download a copy of an existing repository to a local working directory.

```bash
# HTTPS clone (uses username + token)
git clone https://<host>/<owner>/<repo>.git

# SSH clone (uses SSH key)
git clone git@<host>:<owner>/<repo>.git
```


```text title="Expected output"
Cloning into '<repo>'...
remote: Enumerating objects: 2847, done.
remote: Counting objects: 100% (2847/2847), done.
remote: Compressing objects: 100% (1203/1203), done.
remote: Receiving objects: 100% (2847/2847), done.
Resolving deltas: 100% (1456/1456), done.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: could not read Username for 'https://<host>': No such device or address` | Ensure your token is set in `~/.git-credentials` or use `git config --global credential.helper store` after entering credentials once. |
    | `fatal: Could not read from remote repository. Please make sure you have the correct access rights and the repository exists.` | Verify your SSH key is added to the Git server (`ssh-add ~/.ssh/id_rsa`) and your public key is registered in your account's SSH keys. |
    | `fatal: repository '<url>' not found` | Confirm the repository URL is correct, the owner/repo names match exactly, and you have access permissions to the repository. |
After cloning, verify `git status` shows a clean working tree before making changes.

---

## Create and Switch Branches

Create a feature branch from the latest main and push it to the remote to enable pull requests.

```bash
# Create and switch (legacy syntax)
git checkout -b feature/my-branch

# Create and switch (modern syntax)
git switch -c feature/my-branch

# Push the new branch and set upstream tracking
git push -u origin feature/my-branch
```


```text title="Expected output"
Switched to a new branch 'feature/my-branch'
Switched to a new branch 'feature/my-branch'
Enumerating objects: 42, done.
Counting objects: 100% (42/42), done.
Delta compression using up to 8 threads
Compressing objects: 100% (28/28), done.
Writing objects: 100% (28/28), 3.2 KiB | 1.6 MiB/s, done.
Total 28 (delta 14), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (14/14), done.
remote: Create a pull request for 'feature/my-branch' on GitHub by visiting:
remote: https://github.com/myorg/myrepo/pull/new/feature/my-branch
To github.com:myorg/myrepo.git
 * [new branch]      feature/my-branch -> feature/my-branch
Branch 'feature/my-branch' set up to track remote branch 'feature/my-branch' from 'origin'.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: Not a git repository (or any of the parent directories): .git` | Run `git init` or `cd` into an existing Git repository before creating branches. |
    | `fatal: 'origin' does not appear to be a 'git' repository` | Verify the remote exists with `git remote -v` and add it with `git remote add origin <url>` if missing. |
    | `error: pathspec 'feature/my-branch' did not match any file(s) known to git` | Ensure you are on the correct branch with `git branch -a` and check for typos in the branch name. |
Always branch from an up-to-date main: `git switch main && git pull` before creating the branch.

---

## Commit and Push Changes

Stage, commit, and push changes to the remote branch.

```bash
# Stage specific files
git add <file1> <file2>

# Stage interactively (review each hunk)
git add -p

# Commit with a descriptive message
git commit -m "fix: handle null pointer on startup"

# Push to the tracked remote branch
git push
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
[main 7a3f2c9] fix: handle null pointer on startup
 2 files changed, 14 insertions(+), 3 deletions(-)
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using 65 bytes/65 bytes
Writing objects: 100% (3/3), 298 bytes | 298.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), done.
To github.com:ops-team/infrastructure.git
   4f8e1b2..7a3f2c9  main -> main
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: pathspec '<file1>' did not match any files` | Verify the file paths exist and use correct relative paths from the repository root. |
    | `fatal: The current branch main has no upstream branch.` | Run `git push -u origin main` to set the upstream branch before pushing. |
    | `error: Your local changes to the following files would be overwritten by merge` | Pull the latest changes with `git pull` before pushing, or stash uncommitted changes with `git stash`. |
Write commit messages in the imperative mood and reference the issue or ticket number where applicable.

---

## Create a Merge Request / Pull Request

Open a review request from a pushed feature branch.

**GitLab:** Push branch → navigate to the repository → click **New Merge Request** → set source branch and target branch → assign a reviewer → add a description linking the issue → **Submit**.

**GitHub:** Navigate to **Pull Requests > New Pull Request** → compare branches → fill in title and description → assign reviewers → **Create Pull Request**.

Ensure CI passes before requesting review.

---

## Resolve a Merge Conflict

Conflicts occur when two branches modify the same lines. Resolve them before the merge or rebase can complete.

```bash
# Fetch latest and attempt merge
git fetch
git merge origin/main

# Git marks conflicting files — open each and look for conflict markers:
# <<<<<<< HEAD
# your changes
# =======
# incoming changes
# >>>>>>> origin/main

# Edit the file to keep the correct content, remove the markers, then:
git add <resolved-file>
git commit
```


```text title="Expected output"
remote: Enumerating objects: 24, done.
remote: Counting objects: 100% (24/24), done.
remote: Compressing objects: 100% (8/8), done.
remote: Receiving objects: 100% (16/16), 3.2 KiB | 1.6 MiB/s, done.
remote: Resolving deltas: 100% (6/6), done.
From github.com:company/infrastructure
   a7f3e21..c9d2b84  main       -> origin/main
Auto-merging config/deployment.yaml
CONFLICT (content): Merge conflict in config/deployment.yaml
Automatic merge failed; fix conflicts and then commit the result.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: Your local changes to 'config/deployment.yaml' would be overwritten by merge` | Stash uncommitted changes with `git stash` before running `git merge`. |
    | `fatal: pathspec '<resolved-file>' did not match any files` | Verify the exact filename with `git status` and ensure you're in the repository root directory. |
---

## Revert a Bad Commit

Choose the approach based on whether the bad commit has already been pushed.

```bash
# Safe revert — creates a new commit that undoes the changes (use after push)
git revert <commit-sha>
git push

# Hard reset — discards the commit locally (use only before push)
git reset --hard <commit-sha>
```


```text title="Expected output"
# Safe revert — creates a new commit that undoes the changes (use after push)
[main 7a3f2c9] Revert "Fix authentication timeout logic"
 1 file changed, 12 insertions(+), 12 deletions(-)
# Hard reset — discards the commit locally (use only before push)
HEAD is now at 5e8b1a2 Update database connection pool settings
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: commit <commit-sha> is not a valid SHA-1` | Verify the commit SHA is correct by running `git log --oneline` and copy the full or abbreviated hash. |
    | `fatal: You are currently in the middle of a revert. Cannot proceed.` | Complete or abort the ongoing revert with `git revert --abort` before attempting another operation. |
    | `error: Your local changes to the following files would be overwritten by merge` | Stash uncommitted changes with `git stash` before running `git reset --hard`. |
Never hard-reset a commit that others have already pulled from a shared branch.

---

## Manage Access Tokens and Deploy Keys

Control programmatic access to repositories via tokens and deploy keys.

**GitLab personal access token:**

1. **Settings > Access Tokens > Add new token** → set a name, expiry date, and required scopes (e.g., `read_repository`, `write_repository`).
2. Copy the token immediately — it is not shown again.
3. Store in a secrets manager; never commit to a repository.

**Deploy keys (read-only CI access):**

1. **Settings > Repository > Deploy Keys > Add Deploy Key** → paste the public key from the CI service.
2. Enable **Write access** only if the CI pipeline needs to push (e.g., auto-tagging).
3. Rotate tokens and keys on a schedule or immediately on suspected compromise.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Git — Health Checks](../health-checks/)
- [Git — CLI Reference](../cli-reference/)
- [Git — Common Issues](../../troubleshooting/common-issues/)
