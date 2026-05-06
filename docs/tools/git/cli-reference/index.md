# Git CLI Reference

Commonly used Git commands for version control, branching, and collaboration.

---

## Setup & Config

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor vim
git config --list
git config --global alias.st status
```

---

## Repository

```bash
# Init and clone
git init
git clone <url>
git clone <url> <directory>
git clone --depth 1 <url>       # Shallow clone

# Remotes
git remote -v
git remote add origin <url>
git remote remove <name>
git remote set-url origin <new_url>
```

---

## Status & Log

```bash
git status
git diff
git diff --staged
git diff <branch1>..<branch2>

git log
git log --oneline
git log --oneline --graph --all
git log -p                      # With diffs
git log --author="name"
git log --since="2 weeks ago"
git log --follow <file>
git show <commit>
```

---

## Staging & Committing

```bash
git add <file>
git add .
git add -p                      # Interactive hunk staging

git commit -m "message"
git commit --amend              # Amend last commit (local only)
git commit --amend --no-edit    # Amend without changing message
```

---

## Branches

```bash
# List
git branch
git branch -a                   # Include remotes
git branch -v                   # With last commit

# Create / switch
git branch <name>
git checkout -b <name>
git switch -c <name>            # Modern syntax
git switch <name>

# Rename
git branch -m <old> <new>

# Delete
git branch -d <name>            # Safe delete
git branch -D <name>            # Force delete
git push origin --delete <name> # Delete remote branch

# Track remote
git branch --set-upstream-to=origin/<name>
```

---

## Merge & Rebase

```bash
# Merge
git merge <branch>
git merge --no-ff <branch>      # Always create merge commit
git merge --squash <branch>     # Squash into one commit
git merge --abort

# Rebase
git rebase <branch>
git rebase -i HEAD~3            # Interactive rebase (last 3 commits)
git rebase --continue
git rebase --abort
git rebase --skip
```

---

## Fetch, Pull & Push

```bash
git fetch
git fetch --all
git fetch --prune               # Clean up deleted remote branches

git pull
git pull --rebase               # Rebase instead of merge
git pull origin <branch>

git push
git push -u origin <branch>     # Set upstream and push
git push --force-with-lease     # Safe force push
git push --tags
git push origin :<branch>       # Delete remote branch
```

---

## Stash

```bash
git stash
git stash push -m "description"
git stash list
git stash pop                   # Apply last + remove
git stash apply stash@{0}      # Apply without removing
git stash drop stash@{0}
git stash clear
git stash show -p stash@{0}    # View diff
```

---

## Tags

```bash
git tag
git tag <name>                  # Lightweight tag
git tag -a <name> -m "msg"      # Annotated tag
git tag -a <name> <commit>      # Tag a specific commit
git push origin <tag>
git push --tags
git tag -d <name>               # Delete local tag
git push origin --delete <tag>  # Delete remote tag
```

---

## Reset & Restore

```bash
# Unstage file
git restore --staged <file>

# Discard working directory changes
git restore <file>

# Reset commits (keep changes staged)
git reset --soft HEAD~1

# Reset commits (keep changes unstaged)
git reset --mixed HEAD~1

# Reset commits (discard all changes)
git reset --hard HEAD~1

# Reset to remote state
git fetch && git reset --hard origin/<branch>
```

---

## Cherry-pick

```bash
git cherry-pick <commit>
git cherry-pick <commit1>..<commit2>
git cherry-pick --no-commit <commit>
git cherry-pick --abort
```

---

## Bisect

```bash
git bisect start
git bisect bad                  # Current commit is bad
git bisect good <commit>        # Last known good commit
git bisect good / git bisect bad
git bisect reset
```

---

## Submodules

```bash
git submodule add <url> <path>
git submodule update --init --recursive
git submodule foreach git pull
```

---

## Useful Aliases

```bash
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.undo "reset --soft HEAD~1"
git config --global alias.unstage "restore --staged"
git config --global alias.aliases "config --get-regexp alias"
```
