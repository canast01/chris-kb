# DHCP

<div class="kb-summary">
Dynamic Host Configuration Protocol (DHCP) automates IP address assignment using a four-step DORA handshake (Discover, Offer, Request, Ack) over UDP — client broadcasts on port 68, server listens on port 67. The primary operational concerns are scope design, lease time tuning, option correctness (gateway, DNS, domain), and failover configuration for high availability, as DHCP failure renders an entire subnet unreachable without static fallback.
</div>

        DORA HANDSHAKE
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Client (new device)              DHCP Server                                                         │
│  ┌───────────────────┐            ┌────────────────────────┐                                          │
│  │  No IP yet        │            │  Scope: 192.168.1.0/24 │                                          │
│  │                   │            │  Pool: .100 – .200     │                                          │
│  │  1. DISCOVER ─────┼────────────┼►  (broadcast)          │                                          │
│  │    src: 0.0.0.0   │            │  server receives       │                                          │
│  │    dst: broadcast │            │                        │                                          │
│  │                   │◄───────────┼── 2. OFFER             │                                          │
│  │                   │            │   "here's 192.168.1.105"│                                         │
│  │  3. REQUEST ──────┼────────────┼►  (broadcast)          │                                          │
│  │    "I want .105"  │            │   server confirms lease │                                         │
│  │                   │◄───────────┼── 4. ACK               │                                          │
│  │  IP: 192.168.1.105│            │   lease begins         │                                          │
│  │  GW: 192.168.1.1  │            │   options delivered    │                                          │
│  │  DNS: 10.0.0.53   │            └────────────────────────┘                                          │
│  └───────────────────┘                                                                                │
│  Renewal at 50% of lease time (T1); rebind at 87.5% (T2)                                              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Client gets APIPA address (169.254.x.x) | DHCP server unreachable; scope exhausted | Verify DHCP service is running; check scope pool utilisation; confirm L3 relay agent (ip helper-address) on router |
| Correct IP but wrong gateway/DNS | Option configuration on scope | Review scope options 3 and 6; check for server-level options overriding scope options |
| Lease pool exhausted | Lease database size; short lease times | Extend lease time; increase pool range; check for rogue devices; review lease database for stale entries |
| Duplicate IP address conflict | Reservation or static conflict | Exclude static IPs from scope range; verify no duplicate MAC reservations |
| DHCP failover replication broken | Partner server unreachable; clock skew | Check failover partner connectivity; sync time between servers; restart DHCP service |
| PXE boot fails at DHCP stage | Options 66/67 missing or wrong | Verify TFTP server IP (opt 66) and bootfile (opt 67); confirm scope is active on correct VLAN |
