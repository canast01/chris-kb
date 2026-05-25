# MDS — Health Checks

> Part of the [Cisco MDS](../../index.md) reference.

---

## Daily Checks

Run these checks at the start of each shift or as part of a morning SAN review. The goal is to catch degraded states (a port down, a missing FLOGI entry, a failed PSU) before they become incidents.

| Check | Command | Expected Result |
|---|---|---|
| FC interface states | `show interface brief` | All connected ports in `up` state; no `errDisabled` or unexpected `down` |
| FLOGI database | `show flogi database` | All expected host HBAs and storage target ports present |
| Fabric topology | `show topology` | ISL links up; no unexpected topology changes |
| Active zoneset | `show zoneset active vsan all` | Active zoneset name and member count match expected |
| Recent syslog | `show logging last 50` | No `critical` or `error`-level entries in the last window |
| Hardware health | `show environment` | PSUs, fans, and temperature sensors all reporting normal |
| NX-OS version consistency | `show version` | All switches in the fabric on the same approved NX-OS release |
| NDFC / DCNM alarms | NDFC dashboard | No active fabric alarms or topology anomalies |

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

---

## Interpreting Key Outputs

### show interface brief

Each FC interface appears as a line with state, VSAN, mode, speed, and connected port FCID.

```
fc1/1    10     up      F      32000   auto  on   0x010200
fc1/2    10     up      F      32000   auto  on   0x010400
fc1/3    --     down    --     --      auto  --   --
fc1/5    10     trunking TE    32000   auto  on   --
```

| State | Meaning | Action |
|---|---|---|
| `up` | Port is active and a device is logged in | Normal |
| `down` | No signal — cable, SFP, or peer issue | Investigate SFP and cable; check peer switch port |
| `errDisabled` | Port was disabled due to an error condition | Check `show interface fc<x/y>` for reason; flap the port after resolving |
| `trunking` | TE port ISL is up and carrying VSANs | Normal for ISL ports |
| `isolated` | VSAN isolated — usually a VSAN merge conflict | Check `show vsan` and trunk allowed VSANs |

### show flogi database

```
show flogi database vsan 10

---------------------------------------------------------------------------
INTERFACE        VSAN    FCID           PORT NAME               NODE NAME
---------------------------------------------------------------------------
fc1/1            10    0x010200  21:00:00:24:ff:a1:b2:c3  20:00:00:24:ff:a1:b2:c3
fc1/2            10    0x010400  21:00:00:24:ff:d4:e5:f6  20:00:00:24:ff:d4:e5:f6
fc1/8            10    0x010600  52:4a:93:7c:00:00:00:01  52:4a:93:7c:00:00:00:00
```

Compare the list against the expected device register (CMDB or SAN design spreadsheet). A host HBA or storage target missing from this output is a fault condition.

### show environment

```
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

Any `Failed`, `Absent`, or `Minor/Major` temperature alerts require immediate investigation.

---

## Weekly Checks

In addition to daily checks, perform these weekly:

- [ ] **Port error counters**: `show interface fc<x/y> counters errors` on all active ports — flag any non-zero CRC, link-failure, or loss-of-sync counters since last clear
- [ ] **VSAN membership audit**: `show vsan membership` — confirm no ports in unexpected VSANs
- [ ] **Device alias consistency**: `show device-alias database` — confirm all aliases are current and match CMDB
- [ ] **Zone database diff**: compare `show zone vsan <id>` output against change tickets to ensure only authorised zones exist
- [ ] **ISL utilisation**: review NDFC performance graphs for ISL bandwidth — flag any ISL at > 70% sustained utilisation
- [ ] **Trunk allowed VSANs**: `show trunk` — confirm only intended VSANs are allowed on each ISL trunk

```bash
# Weekly additions to daily sweep
show interface fc1/1 counters errors   # repeat per port
show vsan membership
show device-alias database
show zone vsan 10
show trunk
show port-channel summary
```

---

## Monthly Checks

- [ ] **NX-OS version vs. Cisco recommended**: cross-reference `show version` against Cisco's current recommended MDS NX-OS release for the platform
- [ ] **SmartNet / maintenance contract expiry**: verify switches are covered in contract management system
- [ ] **EPLD version**: `show version module all` — confirm EPLD versions are current for the NX-OS release in use
- [ ] **AAA / TACACS+ reachability**: `test aaa group tacacs+ <test-user> <test-pass>` — confirm AAA is functioning
- [ ] **SNMP trap receiver**: confirm trap receiver in NDFC / NMS is receiving traps from all MDS switches
- [ ] **Configuration backup**: verify automated backup job ran successfully for the previous 30 days; spot-check at least two backup files

---

## Health Check Script (Quick Reference)

The following command sequence captures all key health state in a single SSH session. Redirect to a file for archival.

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

For automated health checks, see the [Scripts](../scripts/index.md) page for the `mds_fabric_health.sh` and `mds_daily_check.sh` scripts.

---

## Alarm Thresholds

Use these thresholds to determine severity when evaluating check results:

| Metric | Warning | Critical |
|---|---|---|
| FC interfaces down | 1 or more | 5 or more |
| FLOGI entries below baseline | > 5% fewer than expected | > 20% fewer |
| ISL utilisation | > 70% sustained | > 90% sustained |
| CPU utilisation | > 60% | > 80% |
| Environmental alerts | Minor threshold | Major threshold or fan/PSU failure |
| Log error rate | 1–5 errors in window | > 5 errors or any `critical`-level entry |

---

## Pre-Change Baseline

Before any change (zoning update, firmware upgrade, port move), capture a full baseline:

```bash
show version
show running-config
show interface brief
show flogi database
show zoneset active vsan all
show environment
show logging last 50
```

Save this output to the change ticket. It becomes the reference for post-change validation and rollback evidence.
