---
tags:
  - troubleshooting
  - cisco-dcnm
  - san
  - known-issues
---
# Cisco DCNM — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Cisco DCNM (Data Center Network Manager) bugs, error codes, and workarounds covering switch discovery, deployment, and licensing.

*Applies to: Cisco DCNM 11.x / NDFC 12.x*
</div>

```text
┌───────────────────────────────────────────── Cisco DCNM ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Data Center Network Manager — LAN and SAN fabric management platform             │   │
│   │               Protocols: SNMP v3 · SSH · REST API · HTTPS (UI) · NX-API · syslog              │   │
│   │            Management: DCNM web UI · REST API · CLI; migrated to NDFC in NX-OS 10.x           │   │
│   │           Switch discovery -> fabric inventory -> zone set push -> traffic analytics          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Control           │  │         DCNM server         │  │    Linux OVA / bare-metal   │   │
│   │          LAN fabric         │  │         NX-OS fabric        │  │     VXLAN/EVPN templates    │   │
│   │          SAN fabric         │  │        MDS zone sets        │  │       VSAN + zone push      │   │
│   │          Discovery          │  │        CDP/SNMP scan        │  │       Seed IP required      │   │
│   │          Analytics          │  │         SAN Insights        │  │    Latency + I/O metrics    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   DCNM server    │Fabric management │     HTTPS 443     │   LDAP / local   │OVA or ISO install│   │
│   │       POAP       │ Zero-touch boot  │    DHCP + TFTP    │       N/A        │ NX-OS auto-boot  │   │
│   │   SAN Insights   │  I/O analytics   │      Internal     │    Role-based    │NX-OS lic. needed │   │
│   │     Zone set     │SAN access control│     FC / FCIP     │   VSAN scoped    │1 active set/VSAN │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: DCNM server -> managed Cisco MDS/Nexus switches -> hosts + storage arrays                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DCNM         = Data Center Network Manager; Cisco fabric management platform                         │
│  NDFC         = Nexus Dashboard Fabric Controller; successor to DCNM                                  │
│  POAP         = Power-On Auto Provisioning; zero-touch NX-OS bootstrap                                │
│  SAN Insights = DCNM analytics: per-flow latency and I/O throughput from MDS                          │
│  Zone set     = named collection of zones activated together in a VSAN                                │
│  VSAN         = Virtual SAN; logical partitioning of a Cisco FC fabric                                │
│  Fabric template = DCNM/NDFC config skeleton defining VXLAN/BGP overlay params                        │
│  NX-API       = Cisco REST API on NX-OS switches for programmatic config                              │
│  CDP          = Cisco Discovery Protocol; used by DCNM to map switch topology                         │
│  Federation   = linking multiple DCNM servers to manage a larger fabric                               │
│  SNMP trap    = alert pushed from switch to DCNM on threshold or port event                           │
│  Performance  = DCNM built-in port utilisation and error-rate trending                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- DCNM errors appear in the DCNM Dashboard → Alarms.
- DCNM → Administration → Logs for service-level diagnostics.
- Most discovery failures are SSH or SNMP connectivity issues.

## Switch Discovery

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot discover switch — SSH timeout` | DCNM 11.x | TCP 22 blocked from DCNM to switch management IP | Verify TCP 22 from DCNM server to switch management IP | N/A |
| Switch discovered but showing `Out of Sync` | DCNM 11.x | Config in DCNM DB doesn't match live switch config | Trigger sync: DCNM → Inventory → Devices → right-click → Sync | N/A |

## Deployment

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Config deployment fails: `Cannot push to switch` | DCNM 11.x | DCNM write credentials (SSH) no longer valid | Update switch credentials in DCNM → Administration → Credentials | N/A |
| `Deployment preview differs from expected` | DCNM 11.x | Manual change made directly on switch (out-of-band) | Review diff in DCNM; reconcile with `Recalculate` before deploying | N/A |

## See also

- [Cisco DCNM — Common Issues](common-issues/)
- [Cisco MDS — Known Issues](../../mds/troubleshooting/known-issues.md)
- [Cisco Nexus Dashboard — Known Issues](../../nexus-dashboard/troubleshooting/known-issues.md)
