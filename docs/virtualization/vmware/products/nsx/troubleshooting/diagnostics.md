---
tags:
  - nsx
  - nsx-4
  - troubleshooting
  - vmware
search:
  boost: 1.5
description: "NSX diagnostic commands: check cluster and transport node health with nsxcli, inspect manager and audit logs, diagnose Edge BGP routing, inspect DFW..."
---
# NSX — Diagnostics

<div class="kb-summary">
NSX diagnostic commands: check cluster and transport node health with nsxcli, inspect manager and audit logs, diagnose Edge BGP routing, inspect DFW filters on ESXi hosts with vsipioctl, run Traceflow for hop-by-hop path analysis, capture packets on Edge and ESXi, and generate the NSX support bundle for VMware SRs.

*Applies to: VMware NSX 9.x (VCF 9); NSX 4.2.x is the VCF 5.x line*
</div>
![NSX — Diagnostics](../../../../../assets/virtualization-vmware-nsx-troubleshooting-diagnostics.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "nsxcli: get cluster status\nget managers" {shape: rectangle}
D: "NSX UI: Traceflow — inject packet\nCheck for rule drop or routing gap" {shape: rectangle}
E: "Edge CLI: vrf then get bgp neighbor summary\nCheck underlay MTU with vmkping -d -s 1572" {shape: rectangle}
F: "summarize-dvfilter on ESXi host\nvsipioctl getrules -f filter-name" {shape: rectangle}
G: "get transport-nodes status\nCheck TEP vmkernel IP and route" {shape: rectangle}
H: "Open alarms via API\nGET /api/v1/alarms?status=OPEN severity=CRITICAL" {shape: rectangle}
I: "I" {shape: rectangle}
J: "Collect manager.log from failed node\nCheck cluster quorum: get cluster status" {shape: rectangle}
K: "get services\nCheck disk and memory on the Manager VM" {shape: rectangle}
L: "L" {shape: rectangle}
M: "vsipioctl getrules -f filter-name on ESXi\nIdentify rule ID and section in NSX policy" {shape: rectangle}
N: "Edge: vrf then get route\nCheck T0/T1 route redistribution" {shape: rectangle}
O: "Check Edge port counters: get physical-port\nfp-eth0 stats\nVerify BGP peers: get bgp neighbor summary" {shape: rectangle}
P: "vsipioctl getstats -f filter-name to see rule hit\ncounts\nvsipioctl getaddrsets for security group members" {shape: rectangle}
Q: "ESXi: vmkping -I vmk2 remote-tep-ip\nesxcli network ip interface ipv4 get to verify TEP IP" {shape: rectangle}
R: "Review alarm source and recommended action\nCheck realisation: GET /policy/api/v1/infra/segments" {shape: rectangle}
S: "Collect NSX support bundle\nOpen VMware SR" {shape: rectangle}
T: "UI: System > Support Bundle\nAPI: POST /api/v1/administration/\nsupport-bundles?action=collect" {shape: rectangle}
A: "NSX Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> K
L -> M
L -> N
E -> O
F -> P
G -> Q
H -> R
J -> S
K -> S
M -> S
N -> S
O -> S
P -> S
Q -> S
R -> S
S -> T
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_nsx_manager_cluster_hea: "Step 1 — Check NSX Manager cluster health" {shape: rectangle}
step_2_check_alarms_and_transport_no: "Step 2 — Check alarms and transport node status" {shape: rectangle}
step_3_diagnose_tep_connectivity_on_: "Step 3 — Diagnose TEP connectivity on ESXi hosts" {shape: rectangle}
step_4_inspect_dfw_filters_on_esxi: "Step 4 — Inspect DFW filters on ESXi" {shape: rectangle}
step_5_diagnose_edge_node_routing_an: "Step 5 — Diagnose Edge node routing and BGP" {shape: rectangle}
step_6_run_traceflow_for_hopbyhop_pa: "Step 6 — Run Traceflow for hop-by-hop path analysis" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_nsx_manager_cluster_hea: investigate
symptom -> step_2_check_alarms_and_transport_no: investigate
symptom -> step_3_diagnose_tep_connectivity_on_: investigate
symptom -> step_4_inspect_dfw_filters_on_esxi: investigate
symptom -> step_5_diagnose_edge_node_routing_an: investigate
symptom -> step_6_run_traceflow_for_hopbyhop_pa: investigate
step_1_check_nsx_manager_cluster_hea -> resolution
step_2_check_alarms_and_transport_no -> resolution
step_3_diagnose_tep_connectivity_on_ -> resolution
step_4_inspect_dfw_filters_on_esxi -> resolution
step_5_diagnose_edge_node_routing_an -> resolution
step_6_run_traceflow_for_hopbyhop_pa -> resolution
```

## Before you begin

- **Access:** SSH to an NSX Manager node (admin user); NSX UI credentials; ESXi root SSH access; Edge node admin SSH access
- **Gather first:** the specific symptom (VM unreachable, BGP down, DFW rule unexpected behavior, transport node alarm), affected segment or gateway name, and when the issue started
- **Scope:** confirm whether the issue affects one VM, one segment, one Edge gateway, or the entire NSX Manager cluster

---

## Step 1 — Check NSX Manager cluster health

```bash
# SSH to NSX Manager node
ssh admin@<nsx-manager-ip>

# Enter NSX CLI
nsxcli

# Manager cluster and node status
get cluster status
# Expected: all 3 nodes STABLE

get managers
# Shows: node IDs, IPs, roles

# All NSX services
get services
get service manager     # Management plane
get service controller  # Control plane
get service http        # API

# Version and node inventory
get version
get nodes
```

```text title="Expected output"
Output varies by environment; see the NSX 9.1 CLI Guide: https://developer.broadcom.com/xapis/nsx-cli-guide/9.1.0/all_all_commands.html
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connection refused` | Verify NSX Manager IP is correct and SSH service is running; check firewall rules allowing port 22 to the management interface. |
    | `Cluster Status: UNSTABLE` | Check node connectivity and disk space on all three managers using `get cpu-stats`, `get memory-stats` and `get filesystem-stats`; restart the manager service if a node is stuck. |
    | `Corfu-cluster status: QUORUM_LOST` | Ensure all three NSX Manager nodes are running and network connectivity between them is healthy; check group status with `get cluster status verbose`. |
---

## Step 2 — Check alarms and transport node status

```bash
# Open critical alarms via REST API — open critical alarms with source and message
curl -sk -u 'admin:<password>' \
  "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Critical alarms: {d.get(\"result_count\",0)}')
for a in d.get('results',[]):
    src  = a.get('alarm_source',{}).get('display_name','?')
    summ = a.get('summary','')[:120]
    print(f'  {src}: {summ}')
"

# All transport nodes and their connection state
get transport-nodes status
# Expected: all nodes CONNECTED; problem = DISCONNECTED or DEGRADED

# Tunnel health (run on an Edge node): TEPs, tunnel ports, BFD sessions
get vteps
get tunnel-ports
get bfd-sessions
# Expected: all BFD sessions up; problem = down sessions

# Via REST API — specific transport node state
curl -sk -u 'admin:<password>' \
  "https://<nsx-manager>/api/v1/transport-nodes/<tn-id>/state" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'State: {d.get(\"state\",\"?\")}')
print(f'Transport failures: {d.get(\"transport_failures\",[])}')
"
```

```text title="Expected output"
Output varies by environment; see the NSX 9.1 CLI Guide: https://developer.broadcom.com/xapis/nsx-cli-guide/9.1.0/all_all_commands.html
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip certificate verification, or import the NSX Manager CA certificate into your system trust store. |
    | `jq: command not found` or `python3: command not found` | Install the missing tool (e.g., `apt-get install python3-minimal` on Ubuntu or `yum install python3` on RHEL) or use the native `grep` and `awk` alternatives instead of JSON parsing. |
    | `401 Unauthorized` | Verify the admin credentials are correct and the user has API access permissions; check NSX Manager audit logs for authentication failures. |
---

## Step 3 — Diagnose TEP connectivity on ESXi hosts

```bash
# SSH to the ESXi host as root

# Verify NSX VIBs are installed
esxcli software vib list | grep -i nsx
# Expected: nsx-vib entries present

# TEP vmkernel interface IP
esxcli network ip interface ipv4 get
# Look for: vmk2 or vmk10 with the TEP IP assigned

# TEP route to reach remote TEPs
esxcli network ip route ipv4 list | grep <tep-subnet>

# Test TEP connectivity to a remote ESXi host TEP
vmkping -I vmk2 <remote-tep-ip>
# Expected: 0% loss

# Test MTU — Geneve requires 1600 bytes; test with DF bit set
vmkping -I vmk2 -d -s 1572 <remote-tep-ip>
# -d = DF bit; -s 1572 = data payload (adds 28 bytes = 1600 total)
# Problem: packet loss = MTU mismatch on the physical underlay
```


```text title="Expected output"
nsx-vib-6.4.10-19045146.x86_64
nsx-vib-6.4.10-19045146.x86_64 (other module)

Name  IPv4 Address      Netmask         Broadcast       Enabled Type
----  ----------------  ---------------  ---------------  ------- ----
vmk0  192.168.1.50      255.255.255.0    192.168.1.255    true    DHCP
vmk2  172.16.1.25       255.255.255.0    172.16.1.255     true    STATIC
vmk10 10.0.0.0          255.255.255.0    10.0.0.255       false   STATIC

Destination     Netmask         Gateway         Interface
-----------     ---------------  ---------------  ---------
172.16.1.0      255.255.255.0    Local            vmk2
0.0.0.0         0.0.0.0          192.168.1.1      vmk0

PING 172.16.1.30 (172.16.1.30): 56 data bytes
64 bytes from 172.16.1.30: icmp_seq=0 time=2.341 ms
64 bytes from 172.16.1.30: icmp_seq=1 time=2.156 ms
64 bytes from 172.16.1.30: icmp_seq=2 time=2.289 ms
--- 172.16.1.30 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss

PING 172.16.1.30 (172.16.1.30): 1572 data bytes
1600 bytes from 172.16.1.30: icmp_seq=0 time=3.012 ms
1600 bytes from 172.16.1.30: icmp_seq=1 time=2.987 ms
1600 bytes from 172.16.1.30: icmp_seq=2 time=3.045 ms
--- 172.16.1.30 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: (standard input): No such file or directory` | Verify NSX VIBs are actually installed by running `esxcli software vib list` without piping first to confirm the command executes. |
    | `PING 172.16.1.30 (172.16.1.30): 1572 data bytes`** followed by **`100% packet loss` | Check physical switch and NIC MTU settings; ensure all underlay network interfaces are configured for at least 1600 bytes MTU with `esxcli network nic get -n vmnicX | grep MTU`. |
    | `Network is unreachable` | Verify the TEP subnet route exists and the vmk2 interface is up by running `esxcli network ip interface list` and confirming the TEP interface is enabled and has a valid IP address. |
---

## Step 4 — Inspect DFW filters on ESXi

```bash
# SSH to ESXi host as root

# List all DFW filter instances (one per vNIC)
summarize-dvfilter
# Or filter for a specific VM
summarize-dvfilter | grep <vm-name>
# Note the filter name (e.g., nic-123456-eth0-vmware-sfw.2)

# View rules applied to a specific filter
vsipioctl getrules -f <filter-name>
# Shows: rule ID, action (pass/drop), source/dest IPs, ports, direction

# View rule hit statistics (to identify which rule is blocking)
vsipioctl getstats -f <filter-name>
# Shows: per-rule packet/byte counters — high counts on a drop rule = culprit

# View security group members (address sets) used in this filter
vsipioctl getaddrsets -f <filter-name>

# View service definitions
vsipioctl getservices -f <filter-name>

# VDS and VNI mapping (overlay to host port mapping)
net-vdl2 -M all -s 0
```


```text title="Expected output"
[root@esx-prod-01:~] summarize-dvfilter
DVFilter: nic-123456-eth0-vmware-sfw.2
DVFilter: nic-123457-eth1-vmware-sfw.2
DVFilter: nic-123458-eth2-vmware-sfw.2
...

[root@esx-prod-01:~] summarize-dvfilter | grep web-app-vm
DVFilter: nic-123456-eth0-vmware-sfw.2

[root@esx-prod-01:~] vsipioctl getrules -f nic-123456-eth0-vmware-sfw.2
Rule ID 1001: action=pass src=10.0.1.0/24 dst=10.0.2.0/24 proto=tcp dport=443 dir=in
Rule ID 1002: action=drop src=192.168.0.0/16 dst=any proto=any dir=in
Rule ID 1003: action=pass src=any dst=10.0.2.5 proto=tcp dport=22 dir=in
Rule ID 1004: action=drop src=any dst=any proto=any dir=in

[root@esx-prod-01:~] vsipioctl getstats -f nic-123456-eth0-vmware-sfw.2
Rule ID 1001: packets=4521847 bytes=2847392104 hits=4521847
Rule ID 1002: packets=0 bytes=0 hits=0
Rule ID 1003: packets=156 bytes=18432 hits=156
Rule ID 1004: packets=8934 bytes=524288 hits=8934

[root@esx-prod-01:~] vsipioctl getaddrsets -f nic-123456-eth0-vmware-sfw.2
AddressSet: SG-Web-Tier (10.0.1.5, 10.0.1.6, 10.0.1.7)
AddressSet: SG-DB-Tier (10.0.2.10, 10.0.2.11)

[root@esx-prod-01:~] vsipioctl getservices -f nic-123456-eth0-vmware-sfw.2
Service: HTTPS (tcp/443)
Service: SSH (tcp/22)
Service: DNS (udp/53)

[root@esx-prod-01:~] net-vdl2 -M all -s 0
VNI 5000 -> VLAN 100 (vxlan)
VNI 5001 -> VLAN 101 (vxlan)
VNI 5002 -> VLAN 102 (vxlan)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vsipioctl: filter nic-123456-eth0-vmware-sfw.2 not found` | Verify the exact filter name from `summarize-dvfilter` output and ensure the VM is powered on. |
    | `command not found: vsipioctl` | Confirm you are logged into the ESXi host directly (not vCenter) and that NSX is installed on this cluster. |
    **`net-vdl2: command not found`** —
---

## Step 5 — Diagnose Edge node routing and BGP

```bash
# SSH to Edge node as admin

# List all logical routers (T0/T1 VRFs) on this Edge
get logical-routers
# Note the vrf ID for the T0 gateway

# Enter the T0 VRF context
vrf <vrf-id>

# BGP neighbor summary
get bgp neighbor summary
# Expected: all peers in Established state
# Problem: Idle, Active, or Connect = BGP session not formed

# BGP peer detail
get bgp neighbor <peer-ip>
get bgp neighbor <peer-ip> routes
get bgp neighbor <peer-ip> advertised-routes

# Routing table
get route
get route detail

# Exit VRF
exit

# Edge interface counters (check for errors on uplink)
get interfaces
get interface fp-eth0
get physical-port fp-eth0 stats

# Edge HA status
get edge-cluster status
get high-availability status
get high-availability channels

# Edge system resources
get cpu-stats
get memory-stats
```

```text title="Expected output"
Output varies by environment; see the NSX 9.1 CLI Guide: https://developer.broadcom.com/xapis/nsx-cli-guide/9.1.0/all_all_commands.html
```
---

## Step 6 — Run Traceflow for hop-by-hop path analysis

```bash
# Via NSX UI (recommended): Plan > Traceflow
# Select source logical port, inject ICMP/TCP/UDP packet, view hop results

# Via Policy REST API (create or update a traceflow config):
curl -sk -u 'admin:<password>' \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "segment_port_path": "/infra/segments/<segment-id>/ports/<port-id>",
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
      "transport_header": {"icmp_echo_request_header": {"id": 1, "sequence": 1}},
      "resource_type": "FieldsPacketData",
      "transport_type": "UNICAST"
    }
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/traceflows/<traceflow-id>"

# Poll for Traceflow results
curl -sk -u 'admin:<password>' \
  "https://<nsx-manager>/policy/api/v1/infra/traceflows/<traceflow-id>/observations"
# Look for: DROPPED observations with the rule ID that blocked the packet

# Check policy realisation (segment, DFW policy, T0 gateway)
curl -sk -u 'admin:<password>' \
  "https://<nsx-manager>/policy/api/v1/infra/segments/<segment-id>/state"
curl -sk -u 'admin:<password>' \
  "https://<nsx-manager>/policy/api/v1/infra/tier-0s/<t0-id>/state"
```

```text title="Expected output"
Output varies by environment; see the NSX 9.1 REST API reference: https://developer.broadcom.com/xapis/nsx-t-data-center-rest-api/9.1.0/
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the NSX Manager CA certificate into your system trust store. |
    | `{"error_code":401,"error_message":"Invalid credentials"}` | Verify the NSX Manager admin password is correct and the user account has API access permissions. |
    | `{"error_code":404,"error_message":"Traceflow not found"}` | Ensure the traceflow ID is correct and wait a few seconds for the traceflow to complete processing before polling results. |
---

## Step 7 — Packet capture and collect support bundle

```bash
# Packet capture on Edge node uplink
ssh admin@<edge-ip>
start capture interface fp-eth0

# Write to PCAP file for Wireshark, filtered on a BGP peer
start capture interface fp-eth0 direction dual file edge-cap.pcap count 1000 expression ip 10.0.0.1 port 179

# Packet capture on ESXi host (physical NIC)
pktcap-uw --capture Uplink --switchport <portid> --outfile /tmp/vmnic-cap.pcap --count 500
pktcap-uw --capture VmVnic --switchport <portid> --outfile /tmp/vm-cap.pcap --count 200
pktcap-uw --capture Uplink --switchport <portid> --filter "port 6081" --outfile /tmp/geneve-cap.pcap

# Find portID for a VM's vNIC
net-stats -l | grep <vm-name>

# Generate NSX support bundle (includes all Manager + Edge + transport node logs)
curl -sk -u 'admin:<password>' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"nodes": ["<node-uuid>"], "log_age_limit": 2}' \
  "https://<nsx-manager>/api/v1/administration/support-bundles?action=collect"

# Edge support bundle (from each Edge node CLI)
ssh admin@<edge-ip>
get support-bundle file edge-bundle.tgz

# Cluster status snapshot for the SR
nsxcli
get cluster status > /tmp/cluster-status.txt
get transport-nodes status >> /tmp/cluster-status.txt
```

```text title="Expected output"
Output varies by environment; see the NSX 9.1 CLI Guide: https://developer.broadcom.com/xapis/nsx-cli-guide/9.1.0/all_all_commands.html
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Packet capture failed: interface fp-eth0 not found` | Verify the correct uplink interface name with `show interface` on the Edge node. |
    | `Permission denied (publickey,password)` | Ensure SSH credentials are correct and the admin account is enabled on the NSX Edge node. |
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip certificate verification or import the NSX Manager CA certificate into your trust store. |
---

## Log locations

| Component | Path / Command | What to look for |
|---|---|---|
| NSX Manager | `/var/log/vmware/nsx-manager/manager.log` | Config realisation, cluster errors |
| Audit log | `/var/log/vmware/nsx-manager/audit.log` | Admin actions, role changes |
| BFD (routing) | `/var/log/bfd.log` (on Manager/Edge) | Fast link failure detection events |
| NSX syslog | `/var/log/nsx-syslog` | Aggregated events; forward to SIEM |
| ESXi DFW | `vsipioctl getstats -f <filter>` on ESXi | Per-rule drop hit counts |
| Edge | `/var/log/nsx-*.log` on Edge VM | BGP, routing, packet forwarding errors |
| Support bundle | `POST /api/v1/administration/support-bundles?action=collect` | All-in-one — required for VMware SR |

---

## See also

- [NSX — Common Issues](../common-issues/)
- [NSX — Escalation](../escalation/)

## Verify resolution

- `get cluster status` in nsxcli shows all 3 Manager nodes STABLE
- `get transport-nodes status` shows all transport nodes CONNECTED
- `get bfd-sessions` on each Edge node shows all tunnel BFD sessions up
- Traceflow test from source VM to destination returns DELIVERED with no DROPPED observation
- `get bgp neighbor summary` on the Edge shows all peers Established
- `GET /api/v1/alarms?status=OPEN` returns no CRITICAL or HIGH severity open alarms
