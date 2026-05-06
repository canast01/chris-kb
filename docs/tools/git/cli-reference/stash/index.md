# Stash

> Part of the Git CLI Reference.

---

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
