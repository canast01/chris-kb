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
```mermaid
flowchart TD
    measureWrite["Measure Peak Write Rate\nsymrdf -g rdfg query -v | grep MBs Written"]
    calcBW["Calculate Required Bandwidth\npeak_rate x 1.20 headroom"]
    checkLink["Compare Against Current\nSRDF Link Capacity"]
    sufficient{"Bandwidth\nSufficient?"}
    ok["OK — proceed with\ncurrent link provisioning"]
    upgrade["Engage Network Team\nIncrease WAN Capacity\nor adjust cycle time"]
    monitorCycle["Monitor Cycle Completion Rate\nfor 30 days after change"]

    measureWrite --> calcBW
    calcBW --> checkLink
    checkLink --> sufficient
    sufficient -->|"Yes"| ok
    sufficient -->|"No"| upgrade
    ok --> monitorCycle
    upgrade --> monitorCycle

    style ok fill:#15803d,color:#fff
    style upgrade fill:#be123c,color:#fff
```

---

## See also

- [Srdf A — How It Works](how-it-works/)
- [Srdf A — Integrations](integrations/)
- [Srdf A — Deploy](../deploy/)
