# MDS — Common Issues

> Part of the [Cisco MDS](../../) reference.

---

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
