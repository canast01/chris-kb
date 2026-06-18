---
tags:
  - troubleshooting
  - fibre-channel
  - san
  - networking
  - known-issues
---
# Fibre Channel — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Fibre Channel issues covering HBA, fabric login, zoning, and link instability.

*Applies to: Fibre Channel fabric (Brocade / Cisco MDS), 16G / 32G FC*
</div>

```text
┌──────────────────────────────────────────── Fibre Channel ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Dedicated SAN fabric — HBA, zoning, fabric login, 16G/32G FC                 │   │
│   │                       Protocols: FC-SW (native FC) · FCP (SCSI over FC)                       │   │
│   │               Management: Switch CLI (Brocade FOS / Cisco NX-OS) / HBA software               │   │
│   │               HBA FLOGI -> Fabric login -> Zoning lookup -> Target PLOGI -> I/O               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             HBA             │  │       Host Bus Adapter      │  │       Physical FC port      │   │
│   │            Fabric           │  │        FC switch(es)        │  │     Name server, zoning     │   │
│   │            Zoning           │  │       Soft/hard zoning      │  │      WWN or port-based      │   │
│   │            Target           │  │    Storage array FC port    │  │        Presents LUNs        │   │
│   │            Fault            │  │       CRC/link errors       │  │      SFP/cable quality      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       HBA        │ Host FC connect  │       FC-SW       │   WWN identity   │Driver ver matters│   │
│   │    FC switch     │ Fabric services  │       FC-SW       │    Zoning ACL    │   Name server    │   │
│   │     Zoneset      │  Access control  │        N/A        │       N/A        │Must be activated │   │
│   │       ISL        │Inter-switch link │       FC-SW       │       N/A        │ BB credit limits │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: HBAs in hosts - FC switches/directors - array FC ports - fiber                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HBA            = Host Bus Adapter; the FC interface card in a server                                 │
│  WWN            = World Wide Name; unique 64-bit FC device identifier                                 │
│  FLOGI          = Fabric Login; HBA registers with the fabric on link-up                              │
│  PLOGI          = Port Login; device-to-device login before I/O starts                                │
│  Zoning         = SAN access control; restricts initiator/target pairs                                │
│  Zoneset        = the active collection of zones enforced on a fabric                                 │
│  Name server    = fabric service mapping WWNs to addresses                                            │
│  ISL            = Inter-Switch Link; connects two FC switches                                         │
│  BB credit      = Buffer-to-Buffer credit; FC flow control mechanism                                  │
│  F_Port         = switch port connected to a host or storage HBA                                      │
│  E_Port         = switch port connected to another switch (forms ISL)                                 │
│  LOGO           = Logout; HBA explicitly leaving the fabric                                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- HBA state: `cat /sys/class/fc_host/host*/port_state` (Linux); check HBA management software (QConvergeConsole, OneCommand Manager).
- FC errors surface as SCSI errors in OS (`dmesg | grep scsi`), storage array port stats, or switch port counters.

## HBA and Link

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| HBA port `Link Down` | Fiber broken, SFP failure, or switch port disabled | Check fiber; replace SFP; verify switch port enabled |
| `LOGO` events in switch log — HBA logging out | HBA driver crash or host reboot | Check HBA driver version; update to current stable version |
| High CRC error count on switch port | Dirty fiber connectors or faulty SFP | Clean connectors; replace SFP |
| F_Port stuck in `Initializing` | Zoning not configured for HBA WWN | Add HBA WWN to zone and activate zoneset |

## Zoning

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Host sees all storage devices (no zoning) | No zoneset active | Create zones; activate zoneset |
| Zone merge failed during ISL bring-up | Zone database conflict between switches | Resolve conflict: isolate switches; reconcile zone DBs; remerge |
| New LUN not visible after zoning | Host HBA not logged into fabric after zone add | Rescan HBA: `echo "- - -" > /sys/class/scsi_host/hostX/scan` |

## Performance

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Intermittent I/O latency spikes | ISL congestion or buffer credit depletion | Monitor BB credits on switch; add ISL bandwidth; enable BB credit recovery |
| SCSI timeouts from application | Queue depth too high or path failover taking too long | Reduce HBA queue depth; verify multipath failover time <30s |

## See also

