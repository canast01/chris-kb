# Time Synchronization

```
┌──────────────────────────────────────────────────────────────────────┐
│                      NTP Hierarchy                                   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │  Stratum 1: Internet / GPS NTP Sources                      │     │
│  │  pool.ntp.org · time.cloudflare.com · time.google.com       │     │
│  └──────────────────────────┬───────────────────────────────────┘    │
│                             │  sync (UDP :123)                       │
│  ┌──────────────────────────▼───────────────────────────────────┐    │
│  │  Stratum 2: Internal NTP Servers (2× for redundancy)         │    │
│  │  ntp1.corp.example.com · ntp2.corp.example.com               │    │
│  │  Domain Controllers (Windows AD authoritative time source)   │    │
│  └─────┬──────────────────────┬────────────────────────────────┘     │
│        │  sync                │                                      │
│  ┌─────▼────────┐   ┌─────────▼──────────────────────────────────┐   │
│  │ Linux hosts  │   │  All Infrastructure Clients                │   │
│  │ ESXi hosts   │   │  Switches · Firewalls · Appliances         │   │
│  │ (chrony)     │   │  Windows Servers (w32tm) · VMs             │   │
│  └──────────────┘   └────────────────────────────────────────────┘   │
│                                                                      │
│  Target drift: < 1ms (infra)  ·  Kerberos tolerance: < 5 min         │
└──────────────────────────────────────────────────────────────────────┘
```

Ensure consistent, accurate time across all infrastructure systems. Time drift causes Kerberos authentication failures, TLS errors, log correlation issues, and replication problems.
## chrony (Recommended — RHEL 7+, Ubuntu 18.04+)

```bash
# Status overview
chronyc tracking

# Output fields:
# System time: offset from NTP source (target < 1ms for most infra)
# Leap status: Normal (not adjusting)
# Reference ID: current time source in use

# Show NTP sources and reach/offset
chronyc sources -v

# Force immediate sync
chronyc makestep

# Show recent drift history
chronyc tracking | grep -E "offset|frequency|drift"
```

### chrony Configuration

```conf
# /etc/chrony.conf

# Internal NTP servers (preferred)
server ntp1.corp.example.com iburst prefer
server ntp2.corp.example.com iburst

# Fallback to public NTP pool
pool pool.ntp.org iburst

# Allow only local subnet to query this server (if acting as NTP relay)
allow 10.0.0.0/8

# Log drift
driftfile /var/lib/chrony/drift
rtcsync
makestep 1.0 3
```

```bash
systemctl enable --now chronyd
chronyc waitsync 10  # wait up to 10 polls for sync
```

## ntpd (Legacy)

```bash
# Status
ntpq -p          # show peers and offsets
ntpq -c rv       # show system variables including offset and jitter
timedatectl      # OS-level time status

# Force sync (ntpdate, legacy one-shot)
ntpdate -u pool.ntp.org

# Restart ntpd
systemctl restart ntpd
```

## systemd-timesyncd (Lightweight — Ubuntu default)

```bash
# Status
timedatectl status
timedatectl show-timesync

# Configuration
# /etc/systemd/timesyncd.conf
[Time]
NTP=ntp1.corp.example.com ntp2.corp.example.com
FallbackNTP=pool.ntp.org
RootDistanceMaxSec=5
PollIntervalMinSec=32
PollIntervalMaxSec=2048

systemctl restart systemd-timesyncd
timedatectl set-ntp true
```

## Windows Time Service (w32tm)

```powershell
# Check sync status
w32tm /query /status
w32tm /query /peers

# Force resync
w32tm /resync /force

# Configure NTP source (on domain member — should use DC)
# Members sync from DC automatically; configure DC:
w32tm /config /manualpeerlist:"ntp1.corp.example.com,0x8 ntp2.corp.example.com,0x8" /syncfromflags:manual /reliable:yes /update
net stop w32tm && net start w32tm

# Diagnose
w32tm /stripchart /computer:<ntp-server> /dataonly /samples:5
```

## Monitoring Time Drift

```bash
# Prometheus node_exporter exposes:
# node_timex_offset_seconds — current NTP offset (alert if > 1s)
# node_timex_sync_status — 1 = synced, 0 = not synced

# Alert rule example (Prometheus)
# - alert: NTPNotSynchronised
#   expr: node_timex_sync_status != 1
#   for: 5m

# Quick check across multiple hosts
for h in web-01 web-02 db-01; do
  echo -n "$h: "; ssh $h "chronyc tracking | grep 'System time'"
done
```

## NTP Hierarchy for On-Premises

```
Internet NTP (pool.ntp.org, time.cloudflare.com)
        ↓
  Internal NTP relay servers (2× for redundancy)
        ↓
  All servers, VMs, network devices
```

- Domain Controllers should be configured as authoritative time sources for Windows AD environments
- Linux hosts should point at internal NTP relays (not public NTP directly, to avoid firewall issues)
- Network devices (switches, routers) should sync from same internal NTP sources

## Time Zone Management

```bash
# Set system timezone (Linux)
timedatectl set-timezone Europe/London
timedatectl set-timezone UTC    # preferred for servers

# Verify
date
timedatectl status

# Windows
Set-TimeZone -Id "GMT Standard Time"
Get-TimeZone
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Kerberos auth failing | Time drift > 5 min from DC | `chronyc makestep`; check NTP sources |
| chronyc shows no sources | Firewall blocking UDP 123? | Allow UDP 123 to NTP servers; restart chronyd |
| Large offset but not correcting | `makestep` not in chrony.conf | Add `makestep 1.0 3`; restart chronyd |
| w32tm shows no sync | NTP service not running? Firewall? | `net start w32tm`; check `w32tm /query /peers` |
| Log timestamps inconsistent across hosts | Multiple NTP sources / drift | Standardise to same NTP hierarchy; force sync |
| `timedatectl` shows `NTP service: inactive` | systemd-timesyncd disabled | `timedatectl set-ntp true` |
