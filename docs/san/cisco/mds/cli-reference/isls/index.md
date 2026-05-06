# ISLs & Trunking

> Part of the [Cisco MDS NX-OS CLI Reference](../).

---

```bash
# ISL status
show topology
show trunk
show interface trunk

# TE port (trunking)
interface fc<slot/port>
  switchport trunk allowed vsan <id>
  switchport mode TE
  no shutdown
```
