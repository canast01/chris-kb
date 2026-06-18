---
tags:
  - pure1
  - pure-storage
  - networking
  - firewall
  - ports
  - monitoring
---
# Pure1 — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Pure1 (Pure Storage cloud management and analytics SaaS). Pure1 requires only outbound HTTPS from each managed array to pure1.purestorage.com. No inbound connection from Pure to on-premises infrastructure is required.

*Applies to: Pure1 (cloud portal — no on-premises install)*
</div>

```text
┌───────────────────────────────────────── Storage Pure Pure1 ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Pure: Storage Pure Pure1 platform                               │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: Storage Pure Pure1 management console                       │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Storage Pure Pure1 infrastructure · management network · monitoring                      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Pure               = Storage Pure Pure1 platform overview and core concepts                        │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## How It Works

Pure1 is a fully SaaS-based cloud management platform. Each FlashArray and FlashBlade array ships with a built-in phone-home agent that establishes an **outbound-only** TLS connection to Pure's cloud. Administrators access Pure1 via browser at `pure1.purestorage.com` — no on-premises software is needed.

## Outbound — Arrays to Pure1 Cloud (Required)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | FlashArray management IP | pure1.purestorage.com | Telemetry, health data, proactive support, capacity forecasting |
| 443 | TCP | FlashBlade management IP | pure1.purestorage.com | Same as FlashArray |

## Admin Access (SaaS)

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | pure1.purestorage.com | Admin browser — Pure1 dashboard, AI-driven analytics, support cases |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| FlashArray mgmt IP | pure1.purestorage.com | 443 | Outbound only — no inbound from Pure cloud |
| FlashBlade mgmt IP | pure1.purestorage.com | 443 | Outbound only |
| Admin browsers | pure1.purestorage.com | 443 | SaaS portal |

## Verify

```bash
# From FlashArray or FlashBlade management IP — test Pure1 connectivity
curl -sk -o /dev/null -w "%{http_code}" https://pure1.purestorage.com/

# From FlashArray CLI — verify phone-home status
puremessage test

# From FlashBlade CLI — verify Pure1 telemetry
purealertalert test

# Check outbound 443 from array management network to pure1.purestorage.com
nc -zv pure1.purestorage.com 443
```

## See also

- [Pure1 — Architecture](how-it-works/)
