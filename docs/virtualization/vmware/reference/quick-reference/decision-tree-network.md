---
tags:
  - reference
description: "Use this when a VM cannot communicate on the network — applies to both NSX-T overlay and standard vSphere networking."
---
# Decision Tree: VM Network Issue

<div class="kb-summary">
Use this when a VM cannot communicate on the network — applies to both NSX-T overlay and standard vSphere networking.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
                     VM: Cannot communicate
                               │
                               ▼
                    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
                    │ Ping default GW?    │
                    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
               No ▼                       Yes ▼
    ┌─────────────────────────────────────────────── ┐     ┌ ───────────────────────────────────────────────┐
    │ Check portgroup/VLAN  │     │ Ping destination?    │
    │ assignment            │     └──────────────────────┘
    │ Check MTU mismatch    │     No ▼              Yes ▼
    └───────────────────────┘  ┌──────────┐     ┌──────────────┐
               │               │ Routing? │     │ NSX DFW rule │
               ▼               │ Tier-0   │     │ blocking?    │
    ┌───────────────────────┐  │ BGP peers│     │ Trace Flow   │
    │ NSX segment check:    │  └──────────┘     └──────────────┘
    │ correct tier-1 attach │         │
    │ TEP reachability      │         ▼
    └───────────────────────┘  ┌─────────────────────────┐
                                │ pktcap-uw capture on   │
                                │ vNIC → analyse in Wireshark │
                                └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Step 1 — Basic Connectivity Test

```bash
# From within the VM
ping -c 4 <gateway-ip>
ping -c 4 8.8.8.8
traceroute <destination>
```


```text title="Expected output"
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=2.12 ms
64 bytes from 192.168.1.1: icmp_seq=4 ttl=64 time=1.95 ms

--- 192.168.1.1 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 1.89/2.07/2.34/0.18 ms
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=24.56 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=23.89 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=24.12 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=119 time=23.67 ms

--- 8.8.8.8 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/stddev = 23.67/24.06/24.56/0.35 ms
traceroute to example.com (93.184.216.34), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  1.23 ms  1.45 ms  1.67 ms
 2  10.0.0.1 (10.0.0.1)  5.34 ms  5.12 ms  5.89 ms
 3  203.0.113.45 (203.0.113.45)  12.56 ms  12.34 ms  12.78 ms
 4  93.184.216.34 (93.184.216.34)  18.92 ms  19.01 ms  18.67 ms
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ping: unknown host <gateway-ip>` | Replace `<gateway-ip>` with the actual gateway IP address (e.g., 192.168.1.1) or verify the VM has network connectivity. |
    | `ping: sendto: Operation not permitted` | Check that ICMP is not blocked by the VM's firewall or security group rules; disable the firewall temporarily to test. |
    | `traceroute: command not found` | Install traceroute with `apt-get install traceroute` (Debian/Ubuntu) or `yum install traceroute` (RHEL/CentOS). |
**Cannot ping gateway** → Step 2 (L2/VLAN issue)
**Can ping gateway, not destination** → Step 4 (routing/firewall issue)

## Step 2 — VLAN / Segment Issue

```powershell
# Check VM's port group assignment
Get-VM -Name <vm_name> | Get-NetworkAdapter | Select-Object NetworkName, ConnectionState

# Check port group VLAN ID (for standard/distributed vSwitch)
Get-VDPortgroup -Name <portgroup> | Select-Object Name, VlanConfiguration
```

For NSX overlay segments:
```bash
# Check segment exists and is connected to the correct tier-1
GET /api/v1/logical-switches?display_name=<segment-name>
# Verify attached to correct tier-1 gateway
```


```text title="Expected output"
{
  "results": [
    {
      "id": "logical-switch-001",
      "display_name": "prod-segment-web",
      "state": "SUCCESS",
      "realization_state": "REALIZED",
      "transport_zone_display_name": "TZ-VLAN-100",
      "connectivity": "ON",
      "admin_state": "UP",
      "tier_1_gateways": [
        {
          "target_id": "tier1-gw-prod-01",
          "target_display_name": "tier1-gw-prod-01"
        }
      ]
    }
  ],
  "result_count": 1
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `{"error_code":400,"error_message":"Invalid display_name parameter"}` | Verify the segment name matches exactly (case-sensitive) and is URL-encoded if it contains special characters. |
    | `{"error_code":401,"error_message":"Unauthorized"}` | Ensure your NSX Manager API credentials are valid and the authentication token has not expired. |
    | `{"error_code":404,"error_message":"Segment not found"}` | Confirm the segment exists in NSX Manager and check that you are querying the correct NSX Manager instance. |
**Port group/segment misconfigured** → Correct assignment and re-test.

## Step 3 — MTU Check

VM-to-gateway communication failures can be caused by MTU mismatch (especially in NSX environments where the recommended MTU is 1600+):

```bash
# From VM — test with large packet (NSX requires MTU ≥ 1600 on uplinks)
ping -M do -s 1500 <gateway-ip>   # Linux
ping -f -l 1472 <gateway-ip>      # Windows (1472 + 28 headers = 1500 bytes)

# On ESXi host — check vmnic MTU
esxcfg-nics -l | grep -E "Name|MTU"
```


```text title="Expected output"
PING 10.20.1.1 (10.20.1.1) 1500(1528) bytes of data.
1508 bytes from 10.20.1.1: icmp_seq=1 ttl=64 time=2.341 ms
1508 bytes from 10.20.1.1: icmp_seq=2 ttl=64 time=2.156 ms
1508 bytes from 10.20.1.1: icmp_seq=3 ttl=64 time=2.289 ms
^C
--- 10.20.1.1 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 2.156/2.262/2.341/0.078 ms

Name          Mtu
vmnic0       1500
vmnic1       1500
vmnic2       9000
vmnic3       1500
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ping: -M: unknown option` | Use `ping -M do` on Linux; the `-M` flag is not available on macOS or older Linux versions—verify your OS and use `man ping` to confirm syntax. |
    | `PING: transmit failed. General failure.` | Ensure the gateway IP is reachable and on the same subnet; verify network connectivity with `ipconfig /all` and check firewall rules. |
    | `Command 'esxcfg-nics' not found` | Run the command directly on an ESXi host via SSH or console, not from a vCenter server or Linux VM; verify you are logged into the correct host. |
**Packet loss on large packets** → MTU mismatch on physical switch, dvSwitch, or NSX TEP VLAN.

## Step 4 — Routing Issue

```bash
# From VM
ip route show   # Confirm default gateway is correct
route print     # Windows

# From a Linux jump host on the same segment
traceroute <destination>   # Where does it drop?
```


```text title="Expected output"
# ip route show
default via 192.168.1.1 dev eth0 proto dhcp metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.45 metric 100
169.254.0.0/16 dev eth0 scope link metric 1002

# route print
===========================================================================
Interface List
  16...08:00:27:6a:2f:4c ......Intel(R) PRO/1000 MT Desktop Adapter
===========================================================================
IPv4 Route Table
===========================================================================
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0      192.168.1.1    192.168.1.100      25
      192.168.1.0    255.255.255.0         On-link     192.168.1.100     266

# traceroute 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  2.341 ms  2.156 ms  2.089 ms
 2  10.0.0.1 (10.0.0.1)  8.923 ms  9.104 ms  8.756 ms
 3  203.0.113.45 (203.0.113.45)  24.567 ms  24.892 ms  24.234 ms
 4  * * *
 5  8.8.8.8 (8.8.8.8)  31.245 ms  31.089 ms  30.876 ms
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `SIOCADDRT: No such process` | Verify the gateway IP is reachable and the network interface is up with `ip link show`. |
    | `traceroute: command not found` | Install traceroute with `apt-get install traceroute` (Debian/Ubuntu) or `yum install traceroute` (RHEL/CentOS). |
    | `Network is unreachable` | Confirm the VM's network adapter is connected to the correct vSwitch and the default gateway matches the subnet configuration. |
If traffic drops at the tier-0 edge:
- Check BGP peer state on the edge node:
  ```bash
  get bgp neighbor summary   # All peers should be Established
  ```
- Verify edge uplink connectivity to the physical router

## Step 5 — NSX Distributed Firewall (DFW)

If L2 and routing are confirmed working:

```bash
# Check DFW rules applied to the VM — from ESXi host where VM runs
vsipioctl getrules -f <filter-name>   # Get filter name from VM's vmx file

# Get VM's DFW filter name
summarize-dvfilter | grep -A 5 <vm-name>
```


```text title="Expected output"
Filter: vShield-vm-12345678-abcd-1234-5678-1234567890ab
Direction: IN
Action: ALLOW
Protocol: TCP
DestinationPort: 443
SourceAddress: 192.168.1.0/24
---
Direction: OUT
Action: DROP
Protocol: UDP
DestinationPort: 53
---

VM Name: web-server-prod-01
Filter ID: vShield-vm-12345678-abcd-1234-5678-1234567890ab
Status: ACTIVE
Rules Applied: 8
Last Updated: 2024-01-15 14:32:18
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vsipioctl: command not found` | Ensure you are running this command directly on the ESXi host (SSH into the host), not from vCenter or a remote machine. |
    | `Filter not found or invalid filter name` | Verify the filter name matches exactly what appears in the VM's .vmx file (case-sensitive) by checking `/vmfs/volumes/<datastore>/vm-name/vm-name.vmx`. |
    | `summarize-dvfilter: command not found` | This command is only available on ESXi 6.0+; for older versions, use `net-dvs -l` to list distributed virtual switch filters instead. |
Look for DENY rules matching the traffic flow. Check in NSX Manager:
- Policy → Security → Gateway Firewall and Distributed Firewall
- Use "Trace Flow" to simulate a specific flow and see which rule handles it:
  NSX Manager → Plan & Troubleshoot → Traffic Analysis

## Step 6 — Packet Capture

If still unresolved, capture on the relevant interface:

```bash
# Capture on VM's vNIC from ESXi host
pktcap-uw --switchport <port-id> --proto 0x0800 -o /tmp/capture.pcap

# Get port ID
net-dvs -l | grep -A 10 <vm-name>
```


```text title="Expected output"
Port ID: 67108873
Portset Name: DvsPortset-0
Port Index: 73
Port State: Block
Port Flags: 0x0
VLAN ID: 0
Teaming Policy: loadbalance_srcid
Active Uplinks: vmnic0, vmnic1
Standby Uplinks: (none)
Reserved Clients: (none)

Capturing on port 67108873 with filter 0x0800
Packets captured: 1247
Output file: /tmp/capture.pcap
Capture completed successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `pktcap-uw: command not found` | Run the command directly on the ESXi host via SSH or console, not from a vCenter client machine. |
    | `net-dvs: command not found` | Ensure you are connected to the ESXi host shell; these tools are only available in the ESXi command line, not in vCenter. |
    | `Error: Invalid port ID` | Verify the port ID exists by running `net-dvs -l` first and confirm the VM is powered on and connected to the distributed virtual switch. |
Analyse with Wireshark: download from `/tmp/capture.pcap` via SCP.
