---
tags:
  - reference
---
# Decision Tree: VM Network Issue


<div class="kb-summary">
Use this when a VM cannot communicate on the network — applies to both NSX-T overlay and standard vSphere networking.
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

**Packet loss on large packets** → MTU mismatch on physical switch, dvSwitch, or NSX TEP VLAN.

## Step 4 — Routing Issue

```bash
# From VM
ip route show   # Confirm default gateway is correct
route print     # Windows

# From a Linux jump host on the same segment
traceroute <destination>   # Where does it drop?
```

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

Analyse with Wireshark: download from `/tmp/capture.pcap` via SCP.
