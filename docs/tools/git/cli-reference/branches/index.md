# Branches

> Part of the Git CLI Reference.

---

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
