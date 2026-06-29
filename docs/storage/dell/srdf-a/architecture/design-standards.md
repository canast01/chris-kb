---
tags:
  - architecture
  - dell
---
# SRDF/A — Design Standards
![SRDF/A — Design Standards](../../../../assets/storage-dell-srdf-a-architecture-design-standards.svg)

```bash
symrdf -g <rdfg> query -v | grep "Minimum Cycle Time"
```

```bash
symrdf -g <rdfg> query -v | grep "MBs Written"
```
```bash
symdev show -sid <target_SID> <dev_id> | grep -E "Size|Track"
```
```d2
direction: right

measureWrite: "Measure Peak Write Rate\nsymrdf -g rdfg query -v | grep MBs Written" {shape: rectangle}
calcBW: "Calculate Required Bandwidth\npeak_rate x 1.20 headroom" {shape: rectangle}
checkLink: "Compare Against Current\nSRDF Link Capacity" {shape: rectangle}
sufficient: "sufficient" {shape: rectangle}
ok: "OK — proceed with\ncurrent link provisioning" {shape: rectangle}
upgrade: "Engage Network Team\nIncrease WAN Capacity\nor adjust cycle time" {shape: rectangle}
monitorCycle: "Monitor Cycle Completion Rate\nfor 30 days after change" {shape: rectangle}

measureWrite -> calcBW
calcBW -> checkLink
checkLink -> sufficient
sufficient -> ok
sufficient -> upgrade
ok -> monitorCycle
upgrade -> monitorCycle
```

---

## See also

- [Srdf A — How It Works](../how-it-works/)
- [Srdf A — Integrations](../integrations/)
- [Srdf A — Deploy](../../deploy/)
