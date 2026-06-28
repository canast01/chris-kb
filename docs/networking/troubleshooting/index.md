---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
---
# Networking — Troubleshooting

<div class="kb-summary">
Networking troubleshooting — Layer 1-3 diagnostics, DNS/DHCP failures, routing issues, VLAN misconfigurations, and connectivity tools.
</div>

```bash
nslookup <hostname>
dig <hostname>
dig <hostname> @<dns_server_ip>    # query a specific server directly
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
<a class="kb-card" href="dns-resolution/"><strong>DNS Resolution Failures</strong><span>DNS resolution failure diagnosis — resolver, zone, and client-side troubleshooting steps.</span></a>
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
protocol_symptom_index: "Protocol Symptom Index" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> protocol_symptom_index: investigate
protocol_symptom_index -> resolution
```

## Protocol Symptom Index

| Symptom | Protocol | First command |
|---|---|---|
| Name resolution fails | DNS | `dig @<server> A hostname` |
| Kerberos auth fails | DNS / Kerberos | `dcdiag /test:dns`, check NTP sync |
| TLS handshake fails | TLS | `openssl s_client -connect host:443` |
| Certificate not trusted | TLS/PKI | `openssl verify -CAfile ca.crt cert.crt` |
| LDAP bind fails | LDAP | `ldapsearch -H ldap://dc -x -b "dc=corp,dc=local"` |
| FC port not online | Fibre Channel | `fcinfo hba-port`, `show interface fc` |
| iSCSI target unreachable | iSCSI | `iscsiadm -m discovery`, check port 3260 |
| NTP time drift | NTP | `timedatectl status`, `ntpq -pn` |
