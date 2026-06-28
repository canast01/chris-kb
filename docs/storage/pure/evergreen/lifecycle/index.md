---
tags:
  - pure
---
# Pure Storage Evergreen Lifecycle


<div class="kb-summary">
Pure Storage Evergreen Lifecycle reference covering Evergreen Program Tiers, Software Upgrade (Purity), Drive Replacement, Controller Refresh (Evergreen//Forever), End-of-Life Considerations and 1 more sections.

*Applies to: Evergreen*
</div>
![Pure Storage Evergreen Lifecycle](../../../../assets/storage-pure-evergreen-lifecycle-index.svg)




![Pure Storage Evergreen Lifecycle — Diagram](../../../../assets/storage-pure-evergreen-lifecycle-diagram.svg)

The Evergreen program guarantees that Pure FlashArray and FlashBlade platforms never become obsolete — hardware and software are refreshed non-disruptively as technology evolves.

```d2
direction: right

plan: "Plan" {shape: oval}
evergreen_program_tiers: "Evergreen Program Tiers" {shape: rectangle}
software_upgrade_purity: "Software Upgrade (Purity)" {shape: rectangle}
drive_replacement: "Drive Replacement" {shape: rectangle}
controller_refresh_evergreenforever: "Controller Refresh (Evergreen//Forever)" {shape: rectangle}
endoflife_considerations: "End-of-Life Considerations" {shape: rectangle}
lifecycle_timeline: "Lifecycle Timeline" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> evergreen_program_tiers
evergreen_program_tiers -> software_upgrade_purity
software_upgrade_purity -> drive_replacement
drive_replacement -> controller_refresh_evergreenforever
controller_refresh_evergreenforever -> endoflife_considerations
endoflife_considerations -> lifecycle_timeline
lifecycle_timeline -> validate
```

## Evergreen Program Tiers

| Program | Model | Refresh Included |
|---|---|---|
| Evergreen//Forever | Customer-owned (CapEx) | Controller upgrades; drives purchased |
| Evergreen//Flex | Subscription lease | Hardware within subscription term |
| Evergreen//One | STaaS (Pure-owned) | All hardware; pure manages lifecycle |

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

See the Pure Storage Evergreen//Forever documentation for controller upgrade procedures.

## End-of-Life Considerations

- Purity software is supported for all active subscriptions
- Pure Storage commits to NVM and drive compatibility across generations
- Customer-owned (Evergreen//Forever) arrays receive software support for the platform lifetime

## Lifecycle Timeline

| Activity | Trigger | Lead Time |
|---|---|---|
| Purity upgrade | Pure-scheduled or customer request | 30–90 days notice |
| Drive replacement | Proactive Pure1 alert | 5–14 days for parts |
| Controller upgrade | Generation availability | 90+ days notice |
| Platform EOL | Pure announcement | Multi-year notice |
