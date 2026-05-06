# Performance & Statistics

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# Live cluster stats
isi statistics system list
isi statistics client list
isi statistics protocol list

# Protocol breakdown
isi statistics protocol list --protocol nfs3
isi statistics protocol list --protocol smb2

# Drive stats
isi statistics drive list

# Node-level stats
isi statistics node list
isi statistics node list --node-id <node_id>

# Throughput and IOPS
isi statistics query current --stats node.clientstats.active.nfs

# Performance history
isi statistics history list
```
