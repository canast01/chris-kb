# Data Domain — Common Issues


<div class="kb-summary">
Common Issues reference covering Issue Reference, Error Code Reference, Replication Lag — Step-by-Step Investigation.
</div>

## Issue Reference

| Symptom | Likely Cause | First Action |
|---|---|---|
| Dedup ratio dropped significantly | Encrypted or compressed source data; new data type ingested; DD Boost source-side dedup disabled | `filesys show compression` — identify which MTree changed; check backup software settings |
| Replication context stuck in `Replicating` or falling behind | Network bandwidth saturation; high ingest on source; target filesystem full | `replication status` for lag; `filesys show space` on target; check network with `net show stats` |
| NFS/CIFS mount failure | Export/share removed or IP restriction changed; network routing issue | `nfs show exports` / `cifs show shares`; verify client IP in access list; check `net show all` |
| VTL tape import failure | VTL slot configuration mismatch; FC path not zoned | `vtl show slots`; check FC zoning from backup media server to DD VTL ports |
| Filesystem nearly full (above 90%) | Cleaning not running; rapid data growth; expired data not deleted by backup software | `filesys show space`; check `filesys clean status`; run `filesys clean start` if not already running |
| DDBoost client authentication error | Expired or mismatched DD Boost credentials | Re-register storage unit in backup software; verify with `ddboost show clients` |
| `filesys status` shows disabled | Filesystem did not auto-start after reboot; hardware fault | `filesys enable`; check `alerts show current` for hardware errors |
| Disk in `Absent` or `Failed` state | Physical disk failure or loose connection | `disk show state`; open Dell support case for disk replacement |
| Low restore throughput from DD | Filesystem cleaning running during restore window; fragmentation | `filesys clean status`; stop clean if running: `filesys clean stop`; retry restore |
| Replication authentication failure | DD certificates expired or mismatched between source and target | `replication show` for error message; `adminaccess certificate show`; reissue certificates |
| CloudIQ showing array offline | SCG connectivity lost or SCG service down | Check SCG appliance; verify `autosupport status` on DD; check `net show all` for SCG reachability |
| Autosupport fails to send | Network path to Dell support blocked; proxy required | `autosupport test`; check firewall rules for outbound HTTPS; configure proxy if needed |

## Error Code Reference

| Error | Meaning | Action |
|---|---|---|
| `REPL-ERR-001` | Replication context authentication failure | Recheck DD Boost or replication user credentials on both ends |
| `DDFS-ERR-FULL` | Filesystem at or above hard capacity limit | Emergency clean; delete expired backups; add capacity |
| `HW-DISK-FAIL` | Physical disk failure detected | Do not delay — open Dell support case immediately; check `disk show state` |
| `BOOST-ERR-AUTH` | DD Boost client authentication rejected | Re-register storage unit; verify DD Boost user in backup software |
| `NTP-DRIFT` | NTP clock drift exceeds threshold | `ntp sync`; verify NTP server reachability |

## Replication Lag — Step-by-Step Investigation

1. Run `replication status` — note `Pre-Comp Remaining`, `Throughput`, and `Estimated Completion`
2. If throughput is low, run `net show stats` — check for packet loss or interface errors
3. Run `filesys show space` on the **target** DD — confirm it is not full
4. Check if source ingest rate is higher than replication can drain: `filesys show compression` shows recent write rate
5. If bandwidth is limited, adjust throttle: `replication throttle set <schedule> <bandwidth-kbps>`
6. If the context shows `Error` state: `replication show errors` — review the specific error code
7. For persistent errors, disable and re-enable the replication context:

```bash
replication disable <context>
replication enable <context>
```
```
┌─────────────────────────────────── Dell Data Domain Common Issues ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Top issues: filesystem full, replication broken, restore slow, backup job failures      │   │
│   │           Most root-cause to space exhaustion, network issues, or credential expiry           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Space Issues        │  │      Replication Issues     │  │        Backup/Restore       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        FS > 80% full        │  │        Context broken       │  │         Backup fails        │   │
│   │       Cleaning not run      │  │        Lag > 4 hours        │  │         Restore slow        │   │
│   │       MTree quota hit       │  │         Auth failure        │  │       Cannot mount NFS      │   │
│   │       No space for rep      │  │     Network packet drop     │  │       Boost conn fail       │   │
│   │       Cloud tier fail       │  │        WAN bandwidth        │  │        Corrupt backup       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │     Problem      │   First check    │        Fix        │      Verify      │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     FS full      │filesys show space│   Expire backups  │   Space freed    │  No space freed  │   │
│   │    Rep broken    │ replication show │   resync context  │    Lag drops     │ Persistent break │   │
│   │   Backup fail    │ Backup app logs  │   Check DD space  │   Job succeeds   │  Hardware fault  │   │
│   │   Slow restore   │ Disk show state  │    Check disks    │     Speed OK     │   NVRAM fault    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Context broken   = Replication context in error state; typically network or auth failure           │
│    replication resync= Re-establish broken replication context without full reinitialisation          │
│    Expire backups   = Delete old backup images via backup application; cleaning then frees space      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
