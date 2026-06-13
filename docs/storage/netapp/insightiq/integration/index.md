---
tags:
  - netapp
---
# InsightIQ Integration

<div class="kb-summary">
InsightIQ Integration reference covering Overview, OneFS Data Connector (Inbound), SMTP Email Alerts, SNMP Forwarding to Monitoring Platform, Syslog to SIEM and 2 more sections.

*Applies to: InsightIQ*
</div>

## Overview

InsightIQ integrates primarily with PowerScale (Isilon) clusters for data collection, and with enterprise monitoring, identity, and notification platforms for alerting and access management.

## OneFS Data Connector (Inbound)

The core integration is between InsightIQ and each PowerScale cluster. InsightIQ pulls metrics via the OneFS REST API.

```text
┌──────────────────────────────────── InsightIQ — Integration Guide ────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Email Notifications              │  │                External Tools               │   │
│   │              SMTP configuration              │  │              REST API (limited)             │   │
│   │               Threshold alerts               │  │               CSV for BI tools              │   │
│   │               Report delivery                │  │              Grafana REST proxy             │   │
│   │                Recipient list                │  │              Scheduled reports              │   │
│   │              Alert cadence cfg               │  │              PDF to management              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM → SMTP relay → email · PDF/CSV download from UI · REST on TCP 443                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SMTP = Email relay configured in InsightIQ for threshold alerts and report delivery                  │
│  Threshold alert = Email when a metric (latency, utilisation) exceeds defined limit                   │
│  Report delivery = Scheduled InsightIQ report emailed as PDF to recipient list                        │
│  REST API = InsightIQ exposes limited REST for programmatic data retrieval                            │
│  CSV for BI = Metric data exported as CSV for Power BI, Tableau, or Excel                             │
│  Grafana proxy = REST proxy exposing InsightIQ metrics as Grafana data source                         │
│  Scheduled report = Weekly/monthly report generated and emailed automatically                         │
│  PDF to management = Formatted performance report for storage operations review                       │
│  Recipient list = Email addresses configured in InsightIQ notification settings                       │
│  Alert cadence = How often InsightIQ re-sends alert if threshold remains exceeded                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Alert rules are configured per metric threshold under: **Administration > Alert Settings > Add Alert**

## SNMP Forwarding to Monitoring Platform

InsightIQ can forward threshold breach alerts as SNMP traps to enterprise monitoring platforms (Aria Operations, Nagios, Zabbix).

```text
InsightIQ web UI > Administration > SNMP
- SNMP version: v2c or v3 (prefer v3 for security)
- Community string / auth credentials
- Trap target: <Aria-Operations-IP>:162 or <monitoring-platform>:162
```

For Aria Operations: configure an SNMP trap receiver adapter to ingest InsightIQ traps and map them to Aria alert definitions.

## Syslog to SIEM

InsightIQ appliance events (user logins, configuration changes, service errors) are forwarded to the SIEM via syslog.

```bash
# Configure syslog forwarding on InsightIQ appliance (RHEL/CentOS):
# /etc/rsyslog.d/insightiq.conf
*.* @<SIEM-IP>:514        # UDP
# or
*.* @@<SIEM-IP>:514       # TCP
```

Restart rsyslog after configuration change:
```bash
sudo systemctl restart rsyslog
```

## CSV / PDF Report Export

InsightIQ generates scheduled reports distributed via email or available for download.

```text
InsightIQ web UI > Reports > Scheduled Reports > Add
- Report type: Cluster Performance / Capacity Trend / Protocol Summary
- Format: PDF or CSV
- Schedule: weekly or monthly
- Email recipients: distribution list
```

Reports are suitable for distribution to capacity planning teams and management.

## Integration Summary

| Integration | Direction | Purpose |
|---|---|---|
| OneFS Data Connector | Inbound | Performance and capacity metrics collection |
| Active Directory / LDAP | Inbound | Centralised user authentication |
| SMTP | Outbound | Threshold breach email alerts |
| SNMP | Outbound | Availability and threshold alerts to monitoring platform |
| Syslog to SIEM | Outbound | Appliance event audit forwarding |
| CSV / PDF Export | Outbound | Capacity planning report distribution |
