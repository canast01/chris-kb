---
tags:
  - networking
---
# NTP Firewall Rules

<div class="kb-summary">
NTP Firewall Rules reference covering Required Firewall Rules, Linux — firewalld, Linux — iptables, Windows Firewall, Cisco ASA / Firepower and 2 more sections.
</div>

NTP uses **UDP port 123** for all client-server and peer communication. If this port is blocked between a host and its NTP server, the clock will not synchronise.

```d2
direction: down

required_firewall_rules: "Required Firewall Rules" {shape: rectangle}
linux_firewalld: "Linux — firewalld" {shape: rectangle}
linux_iptables: "Linux — iptables" {shape: rectangle}
windows_firewall: "Windows Firewall" {shape: rectangle}
cisco_asa_firepower: "Cisco ASA / Firepower" {shape: rectangle}
testing_connectivity: "Testing Connectivity" {shape: rectangle}

required_firewall_rules -> linux_firewalld: uses
linux_firewalld -> linux_iptables: uses
linux_iptables -> windows_firewall: uses
windows_firewall -> cisco_asa_firepower: uses
cisco_asa_firepower -> testing_connectivity: uses
```

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


```text title="Expected output"
success
success
success
success
dhcpv6-client http https ntp ssh
rule family="ipv4" source address="10.0.0.0/8" service name="ntp" accept
```

!!! warning "Common errors"
    **`Error: INVALID_SERVICE: ntp not known to firewalld`** — Use `firewall-cmd --get-services | grep ntp` to verify the service name, or replace with the port directly using `--add-port=123/udp`.
    **`Error: COMMAND_FAILED: '/usr/sbin/firewalld' not running`** — Start the firewalld service with `systemctl start firewalld` before running firewall-cmd commands.
    **`Error: INVALID_RULE: rule family="ipv4" source address="10.0.0.0/8" service name="ntp" accept`** — Ensure the rich rule syntax is correct; use `firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" port protocol="udp" port="123" accept'` if the service name is not recognized.
## Linux — iptables

```bash
# Allow outbound NTP
iptables -A OUTPUT -p udp --dport 123 -j ACCEPT
iptables -A INPUT  -p udp --sport 123 -j ACCEPT

# Save
iptables-save > /etc/iptables/rules.v4
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`iptables: No chain/target/match by that name`** — Ensure the iptables kernel module is loaded with `modprobe iptables_filter` and that you have root privileges.
    **`bash: /etc/iptables/rules.v4: Permission denied`** — Run the entire script with `sudo` or ensure the `/etc/iptables/` directory is writable by the current user.
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the ACL syntax matches your device OS (Cisco ASA/IOS format shown); some platforms use different keywords like `allow` instead of `permit`.
    **`% Access list <name> not found`** — Ensure the access list name (e.g., `INSIDE_OUT`) exists before applying it to an interface with the `access-group` command.
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


```text title="Expected output"
ntpdate -q 203.0.113.45
server 203.0.113.45, stratum 2, offset 0.002341, delay 0.04532
45 Jan 12 14:23:18 ntpdate[2847]: adjust time server 203.0.113.45 offset 0.002341 sec

Starting Nmap 7.92 ( https://nmap.org ) at Wed Jan 12 14:23:45 2024
Nmap scan report for ntp.example.com (203.0.113.45)
Host is up (0.045s latency).
PORT    STATE SERVICE
123/udp open  ntp
Nmap done at Wed Jan 12 14:23:46 2024; 1 IP address (1 host up) scanned in 1.23s

Reference ID    : 198.51.100.10 (time.nist.gov)
Stratum         : 2
Ref time (UTC)  : Wed Jan 12 14:23:44 2024
System time     : 0.000234567 seconds slow of NTP time
Reachable

MS Name/IP Address         Stratum Poll Reach LastRx Last sample
===============================================================
^* 203.0.113.45             2      6   377   12    -234us[ -198us] +/-   45ms
^+ 198.51.100.22            2      6   377   18    +156us[ +201us] +/-   52ms
^- 192.0.2.88               3      6   377   22    +892us[ +934us] +/-   78ms

Every 10.0s: chronyc sources                                Wed Jan 12 14:23:55 2024
MS Name/IP Address         Stratum Poll Reach LastRx Last sample
===============================================================
^* 203.0.113.45             2      6   377   15    -198us[ -156us] +/-   45ms
^+ 198.51.100.22            2      6   377   21    +234us[ +289us] +/-   52ms
```

!!! warning "Common errors"
    **`ntpdate[2847]: no server suitable for synchronization found`** — Verify the NTP server IP is correct and reachable via `ping <ntp-server>`, then check firewall rules allow outbound UDP 123.
    **`Nmap scan report for ntp.example.com (203.0.113.45) | Host seems down | QUITTING!`** — Confirm the host is online with `ping` and that your network allows ICMP; use `nmap -Pn -sU -p 123 <ntp-server>` to skip ping checks.
    **`501 Not authorised`** — The NTP server may require authentication or have ACL restrictions; verify the server allows queries from your client IP using `ntpq -p <ntp-server>` instead.
## NTP Server Access Control (chrony)

If a host acts as an NTP server for other hosts, restrict which clients can query it:

```bash
# /etc/chrony.conf — on the NTP server
allow 10.0.0.0/8           # allow internal network
allow 192.168.0.0/16
deny all                   # deny everyone else
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`chrony.conf:2: Unknown command 'allow'`** — Ensure you're editing `/etc/chrony.conf` on a system with chrony installed; if using ntpd instead, use `restrict` directives in `/etc/ntp.conf` instead.
    **`Job for chrony.service failed because the control process exited with error code.`** — Run `chronyc waitsync` or `systemctl restart chrony` after editing to validate syntax; check `journalctl -u chrony -n 20` for the specific parsing error.