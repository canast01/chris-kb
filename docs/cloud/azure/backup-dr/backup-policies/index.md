# Backup Policies


<div class="kb-summary">
Backup policies define when backups run, how many recovery points are retained, and at what tiers
</div>
```text
┌──────────────────────────────────────── Cloud Azure Backup Dr ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Azure: Cloud Azure Backup Dr platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: Cloud Azure Backup Dr management console                     │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Backup Dr infrastructure · management network · monitoring                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Backup Dr platform overview and core concepts                     │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Creating a VM Backup Policy

Policies are defined in JSON. Below is a minimal daily VM backup policy template.

```json
{
  "eTag": null,
  "location": "eastus",
  "properties": {
    "backupManagementType": "AzureIaasVM",
    "instantRpRetentionRangeInDays": 2,
    "schedulePolicy": {
      "schedulePolicyType": "SimpleSchedulePolicy",
      "scheduleRunFrequency": "Daily",
      "scheduleRunTimes": ["2026-01-01T02:00:00Z"]
    },
    "retentionPolicy": {
      "retentionPolicyType": "LongTermRetentionPolicy",
      "dailySchedule": {
        "retentionTimes": ["2026-01-01T02:00:00Z"],
        "retentionDuration": {"count": 30, "durationType": "Days"}
      },
      "weeklySchedule": {
        "daysOfTheWeek": ["Sunday"],
        "retentionTimes": ["2026-01-01T02:00:00Z"],
        "retentionDuration": {"count": 12, "durationType": "Weeks"}
      },
      "monthlySchedule": {
        "retentionScheduleFormatType": "Weekly",
        "retentionScheduleWeekly": [{"daysOfTheWeek": ["Sunday"], "weeksOfTheMonth": ["First"]}],
        "retentionTimes": ["2026-01-01T02:00:00Z"],
        "retentionDuration": {"count": 12, "durationType": "Months"}
      }
    },
    "timeZone": "UTC"
  }
}
```

```bash
# Create the policy from the JSON file
az backup policy create \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <policy-name> \
  --policy @vm-backup-policy.json \
  --backup-management-type AzureIaasVM
```

---

## Retention Rules Reference

| Tier | Minimum | Maximum | Notes |
|---|---|---|---|
| Snapshot (instant restore) | 1 day | 5 days | Stored in the resource group |
| Daily vault | 7 days | 9999 days | Stored in the Recovery Services Vault |
| Weekly vault | 1 week | 5163 weeks | Each Sunday (or chosen day) |
| Monthly vault | 1 month | 1188 months | First/last week of month |
| Yearly vault | 1 year | 99 years | Specified month and week |

---

## Modifying an Existing Policy

```bash
# Export the current policy to a file for editing
az backup policy show \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <policy-name> > current-policy.json

# Apply the modified policy (overwrites existing)
az backup policy set \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <policy-name> \
  --policy @current-policy.json
```

---

## Assigning a Policy to Protected Items

```bash
# Change the policy for an already-protected VM
az backup item set-policy \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --container-name <container-name> \
  --name <vm-name> \
  --backup-management-type AzureIaasVM \
  --workload-type VM \
  --policy-name <new-policy-name>

# List items using a specific policy
az backup item list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --query "[?properties.policyId contains '<policy-name>'].{Name:name, State:properties.protectionState}" \
  --output table
```

---

## Deleting a Policy

```bash
# Delete a policy (only if no items are assigned to it)
az backup policy delete \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <policy-name>
```
