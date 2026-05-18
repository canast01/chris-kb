# Azure — Operations

```
┌─────────────────────────────────────────────────────────────────┐
│                     Azure Operations Overview                    │
└───────────────┬─────────────────────────────────────────────────┘
                │
    ┌───────────┴───────────┐
    ▼                       ▼
┌───────────────┐   ┌───────────────────────────────────────────┐
│  Health Layer │   │              Operational Layer              │
│               │   │                                             │
│ Service Health│   │  ┌──────────────┐  ┌──────────────────┐     │
│ Resource Health│  │  │  Backup Jobs │  │  Azure Update Mgr│     │
│ Monitor Alerts│   │  │  (RSV Vault) │  │  (VM Patching)   │     │
└───────┬───────┘   │  └──────────────┘  └──────────────────┘  │
        │           │  ┌──────────────┐  ┌──────────────────┐  │
        ▼           │  │  Azure CLI   │  │  Scripts / Auto  │  │
┌───────────────┐   │  │  (az vm, az  │  │  (Runbooks, PS)  │  │
│  Action Group │   │  │   monitor)   │  │                  │     │
│  → email/ITSM │   │  └──────────────┘  └──────────────────┘     │
└───────────────┘   └───────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Azure CLI commands, syntax, and quick reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Service health, VM status, load balancer health, and monitor alert review.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Day-to-day operational tasks across compute, storage, and networking.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>VM image management, patching via Azure Update Manager, and service upgrades.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Azure Backup jobs, restore procedures, and Recovery Services vault management.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and reusable Azure CLI code.</span>
</a>

</div>

> Part of the [Azure](../) reference.

---
## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Check Azure Service Health for active events in your subscription |  |  |
| [ ] Review VM power states | `az vm list --show-details --query '[*].[name,powerState]' -o table` |  |
| [ ] Check Azure Monitor activity log alerts | `az monitor activity-log alert list -o table` |  |
| [ ] Review failed backup jobs | `az backup job list --vault-name $VAULT -g $RG --query '[?properties.status==\` |  |
| [ ] Review Azure Advisor for new high-severity recommendations |  |  |
| [ ] Check Key Vault certificate expiry |  | flag any certificates expiring within 30 days |
| [ ] Review Cost Management for anomalies vs. the prior week |  |  |
| [ ] Check Entra ID sign-in logs for failed or suspicious authenticatio |  |  |

## Health Check

- [ ] Confirm Azure CLI is authenticated and targeting the correct subscription
- [ ] Verify all VMs are in `running` power state
- [ ] Confirm load balancers are healthy with no backend pool degradation
- [ ] Check Azure Monitor activity log for error-level events in the last 24 hours
- [ ] Verify all backup jobs completed successfully in the last 24 hours
- [ ] Confirm Key Vault is accessible and no certificates are expiring within 14 days
- [ ] Check NSG flow logs for unexpected denied traffic patterns
- [ ] Verify Entra ID service principal credentials are not expired

```bash
# List VMs with power state
az vm list --show-details \
  --query '[*].[name,resourceGroup,powerState,provisioningState]' \
  -o table

# Load balancer status
az network lb show \
  --name <lb-name> \
  --resource-group <rg> \
  --query '{name:name,provisioningState:provisioningState}' \
  -o table

# Activity log — last 50 events
az monitor activity-log list --max-events 50 \
  --query '[*].[eventTimestamp,level,operationName.localizedValue,status.localizedValue]' \
  -o table

# Failed backup jobs
az backup job list \
  --vault-name $VAULT \
  -g $RG \
  --query '[?properties.status==`Failed`].[properties.jobType,properties.startTime,properties.errorDetails]' \
  -o table
```

## Change Readiness

- [ ] VM snapshot or Recovery Services vault backup verified before change
- [ ] NSG rule changes peer-reviewed and scoped to minimum required access
- [ ] Azure Policy compliance checked — no new non-compliant resources introduced
- [ ] Resource locks reviewed; delete locks removed only if required and re-applied after
- [ ] Rollback plan documented with restore procedure
- [ ] Azure Maintenance Notifications reviewed for conflicting platform maintenance
- [ ] Stakeholders notified of change window

| Item | Status | Notes |
|---|---|---|
| Pre-change backup/snapshot | | Vault name and job ID |
| NSG peer review | | PR or ticket reference |
| Policy compliance check | | Compliant / Non-compliant count |
| Resource lock status | | Locks in place post-change |
| Rollback plan | | Link to runbook |

## Incident Triage

- [ ] Check Azure Service Health for active outages in the affected region or service
- [ ] Review Azure Monitor alerts to identify the affected resource and metric
- [ ] Check resource-specific diagnostics (VM boot diagnostics, NSG flow logs, App Gateway logs)
- [ ] Review Activity Log for changes in the 2 hours before the incident
- [ ] Verify NSG rules and UDR routes have not changed unexpectedly
- [ ] Check load balancer backend pool health and probe status
- [ ] Engage Microsoft Support if the issue is platform-side

| Question | Answer |
|---|---|
| Is this an Azure platform outage? | Check status.azure.com |
| Which resource is affected? | VM / Storage / Network / Other |
| When did the issue start? | Activity Log timestamp |
| What changed recently? | Activity Log last 2 hours |
| Is a rollback possible? | Yes / No — backup available? |

## Maintenance Window

1. Review Azure Maintenance Notifications for any planned platform maintenance that overlaps.
2. Verify VM availability sets or zones are configured to limit blast radius.
3. Confirm Recovery Services vault backup is current before starting.
4. For VMs: deallocate if required, perform maintenance, start and confirm running state.
5. For networking changes: validate NSG rules in staging before applying to production.
6. If Azure Site Recovery (ASR) is configured, validate replication health after the change.
7. Confirm Azure Monitor alerts return to resolved state.
8. Close the maintenance window and notify stakeholders.

## Post-Change Validation

- [ ] All Azure Monitor alerts are resolved
- [ ] All VMs are in `running` power state
- [ ] Load balancer backend pools show all instances healthy
- [ ] Application smoke test passes (login, key transaction, API call)
- [ ] Activity Log shows only expected operations from the maintenance window
- [ ] No new Azure Service Health events opened for affected services
- [ ] Cost Management shows no unexpected charge spikes from the change
- [ ] Key Vault access and certificate validity confirmed
