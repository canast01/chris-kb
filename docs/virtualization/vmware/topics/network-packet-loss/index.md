---
tags:
  - vmware
description: "Network Packet Loss Validation reference covering Symptoms, NIC Statistics, vmkping — Reachability and MTU Testing, PowerCLI Network Checks, Common Causes..."
---
# Network Packet Loss Validation

<div class="kb-summary">
Network Packet Loss Validation reference covering Symptoms, NIC Statistics, vmkping — Reachability and MTU Testing, PowerCLI Network Checks, Common Causes and Fixes and 1 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

symptoms: "Symptoms" {shape: rectangle}
nic_statistics: "NIC Statistics" {shape: rectangle}
vmkping_reachability_and_mtu_testing: "vmkping — Reachability and MTU Testing" {shape: rectangle}
powercli_network_checks: "PowerCLI Network Checks" {shape: rectangle}
common_causes_and_fixes: "Common Causes and Fixes" {shape: rectangle}
ongoing_monitoring: "Ongoing Monitoring" {shape: rectangle}

symptoms -> nic_statistics: uses
nic_statistics -> vmkping_reachability_and_mtu_testing: uses
vmkping_reachability_and_mtu_testing -> powercli_network_checks: uses
powercli_network_checks -> common_causes_and_fixes: uses
common_causes_and_fixes -> ongoing_monitoring: uses
```

## Symptoms

| Symptom | Likely Cause |
|---|---|
| Dropped packets on vmnic | Physical NIC, cable, or switch port issue |
| Slow or failed vMotion | vMotion VMkernel packet loss or high latency |
| VM intermittent connectivity | Port group misconfiguration or uplink saturation |
| vSAN health: network errors | vSAN VMkernel path issues |
| NSX tunnel flapping | Geneve underlay MTU mismatch |

## NIC Statistics

```bash
# Per-NIC stats including drops, errors, and CRC errors
esxcli network nic stats get -n vmnic0
esxcli network nic stats get -n vmnic1

# Key counters to check
# RX/TX dropped   — driver ring buffer overflow
# RX/TX errors    — physical layer (cable, SFP, switch)
# RX/TX CRC       — physical layer corruption

# List all NICs and link state
esxcli network nic list
```


```text title="Expected output"
NIC Statistics for vmnic0
   Packets received: 45782341
   Packets sent: 38291847
   Bytes received: 12847293847
   Bytes sent: 9384729384
   Receive errors: 0
   Transmit errors: 0
   Receive dropped: 127
   Transmit dropped: 0
   Receive CRC: 0
   Collisions: 0

NIC Statistics for vmnic1
   Packets received: 44921847
   Packets sent: 37849201
   Bytes received: 12734928374
   Bytes sent: 9271847293
   Receive errors: 2
   Transmit errors: 0
   Receive dropped: 89
   Transmit dropped: 0
   Receive CRC: 3
   Collisions: 0

Name    PCI Driver   Link State   Speed   Duplex   MAC Address
vmnic0  0000:02:00.0 bnx2x        Up      10000Mbps Full   00:0a:95:9d:68:f2
vmnic1  0000:02:00.1 bnx2x        Up      10000Mbps Full   00:0a:95:9d:68:f3
vmnic2  0000:04:00.0 ixgbe        Down    0Mbps    Half   00:0a:95:9d:68:f4
vmnic3  0000:04:00.1 ixgbe        Up      10000Mbps Full   00:0a:95:9d:68:f5
```

!!! warning "Common errors"
    **`Error: Unknown option or set of options.`** — Verify the NIC name is correct (e.g., vmnic0, not vm-nic0) and that you have ESXi 5.0 or later.
    **`Error: Could not connect to the host.`** — Ensure you are connected to the ESXi host via SSH or vSphere CLI with appropriate credentials.
## vmkping — Reachability and MTU Testing

```bash
# Basic ping from a VMkernel adapter
vmkping -I vmk0 <destination_ip>

# Large packet test (MTU validation — 8972 bytes = 9000 MTU minus headers)
vmkping -I vmk0 -d -s 8972 <destination_ip>

# vSAN VMkernel MTU test
vmkping -I vmk2 -d -s 8972 <peer_vsan_vmk_ip>

# vMotion VMkernel latency test
vmkping -I vmk1 -c 100 <target_host_vmk1_ip>
```


```text title="Expected output"
PING 192.168.100.50 (192.168.100.50): 56 data bytes
64 bytes from 192.168.100.50: icmp_seq=0 ttl=64 time=2.341 ms
64 bytes from 192.168.100.50: icmp_seq=1 ttl=64 time=2.156 ms
64 bytes from 192.168.100.50: icmp_seq=2 ttl=64 time=2.289 ms

PING 192.168.100.50 (192.168.100.50): 8972 data bytes
8972 bytes from 192.168.100.50: icmp_seq=0 ttl=64 time=5.412 ms
8972 bytes from 192.168.100.50: icmp_seq=1 ttl=64 time=5.198 ms
8972 bytes from 192.168.100.50: icmp_seq=2 ttl=64 time=5.667 ms

PING 192.168.1.75 (192.168.1.75): 8972 data bytes
8972 bytes from 192.168.1.75: icmp_seq=0 ttl=64 time=1.834 ms
8972 bytes from 192.168.1.75: icmp_seq=1 ttl=64 time=1.921 ms
8972 bytes from 192.168.1.75: icmp_seq=2 ttl=64 time=1.756 ms

PING 192.168.50.22 (192.168.50.22): 56 data bytes
--- 192.168.50.22 statistics ---
100 packets transmitted, 100 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.891/1.247/3.156/0.412 ms
```

!!! warning "Common errors"
    **`Unknown interface vmk0`** — Verify the VMkernel adapter name with `esxcli network ip interface list` and use the correct interface identifier.
    **`Destination Host Unreachable`** — Confirm the destination IP is reachable and the vSAN/vMotion network routing is configured correctly on both ESXi hosts.
    **`Message too long`** — Reduce the packet size below the MTU (e.g., `-s 8972` for 9000 MTU) or verify the physical switch and vNIC MTU settings match.
Packet loss should always be **zero**. Any loss requires investigation before proceeding with maintenance.

## PowerCLI Network Checks

```powershell
# Physical NIC link state for all hosts in a cluster
Get-Cluster "<cluster>" | Get-VMHost | ForEach-Object {
    $h = $_
    Get-VMHostNetworkAdapter -VMHost $h -Physical |
        Select-Object @{N="Host";E={$h.Name}}, Name, BitRatePerSec,
        @{N="LinkUp";E={$_.ExtensionData.LinkSpeed -ne $null}}
}

# VMkernel adapters and their tagging
Get-VMHostNetworkAdapter -VMHost "<host>" -VMKernel |
    Select-Object Name, IP, VMotionEnabled, ManagementTrafficEnabled, VsanTrafficEnabled

# Portgroup VLAN assignments
Get-VirtualPortGroup -VMHost "<host>" | Select-Object Name, VLanId
```

## Common Causes and Fixes

| Cause | Detection | Fix |
|---|---|---|
| MTU mismatch | `vmkping -d -s 8972` fails | Align MTU on vSwitch, physical switch, and NIC |
| NIC queue full | `esxcli network nic stats` shows drops | Reduce load or enable receive-side scaling (RSS) |
| Bad cable/SFP | CRC errors in NIC stats | Replace cable or SFP |
| Uplink saturation | High TX/RX utilisation | Add uplink or redistribute workloads |
| Wrong VLAN on portgroup | VMs in same subnet can't communicate | Fix VLAN ID in portgroup config |
| Spanning tree topology change | Transient loss after switch change | Enable PortFast on host-facing switch ports |

## Ongoing Monitoring

```bash
# Watch NIC stats (refresh every 2s)
watch -n 2 "esxcli network nic stats get -n vmnic0 | grep -E 'Dropped|Error|CRC'"

# Or use esxtop for real-time network metrics
esxtop   # press 'n' to switch to network view
```


```text title="Expected output"
Every 2.0s: esxcli network nic stats get -n vmnic0 | grep -E 'Dropped|Error|CRC'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                esxcli network nic stats get -n vmnic0 | grep -E 'Dropped|Error|CRC'
```