---
tags:
  - netbackup
  - operations
---
# NetBackup — Procedures


<div class="kb-summary">
Procedures reference covering Backup Policies.

*Applies to: NetBackup 10.x*
</div>

```text
┌─────────────────────────────────────── NetBackup — Procedures ────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Routine Procedures              │  │                DR Procedures                │   │
│   │          Add new protection source           │  │              Initiate failover              │   │
│   │           Modify retention policy            │  │               Validate replica              │   │
│   │          Expire old recover points           │  │              Redirect host I/O              │   │
│   │             Add storage capacity             │  │         Test failover (non-disrupt)         │   │
│   │           Service account rotation           │  │            Failback to production           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           Change Control Requirements for NetBackup                           │   │
│   │           All changes to protection policies require change ticket with rollback plan         │   │
│   │                      Failover tests must be scheduled in maintenance window                   │   │
│   │              Firmware/software upgrades need 48 h pre-approval and backup snapshot            │   │
│   │                  Post-change: verify jobs run successfully for 2 backup cycles                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection             │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master Server = central controller: scheduler, catalog, job manager, policy engine                   │
│  Media Server  = data mover between client and storage; can be co-located with master                 │
│  MSDP          = Media Server Deduplication Pool; inline variable-length block dedup                  │
│  Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot                    │
│  Policy        = defines what, when, and where to back up; contains schedules and clients             │
│  Schedule      = full / differential-incremental / cumulative-incremental timing within policy        │
│  Retention     = how long an image is kept; set per schedule, enforced by catalog expiry              │
│  Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config             │
│  NBU CA        = auto-issued certificate authority; signs host IDs for secure comms                   │
│  vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556           │
│  bpdbjobs      = CLI to query job history: status, duration, exit code, errors                        │
│  bplist        = CLI to list available backup images for a client, policy, or date range              │
│  KMS           = Key Management Service for encryption keys used in backup data encryption            │
│  NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Backup Policies

Use this section for practical NetBackup Policies notes, checks, troubleshooting, commands, change notes, and field references.

### Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

### Useful commands

Add tested commands here.

### Known issues

Add known issues here as they come up.

## Run an Ad-Hoc Backup

`bpbackup -p <policy> -s <schedule> -c <client>` or Admin Console → Client Backups → Manual Backup.

```bash
bpbackup -p <policy> -s <schedule> -c <client>
```

## Restore Files (bprestore)

`bprestore -C <client> -p <policy> -s <schedule> -t <start-time> -T <end-time> <file-list>` — restores to original path.

```bash
bprestore -C <client> -p <policy> -s <schedule> -t <start-time> -T <end-time> <file-list>
```

## Check Job Status

`bpdbjobs -summary` for counts; `bpdbjobs -jobid <id> -L` for detail; `bperror -backstat -hoursago 24` for errors.

```bash
bpdbjobs -summary
bpdbjobs -jobid <id> -L
bperror -backstat -hoursago 24
```

## Expire a Backup Image

`bpexpdate -backupid <id> -d 0` — marks image expired; storage reclaimed at next image cleanup.

```bash
bpexpdate -backupid <id> -d 0
```

## Import a Backup from Tape (Catalog Recovery)

`bpimport -create_db_info -Bidfile <bidfile>` — imports catalog info from tape without restoring data.

```bash
bpimport -create_db_info -Bidfile <bidfile>
```

## Manage Tape Media

`vmupdate -rt TLD -rn <drive>` — update tape inventory; `vmchange -res <media-id>` — move media between pools.

```bash
# Update tape inventory
vmupdate -rt TLD -rn <drive>

# Move media between pools
vmchange -res <media-id>
```

## Configure a New Policy

`bppolicynew <policy-name>` → `bpplclients -add <client> <hardware> <OS> <policy>` → `bpplsched -add <policy> <sched-type>`.

```bash
bppolicynew <policy-name>
bpplclients -add <client> <hardware> <OS> <policy>
bpplsched -add <policy> <sched-type>
```

## Check MSDP Dedup Pool Health

`nbdevquery -listdp -U` — check used/free capacity and dedup ratio; `crcontrol --dsstat` — dedup store detail.

```bash
nbdevquery -listdp -U
crcontrol --dsstat
```

## Collect Debug Logs for Support

`vxlogcfg -a -p 51216 -o 6 && nbpemreq -due` — enable verbose logging; `tar czf /tmp/nbu-logs.tgz /usr/openv/netbackup/logs/` — collect.

```bash
vxlogcfg -a -p 51216 -o 6 && nbpemreq -due
tar czf /tmp/nbu-logs.tgz /usr/openv/netbackup/logs/
```
