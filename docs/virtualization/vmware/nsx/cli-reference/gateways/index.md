# Tier-0 and Tier-1 Gateways

> Part of the [NSX-T CLI Reference](../).

---

## Tier-0 and Tier-1 Gateways

```bash
# List gateways (NSX Manager)
get logical-routers

# On an Edge Node — enter router context
vrf <logical-router-id>

# Show routes
get route
get route detail
get bgp neighbor summary
get bgp neighbor <neighbor_ip>
get bgp neighbor <neighbor_ip> routes

# Forwarding table
get forwarding

# Interfaces
get interfaces
get interface <name>
```
