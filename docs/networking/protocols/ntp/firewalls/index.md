---
tags:
  - networking
---
# NTP Firewall Rules


<div class="kb-summary">
NTP Firewall Rules reference covering Required Firewall Rules, Linux — firewalld, Linux — iptables, Windows Firewall, Cisco ASA / Firepower and 2 more sections.
</div>

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  NTP CLIENT (server/device)                                                                           │
│  ┌──────────────┐   UDP 123 outbound    ┌──────────────────┐                                          │
│  │  Client host │ ─────────────────────►│  NTP Server      │                                          │
│  │  (chrony/    │                       │  (stratum 2)     │                                          │
│  │   w32tm)     │◄──────────────────────│                  │                                          │
│  └──────────────┘   UDP 123 response    └──────────────────┘                                          │
│                     (src port 123)                                                                    │
│  Stateful firewall: return traffic handled automatically                                              │
│  Stateless ACL: must permit both directions explicitly                                                │
│                                                                                                       │
│  NTP SERVER (serving clients):                                                                        │
│  ┌──────────────┐   UDP 123 inbound     ┌──────────────────┐                                          │
│  │  NTP Server  │◄──────────────────────│  Clients         │                                          │
│  │  (chrony     │ ─────────────────────►│                  │                                          │
│  │  allow 10/8) │   UDP 123 response    └──────────────────┘                                          │
│  └──────────────┘                                                                                     │
│                                                                                                       │
│  Rule summary:  permit udp any → ntpserver port 123                                                   │
│                 permit udp ntpserver port 123 → any                                                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

NTP uses **UDP port 123** for all client-server and peer communication. If this port is blocked between a host and its NTP server, the clock will not synchronise.

## Required Firewall Rules

| Direction | Source | Destination | Port | Protocol |
|---|---|---|---|---|
| Outbound | All servers | NTP server(s) | 123 | UDP |
| Inbound (on NTP server) | All clients | NTP server | 123 | UDP |
| Inbound response | NTP server | Client (ephemeral port) | 123 | UDP |

NTP responses use UDP source port 123. Stateful firewalls handle the return traffic automatically. Stateless ACLs need both directions explicit.

## Linux — firewalld

```bash
# Allow NTP client (outbound to NTP servers)
firewall-cmd --permanent --add-service=ntp
firewall-cmd --reload

# If the host IS an NTP server — allow clients to reach it
firewall-cmd --permanent --add-service=ntp
firewall-cmd --reload

# Restrict NTP access to specific source network
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" service name="ntp" accept'
firewall-cmd --reload

# Verify
firewall-cmd --list-services
firewall-cmd --list-rich-rules
```

## Linux — iptables

```bash
# Allow outbound NTP
iptables -A OUTPUT -p udp --dport 123 -j ACCEPT
iptables -A INPUT  -p udp --sport 123 -j ACCEPT

# Save
iptables-save > /etc/iptables/rules.v4
```

## Windows Firewall

```powershell
# Allow outbound NTP (client)
New-NetFirewallRule -DisplayName "NTP Outbound" -Direction Outbound `
  -Protocol UDP -RemotePort 123 -Action Allow

# Allow inbound NTP (if this server serves time to others)
New-NetFirewallRule -DisplayName "NTP Inbound" -Direction Inbound `
  -Protocol UDP -LocalPort 123 -Action Allow
```

## Cisco ASA / Firepower

```bash
# Outbound NTP from inside
access-list INSIDE_OUT extended permit udp any host <ntp-server> eq 123

# Inbound response (stateful — handled automatically by connection tracking)
# If stateless — also permit:
access-list OUTSIDE_IN extended permit udp host <ntp-server> eq 123 any
```

## Testing Connectivity

```bash
# Test UDP 123 reachability (requires ntpdate or nmap)
ntpdate -q <ntp-server>       # query without adjusting clock

# Using nmap
nmap -sU -p 123 <ntp-server>

# Direct NTP packet probe
chronyc -h <ntp-server> tracking 2>/dev/null && echo "Reachable"

# Check current sources — ? means blocked
chronyc sources | grep "?"

# Watch source reach register — should reach 377 if packets are getting through
watch -n 10 'chronyc sources'
```

## NTP Server Access Control (chrony)

If a host acts as an NTP server for other hosts, restrict which clients can query it:

```bash
# /etc/chrony.conf — on the NTP server
allow 10.0.0.0/8           # allow internal network
allow 192.168.0.0/16
deny all                   # deny everyone else
```
