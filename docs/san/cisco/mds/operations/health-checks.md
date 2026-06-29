---
tags:
  - operations
  - san
---
# Cisco MDS 9000 — Health Checks

*Applies to: Cisco MDS / NX-OS*

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

```d2
direction: right

run_this_routine: "Run This Routine" {shape: rectangle}
verify: "Verify" {shape: rectangle}

run_this_routine -> verify
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

```text title="Expected output"
Interface fc1/1 Counters (Errors):
  CRC Errors                    : 0
  Enc Out                       : 0
  Enc In                        : 0
  Too Many BB Transitions       : 0
  Invalid Transmission Word     : 0
  Link Failures                 : 0
  Loss of Sync                  : 2
  Loss of Signal                : 0
  Primitive Seq Protocol Errors : 0
  Invalid Ordered Sets          : 0

VSAN Membership:
  VSAN 1: fc1/1, fc1/2, fc1/3, fc1/4, fc1/5
  VSAN 10: fc2/1, fc2/2, fc2/3, fc2/4
  VSAN 20: fc3/1, fc3/2

Device Alias Database:
  Alias Name: prod-san-01
    Device WWN: 50:00:14:40:5a:2b:c1:e0
  Alias Name: prod-san-02
    Device WWN: 50:00:14:40:5a:2b:c1:f5
  Alias Name: backup-array
    Device WWN: 50:00:09:73:a2:1c:d4:22

Zone Information for VSAN 10:
  Zone: zone-prod-db
    Members: prod-san-01, prod-san-02, host-server-04
  Zone: zone-backup
    Members: backup-array, host-server-05

Trunk Information:
  Trunk Index: 1
    Master Interface: fc1/1
    Trunk Members: fc1/1, fc1/2, fc1/3, fc1/4
    Trunk Mode: ON

Port-Channel Summary:
  Number of port-channels: 2
  Port-Channel 1:
    Status: UP
    Members: fc1/1(OK), fc1/2(OK), fc1/3(OK), fc1/4(OK)
  Port-Channel 2:
    Status: UP
    Members: fc2/1(OK), fc2/2(OK)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the exact interface name with `show interface brief` and use the correct format (e.g., `fc1/1` not `Fc1/1`).
    **`% VSAN does not exist`** — Confirm the VSAN ID exists with `show vsan` before querying its membership or zones.
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

```text title="Expected output"
Cisco MDS 9148S (1 Slot) Chassis ("MDS 9100")
Device ID:abc1234567890def  Serial Number: ABC123456789
Model Number                    : N9K-C9148S-FM
System uptime is 45 days 3 hours 2 minutes

Mod Ports Card Type                    Model              Serial No.
--- ----- -------------------------------------- ------------------- -----------
1   48    1/10G Fibre Channel Module              N9K-M12PQ           JAE12345678

System Temperature: 38 C (Normal)
PS1(RSP): 12V output Normal, Temp 35 C
PS2(RSP): 12V output Normal, Temp 36 C
Fan 1: Normal, Fan 2: Normal

Interface  Vsan  Admin Status  Oper Status  Speed  Type
fc1/1      1     up            up           16G    N_Port
fc1/2      1     up            up           16G    N_Port
fc1/3      10    up            up           16G    N_Port
fc1/4      10    up            down         16G    N_Port
...

FLOGI Database for Vsan 1:
 FCID        Port Name               Node Name              IP Address
 0x010001    50:00:14:40:12:34:56:78 50:00:14:40:12:34:56:79 192.168.1.100

VSAN ID  VSAN Name  State  Default Zoning
1        VSAN0001   active permit
10       VSAN0010   active permit
20       VSAN0020   active permit

VSAN ID  Interop Mode  FC Mode  Enabled
1        default       native   yes
10       default       native   yes

Trunk Mode Enabled

Port-Channel  Ports
1             fc1/1, fc1/2, fc1/3

Active Zoneset: ZoneSet_Prod
 Zone: Zone_Storage (VSAN 10)
  [pwwn] 50:00:14:40:12:34:56:78
  [pwwn] 50:00:14:40:12:34:56:79

VSAN 10 Zone Status:
 Zone Name: Zone_Storage
 Zone Members: 2
 Status: Active

Domain ID  Domain Name  State  Priority
1          mds-core-01  active 1
2          mds-core-02  active 2

Last 50 log entries:
2024 Jan 15 14:32:10 +00:00 mds-core-01 %FSPF-2-FSPF_HELLO_LOSS: FSPF hello loss on interface fc1/4
2024 Jan 15 14:15:22 +00:00 mds-core-01 %ETHPORT-5-IF_DOWN: Interface fc1/4 is down
2024 Jan 15 13:45:01 +00:00 mds-core-01 %ZONE-6-ZONESET_ACTIVATED: ZoneSet_Prod activated

Memory Usage: 68%
CPU Usage: 12%
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in the correct CLI mode
```bash
show version
show running-config
show interface brief
show flogi database
show zoneset active vsan all
show environment
show logging last 50
```


```text title="Expected output"
Cisco MDS 9148S Multilayer Fabric Switch
System uptime is 247 days 14 hours 32 minutes
System version: 8.4(2b)
BIOS: version 3.13(2)

Current configuration:
version 8.4(2b)
feature fcoe
feature fport-channel-trunk
zone name PROD_ZONE vsan 1
  member pwwn 50:00:14:40:5a:1b:2c:3d
  member pwwn 50:00:14:40:5a:1b:2c:4e
zoneset name PROD_ZONESET vsan 1
  member PROD_ZONE
  member BACKUP_ZONE

Interface      IP-Address      Status         Proto-Status
fc1/1          --              trunking       trunk on
fc1/2          --              trunking       trunk on
fc1/3          --              notConnected   initializing
fc1/4          --              connected      online
...

FLOGI Database for VSAN 1:
FCID           Port Name                    Node Name                    Class
0x010100       50:00:14:40:5a:1b:2c:3d     50:00:14:40:5a:1b:2c:00     3
0x010200       50:00:14:40:5a:1b:2c:4e     50:00:14:40:5a:1b:2c:01     3

Active zoneset for VSAN 1: PROD_ZONESET
Zone: PROD_ZONE
  pwwn 50:00:14:40:5a:1b:2c:3d [active]
  pwwn 50:00:14:40:5a:1b:2c:4e [active]

Temperature: 38°C (Normal)
Fan Status: All fans operational
Power Supply 1: OK
Power Supply 2: OK

2024 Jan 15 14:32:15 mds-switch-01 %SYSLOG-3-LINK_DOWN: Interface fc1/3 is down
2024 Jan 15 14:15:22 mds-switch-01 %SYSLOG-5-CONFIG_I: Configured from console by admin
2024 Jan 15 13:48:09 mds-switch-01 %SYSLOG-2-ZONE_ACTIVATION: Zone PROD_ZONESET activated on VSAN 1
2024 Jan 15 12:20:44 mds-switch-01 %SYSLOG-4-FLOGI_REJECT: FLOGI rejected for pwwn 50:00:14:40:5a:1b:2c:5f
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the switch is in the correct mode (enable mode required); use `enable` if needed.
    **`% Incomplete command`** — Add the required parameter (e.g., `show version` not `show ver`); use tab completion to verify syntax.
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
