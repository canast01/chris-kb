---
tags:
  - architecture
  - san
---
# Cisco DCNM — Design Standards
![Cisco DCNM — Design Standards](../../../../assets/san-cisco-cisco-dcnm-architecture-design-standards.svg)


```bash
# On each MDS switch (NX-OS CLI)
zone default-zone permit vsan 10
# Expected after setting deny:
no zone default-zone permit vsan 10
# Verify:
show zone status vsan 10
# Mode: Basic, Default-zone: deny
```


---

```d2
direction: right

center: "Cisco DCNM" {shape: hexagon}
component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

center -> component_a
center -> component_b
center -> component_c
```

## See also

- [Cisco Dcnm — How It Works](how-it-works/)
- [Cisco Dcnm — Integrations](integrations/)
- [Cisco Dcnm — Deploy](../deploy/)
