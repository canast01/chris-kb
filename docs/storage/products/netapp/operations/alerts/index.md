---
tags:
  - netapp
  - operations
---
# NetApp Operations — Alerts

<div class="kb-summary">
Alerts reference covering ONTAP EMS Alerts, AutoSupport Notifications, SNMP Alerting, BlueXP Alerts (Keystone / Cloud Manager), Alert Triage Priority and 2 more sections.

*Applies to: ONTAP 9.x*
</div>

```d2
direction: down

ontap_ems_alerts: "ONTAP EMS Alerts" {shape: rectangle}
autosupport_notifications: "AutoSupport Notifications" {shape: rectangle}
snmp_alerting: "SNMP Alerting" {shape: rectangle}
bluexp_alerts_keystone_cloud_manager: "BlueXP Alerts (Keystone / Cloud Manager)" {shape: rectangle}
alert_triage_priority: "Alert Triage Priority" {shape: rectangle}
resolving_health_alerts: "Resolving Health Alerts" {shape: rectangle}

ontap_ems_alerts -> autosupport_notifications: uses
autosupport_notifications -> snmp_alerting: uses
snmp_alerting -> bluexp_alerts_keystone_cloud_manager: uses
bluexp_alerts_keystone_cloud_manager -> alert_triage_priority: uses
alert_triage_priority -> resolving_health_alerts: uses
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## ONTAP EMS Alerts

```bash
# Show active health alerts
system health alert show

# Show recent critical/error events
event log show -severity critical
event log show -severity error -time ">24h"

# Show subsystem health
system health subsystem show
```


```text title="Expected output"
Active Health Alerts:
Node: cluster1-01
  Alertname: NetAppClusterLowDiskSpace
  Severity: warning
  Description: Aggregate aggr1 is 89% full
  Time: 2024-01-15 14:32:18

Node: cluster1-02
  Alertname: DegradedRAIDStatus
  Severity: critical
  Description: RAID group rg0 has 1 failed disk
  Time: 2024-01-15 13:45:02

Events (Critical):
Time                 Node         Event Code    Message
2024-01-15 13:45:02  cluster1-02  RAID.disk.fail  Disk SN:ABC123XYZ failed in rg0
2024-01-15 12:15:33  cluster1-01  NVRAM.battery.low  NVRAM battery at 45% capacity

Events (Error - Last 24h):
Time                 Node         Event Code    Message
2024-01-15 10:22:15  cluster1-01  LUN.offline    LUN /vol/data/lun0 went offline
2024-01-15 08:19:47  cluster1-02  Fan.speed.low  Fan module 3 running at 60% speed
2024-01-15 06:55:12  cluster1-01  Temp.sensor.high  Temperature sensor PSU-1 reading 78°C

Subsystem Health:
Subsystem              Status    Details
SFO                    ok        -
Storage                warning   Aggregate aggr1: 89% full
NVMe                   ok        -
CIFS                   ok        -
NFS                    ok        -
iSCSI                  ok        -
Cluster                ok        -
```

!!! warning "Common errors"
    **`Error: command not found: system health alert show`** — Verify you are connected to the NetApp cluster with `cluster show` and have appropriate admin privileges.
    **`Error: Access denied. Insufficient privileges for this command.`** — Ensure your user account has the "admin" or "security-admin" role assigned via `security login show`.
    **`Error: No events found matching the specified criteria.`** — Adjust the time filter (e.g., use `-time ">7d"` for the last 7 days) or remove severity filters to broaden results.
## AutoSupport Notifications

AutoSupport triggers automatic case creation with NetApp support for critical events. Verify it is configured:

```bash
system node autosupport show -fields state,support,transport,mail-hosts
```


```text title="Expected output"
Node                                   State      Support    Transport      Mail Hosts
------------------------------------   ---------- ---------- -------------- --------------------------------
cluster1-01                            enabled    full       https          mail.example.com
cluster1-02                            enabled    full       https          mail.example.com
2 entries were displayed.
```

!!! warning "Common errors"
    **`Error: command not found: system`** — Ensure you are connected to the NetApp cluster CLI (SSH to the cluster management IP) rather than a local shell.
    **`Error: This operation is not permitted: insufficient access rights`** — Verify your user account has admin-level privileges; contact your NetApp administrator to grant the required role.
Expected: `state: enable`, `support: true`.

## SNMP Alerting

```bash
# Show SNMP communities and trap hosts
system snmp show
system snmp traphost show
```


```text title="Expected output"
SNMP is enabled

Community: public
    Access Level: ro
    Authentication Protocol: none

Community: netapp-monitor
    Access Level: ro
    Authentication Protocol: sha
    Privacy Protocol: aes128

Trap Host: 192.168.1.100
    Port: 162
    Community: public

Trap Host: 10.20.30.40
    Port: 162
    Community: netapp-monitor
```

!!! warning "Common errors"
    **`Error: This command requires admin or vsadmin privileges`** — Run the command with appropriate cluster admin credentials or from a node with sufficient permissions.
    **`Error: SNMP is not configured on this cluster`** — Enable SNMP first using `system snmp modify -enabled true` before querying trap hosts.
Verify trap destinations are configured to route to your monitoring platform (SCOM, Zabbix, etc.).

## BlueXP Alerts (Keystone / Cloud Manager)

For Keystone subscriptions and Cloud Volumes ONTAP, alerts are surfaced in:
- **BlueXP → Notifications** — capacity, health, and service alerts
- **BlueXP → Digital Wallet** — burst capacity warnings

## Alert Triage Priority

| Severity | Example | Action |
|---|---|---|
| Emergency | Aggregate offline | Immediate — page on-call |
| Alert | Disk failed, HA link down | Same business day |
| Error | LIF down, volume near full | Investigate within 24h |
| Warning | Efficiency below threshold | Review at next available |

## Resolving Health Alerts

```bash
# View active alerts with detail
system health alert show

# Acknowledge an alert (after resolution)
system health alert modify -node <node> -alert-id <id> -acknowledge true

# Clear alert after fixing underlying issue
system health alert delete -node <node> -alert-id <id>
```


```text title="Expected output"
Cluster Name: prod-cluster-01
Node: node-01
Alert ID: DiskShelfPowerSupply.5.1a2b3c4d
Severity: Major
Description: Power supply failure detected in disk shelf SH-01
Status: New
Triggered Time: 2024-01-15 14:32:18

Node: node-02
Alert ID: HighCPUUtilization.2.5e6f7g8h
Severity: Minor
Description: CPU utilization above 85% threshold
Status: New
Triggered Time: 2024-01-15 14:28:45

Node: node-01
Alert ID: DiskShelfPowerSupply.5.1a2b3c4d
Status: Acknowledged
Acknowledged by: admin
Acknowledged Time: 2024-01-15 14:35:22

Alert DiskShelfPowerSupply.5.1a2b3c4d deleted successfully.
```

!!! warning "Common errors"
    **`Error: Node "<node>" not found in cluster`** — Verify the node name matches output from `cluster show` and use the correct node identifier.
    **`Error: Alert ID "<id>" does not exist or has already been deleted`** — Confirm the alert ID is still active using `system health alert show` before attempting deletion.
## Common Alerts

| Alert | Cause | Resolution |
|---|---|---|
| Volume full | Data growth | Resize or enable autosize |
| Disk failed | Hardware failure | Replace disk, verify RAID rebuild |
| HA interconnect down | Cable/port failure | Investigate HA link |
| AutoSupport failure | Proxy or network | Verify outbound connectivity |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [NetApp — Health Checks](../health-checks/)
