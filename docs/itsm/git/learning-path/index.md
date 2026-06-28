---
tags:
  - git
  - learning-path
---
# Git — Learning Path

<div class="kb-summary">
Recommended reading order for Git version control. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Git 2.x*
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | DAG object model, refs, branching strategy | 3–4 h |
| 2 — Deployment | Hosted service config, branch protection, signing | 1–2 h |
| 3 — Operations | PR workflow, tags, submodules, hook management | ongoing |
| 4 — Security | Signed commits, secret scanning, force-push protection | 2 h |
| 5 — Troubleshooting | Reflog recovery, conflict resolution, fsck | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand Git's directed acyclic graph (DAG) object model — blobs, trees, commits, and refs — before using branching strategies on shared team projects.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — object store (blob for file content, tree for directory snapshot, commit for DAG node, tag for named commit), ref model (branches are mutable pointers, tags are immutable, HEAD points to current branch), the index (staging area between working tree and repository), and the three-way merge algorithm
- [Design Standards](../architecture/design-standards/) — branching strategy selection criteria (trunk-based development vs Gitflow vs GitHub Flow), commit message conventions (Conventional Commits format), `.gitignore` standards by language/framework, and monorepo vs multi-repo trade-offs for an infra team
- [Integrations](../architecture/integrations/) — GitHub/GitLab/Bitbucket hosting, pull request workflow as the primary collaboration mechanism, CI/CD triggered on `push` and `pull_request` events, pre-receive hooks for policy enforcement on the server side, and Git submodule patterns for shared code

**Key concepts before moving on**:

- A branch is just a named pointer to a commit — creating a branch is instant and costs nothing
- `git rebase` rewrites commit history (new SHA hashes); `git merge` preserves history with a merge commit — choose based on your team's history policy
- `git reflog` records every change to HEAD — it is the recovery tool for accidentally deleted branches and lost commits
- Never rewrite history (force push) on shared branches that others have already pulled — it requires everyone to hard-reset their local copy

**Why first**: Git's mental model (the DAG) is non-obvious. Engineers who skip this stage routinely create problems — force pushes to main, lost commits, broken histories — that are difficult to recover from.

---

## Stage 2 — Deployment

**Goal**: Configure a Git hosting service with protected branches, required reviews, and signing requirements before teams start committing to shared repositories.

**Read**:

- [Deploy](../deploy/) — repository initialisation, `git remote add origin` setup, branch protection rules (require PR reviews, status checks, no force push), CODEOWNERS file, and initial `.gitignore` and `.gitattributes` configuration
- [Install & Upgrade](../operations/install-upgrade/) — Git version management, global `~/.gitconfig` configuration (user.name, user.email, core.editor, pull.rebase), credential helper setup (keychain/libsecret), and SSH key provisioning for GitHub/GitLab

**Deployment principles**:

- Enable branch protection on `main`/`master` immediately — require at least one reviewer and passing CI before merging
- Add a `CODEOWNERS` file to assign automatic review requests to the right team when specific paths change
- Configure `.gitattributes` for line ending normalisation (`text=auto`) to prevent Windows/Linux line-ending conflicts in mixed teams

---

## Stage 3 — Operations

**Goal**: Keep repositories clean, manage contributions safely, and recover from common mistakes without rewriting shared history.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; remote reachability (`git fetch --dry-run`), branch protection rule status on GitHub/GitLab, CI pipeline health for main branch, and repository disk size for self-hosted Git servers
- [CLI Reference](../operations/cli-reference/) — `git log --oneline --graph`, `git diff`, `git stash`, `git rebase -i`, `git cherry-pick`, `git bisect`, `git reflog`, `git shortlog` — the commands needed beyond basic commit/push/pull
- [Procedures](../operations/procedures/) — pull request workflow (branch → PR → review → squash-and-merge or merge commit), tag and release creation (`git tag -s v1.0.0`), submodule update (`git submodule update --remote`), and `.gitignore` maintenance
- [Backup & Restore](../operations/backup-restore/) — bare repository backup with `git bundle create repo.bundle --all`, mirroring to a secondary remote with `git push --mirror`, and commit recovery via `git reflog` and `git cherry-pick`
- [Scripts](../operations/scripts/) — pre-commit hooks for code linting and secret scanning (`detect-secrets`), commit-msg hooks for Conventional Commits enforcement, and repository health reporting scripts using GitHub/GitLab APIs

**Daily rhythm**: Main branch CI status → open PRs awaiting review → stale feature branches → repository disk usage (self-hosted).

---

## Stage 4 — Security

**Goal**: Prevent sensitive data from entering history, enforce signed commits, and restrict force pushes on all protected branches.

**Read**:

- [Access Control](../security/access-control/) — branch protection rules (required status checks, required reviewers, dismiss stale reviews), CODEOWNERS for automatic reviewer assignment, and repository-level access controls (read/triage/write/maintain/admin roles)
- [Authentication](../security/authentication/) — SSH key vs HTTPS token authentication best practices, deploy keys for read-only CI access, fine-grained personal access tokens (scoped to specific repos and permissions), and GitHub Apps tokens for organisation-level automation
- [Encryption](../security/encryption/) — GPG or SSH commit signing (`git config --global commit.gpgsign true`), signed tag creation (`git tag -s`), signature verification in GitHub/GitLab, TLS for all HTTPS remote operations, and `git-crypt` for encrypting specific files checked into the repository
- [Hardening](../security/hardening/) — scanning history for secrets with `trufflehog` or `gitleaks`, `git-secrets` pre-commit hook to prevent future secret commits, disabling force push to `main` and release branches, and enabling signed pushes via pre-receive hooks on self-hosted servers

---

## Stage 5 — Troubleshooting

**Goal**: Recover from merge conflicts, detached HEAD states, and accidental commits of sensitive data without losing work.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — merge conflict resolution strategy (ours vs theirs vs manual), detached HEAD recovery (`git checkout -b recovery-branch`), accidental commit to wrong branch (`git cherry-pick` + `git reset`), undoing a pushed commit (`git revert`), and submodule pointer mismatch (`git submodule update --init`)
- [Diagnostics](../troubleshooting/diagnostics/) — `git reflog` for finding lost commits and branch tips, `git fsck --lost-found` for dangling objects, `git log --graph --all --oneline` for full history visualisation, and `git bisect run <test-script>` for automated regression hunting
- [Escalation](../troubleshooting/escalation/) — GitHub/GitLab Support for hosting-side issues (repository corruption, access failures), `git gc --aggressive` and `git repack` for local repository performance, and data recovery specialists for catastrophic history loss on self-hosted servers

**Why last**: Troubleshooting makes most sense once you can visualise the DAG and understand how reflog, stash, and the index interact with the working tree.

---

## See also

- [Git — Deploy](../deploy/)
- [Git — Procedures](../operations/procedures/)
- [Git — Common Issues](../troubleshooting/common-issues/)
