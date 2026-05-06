# Events & Audit

> Part of the Dell PowerMax CLI Reference (SYMCLI).

---

```bash
# Events
symevent list -sid <sid>
symevent list -sid <sid> -v
symevent list -sid <sid> -start_time "01/01/2025 00:00:00"
symevent list -sid <sid> -start_time "01/01/2025 00:00:00" -end_time "01/02/2025 00:00:00"

# Audit log
symaudit list -sid <sid>
symaudit list -sid <sid> -v
symaudit list -sid <sid> -start_time "01/01/2025 00:00:00"
symaudit list -sid <sid> -user <username>
```
