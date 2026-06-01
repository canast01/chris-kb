# NTP Validation


<div class="kb-summary">
NTP Validation reference covering Validation Checklist, Validation Commands, Post-Config Convergence, Validating NTP on Multiple Hosts, Common Validation Failures.
</div>

```text
        VALIDATION CHECKLIST
┌──────────────────────────────────────────────────────────────┐
│  chronyc tracking                                            │
│  ├── Leap status: Normal            ✓ (not synchronised = ✗) │
│  ├── Stratum: 2–4                   ✓ (16 = no source = ✗)  │
│  ├── System time: < 100ms           ✓ (> 1s = risk)         │
│  └── Last offset: < 10ms            ✓                        │
│                                                              │
│  chronyc sources -v                                          │
│  ├── At least one source with *     ✓ (all ? = blocked)     │
│  └── Reach = 377                    ✓ (< 377 = packet loss)  │
│                                                              │
│  ntpdate -q <server>                                         │
│  └── Returns offset + delay         ✓ (timeout = UDP blocked)│
│                                                              │
│  PASS criteria:                                              │
│  offset < 128ms, stratum ≤ 3, reach = 377, Leap = Normal    │
└──────────────────────────────────────────────────────────────┘
```

Use these checks after configuring NTP on a new system, after a maintenance window, or when time-sensitive services (Kerberos, TLS, log correlation) report failures.

## Validation Checklist

| Check | Command | Pass Criteria |
|---|---|---|
| Sync state | `chronyc tracking` | Leap status: Normal |
| Offset | `chronyc tracking` | System time < 100ms from NTP |
| Sources reachable | `chronyc sources` | At least one source marked `*` |
| Reach register | `chronyc sources` | Reach = `377` (all polls received) |
| Stratum | `chronyc tracking` | Stratum 2–4 |
| No firewall block | `ntpdate -q <server>` | Returns offset and delay |

## Validation Commands

### Linux — chrony

```bash
# Full sync summary
chronyc tracking

# Source states (* = selected, + = acceptable, ? = unreachable)
chronyc sources -v

# Detailed per-source statistics
chronyc sourcestats -v

# Watch sync converge (useful after first config)
watch -n 5 'chronyc tracking | grep -E "System time|Stratum|Leap"'

# Check daemon is running
systemctl is-active chronyd
```

### Linux — systemd-timesyncd

```bash
timedatectl status
timedatectl show-timesync --all
```

### Windows

```powershell
# Sync status
w32tm /query /status

# Peer information
w32tm /query /peers

# Force resync and verify
w32tm /resync /force
w32tm /query /status | Select-String "Source|Stratum|Last Successful"
```

### Network Devices

```bash
# Cisco IOS
show ntp status          # synchronized: yes
show ntp associations    # peer table with offsets

# Arista EOS
show ntp status
show ntp associations

# Expected: "system clock is synchronized"
```

## Post-Config Convergence

After adding NTP sources, allow up to 5 minutes for chrony to:
1. Poll sources (`iburst` accelerates this to ~2 minutes)
2. Build offset history
3. Select the best source
4. Slew or step the clock

Force immediate convergence:

```bash
# Immediate step if offset is large
chronyc makestep

# Then verify
chronyc tracking | grep "System time"
```

## Validating NTP on Multiple Hosts

```bash
# Quick check across inventory via Ansible
ansible all -i inventory/production/ -m command \
  -a "chronyc tracking | grep -E 'Leap|System time|Stratum'"

# Or via SSH loop
for host in server{01..10}.example.com; do
  echo -n "$host: "
  ssh "$host" "chronyc tracking | grep 'Leap status'"
done
```

## Common Validation Failures

| Failure | Cause | Fix |
|---|---|---|
| `Not synchronised` | No sources reachable | Check firewall (UDP 123), source IPs |
| Offset > 1 second | Clock drifted heavily or stepped | `chronyc makestep` then monitor |
| Stratum 16 | No upstream source | chronyd running but all sources failed |
| Reach not `377` | Packet loss to NTP server | Check network path, DNS resolution of server name |
| Kerberos failure after fix | System clock now correct but Kerberos tickets old | `klist -k` / `kinit` to refresh |
