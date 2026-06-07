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
```text
┌───────────────────────────────────── Git — Operations Procedures ─────────────────────────────────────┐
│                                                                                                       │
│  Standard procedures: branch lifecycle, tagging releases, access management, and repo setup.          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Branch Lifecycle               │  │               Release Tagging               │   │
│   │      Create from main: git checkout -b       │  │           Tag on main after merge           │   │
│   │      Push: git push -u origin <branch>       │  │       Annotated: git tag -a v1.2.3 -m       │   │
│   │      Open PR: link issue, add reviewers      │  │       Push tag: git push origin <tag>       │   │
│   │        Delete after merge: branch -d         │  │        Create GitHub Release from tag       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Feature branches are short-lived; delete after merge to keep repo clean                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Access Management               │  │             New Repository Setup            │   │
│   │        Add collaborator via GitHub UI        │  │             git init / git clone            │   │
│   │           Use teams for org repos            │  │           Add .gitignore + README           │   │
│   │        Roles: Read/Triage/Write/Admin        │  │        Set branch protection on main        │   │
│   │        Audit log: org → Security tab         │  │         Add CODEOWNERS + CI workflow        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab server · branch protection rules · CI pipeline · team permissions                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  git checkout -b = create and switch to new branch in one command                                     │
│  git push -u     = push and set upstream tracking reference                                           │
│  Annotated tag   = tag object with tagger, date, message; preferred for releases                      │
│  GitHub Release  = web UI release tied to tag; includes changelog and assets                          │
│  Collaborator    = individual user added to repo with explicit permission level                       │
│  Team            = GitHub/GitLab group; manage access at team level, not per-user                     │
│  Triage role     = can manage issues/PRs but not write code                                           │
│  Audit log       = org-level event log; tracks access changes and admin actions                       │
│  CODEOWNERS      = auto-assign reviewers to PRs touching specific paths                               │
│  Branch prot.    = rules enforcing CI, reviews, linear history on protected branches                  │
│  .gitignore      = lists patterns for files Git should not track                                      │
│  Short-lived     = feature branches should be merged within days, not weeks                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
```bash
# Find branches with no commits ahead of main
git branch --merged main

# Find branches with no recent activity (older than 90 days)
git for-each-ref --sort=committerdate refs/heads/ \
  --format='%(committerdate:short) %(refname:short)' \
  | awk '$1 < "'$(date -v-90d +%Y-%m-%d)'"'
```
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
```bash
# Step 1: find the tip commit of the deleted branch in reflog
git reflog | grep "branch-name"

# Step 2: recreate the branch at that commit
git switch -c recovered-branch a1b2c3d4

# Alternative: search all unreachable commits
git fsck --lost-found
ls .git/lost-found/commit/
```
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

---

## Clone a Repository

Download a copy of an existing repository to a local working directory.

```bash
# HTTPS clone (uses username + token)
git clone https://<host>/<owner>/<repo>.git

# SSH clone (uses SSH key)
git clone git@<host>:<owner>/<repo>.git
```

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
