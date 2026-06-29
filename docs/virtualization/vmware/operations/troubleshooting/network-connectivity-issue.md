---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
---
# Network Connectivity Issues

<div class="kb-summary">
Troubleshooting VM network connectivity failures — vSwitch/vDS configuration, portgroup VLAN mismatches, VMkernel routing, NSX segment issues, and physical uplink failures.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
vmotion_fails: "vMotion Fails" {shape: rectangle}
vm_network_outage: "VM Network Outage" {shape: rectangle}
host_management_network_issue: "Host Management Network Issue" {shape: rectangle}
nsx_issues: "NSX Issues" {shape: rectangle}
packet_loss_on_a_vm_or_host: "Packet Loss on a VM or Host" {shape: rectangle}
verify: "Verify" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> vmotion_fails: investigate
symptom -> vm_network_outage: investigate
symptom -> host_management_network_issue: investigate
symptom -> nsx_issues: investigate
symptom -> packet_loss_on_a_vm_or_host: investigate
symptom -> verify: investigate
vmotion_fails -> resolution
vm_network_outage -> resolution
host_management_network_issue -> resolution
nsx_issues -> resolution
packet_loss_on_a_vm_or_host -> resolution
verify -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## vMotion Fails

**Step 1 — Check the VMkernel adapter tagged for vMotion:**

```bash
# From ESXi — verify VMkernel adapters and their tags
esxcli network ip interface list
esxcli network ip interface tag get -i vmk1  # vmk1 is typically the vMotion vmk

# Check vMotion is enabled on the vmk
esxcli network ip interface list | grep -A5 vmk1
```


```text title="Expected output"
Name          IPv4 Address         IPv6 Address  MTU  MAC Address        Enabled
vmk0          192.168.1.45         ::1           1500 00:0c:29:a4:2b:1c  true
vmk1          192.168.100.50       ::1           1500 00:0c:29:a4:2b:1d  true
vmk2          192.168.200.10       ::1           1500 00:0c:29:a4:2b:1e  true

vmk1
   Tags: vMotion,Management

Name          IPv4 Address         IPv6 Address  MTU  MAC Address        Enabled
vmk1          192.168.100.50       ::1           1500 00:0c:29:a4:2b:1d  true
```

!!! warning "Common errors"
    **`Could not connect to the host. The host may not be running, or the login credentials may not be valid.`** — Verify ESXi host is reachable and you have valid credentials; if running locally on the host, ensure you're in the DCUI or SSH session.
    **`Unknown option or malformed command.`** — Check esxcli syntax; use `esxcli network ip interface list --help` to verify correct command format for your ESXi version.
**Step 2 — Verify MTU consistency** — vMotion requires jumbo frames (MTU 9000) if configured; a mismatch between the VMkernel adapter, vSwitch, and physical switch will cause failures:

```bash
# Check VMkernel MTU
esxcli network ip interface list | grep -E "Name|MTU"

# Test vMotion network reachability with correct MTU
vmkping -I vmk1 -d -s 8972 <destination-esxi-vmotion-ip>
# -d = don't fragment, -s 8972 = payload size (8972 + 28 byte header = 9000 MTU)
```


```text title="Expected output"
Name                          MTU
vmk0                          1500
vmk1                          9000
vmk2                          1500
vmk3                          9000

PING <destination-esxi-vmotion-ip> (192.168.100.45): 8972 data bytes
8980 bytes from 192.168.100.45: icmp_seq=0 time=2.341 ms
8980 bytes from 192.168.100.45: icmp_seq=1 time=2.156 ms
8980 bytes from 192.168.100.45: icmp_seq=2 time=2.289 ms
8980 bytes from 192.168.100.45: icmp_seq=3 time=2.401 ms

--- 192.168.100.45 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 2.156/2.297/2.401 ms
```

!!! warning "Common errors"
    **`Fragmentation is occurring; packets are fragmented`** — Reduce the payload size or verify the physical switch and vSAN network are configured for jumbo frames (MTU 9000).
    **`vmk1: No such device`** — Verify the vMotion VMkernel adapter exists with `esxcli network ip interface list` and use the correct interface name.
    **`100% packet loss`** — Check network connectivity between hosts, verify the destination IP is reachable, and confirm firewall rules allow ICMP traffic on the vMotion network.
**Step 3 — Check error details in vCenter Tasks:**

- "The migration was not attempted because no valid network is available" → No vMotion vmk on the destination
- "The host is not licensed for vMotion" → Check host licensing
- "EVC mismatch" → CPU feature compatibility; EVC cluster mode may need updating
- "The VM is using a device or file that is not accessible on the target host" → Local VMDK, local ISO, or CD-ROM still attached

---

## VM Network Outage

**Step 1 — Confirm the VM can ping its gateway** from inside the guest. If not, check the virtual NIC is still connected:

```powershell
# PowerCLI — check VM network adapter connection state
Get-VM "VMName" | Get-NetworkAdapter | Select Name, NetworkName, ConnectionState
```

**Step 2 — Check the port group:**

```bash
# From ESXi — list port groups and VLAN IDs
esxcli network vswitch standard portgroup list
esxcli network vswitch dvs vmware portgroup list  # For distributed vSwitch
```


```text title="Expected output"
Name                          VLAN ID  vSwitch
---------------------------  --------  ---------
VM Network                         0  vSwitch0
Management Network                 1  vSwitch0
vMotion                           10  vSwitch0
FT Logging                        20  vSwitch0
iSCSI-A                          100  vSwitch1
iSCSI-B                          101  vSwitch1

Name                          VLAN ID  vSwitch
---------------------------  --------  ---------
DV-Production                     50  DSwitch-Prod
DV-DMZ                            60  DSwitch-Prod
DV-Management                      1  DSwitch-Mgmt
DV-vMotion                        10  DSwitch-Mgmt
```

!!! warning "Common errors"
    **`Could not connect to the host. Error: Connection refused`** — Verify ESXi host is reachable and SSH is enabled (Configuration > Security Profile > Services > SSH).
    **`This command is not supported on this system`** — Confirm you are running the command directly on ESXi; distributed vSwitch commands require vCenter connectivity or must be run from the vCenter CLI.
Confirm the port group VLAN ID matches the upstream switch configuration. A recent switch-side VLAN change will strand all VMs on that port group.

**Step 3 — Check physical uplinks:**

```bash
# Check vmnic link state
esxcli network nic list | grep -E "Name|Link"

# Check which vmnics back the vSwitch
esxcli network vswitch standard list
```


```text title="Expected output"
Name    Link
vmnic0  Up
vmnic1  Up
vmnic2  Down
vmnic3  Up

Name                    Portgroups                          MTU     Promisc Mode   MAC Address        CLT Beacon
vSwitch0                Management Network,VM Network       1500    False          00:50:56:c0:00:01  Enabled
vSwitch1                iSCSI-Network                       9000    False          00:50:56:c0:00:02  Disabled
```

!!! warning "Common errors"
    **`esxcli: command not found`** — Ensure you are running this command directly on an ESXi host via SSH or console, not from a vCenter server or external system.
    **`Unable to find a matching nic`** — Verify the vmnic naming is correct (vmnic0, vmnic1, etc.) and that the network stack is running with `esxcli system module list | grep vsanmgmt`.
**Step 4 — Check NIC teaming policy** — if an uplink failed and the teaming policy does not failover correctly:

```bash
esxcli network vswitch standard policy failover get -v vSwitch0
```


```text title="Expected output"
vSwitch Name: vSwitch0
Active Uplinks: vmnic0, vmnic1
Standby Uplinks: vmnic2
Unused Uplinks: 
Failover Detection: Link Status only
Notify Switches: true
Reverse Direction: false
Load Balancing Policy: Route based on IP hash
Network Failure Detection: Link Status only
```

!!! warning "Common errors"
    **`Error: Unknown option or esxcli command`** — Verify you are running this command on an ESXi host with network management enabled, not from vCenter; use SSH to connect directly to the ESXi host.
    **`Error: Could not find vswitch named vSwitch0`** — Check the correct vSwitch name using `esxcli network vswitch standard list` and replace vSwitch0 with the actual name.
---

## Host Management Network Issue

If the host management network goes down, vCenter loses the host and SSH stops working.

**Recovery path using DCUI (Direct Console User Interface):**

1. Connect to iDRAC/iLO virtual console → open host console.
2. Press F2 to enter DCUI.
3. Go to **Configure Management Network** → verify IP, subnet, gateway, DNS.
4. Press **Escape** and select "Test Management Network" — this runs ping and DNS tests from the host.
5. If the configuration was changed, confirm the management VLAN setting on the physical switch port.

```bash
# Once SSH access is restored — verify management vmk
esxcli network ip interface ipv4 get -i vmk0
esxcli network ip route list
```


```text title="Expected output"
Name  IPv4 Address      IPv4 Netmask      IPv4 Broadcast    Type        DHCP
----  ---------------   ----------------  ----------------  ----------  ----
vmk0  192.168.1.45      255.255.255.0     192.168.1.255     STATIC      false

Destination     Netmask         Gateway         Device
-----------     -------         -------         ------
0.0.0.0         0.0.0.0         192.168.1.1     vmk0
192.168.1.0     255.255.255.0   0.0.0.0         vmk0
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace network.ip.interface.ipv4.get`** — Verify the ESXi version supports this esxcli namespace; use `esxcli network ip interface list` as an alternative on older versions.
    **`Error: Unable to connect to the host`** — Confirm SSH is fully restored and the management network (vmk0) is up by checking `esxcli network ip interface list` first.
---

## NSX Issues

| Symptom | Check |
|---|---|
| VMs on NSX segments cannot communicate | TEP (Tunnel Endpoint) connectivity; VTEP MTU |
| Edge gateway unreachable | Edge node health; BGP peering state |
| Distributed firewall blocking unexpected traffic | DFW rule order; service tag definitions |
| Transport node status red in NSX Manager | Host preparation state; NSX agent on the ESXi host |

```bash
# From ESXi — check NSX VTEP interface
esxcli network ip interface list | grep vmk

# Check TEP ping between two hosts
vmkping -I vmk10 -d -s 1572 <remote-tep-ip>

# Check NSX agent status on ESXi host
/etc/init.d/nsx-opsagent status
/etc/init.d/nsx-mpa status
```


```text title="Expected output"
Name  Portset      IPV4 Address      IPV6 Address  MTU  MAC Address        Enabled
vmk0  Management   192.168.1.45      ::1           1500 00:0c:29:a4:2b:8f  true
vmk1  vMotion      192.168.2.100     ::1           1500 00:0c:29:a4:2b:90  true
vmk10 NSX-VTEP     172.16.50.12      ::1           1600 00:0c:29:a4:2b:91  true
vmk11 NSX-VTEP     172.16.50.13      ::1           1600 00:0c:29:a4:2b:92  true

PING 172.16.50.25 with 1572 bytes of data:
16 bytes from 172.16.50.25: icmp_seq=0 time=2.145 ms
16 bytes from 172.16.50.25: icmp_seq=1 time=1.987 ms
16 bytes from 172.16.50.25: icmp_seq=2 time=2.234 ms
--- 172.16.50.25 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss

nsx-opsagent is running
nsx-mpa is running
```

!!! warning "Common errors"
    **`vmkping: Unknown host <remote-tep-ip>`** — Replace `<remote-tep-ip>` with an actual TEP IP address (e.g., 172.16.50.25) that is reachable from the source host.
    **`nsx-opsagent is not running`** — Restart the NSX agent with `/etc/init.d/nsx-opsagent start` and verify NSX Manager connectivity and licensing.
    **`Unknown command or namespace: network ip interface`** — Verify you are running this command directly on an ESXi host (not vCenter); use `ssh root@<esxi-host>` to connect first.
From NSX Manager UI:
- System → Fabric → Hosts — check each transport node status
- System → Fabric → Edges — check edge node status and tunnel state
- Networking → Tier-0 Gateways → check BGP neighbor state

---

## Packet Loss on a VM or Host

```bash
# From ESXi — check vmnic error counters
esxcli network nic stats get -n vmnic0
# Look for: rx_errors, tx_errors, rx_dropped, tx_dropped

# Check for CRC errors on physical switch port (from switch CLI)
# Cisco: show interface GigabitEthernetX/X counters errors

# Test with vmkping to rule out congestion vs physical errors
vmkping -I vmk0 -c 100 <destination-ip>
```


```text title="Expected output"
Name: vmnic0
Driver: bnx2x
Queue Stats:
  RX packets: 45782156
  RX bytes: 28934521847
  TX packets: 38291045
  TX bytes: 19284756234
  RX errors: 0
  TX errors: 0
  RX dropped: 0
  TX dropped: 0
  RX crc errors: 0
  Collisions: 0

PING 192.168.100.50 (192.168.100.50): 56 data bytes
64 bytes from 192.168.100.50: icmp_seq=0 time=2.145 ms
64 bytes from 192.168.100.50: icmp_seq=1 time=2.089 ms
64 bytes from 192.168.100.50: icmp_seq=2 time=2.156 ms
...
--- 192.168.100.50 statistics ---
100 packets transmitted, 100 packets received, 0% packet loss
round-trip min/avg/max = 2.089/2.134/3.421 ms
```

!!! warning "Common errors"
    **`Error: Could not get nic stats for vmnic0`** — Verify the vmnic exists with `esxcli network nic list` and confirm you have root/admin privileges.
    **`Unable to resolve destination-ip`** — Replace `<destination-ip>` with an actual reachable IP address on the network segment being tested.
    **`vmkping: command not found`** — Confirm you are running this command directly on the ESXi host console or via SSH, not from vCenter.
Common causes:

| Cause | Indicator | Fix |
|---|---|---|
| Duplex mismatch | Incrementing rx/tx errors on vmnic | Force speed/duplex on switch port to match NIC; or set both to auto |
| MTU mismatch | Large packets dropped silently | Set MTU consistently end-to-end |
| Physical cable / transceiver | CRC errors on switch | Reseat or replace cable/SFP |
| NIC teaming imbalance | One vmnic handling all traffic | Review load balancing policy (Route Based on IP hash requires LACP) |
| Congestion on shared path | High latency and drops under load | Check QoS settings; consider storage traffic isolation to a separate vmnic |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificate Issues](certificate-issue.md)
- [Datastore Issues](datastore-inaccessible.md)
- [Host Disconnected / Not Responding](host-disconnected.md)
- [Virtualization Troubleshooting](index.md)
