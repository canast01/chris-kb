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
┌────────────────────────────────────────────── Cisco MDS ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Multilayer Director Switch — enterprise FC SAN switching on NX-OS               │   │
│   │           Protocols: Fibre Channel · FCIP (FC over IP) · iSCSI · FCoE (select SKUs)           │   │
│   │               Management: NX-OS CLI (SSH) · Cisco DCNM / NDFC · SNMP v3 · syslog              │   │
│   │            Host FLOGI -> VSAN assigned -> zone lookup -> storage target accessible            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Fabric           │  │             VSAN            │  │      Isolated FC fabric     │   │
│   │            Zoning           │  │     Zone set (per VSAN)     │  │      WWN or fcid scoped     │   │
│   │           Trunking          │  │         Port-channel        │  │     LACP-like ISL bundle    │   │
│   │          Extension          │  │         FCIP tunnel         │  │       FC over WAN / IP      │   │
│   │             IVR             │  │      Inter-VSAN routing     │  │      Cross-VSAN access      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       VSAN       │ Fabric partition │    FC per VSAN    │  Domain-scoped   │Isolated fwd plane│   │
│   │     Zone set     │  Access control  │     FC fabric     │    WWN / FCID    │1 active per VSAN │   │
│   │       FCIP       │  WAN extension   │     TCP (3225)    │       N/A        │ISL over IP tunnel│   │
│   │       IVR        │Cross-VSAN routing│         FC        │     CFS sync     │IVR zone required │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: host HBA -> MDS port (FC) -> VSAN fabric -> target storage array port                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VSAN         = Virtual SAN; logical isolation of ports within one physical switch                    │
│  Zone set     = named group of zones activated together within a VSAN                                 │
│  FCID         = Fibre Channel ID; 24-bit address assigned on FLOGI                                    │
│  Port-channel = bonded ISL group for bandwidth and redundancy between MDS switches                    │
│  FCIP         = Fibre Channel over IP; extends FC over routed IP WAN links                            │
│  IVR          = Inter-VSAN Routing; controlled cross-VSAN resource sharing                            │
│  CFS          = Cisco Fabric Services; distribution layer for IVR and zoning                          │
│  FSPF         = Fabric Shortest Path First; FC routing protocol on MDS                                │
│  NX-OS        = Cisco network OS powering MDS; CLI and config syntax                                  │
│  SPAN         = Switched Port ANalyzer; port mirroring for traffic capture                            │
│  NPIV         = N-Port ID Virtualization; multiple WWNs per physical HBA port                         │
│  show flogi database = NX-OS command listing all logged-in initiators and targets                     │
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
