# Network Connectivity

Structured approach to diagnosing end-to-end connectivity failures.
## Layer-by-Layer Triage

### Layer 1 — Physical

```bash
# Linux — check interface link state
ip link show
ethtool <interface>    # speed, duplex, link detected
```

### Layer 2 — Switching

```bash
# Check ARP table (confirm MAC resolved)
arp -a
ip neigh show

# Check interface is in correct VLAN
# On switch: show interface status, show vlan brief
```

### Layer 3 — IP / Routing

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

### Layer 4 — Transport

```bash
# Test specific TCP port
nc -zv <host> <port>
telnet <host> <port>
curl -v http://<host>:<port>/

# Check local firewall
iptables -L -n | grep <port>
firewall-cmd --list-all
```

## Path Tracing

```bash
traceroute <destination>    # Linux/Mac
tracert <destination>       # Windows
mtr <destination>           # continuous path trace
```

## Common Connectivity Tests

```bash
# ICMP ping
ping -c 4 <host>

# MTU test (verify no fragmentation)
ping -M do -s 1472 <host>    # Linux (1500 MTU = 1472 payload + 28 headers)
ping -f -l 1472 <host>       # Windows

# DNS and then connect
curl -v https://<fqdn>/
```

## Connectivity from Windows

```powershell
Test-NetConnection -ComputerName <host> -Port <port>
Test-NetConnection <host>    # ICMP test
Resolve-DnsName <host>
```

## Common Issues

| Layer | Issue | Check | Action |
|---|---|---|---|
| L1 | No link | `ethtool` | Check cable, SFP, port status |
| L2 | No ARP | `ip neigh` | Check VLAN, switch port config |
| L3 | No route | `ip route get` | Add route or fix gateway |
| L3 | Firewall blocking | Deny logs | Add firewall rule |
| L4 | Port blocked | `nc -zv` | Check host and network firewall |
