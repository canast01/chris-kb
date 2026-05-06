# Network

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# Interfaces
isi network interfaces list
isi network interfaces view <iface>

# Subnets
isi network subnets list
isi network subnets view <subnet_name>

# IP pools
isi network pools list
isi network pools view <pool_name>
isi network pools create --name <pool> --subnet <subnet> --access-zone <zone>

# Rules (SmartConnect)
isi network rules list
isi network rules view <rule_name>

# DNS
isi network dns view
isi network external settings view

# Ping / connectivity
ping <ip>
isi network interfaces list --node-id <node_id>
```
