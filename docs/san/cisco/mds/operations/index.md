# Operations

> Part of the [Cisco MDS](../) reference.

---

## Daily Checks

- [ ] Run `show interface brief` — confirm all FC interfaces are in connected/up state, flag any that are down or errDisabled
- [ ] Run `show flogi database` — verify all expected hosts and storage devices have logged in, note any missing entries
- [ ] Run `show topology` — confirm fabric topology matches expected, no unexpected ISL changes
- [ ] Run `show zoneset active vsan all` — verify active zone configuration matches expected across all VSANs
- [ ] Run `show logging last 50` — review recent syslog entries for critical or error-level messages
- [ ] Run `show environment` — confirm power supplies, fans, and temperature sensors are all normal
- [ ] Run `show version` — verify NX-OS version is consistent across all switches in the fabric
- [ ] Check Nexus Dashboard or DCNM for any active alarms or fabric health events

## Health Check

- [ ] All FC interfaces in connected/up state: `show interface brief`
- [ ] FLOGI database complete — all hosts and storage present: `show flogi database`
- [ ] Active zoneset matches expected per VSAN: `show zoneset active vsan all`
- [ ] No critical or error syslog messages: `show logging last 50`
- [ ] Power, fans, and temperature all normal: `show environment`
- [ ] No active alarms in Nexus Dashboard / DCNM
- [ ] ISL trunk membership correct: `show trunk`
- [ ] NX-OS version consistent across fabric members: `show version`

```bash
# Full MDS health sweep
show interface brief
show flogi database
show zoneset active vsan all
show logging last 50
show environment
show trunk
show version
```

## Change Readiness

- [ ] Configuration backup taken: `show running-config` output saved to jump host
- [ ] Both fabrics (Fabric A and Fabric B) are healthy before touching either
- [ ] VSAN configuration documented: all VSANs, membership, and active zonesets recorded
- [ ] Zoning change reviewed and approved — peer review of zone diff completed
- [ ] `show flogi database` baselined: full list of logins captured before change
- [ ] Maintenance window approved and communicated to affected storage and compute teams
- [ ] Rollback plan confirmed: procedure to restore zone config or revert VSAN change documented

| Item | Status | Notes |
|---|---|---|
| Running config backup | | `show running-config` to jump host |
| Both fabrics healthy | | `show interface brief` on all switches |
| VSAN config documented | | VSAN-to-port mapping recorded |
| Zone diff peer-reviewed | | Ticket reference |
| Change window approved | | Ticket reference |

## Incident Triage

- [ ] Run `show interface brief` — identify any down or errDisabled FC interfaces
- [ ] Run `show flogi database` — check for missing host or storage device logins
- [ ] Run `show logging last 50` — look for error messages, timestamps, and interface identifiers
- [ ] Run `show environment` — check for hardware faults: PSU failure, fan failure, overtemperature
- [ ] Run `show zoneset active vsan <id>` — verify zoning is not the cause of connectivity loss
- [ ] Check ISL state: `show interface fc<x/y>` on suspected ISL ports
- [ ] Run `show flogi database vsan <id>` — scope FLOGI check to affected VSAN
- [ ] Escalate to Cisco TAC if hardware fault confirmed or interface stays errDisabled after flap

| Question | Answer |
|---|---|
| Which interfaces are down or errDisabled? | `show interface brief` |
| Are all hosts and storage devices logged in? | `show flogi database` |
| What does the syslog show? | `show logging last 50` — error-level entries |
| Is there a hardware fault? | `show environment` — PSU, fan, temp |
| Is zoning blocking connectivity? | `show zoneset active vsan <id>` |

## Maintenance Window

1. Confirm both fabrics are healthy: `show interface brief` and `show flogi database` on all switches
2. Take configuration backup: `copy running-config startup-config` and save `show running-config` to jump host
3. Notify storage and compute teams that Fabric A (or B) will be affected
4. Perform the change on one fabric only — leave the other fabric carrying full host I/O
5. After change, run `show interface brief`, `show flogi database`, and `show zoneset active vsan all` to confirm state
6. Validate host multipath paths are still active via host-side tools
7. Review `show logging last 50` for any errors introduced by the change
8. Repeat procedure on second fabric only after first fabric is fully validated and hosts confirmed healthy

## Post-Change Validation

- [ ] All FC interfaces back in connected/up state: `show interface brief`
- [ ] FLOGI database complete — all hosts and storage logged in: `show flogi database`
- [ ] Active zoneset matches expected post-change config: `show zoneset active vsan all`
- [ ] No new error or critical syslog entries since change: `show logging last 50`
- [ ] Environment still healthy — no new hardware alerts: `show environment`
- [ ] Running config saved to startup config: `copy running-config startup-config`
- [ ] Host multipath paths active and balanced (confirmed via host-side tool)
- [ ] Close change ticket with validation evidence attached
