---
tags:
  - azure
---
# Microsoft Entra ID

<div class="kb-summary">
Microsoft Entra ID (formerly Azure Active Directory) is the cloud-based identity and access management service. It provides authentication, authorisation, and directory services for Azure resources, Microsoft 365, and integrated SaaS applications.

*Applies to: Azure*
</div>

## Entra ID Identity Architecture

```d2
direction: right

onpremAD: "On-Premises AD\nSource of truth" {shape: rectangle}
adConnect: "Azure AD Connect\nDelta sync every 30 min" {shape: rectangle}
entraId: "Microsoft Entra ID\nCloud identity plane" {shape: rectangle}
sso: "SSO\nMicrosoft 365 · SaaS · Azure" {shape: rectangle}
ca: "Conditional Access\nMFA · compliant device · location" {shape: rectangle}
pim: "PIM\nJIT privileged access" {shape: rectangle}
mfa: "MFA\nAuthenticator · FIDO2" {shape: rectangle}

onpremAD -> adConnect
adConnect -> entraId
entraId -> sso
entraId -> ca
entraId -> pim
ca -> mfa
```

## Tenant Overview

```bash
# Show current tenant details
az account show \
  --query "{TenantID:tenantId, SubscriptionID:id, Name:name}"

# List all tenants accessible to the logged-in account
az account tenant list \
  --output table

# Show Entra ID tenant configuration
az rest \
  --method GET \
  --url "https://graph.microsoft.com/v1.0/organization" \
  --query "value[0].{TenantID:id, DisplayName:displayName, Domain:verifiedDomains[0].name}"
```


```text title="Expected output"
{
  "TenantID": "a7c3f8e2-1b4d-4c9a-8f2e-3d5c7b9a1e4f",
  "SubscriptionID": "12345678-1234-1234-1234-123456789012",
  "Name": "Production"
}

TenantId                             DisplayName           CountryCode
------------------------------------  --------------------  -----------
a7c3f8e2-1b4d-4c9a-8f2e-3d5c7b9a1e4f  Contoso Inc           US
b9d4g9f3-2c5e-5d0b-9g3f-4e6d8c0b2f5g  Partner Org           CA

{
  "TenantID": "a7c3f8e2-1b4d-4c9a-8f2e-3d5c7b9a1e4f",
  "DisplayName": "Contoso Inc",
  "Domain": "contoso.onmicrosoft.com"
}
```

!!! warning "Common errors"
    **`ERROR: The command failed with an unexpected status code "401 Unauthorized".`** — Run `az login` to authenticate and ensure your account has permissions to read tenant information.
    **`ERROR: No subscriptions found in account.`** — Verify the account is assigned at least one subscription in the Azure portal or contact your subscription administrator.
## User Management

```bash
# Create a new user
az ad user create \
  --display-name "Chris Anastasiadis" \
  --user-principal-name chris.a@example.com \
  --password "TempP@ssw0rd!" \
  --force-change-password-next-sign-in true

# List all users in the tenant
az ad user list \
  --output table

# Show a specific user
az ad user show \
  --id chris.a@example.com

# Update user display name
az ad user update \
  --id chris.a@example.com \
  --display-name "Christos Anastasiadis"

# Disable a user account
az ad user update \
  --id chris.a@example.com \
  --account-enabled false

# Delete a user
az ad user delete \
  --id chris.a@example.com

# List user's group memberships
az ad user get-member-groups \
  --id chris.a@example.com \
  --output table
```


```text title="Expected output"
{
  "accountEnabled": true,
  "displayName": "Chris Anastasiadis",
  "id": "a7c3f9e2-1b4d-4c8a-9f2e-3d5c7b1a9e4f",
  "userPrincipalName": "chris.a@example.com",
  "userType": "Member"
}
DisplayName                    UserPrincipalName              UserId
-----------------------------  -----------------------------  ------------------------------------
Chris Anastasiadis             chris.a@example.com            a7c3f9e2-1b4d-4c8a-9f2e-3d5c7b1a9e4f
Alice Johnson                  alice.j@example.com            b8d4g0f3-2c5e-5d9b-0g3f-4e6d8c2b0f5g
Bob Martinez                   bob.m@example.com              c9e5h1g4-3d6f-6e0c-1h4g-5f7e9d3c1g6h
Diana Chen                     diana.c@example.com            d0f6i2h5-4e7g-7f1d-2i5h-6g8f0e4d2h7i
...
{
  "accountEnabled": true,
  "displayName": "Chris Anastasiadis",
  "id": "a7c3f9e2-1b4d-4c8a-9f2e-3d5c7b1a9e4f",
  "userPrincipalName": "chris.a@example.com",
  "userType": "Member"
}
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
a7c3f9e2-1b4d-4c8a-9f2e-3d5c7b1a9e4f
```

!!! warning "Common errors"
    **`The user object referenced by id does not exist or one of its referenced properties is invalid.`** — Verify the user exists and the UPN is correctly formatted; use `az ad user list` to confirm the user was created.
    **`Insufficient privileges to complete the operation.`** — Ensure your Azure CLI account has User Administrator or Global Administrator role assigned in Entra ID.
### User Types

| User Type | Description |
|---|---|
| Member | Internal users created in the tenant |
| Guest (B2B) | External users invited via Azure AD B2B |
| Service Principal | Application identity, not a human user |
| Managed Identity | Azure-managed service identity |

## Group Management

```bash
# Create a security group
az ad group create \
  --display-name "sg-platform-engineers" \
  --mail-nickname "sg-platform-engineers"

# List all groups
az ad group list \
  --output table

# Add a member to a group
az ad group member add \
  --group sg-platform-engineers \
  --member-id <user-object-id>

# List group members
az ad group member list \
  --group sg-platform-engineers \
  --output table

# Check if a user is a member of a group
az ad group member check \
  --group sg-platform-engineers \
  --member-id <user-object-id>

# Remove a member from a group
az ad group member remove \
  --group sg-platform-engineers \
  --member-id <user-object-id>
```


```text title="Expected output"
{
  "displayName": "sg-platform-engineers",
  "id": "a7c3f891-2d45-4e8b-9f12-7b5e8c2a1d93",
  "mailNickname": "sg-platform-engineers",
  "mailEnabled": false,
  "securityEnabled": true
}
DisplayName                    MailNickname                   Id
-----------------------------  -----------------------------  ------------------------------------
sg-platform-engineers         sg-platform-engineers         a7c3f891-2d45-4e8b-9f12-7b5e8c2a1d93
sg-developers                  sg-developers                  b8d4g902-3e56-5f9c-0g23-8c6f9d3b2e04
sg-security-team               sg-security-team               c9e5h013-4f67-6g0d-1h34-9d7g0e4c3f15
...
(no output — command completes silently)
DisplayName                    UserPrincipalName              Id
-----------------------------  ---------------------------    ------------------------------------
alice.johnson@contoso.com      alice.johnson@contoso.com      d0f6i124-5g78-7h1e-2i45-0e8h1f5d4g26
bob.smith@contoso.com          bob.smith@contoso.com          e1g7j235-6h89-8i2f-3j56-1f9i2g6e5h37
...
true
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Operation failed with status: 'Bad Request'. Details: Code: Authorization_RequestDenied`** — Ensure your Azure account has sufficient permissions (Directory.ReadWrite.All or Group.ReadWrite.All) in Entra ID.
    **`No group found with name 'sg-platform-engineers'.`** — Use the full group object ID instead of the display name, or verify the group exists with `az ad group list`.
    **`Invalid object identifier '<user-object-id>'.`** — Replace `<user-object-id>` with an actual user object ID from `az ad user list --query "[].id"`.
## Hybrid Identity and Connect Sync

For organisations with on-premises Active Directory, Azure AD Connect or Entra Connect Sync synchronises identities to Entra ID.

| Hybrid Component | Purpose |
|---|---|
| Entra Connect Sync | Sync on-prem AD objects to Entra ID |
| Entra Connect Cloud Sync | Lightweight agent-based sync (replaces Connect for most scenarios) |
| Password Hash Sync (PHS) | Sync password hashes for cloud authentication |
| Pass-Through Authentication (PTA) | Authenticate against on-prem AD directly |
| Federation (ADFS) | On-prem STS issues tokens; Entra ID trusts federation |

```bash
# View sync status (on-prem Entra Connect server — PowerShell)
# Get-ADSyncScheduler
# Start-ADSyncSyncCycle -PolicyType Delta

# Verify last directory sync time via Graph
az rest \
  --method GET \
  --url "https://graph.microsoft.com/v1.0/organization?$select=onPremisesLastSyncDateTime,onPremisesSyncEnabled" \
  --query "value[0].{LastSync:onPremisesLastSyncDateTime, SyncEnabled:onPremisesSyncEnabled}"
```


```text title="Expected output"
{
  "LastSync": "2024-01-15T14:32:47Z",
  "SyncEnabled": true
}
```

!!! warning "Common errors"
    **`Authorization_RequestDenied`** — Ensure your service principal or user account has `Organization.Read.All` permission in Entra ID.
    **`Invalid resource identifier`** — Verify you are authenticated to Azure with `az login` and have access to the correct tenant using `az account set --subscription <tenant-id>`.
## Domain Management

```bash
# List verified domains in the tenant
az rest \
  --method GET \
  --url "https://graph.microsoft.com/v1.0/domains" \
  --query "value[].{Domain:id, IsDefault:isDefault, IsVerified:isVerified}" \
  --output table
```


```text title="Expected output"
Domain                          IsDefault    IsVerified
------------------------------  -----------  -----------
contoso.com                     False        True
contoso.onmicrosoft.com         True         True
partner.contoso.com             False        True
staging.contoso.com             False        False
dev.contoso.com                 False        True
```

!!! warning "Common errors"
    **`Authorization_RequestDenied`** — Ensure your Azure CLI account has at least Directory Reader role or higher in the tenant.
    **`InvalidAuthenticationToken`** — Run `az login` to refresh your authentication token, as it may have expired.
## Entra ID Licence Tiers

| Feature | Free | P1 | P2 |
|---|---|---|---|
| Basic user/group management | Yes | Yes | Yes |
| Conditional Access | No | Yes | Yes |
| MFA | Basic | Yes | Yes |
| Identity Protection | No | No | Yes |
| Privileged Identity Management | No | No | Yes |
| Access Reviews | No | No | Yes |
| Risk-based Conditional Access | No | No | Yes |
