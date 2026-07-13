---
tags:
  - scenarios
  - vmware
description: "A vMotion or Storage vMotion operation fails before completing. This scenario maps the most common failure modes — MTU mismatch, CPU incompatibility..."
---
# vMotion Failing

<div class="kb-summary">
A vMotion or Storage vMotion operation fails before completing. This scenario maps the most common failure
modes — MTU mismatch, CPU incompatibility, VMkernel routing gaps, and NSX segment availability — and gives
the exact CLI commands and vCenter checks to isolate and fix each one.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_read_the_error_message_first: "1. Read the Error Message First" {shape: rectangle}
2_evc_mode_check_cpu_incompatibility: "2. EVC Mode Check (CPU Incompatibility Errors)" {shape: rectangle}
3_vmkernel_mtu_check_most_common_cau: "3. VMkernel MTU Check (Most Common Cause)" {shape: rectangle}
4_vmkernel_routing_check: "4. VMkernel Routing Check" {shape: rectangle}
5_nic_and_driver_validation: "5. NIC and Driver Validation" {shape: rectangle}

products_involved -> 1_read_the_error_message_first: uses
1_read_the_error_message_first -> 2_evc_mode_check_cpu_incompatibility: uses
2_evc_mode_check_cpu_incompatibility -> 3_vmkernel_mtu_check_most_common_cau: uses
3_vmkernel_mtu_check_most_common_cau -> 4_vmkernel_routing_check: uses
4_vmkernel_routing_check -> 5_nic_and_driver_validation: uses
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

Go to **vCenter → Recent Tasks**, find the failed vMotion, and note the exact error string — it is the fastest path to the root cause.

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

If the error references CPU compatibility, check and set the cluster EVC baseline so all hosts present an identical CPU feature set.

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

MTU mismatch between the vMotion VMkernel and the physical switch causes the generic "system error" — test with a jumbo-frame ping before checking anything else.

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


```text title="Expected output"
vmk0  Management
vmk1  VMotion
vmk2  vSAN
PING 192.168.10.42 with 8972 bytes of data:
Reply from 192.168.10.42: bytes=8972 time=2ms TTL=64
Reply from 192.168.10.42: bytes=8972 time=1ms TTL=64
Reply from 192.168.10.42: bytes=8972 time=2ms TTL=64

--- 192.168.10.42 statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0% loss)
```

!!! warning "Common errors"
    **`PING 192.168.10.42 with 8972 bytes of data: Request timed out.`** — Verify the destination VMkernel IP is reachable and the vMotion VMkernel port is enabled on the destination host.
    **`Unable to locate interface vmk1`** — Confirm the vMotion VMkernel adapter exists on the source host by running `esxcli network ip interface list` and use the correct interface name.
    **`Fragmentation is required but DF set.`** — Reduce the payload size to 1472 bytes (`vmkping -I vmk1 -d -s 1472 <destination-vmk1-ip>`) and increase MTU to 9000 on the vSwitch and physical switch port.
```bash
# Verify current MTU on the VMkernel port
esxcli network ip interface list | grep -A5 vmk1

# Verify vSwitch MTU
esxcli network vswitch standard list | grep -E "Name|MTU"

# For VDS — check MTU from vCenter:
# vCenter → Networking → VDS → Configure → Properties → MTU
```


```text title="Expected output"
Name: vmk1
MAC Address: 00:50:56:a1:2c:3f
IPv4 Address: 192.168.1.42
IPv4 Netmask: 255.255.255.0
IPv6 Address: ::1
MTU: 1500
Enabled: true

Name: vSwitch0
MTU: 1500

Name: vSwitch1
MTU: 9000
```

!!! warning "Common errors"
    **`Name: vmk1 not found`** — Verify the VMkernel port exists with `esxcli network ip interface list` and use the correct interface name (e.g., vmk0, vmk1).
    **`error: Unknown command or namespace`** — Ensure you are running this command directly on an ESXi host via SSH or console, not from vCenter; esxcli is not available on vCenter servers.
Look for: `vmkping -d -s 8972` succeeds = MTU is correct end-to-end; failure with large frame but success with 1472-byte frame = switch or vDS MTU set to 1500.

---

## 4. VMkernel Routing Check

The vMotion VMkernel must have a route to the destination host's vMotion VMkernel IP — missing routes silently block vMotion on multi-subnet designs.

```bash
# List all IPv4 routes on the host
esxcli network ip route ipv4 list

# If the destination vmk1 subnet has no route, add a static route:
esxcli network ip route ipv4 add -n <destination-subnet>/<prefix> -g <gateway-ip>

# Verify the VMkernel firewall allows vMotion traffic (port 8000)
esxcli network firewall ruleset list | grep -i vmotion
# Status should be "true" (enabled)
```


```text title="Expected output"
VMkernel Routes
===============
Destination     Netmask         Gateway         VMknic  MTU  Flags
0.0.0.0         0.0.0.0         192.168.1.1     vmk0    1500 UG
192.168.1.0     255.255.255.0   0.0.0.0         vmk0    1500 U
10.20.0.0       255.255.0.0     192.168.1.254   vmk1    1500 UG
172.16.50.0     255.255.255.0   0.0.0.0         vmk2    1500 U

Ruleset              Enabled
vmotion              true
vSphereReplication   false
```

!!! warning "Common errors"
    **`Error: The object has already been added.`** — Verify the route doesn't already exist with `esxcli network ip route ipv4 list` before adding it.
    **`Error: Gateway is not reachable.`** — Ensure the gateway IP is on a directly connected subnet and reachable from the source VMkernel interface.
    **`Error: Unknown option or malformed command.`** — Check that the prefix length is numeric (e.g., `/24` not `/255.255.255.0`) and all parameters are in the correct order.
---

## 5. NIC and Driver Validation

Check the physical NIC backing the vMotion VMkernel for speed, duplex, and error counters before investigating higher layers.

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


```text title="Expected output"
Name                                                    Value
----                                                    -----
Driver                                                  bnx2x
Driver Version                                          1.78.75.v60.11-nsx
Firmware Version                                        7.13.21
Speed                                                   10000 Mb/s
Duplex                                                  Full
MAC Address                                             00:0a:95:9d:42:c1
MTU                                                     1500
Enabled                                                 true
Connected                                               true
Transceiver                                             SFP+ (10GBase-SR)
WakeOnLan Supported                                     false
WakeOnLan Enabled                                        false

   Rx Packets: 8847293
   Rx Bytes: 12456789012
   Rx Errors: 0
   Rx Dropped: 0
   Tx Packets: 7234156
   Tx Bytes: 9876543210
   Tx Errors: 0
   Tx Dropped: 0
```

!!! warning "Common errors"
    **`Could not find NIC vmnic1`** — Verify the NIC name with `esxcli network nic list` and use the correct interface identifier.
    **`Permission denied`** — Run the command as root or with appropriate ESXi host credentials via SSH or vSphere Client.
    **`Rx Errors: 1247 Rx Dropped: 342`** — Check physical cable connections, SFP+ transceiver compatibility, and switch port configuration for the vMotion uplink.
Look for: any non-zero `Drop` or `Error` counter on the vMotion uplink vmnic indicates NIC or cable issues that will cause vMotion timeouts.

---

## 6. NSX Segment Check (VM on NSX-T Overlay Network)

If the VM is on an NSX segment, confirm the segment is bound to the destination host's transport node — missing binding silently fails vMotion.

```bash
# From NSX Manager UI: Networking → Segments → select the segment
# Check "Transport Nodes" tab — destination host must appear as bound

# From NSX Manager CLI or API — list transport nodes for a segment
curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/logical-switches/<ls-id>/transport-node-status" \
  | python3 -m json.tool | grep -E "status|transport_node_id"
```


```text title="Expected output"
{
    "results": [
        {
            "transport_node_id": "tn-1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p",
            "status": "UP",
            "last_update_timestamp": 1699564823000
        },
        {
            "transport_node_id": "tn-9z8y7x6w-5v4u-3t2s-1r0q-9p8o7n6m5l4k",
            "status": "UP",
            "last_update_timestamp": 1699564821000
        },
        {
            "transport_node_id": "tn-4k3j2i1h-0g9f-8e7d-6c5b-4a3z2y1x0w9v",
            "status": "DOWN",
            "last_update_timestamp": 1699564500000
        }
    ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag (already present) or import the NSX Manager CA certificate into your system trust store.
    **`jq: command not found`** — Replace `python3 -m json.tool` with `jq '.'` or ensure Python 3 is installed and in PATH.
    **`HTTP/1.1 401 Unauthorized`** — Verify the admin password is correct and the credentials are properly URL-encoded if they contain special characters.
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


```text title="Expected output"
Name                           Version                        Vendor  Acceptance Level  Install Date
nsx-vib                        4.1.2.1-21567890               VMware  VMwareCertified    2024-01-15
nsx-container-plugin           4.1.2.1-21567890               VMware  VMwareCertified    2024-01-15

Name       Virtual Switch  Enabled  Portgroup  MAC Address        MTU  IP Address      Netstack
vmk0       vSwitch0        true     Management 00:50:56:a1:2c:4f  1500 192.168.1.45    defaultTcpipStack
vmk10      vSwitch1        true     TEP        00:50:56:a1:3d:5e  1600 10.100.50.12    defaultTcpipStack

PING 10.100.50.25 (10.100.50.25): 1572 data bytes
1580 bytes from 10.100.50.25: icmp_seq=0 time=2.145 ms
1580 bytes from 10.100.50.25: icmp_seq=1 time=1.987 ms
1580 bytes from 10.100.50.25: icmp_seq=2 time=2.234 ms
1580 bytes from 10.100.50.25: icmp_seq=3 time=2.056 ms

--- 10.100.50.25 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 1.987/2.105/2.234 ms
```

!!! warning "Common errors"
    **`vmkping: Unknown host <remote-tep-ip>`** — Replace `<remote-tep-ip>` with the actual TEP IP address of the remote ESXi host (e.g., 10.100.50.25).
    **`Cannot find device "vmk10"`** — Verify the TEP VMkernel interface name with `esxcli network ip interface list` and use the correct interface name in the vmkping command.
    **`100% packet loss`** — Check network connectivity between TEP interfaces, verify MTU is set to 1600 on both sides, and confirm NSX overlay network configuration is complete.
Look for: all NSX VIBs at matching versions; `vmkping -I vmk10 -d -s 1572` succeeds to all remote TEP IPs.

---

## 7. Large VM / Memory Bandwidth Timeout

For VMs over 32 GB RAM that time out during the memory copy phase, verify the vMotion network can outpace the VM's memory write rate.

```text
vMotion memory copy phases:
  1. Pre-copy: pages copied while VM runs; dirty pages tracked
  2. Iterative copy: dirty pages re-copied; repeat until convergence
  3. Switchover: VM briefly stunned; final pages copied; VM resumes on destination

Timeout occurs when the VM writes memory faster than the network can copy it.
Requirement: vMotion network bandwidth > VM memory write rate.
```

```bash
# Test actual throughput between hosts using iperf (if available)
# On destination host (as server):
iperf -s -B <destination-vmk1-ip> -p 5201

# On source host (as client):
iperf -c <destination-vmk1-ip> -B <source-vmk1-ip> -p 5201 -t 30
```


```text title="Expected output"
------------------------------------------------------------
Server listening on TCP port 5201
Binding to host 172.16.10.50, port 5201
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[  4] local 172.16.10.40 port 54892 connected to 172.16.10.50 port 5201
[ ID] Interval           Transfer     Bitrate
[  4]   0.00-5.00   sec  1.18 GBytes  2.03 Gbps
[  4]   5.00-10.00  sec  1.21 GBytes  2.08 Gbps
[  4]  10.00-15.00  sec  1.19 GBytes  2.05 Gbps
[  4]  15.00-20.00  sec  1.20 GBytes  2.06 Gbps
[  4]  20.00-25.00  sec  1.17 GBytes  2.01 Gbps
[  4]  25.00-30.00  sec  1.19 GBytes  2.04 Gbps
[  4]   0.00-30.00  sec  7.14 GBytes  2.04 Gbps                  sender
[  4]   0.00-30.00  sec  7.13 GBytes  2.04 Gbps                  receiver
```

!!! warning "Common errors"
    **`iperf: command not found`** — Install iperf on both hosts using `apt-get install iperf` (Ubuntu/Debian) or `yum install iperf` (RHEL/CentOS).
    **`connect to <destination-vmk1-ip> port 5201: Connection refused`** — Ensure the iperf server is running on the destination host before starting the client test.
    **`bind: Cannot assign requested address`** — Verify that the source and destination VMK IP addresses are correct and reachable using `ping` before running iperf.
Look for: throughput well below expected link speed (e.g., 2 Gbps on a 10 Gbps link) indicates a shared uplink with insufficient bandwidth — dedicate a higher-speed uplink to vMotion or increase streams in **Cluster → Configure → vSphere DRS → Advanced Options**.

---

## Key Terms

| Term | Definition |
|---|---|
| vMotion | Live migration feature that moves a powered-on VM between ESXi hosts with no downtime; requires compatible VMkernel networking, CPU baseline, and licensing |
| EVC | Enhanced vMotion Compatibility — cluster-level CPU masking that hides newer CPU features so VMs remain compatible with the oldest host in the cluster |
| VMkernel (vmk) | ESXi logical network interface used for host services; vmk0 = management, vmk1 = vMotion, vmk2 = vSAN, vmk10 = NSX TEP; each tagged for its role |
| MTU | Maximum Transmission Unit — frame size in bytes; vMotion with jumbo frames requires MTU 9000 end-to-end (vSwitch, vDS, physical switch); mismatch silently drops frames |
| vmkping | ESXi CLI tool to test connectivity from a specific VMkernel interface; `-d -s 8972` tests jumbo frame path without fragmentation |
| DFW | Distributed Firewall — NSX kernel-level firewall; follows the VM after vMotion by re-enforcing rules on the destination host's vNIC automatically |
| NSX segment | An overlay logical network backed by GENEVE tunnels; the destination host must be a transport node with the segment bound before vMotion can complete |
| TEP | Tunnel Endpoint — VMkernel interface (typically vmk10) used by NSX to encapsulate overlay traffic in GENEVE tunnels between ESXi hosts |
| vmnic | Physical NIC on the ESXi host; the vmnic backing the vMotion VMkernel must have sufficient speed, full duplex, and no error counters |
| vDS | vSphere Distributed Switch — cluster-wide virtual switch managed from vCenter; MTU and port group settings here affect all hosts connected to it |
| VMotion tag | The network service tag assigned to a VMkernel port that marks it as eligible for vMotion traffic; missing tag produces "No VMkernel adapter" error |
| thumbprint | SSL certificate fingerprint; vMotion uses certificate validation between hosts; a mismatched or expired thumbprint can block migration in secure environments |

---

## Common Mistakes

- **Testing ping to the management IP instead of the vmk1 IP.** Management (vmk0) and vMotion (vmk1) are on different VMkernel ports and may have different routes. Always test to the vmk1 address specifically.
- **Fixing MTU on vSwitch but not on the physical switch.** MTU must match end-to-end: vSwitch → distributed switch → physical switch port → ToR switch. One mismatched hop breaks jumbo frames.
- **Not checking EVC mode first when mixing host hardware generations.** A new host added to a cluster without EVC configured will silently block vMotion for all VMs that have been powered on since a CPU-feature-exposing operation.
- **Overlooking NSX transport node binding.** On NSX-T overlay networks, the destination host must be a transport node with the segment bound to it. This is easy to miss when adding new hosts to a cluster.

---

## Related Scenarios

- [VM Performance Degraded](vm-performance-degraded.md) — DRS triggers vMotion to rebalance load; understanding when vMotion fails under load is connected to performance investigations.
- [VM Inaccessible / HA Failover](vm-inaccessible-ha-failover.md) — HA-initiated restarts and DRS rebalancing after failover both rely on vMotion working correctly.
- [NSX Connectivity Broken](nsx-connectivity-broken.md) — NSX TEP or segment issues that cause vMotion failures overlap with the broader NSX connectivity troubleshooting flow.
