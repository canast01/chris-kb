# Device Groups (Legacy)

> Part of the Dell PowerMax CLI Reference (SYMCLI).

---

```bash
# Create and manage device groups
symdg list -sid <sid>
symdg show <dg_name> -sid <sid>
symdg create <dg_name> -type regular -sid <sid>
symdg delete <dg_name> -sid <sid>
symdg -g <dg_name> add dev <devname> -sid <sid>
symdg -g <dg_name> remove dev <devname> -sid <sid>
```
