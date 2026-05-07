# RecoverPoint — Journals

> Part of the [RecoverPoint](../) reference.

---

## Overview

The RecoverPoint journal is a rolling delta store that records every write made to protected volumes. It enables recovery to any point in time within the journal window. Each copy (production, DR, local) has its own dedicated journal volumes.

| Concept | Description |
|---|---|
| Journal Window | How far back in time you can recover; determined by journal size and write rate |
| Journal Drain | The process of applying journal data to the DR copy during replication |
| Journal Overflow | When write rate exceeds journal drain rate and the journal fills to capacity |
| Bookmark | A named point-in-time marker stored in the journal |

---

## Viewing Journal State

```bash
# SSH to RPA cluster
ssh admin@<rpa-cluster-ip>

# List all journals with utilization and status
journals list

# Detailed journal information for a specific CG
journal status --gname <cg_name>

# REST API — journal volumes per CG copy
RP="https://<rpa-ip>/fapi/rest/5_1"
AUTH="-u admin:password --insecure"

curl -s $AUTH "$RP/group/all_groups_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for g in data.get('innerSet', []):
    for copy in g.get('groupCopies', {}).get('innerSet', []):
        jvols = len(copy.get('journalVolumeList', {}).get('innerSet', []))
        print(f\"CG={g['name']:30s}  copy={copy.get('name','?'):15s}  journal_vols={jvols}\")
"
```

---

## Journal Sizing Guidelines

Journal size determines the recovery window. Size based on the average write rate and required retention.

```
Journal size (GB) = Write rate (MB/s) x 3600 x Retention hours / 1024

Example:
  Write rate: 50 MB/s
  Retention:  4 hours
  Journal size = 50 x 3600 x 4 / 1024 = ~703 GB

Minimum recommended: 10x hourly write rate
```

| Environment Write Rate | Minimum Journal Size | Recommended Retention |
|---|---|---|
| < 10 MB/s | 50 GB | 8 hours |
| 10–50 MB/s | 200–750 GB | 4–8 hours |
| 50–200 MB/s | 750 GB – 3 TB | 2–4 hours |
| > 200 MB/s | Size per calculation | Consult RecoverPoint sizing guide |

---

## Expanding a Journal

Journal volumes can be expanded non-disruptively on most arrays.

```bash
# Step 1 — Identify which journal needs expansion
journals list

# Step 2 — Expand the journal LUN on the storage array
# (PowerMax example via SYMCLI)
symdev -sid <SID> modify <dev_id> -cap <new_size_gb> -captype gb

# Step 3 — Rescan the journal volume in RecoverPoint
# Via RPMA: Group Management → <CG> → Volumes → Rescan

# Step 4 — Confirm expanded capacity
journal status --gname <cg_name>
```

---

## Journal Overflow Response

If a journal reaches 100%, replication halts and the CG enters an error state. A full resync will be required.

```bash
# Check which CG has a full journal
journals list | grep -i "100\|full\|overflow"

# Immediate triage — check link state (overflow may be caused by link down)
links statistics

# Check CG state
group status --gname <cg_name>

# If link is down: restore connectivity — RP will resume draining the journal automatically
# If link is up and journal is > 90%: expand journal immediately (see above)

# If journal overflowed and CG is in error — force full resync after journal is expanded
group start-resync --gname <cg_name>
```

---

## Journal Monitoring Thresholds

Set alerts at the RPMA level and forward events to SIEM via syslog.

| Threshold | Action |
|---|---|
| > 70% | Warning alert; review write rate and link bandwidth |
| > 80% | Critical alert; plan immediate journal expansion |
| > 90% | Emergency; expand journal before replication halts |
| 100% | Replication halted; full resync required after expansion |

```bash
# Set journal alarm threshold (via RPMA / boxmgmt)
# Navigate: Group Management → <CG> → Settings → Journal Alarms
# Set high-watermark threshold to 70%
```
