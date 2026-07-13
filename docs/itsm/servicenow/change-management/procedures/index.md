---
tags:
  - servicenow
description: "ServiceNow change request lifecycle — raising, categorising, routing for CAB approval, implementing, and closing change records."
---
# ServiceNow — Change Management Procedures

<div class="kb-summary">
ServiceNow change request lifecycle — raising, categorising, routing for CAB approval, implementing, and closing change records.

*Applies to: ServiceNow*
</div>

```d2
direction: right

routine_checks: "Routine Checks" {shape: rectangle}
configuration: "Configuration" {shape: rectangle}
monitoring: "Monitoring" {shape: rectangle}
maintenance: "Maintenance" {shape: rectangle}

routine_checks -> configuration
configuration -> monitoring
monitoring -> maintenance
```

## See also

- [ServiceNow — Overview](../../)
