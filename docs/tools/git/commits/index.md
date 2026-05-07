# Git Commits

Commit message conventions, amending commits, squashing, and cherry-picking.

## Commit Message Conventions

Good commit messages make the log scannable and power automated changelogs.

```
# Conventional Commits format
<type>(<scope>): <short summary>

[optional body — wrap at 72 chars]

[optional footer: BREAKING CHANGE, issue refs]

# Examples
feat(auth): add OAuth2 PKCE flow
fix(api): handle null response from billing service
chore(deps): upgrade boto3 to 1.34.0
docs(runbook): add k8s drain procedure
refactor(cache): replace in-memory store with Redis
```

| Type | When to Use |
|------|------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `chore` | Maintenance, tooling, deps |
| `docs` | Documentation only |
| `refactor` | Code change with no behaviour change |
| `test` | Adding or fixing tests |
| `ci` | CI/CD pipeline changes |
| `perf` | Performance improvement |

## Making and Amending Commits

```bash
# Stage specific files and commit
git add src/auth.py tests/test_auth.py
git commit -m "feat(auth): add OAuth2 PKCE flow"

# Stage all tracked changes
git add -u
git commit -m "fix(api): handle null billing response"

# Amend the most recent commit message (before push)
git commit --amend -m "fix(api): handle null response from billing service"

# Amend and add a forgotten file
git add forgotten_file.py
git commit --amend --no-edit

# Add a GPG signature to a commit
git commit -S -m "feat: signed release commit"
```

Only amend commits that have not been pushed to a shared branch.

## Squashing Commits

Squash a chain of WIP commits into a single clean commit before merging.

```bash
# Interactive rebase — squash last 4 commits
git rebase -i HEAD~4
# In the editor: change 'pick' to 's' (squash) for all but the first

# Squash everything on a branch into one commit against main
git switch feature/my-feature
git rebase -i $(git merge-base HEAD main)

# Alternative: merge --squash (no rebase needed)
git switch main
git merge --squash feature/my-feature
git commit -m "feat(platform): add S3 lifecycle management"
```

## Cherry-Picking

Apply a specific commit from another branch without merging the whole branch.

```bash
# Cherry-pick a single commit by hash
git cherry-pick a1b2c3d4

# Cherry-pick a range of commits
git cherry-pick a1b2c3d4^..e5f6g7h8

# Cherry-pick without auto-committing (inspect first)
git cherry-pick -n a1b2c3d4

# Cherry-pick a merge commit (specify parent)
git cherry-pick -m 1 a1b2c3d4

# Abort a cherry-pick in progress
git cherry-pick --abort
```

| Scenario | Command |
|----------|---------|
| Backport a fix to release branch | `git cherry-pick <commit>` |
| Apply multiple commits from hotfix | `git cherry-pick <sha1>^..<sha2>` |
| Try a commit without staging it | `git cherry-pick -n <commit>` |
| Resolve conflict and continue | `git cherry-pick --continue` |

## Viewing Commit History

```bash
# Oneline log
git log --oneline -20

# Graph view across branches
git log --oneline --graph --decorate --all

# Log with diff stats
git log --stat -5

# Search commits by message
git log --grep="PLAT-42" --oneline

# Show commits by author
git log --author="Chris" --oneline --since="2 weeks ago"

# Show the full diff of a specific commit
git show a1b2c3d4
```
