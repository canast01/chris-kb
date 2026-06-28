---
tags:
  - architecture
  - dell
---
# SRDF/S — Integrations

<div class="kb-summary">
SRDF/S integrations: SRDF/Star three-site topology, Microsoft Cluster Services with SRDF/S, Oracle RAC extended cluster, and VMware Metro Storage Cluster.

*Applies to: SRDF/S*
</div>
![SRDF/S — Integrations](../../../../assets/storage-dell-srdf-s-architecture-integrations.svg)

---

## vMSC and SRM Integration Topology

```mermaid
graph TD
    subgraph siteA ["Site A — Production"]
        vcA["vCenter\n(Site A)"]
        srmA["SRM Server\n(Protected Site)"]
        sra1["Dell SRA"]
        esxiA["ESXi Hosts\n(Active VMs)"]
        r1["PowerMax R1"]
        vcA --- srmA
        srmA --- sra1
        esxiA -->|"FC / iSCSI paths"| r1
    end

    subgraph siteB ["Site B — Metro DR"]
        vcB["vCenter\n(Site B)"]
        srmB["SRM Server\n(Recovery Site)"]
        sra2["Dell SRA"]
        esxiB["ESXi Hosts\n(standby)"]
        r2["PowerMax R2"]
        vcB --- srmB
        srmB --- sra2
        esxiB -.->|"at failover only"| r2
    end

    r1 -->|"SRDF/S synchronous"| r2
    srmA <-->|"SRM pairing"| srmB
    sra1 --> r1
    sra2 --> r2
```

---

## Backup from R2

To offload backup I/O from production (R1), take SnapVX snapshots on the R2 side:

```bash
symsnap -sid <target_SID> -sg <sg_name> create -name BACKUP_$(date +%Y%m%d) -ttl 3
# Mount the linked copy to a backup proxy server
symsnap -sid <target_SID> -sg <sg_name> link -name BACKUP_$(date +%Y%m%d) -lnsg <proxy_sg>
```

Note: always snapshot the R2 while it is in `Synchronized` state to ensure consistency.

---

## See also

- [Srdf S — How It Works](../how-it-works/)
- [Srdf S — Design Standards](../design-standards/)
