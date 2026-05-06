# VSANs

> Part of the [Cisco MDS NX-OS CLI Reference](../).

---

```bash
# VSAN status
show vsan
show vsan <id>
show vsan membership
show vsan membership interface fc<slot/port>

# Create VSAN
vsan database
  vsan <id> name "<name>"

# Assign port to VSAN
vsan database
  vsan <id> interface fc<slot/port>
```
