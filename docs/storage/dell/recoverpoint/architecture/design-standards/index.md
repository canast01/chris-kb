---
tags:
  - architecture
  - dell
---
# RecoverPoint — Standards


<div class="kb-summary">
Part of the [RecoverPoint](../../index.md) > [Architecture](../index.md) reference.
</div>

---

## Naming Conventions

### Consistency Groups

```text
┌─────────────────────────────────── RecoverPoint — Design Standards ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Design principles: right-size RPAs, journal volumes, and WAN bandwidth before deployment   │   │
│   │  RPA count: 2 minimum per site; add one RPA per 50 protected VMs or 500 MB/s write throughput │   │
│   │       Journal size: (peak write MB/s) × (CDP window hours) × 3600 × 1.3 overhead factor       │   │
│   │   WAN bandwidth: match replication throughput; deduplicated traffic typically 30–50% of raw   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          RPA Sizing         │  │        Journal Sizing       │  │        Network Design       │   │
│   │        2 RPA minimum        │  │      2–24 hr CDP window     │  │     Dedicated repl VLAN     │   │
│   │        1 RPA / 50 VMs       │  │     ×1.3 overhead factor    │  │        MTU 9000 jumbo       │   │
│   │      4 vCPU / 8 GB RAM      │  │      Separate datastore     │  │      QoS priority class     │   │
│   │     Anti-affinity rules     │  │     VMDK thin provision     │  │      WAN dedup enabled      │   │
│   │       Mgmt IP per RPA       │  │      Alarm on >80% full     │  │       Latency <100 ms       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Physical: RPA VMs pinned to dedicated ESXi hosts; journal on separate LUNs from prod               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RPA sizing          = Calculate RPA count from VM count and write throughput; minimum 2 per site   │
│    Journal sizing      = Peak writes × CDP window × overhead; use RP Sizer tool for accuracy          │
│    CDP window          = How far back in time the journal allows recovery; typically 2–24 hours       │
│    Overhead factor     = 1.3× buffer for journal metadata, sequencing, and burst write absorption     │
│    Anti-affinity       = DRS rule keeping RPA VMs on separate ESXi hosts for HA                       │
│    Dedicated VLAN      = Isolate RPA replication traffic from production VM and management traffic    │
│    Jumbo frames        = MTU 9000 on replication VLAN; reduces fragmentation; improves throughput     │
│    QoS                 = DSCP marking on replication traffic; prioritised over bulk data transfers    │
│    CG design           = Group VMs by application tier; same CG = same RPO and same failover unit     │
│    RP Sizer            = Dell sizing tool; inputs write rate, change rate, and WAN link speed         │
│    Thin provision      = Journal VMDKs thin-provisioned; grow on demand up to alarm threshold         │
│    WAN dedup           = RPA deduplicates replication stream; reduces bandwidth by ~30–50%            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
