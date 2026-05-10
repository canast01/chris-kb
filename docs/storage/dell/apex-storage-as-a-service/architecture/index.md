# APEX Storage as a Service — Overview

> Part of the [APEX Storage as a Service](../../) reference.

---

Dell APEX Storage as a Service (STaaS) is a consumption-based storage model where Dell provisions, owns, and manages the physical infrastructure on-premises at the customer site. Capacity is metered monthly based on committed and burst usage, billed through the APEX Console. The underlying platforms are PowerStore, PowerScale, or PowerFlex, managed by Dell — the customer interacts primarily with the APEX Console or REST API for visibility, capacity requests, and billing reporting.

## Use Cases

| Use Case |
|---|
| Organisations that want on-premises storage economics without capital expenditure or operational management overhead |
| Environments requiring predictable $/TiB subscription pricing with burst capacity headroom |
| Multi-platform environments (block, file, object) under a single consumption agreement |
| IT teams that want to outsource hardware lifecycle management (firmware, hardware replace, capacity adds) to Dell |
| Capacity planning scenarios where future growth is uncertain and over-provisioning risk needs to be avoided |

## Best Practices

| Recommendation | Detail |
|---|---|
| Keep Secure Connect Gateway appliances highly available | deploy two SCG appliances for redundancy; loss of SCG connectivity causes telemetry gaps and may trigger alerts |
| Monitor committed vs. consumed capacity monthly | request tier increases at least 30 days before hitting the committed threshold to avoid burst pricing |
| Use the APEX REST API to build automated capacity reports | feed into internal capacity planning tools |
| Review APEX Console alerts daily | infrastructure issues are Dell's responsibility to remediate but you need to confirm SLA compliance |
| Document subscription details in a runbook | subscription ID, contract end date, committed tier, and burst thresholds for on-call staff |

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
