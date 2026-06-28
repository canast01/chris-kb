---
tags:
  - azure
  - certifications
---
# Azure Practice Notes

<div class="kb-summary">
Azure Practice Notes reference covering ARM vs Bicep vs Terraform, RBAC Scope Hierarchy, Policy vs Initiative, Common Scenario Mappings, Azure AD / Entra ID Key Concepts and 1 more sections.
</div>

## ARM vs Bicep vs Terraform

| Feature | ARM Templates | Bicep | Terraform |
|---|---|---|---|
| Language | JSON | Domain-specific language (DSL) | HCL |
| Azure-native | Yes | Yes | No (provider-based) |
| Transpiles to | — | ARM JSON | — |
| Multi-cloud | No | No | Yes |
| State management | None (Azure is source of truth) | None | Terraform state file |
| Modularity | Linked templates / nested | Modules | Modules |
| IDE support | Good | Better (VS Code Bicep extension) | Good |
| Recommended for new Azure-only IaC | No | Yes | Yes (if multi-cloud needed) |

Exam gotcha: Bicep compiles to ARM; they are functionally equivalent for Azure deployments. Terraform requires a state file — ARM/Bicep do not.

## RBAC Scope Hierarchy

RBAC assignments are inherited downward:

```text
Management Group
  └── Subscription
        └── Resource Group
              └── Resource
```

| Scope Level | Example Assignment | Notes |
|---|---|---|
| Management Group | Reader across all subscriptions | Inherited by all child resources |
| Subscription | Contributor for a dev team | Inherited by all RGs and resources |
| Resource Group | Owner for an app team | Inherited by resources in the RG |
| Resource | Reader on a single storage account | Applies only to that resource |

Key exam points:
- Owner = all permissions including role assignments; Contributor = all except role assignments
- Reader can view but not modify any resource
- A role assignment at a higher scope cannot be blocked by one at a lower scope (no deny in RBAC — use Azure Policy for deny)

## Policy vs Initiative

| Feature | Azure Policy | Initiative (Policy Set) |
|---|---|---|
| Definition | Single rule defining compliance condition | Collection of policy definitions |
| Assignment | Can be assigned independently | Assigned as a group |
| Use case | Enforce one specific rule | Enforce a compliance standard (e.g., PCI DSS) |
| Effect types | Deny, Audit, AuditIfNotExists, Modify, DeployIfNotExists | Inherits effects from member policies |

Policy effects in priority order for exam: Disabled → Append → Modify → Deny → Audit

## Common Scenario Mappings

| Scenario | Answer |
|---|---|
| Prevent creation of public storage accounts organization-wide | Azure Policy (Deny effect) at Management Group |
| Allow a VM to access Key Vault without storing credentials | Managed Identity |
| Route all traffic through a central firewall | User-Defined Routes (UDR) + Azure Firewall |
| Mirror logs from multiple subscriptions to one workspace | Azure Monitor diagnostic settings → Log Analytics |
| Protect against DDoS at Layer 7 | Azure Application Gateway WAF |
| Protect against volumetric DDoS | Azure DDoS Protection Standard |

## Azure AD / Entra ID Key Concepts

- **Conditional Access**: Enforce MFA/device compliance based on user, location, app, risk signal
- **PIM (Privileged Identity Management)**: Just-in-time elevation; audit privileged role assignments
- **Azure AD B2B**: Invite external users to your tenant
- **Azure AD B2C**: Customer identity platform for app sign-in

## Study Checklist

- [ ] Draw the RBAC scope hierarchy from memory with four levels
- [ ] Explain the difference between Owner and Contributor roles
- [ ] Describe when Bicep is preferred over ARM and when Terraform is preferred
- [ ] Know Azure Policy effects in priority order
- [ ] Practice 5 Conditional Access scenario questions
- [ ] Understand Managed Identity vs Service Principal for app authentication
- [ ] Map Policy vs Initiative vs Management Group for org-wide governance questions
