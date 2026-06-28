---
tags:
  - servicenow
---
# ServiceNow — Change Management Procedures

<div class="kb-summary">
ServiceNow change request lifecycle — raising, categorising, routing for CAB approval, implementing, and closing change records.

*Applies to: ServiceNow*
</div>
![ServiceNow — Change Management Procedures](../../../../assets/itsm-servicenow-change-management-procedures-index.svg)




```d2
direction: right

hub: "ServiceNow\nOperations" {shape: hexagon}
routine_checks: "Routine Checks" {shape: rectangle}
configuration: "Configuration" {shape: rectangle}
monitoring: "Monitoring" {shape: rectangle}
maintenance: "Maintenance" {shape: rectangle}

hub -> routine_checks
hub -> configuration
hub -> monitoring
hub -> maintenance
```

## See also

- [ServiceNow — Overview](../../)
