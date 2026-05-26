# Nexus Dashboard Integration
## Overview

Nexus Dashboard integrates with Cisco ACI and NX-OS fabric infrastructure as its core data sources, and extends to ITSM, SIEM, notification, and AAA platforms for operational workflows.

## ACI APIC Integration

The ACI APIC cluster is the primary integration for ACI-based fabrics. NDFC and NDI use the APIC REST API for policy management, fabric visibility, and health data.

```text
Admin > Sites > Add Site
- Site type: ACI
- APIC IP / hostname: <APIC-cluster-VIP>
- Username: (use dedicated service account — svc-nd-apic)
- Password: stored in secrets manager
- For NDO (multi-site): add all APIC clusters across all sites
```
```

NDFC communicates with switches via SSH (provisioning) and SNMP (telemetry/faults).

## DCNM Migration Note

NDFC replaces Cisco DCNM (Data Center Network Manager). If your environment still runs DCNM, plan migration to NDFC as DCNM has reached EOS. NDFC is backward-compatible with existing VXLAN BGP-EVPN fabric policies from DCNM.

## SIEM Integration (Syslog)

Nexus Dashboard forwards fabric faults and system events to the enterprise SIEM via syslog.

```text
Admin > System Settings > Syslog
- Destination IP: <SIEM-collector-IP>
- Port: UDP 514 or TCP 514
- Severity: select minimum severity (Warning or above for production)
- Format: RFC 5424
```

For ACI fabrics, configure APIC syslog forwarding separately (APIC also generates fabric events):
```text
APIC > Admin > External Data Collectors > Monitoring Destinations > Syslog > Add
```

## ServiceNow ITSM Integration

P1/P2 fabric faults auto-create incidents in ServiceNow via the ND alert notification webhook.

```text
Admin > Notifications > Create Notification
- Trigger: NDI Fault severity = Critical or Major
- Action: Webhook
- URL: https://<instance>.service-now.com/api/now/table/incident
- Auth: Basic (svc-nd-snow service account)
- Payload:
  {
    "short_description": "Cisco ND P1 Fault: {{fault.title}} — {{fabric.name}}",
    "severity": "1",
    "assignment_group": "network-ops",
    "description": "{{fault.description}}\nFabric: {{fabric.name}}\nNode: {{node.name}}"
  }
```

## AAA / LDAP Integration

```text
Admin > Authentication > Remote Login Domains > Add
- Protocol: LDAP (LDAPS recommended)
- Server: ldaps://<AD-DC>:636
- Bind DN: CN=svc-nd-ldap,OU=ServiceAccounts,DC=company,DC=com
- Search base: OU=Network,DC=company,DC=com
- Role mapping:
  - AD group: ND_Admins → Nexus Dashboard Admin
  - AD group: ND_Operators → Fabric Operator
  - AD group: ND_ReadOnly → ReadOnly
```

Set the default login domain to LDAP and retain a local break-glass admin account.

## SMTP Notifications

```text
Admin > System Settings > SMTP
- SMTP server: relay.company.com
- Port: 587 (STARTTLS)
- From: nexus-dashboard-alerts@company.com
```

Create notification rules to email specific distribution lists for P2/P3 faults.

## Aria Operations Integration

The Cisco Network Insights management pack for Aria Operations imports NDI fabric health data into vROps for correlation with VMware workload metrics.

```text
Aria Operations > Admin > Solutions > Cisco Network Insights MP
- Nexus Dashboard API URL: https://<ND-VIP>
- Username / password: (read-only service account)
```

## Integration Summary

| Integration | Type | Purpose |
|---|---|---|
| ACI APIC | Inbound | Policy management and ACI fabric visibility |
| NX-OS / NDFC | Inbound | NX-OS fabric management and telemetry |
| SIEM (syslog) | Outbound | Fabric fault and admin event forwarding |
| ServiceNow ITSM | Outbound | P1/P2 fault ticketing |
| LDAP / AAA | Inbound | Centralised user authentication and RBAC |
| SMTP | Outbound | Alert email notifications |
| Aria Operations | Outbound | Correlated VMware + Cisco fabric visibility |
