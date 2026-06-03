```bash
# Verify tag compliance
az policy state list --resource-group <rg> \
    --filter "policyDefinitionId eq '/providers/Microsoft.Authorization/policyDefinitions/<required-tags-id>'" \
    --query "[?complianceState=='NonCompliant']"
```

```text
┌──────────────────────────────── Azure Architecture — Design Standards ────────────────────────────────┐
│                                                                                                       │
│  Naming, tagging, region, and landing zone standards for consistent Azure governance.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Naming Conventions              │  │              Tagging Standards              │   │
│   │     Format: {type}-{app}-{env}-{region}      │  │          env: prod/dev/staging/test         │   │
│   │     Max length: varies by resource type      │  │          owner: team or individual          │   │
│   │       Lowercase alphanumeric + hyphens       │  │          cost-center: finance code          │   │
│   │         Storage: no hyphens in names         │  │         project: workload identifier        │   │
│   │      Global unique: storage + ACR names      │  │       Inherit from RG: tag auto-apply       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Landing zones provide pre-configured subscription patterns enforcing design standards.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Region & Availability             │  │             Landing Zone Design             │   │
│   │       Primary + secondary region pair        │  │         Platform subscriptions: mgmt        │   │
│   │     Paired regions: Azure-defined pairs      │  │     Application landing zones: workload     │   │
│   │         AZs: 3 per supported region          │  │          Connectivity sub: hub VNet         │   │
│   │     Availability Set: update + fault dom     │  │          Identity sub: Entra + DCs          │   │
│   │      SLA: varies per service + zone use      │  │         Policy: enforce at MG level         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure physical regions · Availability Zone data centres · Region-pair replication links              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Landing zone    = Pre-configured subscription with policies, networking, and RBAC baseline           │
│  CAF             = Cloud Adoption Framework; Microsoft guidance for Azure governance                  │
│  Region pair     = Two Azure regions paired for sequential updates and data residency                 │
│  Availability Zone= Physically separate DC within a region; 99.99% SLA when used                      │
│  Update domain   = Availability Set grouping protecting VMs from simultaneous updates                 │
│  Fault domain    = Availability Set grouping on separate hardware/power/network racks                 │
│  Hub VNet        = Central network for shared services: firewall, DNS, VPN gateway                    │
│  Spoke VNet      = Workload VNet peered to hub; isolated per application or team                      │
│  MG policy scope = Policies assigned at MG apply to all child subscriptions and RGs                   │
│  Tag inheritance = Configuring RG tag inheritance propagates tags to child resources                  │
│  Global unique   = Some Azure resource names (storage, ACR) must be globally unique                   │
│  Platform sub    = Dedicated subscriptions for management, connectivity, and identity                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Add delete lock to production resource group
az lock create --name "prod-rg-lock" --resource-group <rg> --lock-type CanNotDelete

# List locks
az lock list --resource-group <rg>
```
```text
Management Group: Corp
├── Platform
│   ├── sub-connectivity-prod       # Hub networking, ExpressRoute, DNS
│   ├── sub-identity-prod           # Domain controllers, ADCS
│   └── sub-management-prod         # Log Analytics, Backup, Automation
├── Landing Zones
│   ├── sub-app01-prod
│   ├── sub-app01-dev
│   ├── sub-app02-prod
│   └── sub-app02-dev
└── Sandbox
    └── sub-sandbox
```
