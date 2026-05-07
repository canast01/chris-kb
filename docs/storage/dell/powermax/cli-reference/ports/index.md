# Ports & Hardware

> Part of the Dell PowerMax CLI Reference (SYMCLI).
---

## Ports

```bash
# List all ports
symport list -sid <sid>
symport list -sid <sid> -v
symport -sid <sid> -dir <dir> -p <port> show

# Fibre Channel login info
symport list -sid <sid> -logged_in
symport -sid <sid> -dir <dir> -p <port> list -logged_in
```

## Physical Disks & Hardware

```bash
# Physical disks
sympd list -sid <sid>
sympd list -sid <sid> -failed
sympd list -sid <sid> -spare
sympd show <pd_name> -sid <sid>

# Disk groups
symdisk list -sid <sid>
symdisk list -sid <sid> -failed
symdisk list -sid <sid> -v

# Hardware status
symcfg -sid <sid> list -disk
symcfg -sid <sid> list -bay
```
