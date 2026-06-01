# Azure — Groups


<div class="kb-summary">
Entra ID (Azure AD) groups are the primary mechanism for managing access at scale.
</div>
```
┌──────────────────────────────────────── Cloud Azure Identity ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Azure: Cloud Azure Identity platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: Cloud Azure Identity management console                      │   │
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
│    Physical: Cloud Azure Identity infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Identity platform overview and core concepts                      │
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


## PowerShell

```powershell
# List groups
Get-AzADGroup | Select-Object DisplayName, Id, SecurityEnabled

# Create group
New-AzADGroup -DisplayName "storage-prod-readers" -MailNickname "storage-prod-readers" -SecurityEnabled

# Add member
Add-AzADGroupMember -TargetGroupObjectId <group-id> -MemberObjectId <user-id>

# List members
Get-AzADGroupMember -GroupObjectId <group-id>
```

## Dynamic Membership Rules

Dynamic groups evaluate rules against user attributes and update membership automatically.

```bash
# All users in a department
(user.department -eq "Engineering")

# Users by job title
(user.jobTitle -contains "Engineer")

# Country + company
(user.country -eq "AU") and (user.companyName -eq "Contoso")

# Custom extension attribute
(user.extensionAttribute1 -eq "prod-access")

# All guest users
(user.userType -eq "Guest")
```

```bash
# Create dynamic group
az ad group create \
  --display-name "dynamic-engineers" \
  --mail-nickname "dynamic-engineers" \
  --group-types "DynamicMembership" \
  --membership-rule '(user.department -eq "Engineering")' \
  --membership-rule-processing-state "On"
```

Dynamic group updates can take up to 24 hours after a rule or attribute change.

## Nested Groups

Security groups can be nested — a group can be a member of another group. Azure RBAC honours transitive membership.

```bash
# Add group-B as a member of group-A
az ad group member add \
  --group <group-A-object-id> \
  --member-id <group-B-object-id>
```

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| User not receiving access after being added | RBAC propagation delay (up to 10 min) | Wait; verify with `az ad group member check` |
| Dynamic group not updating | Rule evaluation delay or invalid rule syntax | Test rule in Entra Portal → Groups → Dynamic membership rules → Validate rules |
| Cannot assign group to Azure role | Group is not a security group (e.g., M365 group) | Recreate as security group |
| Transitive access not working | PIM eligible group memberships are not transitive | Activate eligible membership before relying on nested access |
| Group deletion didn't remove access immediately | Token caching — existing tokens remain valid until expiry | Wait for token TTL (typically 1 hour) |
