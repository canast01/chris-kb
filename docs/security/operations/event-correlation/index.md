---
tags:
  - operations
  - security
---
# Event Correlation

<div class="kb-summary">
Event Correlation reference covering Correlation Workflow, Building a Correlation Timeline, Common Correlation Patterns, SIEM Correlation Rules (Examples), Dependency Map (template) and 1 more sections.
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Dependency Map (template)

Document for each critical service:

```text
Service: ERP Application
  → App server: app01, app02
      → Database: db01 (Oracle)
          → Storage: ONTAP SVM prod-svm, volume erp-data
              → SAN fabric: MDS-A, MDS-B, Zone: erp_zone
      → Load balancer: F5-prod VIP 10.10.10.100
  → Auth: AD domain controllers dc01, dc02
  → DNS: 10.10.10.53
```

## Cross-Platform Log Locations

| System | Log location |
|---|---|
| Linux OS | `/var/log/messages`, `/var/log/syslog`, `journalctl` |
| Windows | Event Viewer: System, Application, Security |
| ONTAP | EMS: `event log show -severity error` |
| VMware | `/var/log/vmkernel.log`, vCenter Events |
| Cisco NX-OS | `show logging last 100` |
| Brocade FOS | `errShow` |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Security Operations — Log Retention](../log-retention/)
- [Security Operations — Runbooks](../runbooks/)
- [Security — Authentication Failures](../../troubleshooting/authentication-failures/)
