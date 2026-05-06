# Discovery & Array Info

> Part of the Dell PowerMax CLI Reference (SYMCLI).

---

```bash
# List all known arrays
symcfg list
symcfg discover
symcfg -sid <sid> list -v
symcfg -sid <sid> show

# Directors and ports
symcfg -sid <sid> list -dir all
symcfg -sid <sid> list -port all

# Cache and memory
symcfg -sid <sid> list -cache
symcfg -sid <sid> list -pool -all
```
