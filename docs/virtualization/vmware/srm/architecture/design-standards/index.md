# SRM — Design Standards


<div class="kb-summary">
Design Standards reference covering Test Network Design, IP Customization Strategy, Recovery Plan Structure Best Practices, RPO Targets and SRA Capability, Test Frequency Recommendations and 1 more sections.
</div>

```text
  Replication Topology + Recovery Plan Structure
┌──────────────────────────────────────────────────────────────┐
│  Protected Site               Recovery Site                  │
│  ┌────────────┐               ┌────────────┐                 │
│  │ VMs on     │──VR/SRA──────►│ Replica    │                 │
│  │ replicated │  (RPO target) │ VMDKs      │                 │
│  │ datastore  │               └────────────┘                 │
│  └────────────┘                                              │
│                                                              │
│  Recovery Plan (priority groups):                            │
│  ┌───────────────────────────────────────────────────────┐   │
│  │  Priority 1: DCs / DNS / DHCP  ──► power on first    │    │
│  │  Priority 2: Database servers  ──► wait for P1 done  │    │
│  │  Priority 3: App servers       ──► wait for P2 done  │    │
│  │  Priority 4: Web / LB          ──► wait for P3 done  │    │
│  │  Priority 5: Non-critical      ──► last              │    │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  Network Mapping: Protected VLAN ──► Recovery VLAN / Test    │
└──────────────────────────────────────────────────────────────┘
```
┌──────────────────────────────────── VMware SRM — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│  SRM design standards define RPO tiers, protection group structure, test frequency,                   │
│  recovery plan priority, and site-pair capacity requirements.                                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              RPO Tier Standards              │  │           Protection Group Design           │   │
│   │          Tier 1: ≤15min (ABR/sync)           │  │          Group by application tier          │   │
│   │           Tier 2: ≤1h (vSR async)            │  │              One plan per group             │   │
│   │           Tier 3: ≤4h (vSR async)            │  │           Startup order: DB first           │   │
│   │          Tier 4: 24h (non-critical)          │  │          Dependencies: script wait          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  RPO tier drives replication technology choice; group VMs by app dependency.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Recovery Site Standards            │  │                Test Standards               │   │
│   │          Capacity: 100% Tier 1 VMs           │  │           Test: at least quarterly          │   │
│   │          Standby: Tier 2–4 (burst)           │  │            Document RTO achieved            │   │
│   │              N+1 hosts minimum               │  │           Cleanup: auto after test          │   │
│   │             Same vSAN disk count             │  │          Evidence: screenshot plan          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Recovery site needs compute and storage for Tier 1 VMs always on standby;                            │
│  WAN bandwidth must sustain replication traffic for all tiers.                                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO           = Recovery Point Objective; acceptable data loss window                                │
│  RTO           = Recovery Time Objective; time to restore service                                     │
│  Tier 1        = most critical; <15min RPO; ABR or vSR 5min                                           │
│  Protection group= set of VMs with same replication and recovery plan                                 │
│  Startup order = SRM powers on VMs in sequence; DB before app                                         │
│  Script wait   = custom step; waits for service health before next VM                                 │
│  Burst capacity= recovery site scales up on failover from off state                                   │
│  N+1 hosts     = recovery site has one host spare for HA during DR                                    │
│  Quarterly test= regulatory minimum for most DR frameworks                                            │
│  Evidence      = screenshot + log of test outcome for audit                                           │
│  Cleanup       = SRM removes test VMs and snapshots after test                                        │
│  WAN BW        = replication bandwidth; plan for peak replication rate                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
VMs retain their IPs. Routing updates (BGP, static routes) redirect traffic to recovery site.

**Option B: Different VLAN IDs, same IP subnets** — Recovery site uses different physical VLANs but same IP subnets (extended L3 or re-advertising the subnets):
```text
Protected: dvPG-App-VLAN100 (10.10.0.0/24)  →  Recovery: dvPG-App-VLAN500 (10.10.0.0/24)
```
No IP customization needed. Requires routing coordination.

**Option C: Different subnets with IP re-addressing** — Recovery site uses entirely different IP ranges:
```text
Protected: 10.10.0.0/24  →  Recovery: 10.20.0.0/24
```
Requires SRM IP customization rules (subnet-level mapping). DNS updates required at recovery.

## Test Network Design

For test failovers, create isolated port groups with no uplink assignment:

```text
dvPG-SRM-Test-App     (no uplink — isolated bubble)
dvPG-SRM-Test-DB      (no uplink — isolated bubble)
```

Map protected-site production port groups → isolated test port groups in SRM's test network mapping (separate from the production failover mapping). This prevents test VMs from reaching production systems.

---

## IP Customization Strategy

### When to Use Subnet-Level Mapping

Best for large environments where subnets map cleanly between sites:

```text
Source subnet: 10.10.0.0/24  →  Target subnet: 10.20.0.0/24
```

All VMs with static IPs in `10.10.0.x` will be re-addressed to `10.20.0.x` (same host portion). Configure in SRM UI: Recovery Plan → IP Customization → **Subnet Mappings**.

### When to Use Per-VM Customization

Use when:
- Target IPs don't follow a simple subnet pattern.
- Only specific VMs need re-addressing.
- Different NICs on the same VM go to different subnets.

Per-VM customization is more granular but doesn't scale well beyond ~50 VMs per plan.

### DHCP at Recovery Site

Use DHCP at recovery site when:
- Recovery site is pre-configured with DHCP scopes matching recovery IP ranges.
- VMs are already configured for DHCP (common for application VMs).
- Simplifies Recovery Plan maintenance.

Avoid DHCP for:
- Database servers (need stable IPs for connection strings).
- Servers referenced in DNS with static A records.
- VMs in IP customization dependency chains.

### IP Customization and DNS

SRM does not update DNS. After failover with IP re-addressing:

1. Configure pre/post-power-on scripts in the Recovery Plan to run DNS update commands.
2. Use low TTL values on production DNS A records (TTL ≤ 300 seconds) to speed propagation.
3. Alternatively, maintain a secondary DNS zone at recovery site that is promoted after failover.

---

## Recovery Plan Structure Best Practices

### Priority Group Design

SRM supports 5 priority groups. Recommended allocation:

| Priority | VM Category | Examples |
|---|---|---|
| 1 | Core infrastructure | Domain controllers, DNS servers, DHCP, NTP |
| 2 | Data tier | Database servers, message queues |
| 3 | Application tier | Application servers, middleware |
| 4 | Presentation tier | Web servers, load balancers |
| 5 | Non-critical / batch | Reporting, batch jobs, dev/test |

- All Priority 1 VMs power on and reach post-power-on step success before Priority 2 starts.
- Within a priority group, VMs start concurrently.
- Add a **Wait for VM tools heartbeat** post-power-on step for infrastructure VMs to enforce sequencing more granularly.

### Recovery Plan Size Limits

| Resource | Recommended Limit |
|---|---|
| VMs per Recovery Plan | ≤ 400 |
| Protection Groups per Recovery Plan | ≤ 20 |
| Concurrent Recovery Plans | 1 per site pair (serialized) |
| Priority groups | 5 (fixed) |
| Custom steps per VM | No hard limit — keep to ≤ 5 per VM |

### Recovery Plan Dependencies

If application A depends on DR site services that are in a separate Recovery Plan:

1. Use **Recovery Plan dependencies** (SRM UI → Recovery Plan → Properties → Dependencies).
2. Plan B will not start until Plan A completes successfully.
3. Use this for layered DR strategies (infra plan → workload plan).

### Multiple Recovery Plans

Organize plans by:
- **Tier** — infrastructure plan + workload plan (dependency chain)
- **Business unit** — separate plans per BU for independent failover
- **Criticality** — mission-critical plan (RTO < 1 hr) vs. standard plan (RTO < 4 hr)

Do not put all VMs in a single monolithic Recovery Plan — this increases blast radius for misconfiguration and makes testing harder.

---

## RPO Targets and SRA Capability

| Replication Method | Minimum RPO | Typical RPO | Notes |
|---|---|---|---|
| Synchronous ABR | 0 (no data loss) | 0 | Requires low-latency WAN (< 5ms RTT); impacts write performance |
| Asynchronous ABR | Array-dependent | 15–30 min | Most common; RPO depends on WAN bandwidth vs change rate |
| vSphere Replication | 5 minutes | 15–30 min | Practical lower bound depends on change rate and bandwidth |
| vSphere Replication (high change) | 5 minutes | May lag | High-churn VMs (databases) may not achieve 5-min RPO without sufficient bandwidth |

### Bandwidth Estimation for VR

```text
Required bandwidth (Mbps) = (Daily change rate GB × 8192) / (86400 × efficiency factor)
Efficiency factor: 0.7 (compression enabled), 0.5 (no compression)

Example:
VM daily change rate = 50 GB
With compression: (50 × 8192) / (86400 × 0.7) = 6.8 Mbps
```

---

## Test Frequency Recommendations

| Activity | Recommended Frequency |
|---|---|
| Full Recovery Plan test (all VMs) | Quarterly minimum; semi-annually acceptable for stable environments |
| Partial test (critical VMs only) | Monthly |
| Protection Group health review | Weekly (automated script or SRM dashboard) |
| RPO compliance check | Daily (automated alert) |
| Network mapping validation | Each time infrastructure changes at either site |
| SRA connectivity check | Weekly |
| SRM license validity check | Monthly |

Regular testing is the only way to confirm recovery plans actually work. Document test results and resolve any failures before the next scheduled test.

---

## SRM Design Checklist

### Pre-Implementation

- [ ] vCenter versions at both sites are SRM-compatible (same major version required).
- [ ] SRM version is compatible with vCenter version (check VMware Compatibility Guide).
- [ ] Network connectivity between sites meets port requirements.
- [ ] Recovery site has sufficient compute, memory, and storage for all protected VMs.
- [ ] Storage replication is configured and healthy at array level before SRM installation.
- [ ] VR Appliances sized for VM count and change rate.
- [ ] Recovery site network (VLANs / NSX segments) mirrors protected site topology.
- [ ] IP customization strategy decided (subnet mapping / per-VM / DHCP).
- [ ] DNS strategy for IP re-addressing defined.
- [ ] SRM service account created with minimum required privileges.

### Post-Implementation

- [ ] All Protection Groups show status **OK**.
- [ ] All protected VMs have placeholder VMs at recovery site.
- [ ] Network mappings configured for all port groups used by protected VMs.
- [ ] Folder and resource mappings configured.
- [ ] Test failover completed for all Recovery Plans.
- [ ] Test cleanup completed successfully.
- [ ] Test failover results documented.
- [ ] RPO compliance monitored and all VMs within target RPO.
