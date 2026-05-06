# Edge Nodes

> Part of the [NSX-T CLI Reference](../).

---

## Edge Nodes

```bash
# Connect to Edge Node via SSH (admin)
get services
get service dataplane
get service router

# System
get node
get node cpu-usage
get node memory

# Uplinks
get interfaces
get interface fp-eth0

# Routing
vrf <lr_id>
get route
get forwarding
get bgp neighbor summary

# Connectivity tests
ping <ip>
traceroute <ip>
curl http://<ip>
```
