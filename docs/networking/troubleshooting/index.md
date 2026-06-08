# Networking — Troubleshooting

```bash
nslookup <hostname>
dig <hostname>
dig <hostname> @<dns_server_ip>    # query a specific server directly
```
```text
┌──────────────────────────────────── Networking — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Network troubleshooting: work from layer 1 up; isolate the failure layer first        │   │
│   │      Tools: ping (L3 reachability), traceroute (path), tcpdump/Wireshark (packet capture)     │   │
│   │      Process: define symptom → test from multiple points → narrow to single failure point     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Diagnostic Steps               │  │                Common Causes                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           L1: link up? SFP seated?           │  │           FW rule blocking traffic          │   │
│   │          L2: MAC learned? VLAN OK?           │  │           VLAN mismatch / missing           │   │
│   │           L3: ping gateway + dest            │  │          Routing missing/incorrect          │   │
│   │            Trace: traceroute path            │  │            MTU mismatch (DF bit)            │   │
│   │           Capture: tcpdump src/dst           │  │           DNS: name not resolving           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Layer       │      Check       │        Tool       │     Symptom      │  Fix direction   │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   L1 Physical    │    Link state    │      show int     │   err-disabled   │    Cable/SFP     │   │
│   │   L2 Data link   │    MAC + VLAN    │      show mac     │   No L2 learn    │   VLAN config    │   │
│   │    L3 Network    │   Route + ping   │     traceroute    │   Unreachable    │     Route/FW     │   │
│   │     L4+ App      │   Port + cert    │    nc / curl -v   │   Conn refused   │    FW/app/TLS    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OSI model    = 7-layer reference model; troubleshoot from bottom up (L1 → L7)                      │
│    MTU          = Maximum Transmission Unit; 1500B Ethernet; jumbo = 9000; mismatch = drops           │
│    DF bit       = Do Not Fragment; test MTU by pinging with DF set and large payload                  │
│    tcpdump      = Packet capture on Linux; filter by host, port, protocol; save to pcap               │
│    err-disabled = Switch port auto-disabled; cause: BPDU guard, port security, duplex mismatch        │
│    Asymmetric   = Forward and return path differ; FW stateful check fails; causes drops               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
ping <dns_server_ip>
nslookup <hostname> <dns_server_ip>
```
```bash
# Forward: name → IP
dig <hostname>

# Reverse: IP → name (PTR)
dig -x <ip>
nslookup <ip>
```
```cmd
ipconfig /flushdns
```
```bash
resolvectl flush-caches
# or
systemctl restart systemd-resolved
```
```bash
# Linux — check interface link state
ip link show
ethtool <interface>    # speed, duplex, link detected
```
```bash
# Check ARP table (confirm MAC resolved)
arp -a
ip neigh show

# Check interface is in correct VLAN
# On switch: show interface status, show vlan brief
```
```bash
# Confirm IP configuration
ip addr show

# Confirm route exists
ip route show
ip route get <destination_ip>

# Default gateway
ip route show default
ping <gateway_ip>
```
```bash
# Test specific TCP port
nc -zv <host> <port>
telnet <host> <port>
curl -v http://<host>:<port>/

# Check local firewall
iptables -L -n | grep <port>
firewall-cmd --list-all
```
```bash
traceroute <destination>    # Linux/Mac
tracert <destination>       # Windows
mtr <destination>           # continuous path trace
```
```bash
# ICMP ping
ping -c 4 <host>

# MTU test (verify no fragmentation)
ping -M do -s 1472 <host>    # Linux (1500 MTU = 1472 payload + 28 headers)
ping -f -l 1472 <host>       # Windows

# DNS and then connect
curl -v https://<fqdn>/
```
```powershell
Test-NetConnection -ComputerName <host> -Port <port>
Test-NetConnection <host>    # ICMP test
Resolve-DnsName <host>
```
```bash
# Extended ping to observe loss pattern
ping -c 100 <destination>

# Continuous path trace with loss stats per hop
mtr <destination>
mtr --report --report-cycles 100 <destination>
```
```bash
# Linux
ethtool -S <interface> | grep -i error
ip -s link show <interface>

# Show interface errors
netstat -i

# Network interface stats
cat /proc/net/dev
```
```bash
ethtool <interface>
# Look for: Speed: 1000Mb/s, Duplex: Full
```
```bash
show interface <int>
# Look for: duplex full, 1000 Mbps
```
```bash
# Linux — show interface TX/RX drops
ip -s link show <interface>
```
```bash
show interface <int> counters    # Cisco
show interface <int>             # look for output drops
```
```bash
# Check SFP/cable on the switch port
show interface <int> transceiver    # Cisco
# Check Rx power — should be within spec
```
```bash
ping -M do -s 8972 <destination>    # iSCSI/NFS MTU test (9000 bytes)
ping -M do -s 1472 <destination>    # standard MTU test
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="network-connectivity/"><strong>Network Connectivity</strong><span>End-to-end connectivity troubleshooting — L1 through L7 diagnostic procedures and tools.</span></a>
</div>
