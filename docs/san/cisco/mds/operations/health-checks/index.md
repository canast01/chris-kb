# MDS — Health Checks

> Part of the [Cisco MDS](../../) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Run `show interface brief` | `show interface brief` | confirm all FC interfaces are in connected/up state, flag any that are down or errDisabled |
| [ ] Run `show flogi database` | `show flogi database` | verify all expected hosts and storage devices have logged in, note any missing entries |
| [ ] Run `show topology` | `show topology` | confirm fabric topology matches expected, no unexpected ISL changes |
| [ ] Run `show zoneset active vsan all` | `show zoneset active vsan all` | verify active zone configuration matches expected across all VSANs |
| [ ] Run `show logging last 50` | `show logging last 50` | review recent syslog entries for critical or error-level messages |
| [ ] Run `show environment` | `show environment` | confirm power supplies, fans, and temperature sensors are all normal |
| [ ] Run `show version` | `show version` | verify NX-OS version is consistent across all switches in the fabric |
| [ ] Check Nexus Dashboard or DCNM for any active alarms or fabric heal |  |  |

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
