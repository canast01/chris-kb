# VMware Design Decisions

<div class="kb-summary">
Architecture decision records for the VMware platform — each decision captures the options considered, the chosen approach, and the reasons behind it. Use these as a starting point when designing a new environment or justifying a recommendation to stakeholders.
</div>

```text
┌──────────────────────────────────── VMware — Design Decisions ────────────────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  Each decision follows: context → options → chosen approach → rationale → trade-offs                  │
│  Decisions are not universal — adjust based on org size, budget, and compliance requirements          │
│                                                                                                       │
│  NETWORKING          STORAGE            COMPUTE / HA         LIFECYCLE            MONITORING          │
│  vSS vs vDS          vSAN vs ext SAN    HA sizing policy      Host profile vs vLCM  Aria vs native    │
│  NSX VLAN vs Overlay NFS vs VMFS        DRS aggression level  VCF vs manual         vROps vs Skyline  │
│  Single vs multi vDS vVols vs SPBM      Fault domains         Aria LCM vs manual    Log aggr. choice  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Networking Decisions

### vSS vs vDS — Standard vs Distributed Switch

**Context:** Every ESXi cluster needs a virtual switching layer. The choice between Standard Switch (vSS) and Distributed Switch (vDS) affects operational consistency, feature availability, and recovery scenarios.

| Factor | vSS | vDS |
|---|---|---|
| Configuration scope | Per-host; must configure each host individually | Cluster-wide; single policy applied to all hosts |
| NIOC (Network I/O Control) | No | Yes — required for vSAN / vMotion bandwidth guarantees |
| LACP (active/active bonding) | No | Yes |
| Port mirroring | No | Yes |
| Host Profiles integration | Basic | Full — vDS config captured in host profile |
| Cost | Included in all editions | Requires vSphere Enterprise Plus or VCF |
| Recovery risk | Host config independent; survives vCenter outage | Depends on vCenter for port-group changes; host maintains config after disconnect |

**Decision:** Use vDS for all production clusters. vSS is acceptable only for isolated test environments or single-host labs.

**Rationale:** NIOC is required for vSAN performance guarantees. Without vDS, vSAN traffic competes equally with VM traffic during peak periods. LACP bonding and port mirroring are standard enterprise requirements. The additional cost is justified for any multi-host cluster.

**Trade-off:** vDS port group changes require vCenter connectivity. If vCenter is unavailable during an emergency, vDS port group modifications cannot be made — plan emergency procedures accordingly.

---

### NSX Transport — VLAN vs Overlay (Geneve)

**Context:** NSX supports two segment types: VLAN-backed (no encapsulation, uses physical VLANs) and Overlay (Geneve encapsulation over IP, independent of physical topology). The choice determines whether workloads can move freely across physical sites and how the physical network must be configured.

| Factor | VLAN Segments | Overlay Segments (Geneve) |
|---|---|---|
| Physical dependency | Requires a VLAN per segment; VLANs provisioned on physical switches | IP fabric only; no VLAN per workload needed |
| Cross-host mobility | VM vMotion requires same VLAN available on both hosts | VM vMotion anywhere the TEP IP is reachable |
| MTU requirement | Standard 1500 MTU | MTU 9000 required on all TEP paths (physical + virtual) |
| DFW microsegmentation | Partial — East-West traffic still hits physical switch | Full — DFW inspects all traffic at the vNIC level |
| Physical switch config | New VLAN for each segment | Only two static VLANs needed: TEP + Edge uplink |

**Decision:** Use Overlay segments for all workload VMs. Reserve VLAN segments for edge uplinks and physical appliances that cannot support Geneve.

**Rationale:** Overlay segments decouple workload placement from physical topology, enabling full cross-host and cross-site vMotion without physical switch changes. DFW microsegmentation requires Overlay — VLAN segments bypass distributed firewall East-West inspection.

**Trade-off:** Overlay requires MTU 9000 end-to-end on all TEP paths. Confirm physical switch support and ToR configuration before deploying. MTU misconfiguration causes silent packet fragmentation that is hard to diagnose.

---

### Single vDS vs Multiple vDS per Cluster

**Context:** A cluster can use one vDS (all traffic types on one switch) or separate vDS instances per traffic type (management, vSAN, vMotion, VM traffic). 

| Factor | Single vDS | Multiple vDS |
|---|---|---|
| Operational simplicity | One switch to manage | Multiple switch objects; more consistent port-group naming |
| Isolation | NIOC + separate portgroups | Physical switch uplink separation possible |
| Recovery complexity | Single switch failure impacts all traffic | Isolated failure — one switch down does not affect others |
| Typical use | Most enterprise deployments | Environments with strict traffic separation compliance requirements |

**Decision:** Single vDS with NIOC traffic type policies is preferred for most environments. Multiple vDS only if compliance requires physical isolation of management vs VM traffic.

---

## Storage Decisions

### vSAN vs External SAN

**Context:** New cluster storage can be provided by vSAN (pooled from ESXi local disks) or an external SAN/NAS array. The right choice depends on budget, performance requirements, existing infrastructure, and operational preference.

| Factor | vSAN | External SAN |
|---|---|---|
| Infrastructure cost | No separate storage array required | Array, cables, HBAs, SAN switches required |
| Scalability | Add nodes to add compute and storage together | Storage scales independently of compute |
| HA model | Data distributed across hosts; N+1 hosts for FTT=1 | Dual-controller array with dedicated redundancy |
| Performance ceiling | Limited by local NVMe bandwidth per host | Array can be scaled independently; all-flash arrays offer higher peak IOPS |
| Operational model | Software-defined; managed from vCenter | Separate array management; additional admin overhead |
| Latency | Comparable to all-flash arrays (~0.3–1 ms) | Sub-ms for NVMe-oF; 0.5–2 ms for FC |
| Feature parity | Snapshots, replication (async/sync), encryption, dedup | Mature array features; deep replication options |
| VCF requirement | vSAN required for management domain | External SAN for VI workload domains supported |

**Decision:** vSAN for greenfield clusters where compute and storage scale together. External SAN where workloads have asymmetric compute/storage growth, or where existing array investments must be leveraged.

**Rationale:** vSAN eliminates separate infrastructure stacks and integrates fully with vCenter management. External SAN is preferred when storage and compute teams are separate, when sub-0.5 ms consistent latency is required (NVMe-oF), or when existing array contracts cover the workload.

---

### NFS vs VMFS for Shared Datastores

**Context:** When using an external NAS/SAN, shared datastores can be NFS (file) or VMFS (block). The choice affects features, performance characteristics, and operational complexity.

| Factor | NFS | VMFS |
|---|---|---|
| Transport | IP network | FC or iSCSI |
| VAAI offloads | Partial (VAAI-NAS: fast file clone, reserve space) | Full (VAAI-Block: hardware assisted locking, copy, zeroing) |
| Datastore management | Mount/unmount; no partitioning | LUN provisioning; VMFS formatting |
| Maximum datastore size | Limited by NFS export | 64 TB per VMFS volume |
| VM granularity | Per-VM VMDK files visible on filesystem | Block LUN; VMs not directly visible to storage admin |
| Snapshot offload | Depends on array (VAAI-NAS) | Full VAAI offload on compatible arrays |

**Decision:** VMFS over FC for performance-critical workloads and environments with existing SAN fabric. NFS for file shares, templates, ISO repositories, and secondary storage where IP connectivity is already in place.

---

## Compute and HA Decisions

### HA Admission Control Policy

**Context:** vSphere HA admission control reserves cluster capacity to guarantee VM restarts after a host failure. The three policies — Percentage, Slot-based, and Dedicated Failover Hosts — behave very differently at scale.

| Policy | How it works | Best for |
|---|---|---|
| Percentage-based | Reserve X% of cluster CPU and RAM for failover | Most clusters; straightforward to size |
| Slot-based | Each slot = largest VM CPU + RAM reservation; restricts power-on when slots < failover capacity | Uniform VM sizes only; over-reserves with mixed sizing |
| Dedicated failover hosts | Reserve specific hosts; no VMs run on them | Strict compliance environments; wastes capacity |

**Decision:** Use Percentage-based admission control set to one-host equivalent (e.g., 25% for a 4-node cluster). Review after every VM sizing change — percentage does not automatically account for VM reservation growth.

**Rationale:** Slot-based over-reserves in mixed environments because the slot size is always the largest VM's reservations. A single large VM with explicit CPU/RAM reservations makes slots enormous and prevents other VMs from powering on.

**Caution:** HA admission control is not a substitute for capacity planning — it only guarantees restart, not performance after failover.

---

### DRS Automation Level

| Level | Behaviour | When to use |
|---|---|---|
| Fully Automated | DRS moves VMs without asking | Production clusters with predictable workloads |
| Partially Automated | Initial placement automated; rebalance requires approval | Compliance environments needing change control for vMotion |
| Manual | Recommendations only | Never in production; only for initial testing |

**Decision:** Fully Automated for all production clusters. Migration threshold set to level 3 (balanced) by default; lower to 2 for conservative environments where unnecessary vMotion impacts workloads.

---

## Lifecycle Management Decisions

### Host Profile vs vLCM Image Management

**Context:** vSphere 7.0+ introduced vLCM cluster images as an alternative to host profiles for managing ESXi software. The two models are mutually exclusive per cluster for software management.

| Factor | Host Profiles | vLCM Cluster Image |
|---|---|---|
| Software management | Captures installed VIBs as part of profile | Defines desired image; auto-remediates non-compliant hosts |
| Firmware management | No | Yes (with hardware support plugin) |
| Configuration drift | Comprehensive config check | Software/firmware drift only; use host profile alongside for config |
| Rollback | No native rollback | Stateless ESXi supports image rollback |
| Best for | vSphere 6.x environments; config-only drift | vSphere 7+ with automated patching workflows |

**Decision:** vLCM cluster images for all new vSphere 7+ clusters. Host profiles for configuration settings (NTP, security, SNMP) run alongside vLCM for environments that still need configuration enforcement.

---

### VCF vs Manual Deployment

| Factor | VCF (SDDC Manager) | Manual vSphere + NSX |
|---|---|---|
| Bringup complexity | Automated; JSON-driven bringup workflow | Manual — each component separately |
| Upgrade | SDDC Manager orchestrates full stack upgrade | Manual coordination of version compatibility |
| Licensing | VCF license covers all components | Separate vSphere, NSX, vSAN licenses |
| Flexibility | SDDC Manager enforces specific versions; less flexibility | Full control of versions and configs |
| Operations | SDDC Manager checks drift and compliance | Manual auditing |
| Best for | Net-new SDDC deployments; VCF-licensed orgs | Existing environments; budget-constrained; non-standard configs |

**Decision:** VCF for all net-new SDDC deployments where the licensing is available. Manual for brownfield environments already running vSphere + NSX separately, or where VCF's version pinning conflicts with existing workload requirements.

---

## Monitoring Decisions

### Aria Operations vs Native vCenter Alarms

| Factor | Native vCenter Alarms | Aria Operations (vROps) |
|---|---|---|
| Scope | vSphere objects only | vSphere + NSX + vSAN + guest OS + physical hardware |
| Capacity trending | No | Yes — projected depletion dates, what-if scenarios |
| Root cause analysis | No | Workbench shows correlated events and anomalies |
| Alert noise | Low — specific trigger conditions | Higher without tuning; requires policy customisation |
| Cost | Included in vSphere | Requires Aria Operations licence |
| Setup complexity | Minutes | Hours to days (adapters, policies, dashboards) |

**Decision:** Native vCenter alarms for critical operational alerts (host disconnected, vSAN health, HA failure). Aria Operations for capacity planning, trend analysis, and root cause correlation in environments with the Aria licence.

**Rationale:** Native alarms require zero setup and cover the most common actionable events. Aria Operations adds value primarily in larger environments (100+ VMs) where manual capacity management is impractical and where the licence cost is justified.
