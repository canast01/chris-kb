# Replication

> Part of the Dell Unity CLI Reference (Unisphere CLI).

---

```bash
# Replication sessions
uemcli -d <ip> /prot/rep/session show
uemcli -d <ip> /prot/rep/session show -detail

# Pause / resume
uemcli -d <ip> /prot/rep/session -id <session_id> pause
uemcli -d <ip> /prot/rep/session -id <session_id> resume

# Failover
uemcli -d <ip> /prot/rep/session -id <session_id> failover -keepSync

# Sync
uemcli -d <ip> /prot/rep/session -id <session_id> sync
```
