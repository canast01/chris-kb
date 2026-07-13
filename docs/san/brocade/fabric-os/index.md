---
tags:
  - san
description: "Brocade Fabric OS knowledge base covering switch architecture, zoning, ISLs, ports, firmware, CLI references, health checks, scripts, and troubleshooting..."
---
# Brocade Fabric OS

<div class="kb-summary">
Brocade Fabric OS knowledge base covering switch architecture, zoning, ISLs, ports, firmware, CLI references, health checks, scripts, and troubleshooting guides for Fibre Channel SAN environments.

*Applies to: Brocade FOS 9.x*
</div>

<div class="kb-grid kb-grid-2">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>FC services, fabric layer, zone DB sync, and management interfaces.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Health checks, zone management, firmware download, and maintenance.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>DH-CHAP, FCSM, LDAP auth, SNMPv3, and access control hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Port diagnostics, fabric segmentation, ISL issues, and TAC escalation.</span>
</a>

</div>

---

## Platform Summary

| Platform | Type | Max FC Ports | FC Speed | Notes |
|---|---|---|---|---|
| G610 | Fixed | 24x | 32G | Entry-level fixed switch |
| G620 | Fixed | 64x | 32G | Mid-range workhorse |
| G720 | Fixed | 64x | 64G | High-performance fixed |
| G730 | Fixed | 64x | 64G | High-performance, latest gen |
| X7-4 | Director | Up to 192 | 32G/64G | 4-slot director — dual CP |
| X7-8 | Director | Up to 384 | 32G/64G | 8-slot director — dual CP |
| SAN256B-7 | Director | Up to 256 | 64G | High-density director |

Directors (X7-4, X7-8, SAN256B-7) support non-disruptive firmware upgrades via dual Control Processors (CPs). Fixed-form switches (G-series) require a reboot to apply firmware — always upgrade one fabric while the other carries traffic.
