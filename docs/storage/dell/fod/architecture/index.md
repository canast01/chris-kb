# FOD — Overview

> Part of the [Flex on Demand](../../) reference.

---

Dell Flex on Demand (FOD) is a consumption-based capacity model in which additional storage capacity is pre-installed in the array but metered — you pay only for what you use above the committed baseline. Usage is reported monthly via the CloudIQ telemetry pipeline, and burst consumption above the committed tier is billed at a per-TiB rate. FOD provides the cost efficiency of a cloud-like model on-premises without requiring physical capacity additions. It is available on PowerMax, PowerStore, and PowerScale platforms.

## Use Cases

| Use Case |
|---|
| Environments with variable workload patterns where paying for peak capacity all the time is wasteful |
| Dev/test environments that need burst capacity periodically but a low committed baseline |
| Businesses that want to avoid capital expenditure on storage but remain on-premises |
| Organisations running APEX Flex on Demand subscriptions as part of a broader APEX agreement |
| Situations where procurement lead times are too long to meet workload growth demands |

## How FOD Works

A base capacity is licensed outright. Burst capacity above the committed level is metered and billed monthly. FOD contracts define a **base** commitment and a **burst ceiling**. Usage between base and ceiling is billed monthly. Usage above the burst ceiling may trigger over-usage charges or require an immediate license upgrade.

Metering is based on the **maximum capacity used in any hour** during the billing month (peak-hour metering).

## Best Practices

| Recommendation | Detail |
|---|---|
| Set the committed baseline conservatively at contract start and adjust upward at renewal | it is easier to raise a baseline than recover overbilled burst charges |
| Monitor CloudIQ capacity trends weekly | burst events visible before the end-of-month bill |
| Ensure Secure Connect Gateway redundancy | a single SCG failure that causes telemetry gaps can complicate billing disputes |
| Automate monthly usage extraction via CloudIQ API | feed it into a finance reporting system to eliminate manual reconciliation |

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
