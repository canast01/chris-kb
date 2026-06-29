---
tags:
  - git
  - operations
---
# Git — CLI Reference

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


```text title="Expected output"
user.name=Your Name
user.email=you@example.com
core.editor=vim
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
user.name=Your Name
user.email=you@example.com
core.editor=vim
alias.st=status
Initialized empty Git repository in /home/admin/project/.git/
Cloning into 'repo-name'...
remote: Enumerating objects: 2847, done.
remote: Counting objects: 100% (2847/2847), done.
remote: Compressing objects: 100% (1204/1204), done.
Receiving objects: 100% (2847/2847), 18.5 MiB | 2.3 MiB/s, done.
Resolving deltas: 100% (1456/1456), done.
origin  https://git.company.com/infra/repo-name.git (fetch)
origin  https://git.company.com/infra/repo-name.git (push)
```

!!! warning "Common errors"
    **`fatal: not a git repository (or any of the parent directories): .git`** — Run `git init` in the target directory or `git clone` to create a repository first.
    **`fatal: repository not found`** — Verify the repository URL is correct and you have network access; check SSH keys or HTTPS credentials if authentication is required.
    **`error: could not lock config file /home/user/.gitconfig: Permission denied`** — Run the command with appropriate permissions or check file ownership with `ls -la ~/.gitconfig`.
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

```text title="Expected output"
* main
  develop
  feature/auth-system
  hotfix/login-bug

* develop
  feature/auth-system
  hotfix/login-bug
  main
  remotes/origin/develop
  remotes/origin/main
  remotes/origin/staging

  main                    a3f2e1c Merge pull request #847 from team/feature-x
  develop                 7b9d4f2 Refactor authentication module
  feature/auth-system     e8c1a9f Add OAuth2 provider support
  hotfix/login-bug        2d5f6e3 Fix session timeout issue

Renamed branch 'hotfix/login-bug' to 'hotfix/session-timeout'
error: The branch 'old-feature' is not fully merged.
Deleted branch old-feature (was 2d5f6e3).
To github.com:company/repo.git
 - [deleted]             old-feature

Branch 'develop' set up to track remote branch 'develop' from 'origin'.
```

!!! warning "Common errors"
    **`error: The branch 'old-feature' is not fully merged.`** — Use `git branch -D <name>` to force delete, or merge the branch first with `git merge <name>`.
    **`error: pathspec 'feature-name' did not match any file(s) known to git`** — Verify the branch exists with `git branch -a` and check for typos or whitespace in the branch name.
    **`error: refname refs/heads/main not found`** — Ensure you're in a valid git repository with `git status` and that the branch name is correct.
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

```text title="Expected output"
$ git merge feature/auth
Merge made by the 'recursive' strategy.
 src/auth.js | 42 ++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 42 insertions(+)

$ git merge --no-ff feature/payment
Merge made by the 'recursive' strategy.
 src/payment.js | 18 ++++++++++++++++++
 1 file changed, 18 insertions(+)

$ git merge --squash feature/docs
Squashing commits from feature/docs
Auto-merging README.md
SQUASH MERGE ... Squashed 4 commits into working directory

$ git rebase main
Successfully rebased and updated refs/heads/develop.

$ git rebase -i HEAD~3
[detached HEAD 8f3a2c1] Fix: update validation logic
 Date: Thu Jan 16 14:22:09 2025 +0000
 1 file changed, 12 insertions(+)
Rebase in progress; onto 5d7e9b4
You are currently rebasing branch 'feature/api' on '5d7e9b4'.

$ git rebase --continue
[detached HEAD 9c4b1e2] Refactor: simplify error handling
 1 file changed, 8 insertions(+)
Successfully rebased and updated refs/heads/feature/api.
```

!!! warning "Common errors"
    **`error: Your local changes to the following files would be overwritten by merge: src/config.js`** — Commit or stash your changes before merging with `git stash` or `git add && git commit`.
    **`CONFLICT (content): Merge conflict in src/utils.js`** — Resolve conflicts manually in the editor, then run `git add <file>` and `git merge --continue`.
    **`fatal: No rebase in progress`** — You attempted `git rebase --continue` without an active rebase; check status with `git status` first.
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

```text title="Expected output"
remote: Counting objects: 342, done.
remote: Compressing objects: 100% (156/done.
remote: Total 342 (delta 218), reused 289 (delta 189)
Receiving objects: 100% (342/342), 2.45 MiB | 8.32 MiB/s, done.
Resolving deltas: 100% (218/218), done.
From github.com:company/infrastructure
   a7f3e2c..9b1d4f8  main       -> origin/main
   5c8e1a2..6d9f3b4  develop    -> origin/develop
 - [deleted]         feature/old-config
Updating 5c8e1a2..6d9f3b4
Fast-forward
 ansible/playbooks/deploy.yml | 12 ++++++------
 docs/CHANGELOG.md            |  4 ++++
 2 files changed, 8 insertions(+), 4 deletions(-)
To github.com:company/infrastructure
 * [new branch]      feature/new-feature -> origin/feature/new-feature
 * [new tag]         v2.3.1 -> v2.3.1
```

!!! warning "Common errors"
    **`fatal: The current branch main has no upstream branch.`** — Run `git push -u origin main` to set the upstream tracking branch before pushing.
    **`error: failed to push some refs to 'github.com:company/infrastructure'`** — Pull the latest changes with `git pull --rebase` and resolve any conflicts before pushing again.
    **`fatal: refusing to merge unrelated histories`** — Add the `--allow-unrelated-histories` flag to your pull command if intentionally merging divergent branches.
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

```text title="Expected output"
Saved working directory and index state WIP on main: a3f8c2e Add user authentication module
Saved working directory and index state On main: description
stash@{0}: On main: description
stash@{1}: WIP on main: a3f8c2e Add user authentication module
stash@{2}: WIP on develop: 7b2d1f9 Fix database connection pool
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
diff --git a/config/auth.js b/config/auth.js
index 4e8c9d1..2f3a4c6 100644
--- a/config/auth.js
+++ b/config/auth.js
@@ -12,7 +12,7 @@ module.exports = {
-  timeout: 3000,
+  timeout: 5000,
   retries: 2
 };
```

!!! warning "Common errors"
    **`No stash entries found.`** — Verify stashes exist with `git stash list` before attempting `pop`, `apply`, or `drop`.
    **`error: pathspec 'stash@{0}' did not match any file(s) known to git`** — Use the correct stash reference from `git stash list` output (e.g., `stash@{1}` if `stash@{0}` doesn't exist).
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

```text title="Expected output"
v1.0.0
v1.1.0
v1.2.1
v2.0.0-beta
v2.0.0
(no output — command completes silently)
(no output — command completes silently)
Enumerating objects: 1, done.
Counting objects: 100% (1/1), done.
Writing objects: 100% (1/1), 194 bytes | 194.00 KiB/s, done.
Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:company/repo.git
 * [new tag]         v2.0.0 -> v2.0.0
(no output — command completes silently)
To github.com:company/repo.git
 - [deleted]         v1.2.1
```

!!! warning "Common errors"
    **`error: tag 'v2.0.0' already exists`** — Use `git tag -d v2.0.0` to delete the local tag first, or choose a different tag name.
    **`error: pathspec 'v1.5.0' did not match any files`** — Verify the tag exists with `git tag` and check the exact spelling.
    **`[rejected] v2.0.0 -> v2.0.0 (already exists)`** — Delete the remote tag with `git push origin --delete v2.0.0` before pushing a new one with the same name.
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

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
From github.com:acme-corp/infrastructure.git
 * branch            main       -> FETCH_HEAD
HEAD is now at 7f3a2c9 Update deployment config for prod-us-east-1
```

!!! warning "Common errors"
    **`error: pathspec '<file>' did not match any files`** — Verify the file path is correct and exists in the repository with `git status`.
    **`fatal: Not a git repository (or any of the parent directories): .git`** — Ensure you are in the root directory of a git repository or navigate to the correct project folder.
    **`error: Your local changes to the following files would be overwritten by merge: <file>`** — Stash uncommitted changes with `git stash` before running `git reset --hard origin/<branch>`.
```bash
git cherry-pick <commit>
git cherry-pick <commit1>..<commit2>   # range (exclusive start)
git cherry-pick --no-commit <commit>   # apply changes without committing
git cherry-pick --abort
```

```text title="Expected output"
[main 7a3f2c9] Fix: resolve authentication timeout in login module
 Date: Thu Mar 14 10:22:15 2024 +0000
 1 file changed, 12 insertions(+), 5 deletions(-)
[main 5b8e1d4] Refactor: simplify database connection pooling
 Date: Thu Mar 14 10:18:42 2024 +0000
 1 file changed, 28 insertions(+), 8 deletions(-)
[main 9c2f6a1] Docs: update API endpoint documentation
 Date: Thu Mar 14 10:15:09 2024 +0000
 1 file changed, 15 insertions(+)
```

!!! warning "Common errors"
    **`error: could not apply <commit>... hint: after resolving the conflicts, mark the resolved files with "git add <paths>" or "git rm <paths>" then run "git cherry-pick --continue"`** — Resolve merge conflicts in the affected files, stage them with `git add`, then run `git cherry-pick --continue`.
    **`fatal: <commit> is not a commit`** — Verify the commit hash or reference exists in the repository using `git log` and ensure you're using the correct commit identifier.
    **`error: your local changes to the following files would be overwritten by merge`** — Commit or stash your current working directory changes with `git stash` before attempting the cherry-pick.
```bash
git bisect start
git bisect bad                   # mark current commit as broken
git bisect good <commit>         # mark last known working commit
# Git checks out the midpoint — test it, then:
git bisect good                  # or: git bisect bad
git bisect reset                 # end bisect session
```

```text title="Expected output"
$ git bisect start
$ git bisect bad
$ git bisect good v1.2.3
Bisecting: 47 revisions left to test after this (roughly 6 steps)
[a7f3e2c1d9b4e8f6a2c5d1e9f3a7b4c6] Merge pull request #1247 from feature/auth-refactor
$ git bisect good
Bisecting: 23 revisions left to test after this (roughly 5 steps)
[5e8d1c2a9f4b7e3d6a1c5f2e8b3a9d4c] Fix session timeout handling
$ git bisect reset
Previous HEAD position was 5e8d1c2a9f4b7e3d6a1c5f2e8b3a9d4c Fix session timeout handling
Switched to branch 'main'
```

!!! warning "Common errors"
    **`fatal: Not a valid object name`** — Verify the commit hash or tag exists with `git log --oneline` before passing it to `git bisect good`.
    **`fatal: You need to have at least one bad and one good commit.`** — Mark at least one commit as bad and one as good before Git can bisect; run `git bisect bad` and `git bisect good <commit>` in sequence.
    **`fatal: cannot bisect with only one old and one new`** — Ensure the "good" commit is actually an ancestor of the "bad" commit; if reversed, start over with `git bisect reset` and swap them.
```bash
git submodule add <url> <path>
git submodule update --init --recursive   # after cloning a repo with submodules
git submodule foreach git pull            # update all submodules to latest
```

```text title="Expected output"
Cloning into '/path/to/submodule'...
remote: Enumerating objects: 1247, done.
remote: Counting objects: 100% (1247/1247), done.
remote: Compressing objects: 100% (892/892), done.
remote: Receiving objects: 100% (1247/1247), 2.34 MiB | 8.92 MiB/s, done.
remote: Resolving deltas: 100% (634/634), done.
Submodule path 'path': checked out 'a3f8e2c1b9d4e7f6a2c5b8e1d4f7a3c6'
Entering 'path'
From github.com:org/submodule-repo
   f2e1d3c..a3f8e2c  main       -> origin/main
Already up to date.
```

!!! warning "Common errors"
    **`fatal: destination path '<path>' already exists and is not an empty directory`** — Remove the existing directory or choose a different path for the submodule.
    **`fatal: No url found for submodule path '<path>' in .gitmodules`** — Ensure the submodule entry exists in `.gitmodules` and run `git submodule sync` before updating.
```bash
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.undo "reset --soft HEAD~1"
git config --global alias.unstage "restore --staged"
git config --global alias.aliases "config --get-regexp alias"
```

```d2
direction: down

verify: "Verify" {shape: rectangle}

```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Git — Procedures](../procedures/)
- [Git — Scripts](../scripts/)
- [Git — Health Checks](../health-checks/)
