# SRM — Design Standards

## SRM Server Sizing

### SRM Appliance (8.x+)

VMware ships SRM as an OVA appliance from version 8.x. Sizing is based on the number of protected VMs.

| Deployment Size | Protected VMs | vCPU | RAM | Disk |
|---|---|---|---|---|
| Tiny | ≤ 100 | 2 | 8 GB | 40 GB |
| Small | ≤ 250 | 4 | 12 GB | 40 GB |
| Medium | ≤ 500 | 8 | 16 GB | 40 GB |
| Large | ≤ 1000 | 16 | 32 GB | 40 GB |

Notes:
- These values are per SRM appliance (one per site).
- VM count refers to protected VMs, not total VMs in the vCenter.
- If running concurrent Recovery Plan tests or executions, scale up by one tier.
- SRM appliance root disk is thin-provisioned; ensure datastore has headroom for logs.

### SRM Server (Windows, pre-8.x)

| Protected VMs | vCPU | RAM |
|---|---|---|
| ≤ 100 | 2 | 4 GB |
| 100–500 | 4 | 8 GB |
| 500–1000 | 8 | 16 GB |

---

## Network Requirements

### SRM Site-to-Site Ports

All communication between SRM Servers at the two sites traverses the WAN link. Ensure firewall rules permit:

| Source | Destination | Port | Protocol | Purpose |
|---|---|---|---|---|
| SRM Server (protected) | SRM Server (recovery) | 443 | TCP | SRM site pairing HTTPS API |
| SRM Server (recovery) | SRM Server (protected) | 443 | TCP | Bi-directional site pairing |
| SRM Server (protected) | SRM Server (recovery) | 9086 | TCP | SRM legacy pairing (pre-8.x) |
| vCenter (protected) | vCenter (recovery) | 443 | TCP | Cross-vCenter VM operations |
| ESXi hosts (protected) | VR Appliance (recovery) | 44046 | TCP | vSphere Replication data |
| VR Appliance (protected) | VR Appliance (recovery) | 10000, 10001 | TCP | VR management channel |
| SRM Server | Storage array management | 443 | TCP | SRA to array API |

### SRM Local Site Ports

| Source | Destination | Port | Protocol | Purpose |
|---|---|---|---|---|
| SRM Server | vCenter Server | 443 | TCP | SRM ↔ vCenter API |
| vSphere Client browser | SRM Server | 443 | TCP | UI access |
| SRM Server | ESXi hosts | 443, 902 | TCP | VM power operations |
| SRM Server | VR Appliance | 8043 | TCP | SRM ↔ VR integration |

---

## vSphere Replication Appliance Sizing

VR Appliance sizing depends on both VM count and aggregate daily change rate.

| Deployment Size | Protected VMs | Daily Change Rate | vCPU | RAM |
|---|---|---|---|---|
| Small | ≤ 100 | Low (< 100 GB/day) | 4 | 8 GB |
| Medium | ≤ 500 | Medium (100–500 GB/day) | 8 | 16 GB |
| Large | ≤ 2000 | High (> 500 GB/day) | 16 | 32 GB |

Guidelines:
- Deploy one VR Appliance per site minimum. Scale out with additional VR Appliances for high VM counts.
- VR Appliances can be load-balanced for replication sessions — configure in VAMI → Configuration → Servers.
- Low RPO (5–15 min) on many VMs increases change rate impact significantly — account for this in sizing.

---

## Recovery Site Network Design

### Shadow Port Groups

For every production VLAN at the protected site, create a corresponding port group at the recovery site. Common patterns:

**Option A: Same VLAN IDs** — If WAN connectivity is re-routed and the recovery site switches can accommodate the same VLAN IDs:
```
Protected: dvPG-App-VLAN100  →  Recovery: dvPG-App-VLAN100
Protected: dvPG-DB-VLAN200   →  Recovery: dvPG-DB-VLAN200
```
VMs retain their IPs. Routing updates (BGP, static routes) redirect traffic to recovery site.

**Option B: Different VLAN IDs, same IP subnets** — Recovery site uses different physical VLANs but same IP subnets (extended L3 or re-advertising the subnets):
```
Protected: dvPG-App-VLAN100 (10.10.0.0/24)  →  Recovery: dvPG-App-VLAN500 (10.10.0.0/24)
```
No IP customization needed. Requires routing coordination.

**Option C: Different subnets with IP re-addressing** — Recovery site uses entirely different IP ranges:
```
Protected: 10.10.0.0/24  →  Recovery: 10.20.0.0/24
```
Requires SRM IP customization rules (subnet-level mapping). DNS updates required at recovery.

### Test Network Design

For test failovers, create isolated port groups with no uplink assignment:

```
dvPG-SRM-Test-App     (no uplink — isolated bubble)
dvPG-SRM-Test-DB      (no uplink — isolated bubble)
```

Map protected-site production port groups → isolated test port groups in SRM's test network mapping (separate from the production failover mapping). This prevents test VMs from reaching production systems.

---

## IP Customization Strategy

### When to Use Subnet-Level Mapping

Best for large environments where subnets map cleanly between sites:

```
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

```
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
