---
tags:
  - operations
  - san
---
# Brocade SANnav — Health Checks

*Applies to: Brocade FOS 9.x*

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

1. `systemctl status sannav` on the SANnav appliance — confirm all component services are **active (running)**
2. SANnav UI → Dashboard — verify all discovered fabrics show **Connected** status; flag any Unknown or Disconnected
3. SANnav → Fabrics → switch list — confirm all switches appear as **Managed**; investigate any Unmanaged or Unreachable
4. SANnav → Alarms → filter by Status: Open, Severity: Critical/Major — review and acknowledge or escalate each
5. SANnav → Performance → port/ISL graphs — confirm data collection is active (non-flat graphs); missing data indicates collection failure
6. `df -h /opt/brocade/sannav/data` on SANnav appliance — alert and investigate if filesystem usage exceeds **80%**
7. SANnav → Administration → Certificates — review expiry dates; raise a ticket for any certificate expiring within 60 days

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Sannav — Procedures](../procedures/)
- [Sannav — CLI Reference](../cli-reference/)
- [Sannav — Common Issues](../../troubleshooting/common-issues/)
