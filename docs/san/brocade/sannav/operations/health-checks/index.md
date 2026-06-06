# Brocade SANnav — Health Checks

```bash
# SSH to appliance
ssh admin@sannav-dc1.corp.example.com

# Check service status
sannav status
# Expected: all services: running

# Check disk usage
df -h /opt/sannav
# Alert if Use% > 80

# Check application logs for errors
grep -i "ERROR\|FATAL" /opt/sannav/logs/server.log | tail -50

# Check discovery engine for unreachable switches
grep "unreachable\|connection refused\|timeout" /opt/sannav/logs/discovery.log | tail -30

# Check event engine
grep -i "ERROR" /opt/sannav/logs/event-engine.log | tail -20

# Check NTP sync
timedatectl status
# Expected: "synchronized: yes"
```
```text
┌─────────────────────────────────── Brocade SANnav — Health Checks ────────────────────────────────────┐
│                                                                                                       │
│  SANnav health checks: MAPS dashboards, port error trends, switch status, ISL load.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           SANnav Dashboard Health            │  │             Switch-Level Health             │   │
│   │       MAPS: active alerts by severity        │  │         switchstatusshow: all green         │   │
│   │          Fabric topology: no split           │  │         sensorshow: temp < threshold        │   │
│   │       Port inventory: no offline ports       │  │           Fan + PSU: healthy state          │   │
│   │       Firmware currency: < 2 versions        │  │         CP status: active + standby         │   │
│   │         Zone config: saved == active         │  │          Port errors < 10/day limit         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  MAPS and SANnav dashboards are primary health indicators; review daily.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             ISL & Fabric Health              │  │            SANnav Platform Health           │   │
│   │          islshow: utilisation < 70%          │  │         SANnav service: all running         │   │
│   │        ISL BB credits: no starvation         │  │           DB size: within capacity          │   │
│   │          fabricshow: single fabric           │  │          HA sync: primary = standby         │   │
│   │        Bottleneck: no congested ISLs         │  │           Backup: last job success          │   │
│   │        D_Port: link quality > -3 dBm         │  │          Alerts: SMTP + SNMP active         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Brocade FC switch chassis · SFP optical levels · ISL cables · SANnav VM resources                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  MAPS            = Monitoring and Alerting Policy Suite; tracks thresholds per port                   │
│  switchstatusshow= overall switch health status; green = all healthy                                  │
│  sensorshow      = temp/fan/PSU readings; alert if temperature exceeds threshold                      │
│  BB credits      = Buffer-to-Buffer credits; starvation causes ISL congestion                         │
│  islshow         = ISL utilisation; > 70% sustained indicates need for more ISLs                      │
│  D_Port          = diagnostic port; optical signal quality measurement (dBm)                          │
│  fabricshow      = single fabric confirmation; split fabric = major incident                          │
│  CP status       = Control Processor; HA pair should have active + standby running                    │
│  Bottleneck      = SANnav congestion detection; ISL fully utilized under load                         │
│  HA sync         = primary and standby SANnav databases must be in sync                               │
│  Zone config     = saved config should match active config; divergence = risk                         │
│  dBm             = decibels relative to 1 milliwatt; SFP optical power measurement                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Run This Routine

1. `systemctl status sannav` on the SANnav appliance — confirm all component services are **active (running)**
2. SANnav UI → Dashboard — verify all discovered fabrics show **Connected** status; flag any Unknown or Disconnected
3. SANnav → Fabrics → switch list — confirm all switches appear as **Managed**; investigate any Unmanaged or Unreachable
4. SANnav → Alarms → filter by Status: Open, Severity: Critical/Major — review and acknowledge or escalate each
5. SANnav → Performance → port/ISL graphs — confirm data collection is active (non-flat graphs); missing data indicates collection failure
6. `df -h /opt/brocade/sannav/data` on SANnav appliance — alert and investigate if filesystem usage exceeds **80%**
7. SANnav → Administration → Certificates — review expiry dates; raise a ticket for any certificate expiring within 60 days
