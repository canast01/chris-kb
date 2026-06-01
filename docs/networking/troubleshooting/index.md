# Network Troubleshooting

<div class="kb-summary">
Network troubleshooting knowledge base covering connectivity testing, packet loss diagnosis, path tracing, and reachability validation.
</div>

## DNS Troubleshooting

### Symptoms

- Hostname fails to resolve; application errors by name but not by IP
- Intermittent resolution failures — services randomly unreachable
- NFS/CIFS mounts failing (PTR record missing)
- Authentication failures (Kerberos requires working forward + reverse DNS)

### Triage Steps

#### 1. Test Resolution Directly

```bash
nslookup <hostname>
dig <hostname>
dig <hostname> @<dns_server_ip>    # query a specific server directly
```
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

#### 3. Test DNS Server Reachability

```bash
ping <dns_server_ip>
nslookup <hostname> <dns_server_ip>
```

#### 4. Forward and Reverse Resolution

```bash
# Forward: name → IP
dig <hostname>

# Reverse: IP → name (PTR)
dig -x <ip>
nslookup <ip>
```

Missing PTR records cause Kerberos failures and NFS/CIFS auth issues.

#### 5. Flush DNS Cache

**Windows:**
```cmd
ipconfig /flushdns
```

**Linux (systemd-resolved):**
```bash
resolvectl flush-caches
# or
systemctl restart systemd-resolved
```

#### 6. Test from Multiple Systems

If one server resolves but another doesn't, the issue is host-specific — wrong server configured, stale cache, or host firewall blocking UDP 53.

### Common Issues

| Symptom | Cause | Fix |
|---|---|---|
| NXDOMAIN | Record missing or wrong zone | Add/fix DNS record |
| Timeout | DNS server unreachable | Check firewall and DNS health |
| Wrong IP returned | Stale or duplicate record | Flush cache; fix record |
| Reverse lookup fails | Missing PTR record | Add PTR in DNS |
| Works by IP not name | Wrong DNS configured | Fix `/etc/resolv.conf` or DHCP |

## Network Connectivity

Structured approach to diagnosing end-to-end connectivity failures.

### Layer-by-Layer Triage

#### Layer 1 — Physical

```bash
# Linux — check interface link state
ip link show
ethtool <interface>    # speed, duplex, link detected
```

#### Layer 2 — Switching

```bash
# Check ARP table (confirm MAC resolved)
arp -a
ip neigh show

# Check interface is in correct VLAN
# On switch: show interface status, show vlan brief
```

#### Layer 3 — IP / Routing

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

#### Layer 4 — Transport

```bash
# Test specific TCP port
nc -zv <host> <port>
telnet <host> <port>
curl -v http://<host>:<port>/

# Check local firewall
iptables -L -n | grep <port>
firewall-cmd --list-all
```

### Path Tracing

```bash
traceroute <destination>    # Linux/Mac
tracert <destination>       # Windows
mtr <destination>           # continuous path trace
```

### Common Connectivity Tests

```bash
# ICMP ping
ping -c 4 <host>

# MTU test (verify no fragmentation)
ping -M do -s 1472 <host>    # Linux (1500 MTU = 1472 payload + 28 headers)
ping -f -l 1472 <host>       # Windows

# DNS and then connect
curl -v https://<fqdn>/
```

### Connectivity from Windows

```powershell
Test-NetConnection -ComputerName <host> -Port <port>
Test-NetConnection <host>    # ICMP test
Resolve-DnsName <host>
```

### Common Issues

| Layer | Issue | Check | Action |
|---|---|---|---|
| L1 | No link | `ethtool` | Check cable, SFP, port status |
| L2 | No ARP | `ip neigh` | Check VLAN, switch port config |
| L3 | No route | `ip route get` | Add route or fix gateway |
| L3 | Firewall blocking | Deny logs | Add firewall rule |
| L4 | Port blocked | `nc -zv` | Check host and network firewall |

## Packet Loss

Packet loss causes degraded application performance, storage I/O timeouts, replication lag, and vMotion failures.

### Identify the Loss

```bash
# Extended ping to observe loss pattern
ping -c 100 <destination>

# Continuous path trace with loss stats per hop
mtr <destination>
mtr --report --report-cycles 100 <destination>
```

`mtr` shows loss per hop — if loss appears at hop N but not N+1, it's ICMP de-prioritization by the router, not true loss. True loss appears at hop N and all subsequent hops.

### Interface Error Counters

```bash
# Linux
ethtool -S <interface> | grep -i error
ip -s link show <interface>

# Show interface errors
netstat -i

# Network interface stats
cat /proc/net/dev
```

### Duplex / Speed Mismatch

Half-duplex on a switch port causes severe packet loss under load:

```bash
ethtool <interface>
# Look for: Speed: 1000Mb/s, Duplex: Full
```

On the switch:
```bash
show interface <int>
# Look for: duplex full, 1000 Mbps
```

### Congestion / Queue Drops

```bash
# Linux — show interface TX/RX drops
ip -s link show <interface>
```

On the switch, check output drops:
```bash
show interface <int> counters    # Cisco
show interface <int>             # look for output drops
```

### Physical Layer Checks

```bash
# Check SFP/cable on the switch port
show interface <int> transceiver    # Cisco
# Check Rx power — should be within spec
```

### MTU Issues (Fragmentation)

Packet loss with large frames may be MTU-related:

```bash
ping -M do -s 8972 <destination>    # iSCSI/NFS MTU test (9000 bytes)
ping -M do -s 1472 <destination>    # standard MTU test
```

Any failure with do-not-fragment set indicates an MTU mismatch somewhere in the path.

### Common Causes

| Cause | Check | Action |
|---|---|---|
| Duplex mismatch | `ethtool` / switch port | Force full duplex on both ends |
| Congestion / drops | Interface counters | Increase bandwidth or QoS |
| Bad cable / SFP | Rx power, error counters | Replace SFP or cable |
| MTU mismatch | DF-bit ping | Align MTU across path |
| Physical interface errors | `ip -s link show` | Replace NIC or port |
