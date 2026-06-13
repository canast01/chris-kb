---
tags:
  - operations
  - pure
---
# FlashBlade — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering Purity Version Matrix, Upgrade Paths, Refresh Planning, EOL Tracking.

*Applies to: FlashBlade Purity//FB 4.x*
</div>

```text
Purity//FB Non-Disruptive Upgrade (NDU)
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  1. Review release notes + Pure1 upgrade planning    │
  │     tool — verify version compatibility              │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                             ▼
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  2. Pre-check: purefb upgrade check                  │
  │     (alerts, blade health, replication lag)          │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                             ▼
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  3. Stage + execute upgrade                          │
  │     Blades upgrade one at a time — I/O continues    │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                             ▼
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  4. Validate: purefb array list                      │
  │     All blades on new version, no alerts             │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [FlashBlade Operations](index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Purity Version Matrix

| Version | Release Date | End of Support | Notes |
|---|---|---|---|
| Purity//FB 4.4.x | Q4 2024 | Q4 2027 (est.) | Current major; ActiveCluster for file systems GA, pNFS enhancements |
| Purity//FB 4.3.x | Q2 2024 | Q2 2027 (est.) | S3 lifecycle policies, object lock (WORM) support |
| Purity//FB 4.2.x | Q4 2023 | Q4 2026 (est.) | SMB multichannel, NFS v4.1 pNFS generally available |
| Purity//FB 4.1.x | Q2 2023 | Q2 2026 (est.) | Approaching end of active support — plan upgrade |
| Purity//FB 4.0.x | Q4 2022 | Q4 2025 (est.) | End of support approaching — upgrade required |
| Purity//FB 3.3.x | Q2 2022 | Reached EOS | No longer supported — upgrade required |
| Purity//FB 3.2.x and earlier | Various | Reached EOS | No longer supported — upgrade required |

> Verify current EOS dates at [Pure Support Portal](https://support.purestorage.com). Pure updates EOS dates per release cycle.

## Upgrade Paths

Pure Storage applies an **N-2 support policy** for Purity//FB: only the two most recent minor release trains receive full support including bug fixes and security patches.

**Supported upgrade sequences:**

- Patch-level upgrades within the same minor train are always supported (e.g., 4.2.0 → 4.2.5)
- Cross-minor upgrades are supported within the N-2 window (e.g., 4.1.x → 4.3.x)
- Upgrading from Purity//FB 3.x to 4.x may require an intermediate upgrade step — verify in Pure1 upgrade planning tool before proceeding
- Never skip more than two minor versions without confirming the upgrade path with Pure Support

**Pre-upgrade steps:**

```bash
# Confirm current version
purefb array list

# Check all blades are healthy before upgrading
purefb blade list

# Check no hardware alerts are open
purefb alert list

# Verify all filesystem replica links are healthy (if ActiveDR is configured)
purefb replication list
```

**Upgrade execution:**

- FlashBlade upgrades are non-disruptive; Purity//FB performs a rolling blade upgrade
- NFS, SMB, and S3 clients may experience brief session reconnects as individual blades restart
- Download the upgrade image from Pure Support portal and stage via the GUI or CLI
- Execute the upgrade during a maintenance window; monitor progress in the GUI or Pure1

## Refresh Planning

| Trigger | Action | Lead Time |
|---|---|---|
| Blade model approaching hardware EOL | Contact Pure account team to evaluate chassis refresh or Evergreen blade swap | 6–12 months |
| Chassis approaching physical capacity limit (max blades installed) | Plan additional chassis deployment | 3–6 months (procurement) |
| Capacity headroom below 20% | Procure additional blades or expand existing chassis | 4–8 weeks (blade delivery) |
| Purity//FB version approaching N-2 boundary | Plan and execute Purity upgrade | Schedule within 90 days |
| Protocol requirement not met by current Purity version | Upgrade Purity to enable required feature (e.g., pNFS, SMB 3.0) | Plan upgrade in next maintenance cycle |

**Blade addition (non-disruptive scale-out):**

1. Insert new blades into available chassis slots
2. Run `purefb blade add` to integrate the new blade into the cluster
3. Purity//FB automatically rebalances data across all blades — no client interruption
4. Monitor rebalance progress in Pure1 or via `purefb blade list`

## EOL Tracking

| Version | Status | Recommended Action |
|---|---|---|
| Purity//FB 4.0.x | Approaching EOS | Upgrade to 4.2.x or 4.3.x within 90 days |
| Purity//FB 3.3.x | End of Support | Upgrade immediately |
| Purity//FB 3.2.x and earlier | End of Support | Upgrade immediately — contact Pure Support for upgrade path |
| FlashBlade //S original hardware | Check with Pure account team | Some early chassis generations have hardware EOL dates approaching — verify with Pure |

Maintain a quarterly review cadence against Pure's published hardware and software EOL list. Subscribe to Pure Support notifications for your array's Purity//FB version.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
