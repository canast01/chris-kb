# Git — Standards

## Commit Standards

Commit message conventions, amending commits, squashing, and cherry-picking.

## Commit Message Conventions

Good commit messages make the log scannable and power automated changelogs.

```bash
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

---

## Tagging Standards

Annotated vs lightweight tags, GPG signing, pushing tags, and release tag workflows.

## Annotated vs Lightweight Tags

| Type | Stores Author/Date | Message | GPG Signable | Use For |
|------|--------------------|---------|-------------|---------|
| Annotated | Yes | Yes | Yes | Releases, milestones |
| Lightweight | No | No | No | Local markers, temp refs |

```bash
# Create a lightweight tag
git tag v2.3.0

# Create an annotated tag (preferred for releases)
git tag -a v2.3.0 -m "Release v2.3.0: add S3 lifecycle management"

# Create an annotated tag on a past commit
git tag -a v2.2.1 a1b2c3d4 -m "Backport fix for auth timeout"

# List all tags
git tag

# List tags matching a pattern
git tag -l "v2.*"

# Show tag details (annotated)
git show v2.3.0
```

## Signing Tags with GPG

```bash
# Sign a tag with your default GPG key
git tag -s v2.3.0 -m "Signed release v2.3.0"

# Sign with a specific key
git tag -u KEYID -a v2.3.0 -m "Release v2.3.0"

# Verify a signed tag
git tag -v v2.3.0

# Configure default signing key
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global tag.gpgsign true
```

## Pushing Tags

Tags are not pushed automatically — you must push them explicitly.

```bash
# Push a single tag
git push origin v2.3.0

# Push all local tags
git push origin --tags

# Push all annotated tags only
git push origin --follow-tags

# Delete a remote tag
git push origin --delete v2.3.0
git push origin :refs/tags/v2.3.0   # equivalent

# Delete a local tag
git tag -d v2.3.0
```

## Release Tag Workflow

A standard release workflow using annotated, signed tags:

```bash
# 1. Ensure you're on main and up to date
git switch main
git pull --rebase origin main

# 2. Run tests / build
make test

# 3. Create the annotated tag
git tag -a v2.4.0 -m "Release v2.4.0

Changes:
- feat: S3 lifecycle management
- fix: auth token expiry handling
- chore: upgrade boto3 to 1.34.0"

# 4. Push commits and tag together
git push origin main
git push origin v2.4.0

# 5. Create GitHub/GitLab release from tag (gh CLI)
gh release create v2.4.0 \
  --title "v2.4.0" \
  --notes "See CHANGELOG.md for details"
```

## Semantic Versioning with Tags

```bash
# Find the latest release tag
git describe --tags --abbrev=0

# Get full version string including commits since last tag
git describe --tags

# Check if current commit is exactly on a tag
git describe --exact-match --tags HEAD 2>/dev/null || echo "not a tagged commit"

# List tags sorted by semver
git tag -l "v*" | sort -V
```

| Tag Pattern | Example | Meaning |
|-------------|---------|---------|
| `vMAJOR.MINOR.PATCH` | `v2.4.0` | Full release |
| `vMAJOR.MINOR.PATCH-rc.N` | `v2.4.0-rc.1` | Release candidate |
| `vMAJOR.MINOR.PATCH-beta.N` | `v2.4.0-beta.1` | Beta build |
| `vMAJOR.MINOR.PATCH-hotfix` | `v2.3.1` | Emergency patch |
