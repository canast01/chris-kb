# Git — Standards


<div class="kb-summary">
Standards reference covering Commit Standards, Commit Message Conventions, Squashing Commits, Cherry-Picking, Viewing Commit History and 6 more sections.
</div>

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
┌─────────────────────────────────────── Git — Design Standards ────────────────────────────────────────┐
│                                                                                                       │
│  Branching strategy, commit conventions, and repository standards for team-managed Git repos.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Branching Strategy              │  │              Commit Conventions             │   │
│   │           main: always deployable            │  │      Type: feat/fix/chore/docs/refactor     │   │
│   │       feature/<ticket>-<desc> pattern        │  │          Scope: component in parens         │   │
│   │        release/<semver> for cutpoints        │  │       Subject: imperative, < 72 chars       │   │
│   │        hotfix/<ticket>-<desc> pattern        │  │        Body: why, not what (optional)       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Naming standards enable automation; message conventions power changelog generation                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Repository Standards             │  │               Review Standards              │   │
│   │        .gitignore: language-specific         │  │        Require ≥ 2 approvals on main        │   │
│   │         README: purpose + quickstart         │  │      Dismiss stale reviews on new push      │   │
│   │        CODEOWNERS: auto-assign review        │  │        Require status checks to pass        │   │
│   │      Branch protection on main/release       │  │       Squash or rebase merge preferred      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab · branch protection rules · CODEOWNERS file · CI status checks                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Conventional Commits= specification for structured commit messages (type(scope): subject)            │
│  CODEOWNERS   = file mapping path patterns to required reviewers                                      │
│  Semver       = semantic versioning: MAJOR.MINOR.PATCH                                                │
│  Squash merge = combines all PR commits to one; cleaner main history                                  │
│  Status check = CI job result required before merge; blocks broken code                               │
│  Stale review = approval dismissed when new commits pushed; forces re-review                          │
│  Hotfix       = emergency fix branch off main/release; merged back to both                            │
│  Cutpoint     = release branch created at a specific commit to stabilise                              │
│  Imperative   = commit subject in present tense: "Add feature" not "Added"                            │
│  Branch prot. = GitHub/GitLab rule preventing direct push to protected branch                         │
│  .gitignore   = lists file patterns excluded from tracking (secrets, build artifacts)                 │
│  Changelog    = auto-generated from conventional commits by tools like release-it                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
