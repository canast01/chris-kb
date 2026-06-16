---
tags:
  - troubleshooting
  - sannav
  - brocade
  - san
  - known-issues
---
# Brocade SANnav — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known SANnav bugs, error codes, and workarounds covering switch discovery, performance data, and upgrade issues.

*Applies to: SANnav 2.3.x*
</div>

```text
┌─────────────────────────────────────────── Brocade SANnav ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              SAN management platform — discovery, health, topology, and analytics             │   │
│   │           Protocols: REST API · SNMP v3 · syslog · HTTPS (UI) · SSH (switch access)           │   │
│   │                Management: SANnav web UI · REST API · email/SNMP alert delivery               │   │
│   │             Switch discovery -> topology map -> MAPS event -> alert -> remediation            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Management         │  │       SANnav server VM      │  │     Postgres + InfluxDB     │   │
│   │          Discovery          │  │      Switch seed + scan     │  │    SSH credentials needed   │   │
│   │          Monitoring         │  │      MAPS + port stats      │  │     Time-series metrics     │   │
│   │           Topology          │  │      Fabric map + ISLs      │  │    Rebuilt on rediscover    │   │
│   │          Analytics          │  │      Traffic + latency      │  │      Stored in InfluxDB     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  SANnav server   │Central management│     HTTPS 443     │   LDAP / local   │OVA or bare-metal │   │
│   │   Switch agent   │ Telemetry source │     SSH / SNMP    │   Switch creds   │FOS 9.x+ required │   │
│   │   Alert engine   │ MAPS event relay │    SNMP / email   │       N/A        │Customizable rules│   │
│   │     REST API     │Automation access │     HTTPS 443     │    API token     │  JSON responses  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: SANnav server VM -> managed Brocade FC switches -> fabric topology data                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Discovery    = SANnav process that connects to seed switches and maps the fabric                     │
│  Seed switch  = first switch SANnav contacts; used to traverse the rest of fabric                     │
│  MAPS         = Monitoring and Alerting Policy Suite; threshold-based port alerts                     │
│  Topology map = visual representation of switches, ISLs, and connected hosts                          │
│  InfluxDB     = time-series database storing SANnav performance metrics                               │
│  Port mirroring = SAN traffic copy for analysis (requires FOS license)                                │
│  Audit log    = records all configuration changes made via SANnav or switch CLI                       │
│  Collector    = SANnav component gathering telemetry from each managed switch                         │
│  Alert group  = logical set of thresholds applied uniformly to a set of ports                         │
│  Dashboard    = SANnav home view showing fabric health, alerts, and top talkers                       │
│  REST token   = API Bearer token scoped to a SANnav user role                                         │
│  OVA          = Open Virtual Appliance; SANnav deployment package for vSphere                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- SANnav errors appear in Dashboard → Events and in SANnav → Administration → Logs.
- Most discovery failures are SNMP or SSH connectivity issues from SANnav to switches.

## Switch Discovery

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Switch not appearing after add | SANnav 2.3 | SNMP community mismatch or UDP 161 blocked | Verify SNMP community string; verify UDP 161 from SANnav to switch | N/A |
| `SSH authentication failed` during discovery | SANnav 2.3 | SANnav credentials incorrect for switch admin | Update switch credentials in SANnav → Administration → Credentials | N/A |
| SNMP trap not appearing in SANnav | SANnav 2.3 | Switch SNMP trap destination not pointing to SANnav | Configure trap on switch: `snmpconfig --set snmpv1` with SANnav IP | N/A |

## Performance Data

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Performance graphs empty for discovered switch | SANnav 2.3 | Performance monitoring not enabled for switch | Enable monitoring: SANnav → Monitoring → Performance Monitoring → Add Targets | N/A |
| Port utilization showing 0% for active ports | SANnav 2.3 | Counter polling interval set too high | Reduce polling interval to 30 seconds for active monitoring | N/A |

## See also

- [Brocade SANnav — Common Issues](common-issues.md)
- [Brocade Fabric OS — Known Issues](../../fabric-os/troubleshooting/known-issues/)
