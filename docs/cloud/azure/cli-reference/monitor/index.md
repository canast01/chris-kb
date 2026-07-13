---
tags:
  - azure
description: "Azure Monitor CLI: az monitor metrics list, az monitor alert create, az monitor log-analytics query, az monitor diagnostic-settings create, and workspace..."
---
# Monitor & Alerts

<div class="kb-summary">
Azure Monitor CLI: `az monitor metrics list`, `az monitor alert create`, `az monitor log-analytics query`, `az monitor diagnostic-settings create`, and workspace management.

*Applies to: Azure*
</div>

> Part of the Azure CLI Reference.

---

```bash
# Activity log
az monitor activity-log list --max-events 50
az monitor activity-log list --resource-group <rg> --offset 24h

# Metrics
az monitor metrics list --resource <resource_id> --metric "Percentage CPU"
az monitor metrics list-definitions --resource <resource_id>

# Alerts
az monitor alert list --resource-group <rg>
az monitor action-group list

# Diagnostic settings
az monitor diagnostic-settings list --resource <resource_id>
az monitor diagnostic-settings create --name <name> --resource <resource_id> \
  --workspace <workspace_id> --metrics '[{"category":"AllMetrics","enabled":true}]'
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [Azure CLI Reference](../index.md)
- [Azure Operations](../../operations/index.md)
- [Azure Monitoring](../../monitoring/index.md)
