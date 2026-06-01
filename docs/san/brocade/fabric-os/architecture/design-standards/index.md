# FabricOS — Standards


<div class="kb-summary">
> Part of the [Architecture](../index.md) reference.
</div>

---

## Switch Naming

```text
<site>-san-sw<nn>
```
```
┌──────────────────────────────── Brocade Fabric OS — Design Standards ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FOS design standards for production SAN: topology, naming, ISL sizing, HA, security      │   │
│   │        Topology: dual-fabric A/B design; no single-fabric dependency for storage access       │   │
│   │         Domain IDs: statically assigned; Fabric A starts at 1, Fabric B starts at 100         │   │
│   │         ISL sizing: minimum 2 ISLs per switch pair; trunk for bandwidth and redundancy        │   │
│   │       Zone naming: host_alias_storage_alias format; no generic zone names in production       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Topology standards -> naming conventions -> ISL design -> HA and redundancy rules                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Topology          │  │         Naming / IDs        │  │           HA / ISL          │   │
│   │       Dual fabric A/B       │  │      Static domain IDs      │  │          Min 2 ISLs         │   │
│   │       Core-edge design      │  │       Zone naming std       │  │         ISL trunking        │   │
│   │       No single fabric      │  │        Alias per HBA        │  │        Director core        │   │
│   │        Separate VSANs       │  │        Config naming        │  │        Redundant PSU        │   │
│   │       Buffer planning       │  │       FW rev tracking       │  │        OOB mgmt path        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Core switches (directors) connect to all edge switches; no edge-to-edge ISLs                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Standard     │       Rule       │     Rationale     │       Tool       │      Notes       │   │
│   │   Dual fabric    │    A+B always    │    HA for hosts   │  Multi-pathing   │  MPIO required   │   │
│   │    Domain ID     │  Static assign   │   Predictability  │     portcfg      │  A=1-99, B=100+  │   │
│   │    ISL trunk     │  Min 2 per pair  │     Redundancy    │    SANnav/CLI    │ Same speed ISLs  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: dual directors at core · edge switches per row · redundant ISL paths                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dual fabric    = Two independent FC fabrics (A and B); each host has one HBA in each               │
│    Core-edge      = Directors at core; fixed-port switches at edge; no edge-to-edge ISLs              │
│    Domain ID      = Statically assigned switch identifier; dynamic assignment risks reconfiguring     │
│    ISL trunk      = Bundled ISLs between same switch pair for bandwidth and redundancy                │
│    Zone naming    = Standard: srvname_hba0_arrayname_sp0; enables instant identification              │
│    Alias          = WWN alias per HBA port; one alias per physical port, not per LUN                  │
│    Buffer credit  = Must be planned for long-distance ISLs; insufficient credits cause congestion     │
│    MPIO           = Multi-path I/O on host; uses both fabric A and B paths for redundancy             │
│    OOB mgmt       = Out-of-band Ethernet management must be redundant and always accessible           │
│    PSU redundancy = Each switch/director must have redundant power supplies from separate PDUs        │
│    FW tracking    = Firmware version matrix maintained; all switches in fabric same minor version     │
│    Config naming  = Zone config names include date/ticket reference for auditability                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

---

## Security Standards

| Control | Standard |
|---|---|
| SNMP | SNMPv3 only; community strings in vault; quarterly rotation |
| Management access | SSH only; Telnet disabled; `sshutil disable telnet` |
| RADIUS/TACACS+ | All fabrics must use central AAA; local accounts for break-glass only |
| Audit logging | `auditcfg --set 1` — all logins and config changes logged |

---

## Firmware Standards

- All switches in a fabric must run the same Fabric OS version (FOS)
- New FOS versions applied to Fabric B first, validated, then Fabric A
- Minimum: stay within 1 major FOS version of Broadcom's current release
- Check FOS EOL: [support.broadcom.com](https://support.broadcom.com) → Product Lifecycle
