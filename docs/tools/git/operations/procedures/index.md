# Git — Procedures

## Branching

Branch naming conventions, creating and deleting branches, tracking remotes, and merge vs rebase.

## Branch Naming Conventions

Consistent naming makes automation and review easier.

```
# Common prefixes
feature/  — New functionality (feature/add-login-page)
fix/      — Bug fixes (fix/null-pointer-on-startup)
chore/    — Maintenance, deps, config (chore/upgrade-node-18)
docs/     — Documentation changes (docs/update-api-reference)
hotfix/   — Urgent production fixes (hotfix/payment-timeout)
release/  — Release preparation (release/v2.4.0)
```

| Pattern | Example | Use Case |
|---------|---------|----------|
| `feature/<ticket>-<slug>` | `feature/PLAT-42-s3-lifecycle` | Ticket-linked work |
| `fix/<ticket>-<slug>` | `fix/PLAT-99-oom-restart` | Bug fixes |
| `hotfix/<version>` | `hotfix/v2.3.1` | Emergency patch |
| `release/<semver>` | `release/v3.0.0` | Release branch |
| `<user>/<description>` | `chris/explore-caching` | Personal experiments |

## Creating and Switching Branches

```bash
# Create and switch in one step
git switch -c feature/PLAT-42-s3-lifecycle

# Create from a specific base (not current HEAD)
git switch -c fix/auth-bug origin/main

# List all local branches
git branch

# List all branches including remotes
git branch -a

# List branches with last commit info
git branch -v
```

## Deleting Branches

```bash
# Delete a merged local branch (safe — fails if unmerged)
git branch -d feature/PLAT-42-s3-lifecycle

# Force-delete an unmerged branch
git branch -D feature/abandoned-experiment

# Delete a remote branch
git push origin --delete feature/PLAT-42-s3-lifecycle

# Prune stale remote-tracking references
git fetch --prune
git remote prune origin

# One-liner: delete all local branches already merged into main
git branch --merged main | grep -v '^* \|main\|master' | xargs git branch -d
```

## Tracking Remote Branches

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

## Merge vs Rebase

| Strategy | Creates Merge Commit | Preserves History | Best For |
|----------|---------------------|------------------|----------|
| `git merge` | Yes | Linear + merge commits | Long-lived branches, teams |
| `git merge --squash` | No (one commit) | Squashed | Small features into main |
| `git rebase` | No | Rewrites commits | Local cleanup before PR |
| `git rebase -i` | No | Interactive rewrite | Squash, reorder, edit messages |

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

## Stale Branch Cleanup

```bash
# Find branches with no commits ahead of main
git branch --merged main

# Find branches with no recent activity (older than 90 days)
git for-each-ref --sort=committerdate refs/heads/ \
  --format='%(committerdate:short) %(refname:short)' \
  | awk '$1 < "'$(date -v-90d +%Y-%m-%d)'"'
```

---

## Recovery

Using git reflog, reset, revert, and recovering deleted branches or lost commits.

## git reflog — Your Safety Net

The reflog records every movement of HEAD and branch pointers, including those that are not in the regular log.

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

The reflog retains entries for 90 days (default). Expired entries cannot be recovered.

## git reset

`reset` moves the branch pointer and optionally modifies the index and working tree.

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

| Mode | Branch Pointer | Index | Working Tree |
|------|---------------|-------|-------------|
| `--soft` | Moved | Unchanged | Unchanged |
| `--mixed` | Moved | Reset | Unchanged |
| `--hard` | Moved | Reset | Reset (destructive) |

Never use `--hard` on shared branches without team coordination.

## git revert — Safe Undo for Shared Branches

`revert` creates a new commit that undoes a previous one. Safe to use on main/production branches.

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

## Recovering Deleted Branches

```bash
# Step 1: find the tip commit of the deleted branch in reflog
git reflog | grep "branch-name"

# Step 2: recreate the branch at that commit
git switch -c recovered-branch a1b2c3d4

# Alternative: search all unreachable commits
git fsck --lost-found
ls .git/lost-found/commit/
```

## Recovering Lost Commits

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

## Recovering Stashed Changes

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

| Problem | Recovery Command |
|---------|----------------|
| Deleted branch | `git switch -c name <hash from reflog>` |
| Bad `reset --hard` | `git reset --hard HEAD@{N}` from reflog |
| Committed to wrong branch | `git cherry-pick` onto correct branch |
| Lost stash | `git fsck --no-reflogs` + inspect dangling |
| Accidentally amended | `git reset --soft ORIG_HEAD` |
