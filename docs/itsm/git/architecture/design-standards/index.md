---
tags:
  - architecture
  - git
---
# Git — Design Standards

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

---

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## See also

- [Git — Deploy](../../deploy/)
