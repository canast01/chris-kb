# Cisco MDS

<div class="kb-summary">
Cisco MDS 9000 series switches knowledge base covering fabric architecture, zoning, VSANs, ISLs, CLI references, health checks, scripts, and troubleshooting guides for Fibre Channel SAN environments.
</div>

```
┌────────────────────────────────────── Cisco MDS 9000 — Overview ──────────────────────────────────────┐
│                                                                                                       │
│  MDS 9000: Cisco enterprise FC/FCoE switch family. Modular directors and fixed switches.              │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Product Family       │  │       Key Capabilities      │  │          Management         │   │
│   │   9706/9710/9718 directors  │  │     FC 32/64G port speed    │  │     DCNM: GUI + REST API    │   │
│   │  9148T fixed 48-port switch │  │  VSAN: logical segmentation │  │        NX-OS CLI: SSH       │   │
│   │  9132T 32-port fixed switch │  │  FCoE: Fibre Chan over Eth  │  │       SNMP v3 polling       │   │
│   │  9700 high-density director │  │   FICON: mainframe support  │  │       NetConf/gRPC API      │   │
│   │     HA: dual supervisors    │  │     D-Port: diagnostics     │  │     TACACS+/RADIUS auth     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  MDS 9000 is the Cisco flagship FC switch; VSAN and zoning are core SAN functions.                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │         VSAN design         │  │       Zone management       │  │        RBAC + TACACS+       │   │
│   │      ISL / PortChannel      │  │        Firmware ISSU        │  │     DH-CHAP switch auth     │   │
│   │         FSPF routing        │  │      Health monitoring      │  │         SNMPv3 only         │   │
│   │         FCoE gateway        │  │     Performance analysis    │  │       AES-256 link enc      │   │
│   │      FCIP for DWDM WAN      │  │        Backup/restore       │  │     CFS security policy     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS director chassis · line cards/blades · dual supervisors · SFP transceivers · FC cables           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VSAN            = Virtual SAN; logical FC fabric on MDS; isolates traffic by VSAN ID                 │
│  Zoning          = FC access control; defines which initiators can see which targets                  │
│  ISL             = Inter-Switch Link; E_Port connection between two FC switches                       │
│  PortChannel     = aggregated ISL bundle; increases bandwidth and provides redundancy                 │
│  FSPF            = Fabric Shortest Path First; FC routing protocol for path selection                 │
│  ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic disruption              │
│  FCoE            = Fibre Channel over Ethernet; FC protocol encapsulated in 10/25GbE                  │
│  FICON           = Fibre Connection; IBM mainframe I/O protocol over FC fabric                        │
│  FCIP            = Fibre Channel over IP; FC frames tunnelled over IP/WAN                             │
│  DH-CHAP         = Diffie-Hellman CHAP; ISL authentication between MDS switches                       │
│  CFS             = Cisco Fabric Services; distributes config across fabric                            │
│  D-Port          = diagnostic port; tests link signal quality and latency                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── Cisco MDS 9000 — Overview ──────────────────────────────────────┐
│                                                                                                       │
│  MDS 9000: Cisco enterprise FC/FCoE switch family. Modular directors and fixed switches.              │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Product Family       │  │       Key Capabilities      │  │          Management         │   │
│   │   9706/9710/9718 directors  │  │     FC 32/64G port speed    │  │     DCNM: GUI + REST API    │   │
│   │  9148T fixed 48-port switch │  │  VSAN: logical segmentation │  │        NX-OS CLI: SSH       │   │
│   │  9132T 32-port fixed switch │  │  FCoE: Fibre Chan over Eth  │  │       SNMP v3 polling       │   │
│   │  9700 high-density director │  │   FICON: mainframe support  │  │       NetConf/gRPC API      │   │
│   │     HA: dual supervisors    │  │     D-Port: diagnostics     │  │     TACACS+/RADIUS auth     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  MDS 9000 is the Cisco flagship FC switch; VSAN and zoning are core SAN functions.                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │         VSAN design         │  │       Zone management       │  │        RBAC + TACACS+       │   │
│   │      ISL / PortChannel      │  │        Firmware ISSU        │  │     DH-CHAP switch auth     │   │
│   │         FSPF routing        │  │      Health monitoring      │  │         SNMPv3 only         │   │
│   │         FCoE gateway        │  │     Performance analysis    │  │       AES-256 link enc      │   │
│   │      FCIP for DWDM WAN      │  │        Backup/restore       │  │     CFS security policy     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS director chassis · line cards/blades · dual supervisors · SFP transceivers · FC cables           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VSAN            = Virtual SAN; logical FC fabric on MDS; isolates traffic by VSAN ID                 │
│  Zoning          = FC access control; defines which initiators can see which targets                  │
│  ISL             = Inter-Switch Link; E_Port connection between two FC switches                       │
│  PortChannel     = aggregated ISL bundle; increases bandwidth and provides redundancy                 │
│  FSPF            = Fabric Shortest Path First; FC routing protocol for path selection                 │
│  ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic disruption              │
│  FCoE            = Fibre Channel over Ethernet; FC protocol encapsulated in 10/25GbE                  │
│  FICON           = Fibre Connection; IBM mainframe I/O protocol over FC fabric                        │
│  FCIP            = Fibre Channel over IP; FC frames tunnelled over IP/WAN                             │
│  DH-CHAP         = Diffie-Hellman CHAP; ISL authentication between MDS switches                       │
│  CFS             = Cisco Fabric Services; distributes config across fabric                            │
│  D-Port          = diagnostic port; tests link signal quality and latency                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Upgrade Workflow Summary

1. Confirm both fabrics are healthy: `show interface brief`, `show flogi database`
2. Back up running configuration: `copy running-config scp://<server>/<path>/mds-<hostname>-<date>.cfg`
3. Save a named checkpoint: `checkpoint pre-upgrade`
4. Verify target NX-OS is HCL-compatible with connected HBA drivers and storage microcode
5. For directors (9706/9710): confirm dual supervisors active and use ISSU for non-disruptive upgrade
6. For fixed switches: schedule a maintenance window — `install all` reloads the switch
7. Upgrade Fabric B first; validate; then Fabric A
8. Post-upgrade: `show version`, `show interface brief`, `show zoneset active vsan all`

---

## Operational Reference

| Task | Go To |
|---|---|
| Zone a new host | [Procedures — Zoning](operations/procedures/index.md) |
| Troubleshoot a down FC port | [Troubleshooting — Common Issues](troubleshooting/common-issues/index.md) |
| Run NX-OS upgrade | [Install & Upgrade](operations/install-upgrade/index.md) |
| Backup / restore config | [Backup & Restore](operations/backup-restore/index.md) |
| Full CLI reference | [CLI Reference](operations/cli-reference/index.md) |
| Automation scripts | [Scripts](operations/scripts/index.md) |
| Security hardening | [Security — Hardening](security/hardening/index.md) |
