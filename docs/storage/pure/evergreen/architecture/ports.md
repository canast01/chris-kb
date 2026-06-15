---
tags:
  - evergreen
  - pure-storage
  - networking
  - firewall
  - ports
---
# Pure Storage Evergreen — Ports and Network Requirements

<div class="kb-summary">
Pure Storage Evergreen is a commercial subscription program — it is not a separate software product and does not introduce additional network ports. All port requirements come from the underlying FlashArray or FlashBlade hardware being managed.

*Applies to: Evergreen//Forever, Evergreen//Flex subscription programs*
</div>

```text
┌─────────────────────────────────────── Storage Pure Evergreen ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Pure: Storage Pure Evergreen platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                     Management: Storage Pure Evergreen management console                     │   │
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
│    Physical: Storage Pure Evergreen infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Pure               = Storage Pure Evergreen platform overview and core concepts                    │
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

Evergreen is Pure Storage's non-disruptive upgrade and subscription licensing model. Customers receive ongoing controller and software upgrades as part of their subscription — no separate Evergreen management plane or appliance is deployed on-premises.

The only network-level requirement specific to Evergreen is that each array can reach **pure1.purestorage.com:443** to enable proactive support, upgrade scheduling, and entitlement verification.

## Relevant Port Pages

| Component | Ports Page |
|---|---|
| FlashArray (block storage) | [Pure Storage FlashArray — Ports](../flasharray/architecture/ports/) |
| FlashBlade (file/object) | [Pure Storage FlashBlade — Ports](../flashblade/architecture/ports/) |
| Pure1 cloud telemetry | [Pure1 — Ports](../pure1/architecture/ports/) |

## Upgrade-Related Connectivity (Outbound)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | FlashArray/FlashBlade mgmt IP | pure1.purestorage.com | Upgrade notifications, controller swap coordination, entitlement check |

## See also

- [Pure Storage Evergreen — Architecture](how-it-works/)
- [Pure Storage FlashArray — Ports](../flasharray/architecture/ports/)
- [Pure Storage FlashBlade — Ports](../flashblade/architecture/ports/)
- [Pure1 — Ports](../pure1/architecture/ports/)
