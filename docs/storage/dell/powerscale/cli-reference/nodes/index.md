# Nodes

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# List nodes
isi node list
isi node view <node_id>

# Node hardware details
isi node hardware view <node_id>

# Node drives
isi node drives list <node_id>
isi node drives view <node_id> <bay>

# Node sensors
isi node sensors view <node_id>

# Smartfail / readd a node
isi devices smartfail -d <node_id>
isi devices add -d <node_id>
```
