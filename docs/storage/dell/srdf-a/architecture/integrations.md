---
tags:
  - architecture
  - dell
---
# SRDF/A — Integrations

<div class="kb-summary">
SRDF/A integrations: coexistence with TimeFinder snapshots, RecoverPoint on VMAX, EMC SRDF/EDP (extended distance), and Symmetrix DMX compatibility.

*Applies to: SRDF/A*
</div>
![SRDF/A — Integrations](../../../../assets/storage-dell-srdf-a-architecture-integrations.svg)

---

## SRM Integration Topology

```mermaid
graph TD
    subgraph prodSite ["Production Site"]
        srmProd["SRM Server\n(Protected Site)"]
        sra1["Dell SRA\n(SRM Plugin)"]
        unisphere1["Unisphere for PowerMax"]
        r1array["PowerMax R1"]
        srmProd --- sra1
        sra1 --> unisphere1
        unisphere1 --> r1array
    end

    subgraph drSite ["DR Site"]
        srmDr["SRM Server\n(Recovery Site)"]
        sra2["Dell SRA\n(SRM Plugin)"]
        unisphere2["Unisphere for PowerMax"]
        r2array["PowerMax R2"]
        srmDr --- sra2
        sra2 --> unisphere2
        unisphere2 --> r2array
    end

    r1array -->|"SRDF/A async replication"| r2array
    srmProd <-->|"SRM pairing channel"| srmDr
```

---

## See also

- [Srdf A — How It Works](how-it-works/)
- [Srdf A — Design Standards](design-standards/)
