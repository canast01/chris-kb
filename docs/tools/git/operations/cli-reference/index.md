# Git — CLI Reference


<div class="kb-summary">
Git is the standard distributed version control system. Every developer has a full copy of the repository history — commits, branches, and tags. Changes are staged before committing, and synced with remote repositories via push/pull.
</div>

> Install: `brew install git` (macOS), `apt install git` (Debian/Ubuntu), or download from git-scm.com. Configure once with `git config --global user.name` and `git config --global user.email`.

---

## Setup, Config & Remotes

One-time configuration for Git identity and editor preferences. Remotes are named pointers to other copies of the repository (typically `origin` = the server you cloned from).

```bash
# Identity (required — used in every commit you make)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor vim
git config --list

# Useful alias
git config --global alias.st status

# Initialize and clone
git init
git clone <url>
git clone <url> <directory>
git clone --depth 1 <url>       # shallow clone — just the latest snapshot, no full history

# Remotes
git remote -v
git remote add origin <url>
git remote remove <name>
git remote set-url origin <new_url>
```
┌───────────────────────────────────────── Git — CLI Reference ─────────────────────────────────────────┐
│                                                                                                       │
│  Essential Git CLI commands grouped by workflow area with common flags and usage patterns.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Basic Operations               │  │                  Branching                  │   │
│   │          git init / git clone <url>          │  │           git branch [-a|-r|-d|-D]          │   │
│   │         git add [-p | .] / git reset         │  │            git checkout -b <name>           │   │
│   │             git commit -m "msg"              │  │            git switch [-c] <name>           │   │
│   │       git status / git diff [--cached]       │  │         git merge [--no-ff] <branch>        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    add -p stages hunks interactively; diff --cached shows staged vs last commit                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Remote and History              │  │                   Advanced                  │   │
│   │        git fetch [--prune] / git pull        │  │            git rebase [-i] <base>           │   │
│   │      git push [-u] [--force-with-lease]      │  │          git stash [push|pop|list]          │   │
│   │         git log [--oneline --graph]          │  │            git cherry-pick <sha>            │   │
│   │        git tag -a <v> -m / push <tag>        │  │          git bisect start/good/bad          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Developer workstation · terminal / shell · Git remote server                                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  git add -p        = interactive hunk staging; review each change before staging                      │
│  diff --cached     = shows staged changes relative to last commit                                     │
│  --force-with-lease= safe force push; fails if remote has unexpected commits                          │
│  rebase -i         = interactive rebase; squash/edit/reorder commits                                  │
│  git bisect        = binary search commits to find regression-introducing commit                      │
│  stash push        = save dirty working tree with optional message                                    │
│  stash pop         = restore last stash and remove from stash stack                                   │
│  cherry-pick       = apply diff of specific commit to current branch                                  │
│  --no-ff           = always create merge commit even for fast-forward                                 │
│  branch -D         = force-delete branch even if not merged                                           │
│  git switch -c     = create and switch (modern alternative to checkout -b)                            │
│  log --graph       = ASCII graph of branch/merge topology in terminal                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## Staging & Committing

Changes must be explicitly staged before they're included in a commit. `git add -p` lets you stage individual hunks — useful for splitting one set of edits into multiple focused commits.

```bash
git add <file>
git add .                        # stage everything in the current directory
git add -p                       # interactive: choose which hunks to stage

git commit -m "message"
git commit --amend               # rewrite the last commit (local-only — don't amend pushed commits)
git commit --amend --no-edit     # amend without changing the message
```

---

## Branches

Branches are cheap and fast in Git — create them freely to isolate work. The modern `git switch` command is cleaner than `git checkout` for branch operations.

```bash
# List
git branch
git branch -a                   # include remote-tracking branches
git branch -v                   # with last commit

# Create / switch
git branch <name>
git checkout -b <name>          # create and switch (classic syntax)
git switch -c <name>            # create and switch (modern syntax)
git switch <name>               # switch to existing branch

# Rename
git branch -m <old> <new>

# Delete
git branch -d <name>            # safe delete (refuses if unmerged)
git branch -D <name>            # force delete
git push origin --delete <name> # delete the remote branch

# Set upstream (track remote branch)
git branch --set-upstream-to=origin/<name>
```

---

## Merge & Rebase

Merge integrates changes from another branch. Rebase replays your commits on top of another branch — it creates a linear history but rewrites commits (never rebase shared/pushed commits).

```bash
# Merge
git merge <branch>
git merge --no-ff <branch>      # always create a merge commit (even if fast-forward possible)
git merge --squash <branch>     # squash all branch commits into one unstaged change
git merge --abort               # abort a conflicted merge

# Rebase (replay current branch commits on top of <branch>)
git rebase <branch>
git rebase -i HEAD~3            # interactive rebase of last 3 commits (squash, reword, drop)
git rebase --continue           # after resolving conflicts
git rebase --abort
git rebase --skip
```

---

## Fetch, Pull & Push

Fetch downloads changes from the remote without applying them. Pull downloads and merges (or rebases) them. Push uploads your commits to the remote.

```bash
git fetch
git fetch --all                 # fetch all remotes
git fetch --prune               # also remove remote-tracking branches that no longer exist

git pull
git pull --rebase               # rebase instead of merge (keeps linear history)
git pull origin <branch>

git push
git push -u origin <branch>     # push and set upstream tracking
git push --force-with-lease     # safe force push — fails if remote has changes you haven't seen
git push --tags                 # push all tags
git push origin :<branch>       # delete a remote branch (older syntax)
```

---

## Stash

Stash saves your uncommitted changes temporarily so you can switch context. It's a stack — you can have multiple stashes, each identified by `stash@{n}`.

```bash
git stash
git stash push -m "description"  # stash with a label
git stash list
git stash pop                    # apply top stash and remove it from the stack
git stash apply stash@{0}        # apply without removing from stack
git stash drop stash@{0}         # remove a specific stash
git stash clear                  # remove all stashes
git stash show -p stash@{0}      # view the diff of a stash
```

---

## Tags

Tags mark specific commits — typically used for release versions. Annotated tags include a message and are the standard for releases. Lightweight tags are just a pointer to a commit.

```bash
git tag                          # list all tags
git tag <name>                   # create lightweight tag at HEAD
git tag -a <name> -m "msg"       # create annotated tag (preferred for releases)
git tag -a <name> <commit>       # annotate a specific past commit
git push origin <tag>            # push a single tag
git push --tags                  # push all tags
git tag -d <name>                # delete local tag
git push origin --delete <tag>   # delete remote tag
```

---

## Reset & Restore

Undo staged changes, discard working directory edits, or move the branch pointer back to an earlier commit. `--hard` discards everything — use with care.

```bash
# Unstage a file (keep the changes in working directory)
git restore --staged <file>

# Discard working directory changes (permanent — gone immediately)
git restore <file>

# Move branch pointer back N commits
git reset --soft HEAD~1          # move pointer back, keep changes staged
git reset --mixed HEAD~1         # move pointer back, keep changes unstaged (default)
git reset --hard HEAD~1          # move pointer back, discard all changes

# Reset to match the remote branch exactly
git fetch && git reset --hard origin/<branch>
```

---

## Advanced (Cherry-pick, Bisect, Submodules)

Specialized tools for precise commit selection, binary-search debugging, and managing repositories-within-repositories.

### Cherry-pick

Apply a specific commit from another branch onto the current branch — useful when you want one fix without merging an entire feature branch.

```bash
git cherry-pick <commit>
git cherry-pick <commit1>..<commit2>   # range (exclusive start)
git cherry-pick --no-commit <commit>   # apply changes without committing
git cherry-pick --abort
```

### Bisect

Binary-search through commit history to find which commit introduced a bug. Git checks out the midpoint, you test and mark good/bad, and it narrows down automatically.

```bash
git bisect start
git bisect bad                   # mark current commit as broken
git bisect good <commit>         # mark last known working commit
# Git checks out the midpoint — test it, then:
git bisect good                  # or: git bisect bad
git bisect reset                 # end bisect session
```

### Submodules

Embed another Git repository inside your repo. Useful for vendored dependencies or shared libraries managed separately.

```bash
git submodule add <url> <path>
git submodule update --init --recursive   # after cloning a repo with submodules
git submodule foreach git pull            # update all submodules to latest
```

### Useful Aliases

```bash
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.undo "reset --soft HEAD~1"
git config --global alias.unstage "restore --staged"
git config --global alias.aliases "config --get-regexp alias"
```
