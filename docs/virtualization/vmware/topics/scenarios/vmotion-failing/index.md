# vMotion Failing

<div class="kb-summary">
A vMotion or Storage vMotion operation fails before completing. This scenario maps the most common failure
modes — MTU mismatch, CPU incompatibility, VMkernel routing gaps, and NSX segment availability — and gives
the exact CLI commands and vCenter checks to isolate and fix each one.
</div>

```text
┌─────────────────────────────────────── vMotion Failing — Investigation Flow ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: vCenter Recent Tasks — vMotion task Failed; note the exact error message                  ││
│   └──────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                              │                                                        │
│        ┌───────────────────┬─────────────────┼───────────────────┬───────────────────┐                │
│        ▼                   ▼                 ▼                   ▼                   ▼                │
│  ┌───────────┐       ┌───────────┐     ┌───────────┐      ┌───────────┐       ┌───────────┐           │
│  │ "Incompat-│       │ "A general│     │ "Migration│      │ "The      │       │ "Timed    │           │
│  │ ible CPU" │       │ system    │     │ was       │      │ host is   │       │ out" —    │           │
│  │ or CPU    │       │ error"    │     │ canceled" │      │ not lic-  │       │ large VM  │           │
│  │ mismatch  │       │ — network │     │ — timeout │      │ ensed"    │       │ or low BW │           │
│  └─────┬─────┘       └─────┬─────┘     └─────┬─────┘      └─────┬─────┘       └─────┬─────┘           │
│        │                   │                 │                   │                   │                │
│        ▼                   ▼                 ▼                   ▼                   ▼                │
│  ┌───────────┐       ┌───────────┐     ┌───────────┐      ┌───────────┐       ┌───────────┐           │
│  │ Check EVC │       │ Test MTU  │     │ Check vmk │      │ vCenter → │       │ Check BW  │           │
│  │ mode on   │       │ vmkping   │     │ routing + │      │ Admin →   │       │ between   │           │
│  │ cluster   │       │ -d -s8972 │     │ firewall  │      │ Licences  │       │ hosts     │           │
│  └───────────┘       └───────────┘     └───────────┘      └───────────┘       └───────────┘           │
│                                              │                                                        │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  NSX segment check: segment available on destination host transport node?                         ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | vMotion initiation; EVC mode; licence validation; Recent Tasks |
| ESXi | VMkernel ports; MTU; NIC driver; vMotion routing |
| vSAN | Storage vMotion component relocation during cross-host migration |
| NSX | Segment availability on destination transport node; DFW follows the VM |

---

## 1. Read the Error Message First

Go to **vCenter → Recent Tasks**, find the failed vMotion and expand the error details. The error string is the fastest path to the root cause.

```text
Common vMotion error messages:
  "A general system error occurred"
      → Usually a network problem: MTU mismatch, firewall blocking port 8000/902, or
        no route between vmk1 addresses of source and destination.

  "The migration was canceled by the source host"
      → Timeout during memory copy. Common on VMs with > 32 GB RAM or with
        high memory write rate (database, in-memory cache). Check network bandwidth.

  "The virtual machine is incompatible with the destination host"
  "CPU instruction set incompatibility"
      → CPU feature mismatch. Check EVC mode.

  "The host is not licensed for vMotion"
      → Licence assignment issue. Check vCenter Administration → Licences.

  "No VMkernel adapter with the required tag was found"
      → VMkernel port on source or destination has no vMotion tag set.
```

---

## 2. EVC Mode Check (CPU Incompatibility Errors)

If the error references CPU compatibility, check the cluster's Enhanced vMotion Compatibility (EVC) setting.

Navigate to **Cluster → Configure → VMware EVC**.

```text
EVC modes (Intel, ascending):
  Merom, Penryn, Nehalem, Westmere, Sandy Bridge, Ivy Bridge,
  Haswell, Broadwell, Skylake, Cascade Lake, Ice Lake ...

A destination host must be at or above the cluster's EVC baseline.
If a new host generation was added without setting EVC, vMotion to
that host will fail for any running VM with CPU features exposed.
```

If EVC is disabled or the destination host is below the baseline:

1. Power off VMs on the new host
2. Set cluster EVC to a baseline supported by all hosts
3. Power VMs back on — they will resume with the masked CPU feature set

---

## 3. VMkernel MTU Check (Most Common Cause)

MTU mismatch between the vMotion VMkernel port and the physical switch is the most frequent cause of the generic "system error".

```bash
# On source host — identify vMotion VMkernel port
esxcli network ip interface tag list

# Output example:
# vmk0  Management
# vmk1  VMotion
# vmk2  vSAN

# Test path from vmk1 to destination host vmk1 with jumbo frame (no-fragment flag)
# -d = do not fragment; -s = payload size 8972 (8972 + 28 byte header = 9000 byte frame)
vmkping -I vmk1 -d -s 8972 <destination-vmk1-ip>

# If this fails but -s 1472 succeeds: MTU set to 1500 on switch or vSwitch
# Fix: set vSwitch MTU to 9000 on source AND destination AND physical switch port
```

```bash
# Verify current MTU on the VMkernel port
esxcli network ip interface list | grep -A5 vmk1

# Verify vSwitch MTU
esxcli network vswitch standard list | grep -E "Name|MTU"

# For VDS — check MTU from vCenter:
# vCenter → Networking → VDS → Configure → Properties → MTU
```

---

## 4. VMkernel Routing Check

The vMotion VMkernel must have a route to the destination host's vMotion VMkernel IP. If they are on different subnets, a gateway or static route is required.

```bash
# List all IPv4 routes on the host
esxcli network ip route ipv4 list

# If the destination vmk1 subnet has no route, add a static route:
esxcli network ip route ipv4 add -n <destination-subnet>/<prefix> -g <gateway-ip>

# Verify the VMkernel firewall allows vMotion traffic (port 8000)
esxcli network firewall ruleset list | grep -i vmotion
# Status should be "true" (enabled)
```

---

## 5. NIC and Driver Validation

```bash
# Check NIC driver, link speed, and duplex on the vMotion uplink
esxcli network nic get -n vmnic1

# Key fields:
#   Speed           — should be 10000 Mb/s or higher for vMotion
#   Duplex          — Full
#   Driver Version  — compare against VMware HCL if suspect

# Check for NIC errors on the vMotion uplink
esxcli network nic stats get -n vmnic1 | grep -E "Rx|Tx|Drop|Error"
```

---

## 6. NSX Segment Check (VM on NSX-T Overlay Network)

If the VM is connected to an NSX segment, the segment must be instantiated on the destination host's transport node. The DFW policy follows the VM automatically, but if the segment itself is not bound to the destination host, vMotion will fail.

```bash
# From NSX Manager UI: Networking → Segments → select the segment
# Check "Transport Nodes" tab — destination host must appear as bound

# From NSX Manager CLI or API — list transport nodes for a segment
# GET https://<nsx-manager>/api/v1/logical-switches/<ls-id>/transport-node-status

curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/logical-switches/<ls-id>/transport-node-status" \
  | python3 -m json.tool | grep -E "status|transport_node_id"
```

Also verify the destination host's NSX kernel modules are loaded:

```bash
# From destination ESXi host
esxcli software vib list | grep -i nsx

# Check TEP (tunnel endpoint) connectivity from destination host
esxcli network ip interface list | grep -i vmk
# vmk10 is typically the TEP VMkernel

vmkping -I vmk10 <remote-tep-ip> -d -s 1572
# 1572 = 1600 byte GENEVE frame minus headers
```

---

## 7. Large VM / Memory Bandwidth Timeout

If the VM has more than 32 GB of RAM and vMotion times out during the memory copy phase:

```text
vMotion memory copy phases:
  1. Pre-copy: pages copied while VM runs; dirty pages tracked
  2. Iterative copy: dirty pages re-copied; repeat until convergence
  3. Switchover: VM briefly stunned; final pages copied; VM resumes on destination

Timeout occurs when the VM writes memory faster than the network can copy it.
Requirement: vMotion network bandwidth > VM memory write rate.
```

Check available bandwidth on the vMotion VMkernel:

```bash
# Test actual throughput between hosts using iperf (if available)
# On destination host (as server):
iperf -s -B <destination-vmk1-ip> -p 5201

# On source host (as client):
iperf -c <destination-vmk1-ip> -B <source-vmk1-ip> -p 5201 -t 30
```

If bandwidth is insufficient, dedicate a higher-speed uplink to the vMotion VMkernel or increase the number of vMotion streams in **Cluster → Configure → vSphere DRS → Advanced Options**.

---

## Common Mistakes

- **Testing ping to the management IP instead of the vmk1 IP.** Management (vmk0) and vMotion (vmk1) are on different VMkernel ports and may have different routes. Always test to the vmk1 address specifically.
- **Fixing MTU on vSwitch but not on the physical switch.** MTU must match end-to-end: vSwitch → distributed switch → physical switch port → ToR switch. One mismatched hop breaks jumbo frames.
- **Not checking EVC mode first when mixing host hardware generations.** A new host added to a cluster without EVC configured will silently block vMotion for all VMs that have been powered on since a CPU-feature-exposing operation.
- **Overlooking NSX transport node binding.** On NSX-T overlay networks, the destination host must be a transport node with the segment bound to it. This is easy to miss when adding new hosts to a cluster.

---

## Related Scenarios

- [VM Performance Degraded](../vm-performance-degraded/index.md) — DRS triggers vMotion to rebalance load; understanding when vMotion fails under load is connected to performance investigations.
- [VM Inaccessible / HA Failover](../vm-inaccessible-ha-failover/index.md) — HA-initiated restarts and DRS rebalancing after failover both rely on vMotion working correctly.
- [NSX Connectivity Broken](../nsx-connectivity-broken/index.md) — NSX TEP or segment issues that cause vMotion failures overlap with the broader NSX connectivity troubleshooting flow.
