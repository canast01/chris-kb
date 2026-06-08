# NTP Sources


<div class="kb-summary">
NTP Sources reference covering Stratum Hierarchy, Viewing Sources — chrony (Linux), Source Statistics, Configuring Sources (chrony), Windows — w32tm Source Config and 2 more sections.
</div>

        SOURCE SELECTION AND PREFERENCE
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  /etc/chrony.conf                                                                                     │
│  server ntp1.example.com iburst prefer  ◄── primary                                                   │
│  server ntp2.example.com iburst         ◄── acceptable alt                                            │
│  server ntp3.example.com iburst         ◄── third source                                              │
│                                                                                                       │
│  chronyc sources -v                                                                                   │
│  ┌────┬─────────────────────┬───────┬──────┬───────────┐                                              │
│  │ MS │ Name/IP             │Stratum│Reach │ Offset    │                                              │
│  ├────┼─────────────────────┼───────┼──────┼───────────┤                                              │
│  │ ^* │ ntp1.example.com    │  2    │ 377  │ -1.2ms    │   │ ◄ selected
│  │ ^+ │ ntp2.example.com    │  2    │ 377  │ +0.3ms    │   │ ◄ acceptable
│  │ ^- │ ntp3.example.com    │  3    │ 377  │ +2.1ms    │   │ ◄ excluded
│  │ ^? │ ntp4.example.com    │  -    │  17  │   -       │   │ ◄ unreachable
│  └────┴─────────────────────┴───────┴──────┴───────────┘                                              │
│  Minimum 3 sources required for reliable clock selection                                              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

An NTP source is a time server that the local daemon polls to correct the system clock. Source quality determines how accurate the local clock can be.

## Stratum Hierarchy

```text
Stratum 0 — atomic clock / GPS receiver (hardware reference)
Stratum 1 — directly connected to stratum 0 (public NTP servers)
Stratum 2 — synced from stratum 1 (most enterprise NTP servers)
Stratum 3 — synced from stratum 2 (internal hosts syncing from internal NTP)
```

Production servers should sync to internal stratum 2 servers. Stratum 10+ or `unsynchronised` is a problem.

## Viewing Sources — chrony (Linux)

```bash
# Source list with reach, offset, and jitter
chronyc sources -v

# Output interpretation:
# M — mode: * = current best, + = acceptable, - = excluded, ? = not reached
# Name/IP — source address
# Stratum — source stratum
# Poll — current poll interval (log2 seconds)
# Reach — 8-bit shift register (377 = all 8 polls reached)
# Last Rx — seconds since last sample
# Last sample — offset and error estimate
```

```text
MS Name/IP address         Stratum Poll Reach Last Rx Last sample
==================================================================
^* ntp1.example.com              2   6   377    23   -1.2ms[  -1.1ms] +/- 4.5ms
^+ ntp2.example.com              2   6   377    24   +0.3ms[  +0.3ms] +/- 6.1ms
^- ntp3.example.com              3   6   377    25   +2.1ms[  +2.1ms] +/- 9.0ms
```

| Symbol | Meaning |
|---|---|
| `*` | Currently selected source |
| `+` | Acceptable alternative (will be used if `*` fails) |
| `-` | Discarded by the selection algorithm |
| `?` | Source not reachable |
| `x` | Falseticker (clock appears wrong) |

## Source Statistics

```bash
# Per-source frequency offset and jitter history
chronyc sourcestats -v

# Show reference ID and source details
chronyc tracking
```

## Configuring Sources (chrony)

```bash
# /etc/chrony.conf
server ntp1.example.com iburst prefer
server ntp2.example.com iburst
server ntp3.example.com iburst

# iburst — sends 4 packets immediately on startup for faster initial sync
# prefer — prefer this source over others of similar quality
# minpoll/maxpoll — override default polling interval (log2 seconds)
server ntp1.example.com iburst minpoll 4 maxpoll 8

# Reload without restarting
chronyc reload sources
```

## Windows — w32tm Source Config

```powershell
# Set NTP sources
w32tm /config /manualpeerlist:"ntp1.example.com,0x8 ntp2.example.com,0x8" \
  /syncfromflags:manual /update

# Show current peers and their offsets
w32tm /query /peers

# Force sync
w32tm /resync /force
```

## Cisco / Arista Sources

```bash
# Cisco IOS
ntp server ntp1.example.com prefer
ntp server ntp2.example.com

show ntp associations     # sync status per peer
show ntp status           # current stratum and sync state

# Arista EOS
ntp server ntp1.example.com prefer
ntp server ntp2.example.com

show ntp status
show ntp associations
```

## Common Source Issues

| Symptom | Cause | Check |
|---|---|---|
| All sources `?` | UDP 123 blocked | Firewall rules; `nc -u <ntp-ip> 123` |
| `x` (falseticker) | Source clock is wrong | Remove source; investigate server |
| Reach not `377` | Intermittent packet loss | Check network path to NTP server |
| Only one source available | Other sources unreachable | Ensure minimum 3 sources for proper selection |
