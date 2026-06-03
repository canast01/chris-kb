# Azure Standards

<div class="kb-summary">
Azure Standards reference covering Naming Convention, Tagging Policy, Security Standards, RBAC Inheritance Model, Resource Lock Standards and 6 more sections.
</div>

## Naming Convention

Pattern: `<type>-<env>-<region>-<name>[-<seq>]` using CAF abbreviations:

| Resource | Example |
|---|---|
| Resource Group | `rg-prod-euw-network` |
| Virtual Network | `vnet-prod-euw-hub` |
| Subnet | `snet-prod-euw-app` |
| VM | `vm-prod-euw-appserver-01` |
| NSG | `nsg-prod-euw-app` |
| Key Vault | `kv-prod-euw-secrets` |
| Storage Account | `stcorpprodeuwa01` (no hyphens — SA naming is strict) |
| App Service | `app-prod-euw-apimain` |
| AKS Cluster | `aks-prod-euw-platform` |

Region abbreviations: `euw` = West Europe, `eun` = North Europe, `use` = East US.

Full CAF naming reference: [aka.ms/caf/naming](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming).

## Tagging Policy

Mandatory tags enforced via Azure Policy deny assignments at Management Group level:

| Tag Key | Example | Enforcement |
|---|---|---|
| `Environment` | `prod`, `staging`, `dev` | Required on all resources |
| `Owner` | `infra-team` | Required on all resources |
| `CostCentre` | `CC-1234` | Required on all resource groups |
| `Application` | `erp-frontend` | Required on all resources |

```bash
# Verify tag compliance
az policy state list --resource-group <rg> \
    --filter "policyDefinitionId eq '/providers/Microsoft.Authorization/policyDefinitions/<required-tags-id>'" \
    --query "[?complianceState=='NonCompliant']"
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

## Resource Lock Standards

Apply locks to prevent accidental deletion of production infrastructure:

```bash
# Add delete lock to production resource group
az lock create --name "prod-rg-lock" --resource-group <rg> --lock-type CanNotDelete

# List locks
az lock list --resource-group <rg>
```

## Approved Regions

Azure resources may only be deployed in:
- `westeurope` — primary
- `northeurope` — secondary / DR

Enforced via Azure Policy: `Allowed locations` assignment at root Management Group.

---


## Resource Naming Conventions

All cloud resources must follow a consistent naming pattern to enable filtering, cost attribution, and automation. Names are lowercase, hyphen-delimited, and include environment and region codes.

| Resource Type | Pattern | Example |
|---|---|---|
| Resource Group | `rg-{env}-{region}-{name}` | `rg-prod-eus2-networking` |
| Virtual Machine | `vm-{app}-{env}-{num}` | `vm-webapi-prod-01` |
| Storage Account | `sa{env}{region}{name}` (no hyphens, max 24 chars) | `saprodeus2appdata` |
| Key Vault | `kv-{env}-{name}` | `kv-prod-secrets` |
| Virtual Network | `vnet-{env}-{region}` | `vnet-prod-eus2` |
| Subnet | `snet-{role}-{env}` | `snet-app-prod` |
| Network Security Group | `nsg-{role}-{env}` | `nsg-app-prod` |
| Load Balancer | `lb-{app}-{env}` | `lb-webapi-prod` |

Region codes: `eus2` (East US 2), `weu` (West Europe), `seau` (Southeast Asia), `uks` (UK South).

Environment codes: `prod`, `stg`, `dev`, `sbx`.

## Tagging Requirements

All resources must carry the following tags at creation. Missing tags block deployment via policy enforcement.

**Mandatory tags:**

- `env` — `prod` | `stg` | `dev` | `sbx`
- `owner` — email of the team or service owner
- `application` — application or workload name
- `cost-centre` — finance cost code (e.g. `cc-1042`)
- `created-by` — automation tool or engineer login
- `criticality` — `high` | `medium` | `low`

**Optional but recommended:**

- `support-tier` — `24x7` | `business-hours`
- `data-classification` — `public` | `internal` | `confidential`

Tags are enforced via Azure Policy `Require tag on resources`. Any resource missing mandatory tags is flagged in the compliance dashboard within 24 hours.

## Subscription Structure

Subscriptions are organised by workload and environment, not by team. Each production workload gets a dedicated subscription to enforce blast radius isolation.

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

Each landing zone subscription inherits policy from its management group. Do not place prod and non-prod workloads in the same subscription.

## Baseline Configuration Requirements

Every deployed resource must meet these baseline config checks before being marked build-complete.

**Networking:**
- All VMs deployed into a named subnet, not directly into a VNet
- No public IP unless explicitly approved; use Azure Bastion or private endpoints
- NSG attached at subnet level; NIC-level NSGs only for exceptions with justification

**Identity and Access:**
- System-assigned managed identity enabled on all VMs and function apps
- No local credentials stored; secrets go to Key Vault
- Subscription Owner role: maximum two named accounts plus one break-glass

**Diagnostics:**
- Boot diagnostics enabled on all VMs
- Diagnostic settings configured to send platform logs to central Log Analytics workspace
- Azure Monitor Agent deployed and reporting within 15 minutes of build

**Encryption:**
- OS and data disks encrypted with platform-managed keys minimum; customer-managed keys for confidential data
- Storage accounts: `Require secure transfer` enabled, TLS 1.2 minimum

## Approval and Deployment Process

All cloud builds follow a four-stage gate process before production promotion.

1. **Design review** — architecture diagram reviewed by platform team; naming and tagging confirmed
2. **Terraform plan review** — PR raised, plan output reviewed, no resource deletions without explicit sign-off
3. **Dev/staging validation** — functional tests pass, monitoring agent confirmed active
4. **Production deployment** — deployment window booked, rollback plan documented in change record

Deployments to production subscriptions require a ServiceNow change record number in the pipeline run. Pipelines reject runs without a valid change reference.
