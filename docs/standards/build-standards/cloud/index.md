# Cloud Build Standards

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

```
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
