# Merge & Rebase

> Part of the Git CLI Reference.

---

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
