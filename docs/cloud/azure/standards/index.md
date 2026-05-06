# Azure Standards

Resource naming follows the pattern `env-region-service-suffix` in lowercase with hyphens (e.g., `prod-euw-vm-appserver-01`), using Azure abbreviations for resource types as documented in the Cloud Adoption Framework. All resources must carry four mandatory tags — Environment, Owner, CostCentre, and Application — enforced through Azure Policy deny assignments at the Management Group level. Production resource groups have Delete locks applied to prevent accidental removal, and all NSG rules must include a description field documenting the business justification.

| Standard | Requirement |
|---|---|
| Naming | `env-region-service-suffix`, lowercase, hyphens, CAF abbreviations |
| Tagging | Environment, Owner, CostCentre, Application on all resources |
| Azure Policy | Deny: missing tags, public IP on VMs, non-approved regions, unencrypted disks |
| Resource locks | CanNotDelete lock on all production resource groups |
| NSG rules | Description field mandatory; allow rules reviewed quarterly |
| Managed disks | Minimum Premium SSD for production; ephemeral OS disk where supported |
