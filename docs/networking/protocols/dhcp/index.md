---
tags:
  - networking
description: "Dynamic Host Configuration Protocol (DHCP) automates IP address assignment using a four-step DORA handshake (Discover, Offer, Request, Ack) over UDP —..."
---
# DHCP

<div class="kb-summary">
Dynamic Host Configuration Protocol (DHCP) automates IP address assignment using a four-step DORA handshake (Discover, Offer, Request, Ack) over UDP — client broadcasts on port 68, server listens on port 67. The primary operational concerns are scope design, lease time tuning, option correctness (gateway, DNS, domain), and failover configuration for high availability, as DHCP failure renders an entire subnet unreachable without static fallback.
</div>

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="scopes/">
  <strong>Scopes</strong>
  <span>IP range configuration, subnet mask, exclusions, and scope activation across server implementations.</span>
</a>

<a class="kb-card" href="leases/">
  <strong>Leases</strong>
  <span>Lease duration recommendations, renewal (T1/T2) timers, lease database inspection, and pool exhaustion.</span>
</a>

<a class="kb-card" href="reservations/">
  <strong>Reservations</strong>
  <span>MAC-based IP reservations for servers, printers, and infrastructure — static assignment via DHCP.</span>
</a>

<a class="kb-card" href="options/">
  <strong>Options</strong>
  <span>Common DHCP options: option 3 (gateway), option 6 (DNS), option 15 (domain), option 66/67 (PXE boot).</span>
</a>

<a class="kb-card" href="failover/">
  <strong>Failover</strong>
  <span>Windows DHCP failover (hot-standby / load balance), ISC dhcpd failover, and Kea HA configuration.</span>
</a>

</div>

## Quick Reference

**DORA handshake:**

| Step | Direction | Description |
|---|---|---|
| Discover | Client → Broadcast (255.255.255.255) | Client searches for a DHCP server |
| Offer | Server → Client (broadcast or unicast) | Server proposes IP + lease terms |
| Request | Client → Broadcast | Client requests the offered IP |
| Ack | Server → Client | Server confirms; lease begins |

**Common DHCP options:**

| Option | Name | Example value |
|---|---|---|
| 1 | Subnet mask | 255.255.255.0 |
| 3 | Default gateway | 192.168.1.1 |
| 6 | DNS servers | 8.8.8.8, 8.8.4.4 |
| 15 | Domain name | corp.example.com |
| 51 | Lease time | 86400 (24 hours) |
| 66 | TFTP server | 192.168.1.10 |
| 67 | Bootfile name | pxelinux.0 |

**Lease time guidelines:**

| Environment | Recommended lease time |
|---|---|
| Servers / infrastructure | 8 days (long — reduces churn) |
| Workstations | 24 hours |
| Guest / public WiFi | 1–4 hours |
| High-density / transient | 30 minutes |

## Common Commands / Config

```bash
# Linux: View current DHCP lease details
cat /var/lib/dhclient/dhclient.leases
# or for systemd-networkd:
networkctl status

# Linux: Force DHCP renewal
dhclient -r eth0 && dhclient eth0
# or with NetworkManager:
nmcli con up <connection-name>

# View DHCP leases on ISC dhcpd server
cat /var/lib/dhcpd/dhcpd.leases

# Windows: View current IP configuration (shows lease expiry)
ipconfig /all

# Windows: Release and renew DHCP lease
ipconfig /release && ipconfig /renew

# Windows Server: List all DHCP scopes (PowerShell)
Get-DhcpServerv4Scope -ComputerName <dhcp-server>

# Windows Server: Show active leases in a scope
Get-DhcpServerv4Lease -ComputerName <dhcp-server> -ScopeId 192.168.1.0

# Windows Server: Add a reservation
Add-DhcpServerv4Reservation -ScopeId 192.168.1.0 `
  -IPAddress 192.168.1.50 -ClientId "AA-BB-CC-DD-EE-FF" `
  -Description "Printer-01"

# Check DHCP pool utilisation (Windows)
Get-DhcpServerv4ScopeStatistics -ComputerName <dhcp-server>
```


```text title="Expected output"
# Linux: View current DHCP lease details
lease {
  interface "eth0";
  fixed-address 192.168.1.105;
  option subnet-mask 255.255.255.0;
  option routers 192.168.1.1;
  option domain-name-servers 8.8.8.8,8.8.4.4;
  renew 4 2024/01/15 14:32:15;
  expire 4 2024/01/15 22:32:15;
}

# Linux: Force DHCP renewal
Listening on LPF/eth0/08:00:27:a4:c2:f1
Sending on   LPF/eth0/08:00:27:a4:c2:f1
Sending on   Socket/fallback
DHCPDISCOVER on eth0 to 255.255.255.255 port 67 interval 3
DHCPOFFER from 192.168.1.1
DHCPACK from 192.168.1.1
bound to 192.168.1.106 -- renewal in 28800 seconds.

# View DHCP leases on ISC dhcpd server
lease 192.168.1.50 {
  starts 1 2024/01/15 10:15:22;
  ends 1 2024/01/15 18:15:22;
  hardware ethernet aa:bb:cc:dd:ee:ff;
  uid "printer-01";
  set vendor-string "Canon-MF445dw";
  binding state active;
}

# Windows: View current IP configuration (shows lease expiry)
Ethernet adapter Ethernet:
   Connection-specific DNS Suffix: example.com
   IPv4 Address: 192.168.1.42
   Subnet Mask: 255.255.255.0
   Default Gateway: 192.168.1.1
   DHCP Server: 192.168.1.10
   Lease Obtained: Monday, January 15, 2024 10:15:22 AM
   Lease Expires: Monday, January 15, 2024 6:15:22 PM

# Windows: Release and renew DHCP lease
Successfully released the IPv4 address for adapter "Ethernet".
Successfully renewed the IPv4 address for adapter "Ethernet".

# Windows Server: List all DHCP scopes
ScopeId         : 192.168.1.0
Name            : Main-Office
SubnetMask      : 255.255.255.0
State            : Active
StartRange       : 192.168.1.100
EndRange         : 192.168.1.200
ActivationState  : True

# Windows Server: Show active leases in a scope
IPAddress        HostName         ClientID                    LeaseExpiryTime
---------        --------         --------                    ---------------
192.168.1.105    ws-dev-01        5254001234ab                1/15/2024 6:15:22 PM
192.168.1.110    printer-floor2   aabbccddeeff                1/15/2024 6:18:45 PM
192.168.1.115    iot-sensor-03    001a2b3c4d5e
```
**ISC dhcpd scope example (/etc/dhcp/dhcpd.conf):**
```bash
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.100 192.168.1.200;
  option routers 192.168.1.1;
  option domain-name-servers 192.168.1.10, 192.168.1.11;
  option domain-name "corp.example.com";
  default-lease-time 86400;
  max-lease-time 604800;
}
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `subnet declaration not terminated with semicolon` | Add a semicolon after the closing brace: `}` |
    | `unknown option domain-name-servers` | Use the correct DHCP option syntax `domain-name-servers` without hyphens in the value list, or verify the dhcpd.conf man page for your ISC DHCP version. |
## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Client gets APIPA address (169.254.x.x) | DHCP server unreachable; scope exhausted | Verify DHCP service is running; check scope pool utilisation; confirm L3 relay agent (ip helper-address) on router |
| Correct IP but wrong gateway/DNS | Option configuration on scope | Review scope options 3 and 6; check for server-level options overriding scope options |
| Lease pool exhausted | Lease database size; short lease times | Extend lease time; increase pool range; check for rogue devices; review lease database for stale entries |
| Duplicate IP address conflict | Reservation or static conflict | Exclude static IPs from scope range; verify no duplicate MAC reservations |
| DHCP failover replication broken | Partner server unreachable; clock skew | Check failover partner connectivity; sync time between servers; restart DHCP service |
| PXE boot fails at DHCP stage | Options 66/67 missing or wrong | Verify TFTP server IP (opt 66) and bootfile (opt 67); confirm scope is active on correct VLAN |
