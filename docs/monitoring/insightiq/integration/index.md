# InsightIQ Integration
## Overview

InsightIQ integrates primarily with PowerScale (Isilon) clusters for data collection, and with enterprise monitoring, identity, and notification platforms for alerting and access management.

## OneFS Data Connector (Inbound)

The core integration is between InsightIQ and each PowerScale cluster. InsightIQ pulls metrics via the OneFS REST API.

```text
Configuration: InsightIQ web UI > Administration > Clusters > Add Cluster
- OneFS management IP or SmartConnect zone name
- Username: svc-insightiq (read-only OneFS account)
- Collection interval: configurable (default: 30 seconds, aggregated to 5-minute buckets)
- TLS: enforce HTTPS for API calls to OneFS management port (TCP 8080)
```
```

## Active Directory SSO (LDAP Integration)

InsightIQ supports LDAP/AD integration for centralised user authentication.

```text
InsightIQ web UI > Administration > Authentication > LDAP
- LDAP server: ldap://<DC-FQDN>:389 or ldaps://<DC-FQDN>:636
- Bind DN: CN=svc-iiq-ldap,OU=ServiceAccounts,DC=company,DC=com
- Base DN: OU=StorageTeam,DC=company,DC=com
- Group mapping: LDAP group → InsightIQ admin or viewer role
```

Use LDAPS (TCP 636) to encrypt LDAP traffic. Store the bind account password in the secrets manager.

## SMTP Email Alerts

InsightIQ sends alert emails directly from the appliance via SMTP. Configure the outbound SMTP relay.

```text
InsightIQ web UI > Administration > Email Settings
- SMTP server: relay.company.com
- Port: 587 (STARTTLS)
- From address: insightiq-alerts@company.com
- Recipients: configure per alert rule (storage-ops@company.com)
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
