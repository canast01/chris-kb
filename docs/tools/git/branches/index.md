# Git Branches

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
