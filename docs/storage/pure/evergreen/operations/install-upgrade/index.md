# Evergreen — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering Evergreen Program Tiers, Software Upgrade (Purity), Drive Replacement, Controller Refresh (Evergreen//Forever), Lifecycle Timeline and 1 more sections.
</div>

```text
Evergreen Upgrade Types
  ┌────────────────────────────────────────────────────────┐
  │  Purity NDU Software Upgrade                           │
  │  Customer-initiated, fully non-disruptive              │
  │  purearray upgrade --check → --stage → --exec         │
  └────────────────────────────────────────────────────────┘
  ┌────────────────────────────────────────────────────────┐
  │  Ever Modern Controller Refresh (~3 yr cycle)          │
  │  Pure-executed, non-disruptive                         │
  │  Scheduled with Pure account team (90+ day lead time)  │
  └────────────────────────────────────────────────────────┘
  ┌────────────────────────────────────────────────────────┐
  │  Capacity Expansion                                    │
  │  Add NVMe shelf or True Forward amendment              │
  │  Pure installs new shelf (hot-add, non-disruptive)     │
  └────────────────────────────────────────────────────────┘
```

> Part of the [Evergreen Operations](../index.md) reference.

---

## Evergreen Program Tiers

| Program | Model | Refresh Included |
|---|---|---|
| Evergreen//Forever | Customer-owned (CapEx) | Controller upgrades; drives purchased |
| Evergreen//Flex | Subscription lease | Hardware within subscription term |
| Evergreen//One | STaaS (Pure-owned) | All hardware; Pure manages lifecycle |

## Software Upgrade (Purity)

Purity (FlashArray OS) upgrades are non-disruptive and performed by Pure Storage:

1. Pure Storage schedules upgrade with advance notice
2. Customer confirms maintenance window
3. Pure upgrades both controllers sequentially — no I/O interruption
4. Purity version is validated post-upgrade

```bash
# Verify current Purity version
purecli array list | grep -i version
# or in GUI: System → Software
```

## Drive Replacement

Drives are monitored by Pure1 and replaced proactively before failure:

- Pure Storage ships replacement drive
- Pure engineer (or guided remote process) swaps drive
- Parity rebuild begins automatically
- No host impact during rebuild

```bash
# Check drive health
purecli drive list
purecli drive list --filter "status!=healthy"
```

## Controller Refresh (Evergreen//Forever)

Under Evergreen//Forever, controllers are refreshed when new generations are available:
- Customer purchases new controller shelf
- Pure performs non-disruptive controller swap
- Data remains in place (no migration required)

### How Controller Upgrades Work

1. Pure Storage proactively schedules controller upgrades based on technology lifecycle
2. Customer receives advance notice (typically 90+ days)
3. The upgrade is performed non-disruptively by Pure Storage engineers
4. Active I/O continues during the upgrade — hosts see no interruption

### Customer Pre-Upgrade Responsibilities

- Confirm maintenance window with the Pure Storage team
- Verify all hosts are healthy and paths are redundant
- Ensure no in-progress background tasks (e.g., parity rebuilds) would extend the window

```bash
# Check array health before upgrade
purecli array list
purecli drive list
purecli alert list
```

### Verifying Paths During/After Upgrade

**On the host:**

```bash
# Linux with multipath
multipath -ll

# Windows PowerShell (MPIO)
mpclaim -s -d

# VMware
esxcli storage nmp device list
```

Confirm all expected paths are active after the upgrade completes.

### Post-Upgrade Verification

```bash
purecli array list     # Confirm new controller hardware
purecli hardware list  # All components healthy
purecli alert list     # No post-upgrade alerts
```

### Common Considerations

| Item | Detail |
|---|---|
| Downtime | None — non-disruptive by design |
| Pre-requisite | Dual-path host connectivity required |
| Scheduling | Coordinated with Pure Storage |
| Data migration | None — data stays in place |
| Host action required | None (verify paths post-upgrade) |

## Lifecycle Timeline

| Activity | Trigger | Lead Time |
|---|---|---|
| Purity upgrade | Pure-scheduled or customer request | 30–90 days notice |
| Drive replacement | Proactive Pure1 alert | 5–14 days for parts |
| Controller upgrade | Generation availability | 90+ days notice |
| Platform EOL | Pure announcement | Multi-year notice |

## End-of-Life Considerations

- Purity software is supported for all active subscriptions
- Pure Storage commits to NVM and drive compatibility across generations
- Customer-owned (Evergreen//Forever) arrays receive software support for the platform lifetime
