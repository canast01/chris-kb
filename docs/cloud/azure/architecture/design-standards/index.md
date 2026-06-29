---
tags:
  - architecture
  - azure
---
# Azure Architecture — Design Standards

```bash
# Verify tag compliance
az policy state list --resource-group <rg> \
    --filter "policyDefinitionId eq '/providers/Microsoft.Authorization/policyDefinitions/<required-tags-id>'" \
    --query "[?complianceState=='NonCompliant']"
```


```text title="Expected output"
[
  {
    "resourceId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
    "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/1e30a7b5-1f4a-4c8d-9e2f-3a4b5c6d7e8f",
    "policyDefinitionReferenceId": "requireTagsPolicy",
    "complianceState": "NonCompliant",
    "lastComplianceStateChangeAt": "2024-01-15T09:23:45Z",
    "firstEvaluationDate": "2024-01-10T08:00:00Z"
  },
  {
    "resourceId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstg2024",
    "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/1e30a7b5-1f4a-4c8d-9e2f-3a4b5c6d7e8f",
    "policyDefinitionReferenceId": "requireTagsPolicy",
    "complianceState": "NonCompliant",
    "lastComplianceStateChangeAt": "2024-01-14T14:12:30Z",
    "firstEvaluationDate": "2024-01-10T08:00:00Z"
  }
]
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --resource-group/-g`** — Provide the resource group name using `-g <rg-name>` or `--resource-group <rg-name>`.
    **`ERROR: Invalid filter expression. Invalid property name 'policyDefinitionId'.`** — Use the correct property name `policyDefinitionReferenceId` instead of `policyDefinitionId` in the filter expression.
    **`ERROR: No registered resource provider found for location 'eastus'.`** — Ensure the subscription is active and the resource group exists by running `az group show -n <rg>`.
```bash
# Add delete lock to production resource group
az lock create --name "prod-rg-lock" --resource-group <rg> --lock-type CanNotDelete

# List locks
az lock list --resource-group <rg>
```

```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg-001/providers/Microsoft.Authorization/locks/prod-rg-lock",
  "level": "ResourceGroup",
  "name": "prod-rg-lock",
  "notes": null,
  "owners": [],
  "resourceGroup": "prod-rg-001",
  "type": "Microsoft.Authorization/locks"
}
[
  {
    "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg-001/providers/Microsoft.Authorization/locks/prod-rg-lock",
    "level": "ResourceGroup",
    "name": "prod-rg-lock",
    "notes": null,
    "owners": [],
    "resourceGroup": "prod-rg-001",
    "type": "Microsoft.Authorization/locks"
  }
]
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name is correct and exists in your subscription with `az group list`.
    **`AuthorizationFailed`** — Ensure your Azure account has `Microsoft.Authorization/locks/write` permissions on the resource group.
![Azure Architecture — Design Standards — Diagram](../../../../assets/cloud-azure-architecture-design-standards-diagram.svg)

---

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## See also

- [Azure — Deploy](../../deploy/)
