# RecoverPoint — Common Issues


<div class="kb-summary">
> Part of the [RecoverPoint](../../index.md) > [Troubleshooting](../index.md) reference.
</div>

---

## CG in Error State

**Symptoms:** CG status shows `Error` or `Communication Problem` in the RecoverPoint Management Application (RPMA).

**Diagnostic Steps:**

```bash
# Via boxmgmt SSH to RPA
boxmgmt cg check_cg <CG-name>
boxmgmt list cg
boxmgmt system status
```
```
┌──────────────────────────────────── RecoverPoint — Common Issues ─────────────────────────────────────┐
│                                                                                                       │
│   │     Symptom      │   Likely Cause   │    First Check    │       Fix        │      Verify      │   │
│   │     High lag     │  WAN congestion  │ get compression s │throttle or upgra │   get all rpas   │   │
│   │   CG suspended   │   journal full   │ check journal cap │expand journal vo │  get journal st  │   │
│   │ Splitter offline │ESXi host restart │ vSphere events lo │re-register split │  get splitter i  │   │
│   │   Image stuck    │stale image acces │ image access disa │  force release   │  get all groups  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     General Triage Pattern                                    │   │
│   │          Is the issue new or recurring? New = recent change; Recurring = config problem       │   │
│   │             Is it isolated to one source or all? Isolated = agent; All = server/repo          │   │
│   │                          Check logs first: image access enable/disable                        │   │
│   │                    If unresolved in 2h: open vendor case with full log bundle                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites           │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication          │
│  Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA                  │
│  Journal       = write-order-consistent storage capturing all writes for point-in-time access         │
│  Consistency Group= set of volumes protected together; writes are applied in order across all         │
│  Bookmark      = named marker in journal; enables deterministic recovery to a known state             │
│  Image Access  = mounting a journal point-in-time image to a host for testing or recovery             │
│  Failover      = activating the replica at the recovery site; breaks replication relationship         │
│  Test Copy     = non-disruptive image access for validation without breaking replication              │
│  RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero          │
│  RTO           = Recovery Time Objective; time from failover to service restored                      │
│  Reverse       = after failover, replicates from recovery site back to re-sync production             │
│  Splitter Lag  = delay between host write and journal commit; monitor for replication health          │
│  CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps          │
│  Distributed CG= consistency group spanning volumes on multiple storage arrays                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

**RP4VM software splitter (ESXi):**
- Check ESXi host kernel module: `esxcli software vib list | grep rp`
- Restart splitter on ESXi if needed (requires brief I/O pause — schedule maintenance)

---

## RPO Violation

**Symptoms:** RPO alarm fires; CG reports lag exceeding threshold.

**Diagnostic Steps:**
1. Check WAN link utilization — is bandwidth saturated?
2. Check write rate increase (application change or batch job)
3. Verify RPA cluster load — distribute CGs if one RPA is overloaded
4. Review journal state for overflow

```bash
boxmgmt cg check_cg <CG-name>
boxmgmt system performance
```

---

## Failover Did Not Complete Cleanly

**Symptoms:** After a failover, CG is stuck in `Failover in progress` or production site does not become accessible on DR.

**Steps:**
1. Verify all journal data has been applied at DR site
2. Check image access logs in RPMA
3. If failover is incomplete, use `Enable Image Access` manually for the desired recovery point
4. After application validation, use `Recover Production` to complete the failover

```bash
boxmgmt cg enable_image_access <CG-name> <copy-name>
boxmgmt cg recover_production <CG-name>
```

**If re-sync is required after failover:**
- Use `Direct Access` mode to start recovery, then initiate resync back to production

---

## Link Down / WAN Outage

**During outage:**
- CGs accumulate in journal at production site
- Monitor journal capacity; alert if > 70%
- No action needed if journal has capacity; RP resumes automatically when link restores

**After link restores:**
- Monitor resync rate and lag reduction
- Verify RPO returns to compliance within expected window
- Check for any CGs that failed to resume automatically
