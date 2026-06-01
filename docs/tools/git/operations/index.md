# Git — Operations



<div class="kb-summary">
Git — Operations reference.
</div>

```text
┌────────────────────────────────────────── Git — Operations ───────────────────────────────────────────┐
│                                                                                                       │
│  Day-to-day Git operations: procedures, backup, health, installs, scripts, CLI reference.             │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Procedures         │  │      Repository Hygiene     │  │        CLI Essentials       │   │
│   │    Branch lifecycle mgmt    │  │   git gc: compress + prune  │  │     add / commit / push     │   │
│   │   Tag and release process   │  │   git remote prune origin   │  │     fetch / pull / merge    │   │
│   │     Access provisioning     │  │     Large file: Git LFS     │  │     log / diff / status     │   │
│   │     Mirror / backup sync    │  │     Archive: git bundle     │  │    rebase / reset / stash   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab server · developer workstations · CI runners · backup storage                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  git gc       = garbage collection; repacks objects, prunes unreachable                               │
│  git prune    = removes unreachable objects from object store                                         │
│  Git LFS      = Large File Storage; replaces binaries with pointer files                              │
│  git bundle   = packs repo into single file for offline transfer                                      │
│  Mirror clone = --mirror clones all refs including remotes; for backup                                │
│  remote prune = removes local tracking refs deleted from remote                                       │
│  Release tag  = annotated tag on main at release point; triggers pipeline                             │
│  Access prov. = adding collaborator or team permission on GitHub/GitLab                               │
│  git log      = commit history; --oneline --graph shows branch topology                               │
│  git diff     = shows changes between working tree, index, or commits                                 │
│  git reset    = moves HEAD; --soft keeps index, --hard discards all                                   │
│  git stash    = saves dirty state to stack; pop restores last stash                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Complete Git command reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Repository health monitoring and validation.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Branching, recovery, and workflow procedures.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation and upgrade procedures.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup strategies and restore procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and utilities.</span>
</a>

</div>
