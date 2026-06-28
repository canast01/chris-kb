---
tags:
  - architecture
  - azure
---
# Azure Architecture — Design Standards
![Azure Architecture — Design Standards](../../../../assets/cloud-azure-architecture-design-standards-index.svg)


```bash
# Verify tag compliance
az policy state list --resource-group <rg> \
    --filter "policyDefinitionId eq '/providers/Microsoft.Authorization/policyDefinitions/<required-tags-id>'" \
    --query "[?complianceState=='NonCompliant']"
```

```bash
# Add delete lock to production resource group
az lock create --name "prod-rg-lock" --resource-group <rg> --lock-type CanNotDelete

# List locks
az lock list --resource-group <rg>
```
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
