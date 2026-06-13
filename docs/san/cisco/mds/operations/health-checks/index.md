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
```text
┌─────────────────────────────────── Cisco MDS 9000 — Health Checks ────────────────────────────────────┐
│                                                                                                       │
│  MDS health: show system, show interface, VSAN state, ISL utilisation, zone sync.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Hardware Health                │  │          Fabric Connectivity Health         │   │
│   │          show system health: all OK          │  │            show vsan: all active            │   │
│   │          show environment: temp/PSU          │  │          show interface trunk: ISL          │   │
│   │           show module: all online            │  │          show port-channel: member          │   │
│   │         show version: correct NX-OS          │  │          show flogi database: count         │   │
│   │         show redundancy: sup active          │  │           ISL util < 70% sustained          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  show system health and show environment cover hardware; VSAN/ISL cover fabric.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Port & Zone Health              │  │              Performance Health             │   │
│   │         show interface fc: no errors         │  │           show analytics ITL flow           │   │
│   │         CRC errors: 0 per day target         │  │            show interface counter           │   │
│   │          show zone active: matches           │  │          BB credits: no starvation          │   │
│   │         show device-alias: no stale          │  │            SFP optical: > -3 dBm            │   │
│   │         CFS: zone in sync on all sw          │  │            Latency < 1ms per ITL            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS director chassis · supervisor module · line card blades · SFP transceivers                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  show system health= NX-OS; overall switch health including modules and fabric                        │
│  show environment = NX-OS; temperature, fan RPM, and PSU voltage readings                             │
│  show module      = NX-OS; line card / supervisor status and operational state                        │
│  show redundancy  = supervisor HA state; active + standby both must be present                        │
│  show flogi database= FC login database; count should match expected device list                      │
│  show interface fc= per-port counters: CRC, loss-of-sync, credit starvation                           │
│  show zone active = active zone set members per VSAN; verify correct aliases                          │
│  show device-alias= CFS-distributed device alias database; check for orphans                          │
│  CRC errors       = Cyclic Redundancy Check; non-zero = bad SFP or cable                              │
│  BB credits       = Buffer-to-Buffer credits; zero = port paused; check starvation                    │
│  SFP optical      = signal power in dBm; < -3 dBm indicates degraded transceiver                      │
│  show analytics   = MDS 9700 ITL flow analytics: IOPS, throughput, latency                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
