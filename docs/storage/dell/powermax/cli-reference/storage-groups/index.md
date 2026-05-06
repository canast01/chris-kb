# Storage Groups

> Part of the Dell PowerMax CLI Reference (SYMCLI).

---

```bash
# List
symsg list -sid <sid>
symsg list -sid <sid> -v
symsg show <sg_name> -sid <sid>
symsg show <sg_name> -sid <sid> -v

# Create / delete
symsg create <sg_name> -sid <sid> -type regular
symsg create <sg_name> -sid <sid> -type parent
symsg delete <sg_name> -sid <sid>

# Add / remove devices
symsg -sid <sid> -sg <sg_name> add dev <devname>
symsg -sid <sid> -sg <sg_name> remove dev <devname>

# Add child SG to parent SG
symsg -sid <sid> -sg <parent_sg> add sg <child_sg>
symsg -sid <sid> -sg <parent_sg> remove sg <child_sg>

# Rename
symsg rename <old_sg> -new_sg_name <new_sg> -sid <sid>
```
