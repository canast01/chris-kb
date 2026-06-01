# Cost Allocation Tags


<div class="kb-summary">
Tags are the primary mechanism for attributing Azure costs to teams, projects, environments, and cost centres.
</div>
```text
┌────────────────────────────────────────── Cloud Azure Cost ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Azure: Cloud Azure Cost platform                               │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                        Management: Cloud Azure Cost management console                        │   │
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
│    Physical: Cloud Azure Cost infrastructure · management network · monitoring                        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Cost platform overview and core concepts                          │
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


## Enforcement with Policy

Use Azure Policy to enforce tag presence and valid values. The built-in `Require a tag on resources` and `Require a tag and its value on resources` policies cover most cases.

```bash
# Assign built-in "Require a tag on resources" policy at subscription scope
az policy assignment create \
  --name "require-cost-centre-tag" \
  --policy "871b6d14-10aa-478d-b590-94f262ecfa99" \
  --scope "/subscriptions/<subscription-id>" \
  --params '{"tagName": {"value": "cost-centre"}}'

# List all policy assignments on a subscription
az policy assignment list \
  --scope "/subscriptions/<subscription-id>" \
  --output table

# Check compliance state for the assignment
az policy state list \
  --policy-assignment "require-cost-centre-tag" \
  --query "[?complianceState=='NonCompliant'].{Resource:resourceId}" \
  --output table
```

### Policy Effect Options for Tag Enforcement

| Effect | Behaviour |
|---|---|
| `Audit` | Logs non-compliant resources; does not block creation |
| `Deny` | Blocks resource creation/update if tag is missing |
| `Modify` | Automatically adds or updates the tag at creation time |

Start with `Audit` to baseline compliance, then switch to `Deny` or `Modify` after a remediation sprint.

## Cost Allocation Rules

In Microsoft Cost Management, cost allocation rules let you redistribute shared costs (e.g., a shared networking subscription) to other subscriptions or resource groups based on tag-defined proportions.

```bash
# Cost allocation rules are managed via the Cost Management REST API or portal.
# Use the CLI to verify tag coverage before configuring allocation:

# Count resources per team tag value
az resource list \
  --query "sort_by([].{Team:tags.team, Name:name}, &Team)" \
  --output table
```

## Tag Inheritance

Tags do not automatically inherit from resource group to child resources. Use the `Inherit a tag from the resource group` built-in policy to propagate resource group tags.

```bash
# Assign tag inheritance policy for 'environment' tag
az policy assignment create \
  --name "inherit-environment-tag" \
  --policy "96670d01-0a4d-4649-9c89-2d3abc0a5025" \
  --scope "/subscriptions/<subscription-id>" \
  --params '{"tagName": {"value": "environment"}}'
```

## Reporting on Tag Coverage

```bash
# Export all resources with their tags to JSON for audit
az resource list \
  --query "[].{Name:name, RG:resourceGroup, Tags:tags}" \
  --output json > resource-tags-$(date +%Y%m%d).json

# Resources with no tags at all
az resource list \
  --query "[?tags == null || tags == {}].{Name:name, RG:resourceGroup, Type:type}" \
  --output table
```
