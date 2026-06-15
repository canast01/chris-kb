---
tags:
  - troubleshooting
  - cisco-mds
  - san
  - known-issues
---
# Cisco MDS — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Cisco MDS SAN switch bugs, error codes, and workarounds covering FC ports, VSAN, zoning, and IVR.

*Applies to: Cisco MDS NX-OS 8.x / 9.x*
</div>

```text
┌──────────────────────────────────────────── San Cisco Mds ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Cisco: San Cisco Mds platform                                 │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                          Management: San Cisco Mds management console                         │   │
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
│    Physical: San Cisco Mds infrastructure · management network · monitoring                           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cisco              = San Cisco Mds platform overview and core concepts                             │
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


## Before you begin

- `show interface fc1/1` for port status; `show flogi database` for logged-in devices.
- `show tech-support` for full diagnostic bundle.
- `show logging` for recent syslog entries.

## FC Ports

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Port `sfpAbsent` or `noOperReason` | MDS NX-OS 8.x | SFP not inserted or not supported | Verify SFP installed; check `show interface fc x/y transceiver` for support | N/A |
| Port `errDisabled` — link flapping | MDS NX-OS 8.x | Excessive link state changes (LOS events) | Check fiber; replace SFP; `shut/no shut` to re-enable after fixing root cause | N/A |

## Zoning

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Zone not found in active zoneset` | MDS NX-OS 8.x | Zoneset activated without the new zone included | Re-activate zoneset: `zoneset activate name <name> vsan <id>` | N/A |
| `Merge failure` between MDS switches | MDS NX-OS 8.x | Zone database conflict between switches | Resolve with `show zone merge-control vsan <id>`; manually align zone DBs | N/A |

## VSAN

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VSAN isolated after trunk link change | MDS NX-OS 8.x | VSAN not included in trunk allowed list on ISL | Add VSAN to trunk: `switchport trunk allowed vsan add <id>` | N/A |

## See also

- [Cisco MDS — Common Issues](common-issues.md)
- [Cisco DCNM — Known Issues](../../cisco-dcnm/troubleshooting/known-issues/)
