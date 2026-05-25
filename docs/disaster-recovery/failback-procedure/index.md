# Disaster Recovery Failback Procedure

A controlled process for returning production workloads to the primary site after an outage has been resolved.
## Decision Gate — When to Failback

Before initiating failback, confirm:
- [ ] Primary site fully restored and tested (power, network, storage, compute)
- [ ] Root cause of original outage identified and resolved
- [ ] Management approval obtained
- [ ] Maintenance window or low-impact window planned
- [ ] All DR-site changes documented (data written to DR since failover)

> **Failback is not urgent.** Running stable on DR is better than a rushed failback that causes a second outage.

## Phase 1 — Prepare Primary Site

```bash
# Confirm primary storage arrays healthy
# ONTAP
system health status show
storage disk show -broken

# Pure FlashArray
purecli array get
purecli drive list | grep -v healthy

# Confirm primary SAN fabric healthy
show interface fc brief           # Cisco MDS
switchshow                        # Brocade
```
┌──────────────────────────────────────── DR Failback Procedure ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      DR Failback Procedure — reverse replicate, re-sync, validate, cut back to production     │   │
│   │                   See product-specific sub-sections for detailed procedures                   │   │
│   │          DR success depends on: documented runbooks · tested failover · validated RTO         │   │
│   │          Minimum DR posture: defined RPO/RTO · tested backups · known escalation path         │   │
│   │        Test DR procedures quarterly; document results; update runbooks after each test        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Production site · DR site · Replication link · Management network · Vault network                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO           = Recovery Point Objective; max acceptable data loss window                            │
│  RTO           = Recovery Time Objective; max acceptable downtime before restore                      │
│  Failover      = activating the DR site; redirecting hosts to replica resources                       │
│  Failback      = returning operations to production site after DR resolved                            │
│  Runbook       = step-by-step documented procedure for a specific DR scenario                         │
│  IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery                    │
│  Clean Room    = isolated vCenter + workstations for cyber recovery validation                        │
│  Air Gap       = network isolation preventing attacker lateral movement to vault                      │
│  DR Test       = planned failover test; validates RTO without real disaster                           │
│  Replication   = continuous or periodic data copy to secondary site or vault                          │
│  Recovery Tier = classification: hot/warm/cold based on RTO requirement                               │
│  BIA           = Business Impact Analysis; drives RPO/RTO targets per system                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**SRDF — restore R1 as source:**
```bash
# Restore normal direction after failover
symrdf -g <rdfgroup> restore -noprompt

# Confirm R1 is synchronized
symrdf -g <rdfgroup> query
```

**Veeam — run a final backup at DR before failback:**
1. Veeam Backup & Replication → Replication jobs → Run job
2. Confirm backup completes before proceeding

## Phase 3 — Plan the Cutover Window

- Agree on maintenance window with application owners
- Set DNS TTL to 60 seconds at least 1 hour before cutover
- Notify users of planned outage window
- Have rollback plan documented: if failback fails, return to DR

## Phase 4 — Initiate Failback

**Graceful shutdown at DR:**
```bash
systemctl stop <application-service>
# Confirm no active sessions
ss -tnp | grep <port>
```

**Wait for replication to catch up:**
```bash
# ONTAP — confirm lag is zero before breaking
snapmirror show -destination-path <primary-svm>:<primary-vol> -fields lag-time
# lag-time should be 00:00:00 or very small

# Break mirror — primary volume becomes writable
snapmirror break -destination-path <primary-svm>:<primary-vol>
```

**VMware SRM — reprotect and failback:**
1. Site Recovery → Recovery Plans → select plan
2. Click **Reprotect** (reverses protection direction)
3. After reprotect completes — **Run** → choose **Planned Migration**

**Manual VM failback (PowerCLI):**
```powershell
# Shut down VM at DR
Stop-VM -VM "<vm-name>" -Confirm:$false

# Power on at primary (VM should already be registered from original config)
Start-VM -VM "<vm-name>" -Server <primary-vcenter>
```

## Phase 5 — Post-Failback Validation

```bash
# Storage visible at primary hosts
multipath -ll
lsblk
df -h

# Application services
systemctl start <service>
systemctl status <service>

# Application health
curl -vk https://<primary-app-url>/health
```

**Database integrity check:**
```bash
# PostgreSQL
psql -U <user> -c "SELECT pg_database_size('<db>');"

# MSSQL (PowerShell)
Invoke-Sqlcmd -Query "DBCC CHECKDB('<db>') WITH NO_INFOMSGS" -ServerInstance <primary-sql>
```

## Phase 6 — Restore Normal Replication

Once primary is confirmed stable, re-establish replication from primary → DR:

```bash
# ONTAP — resync back to original direction
snapmirror resync -source-path <primary-svm>:<primary-vol> -destination-path <dr-svm>:<dr-vol>

# Confirm
snapmirror show -destination-path <dr-svm>:<dr-vol>
```

## Failback Checklist

- [ ] Primary site confirmed stable — hardware, network, storage
- [ ] Root cause resolved and documented
- [ ] Reverse replication running and lag within RPO
- [ ] Application gracefully stopped at DR
- [ ] Final sync completed (lag = 0)
- [ ] Mirror broken; primary volumes writable
- [ ] VMs powered on at primary
- [ ] Application responding at primary endpoints
- [ ] DNS reverted to primary IPs
- [ ] Monitoring reverted to primary targets
- [ ] Forward replication (primary → DR) re-established
- [ ] Incident ticket closed with full timeline and RTO/RPO met

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Replication lag won't close | Large data written at DR during outage | Plan longer sync window; extend maintenance window |
| Primary LUNs not visible | SAN zoning issue | Verify zones include primary HBAs; rescan |
| Application data inconsistency | DR writes not in sync | Check consistency group membership; investigate missing writes |
| DNS not resolving to primary | TTL still cached | Wait for TTL expiry or flush DNS |
| VMs won't start at primary | Snapshot/delta files from DR | Consolidate VM snapshots before failing back |
