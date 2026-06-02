# MDS — Standards


<div class="kb-summary">
> Part of the [Cisco MDS](../../index.md) reference.
</div>

---

## Switch Naming

```text
<site>-mds-sw<nn>
```
```
┌────────────────────────────────── Cisco MDS 9000 — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│  MDS design principles: dual-fabric A/B, VSAN per workload, PortChannel ISLs, ISSU.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Fabric Design                 │  │                 VSAN Design                 │   │
│   │          Dual fabric A and B always          │  │          One VSAN per workload type         │   │
│   │       No single switch failure impact        │  │         VSAN 1 never used: reserved         │   │
│   │         ISL PortChannel: min 2 ports         │  │         Prod/dev/test separate VSAN         │   │
│   │          Over-subscription: 7:1 max          │  │         VSAN QoS: priority per VSAN         │   │
│   │          Directors: 9706/9710/9718           │  │             FCoE: separate VSAN             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Dual fabric is non-negotiable; VSAN per workload prevents blast-radius cross-talk.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Zone Design                  │  │            Operational Standards            │   │
│   │         WWN zoning: not port zoning          │  │          ISSU upgrade: all upgrades         │   │
│   │          Single initiator per zone           │  │          TACACS+ via ISE: mandatory         │   │
│   │          Alias: device name not WWN          │  │           NX-OS: < 2 versions lag           │   │
│   │         Default deny: no open zones          │  │          SNMPv3 only: disable v1/v2         │   │
│   │            Zone set: one per VSAN            │  │         Backup: config + zone daily         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS director pair (A+B) · dual supervisor per director · SFP transceivers · FC cables                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Dual fabric     = two independent FC fabrics; every host and array dual-homed                        │
│  VSAN            = Virtual SAN; one VSAN per workload (prod/dev/test separate)                        │
│  VSAN 1          = default VSAN; avoid using it; reserved for management                              │
│  PortChannel ISL = bundled ISLs; PortChannel1 is recommended minimum 2 links                          │
│  7:1             = recommended over-subscription ratio for FC storage traffic                         │
│  WWN zoning      = zone by HBA World Wide Name; survives port changes                                 │
│  Single initiator= one HBA per zone; prevents initiator-to-initiator traffic                          │
│  Device alias    = human-readable name for WWN; managed via CFS distribution                          │
│  Default deny    = no zone = no communication; strict zone policy                                     │
│  ISSU            = In-Service Software Upgrade; required for all NX-OS upgrades                       │
│  TACACS+ via ISE = Cisco ISE provides TACACS+ for all MDS admin auth                                  │
│  Zone set        = one active zone set per VSAN at a time; backup sets inactive                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## ISL Standards

| Parameter | Standard |
|---|---|
| Port-channel ISLs | Minimum 2 physical links per channel group |
| ISL speed | 32G Fibre Channel minimum for new deployments |
| Load balancing | Source-ID/Destination-ID exchange-based (`port-channel load-balance src-dst-oxid`) |
| Trunk mode | Enabled on ISL ports: `switchport trunk mode on` |

Verify port-channel ISL:
```bash
show port-channel summary
show interface san-port-channel 1
```

## AAA / Authentication Standards

| Control | Standard |
|---|---|
| AAA | TACACS+ primary, RADIUS fallback |
| Local accounts | Break-glass only; one local admin per fabric |
| Role | `network-admin` for infrastructure team; `network-operator` for read-only |
| TACACS+ encryption | Enable key encryption: `tacacs-server key 7 <encrypted>` |

## NX-OS Version Standards

- All MDS switches in a fabric must run the same NX-OS major release (e.g., 9.2.x)
- Apply maintenance releases to Fabric B first, validate, then Fabric A
- Minimum: stay within N-2 of Cisco's current MDS NX-OS release
- Check EOL/EOS: [cisco.com/go/eos](https://www.cisco.com/c/en/us/products/eos-eol-policy.html)

## SNMP Standards

- SNMPv3 only; SNMPv1/v2 disabled
- Auth protocol: SHA; Privacy protocol: AES-128 minimum
- Community strings (if SNMPv2 legacy required): in vault, quarterly rotation
- SNMP trap receiver: Nexus Dashboard or Aria Operations collector

## Cisco NDFC Integration

All MDS switches should be managed through Cisco NDFC (Nexus Dashboard Fabric Controller):
- Fabric discovery: NDFC discovers switches via SSH/SNMP
- SAN fabric view: topology, VSAN health, ISL utilisation
- Zone management: preferred over per-switch CLI for large fabrics
