# Reset & Restore

> Part of the Git CLI Reference.

---

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
