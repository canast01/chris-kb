# FOD — Standards

> Part of the [Flex on Demand](../../) reference.

---

## Upgrade Notes

| Step | Action |
|---|---|
| 1 | FOD billing is unaffected by firmware upgrades, but confirm CloudIQ telemetry resumes promptly after any maintenance that takes the array offline |
| 2 | After adding physical burst capacity under a FOD agreement, confirm CloudIQ reflects the new total installed capacity |
| 3 | If the array is migrated or replaced, work with Dell to transfer the FOD contract to the new system SID |

## Design Standards

- Monitor CloudIQ capacity trends weekly so burst events are visible before the end-of-month bill
- Deploy two SCG appliances for redundancy — a single SCG failure silently causes telemetry gaps that complicate billing disputes
- Automate monthly usage extraction via CloudIQ API and feed into a finance reporting system
- Set the committed baseline conservatively at contract start; adjust upward at renewal
- Review monthly metered usage report from CloudIQ or APEX Console and compare to contracted baseline
