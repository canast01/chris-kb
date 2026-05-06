# MTrees (Data Management Units)

> Part of the Dell Data Domain CLI Reference.

---

```bash
# List MTrees
mtree list
mtree show <mtree_name>

# Create / delete
mtree create /data/col1/<mtree_name>
mtree delete /data/col1/<mtree_name>

# Quota
mtree quota set hard-limit <size> <unit> /data/col1/<mtree_name>
mtree quota show
```
