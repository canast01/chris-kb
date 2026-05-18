# Pure Storage Operations — Alerts

```
  Pure Alert Flow

  FlashArray / FlashBlade
  ┌─────────────────────────┐
  │  Array event generated  │
  │  (drive, temp, capacity,│
  │   replication, network) │
  └────────────┬────────────┘
               │
  ┌────────────▼────────────┐
  │  Pure1 (phone-home)     │
  │  Consolidated alert     │
  │  dashboard              │
  └────┬──────┬──────┬──────┘
       │      │      │
       ▼      ▼      ▼
  ┌────────┐ ┌─────┐ ┌────────────┐
  │ Email  │ │SNMP │ │  Syslog    │
  │ alert  │ │trap │ │  ──► SIEM  │
  └────────┘ └─────┘ └────────────┘
       │
       ▼
  ┌────────────────────────────────┐
  │  Response                      │
  │  Critical ──► page on-call now │
  │  Warning  ──► investigate today│
  │  Info     ──► review when able │
  └────────────────────────────────┘
```

## Viewing Alerts

```bash
# CLI — FlashArray
purecli alert list

# CLI — FlashBlade
purefb alert list
```

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

## Pre-Change Alert Check

Before any maintenance:
```bash
purecli alert list      # FlashArray
purefb alert list       # FlashBlade
```

Do not proceed if critical alerts are active.
