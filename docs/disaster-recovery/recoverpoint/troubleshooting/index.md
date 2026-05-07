# RecoverPoint — Troubleshooting

```mermaid
flowchart LR
    RecoverPoint["RecoverPoint"]
    RecoverPoint --> S0["Common Issues"]
    RecoverPoint --> S1["Log Locations"]
    RecoverPoint --> S2["Support Bundle Collection"]
```

## Common Issues

### CG in Error State

**Symptoms:** CG status shows `Error` or `Communication Problem` in the RecoverPoint Management Application (RPMA).

**Diagnostic Steps:**

```bash
# Via boxmgmt SSH to RPA
boxmgmt cg check_cg <CG-name>
boxmgmt list cg
boxmgmt system status
```

**Common causes:**

| Cause | Resolution |
|---|---|
| Journal volume full | Expand journal LUN or reduce retention window |
| WAN link down | Restore connectivity; RP will resume replication automatically once link recovers |
| Splitter communication failure | See Splitter section below |
| RPA node offline | Check RPA cluster health; redistribute CGs if node is failed |
| Storage path failure | Verify zoning and array paths to journal volumes |

---

### Journal Overflow

**Symptoms:** CG RPO alarm triggered; journal shows > 90% utilization.

```bash
boxmgmt journal list
boxmgmt journal status <journal-name>
```

**Resolution:**
1. Identify which CG is generating excess writes
2. Expand journal volume (can be done non-disruptively on most arrays)
3. If link is down and journal is exhausted, a full resync may be required after link restoration
4. Review if RPO target is realistic for the write rate

---

### Splitter Communication Failure

**Symptoms:** CG shows `Splitter connection problem`; writes may be blocked or split-brain situation.

**PowerMax hardware splitter:**
```bash
# On PowerMax (via Solutions Enabler / SYMCLI)
symrdf -sid <SID> list

# Check splitter registration in RP
boxmgmt splitter list
boxmgmt splitter status <splitter-name>
```

**RP4VM software splitter (ESXi):**
- Check ESXi host kernel module: `esxcli software vib list | grep rp`
- Restart splitter on ESXi if needed (requires brief I/O pause — schedule maintenance)

---

### RPO Violation

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

### Failover Did Not Complete Cleanly

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

### Link Down / WAN Outage

**During outage:**
- CGs accumulate in journal at production site
- Monitor journal capacity; alert if > 70%
- No action needed if journal has capacity; RP resumes automatically when link restores

**After link restores:**
- Monitor resync rate and lag reduction
- Verify RPO returns to compliance within expected window
- Check for any CGs that failed to resume automatically

## Log Locations

| Log | Location |
|---|---|
| RPA system logs | Accessible via `boxmgmt` → `Support` → `Collect support bundle` |
| RPMA audit log | RecoverPoint Management Application → Reports → Audit Log |
| Splitter logs (ESXi) | `/var/log/vmkernel.log` on ESXi host |

## Support Bundle Collection

```bash
# Via boxmgmt
boxmgmt support collect_bundle
```

Upload bundle to Dell Support case via https://www.dell.com/support.
