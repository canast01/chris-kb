---
tags:
  - architecture
  - servicenow
---
# ServiceNow — Architecture

<div class="kb-summary">
ServiceNow is a multi-instance SaaS platform with fully isolated per-customer stacks. On-premises integration is handled via MID Servers — outbound-only Java agents that eliminate inbound firewall requirements.
</div>

![ServiceNow Architecture](../../../assets/servicenow-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Instance model, node topology, MID Servers, platform components, and upgrade lifecycle.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>

---

## Instance Hierarchy

| Instance | Purpose |
|---|---|
| Dev | Development and initial testing |
| Test / UAT | Validation before production promotion |
| Production | Live environment |

---

## Platform Node Topology

