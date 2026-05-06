# Interfaces & Ports

> Part of the [Cisco MDS NX-OS CLI Reference](../).

---

```bash
# Interface status
show interface brief
show interface fc<slot/port>
show interface fc<slot/port> counters
show interface fc<slot/port> transceiver

# Port configuration
interface fc<slot/port>
  switchport mode {auto | E | F | Fx | NP | TE | SD | ST}
  shutdown
  no shutdown

# Bulk operations
show interface fc<slot/port> - fc<slot/port> brief

# Physical topology
show topology
show fcdomain
show fcdomain domain-list
```
