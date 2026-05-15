# Cisco MDS

<div class="kb-summary">
Cisco MDS 9000 series switches knowledge base covering fabric architecture, zoning, VSANs, ISLs, CLI references, health checks, scripts, and troubleshooting guides for Fibre Channel SAN environments.
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>

## Overview

Cisco MDS 9000 series switches are purpose-built enterprise Fibre Channel SAN switches running NX-OS for SAN. The platform spans fixed-configuration switches (MDS 9132T, 9148T, 9396T) and modular directors (MDS 9706, 9710) capable of hundreds of 32G/64G FC ports per chassis.

The defining feature of the MDS platform is **VSAN (Virtual SAN)** — each physical fabric can host multiple independent logical fabrics, each with its own FC Name Server, domain ID space, zoning database, and FLOGI table. This allows production, replication, and test traffic to share physical infrastructure with complete isolation.

MDS fabrics are managed per-switch via NX-OS CLI or centrally via **Cisco NDFC (Nexus Dashboard Fabric Controller)**, which provides topology visibility, zone management, firmware orchestration, and SAN analytics.

---

## Platform Summary

| Model | Form Factor | Max FC Ports | Key Feature |
|---|---|---|---|
| MDS 9132T | 1U fixed | 32x 32G FC | Entry-level, NPV capable |
| MDS 9148T | 2U fixed | 48x 32G FC | Mid-range |
| MDS 9396T | 2U fixed | 96x 32G FC | High-density fixed |
| MDS 9706 | Director 6-slot | Up to 384x 32G FC | Modular director, ISSU |
| MDS 9710 | Director 10-slot | Up to 576x 32G FC | Large-scale director, ISSU |

Directors (9706/9710) support **ISSU (In-Service Software Upgrade)** — non-disruptive NX-OS upgrades when dual supervisors are installed. Fixed-configuration switches require a reload for NX-OS upgrades.

---

## Key Concepts

| Concept | Description |
|---|---|
| VSAN | Virtual SAN — logical fabric isolation on shared physical hardware |
| Zoning | Controls which initiators (hosts) can communicate with which targets (storage) |
| FLOGI | Fabric Login — the handshake a device uses to join the SAN fabric |
| FCID | Fabric-assigned address assigned to each logged-in device |
| FCNS | FC Name Server — directory of all logged-in devices per VSAN |
| ISL | Inter-Switch Link — connects two MDS switches to form a multi-switch fabric |
| TE Port | Trunking E_Port — carries multiple VSANs over a single ISL |
| Port Channel | Aggregated ISL group for bandwidth and redundancy |
| Device Alias | Human-readable name mapped to a port WWN (pWWN) |
| Enhanced Zoning | Default-deny zoning mode — only explicitly zoned devices can communicate |
| CFS | Cisco Fabric Services — distributes config (device aliases, zoning) across switches |
| IVR | Inter-VSAN Routing — allows controlled routing between VSANs |
| FCIP | Fibre Channel over IP — FC tunneling over WAN/DWDM for DR replication |
| ISSU | In-Service Software Upgrade — non-disruptive NX-OS upgrade on directors |

---

## Daily Checks

| Check | Command | Expected |
|---|---|---|
| FC interfaces up | `show interface brief` | All connected FC ports in `up` state |
| Devices logged in | `show flogi database` | All expected host HBAs and storage targets present |
| Fabric topology | `show topology` | ISLs all up; topology matches design |
| Active zoning | `show zoneset active vsan all` | Active zoneset name and members match expected |
| Recent log events | `show logging last 50` | No `critical` or `error`-level entries |
| Hardware health | `show environment` | PSUs, fans, and temperature all normal |

```bash
# Quick fabric health sweep
show interface brief
show flogi database
show topology
show zoneset active vsan all
show logging last 50
show environment
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
| Zone a new host | [Procedures — Zoning](operations/procedures/) |
| Troubleshoot a down FC port | [Troubleshooting — Common Issues](troubleshooting/common-issues/) |
| Run NX-OS upgrade | [Install & Upgrade](operations/install-upgrade/) |
| Backup / restore config | [Backup & Restore](operations/backup-restore/) |
| Full CLI reference | [CLI Reference](operations/cli-reference/) |
| Automation scripts | [Scripts](operations/scripts/) |
| Security hardening | [Security — Hardening](security/hardening/) |
