---
tags:
  - operations
  - pure
---
# Pure Storage Operations — Alerts

<div class="kb-summary">
Alerts reference covering Viewing Alerts, Alert Severity Levels, Common Alert Types, Pure1 Phone-Home Connectivity, Alert Notifications and 2 more sections.

*Applies to: FlashArray Purity 6.x*
</div>

![Pure Storage Operations — Alerts — Diagram](../../../../../assets/storage-pure-operations-alerts-diagram.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Viewing Alerts

```bash
# CLI — FlashArray
purecli alert list

# CLI — FlashBlade
purefb alert list
```


```text title="Expected output"
=== FlashArray Alerts ===
ID                                   Severity  Category        Created                 Message
8f3c9e2a-1b4d-47e8-9c2f-5d8e1a6b4c2f Critical  Hardware        2024-01-15T14:32:18Z    Controller 1 temperature threshold exceeded
3d7a2e1f-9c4b-41e6-8a5f-2b9d7c3e1a4f Warning   Performance     2024-01-15T13:45:22Z    Array latency above baseline
7b2f4a8c-5e1d-43f9-b8a2-1c6d9e3f5a7b Info      Capacity        2024-01-15T12:10:05Z    Snapshot space usage at 78%
...

=== FlashBlade Alerts ===
ID                                   Severity  Category        Created                 Message
c4e9f1a3-2d5b-48f7-9a1e-6c3b8d2f4a9e Critical  Replication     2024-01-15T14:28:41Z    Replication lag exceeds 5 minutes
9a1b3c5d-7e2f-41a8-b6c9-4d8e2a3f5c7b Warning   Hardware        2024-01-15T13:52:09Z    Blade 3 disk utilization at 92%
2f5a8c1e-3b7d-49f6-a4c2-8e1d6b3f9a5c Info      Configuration  2024-01-15T11:33:27Z    NFS export policy updated
...
```

!!! warning "Common errors"
    **`purecli: command not found`** — Install the Pure Storage CLI package or add it to your PATH environment variable.
    **`Error: Unable to connect to array at <ip>. Connection refused`** — Verify the array management IP is reachable and the management service is running with `ssh admin@<array-ip> pureadmin status`.
    **`Error: Authentication failed. Invalid credentials`** — Confirm your Pure Storage credentials are configured correctly in `~/.purerc` or via environment variables.
Via Pure1:
- **Pure1 → Alerts** — consolidated alerts across all arrays

## Alert Severity Levels

| Severity | Meaning | Response |
|---|---|---|
| Critical | Immediate risk to data or availability | Page on-call immediately |
| Warning | Degraded component or approaching threshold | Investigate same day |
| Info | Non-critical informational event | Review at next opportunity |

## Common Alert Types

| Alert | Cause | Action |
|---|---|---|
| Drive unhealthy / failed | Media degradation | Pure Support replaces proactively |
| Controller temperature high | Cooling issue or blocked airflow | Check data center cooling |
| Capacity above threshold | Data growth | Expand or clean up |
| Replication lag high | Network or congestion | Check inter-array connectivity |
| Pure1 connectivity lost | Outbound connectivity | Check firewall/proxy settings |

## Pure1 Phone-Home Connectivity

Pure arrays communicate with Pure1 for proactive support and monitoring. Verify connectivity:

```bash
# FlashArray
purecli phone-home list

# FlashBlade
purefb phone-home list
```


```text title="Expected output"
# FlashArray
Phone Home Status: enabled
Last Phone Home: 2024-01-15 14:32:18 UTC
Phone Home Server: https://phonehome.purestorage.com
Proxy Enabled: false
Proxy Server: none
Certificate Validation: enabled
Last Successful Upload: 2024-01-15 14:32:45 UTC
Upload Interval: 24 hours
Data Categories: performance, capacity, hardware_health

# FlashBlade
Phone Home Status: enabled
Last Phone Home: 2024-01-15 14:35:22 UTC
Phone Home Server: https://phonehome.purestorage.com
Proxy Enabled: false
Certificate Validation: enabled
Last Successful Upload: 2024-01-15 14:35:50 UTC
Upload Interval: 24 hours
```

!!! warning "Common errors"
    **`purecli: command not found`** — Install the Pure Storage CLI tools or add the installation directory to your PATH environment variable.
    **`Error: Unable to connect to array at <ip>. Connection refused`** — Verify the array management IP is reachable and the purecli credentials are configured correctly with `purecli login`.
    **`Error: Authentication failed. Invalid API token`** — Re-authenticate using `purecli login` with valid credentials or refresh the API token in your Pure Storage management console.
If phone-home fails, Pure Support cannot proactively monitor the array.

## Alert Notifications

Alerts are delivered via:
- **Email** — configured in array management settings
- **SNMP traps** — for integration with monitoring platforms (SCOM, Zabbix)
- **Pure1** — cloud management portal
- **Syslog** — for SIEM forwarding

## Acknowledge and Close Alerts

```bash
# FlashArray — acknowledge an alert
purecli alert acknowledge --id <alert_id>

# FlashBlade
purefb alert update --id <alert_id> --action acknowledge
```


```text title="Expected output"
Alert 123456 acknowledged successfully.
```

!!! warning "Common errors"
    **`Error: Alert ID not found`** — Verify the alert ID exists by running `purecli alert list` or `purefb alert list` first.
    **`Error: Authentication failed`** — Ensure you are authenticated to the Pure array with valid credentials using `purecli login` or `purefb login`.
## Pre-Change Alert Check

Before any maintenance:
```bash
purecli alert list      # FlashArray
purefb alert list       # FlashBlade
```


```text title="Expected output"
FlashArray Alerts:
Name                          Severity  State      Opened
controller_temp_high          warning   open       2024-01-15T09:23:45Z
disk_predictive_failure       critical  open       2024-01-15T08:47:12Z
replication_lag_exceeded       warning   open       2024-01-14T22:15:33Z
ntp_sync_lost                 info      resolved   2024-01-14T18:30:22Z

FlashBlade Alerts:
Name                          Severity  State      Opened
blade_fan_speed_low           warning   open       2024-01-15T10:12:08Z
network_interface_down        critical  open       2024-01-15T07:55:41Z
capacity_threshold_exceeded    warning   open       2024-01-14T19:44:19Z
```

!!! warning "Common errors"
    **`purecli: command not found`** — Install the Pure Storage CLI package or add it to your PATH environment variable.
    **`Error: Unable to connect to array at <ip>. Connection refused`** — Verify the array management IP is reachable and the management service is running with `ping` and `ssh`.
    **`Error: Invalid credentials for user '<user>'`** — Ensure your Pure Storage credentials are correctly configured in `~/.purerc` or via environment variables.
Do not proceed if critical alerts are active.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Pure Storage — Pure1](../pure1/)
- [Pure Storage — Support Cases](../support-cases/)
- [Pure Storage — Health Checks](../../flasharray/operations/health-checks/)
