---
tags:
  - git
  - troubleshooting
---
# Git — Troubleshooting



<div class="kb-summary">
Diagnosing merge conflicts, broken remote connections, rebase failures, and common Git workflow errors.
</div>

```text
┌──────────────────────────────────────── Git — Troubleshooting ────────────────────────────────────────┐
│                                                                                                       │
│  Git troubleshooting: merge conflicts, recovering lost commits, and common error patterns.            │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Merge Conflicts       │  │         Lost Commits        │  │         Push Errors         │   │
│   │  git status: list conflicts │  │     git reflog: find SHA    │  │ non-fast-forward: pull first│   │
│   │ Edit markers: <<<, ===, >>> │  │    git cherry-pick <sha>    │  │ rejected: check branch prot.│   │
│   │ git add + commit to resolve │  │    git reset --hard <sha>   │  │ permission denied: check key│   │
│   │   git mergetool: 3-pane UI  │  │   git fsck: find dangling   │  │timeout: check proxy/firewall│   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Developer workstation · Git remote · network / firewall · SSH agent                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Conflict markers= <<<<<<< HEAD / ======= / >>>>>>> branch; delimit conflicting hunks                 │
│  git reflog      = per-ref log of all pointer movements; survives reset --hard                        │
│  Dangling commit = commit with no ref; found by git fsck --lost-found                                 │
│  non-fast-forward= push rejected; remote has commits not in local history                             │
│  Branch protect. = push rejected by server-side policy; check required status checks                  │
│  Permission denied= SSH key not registered or wrong key; test with ssh -T                             │
│  git mergetool   = opens configured 3-way merge editor (vimdiff, kdiff3)                              │
│  reset --hard    = moves HEAD to SHA and discards working tree; use with care                         │
│  cherry-pick     = applies diff of SHA to current branch; recovers specific commit                    │
│  fsck --lost-found= writes dangling objects to .git/lost-found/                                       │
│  Proxy/firewall  = corporate network may block SSH 22; use HTTPS or SSH over 443                      │
│  ssh -T          = tests SSH connection to git@github.com; confirms key accepted                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently encountered problems and fixes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands and log analysis.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Escalation paths and support procedures.</span>
</a>

</div>
