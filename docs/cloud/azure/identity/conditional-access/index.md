---
tags:
  - azure
description: "Conditional Access (CA) policies are the enforcement engine of Zero Trust in Microsoft Entra ID. They evaluate signals (user, location, device, app, risk)..."
---
# Conditional Access

<div class="kb-summary">
Conditional Access (CA) policies are the enforcement engine of Zero Trust in Microsoft Entra ID. They evaluate signals (user, location, device, app, risk) and grant, block, or require additional controls (MFA, compliant device) before granting access.

*Applies to: Azure*
</div>

## Conditional Access Evaluation Flow

```d2
direction: right

signIn: "Sign-in Attempt" {shape: rectangle}
signals: "Signals Evaluated\nuser · location · device · app · risk" {shape: rectangle}
policiesEval: "All matching CA policies evaluated" {shape: rectangle}
block: "block" {shape: rectangle}
blocked: "Access BLOCKED" {shape: rectangle}
granted: "Access GRANTED\ntoken issued" {shape: rectangle}
mfaReq: "mfaReq" {shape: rectangle}
mfaComplete: "mfaComplete" {shape: rectangle}
compliantReq: "compliantReq" {shape: rectangle}

signIn -> signals
signals -> policiesEval
policiesEval -> block
```

## CA Policy Creation

Conditional Access policies are primarily managed through the Entra ID portal or Microsoft Graph API. The `az` CLI covers some operations via the `az ad` extension and `az rest`.

```bash
# List all Conditional Access policies via Microsoft Graph
az rest \
  --method GET \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies" \
  --query "value[].{Name:displayName, State:state, ID:id}" \
  --output table

# Get details of a specific CA policy
az rest \
  --method GET \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies/<policy-id>"

# Create a CA policy (require MFA for all users)
az rest \
  --method POST \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies" \
  --body '{
    "displayName": "Require MFA for all users",
    "state": "enabledForReportingButNotEnforced",
    "conditions": {
      "users": {"includeUsers": ["All"]},
      "applications": {"includeApplications": ["All"]}
    },
    "grantControls": {
      "operator": "OR",
      "builtInControls": ["mfa"]
    }
  }'

# Enable a CA policy (change state to enabled)
az rest \
  --method PATCH \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies/<policy-id>" \
  --body '{"state": "enabled"}'

# Delete a CA policy
az rest \
  --method DELETE \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies/<policy-id>"
```


```text title="Expected output"
Name                                    State                              ID
──────────────────────────────────────  ───────────────────────────────────  ────────────────────────────────────
Require MFA for all users               enabledForReportingButNotEnforced   a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6
Block legacy authentication             enabled                            b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7
Require compliant device                enabled                            c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8
Require MFA for admin roles              enabled                            d4e5f6g7-h8i9-40j0-k1l2-m3n4o5p6q7r8
Block high-risk sign-ins                enabledForReportingButNotEnforced   e5f6g7h8-i9j0-41k1-l2m3-n4o5p6q7r8s9

{
  "id": "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "displayName": "Require MFA for all users",
  "state": "enabledForReportingButNotEnforced",
  "conditions": {...},
  "grantControls": {...}
}

{
  "id": "f6g7h8i9-j0k1-42l2-m3n4-o5p6q7r8s9t0",
  "displayName": "Require MFA for all users",
  "state": "enabledForReportingButNotEnforced"
}

(no output — command completes silently)

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Authorization_RequestDenied: Insufficient privileges to complete the operation.` | Ensure your Azure AD account has the Conditional Access Administrator or Global Administrator role assigned. |
    | `Invalid template expansion: <policy-id>` | Replace `<policy-id>` with an actual policy UUID (e.g., `a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6`) from the list output. |
    | `Bad Request: Invalid request body` | Validate the JSON body syntax and ensure required fields like `displayName`, `state`, `conditions`, and `grantControls` are properly formatted without trailing commas. |
## Conditions

Conditions define the context in which a policy applies. Multiple conditions can be combined with AND logic.

| Condition | Options | Example Use |
|---|---|---|
| Users and groups | Include/exclude users, groups, roles, guests | Exclude break-glass accounts |
| Cloud apps | Include/exclude specific apps or all apps | Target Office 365 only |
| Locations | Named locations, trusted IPs, countries | Block access from outside approved countries |
| Device platforms | Windows, iOS, Android, macOS, Linux | Require compliant device for mobile |
| Client apps | Browser, mobile/desktop apps, legacy auth | Block legacy authentication clients |
| Sign-in risk | Low, medium, high (requires Entra ID P2) | Require MFA when sign-in risk is high |
| User risk | Low, medium, high (requires Entra ID P2) | Block sign-in when user risk is high |

## Grant Controls

Grant controls define what is required for access to be granted when conditions are met.

| Control | Description |
|---|---|
| Require MFA | User must complete multi-factor authentication |
| Require compliant device | Device must be Intune-compliant |
| Require hybrid Azure AD joined device | Device must be hybrid joined |
| Require approved client app | App must be on the approved list |
| Require app protection policy | App must have Intune MAM policy |
| Block access | Deny all access when conditions match |

```bash
# Create a policy to block legacy authentication
az rest \
  --method POST \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies" \
  --body '{
    "displayName": "Block legacy authentication",
    "state": "enabled",
    "conditions": {
      "users": {"includeUsers": ["All"]},
      "applications": {"includeApplications": ["All"]},
      "clientAppTypes": ["exchangeActiveSync", "other"]
    },
    "grantControls": {
      "operator": "OR",
      "builtInControls": ["block"]
    }
  }'
```


```text title="Expected output"
{
  "id": "12a4b5c6-7d8e-9f0a-1b2c-3d4e5f6a7b8c",
  "displayName": "Block legacy authentication",
  "state": "enabled",
  "createdDateTime": "2024-01-15T09:42:33.1234567Z",
  "modifiedDateTime": "2024-01-15T09:42:33.1234567Z",
  "conditions": {
    "users": {
      "includeUsers": [
        "All"
      ]
    },
    "applications": {
      "includeApplications": [
        "All"
      ]
    },
    "clientAppTypes": [
      "exchangeActiveSync",
      "other"
    ]
  },
  "grantControls": {
    "operator": "OR",
    "builtInControls": [
      "block"
    ]
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Authorization_RequestDenied` | Ensure your Azure AD account has the Policy.ReadWrite.ConditionalAccess permission or is assigned the Conditional Access Administrator role. |
    | `Invalid JSON in request body` | Validate the JSON syntax using `jq` before submission: `echo '<json>' | jq .` |
    | `Insufficient privileges to complete the operation` | Verify you are authenticated with `az account show` and have Global Administrator or Conditional Access Administrator role in the target tenant. |
## Named Locations

Named locations represent trusted IP ranges or countries/regions used in Conditional Access conditions.

```bash
# Create a named location (IP range)
az rest \
  --method POST \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccess/namedLocations" \
  --body '{
    "@odata.type": "#microsoft.graph.ipNamedLocation",
    "displayName": "Office Network",
    "isTrusted": true,
    "ipRanges": [
      {"@odata.type": "#microsoft.graph.iPv4CidrRange", "cidrAddress": "203.0.113.0/24"}
    ]
  }'

# List named locations
az rest \
  --method GET \
  --url "https://graph.microsoft.com/v1.0/identity/conditionalAccess/namedLocations" \
  --query "value[].{Name:displayName, Type:\"@odata.type\", ID:id}" \
  --output table
```


```text title="Expected output"
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "displayName": "Office Network",
  "createdDateTime": "2024-01-15T10:32:45.123Z",
  "modifiedDateTime": "2024-01-15T10:32:45.123Z",
  "@odata.type": "#microsoft.graph.ipNamedLocation",
  "isTrusted": true,
  "ipRanges": [
    {
      "@odata.type": "#microsoft.graph.iPv4CidrRange",
      "cidrAddress": "203.0.113.0/24"
    }
  ]
}

Name                 Type                                    ID
-------------------  ----------------------------------------  ------------------------------------
Office Network       #microsoft.graph.ipNamedLocation        550e8400-e29b-41d4-a716-446655440000
Corporate VPN        #microsoft.graph.ipNamedLocation        660e8400-e29b-41d4-a716-446655440001
Guest WiFi           #microsoft.graph.countryNamedLocation   770e8400-e29b-41d4-a716-446655440002
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Authorization_RequestDenied: Insufficient privileges to complete the operation.` | Ensure your Azure AD account has the "Conditional Access Administrator" or "Global Administrator" role assigned. |
    | `Invalid JSON in request body` | Validate the JSON syntax in the `--body` parameter; check for missing commas or mismatched quotes around field names like `@odata.type`. |
    | `The request body parameter 'ipRanges' cannot be null or empty.` | Include at least one valid IPv4 or IPv6 CIDR range in the `ipRanges` array with proper `@odata.type` declaration. |
## Report-Only Mode

Always deploy new policies in `enabledForReportingButNotEnforced` (report-only) state first. This allows you to see sign-in impact in logs before enforcing.

| State | Description |
|---|---|
| `enabled` | Policy is enforced |
| `disabled` | Policy is inactive |
| `enabledForReportingButNotEnforced` | Policy evaluates but does not enforce; logs impact |

### Sign-in Log Review

```bash
# Check CA policy impact in sign-in logs via Graph
az rest \
  --method GET \
  --url "https://graph.microsoft.com/v1.0/auditLogs/signIns?\$filter=createdDateTime ge 2026-05-01T00:00:00Z&\$select=userPrincipalName,appDisplayName,conditionalAccessStatus,appliedConditionalAccessPolicies" \
  --query "value[?conditionalAccessStatus != 'notApplied'][].{User:userPrincipalName, App:appDisplayName, Status:conditionalAccessStatus}"
```


```text title="Expected output"
[
  {
    "User": "john.smith@contoso.com",
    "App": "Microsoft Teams",
    "Status": "success"
  },
  {
    "User": "sarah.jones@contoso.com",
    "App": "Azure Portal",
    "Status": "failure"
  },
  {
    "User": "mike.chen@contoso.com",
    "App": "Microsoft Exchange Online",
    "Status": "success"
  },
  {
    "User": "lisa.wang@contoso.com",
    "App": "SharePoint Online",
    "Status": "success"
  },
  {
    "User": "david.kumar@contoso.com",
    "App": "Azure Portal",
    "Status": "failure"
  }
]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Authorization_RequestDenied` | Ensure your Azure CLI account has `AuditLog.Read.All` permission in Microsoft Graph API. |
    | `Invalid filter clause value: '2026-05-01T00:00:00Z'` | Use a valid past date in ISO 8601 format (e.g., `2024-05-01T00:00:00Z`) instead of a future date. |
## CA Policy Deployment Checklist

| Step | Action |
|---|---|
| 1 | Identify break-glass accounts and exclude from all CA policies |
| 2 | Create policy in report-only mode |
| 3 | Review sign-in logs for 48–72 hours |
| 4 | Confirm no legitimate access is blocked |
| 5 | Switch policy to `enabled` |
| 6 | Monitor sign-in failure rates for 24 hours post-enable |
