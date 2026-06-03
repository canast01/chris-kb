# NSX — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Ports and Protocols Reference, Log Locations, NSX Manager CLI Diagnostics, Edge Node CLI Diagnostics, ESXi Host NSX Diagnostics and 4 more sections.
</div>

## Ports and Protocols Reference

| Traffic | Protocol | Port | Direction |
|---|---|---|---|
| NSX Manager UI/API | HTTPS | 443 | Client → Manager |
| NSX Manager CLI (SSH) | SSH | 22 | Admin → Manager |
| Geneve overlay | UDP | 6081 | TEP → TEP (ESXi/Edge) |
| BGP | TCP | 179 | Edge uplink → Physical router |
| BFD | UDP | 3784 | Edge uplink → Physical router |
| vCenter → NSX Manager | HTTPS | 443 | vCenter → Manager |
| NSX Manager → ESXi | HTTPS | 443 | Manager → ESXi host |
| NSX Manager → iDRAC | HTTPS | 443 | Manager → iDRAC (for bare-metal Edge) |
| DNS | TCP/UDP | 53 | Manager/Edge → DNS servers |
| NTP | UDP | 123 | Manager/Edge → NTP servers |
| Syslog (UDP) | UDP | 514 | Manager/Edge → Syslog server |
| Syslog (TLS) | TCP | 6514 | Manager/Edge → Syslog server |

---

## Log Locations

### NSX Manager

| Log File | Location | Content |
|---|---|---|
| Manager | `/var/log/vmware/nsx-manager/manager.log` | Control plane, policy realisation |
| API | `/var/log/vmware/nsx-manager/audit.log` | API calls, user actions, role changes |
| HTTP access | `/var/log/vmware/nsx-manager/access.log` | API endpoint access log |
| Cluster | `/var/log/vmware/nsx-manager/corfu.log` | Corfu DB / Raft state |
| System | `/var/log/syslog` | OS-level system events |

```bash
# SSH to NSX Manager node
# Live log tail
tail -f /var/log/vmware/nsx-manager/manager.log

# Search for realisation errors
grep -i "error\|fail\|exception" /var/log/vmware/nsx-manager/manager.log | tail -30

# Search audit log for admin actions
grep -i "role\|login\|delete\|create" /var/log/vmware/nsx-manager/audit.log | tail -20
```text
┌────────────────────────────────────────── NSX — Diagnostics ──────────────────────────────────────────┐
│                                                                                                       │
│  NSX log locations, Traceflow tool, IPFIX flow export, and support bundles.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Key Log Files                 │  │                Traceflow Tool               │   │
│   │          /var/log/proton (manager)           │  │           NSX UI: Plan > Traceflow          │   │
│   │             /var/log/nsx-syslog              │  │            Inject L2/L3/L4 packet           │   │
│   │          /var/log/bfd.log (routing)          │  │             See path hop by hop             │   │
│   │           ESXi: /var/log/nsx-*.log           │  │           Identify drop + rule hit          │   │
│   │           Edge: /var/log/nsx-*.log           │  │             Bidirectional trace             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Logs → Traceflow for path/DFW → IPFIX for flows → bundle for GSS.                                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             IPFIX / Flow Export              │  │                Support Bundle               │   │
│   │          DFW IPFIX per-rule export           │  │         UI: System > Support Bundle         │   │
│   │          Collector: Aria NI / sflow          │  │          API: POST /api/v1/suppbndl         │   │
│   │          Flow visibility map build           │  │            Includes all node logs           │   │
│   │         Used for micro-seg planning          │  │           Select: manager + edges           │   │
│   │         Identify undocumented flows          │  │             Upload to VMware SR             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs, Edge VMs, ESXi nodes, IPFIX collector, management network                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  proton log  = NSX Manager core process log; cluster/config events                                    │
│  Traceflow   = NSX packet path simulation; shows rule hits and drops                                  │
│  IPFIX       = IP Flow Info Export; protocol for DFW flow telemetry                                   │
│  Aria NI     = Aria Network Insight; NSX flow analytics platform                                      │
│  sFlow       = sampling protocol; alternative to IPFIX for flows                                      │
│  BFD         = Bidirectional Forwarding Detection; fast link failure detect                           │
│  nsx-syslog  = aggregated NSX system log; forwarded to SIEM                                           │
│  Support bundle = NSX zip; all nodes logs + configs for GSS                                           │
│  SR          = Service Request; VMware GSS support ticket                                             │
│  Drop observation = Traceflow result showing which rule blocked packet                                │
│  Flow visibility = map of who talks to whom; built from IPFIX data                                    │
│  Bidirectional= Traceflow sends packets in both directions simultaneously                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## NSX Manager CLI Diagnostics

```bash
# SSH to any NSX Manager node
nsxcli

# Cluster and node health
get cluster status
get managers
get clusters
get corfu-cluster status

# Services
get services
get service http
get service manager
get service controller

# Transport infrastructure
get transport-nodes
get transport-node-status
get tunnel endpoints
get tunnel status

# Overlay
get logical-switches
get logical-routers

# Alarms
get alarms
get alarms | grep -i "critical\|high"

# Version
get version
get nodes
```

---

## Edge Node CLI Diagnostics

```bash
# SSH to Edge node (admin user)
# All routing commands require VRF context

# List all logical routers (VRFs) on this Edge
get logical-routers

# Enter T0 gateway VRF
vrf <vrf-id>

# Routing
get route
get route detail
get forwarding

# BGP
get bgp neighbor summary
get bgp neighbor <peer-ip>
get bgp neighbor <peer-ip> routes
get bgp neighbor <peer-ip> advertised-routes
get bgp config

# Exit VRF context
exit

# Interface status
get interfaces
get interface fp-eth0
get interface fp-eth0 counters

# High Availability
get edge-cluster status
get high-availability status
get high-availability channels

# System
get node
get node cpu-usage
get node memory
get services
get version
```

---

## ESXi Host NSX Diagnostics

```bash
# SSH to ESXi host as root

# Verify NSX VIBs are installed
esxcli software vib list | grep -i nsx

# TEP vmkernel IP
esxcli network ip interface ipv4 get

# TEP route reachability
esxcli network ip route ipv4 list | grep <tep-subnet>

# Test TEP connectivity (replace vmk2 and IP with your TEP vmk)
vmkping -I vmk2 <remote-tep-ip>
vmkping -I vmk2 -d -s 1572 <remote-tep-ip>   # MTU test

# DFW filter inspection
summarize-dvfilter                             # List all filters
summarize-dvfilter | grep <vm-name>           # Filter for a specific VM

vsipioctl getrules -f <filter-name>           # Rules applied to this filter
vsipioctl getstats -f <filter-name>           # Rule hit counts
vsipioctl getaddrsets -f <filter-name>        # Security group memberships
vsipioctl getservices -f <filter-name>        # Service definitions in rules

# vDS and VNI mapping
net-vdl2 -M all -s 0
```

---

## Traceflow

Traceflow injects a synthetic probe packet into the logical network and traces its path hop-by-hop. Use it to determine exactly where a packet is being dropped.

### Launch Traceflow

**NSX Manager UI: Plan & Troubleshoot → Traceflow**

Or via API:

```bash
# Create a traceflow request
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "lport_id": "<source-vm-logical-port-id>",
    "packet": {
      "eth_header": {
        "src_mac": "<source-vm-mac>",
        "dst_mac": "<gateway-or-dest-mac>"
      },
      "ip_header": {
        "src_ip": "10.0.1.10",
        "dst_ip": "10.0.2.20",
        "ttl": 64,
        "protocol": 1
      },
      "icmp_header": {
        "icmp_type": 8,
        "icmp_code": 0
      },
      "resource_type": "FieldsPacketData",
      "transport_type": "UNICAST"
    }
  }' \
  "https://<nsx-manager>/api/v1/traceflows"

# Poll for results
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/traceflows/<traceflow-id>"
```

### Traceflow Output Interpretation

| Observation Type | Meaning |
|---|---|
| `FORWARDED` at a hop | Packet passed through this component |
| `DROPPED` at a hop | Packet dropped here — check rule or route |
| `RECEIVED` at destination | Packet reached the destination |
| `DELIVERED` at ESXi host | Packet delivered to VM vNIC |

If Traceflow shows `DROPPED` at the DFW filter of the source VM, the drop reason will identify the specific rule ID.

---

## Packet Capture

### Edge Node Packet Capture

```bash
# SSH to Edge node

# Capture on physical uplink
debug packet capture interface fp-eth0 count 500
debug packet capture interface fp-eth0 filter "host 10.0.0.1 and tcp port 179" count 200

# Capture on overlay interface (Geneve)
debug packet capture interface nsx-geneve count 500

# Write to file for Wireshark
debug packet capture interface fp-eth0 file /tmp/edge-cap.pcap count 1000

# Copy from Edge to external location
scp /tmp/edge-cap.pcap user@jumphost:/tmp/
```

### ESXi Host Packet Capture

```bash
# Capture on a physical NIC (vmnic)
pktcap-uw --capture Uplink --switchport <portid> --outfile /tmp/vmnic-cap.pcap --count 500

# Capture on a vDS port (VM's traffic)
pktcap-uw --capture VmVnic --switchport <portid> --outfile /tmp/vm-cap.pcap --count 200

# Find the portID for a VM's vNIC
net-stats -l | grep <vm-name>

# Capture with BPF filter
pktcap-uw --capture Uplink --switchport <portid> --filter "port 6081" --outfile /tmp/geneve-cap.pcap
```

---

## API-Based Diagnostics

### Check Realisation State

After making a policy change, verify it has been realised on all transport nodes:

```bash
# Check segment realisation
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/segments/<segment-id>/state"

# Check security policy realisation
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/realized-state/realized-entities?intent_path=/infra/domains/default/security-policies/<policy-id>"

# Check T0 gateway realisation
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/tier-0s/<t0-id>/state"
```

### Check Open Alarms

```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Critical alarms: {d.get(\"result_count\",0)}')
for a in d.get('results',[]):
    src  = a.get('alarm_source',{}).get('display_name','?')
    summ = a.get('summary','')[:100]
    ts   = a.get('timestamp_epoch','?')
    print(f'  [{ts}] {src}: {summ}')
"
```

### Check Transport Node Connectivity to Manager

```bash
# Transport node should have a connection_state of "success" or "in_sync"
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/transport-nodes/<tn-id>/state" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'State: {d.get(\"state\",\"?\")}')
print(f'Transport failures: {d.get(\"transport_failures\",[])}')
"
```

---

## Diagnostic Data Collection for Support

When opening a Broadcom support case for NSX:

```bash
# 1. NSX Manager support bundle (from any Manager node)
# UI: System → Support Bundle → Download
# Or via API:
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"log_age": 48}' \
  "https://<nsx-manager>/api/v1/node/support-bundles"

# 2. Edge node tech support bundle (from each Edge node CLI)
collect tech-support

# 3. Cluster status snapshot
nsxcli
get cluster status > /tmp/cluster-status.txt
get transport-node-status >> /tmp/cluster-status.txt
get tunnel status >> /tmp/cluster-status.txt

# 4. DFW filter output from affected ESXi host
summarize-dvfilter > /tmp/dvfilter.txt
vsipioctl getrules -f <affected-filter> >> /tmp/dvfilter.txt
```

Provide timestamps of when the issue started, what changes were made in the 24 hours before the issue, and a clear description of the impact scope.
