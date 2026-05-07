# Git Tags

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

## Checking Out Tags

```bash
# Check out a tag (detached HEAD)
git checkout v2.3.0

# Create a branch from a tag for patching
git switch -c hotfix/v2.3.1 v2.3.0

# List commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline
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
