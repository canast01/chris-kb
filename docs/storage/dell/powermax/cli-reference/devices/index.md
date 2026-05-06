# Devices

> Part of the Dell PowerMax CLI Reference (SYMCLI).

---

```bash
# List devices
symdev list -sid <sid>
symdev list -sid <sid> -v
symdev list -sid <sid> -assigned
symdev list -sid <sid> -unassigned
symdev list -sid <sid> -mapped
symdev list -sid <sid> -spare
symdev list -sid <sid> -failed
symdev list -sid <sid> -tdev

# Device details
symdev show <devname> -sid <sid>
symdev show <devname> -sid <sid> -v

# Device performance
symdev list -sid <sid> -perf
```
