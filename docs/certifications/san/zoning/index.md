# SAN Zoning


<div class="kb-summary">
SAN Zoning reference covering Zone Types, Hard vs Soft Zoning, Zone Sets, Single-Initiator Zoning, Cisco VSAN vs Brocade Virtual Fabric and 1 more sections.
</div>
```text
┌────────────────────────────────────── Certifications San Zoning ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            San: Certifications San Zoning platform                            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Certifications San Zoning management console                   │   │
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
│    Physical: Certifications San Zoning infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    San                = Certifications San Zoning platform overview and core concepts                 │
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


## Zone Types

| Zone Type | Member Identifier | Pros | Cons |
|---|---|---|---|
| WWPN (WWN) Zoning | World Wide Port Name | Portable across fabric; survives port moves | Must update zone when HBA replaced |
| Port (Domain:Port) Zoning | Switch Domain + Port number | Survives HBA replacement | Must update zone if device moves to different port |
| Mixed Zoning | WWPN + Domain:Port in same zone | Flexibility | More complex; less common |
| Alias Zoning | Alias name → WWPN mapping | Human-readable zone members | Alias must be kept up to date |

Best practice: Use WWPN-based zoning (alias-based for readability) as the industry default. Port zoning is used in environments where HBA replacement is frequent and port assignments are fixed.

## Hard vs Soft Zoning

| Feature | Hard Zoning | Soft Zoning |
|---|---|---|
| Enforcement | ASIC/hardware — frame-level blocking | Name Server only — blocks discovery |
| Security | High — no communication possible outside zone | Lower — a host with a known FCID can still communicate |
| Performance | No overhead | No overhead |
| Default behavior | Supported on all modern switches | Older fallback; not recommended alone |

Exam rule: Hard zoning is enforced in ASIC hardware and is the default on all modern switches. Soft zoning only prevents a host from discovering targets via the Name Server — it does not physically block frames.

## Zone Sets

| Concept | Definition |
|---|---|
| Zone | A group of ports/WWPNs that can communicate with each other |
| Zone Set (Zone Configuration) | A named collection of zones; only ONE can be active at a time per fabric |
| Zone Database | The full repository of zone and zone set definitions stored on the switch |
| Active Zone Set | The currently enforced zone set; changes to zone DB do not affect fabric until a zone set is activated |

Activation behavior:
- When a zone set is activated it is distributed to all switches in the fabric via RSCN
- Only one zone set can be active per fabric (per VSAN on Cisco)
- Deactivating a zone set removes all zoning — all ports can see all other ports (open fabric)

## Single-Initiator Zoning

The industry-standard design principle:

- Each zone contains exactly ONE initiator (host WWPN) and one or more targets (storage port WWPNs)
- Single-initiator, single-target: maximum isolation; one zone per initiator-target pair
- Single-initiator, multi-target: one zone per host; less isolation but manageable for known-good environments

Avoid multi-initiator zones: if two hosts share a zone with a target and one host behaves badly, it can impact the other.

## Cisco VSAN vs Brocade Virtual Fabric

| Feature | Cisco VSAN | Brocade Virtual Fabric |
|---|---|---|
| Scope | Logical partition of a physical fabric | Logical partition of a chassis |
| Zone isolation | Per-VSAN zone DB | Per-Virtual Fabric zone DB |
| Inter-VSAN routing | IVR (Inter-VSAN Routing) | Not natively supported |
| Default zone behavior | Deny (no default zoning across VSANs) | Configurable |

## Study Checklist

- [ ] Explain the difference between hard and soft zoning and why hard is preferred
- [ ] Describe single-initiator zoning and why multi-initiator zones are avoided
- [ ] Walk through what happens when a zone set is activated (RSCN distribution)
- [ ] Explain what happens if a zone set is deactivated (open fabric)
- [ ] Compare WWPN vs port zoning — give a scenario where each is preferred
- [ ] Know the Brocade commands to create a zone, add members, create a zone set, and activate it
- [ ] Know the Cisco MDS equivalent zone configuration commands
