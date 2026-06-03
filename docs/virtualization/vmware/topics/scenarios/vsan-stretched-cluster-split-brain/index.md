# vSAN Stretched Cluster Split-Brain

<div class="kb-summary">
A vSAN stretched cluster spans two sites with a witness appliance at a third location. Split-brain
occurs when inter-site connectivity is lost and both sites believe they are the primary — each side
cannot see the other. The witness appliance decides which site retains quorum. This scenario covers
identifying the failure, understanding the quorum decision, and safely recovering after connectivity
is restored.
</div>

```text
┌────────────────────────── vSAN Stretched Cluster Split-Brain — Investigation Flow ─────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: vCenter shows hosts at one site disconnected OR vSAN health shows cluster partition          ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                        ┌───────────────────────┼───────────────────────┐                              │
│                        ▼                       ▼                       ▼                              │
│   ┌─────────────────────────────┐  ┌─────────────────────────┐  ┌────────────────────────────┐        │
│   │  Witness reachable from     │  │  Witness unreachable     │  │  Both sites reachable but  │       │
│   │  one site only              │  │  from both sites         │  │  vSAN partition detected   │       │
│   │  → quorum on reachable site │  │  → full isolation event  │  │  → unicast agent issue     │       │
│   └──────────────┬──────────────┘  └────────────┬────────────┘  └────────────────────────────┘        │
│                  │                               │                                                    │
│                  ▼                               ▼                                                    │
│   ┌─────────────────────────────┐  ┌─────────────────────────────────────────────────────────────────┐│
│   │  Preferred site retains     │  │  All VMs stopped — manual intervention required                 ││
│   │  quorum; secondary site     │  │  Contact GSS before forced quorum election                      ││
│   │  VMs stopped by HA          │  └─────────────────────────────────────────────────────────────────┘│
│   └──────────────┬──────────────┘                                                                     │
│                  ▼                                                                                    │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  After connectivity restored: monitor resync queue — do NOT perform maintenance until complete      ││
│   └─────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vSAN | Stretched cluster configuration, witness appliance, quorum calculation, resync |
| vCenter | Cluster and host state visibility; fault domain and preferred site configuration |
| ESXi | Hosts at each site; vSAN VMkernel (vmk2) inter-site traffic |
| NSX | Inter-site overlay segments; if NSX segments are stretched, connectivity also depends on NSX |

---

## 1. Identify the Failure — What Does vCenter Show?

Check these two indicators first:

- **vCenter host list**: are hosts at one or both sites showing **Disconnected** or
  **Not Responding**?
- **vSAN Skyline Health**: vCenter → Cluster → **Monitor** → **vSAN** → **Skyline Health** →
  look for **"vSAN cluster partition detected"** or **"Stretched cluster health"** failures.

If hosts are disconnected and vSAN health shows a partition, inter-site connectivity is down.
If hosts appear connected but vSAN health shows a partition, the vSAN VMkernel network has an
issue independent of the management network.

---

## 2. Check Witness Appliance Reachability

The witness appliance is the tiebreaker. It holds a vote that determines which site retains
quorum when inter-site communication is lost.

In vCenter: locate the **witness host** object (it appears as a host, not a VM). Is it:
- **Connected** — the witness is reachable and voting
- **Disconnected** — the witness is unreachable; quorum decision depends on preferred site config

The witness votes for the site it can still reach. If the witness can reach Site A but not Site B:
Site A keeps quorum and VMs continue running. Site B VMs are stopped by vSphere HA.

```bash
# From Site A ESXi host — ping witness vSAN VMkernel IP
vmkping -I vmk2 <witness-vsan-vmk-ip>

# From Site B ESXi host — same test
vmkping -I vmk2 <witness-vsan-vmk-ip>
```

---

## 3. Confirm the Preferred Site Configuration

The preferred site is the tiebreaker when the witness vote does not resolve the partition. In a
50/50 network split where the witness is also unreachable, the preferred site keeps quorum.

vCenter → Cluster → **Configure** → **vSAN** → **Fault Domains**.

The fault domain labelled **Preferred** is the site that retains quorum when no witness vote is
available. Confirm this is documented and matches your DR runbook.

---

## 4. Determine Current Quorum State

Use the quorum decision table to understand what the cluster should be doing right now:

| Site A reachable | Site B reachable | Witness reachable | Expected outcome |
|---|---|---|---|
| Yes | No | Yes | Site A runs; Site B VMs stopped by HA |
| No | Yes | Yes | Site B runs if preferred, or witness votes for B |
| Yes | No | No | Site A runs only if configured as preferred site |
| No | No | Yes | Neither site has quorum — all VMs stopped |
| Yes | Yes | No | Both sites run — split-brain risk; monitor closely |

If the actual behaviour does not match this table, there is a configuration error in the fault
domain or preferred site settings.

---

## 5. Check Inter-Site vSAN Network Path

vSAN inter-site replication traffic uses the vSAN VMkernel interface (tagged vmk2 or equivalent
in your environment). Test reachability and MTU:

```bash
# From a Site A ESXi host — ping a Site B host's vSAN vmk IP
# -d: do not fragment; -s 8972: full-size vSAN packet (8972 bytes payload)
vmkping -I vmk2 <site-b-vsan-vmk-ip> -d -s 8972

# Check the vSAN VMkernel interface is active and has the correct IP
esxcli network ip interface ipv4 get
```

A failed large-packet ping (8972 bytes) with a successful small-packet ping indicates an MTU
mismatch on the inter-site link. vSAN requires MTU 9000 on the inter-site network.

```bash
# Check vSAN cluster membership — which hosts are in the cluster from this host's view
esxcli vsan cluster get

# Check inter-site communication partners
esxcli vsan debug vmdk list
```

---

## 6. Forced Recovery — Full Isolation (Last Resort)

If ALL inter-site and witness connectivity is lost simultaneously, no site has quorum and all
VMs across both sites stop. This is a full datacenter isolation scenario.

**Contact VMware/Dell GSS before proceeding with forced quorum.** Forcing quorum incorrectly
when both sites are actually running creates data divergence that requires manual reconciliation.

```bash
# LAST RESORT ONLY — force master election on the surviving site
# Only run this if you have confirmed the other site is fully powered off
# and there is zero risk of both sites writing simultaneously
esxcli vsan cluster forcemasterelection
```

After forced election, VMs on the surviving site can be started. The secondary site must be
treated as potentially diverged and should not be started until vSAN resync completes after
connectivity is restored.

---

## 7. After Connectivity Restores — Monitor Resync

When inter-site network connectivity comes back, vSAN automatically begins resyncing objects
between sites. This process can take minutes to hours depending on how many objects changed
during the partition.

Monitor resync progress: vCenter → **vSAN** → **Monitor** → **Resyncing Objects**.

```bash
# Check resync queue from ESXi host
esxcli vsan debug object list | grep -i resync

# Get object resync status
esxcli vsan debug resync list
```

**Do not perform host maintenance, storage policy changes, or vSAN upgrades until resync
completes.** Resyncing adds I/O overhead. Any additional disruption during resync risks
further object degradation.

---

## 8. Post-Incident — Stretched Cluster Health Check

After full recovery, run a complete vSAN stretched cluster health validation:

vCenter → **vSAN** → **Skyline Health** → **All Checks** → filter for the
**Stretched cluster** category.

Key checks to verify:

| Health check | What it validates |
|---|---|
| Stretched cluster health | Overall partition and witness connectivity status |
| Unicast agent configuration | vSAN agent IPs configured correctly on all hosts |
| Preferred fault domain | Preferred site is set and matches your DR documentation |
| Witness host connectivity | Witness can reach both sites' vSAN VMkernel IPs |

---

## Common Mistakes

- **Manually starting VMs on the secondary site during split-brain.** If both sites are writing
  to the same vSAN objects simultaneously, the data diverges. This is unrecoverable without a
  restore from backup.
- **Not monitoring resync after connectivity restores.** Resync is automatic but must complete
  before the cluster is considered healthy. Skipping this check and performing maintenance
  immediately after recovery frequently causes a second disruption.
- **Placing the witness on the same network as one of the sites.** If Site A's network fails and
  the witness is on Site A's subnet, the witness goes unreachable at the same time — eliminating
  the tiebreaker. The witness must be on a truly independent network path.

---

## Related Scenarios

- [vSAN Disk or Component Failure](../vsan-disk-component-failure/index.md) — A disk failure at one site during resync after a partition is a common compounding event.
- [Datastore Full / Capacity Alarm](../datastore-full-capacity-alarm/index.md) — vSAN resync after a partition consumes additional capacity; a near-full cluster can hit the 80% write-stop threshold during resync.
- [NTP Drift / SSO Certificate Issues](../ntp-drift-sso-certificate/index.md) — NTP drift between sites causes certificate validation failures that can disrupt vSAN unicast agent communication.
