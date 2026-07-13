---
tags:
  - architecture
  - san
description: "Cisco MDS design standards: VSANs for fabric segmentation, port-channel ISL configuration, N-port virtualisation (NPV) mode, and buffer credit sizing."
---
# MDS — Standards

<div class="kb-summary">
Cisco MDS design standards: VSANs for fabric segmentation, port-channel ISL configuration, N-port virtualisation (NPV) mode, and buffer credit sizing.

*Applies to: Cisco MDS · Nexus*
</div>
![MDS — Standards](../../../../assets/san-cisco-mds-architecture-design-standards.svg)

---

## Switch Naming

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


```text title="Expected output"
Flags:  D - down        P - bundled in port-channel
        I - stand-alone p - bundled in lacp
        H - Hot-standby (LACP only)
        R - Layer3       S - Layer2
        U - in use       N - not in use, no aggregation
        f - failed to allocate aggregator

Number of channel-groups in use: 2
Number of Ethernet channels: 2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)       LACP        Fc1/1(P)   Fc1/2(P)   Fc1/3(P)   Fc1/4(P)
2      Po2(SU)       LACP        Fc1/5(P)   Fc1/6(P)

Port-channel1 is up
  Hardware is Fibre Channel
  Port WWN is 50:00:0a:09:8c:2d:45:67
  Admin port mode is F, Physical port mode is F
  Port mode trunk allowed Vsan(s) (1,10,20,100)
  Port mode is TE
  Last clearing of "show interface" counters never
  30 seconds input rate 2048000 bits/sec, 256000 bytes/sec
  30 seconds output rate 2048000 bits/sec, 256000 bytes/sec
  Received 45678901 bytes, Transmitted 43210567 bytes
  Received 234567 frames, Transmitted 232145 frames
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the exact command syntax; on some MDS firmware versions use `show port-channel summary` without additional parameters.
    **`Port-channel1 does not exist`** — Ensure the port-channel has been created with `interface port-channel 1` and members have been assigned before querying its status.
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

---

## See also

- [Mds — How It Works](../how-it-works/)
- [Mds — Integrations](../integrations/)
- [Mds — Deploy](../../deploy/)
