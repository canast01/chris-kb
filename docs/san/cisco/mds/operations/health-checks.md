---
tags:
  - operations
  - san
---
# Cisco MDS 9000 — Health Checks

```bash
# Full daily health sweep — run on each MDS switch
show interface brief
show flogi database
show topology
show zoneset active vsan all
show logging last 50
show environment
show version
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. `show system health` — verify **pass** for all subsystem checks; any fail requires investigation before proceeding
2. `show module` — confirm all supervisor and line card modules show **Ok**; degraded or powered-down modules need immediate attention
3. `show vsan` — verify all expected VSANs are **active** and contain member ports; suspended VSANs indicate fabric issue
4. `show interface fc brief` — all in-use ports should be **connected** in F-port or trunk mode; down ports need investigation
5. `show zoneset active vsan <id>` — confirm the correct zone set name is activated per VSAN; verify member count matches expected
6. `show interface fc brief` — check Rx and Tx counters column for non-zero CRC or link-reset values; replace cable or SFP if non-zero
7. `show flogi database vsan <id>` — verify all expected host HBAs and storage array ports are present; missing entries indicate login failure
8. `show interface fc <isl-port> counters` — review ISL error counters for CRC, loss-of-sync, or credit starvation; repeat for each ISL port

```text
show environment

Fan:
   Fan Model          Fan State    Airflow
   ----------------   ----------   -------
   Fan Module 1       Ok           front-to-back

Temperature:
   Module   Sensor        MajorThresh   MinorThresh   CurTemp   Status
   ------   --------      -----------   -----------   -------   ------
   1        Inlet         75            70             28        Ok

Power Supply:
   PS  Model                 Input Current  Output Current  Status
   --  --------------------  -------------  --------------  ------
   1   DS-CAC-3000W          OK             OK              Ok
   2   DS-CAC-3000W          OK             OK              Ok
```
```bash
# Weekly additions to daily sweep
show interface fc1/1 counters errors   # repeat per port
show vsan membership
show device-alias database
show zone vsan 10
show trunk
show port-channel summary
```
```bash
show version
show module
show environment
show interface brief
show flogi database
show vsan
show vsan membership
show trunk
show port-channel summary
show zoneset active vsan all
show zone status vsan 10
show logging last 50
show system resources
show fcdomain domain-list vsan 10
```
```bash
show version
show running-config
show interface brief
show flogi database
show zoneset active vsan all
show environment
show logging last 50
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Mds — Procedures](../procedures/)
- [Mds — CLI Reference](../cli-reference/)
- [Mds — Common Issues](../../troubleshooting/common-issues/)
