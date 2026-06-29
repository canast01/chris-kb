---
tags:
  - architecture
  - netapp
---
# Superna Eyeglass — Integrations

<div class="kb-summary">
Integrations reference covering NetApp PowerScale (SyncIQ), Syslog / SIEM, Email Notifications.

*Applies to: Superna Eyeglass*
</div>
![Superna Eyeglass — Integrations](../../../../assets/storage-netapp-superna-eyeglass-architecture-integrations.svg)

## NetApp PowerScale (SyncIQ)

```mermaid
flowchart LR
    subgraph "Production Site"
        primaryPS["PowerScale Cluster A\n(Production)"]
        synciqPol["SyncIQ Policies\nContinuous / Scheduled"]
    end
    subgraph "DR Site"
        drPS["PowerScale Cluster B\n(DR)"]
    end
    subgraph "Management Plane"
        eyeglass["Superna Eyeglass\nDR Assistant"]
        ad["Active Directory\nAD group ACLs"]
        dns["DNS Server\nWindows DNS / BIND"]
        siem["SIEM / Monitoring\nSNMP / Syslog"]
    end

    primaryPS -->|"SyncIQ replication"| drPS
    eyeglass -->|"OneFS REST API\nmonitors SyncIQ"| primaryPS
    eyeglass -->|"OneFS REST API\nchecks DR readiness"| drPS
    ad -->|"AD group mapping\nfor share ACLs"| eyeglass
    eyeglass -->|"DNS cutover\nzone delegation"| dns
    eyeglass -->|"SNMP traps\nsyslog events"| siem
```

## Syslog / SIEM

Forward Eyeglass audit trail to SIEM:

1. Eyeglass Admin UI: Configuration → Syslog
2. Enter SIEM IP, port 514 (UDP) or 6514 (TLS)

Alert in SIEM on:
- Failover initiated (any event)
- DR readiness score < 100% for > 15 minutes
- Eyeglass appliance unreachable

## Email Notifications

Eyeglass Admin UI: Configuration → Notifications → Email:
- Configure SMTP relay
- Add distribution lists for DR team and on-call
- Enable notifications for: failover events, readiness changes, SyncIQ policy errors

---

## See also

- [Superna Eyeglass — How It Works](../how-it-works/)
- [Superna Eyeglass — Design Standards](../design-standards/)
