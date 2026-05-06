# Events & Alerts

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# View events
isi event events list
isi event events list --severity critical
isi event events list --start-time <YYYY-MM-DD>

# Acknowledge / resolve events
isi event events resolve <event_id>

# Alert channels
isi event channels list
isi event channels view <channel_name>

# SNMP
isi snmp settings view
```
