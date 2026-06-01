# Git — Architecture

<div class="kb-summary">
Git is a distributed version control system where every clone is a complete repository. Enterprise deployments use GitHub Enterprise Server or GitLab Self-Managed as the integration point, with Gitaly handling all repository I/O.
</div>

```
┌───────────────────────────────────────── Git — Architecture ──────────────────────────────────────────┐
│                                                                                                       │
│  Git object model and distributed repository architecture: object store, refs, and remotes.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Object Store (.git/objects)          │  │            References (.git/refs)           │   │
│   │         Blob: file content snapshot          │  │          Branch: refs/heads/<name>          │   │
│   │           Tree: directory listing            │  │            Tag: refs/tags/<name>            │   │
│   │         Commit: tree + parent + msg          │  │        Remote: refs/remotes/<remote>        │   │
│   │        Pack files: compressed objects        │  │         HEAD: current branch pointer        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Local objects pushed to remote; remote refs track upstream state                                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Working Tree                 │  │              Remote Repository              │   │
│   │           Untracked: not in index            │  │        Bare repo: objects only, no WC       │   │
│   │          Modified: tracked, changed          │  │      Push: send local objects upstream      │   │
│   │       Staged: in index, not committed        │  │        Fetch: download without merge        │   │
│   │         Config: .git/config per repo         │  │         Hooks: pre/post push/receive        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab servers · developer workstations · CI/CD runners · bare clone mirrors                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Blob         = raw file content stored as compressed object; keyed by SHA-1                          │
│  Tree         = directory snapshot; maps filenames to blob/tree SHAs                                  │
│  Commit       = points to one tree + zero or more parent commits                                      │
│  Pack file    = compressed bundle of many objects; created during gc/clone                            │
│  Bare repo    = repository without working copy; used as remote (servers)                             │
│  Index        = binary file (.git/index) staging area for next commit                                 │
│  Reflog       = local log of all ref changes; useful for recovery                                     │
│  Hook         = shell script triggered at git events; server hooks enforce policy                     │
│  WC           = working copy / working tree; checked-out files on disk                                │
│  Object store = content-addressed storage in .git/objects; shared via pack                            │
│  Upstream     = remote branch tracked by local branch; git pull target                                │
│  Refspec      = mapping of local to remote refs used by fetch/push                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────── Git — Architecture ──────────────────────────────────────────┐
│                                                                                                       │
│  Git object model and distributed repository architecture: object store, refs, and remotes.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Object Store (.git/objects)          │  │            References (.git/refs)           │   │
│   │         Blob: file content snapshot          │  │          Branch: refs/heads/<name>          │   │
│   │           Tree: directory listing            │  │            Tag: refs/tags/<name>            │   │
│   │         Commit: tree + parent + msg          │  │        Remote: refs/remotes/<remote>        │   │
│   │        Pack files: compressed objects        │  │         HEAD: current branch pointer        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Local objects pushed to remote; remote refs track upstream state                                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Working Tree                 │  │              Remote Repository              │   │
│   │           Untracked: not in index            │  │        Bare repo: objects only, no WC       │   │
│   │          Modified: tracked, changed          │  │      Push: send local objects upstream      │   │
│   │       Staged: in index, not committed        │  │        Fetch: download without merge        │   │
│   │         Config: .git/config per repo         │  │         Hooks: pre/post push/receive        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab servers · developer workstations · CI/CD runners · bare clone mirrors                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Blob         = raw file content stored as compressed object; keyed by SHA-1                          │
│  Tree         = directory snapshot; maps filenames to blob/tree SHAs                                  │
│  Commit       = points to one tree + zero or more parent commits                                      │
│  Pack file    = compressed bundle of many objects; created during gc/clone                            │
│  Bare repo    = repository without working copy; used as remote (servers)                             │
│  Index        = binary file (.git/index) staging area for next commit                                 │
│  Reflog       = local log of all ref changes; useful for recovery                                     │
│  Hook         = shell script triggered at git events; server hooks enforce policy                     │
│  WC           = working copy / working tree; checked-out files on disk                                │
│  Object store = content-addressed storage in .git/objects; shared via pack                            │
│  Upstream     = remote branch tracked by local branch; git pull target                                │
│  Refspec      = mapping of local to remote refs used by fetch/push                                    │
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


