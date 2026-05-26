# NetBackup — Common Issues

> Part of the [NetBackup Troubleshooting](../index.md) reference.

---

## Common Issue Summary

| Symptom | Likely Cause | Action |
|---|---|---|
| Job fails with status 23 | Socket read/write error between master and client | Check network connectivity; verify `bpcd` running on client; check firewall on TCP 13782 |
| Job fails with status 59 | Access denied to client — host name mismatch | Verify `CLIENT_NAME` in `bp.conf` matches server's entry; check `hosts` resolution |
| Job fails with status 83 | Media write error | Check tape drive firmware; run `tpclean` if tape; inspect `bptm` logs for hardware errors |
| Job fails with status 96 | Unable to allocate new media for backup | Check available blank or appendable media; review volume pool assignments |
| Job fails with status 196 | Client backup was not attempted — window missed | Review schedule intervals and backup window settings; check if prior job held the window |
| Job fails with status 213 | No storage units available | Confirm STU is not offline; check media server connectivity; check disk STU free space |
| Catalog backup fails | NBU catalog path full or catalog corruption | Check `/usr/openv/netbackup/db` disk usage; run `bpdbm -consistency` check |
| Media server unreachable | `nbemm` communication failure | Run `nbemmcmd -listhosts`; check `bprd` and `nbemm` daemons; verify DNS resolution |
| Client connection timeout | `bpcd` not running or firewall blocking 13782/tcp | `bpps -a` on client to confirm daemons; telnet/nc test from master to client port 13782 |
| Deduplication ratio drops suddenly | Client-side dedup disabled or fingerprint DB issue | Check `msdp` logs; confirm `ENABLE_CLIENT_SIDE_DEDUP` in `bp.conf`; run `cacontrol --dsstat` |
| Restore job queued but never runs | No available restore window or resource conflict | Check `bprd` queue; confirm no `MAX_STREAMS_PER_DRIVE` saturation; check vault/duplication jobs |
| Drive reported DOWN in robot | Drive hardware error or path failover | Run `vmcheckxxx -rptdrv`; check `bptm` log; physically inspect SCSI/FC path |

---

## Backup Failures

### Status 23 — Socket read/write error

Status 23 occurs when the network connection between master and client is interrupted during job execution.

```bash
# Check bpcd is running on the client
bpps -a | grep bpcd

# Test connectivity from master to client on NetBackup port
telnet <client-hostname> 13782

# Review bpcd log on client
tail -200 /usr/openv/netbackup/logs/bpcd/log.<yyyymmdd>

# Review bpbrm log on master
tail -200 /usr/openv/netbackup/logs/bpbrm/log.<yyyymmdd>
```
```

Mismatches between DNS short name and FQDN are a common cause. Ensure `CLIENT_NAME` is set to exactly the name the master server uses.

### Status 83 — Media write error (tape)

```bash
# Check bptm log for hardware-level error detail
grep -i "error\|fail" /usr/openv/netbackup/logs/bptm/log.<yyyymmdd>

# Query drive status
vmquery -b -drive <drive-index>

# Clean drive if mount count threshold exceeded
tpclean -C <drive-name>
```

If errors persist after cleaning, engage tape vendor support and check robotic library firmware version.

### Status 96 — Unable to allocate new media

```bash
# List available scratch media
vmquery -b -r <robot-number> | grep -i "scratch\|blank"

# Check volume pool assignment for the policy
bppllist <policyname> -L | grep -i pool

# Move unassigned media to the correct scratch pool
vmchange -m <mediaid> -vp <volume-pool>
```

---

## Catalog Issues

### Catalog backup not completing

NetBackup catalog backup is the most critical job. If it has not run in the last 6 hours, investigate immediately.

```bash
# Check catalog backup job history
bplist -S <master-server> -policy NBU_Catalog -Listdead -d 01/01/1970 00:00:00

# Force an immediate catalog backup
bpbackup -p NBU_Catalog_Backup

# Check catalog database consistency
bpdbm -consistency -verbose
```

Catalog backup failures often indicate disk space issues under `/usr/openv/netbackup/db`. Check with `df -h` and clear old image files with `bpexpdate` if appropriate.

---

## Storage Unit Issues

### Disk STU full — new jobs queued but not running

```bash
# Check all STU free space
bpstulist -U

# Check disk pool usage (MSDP / AdvancedDisk)
nbdevquery -listdp -stype PureDisk -U

# Expire old images to reclaim space
bpexpdate -policy <policyname> -d 0 -backupid <backup-id>

# Run image cleanup to actually reclaim the space
bpimage -cleanup
```

---

## Deduplication (MSDP) Issues

### Deduplication ratio drops

```bash
# Check MSDP pool status
cacontrol --dsstat -d <msdp-path>

# Check fingerprint database health
cacontrol --dbstat

# Review dedupe log for anomalies
tail -500 /usr/openv/netbackup/logs/spoold/log.<yyyymmdd>
```

If `cacontrol --dbstat` reports database errors, do not run further jobs until the MSDP pool is recovered. Engage Veritas support with the `nbsupport` bundle.
