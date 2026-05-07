# Git Recovery

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
