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


```text title="Expected output"
(no output — this is a documentation block showing commit message format conventions, not executable commands)
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

```text title="Expected output"
[main a1b2c3d] Fix authentication timeout in session handler
 Date: Thu Mar 14 10:22:45 2024 +0000
 1 file changed, 3 insertions(+), 1 deletion(-)
[main e5f6g7h] Refactor database connection pooling
 Date: Thu Mar 14 10:18:12 2024 +0000
 1 file changed, 12 insertions(+), 8 deletions(-)
[main f7g8h9i] Update logging configuration
 Date: Thu Mar 14 10:15:33 2024 +0000
 1 file changed, 5 insertions(+), 2 deletions(-)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`error: commit a1b2c3d4 is a merge but no -m option was given.`** — Use `git cherry-pick -m 1 <commit>` to specify which parent of the merge commit to use.
    **`error: could not apply a1b2c3d4... Fix authentication timeout`** — Resolve merge conflicts manually with `git status`, edit conflicted files, then run `git cherry-pick --continue`.
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

```text title="Expected output"
a1b2c3d4 Merge pull request #847 from feature/api-gateway-v2
b5c6d7e8 feat: implement circuit breaker pattern for service mesh
c9d0e1f2 docs: update architecture decision records
d3e4f5g6 refactor: consolidate config management layer
e7f8g9h0 fix: resolve race condition in cache invalidation
f1g2h3i4 chore: bump kubernetes client to 1.28.2
g5h6i7j8 test: add integration tests for load balancer
h9i0j1k2 ci: update github actions workflow
i3j4k5l6 perf: optimize database query indexes
j7k8l9m0 style: format code per linting standards
k1l2m3n4 docs: add troubleshooting guide for TLS issues
l5m6n7o8 feat: add prometheus metrics exporter
m9n0o1p2 fix: handle graceful shutdown in worker pools
n3o4p5q6 refactor: split monolithic service into microservices
o7p8q9r0 Initial commit

* commit a1b2c3d4 (HEAD -> main, origin/main)
|\  Merge: b5c6d7e8 x9y0z1a2
| * commit x9y0z1a2 (origin/feature/api-gateway-v2)
| | feat: implement circuit breaker pattern for service mesh
| |
* | commit b5c6d7e8 (origin/develop)
|/  docs: update architecture decision records
|
* commit c9d0e1f2
| feat: add prometheus metrics exporter
|
* commit d3e4f5g6
  refactor: consolidate config management layer

commit a1b2c3d4
Author: Chris Martinez <chris.martinez@company.com>
Date:   Wed Nov 15 14:32:18 2024 -0800

    Merge pull request #847 from feature/api-gateway-v2
    
    Circuit breaker implementation for resilient service communication

 src/gateway/circuit_breaker.go | 142 ++++++++++++++++++++++++++++++++++
 src/gateway/middleware.go       |  28 ++++---
 tests/gateway/circuit_test.go   |  95 +++++++++++++++++++++++
 3 files changed, 265 insertions(+), 28 deletions(-)

diff --git a/src/gateway/circuit_breaker.go b/src/gateway/circuit_breaker.go
new file mode 100644
index 0000000..a1b2c3d
--- /dev/null
+++ b/src/gateway/circuit_breaker.go
@@ -0,0 +1,142 @@
+package gateway
+
+import (
+	"sync"
+	"time"
+)
+
+type CircuitBreaker struct {
+	state       string
+	failCount   int
+	lastFailTime time.Time
+	mu          sync.RWMutex
+}
```

!!! warning "Common errors"
    **`fatal: your current branch 'main' does not have any commits yet`** — Initialize the repository with at
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

```text title="Expected output"
v2.2.1
v2.3.0
v2.3.0
tag v2.3.0
Tagger: Sarah Chen <sarah.chen@company.com>
Date:   Thu Mar 14 09:47:23 2024 -0700

Release v2.3.0: add S3 lifecycle management

commit 8f9e7d6c5b4a3f2e1d0c9b8a7f6e5d4c
Author: Sarah Chen <sarah.chen@company.com>
Date:   Thu Mar 14 09:45:12 2024 -0700

    Add S3 lifecycle management policies
```

!!! warning "Common errors"
    **`fatal: tag 'v2.3.0' already exists`** — Delete the existing tag with `git tag -d v2.3.0` before recreating it, or use a different version number.
    **`error: object 'a1b2c3d4' not found`** — Verify the commit hash exists in your repository with `git log --oneline` and use the full or correct short SHA.
    **`fatal: Failed to resolve 'HEAD' as a valid ref.`** — Initialize the repository with `git init` and create an initial commit before tagging.
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

```text title="Expected output"
[master 7a4c8f2] Signed release v2.3.0
object 7a4c8f2d9e1f3b5a8c2d4e6f7a9b1c3d
type commit
tagger: John Doe <john.doe@company.com> 1703084521 +0000

Signed release v2.3.0
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE4K8vF3mN2pQrS9tL8xY2Z3aB5cEFAmVqK2sACgkQ8xY2Z3aB
5cE7Uw/+KL9m3vF2nQ8pR4sT6uV7wX9yZ1aB2cD4eF5gH6iJ7kL8mN9oP0qR1sT2u
...
-----END PGP SIGNATURE-----

object 7a4c8f2d9e1f3b5a8c2d4e6f7a9b1c3d
type commit
tagger: Jane Smith <jane.smith@company.com> 1703084634 +0000

tag v2.3.0
Tagger: Jane Smith <jane.smith@company.com>
Date:   Wed Dec 20 14:23:54 2023 +0000

Release v2.3.0

gpg: Signature made Wed Dec 20 14:23:54 2023 UTC
gpg: Good signature from "Jane Smith <jane.smith@company.com>" [ultimate]
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`error: gpg failed to sign the data`** — Ensure GPG is installed (`apt install gnupg` or `brew install gnupg`) and your GPG agent is running (`gpg-agent --daemon`).
    **`error: key KEYID not found`** — Verify the key ID exists with `gpg --list-secret-keys --keyid-format=long` and use the correct 16-character ID.
    **`fatal: tag 'v2.3.0' already exists`** — Delete the existing tag with `git tag -d v2.3.0` before creating a new one, or use a different version number.
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

```text title="Expected output"
Counting objects: 12, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (8/8), done.
Writing objects: 100% (12/12), 2.3 KiB | 1.1 MiB/s, done.
Total 12 (delta 4), reused 0 (delta 0)
To github.com:acme-corp/itsm-repo.git
 * [new tag]         v2.3.0 -> v2.3.0
Enumerating objects: 156, done.
Counting objects: 100% (156/156), done.
Delta compression using up to 8 threads.
Compressing objects: 100% (98/98), done.
Writing objects: 100% (145/145), 18.4 KiB | 2.7 MiB/s, done.
Total 145 (delta 67), reused 0 (delta 0)
To github.com:acme-corp/itsm-repo.git
 * [new tag]         v2.1.5 -> v2.1.5
 * [new tag]         v2.2.0 -> v2.2.0
 * [new tag]         v2.3.0 -> v2.3.0
To github.com:acme-corp/itsm-repo.git
 - [deleted]         v2.3.0
Deleted tag 'v2.3.0' (was abc1234)
```

!!! warning "Common errors"
    **`fatal: tag 'v2.3.0' not found.`** — Verify the tag exists locally with `git tag -l` before attempting deletion.
    **`remote: error: deny updating a hidden ref`** — Ensure you have push permissions on the repository and the tag is not protected by branch protection rules.
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

```text title="Expected output"
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
Current branch main is up to date with origin/main.
Running tests...
✓ unit tests passed (42 tests)
✓ integration tests passed (18 tests)
✓ linting passed
Build successful
Created tag v2.4.0 (object a7f3c2e9)
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 1.2 KiB, done.
Total 12 (delta 4), reused 0 (delta 0), pack-reused 0
To github.com:platform/infra-core.git
   f4e2b1d..a7f3c2e  main -> main
To github.com:platform/infra-core.git
 * [new tag]         v2.4.0 -> v2.4.0
✓ Release created: https://github.com/platform/infra-core/releases/tag/v2.4.0
```

!!! warning "Common errors"
    **`error: pathspec 'main' did not match any file known to git`** — Verify the default branch name with `git branch -a` and use the correct name (e.g., `master` or `main`).
    **`fatal: Not a git repository (or any of the parent directories): .git`** — Run the command from the root of the git repository or clone the repository first.
    **`fatal: Authentication failed for 'https://github.com/...'`** — Configure SSH keys with `ssh-keygen` and update the remote URL to SSH format with `git remote set-url origin git@github.com:owner/repo.git`.
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


```text title="Expected output"
v2.4.1
v2.4.1-18-gf7a3c9d
not a tagged commit
v1.8.0
v1.9.2
v2.0.0
v2.1.3
v2.4.1
```

!!! warning "Common errors"
    **`fatal: No names found, cannot describe anything.`** — Initialize tags in the repository with `git tag v1.0.0` or fetch tags from remote with `git fetch --tags`.
    **`fatal: No annotated tags can describe '<commit>'.`** — Create annotated tags instead of lightweight tags using `git tag -a v2.5.0 -m "Release 2.5.0"` rather than `git tag v2.5.0`.
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
