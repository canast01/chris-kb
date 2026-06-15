---
tags:
  - architecture
  - git
---
# Git — Architecture

<div class="kb-summary">
Git is a distributed version control system where every clone is a complete repository. Enterprise deployments use GitHub Enterprise Server or GitLab Self-Managed as the integration point, with Gitaly handling all repository I/O.

*Applies to: Git 2.x*
</div>

```text
┌────────────────────────────────────── Git Architecture Overview ──────────────────────────────────────┐
│                                                                                                       │
│  Git is a distributed version control system. Every clone is a full copy of the                       │
│  repository history. Content is stored as an immutable object DAG (directed acyclic                   │
│  graph); branches and tags are lightweight pointers (refs) to commits.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Object Store (.git/objects)          │  │                 Working Tree                │   │
│   │         Blob: file content snapshot          │  │          Checked-out files on disk          │   │
│   │           Tree: directory listing            │  │       Staging area (index) for commit       │   │
│   │        Commit: tree+parent+author+msg        │  │          .git/index: staged changes         │   │
│   │       Tag: annotated pointer to commit       │  │           HEAD: current branch tip          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Refs and Remotes               │  │              Hosting Platforms              │   │
│   │        Branch: movable ref to commit         │  │        GitHub: PRs, Actions, Packages       │   │
│   │          Remote: named URL (origin)          │  │         GitLab: CI/CD, MR, registry         │   │
│   │         fetch/pull: sync remote refs         │  │         Bitbucket: Jira integration         │   │
│   │         push: send commits to remote         │  │          Gitea/Forgejo: self-hosted         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical infrastructure: Git repos stored as bare repositories on disk; object                       │
│  packs compress loose objects (git gc); remotes accessed via HTTPS or SSH; hosted                     │
│  platforms add auth, access control, CI/CD pipelines, and code review workflows.                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DAG            = directed acyclic graph; commit history; no cycles                                   │
│  Blob           = immutable snapshot of a single file; addressed by SHA-256                           │
│  Tree           = directory snapshot; maps names to blobs and sub-trees                               │
│  Commit         = tree + parent commit(s) + author metadata + message                                 │
│  Branch         = lightweight movable ref; file in .git/refs/heads/                                   │
│  HEAD           = ref to current branch (or detached commit in detached HEAD)                         │
│  Remote         = named URL of another repository; push/pull target                                   │
│  origin         = conventional default remote name after git clone                                    │
│  Staging area   = index; accumulates changes before they become a commit                              │
│  Pack file      = compressed bundle of many objects; created by git gc                                │
│  Rebase         = re-apply commits on top of a different base; rewrites history                       │
│  Merge commit   = commit with two parents; preserves branch topology                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Git Architecture](../../../assets/git-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Object model, ref system, GHES/GitLab topology, and git push data flow.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Branching standards, repository conventions, and best practices.</span></a>
</div>

---

## Object Model Summary

| Object | Description |
|--------|-------------|
| **blob** | Raw file content |
| **tree** | Directory listing mapping names to blob/tree SHAs |
| **commit** | Points to a tree; records author, message, parent commits |
| **tag** | Annotated reference to another object |

---

## Distributed Architecture

