---
tags:
  - netbackup
  - troubleshooting
search:
  boost: 1.5
---
# NetBackup — Common Issues

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

```bash
# Check catalog backup job history
bplist -S <master-server> -policy NBU_Catalog -Listdead -d 01/01/1970 00:00:00

# Force an immediate catalog backup
bpbackup -p NBU_Catalog_Backup

# Check catalog database consistency
bpdbm -consistency -verbose
```
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
```bash
# Check MSDP pool status
cacontrol --dsstat -d <msdp-path>

# Check fingerprint database health
cacontrol --dbstat

# Review dedupe log for anomalies
tail -500 /usr/openv/netbackup/logs/spoold/log.<yyyymmdd>
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
A: "Status 25 — client connect refused" {shape: rectangle}
B: "Media manager volume busy" {shape: rectangle}
C: "Catalog backup failed" {shape: rectangle}
D: "Policy class mismatch" {shape: rectangle}
E: "Master / media server connectivity loss" {shape: rectangle}
A1: "A1" {shape: rectangle}
A2: "Start bpcd and verify port 13782 open — see Before you begin" {shape: rectangle}
A3: "Check bpbrm and bpcd logs for TLS or host ID error" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "Check ltid process and tpconfig -d — see Before you begin" {shape: rectangle}
B3: "Check for volume in use by another job; wait or cancel conflicting job" {shape: rectangle}
C1: "C1" {shape: rectangle}
C2: "Check MSDP pool and STU free space — see Before you begin" {shape: rectangle}
C3: "Run bpdbm -consistency and force catalog backup with bpbackup" {shape: rectangle}
D1: "D1" {shape: rectangle}
D2: "Correct policy type in NetBackup console to match client OS" {shape: rectangle}
D3: "Check schedule type and retention level for the policy" {shape: rectangle}
E1: "E1" {shape: rectangle}
E2: "Restart NetBackup services on master and check firewall rules" {shape: rectangle}
E3: "Check NBU CA host ID certificate validity on media server" {shape: rectangle}

S -> A
S -> B
S -> C
S -> D
S -> E
A1 -> A2
A1 -> A3
B1 -> B2
B1 -> B3
C1 -> C2
C1 -> C3
D1 -> D2
D1 -> D3
E1 -> E2
E1 -> E3
```

---

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Netbackup — Diagnostics](../diagnostics/)
- [Netbackup — Escalation](../escalation/)
- [Netbackup — Health Checks](../../operations/health-checks/)
