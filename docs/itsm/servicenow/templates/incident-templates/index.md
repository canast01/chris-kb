---
tags:
  - servicenow
description: "Incident record templates for common failure types — P1 outage, service degradation, security incident, and infrastructure failure templates."
---
# ServiceNow — Incident Templates

<div class="kb-summary">
Incident record templates for common failure types — P1 outage, service degradation, security incident, and infrastructure failure templates.

*Applies to: ServiceNow*
</div>

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
