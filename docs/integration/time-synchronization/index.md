# Integration — Time Synchronization (NTP)

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

```text
┌────────────────────────────── Integration — Time Synchronization (NTP) ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Accurate time is critical: Kerberos (5 min skew max), TLS certs, log correlation       │   │
│   │        Hierarchy: external NTP (stratum 1/2) → internal NTP servers → all infra clients       │   │
│   │        Alert: offset > 100ms; drift > 50ms/s; stratum 16 = unsynchronised = investigate       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  NTP Config                  │  │               Troubleshooting               │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           Linux: /etc/chrony.conf            │  │          chronyc tracking (offset)          │   │
│   │            Windows: w32tm /config            │  │              timedatectl status             │   │
│   │            ESXi: host NTP config             │  │             w32tm /query /status            │   │
│   │         Appliance: NTP server in UI          │  │             Stratum 16 = no sync            │   │
│   │           Firewall: UDP 123 to NTP           │  │            Check FW UDP 123 open            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Stratum      = Distance from reference clock; 0 = atomic; infra uses stratum 2-3                   │
│    Offset       = Difference between client time and server time; < 100ms is normal                   │
│    Drift        = Rate at which clock gains/loses time; chrony compensates automatically              │
│    Stratum 16   = NTP "not synchronised" state; Kerberos will fail within 5 min                       │
│    chronyc      = Chrony client tool; tracking, sources, makestep commands                            │
│    w32tm        = Windows NTP tool; /query /status shows source, stratum, offset                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
```text
Internet NTP (pool.ntp.org, time.cloudflare.com)
        ↓
  Internal NTP relay servers (2× for redundancy)
        ↓
  All servers, VMs, network devices
```
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
