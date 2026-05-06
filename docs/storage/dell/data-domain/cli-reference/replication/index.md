# Replication

> Part of the Dell Data Domain CLI Reference.

---

```bash
# Status
replication show all
replication show config
replication show stats

# Context operations
replication add source mtree://<src_host>/data/col1/<mtree> destination mtree://<dst_host>/data/col1/<mtree>
replication initialize <context_id>
replication resync <context_id>
replication sync <context_id>
replication break <context_id>

# Monitoring lag
replication status
replication show stats | grep lag

# Failover (passive side)
replication failover <context_id>
```
