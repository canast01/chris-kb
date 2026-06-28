---
tags:
  - certifications
  - san
---
# SAN Practice Notes

<div class="kb-summary">
SAN Practice Notes reference covering Zoning Exam Questions, Fabric Login Sequence — Common Error Scenarios, Common Wrong Answers to Avoid, Key Numbers to Memorize, Quick Reference: Brocade vs Cisco Terminology and 1 more sections.
</div>

## Zoning Exam Questions

Most SAN exam zoning questions test:
1. Whether to use WWPN zoning vs port (domain:port) zoning
2. Single-initiator single-target vs single-initiator multi-target zone design
3. What happens when a zone set is not activated
4. Hard vs soft zoning enforcement

| Question Type | Key Discriminator | Correct Answer Direction |
|---|---|---|
| "Zone change not taking effect" | Zone set activation | Zone DB changes require zone set activation to take effect |
| "New HBA added, no access" | WWPN must be in zone | Add new WWPN to zone and re-activate zone set |
| "Maximum security" | Hard zoning | Hard zoning enforced in hardware; soft zoning in Name Server only |
| "HBA replaced" | WWPN changes | WWPN-based zones must be updated; port zoning survives HBA swap |
| "Zone on wrong switch" | Fabric-wide zone DB | Zone DB is distributed across the fabric via RSCNs |

## Fabric Login Sequence — Common Error Scenarios

| Symptom | Likely Cause | Investigation Step |
|---|---|---|
| Host not visible in Name Server | FLOGI not completing | Check for Domain ID conflict; verify F_Port link |
| Host cannot see target LUN | Zone not including both WWPN | Check active zone set for both initiator and target WWPN |
| Intermittent I/O errors | ISL congestion or BB_Credit exhaustion | Check ISL utilization; check buffer-to-buffer credits |
| Fabric segmentation | Domain ID conflict during switch merge | Verify domain IDs are unique before connecting switches |
| RSCN storm | Too many devices logging in/out | Check for flapping links; consider RSCN fencing per-zone |

## Common Wrong Answers to Avoid

- **Zone set = zone**: A zone set is a collection of zones. Activating a zone set activates all zones in it. Only one zone set can be active at a time per fabric.
- **WWNN for zoning**: Always zone by WWPN. WWNN identifies the HBA card; WWPN identifies each individual port.
- **Soft zoning = same security as hard**: Soft zoning only prevents Name Server queries; a host with a direct FCID can still communicate. Hard zoning blocks at the ASIC level.
- **ISL and E_Port are different things**: E_Port is the port type; ISL is the link between two E_Ports. A trunked ISL uses TE_Ports.
- **Domain ID range**: Valid domain IDs are 1–239. Exam questions sometimes include 0 or 240+ as wrong options.

## Key Numbers to Memorize

| Parameter | Value |
|---|---|
| FCID bit width | 24 bits (Domain 8 + Area 8 + Port 8) |
| Valid domain ID range | 1–239 |
| Max switches in a single FC fabric | 239 |
| FC frame max payload | 2112 bytes |
| BB_Credit default (Brocade) | 16 |
| FC-16G line rate | 14.025 Gbps (usable after 64B/66B encoding) |
| WWPN length | 64 bits (8 bytes), displayed as 16 hex digits |

## Quick Reference: Brocade vs Cisco Terminology

| Concept | Brocade (FOS) | Cisco (NX-OS / MDS) |
|---|---|---|
| Virtual fabric | Virtual Fabric (VF) | VSAN |
| ISL trunking | ISL Trunking | PortChannel |
| Zone database | Zone DB | Zone DB |
| Principal switch | Fabric Principal | Principal Switch |
| Admin command | CLI: `switchshow`, `zoneshow` | CLI: `show flogi database`, `show zone` |

## Study Checklist

- [ ] Practice 10 zoning scenario questions and identify the zone set activation trap
- [ ] Memorize FCID structure (24-bit = Domain + Area + Port)
- [ ] Know the difference between hard and soft zoning enforcement
- [ ] Understand why WWPN changes when an HBA is replaced
- [ ] Review Brocade and Cisco equivalent terminology
- [ ] Study RSCN behavior and when RSCN fencing is beneficial
