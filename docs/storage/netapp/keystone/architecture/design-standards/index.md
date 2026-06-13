---
tags:
  - architecture
  - netapp
---
# Keystone — Standards


<div class="kb-summary">
Standards reference covering Service Level Selection, Naming Conventions, Capacity Management.
</div>

```text
┌─────────────────────────── NetApp Keystone — Architecture Design Standards ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Design standards: service level -> hardware, network redundancy, sizing, burst        │   │
│   │          Extreme: AFF A-series NVMe; <1ms latency; 10k+ IOPS/TB committed throughput          │   │
│   │            Network: dedicated NFS/iSCSI VLAN MTU 9000; dual FC; separate mgmt VLAN            │   │
│   │           HA: dual-node ONTAP cluster; storage failover within 60 s; SFO/CFO policy           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Workload SLO -> tier -> NW design -> multipath -> committed sizing -> burst budget                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Tier Standards       │  │        Network Design       │  │         HA & Sizing         │   │
│   │        Extreme: NVMe        │  │        Dedicated VLAN       │  │         Dual node HA        │   │
│   │       Premium: AFF SSD      │  │         MTU 9000 NFS        │  │         SFO 60 s RTO        │   │
│   │        Standard: SSD        │  │        Dual FC fabric       │  │        MPIO 4+ paths        │   │
│   │          Value: HDD         │  │        OOB mgmt VLAN        │  │        Commit 70-80%        │   │
│   │       Burst 20% extra       │  │         IPMI/BMC OOB        │  │       Burst alert 90%       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Commit 70-80% of expected peak; burst rate covers spikes; review quarterly with KSM                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Area       │     Standard     │        Why        │      Verify      │      Notes       │   │
│   │     NFS MTU      │    9000 jumbo    │     Throughput    │   ping -s 8972   │    End-to-end    │   │
│   │    Multipath     │    ALUA/MPIO     │      4 paths      │   sanlun show    │     FC/iSCSI     │   │
│   │    Committed     │   70-80% peak    │      Cost ctl     │    Active IQ     │    Quarterly     │   │
│   │   Burst alert    │   90% of burst   │     Avoid fees    │    Alert rule    │   Auto notify    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: AFF/FAS nodes in rack · dual 10/25 GbE per node · 16/32Gb HBAs for FC                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SFO      = Storage Failover; ONTAP HA takeover of partner node storage in <60 s                    │
│    CFO      = Controller Failover; faster variant; non-disruptive LIF failover                        │
│    MPIO     = Multipath I/O; OS driver balancing I/O across multiple HBA/NIC paths                    │
│    ALUA     = Asymmetric Logical Unit Access; preferred vs non-preferred path hints                   │
│    MTU 9000 = Jumbo frames for NFS/iSCSI; requires end-to-end switch config                           │
│    Burst    = Capacity above committed level; billed at premium burst rate                            │
│    KSM      = Keystone Success Manager; NetApp advisor for capacity planning                          │
│    BMC      = Baseboard Management Controller; OOB access for remote power/console                    │
│    IPMI     = Intelligent Platform Management Interface; OOB management standard                      │
│    NVMe-oF  = NVMe over Fabrics (FC or TCP); <100 us block latency                                    │
│    AFF A    = AFF A-series; all-NVMe flash; highest performance tier                                  │
│    AFF C    = AFF C-series; capacity-optimised all-flash; QLC NAND                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Keystone Architecture](../index.md) reference.

---

## Service Level Selection

- Map each application tier to the appropriate Keystone service tier before provisioning: Extreme for databases and high-IOPS workloads, Premium for virtualization and mixed workloads, Standard for file and backup
- Document the committed capacity per tier per application in the CMDB or capacity register
- Review burst usage monthly — persistent burst usage signals that committed capacity should be increased at the next amendment opportunity
- Do not downgrade a workload from a higher performance tier to a lower one mid-subscription; plan service level assignments carefully at provisioning time

## Naming Conventions

- Volume naming follows the site-standard naming convention; do not deviate for Keystone-managed volumes
- Tag each volume with the application owner and Keystone service level to enable accurate consumption attribution and chargeback
- Use QoS policy-group names that clearly identify the Keystone service level, e.g., `extreme-ks`, `premium-ks`, `standard-ks` — this reduces the risk of volumes being assigned to the wrong tier
- Snapshots on Keystone volumes follow the same naming convention as standard ONTAP snapshots; excessive snapshots on premium tiers consume high-cost committed capacity unnecessarily

## Capacity Management

| Threshold | Action |
|---|---|
| 70% of committed capacity | Internal review; forecast growth timeline |
| 80% of committed capacity | Alert triggered; begin capacity amendment process |
| 90% of committed capacity | Burst activates; escalate to Keystone Success Manager |
| Burst limit reached | Further provisioning blocked; emergency amendment required |

- Set EMS capacity threshold alerts at 80% of committed tier within ONTAP; configure BlueXP notifications for Keystone capacity events
- Request a committed capacity increase at least 60 days before anticipated growth to allow for NetApp procurement and order processing
- Generate and archive monthly consumption reports from the BlueXP digital wallet for internal chargeback or showback to business units
