---
tags:
  - scenarios
  - vmware
  - vsan
  - vsphere-8
---
# vSAN Stretched Cluster Split-Brain

<div class="kb-summary">
A vSAN stretched cluster spans two sites with a witness appliance at a third location. Split-brain
occurs when inter-site connectivity is lost and both sites believe they are the primary — each side
cannot see the other. The witness appliance decides which site retains quorum. This scenario covers
identifying the failure, understanding the quorum decision, and safely recovering after connectivity
is restored.

*Applies to: vSphere 7.x / 8.x*
</div>

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vSAN | Stretched cluster configuration, witness appliance, quorum calculation, resync |
| vCenter | Cluster and host state visibility; fault domain and preferred site configuration |
| ESXi | Hosts at each site; vSAN VMkernel (vmk2) inter-site traffic |
| NSX | Inter-site overlay segments; if NSX segments are stretched, connectivity also depends on NSX |

---

## 1. Identify the Failure — What Does vCenter Show?

Check two indicators first: vCenter host list for **Disconnected/Not Responding** hosts, and vCenter → Cluster → **Monitor** → **vSAN** → **Skyline Health** for partition alerts.

Look for: hosts disconnected + vSAN partition = inter-site link down; hosts connected + vSAN partition = vSAN VMkernel network issue independent of management.

---

## 2. Check Witness Appliance Reachability

The witness appliance holds the tiebreaker vote — it determines which site retains quorum when inter-site communication is lost.

In vCenter, locate the **witness host** object and check its state: **Connected** = voting; **Disconnected** = quorum falls back to preferred site config.

Look for: which site the witness can still reach — that site keeps quorum and its VMs keep running; the other site's VMs are stopped by vSphere HA.

```bash
# From Site A ESXi host — ping witness vSAN VMkernel IP
vmkping -I vmk2 <witness-vsan-vmk-ip>

# From Site B ESXi host — same test
vmkping -I vmk2 <witness-vsan-vmk-ip>
```

---

## 3. Confirm the Preferred Site Configuration

The preferred site retains quorum when the witness is also unreachable and neither site can reach the other.

Check: vCenter → Cluster → **Configure** → **vSAN** → **Fault Domains** — the fault domain labelled **Preferred** must match your DR runbook.

---

## 4. Determine Current Quorum State

Use the table to determine expected cluster behaviour and compare with what vCenter is showing:

| Site A reachable | Site B reachable | Witness reachable | Expected outcome |
|---|---|---|---|
| Yes | No | Yes | Site A runs; Site B VMs stopped by HA |
| No | Yes | Yes | Site B runs if preferred, or witness votes for B |
| Yes | No | No | Site A runs only if configured as preferred site |
| No | No | Yes | Neither site has quorum — all VMs stopped |
| Yes | Yes | No | Both sites run — split-brain risk; monitor closely |

Look for: actual behaviour that does not match the table — indicates a configuration error in the fault domain or preferred site settings.

---

## 5. Check Inter-Site vSAN Network Path

Test reachability and MTU on the vSAN VMkernel interface (tagged vmk2 or equivalent) used for inter-site replication traffic:

```bash
# From a Site A ESXi host — ping a Site B host's vSAN vmk IP
# -d: do not fragment; -s 8972: full-size vSAN packet (8972 bytes payload)
vmkping -I vmk2 <site-b-vsan-vmk-ip> -d -s 8972

# Check the vSAN VMkernel interface is active and has the correct IP
esxcli network ip interface ipv4 get
```

Look for: failed 8972-byte ping with successful small-packet ping = MTU mismatch on the inter-site link (vSAN requires MTU 9000).

```bash
# Check vSAN cluster membership — which hosts are in the cluster from this host's view
esxcli vsan cluster get

# Check inter-site communication partners
esxcli vsan debug vmdk list
```

---

## 6. Forced Recovery — Full Isolation (Last Resort)

Use only when all inter-site and witness connectivity is confirmed lost and all VMs have stopped — contact VMware/Dell GSS before proceeding.

**Forcing quorum incorrectly when both sites are still running creates data divergence requiring manual reconciliation.**

```bash
# LAST RESORT ONLY — force master election on the surviving site
# Only run this if you have confirmed the other site is fully powered off
# and there is zero risk of both sites writing simultaneously
esxcli vsan cluster forcemasterelection
```

After forced election, start VMs on the surviving site only; treat the secondary site as potentially diverged and do not start it until vSAN resync completes after connectivity is restored.

---

## 7. After Connectivity Restores — Monitor Resync

When inter-site connectivity comes back, vSAN automatically resyncs objects — this can take minutes to hours depending on change volume during the partition.

Monitor: vCenter → **vSAN** → **Monitor** → **Resyncing Objects**.

```bash
# Check resync queue from ESXi host
esxcli vsan debug object list | grep -i resync

# Get object resync status
esxcli vsan debug resync list
```

**Do not perform host maintenance, storage policy changes, or vSAN upgrades until resync completes** — resync adds I/O overhead, and any disruption risks further object degradation.

---

## 8. Post-Incident — Stretched Cluster Health Check

After full recovery, run a complete vSAN Skyline Health validation: vCenter → **vSAN** → **Skyline Health** → **All Checks** → filter for the **Stretched cluster** category.

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

## Key Terms

| Term | Definition |
|---|---|
| Stretched cluster | A vSAN cluster whose hosts are distributed across two physical sites (fault domains), providing cross-site HA and data mirroring between locations |
| Witness appliance | A lightweight VM deployed at a third site that holds one vote per vSAN object; acts as tiebreaker when the two data sites cannot reach each other |
| Preferred site | The fault domain configured to retain quorum when the witness is also unreachable; if both sites are isolated from the witness, the preferred site keeps running |
| Fault domain | A logical grouping in vSAN that maps to a physical failure boundary — in a stretched cluster, each site is a separate fault domain |
| Split-brain | The condition where both sites believe they have quorum and attempt to write to the same vSAN objects simultaneously; the witness prevents this under normal conditions |
| Quorum | The minimum number of votes required for a vSAN object to accept write I/O; requires more than half of the total votes (data components + witness component) |
| vSAN resync | The process by which vSAN re-mirrors object components that fell out of sync during a partition; runs automatically after connectivity restores |
| Inter-site link | The dedicated WAN or dark-fibre connection between the two stretched cluster sites; carries vSAN replication traffic, management, and overlay data |
| GENEVE | The overlay encapsulation protocol used by NSX for inter-site stretched segments; loss of the inter-site link disrupts both vSAN and NSX overlay traffic simultaneously |
| Site partition | The network isolation event that splits the two fault domains; vSAN detects this as a cluster partition and invokes the quorum/witness decision |
| forcemasterelection | An ESXi CLI command (`esxcli vsan cluster forcemasterelection`) used as a last resort to force a vSAN master election on the surviving site when normal quorum is impossible |
| vSAN Skyline Health | The built-in health check framework for vSAN accessible via vCenter; includes stretched-cluster-specific checks for partition state, witness connectivity, and unicast agent config |

---

## Related Scenarios

- [vSAN Disk or Component Failure](vsan-disk-component-failure/index.md) — A disk failure at one site during resync after a partition is a common compounding event.
- [Datastore Full / Capacity Alarm](datastore-full-capacity-alarm/index.md) — vSAN resync after a partition consumes additional capacity; a near-full cluster can hit the 80% write-stop threshold during resync.
- [NTP Drift / SSO Certificate Issues](ntp-drift-sso-certificate/index.md) — NTP drift between sites causes certificate validation failures that can disrupt vSAN unicast agent communication.
