---
tags:
  - troubleshooting
  - brocade
  - fabric-os
  - san
  - known-issues
---
# Brocade Fabric OS — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Fabric OS bugs, error codes, and workarounds covering switch health, zoning, and ISL issues.

*Applies to: Fabric OS 9.x*
</div>

```text
┌────────────────────────────────────────── Brocade Fabric OS ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             FC SAN switch OS — zoning, NPIV, ISL trunking, port health monitoring             │   │
│   │                Protocols: Fibre Channel (E/F/N-port) · FCIP · FSPF path routing               │   │
│   │              Management: FOS CLI (SSH) · Brocade Network Advisor · SNMP · syslog              │   │
│   │              Host FLOGI -> fabric login -> zoning lookup -> target access granted             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Fabric           │  │       Principal switch      │  │       Elects Domain ID      │   │
│   │            Zoning           │  │     Zone config / alias     │  │     WWN or port-ID based    │   │
│   │             ISL             │  │         E-port trunk        │  │     FSPF routes over ISL    │   │
│   │             NPIV            │  │       Virtual N-ports       │  │      Multiple WWNs/HBA      │   │
│   │            Health           │  │        MAPS / RASlog        │  │    Port error thresholds    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   Zone config    │  Access control  │     FC fabric     │  WWN / port ID   │One active config │   │
│   │    ISL trunk     │ Switch-to-switch │     FC E-port     │   Domain trust   │FSPF load-balances│   │
│   │   MAPS policy    │Port health alerts│      Internal     │       RBAC       │ Alert thresholds │   │
│   │     FOS CLI      │Switch management │        SSH        │    Admin user    │ fw-download cmd  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: host HBA -> FC switch (Fabric OS) -> ISL trunk -> target switch -> storage array           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FLOGI        = Fabric LOGIn; HBA registers WWN with fabric, receives FC address                      │
│  PLOGI        = Port LOGIn; initiator opens session to a specific target port                         │
│  WWN          = World Wide Name; 8-byte unique ID for HBA or storage port                             │
│  Domain ID    = fabric-unique switch number (1-239) assigned by principal switch                      │
│  Zoning       = access control defining which initiators can reach which targets                      │
│  ISL          = Inter-Switch Link; E-port connection between two FC switches                          │
│  FSPF         = Fabric Shortest Path First; FC routing protocol for path selection                    │
│  NPIV         = N-Port ID Virtualization; multiple virtual WWNs per physical HBA                      │
│  MAPS         = Monitoring and Alerting Policy Suite; port-error health thresholds                    │
│  RASlog       = Reliability/Availability/Serviceability log; FOS event log                            │
│  VF           = Virtual Fabric; logical chassis partitioning into multiple fabrics                    │
│  firmwaredownload = FOS command to stage and activate a new Fabric OS version                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Run `switchshow` for port status; `fabricshow` for fabric topology.
- `supportshow` generates full diagnostic output for support escalation.
- FOS RAS messages are logged in `errdump` — check for persistent error patterns.

## Switch and Port Health

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Port `Faulty` state | FOS 9.x | SFP fault, dirty connector, or link training failure | Clean SFP; replace SFP; run `portdisable/portenable` to re-init | N/A |
| `Too many errors — port disabled` | FOS 9.x | CRC error count threshold exceeded on port | Check fiber connector; replace SFP; inspect cable | N/A |
| F_Port stuck in `Initializing` | FOS 9.x | HBA not completing FLOGI | Check zoning for HBA WWN; verify HBA driver; check `nsshow` for login | N/A |

## Zoning

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Zone not found` after fabric merge | FOS 9.x | Zone databases conflict during merge; merge aborted | Resolve zone conflict: `cfgshow` on both switches; manually align zone DBs | N/A |
| Host sees extra devices after zoning change | FOS 9.x | Host HBA cached old RSCNs; did not re-query name server | Rescan HBA on host: `echo "- - -" > /sys/class/scsi_host/hostX/scan` | N/A |

## ISL / Trunking

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| ISL `Offline` after maintenance | FOS 9.x | ISL port disabled; or speed mismatch between switches | Verify speed: `portcfgspeed`; re-enable ISL port | N/A |
| FSPF routing suboptimal — traffic not using fastest ISL | FOS 9.x | FSPF cost metric not reflecting ISL bandwidth | Set FSPF link cost proportional to bandwidth: `linkCost` command | N/A |

## See also

- [Brocade Fabric OS — Common Issues](common-issues.md)
- [Brocade SANnav — Known Issues](../../sannav/troubleshooting/known-issues/)
