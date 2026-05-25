# Aria Operations — Install & Upgrade

```text
Aria Operations — Upgrade Paths
┌─────────────────────────────────────────────────────┐
│  Option A: Aria Suite Lifecycle (Recommended)       │
│                                                     │
│  Aria LCM → Lifecycle Operations                    │
│  → select environment → Upgrade                     │
│  → select target version from marketplace           │
│  → run pre-upgrade health checks                    │
│  → LCM upgrades nodes in sequence:                  │
│                                                     │
│    Data nodes → Replica → Primary                   │
│    (primary always last)                            │
└──────────────────────────┬──────────────────────────┘
                           │ or
                           ▼
┌─────────────────────────────────────────────────────┐
│  Option B: In-Product Upgrade (Standalone)          │
│                                                     │
│  Admin → Software Update → Upload PAK               │
│  → Run pre-check → Proceed                          │
│                                                     │
│  Air-gap:                                           │
│  vracli software-update install --file <pak>        │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  Pre-Upgrade Gate (must pass before proceeding)     │
│  ✔ All nodes Online (Admin → Cluster Management)    │
│  ✔ All adapters Collecting                          │
│  ✔ Disk < 70% on /storage/db                        │
│  ✔ NTP delta < 1s on all nodes                      │
│  ✔ VM snapshots taken (revert window)               │
│  ✔ Backup completed within last 24h                 │
└─────────────────────────────────────────────────────┘
```

## Version History and Rebranding

| Product Name | Version | Notes |
|-------------|---------|-------|
| vRealize Operations Manager | 8.0 – 8.6 | Legacy name |
| VMware Aria Operations | 8.10 – 8.18 | Rebranded Q3 2022 |

> Check the [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com/) for supported vSphere versions per Aria Operations release.

---

## Upgrade Paths

### Via Aria Suite Lifecycle (Recommended)

1. Log in to Aria Suite Lifecycle (LCM) → **Lifecycle Operations**
2. Select the environment containing Aria Operations
3. Click **Upgrade** and select the target version from the marketplace
4. Run pre-upgrade health checks
5. Follow the LCM wizard — nodes are upgraded in sequence (data nodes → replica → primary)

### In-Product Upgrade Wizard (Standalone)

1. Log in to Aria Operations UI → **Administration > Software Update**
2. Upload the PAK file or point to the online repository
3. Run pre-check validation
4. Proceed with upgrade

### Manual PAK File (Air-gap)

```bash
# Download PAK from Broadcom Customer Connect
# Upload via UI: Administration > Software Update > Upload PAK
# Or SCP to appliance and trigger via CLI:
vracli software-update install --file /tmp/VMware-vRealize-Operations-<version>.pak
```

---

## Interoperability Matrix

| Aria Operations | vSphere / ESXi | NSX-T | vSAN |
|-----------------|---------------|-------|------|
| 8.18 | 7.0 U3+, 8.0+ | 4.x | 8.0+ |
| 8.16 | 7.0 U2+, 8.0 | 4.x | 7.0+ |
| 8.14 | 7.0 U1+, 8.0 | 3.x, 4.x | 7.0+ |

> Always verify against the official interop matrix before upgrading.

---

## EOL Tracking

| Version | GA Date | EOL Date |
|---------|---------|----------|
| vROps 8.6.x | 2021-10 | Per Broadcom lifecycle policy |
| vROps 8.10.x | 2022-10 | Per Broadcom lifecycle policy |
| Aria Operations 8.14+ | 2023+ | Check Broadcom lifecycle page |

Reference: [Broadcom Lifecycle Policy](https://support.broadcom.com/lifecycle-management)

---

## Pre-Upgrade Checklist

- [ ] Current version and target version interoperability verified
- [ ] Snapshot of all cluster VMs taken (revert window)
- [ ] Cluster health shows all nodes **Online**
- [ ] All adapter instances show **Collecting**
- [ ] PAK file or LCM repository access confirmed
- [ ] Maintenance window scheduled; alert notification sent
- [ ] Backup of custom dashboards, alert definitions, and super metrics exported

---

## Post-Upgrade Validation

- [ ] Cluster management page shows all nodes **Online**
- [ ] All adapters resume collecting (allow 15–30 min after upgrade)
- [ ] UI version string matches target in Administration > About
- [ ] Dashboards and alerts still present
- [ ] Custom content (super metrics, views) intact

---

## Related Sections

- [Architecture](../../architecture/index.md) — node roles
- [Operations](../index.md) — health checks
- [Escalation](../../troubleshooting/escalation/index.md) — opening upgrade-related cases
