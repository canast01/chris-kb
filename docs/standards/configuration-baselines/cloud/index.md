# Cloud Configuration Baseline

## Azure Policy Required Settings

All subscriptions in the landing zone management group inherit a baseline policy set. The following policies are enforced (effect: `Deny` or `Audit` as noted).

| Policy | Effect | Notes |
|---|---|---|
| Require tag: `env` | Deny | Blocks resource creation without tag |
| Require tag: `owner` | Deny | Must be a valid email |
| Require tag: `cost-centre` | Deny | Must match finance code format |
| Allowed locations | Deny | East US 2, West Europe, UK South only |
| Allowed VM SKUs | Audit | Non-standard SKUs flagged for review |
| Require secure transfer on storage | Deny | TLS only; HTTP rejected |
| Require HTTPS on App Service | Deny | — |
| Allowed resource types | Audit | Unapproved types trigger alert to platform team |
| Enforce Azure Monitor Agent | AuditIfNotExists | Non-compliant resources flagged within 24 hours |
| No public IPs without approval tag | Deny | Tag `public-ip-approved: true` required |

Policy compliance is reviewed weekly. Subscriptions with a compliance score below 90% are escalated to the workload team.

## NSG Baseline Rules

Every NSG must include the following baseline rules. These are deployed by the Terraform `nsg_baseline` module and must not be removed.

**Inbound deny-all rule (lowest priority):**
```
Priority: 4096  Action: Deny  Source: *  Destination: *  Protocol: *
```

**Required inbound allow rules (applied to management subnets):**

- Allow HTTPS (443) from `10.10.0.0/16` (corporate network)
- Allow SSH (22) or RDP (3389) from the Bastion subnet only (`10.10.8.0/27`)
- Allow ICMP from corporate network for monitoring

**Required outbound rules:**

- Allow DNS (UDP 53) to internal resolvers (`10.10.0.10`, `10.10.0.11`)
- Allow NTP (UDP 123) to internal NTP servers
- Deny outbound internet by default; exceptions require explicit approval and a named allow rule

## Diagnostic Settings and Log Routing

Every Azure resource must send platform logs and metrics to the central Log Analytics workspace. Diagnostic settings are deployed by the `diag_baseline` Terraform module.

Required log categories by resource type:

| Resource Type | Log Categories | Metrics |
|---|---|---|
| Virtual Machine | Boot diagnostics, Guest OS (via AMA) | CPU, disk, network |
| Storage Account | StorageRead, StorageWrite, StorageDelete | Transactions, capacity |
| Key Vault | AuditEvent | — |
| NSG | NetworkSecurityGroupEvent, NetworkSecurityGroupRuleCounter | — |
| Load Balancer | LoadBalancerAlertEvent | Health probe status |
| SQL Database | SQLSecurityAuditEvents, Errors | DTU, connections |

Log Analytics workspace retention: 90 days (hot). Archive tier: 1 year.

## RBAC Minimum Standards

Role assignments follow least-privilege. The built-in `Contributor` role must not be assigned to users at subscription scope; use `Reader` and narrow custom roles instead.

Approved role assignments at subscription scope:

- Platform team SPN: `Contributor` (for automation only)
- Break-glass account: `Owner` (two accounts per subscription, Entra PIM)
- Operations team: `Reader` plus resource-specific roles via PIM

All role assignments must have:
- Justification in the assignment description
- Expiry set for JIT assignments (maximum 8-hour activation via PIM)
- No wildcard service principals

Review all role assignments quarterly. Remove any assignment that cannot be attributed to a current use case.

## Tagging Enforcement and RBAC Audit Commands

```bash
# List non-compliant resources (missing mandatory tags)
az policy state list \
  --resource-group rg-prod-eus2-app01 \
  --filter "complianceState eq 'NonCompliant'" \
  --query "[].{resource:resourceId, policy:policyDefinitionName}" -o table

# List all role assignments in a subscription
az role assignment list --subscription <sub-id> \
  --include-inherited --output table

# Check diagnostic settings on a VM
az monitor diagnostic-settings list \
  --resource /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm>
```
