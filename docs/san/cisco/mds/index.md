---
tags:
  - san
---
# Cisco MDS

<div class="kb-summary">
Cisco MDS 9000 series switches knowledge base covering fabric architecture, zoning, VSANs, ISLs, CLI references, health checks, scripts, and troubleshooting guides for Fibre Channel SAN environments.

*Applies to: Cisco MDS · Nexus*
</div>

<div class="kb-grid kb-grid-2">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>VSAN design, ISL topology, FCoE gateway, and FCIP WAN extension.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Zone management, ISSU firmware upgrades, health monitoring, and backup.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>RBAC, TACACS+, DH-CHAP, SNMPv3, and AES-256 link encryption.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Port issues, VSAN isolation, domain conflicts, and ISL problems.</span>
</a>

</div>

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
| Zone a new host | [Procedures — Zoning](operations/procedures//) |
| Troubleshoot a down FC port | [Troubleshooting — Common Issues](troubleshooting/common-issues//) |
| Run NX-OS upgrade | [Install & Upgrade](operations/install-upgrade//) |
| Backup / restore config | [Backup & Restore](operations/backup-restore//) |
| Full CLI reference | [CLI Reference](operations/cli-reference//) |
| Automation scripts | [Scripts](operations/scripts//) |
| Security hardening | [Security — Hardening](security/hardening//) |
