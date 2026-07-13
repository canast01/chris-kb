---
tags:
  - scenarios
  - vmware
  - vsan
  - vsphere-8
description: "A vSAN stretched cluster spans two sites with a witness appliance at a third location. Split-brain occurs when inter-site connectivity is lost and both..."
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

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_identify_the_failure_what_does_vce: "1. Identify the Failure — What Does vCenter Show?" {shape: rectangle}
2_check_witness_appliance_reachabili: "2. Check Witness Appliance Reachability" {shape: rectangle}
3_confirm_the_preferred_site_configu: "3. Confirm the Preferred Site Configuration" {shape: rectangle}
4_determine_current_quorum_state: "4. Determine Current Quorum State" {shape: rectangle}
5_check_intersite_vsan_network_path: "5. Check Inter-Site vSAN Network Path" {shape: rectangle}

products_involved -> 1_identify_the_failure_what_does_vce: uses
1_identify_the_failure_what_does_vce -> 2_check_witness_appliance_reachabili: uses
2_check_witness_appliance_reachabili -> 3_confirm_the_preferred_site_configu: uses
3_confirm_the_preferred_site_configu -> 4_determine_current_quorum_state: uses
4_determine_current_quorum_state -> 5_check_intersite_vsan_network_path: uses
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


```text title="Expected output"
PING 192.168.50.45 (192.168.50.45): 56 data bytes
64 bytes from 192.168.50.45: icmp_seq=0 time=45.234 ms
64 bytes from 192.168.50.45: icmp_seq=1 time=44.891 ms
64 bytes from 192.168.50.45: icmp_seq=2 time=45.567 ms
64 bytes from 192.168.50.45: icmp_seq=3 time=44.756 ms
64 bytes from 192.168.50.45: icmp_seq=4 time=45.123 ms

--- 192.168.50.45 statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 44.756/45.114/45.567 ms
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unable to find vmkernel interface vmk2` | Verify the correct vmkernel interface name with `esxcli network ip interface list` and substitute the correct interface (e.g., vmk1, vmk3). |
    | `No route to host` | Confirm the witness vSAN VMkernel IP is reachable from the source site's network and that firewall rules permit ICMP traffic on port 8084 (vSAN traffic). |
    | `Network is unreachable` | Check that the witness vSAN VMkernel interface is configured on the correct VLAN and that inter-site network connectivity is established. |
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


```text title="Expected output"
PING <site-b-vsan-vmk-ip> (192.168.50.42): 56 data bytes
64 bytes from 192.168.50.42: icmp_seq=0 ttl=64 time=2.341 ms
64 bytes from 192.168.50.42: icmp_seq=1 ttl=64 time=2.287 ms
64 bytes from 192.168.50.42: icmp_seq=2 ttl=64 time=2.305 ms
64 bytes from 192.168.50.42: icmp_seq=3 ttl=64 time=2.298 ms
--- 192.168.50.42 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 2.287/2.308/2.341 ms

Name    Port Group      IP Address      Netmask         Broadcast       Address Type
vmk0    Management      192.168.10.15   255.255.255.0   192.168.10.255  STATIC
vmk1    vMotion         192.168.20.15   255.255.255.0   192.168.20.255  STATIC
vmk2    vSAN            192.168.50.15   255.255.255.0   192.168.50.255  STATIC
vmk3    Fault Tolerance 192.168.30.15   255.255.255.0   192.168.30.255  STATIC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `PING <site-b-vsan-vmk-ip> (<site-b-vsan-vmk-ip>): sendto: No route to host` | Verify the vSAN network routing between sites is configured and the target IP is reachable; check firewall rules and VLAN configuration. |
    | `Error: Could not find interface vmk2` | Confirm vmk2 exists and is bound to the vSAN port group using `esxcli network ip interface list`. |
Look for: failed 8972-byte ping with successful small-packet ping = MTU mismatch on the inter-site link (vSAN requires MTU 9000).

```bash
# Check vSAN cluster membership — which hosts are in the cluster from this host's view
esxcli vsan cluster get

# Check inter-site communication partners
esxcli vsan debug vmdk list
```


```text title="Expected output"
Cluster UUID: 52d4a8f0-7c2e-4f1a-9b3e-2a1c5d8e9f4b
Cluster Dominance: 52d4a8f0-7c2e-4f1a-9b3e-2a1c5d8e9f4b
Node UUID: esx-prod-01.lab.local
Sub Cluster UUID: 52d4a8f0-7c2e-4f1a-9b3e-2a1c5d8e9f4b
Current Node State: MASTER
Node Health State: HEALTHY

VMDK                                          Owner                    Size      Policy
vm-prod-db-01_1-flat.vmdk                     esx-prod-01.lab.local    102400MB  raid1
vm-prod-web-02_1-flat.vmdk                    esx-prod-02.lab.local    51200MB   raid1
vm-prod-cache_1-flat.vmdk                     esx-prod-03.lab.local    204800MB  raid5
vm-dev-test_1-flat.vmdk                       esx-prod-01.lab.local    25600MB   raid1
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vSAN cluster is not enabled on this host` | Enable vSAN on the host via vCenter or run `esxcli vsan cluster new` to initialize the cluster. |
    | `Unable to contact vSAN cluster — no quorum` | Verify network connectivity between hosts and check that at least half of the cluster members are online and reachable. |
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


```text title="Expected output"
Cluster Master Election initiated.
Master Election in progress...
New Master elected: esx-site-b-01.corp.local (52:54:00:a1:2e:f3)
Cluster reconfiguration started
VSAN cluster is now operational with new master node
Cluster UUID: 522e2d12-a4f2-8f1a-c3e8-7b9a2f4d1e5c
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: VSAN cluster is not in a valid state for master election` | Verify all nodes in the cluster are in healthy state using `esxcli vsan cluster get` before forcing election. |
    | `Error: Cannot perform master election while both sites are active` | Confirm the remote site is completely powered down and unreachable before running this command to prevent split-brain scenarios. |
    | `Error: This command requires VSAN license and cluster mode enabled` | Ensure VSAN is properly licensed on all hosts and cluster mode is activated via vSphere Client before attempting forced election. |
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


```text title="Expected output"
Object UUID                          Resync Status
52a4c8f1-2b3e-4a9c-8d1f-7e6c5b4a3d2c  Resyncing (45%)
7f3d2c1b-9e8a-4f5c-6b7a-8d9e0f1c2b3a  Resyncing (12%)
9c8b7a6f-5e4d-3c2b-1a0f-9e8d7c6b5a4f  Resyncing (78%)
a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d  Resyncing (23%)

Resync Queue Summary:
Total Objects Resyncing: 4
Total Data to Resync: 847 GB
Estimated Time Remaining: 2h 34m
Network Throughput: 52 MB/s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `esxcli: command not found` | Ensure you are logged into an ESXi host directly via SSH; this command is not available on vCenter. |
    | `No matching processes were found` | The VSAN service may not be running; restart it with `systemctl restart vsanmgmt` or verify VSAN is enabled on the cluster. |
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

- [vSAN Disk or Component Failure](vsan-disk-component-failure.md) — A disk failure at one site during resync after a partition is a common compounding event.
- [Datastore Full / Capacity Alarm](datastore-full-capacity-alarm.md) — vSAN resync after a partition consumes additional capacity; a near-full cluster can hit the 80% write-stop threshold during resync.
- [NTP Drift / SSO Certificate Issues](ntp-drift-sso-certificate.md) — NTP drift between sites causes certificate validation failures that can disrupt vSAN unicast agent communication.
