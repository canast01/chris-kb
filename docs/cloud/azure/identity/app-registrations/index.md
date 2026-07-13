---
tags:
  - azure
description: "An app registration in Microsoft Entra ID creates an identity for an application that needs to authenticate with Azure AD or access Azure resources and..."
---
# App Registrations

<div class="kb-summary">
An app registration in Microsoft Entra ID creates an identity for an application that needs to authenticate with Azure AD or access Azure resources and APIs. It is the foundation for service principals, OAuth2 flows, and API permissions.

*Applies to: Azure*
</div>

## App Registration to Service Principal Model

```d2
direction: right

appReg: "App Registration\n(Home Tenant)\nApplication Object" {shape: rectangle}
sp: "Service Principal\n(Each Tenant where app is used)\nService Principal Object" {shape: rectangle}
creds: "Credentials\nClient Secret OR Certificate" {shape: rectangle}
oidc: "OIDC Federation\nno stored secret" {shape: rectangle}
apiPerms: "API Permissions\nMicrosoft Graph · Azure · custom API" {shape: rectangle}
entraToken: "Entra ID Token\nJWT access token" {shape: rectangle}
resource: "Protected Resource\nMicrosoft Graph · Azure ARM · custom API" {shape: rectangle}

appReg -> sp
appReg -> creds
creds -> oidc
oidc -> apiPerms
sp -> entraToken
entraToken -> resource
```

## Creating an App Registration

```bash
# Create an app registration
az ad app create \
  --display-name "my-api-app" \
  --sign-in-audience AzureADMyOrg

# Create with a redirect URI (for web apps)
az ad app create \
  --display-name "my-web-app" \
  --web-redirect-uris "https://app.example.com/auth/callback" \
  --sign-in-audience AzureADMyOrg

# List all app registrations in the tenant
az ad app list \
  --output table

# Show a specific app registration
az ad app show \
  --id <app-id-or-object-id>

# Update the display name
az ad app update \
  --id <app-id> \
  --display-name "my-api-app-v2"

# Delete an app registration
az ad app delete \
  --id <app-id>
```


```text title="Expected output"
{
  "appId": "a7c3f8e2-1b4d-4c9a-8f2e-3d5c7b9a1e4f",
  "displayName": "my-api-app",
  "id": "d9e2f4a1-5c8b-4e7d-9a2f-1b3c5d7e9f2a",
  "signInAudience": "AzureADMyOrg"
}
{
  "appId": "b8d4g9f3-2c5e-5d0b-9g3f-4e6d8c0b2f5g",
  "displayName": "my-web-app",
  "id": "e0f3g5b2-6d9c-5f8e-0b3g-2c4d6e8f0g3b",
  "signInAudience": "AzureADMyOrg",
  "web": {
    "redirectUris": [
      "https://app.example.com/auth/callback"
    ]
  }
}
DisplayName                 AppId                                ObjectId
--------------------------  ----------------------------------  ------------------------------------
my-api-app                  a7c3f8e2-1b4d-4c9a-8f2e-3d5c7b9a1e4f  d9e2f4a1-5c8b-4e7d-9a2f-1b3c5d7e9f2a
my-web-app                  b8d4g9f3-2c5e-5d0b-9g3f-4e6d8c0b2f5g  e0f3g5b2-6d9c-5f8e-0b3g-2c4d6e8f0g3b
legacy-service              c9e5h0g4-3d6f-6e1c-0h4g-5f7e9d1c3g6c  f1g4h6c3-7e0d-6g9f-1c4h-3d5e7f9g1h4c
...
{
  "appId": "a7c3f8e2-1b4d-4c9a-8f2e-3d5c7b9a1e4f",
  "displayName": "my-api-app",
  "id": "d9e2f4a1-5c8b-4e7d-9a2f-1b3c5d7e9f2a",
  "signInAudience": "AzureADMyOrg",
  "createdDateTime": "2024-01-15T10:32:45.123Z"
}
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Insufficient privileges to complete the operation.`** — Ensure your Azure account has Application Administrator or Cloud Application Administrator role in the tenant.
    **`Invalid value provided for parameter 'id': <app-id>. The value should be a valid UUID or object ID.`** — Replace `<app-id>` or `<app-id-or-
## Client Secrets

Client secrets are password credentials used by confidential clients (server-side applications) to authenticate.

```bash
# Add a client secret to an app registration
az ad app credential reset \
  --id <app-id> \
  --years 1 \
  --append

# List credentials on an app (shows key IDs and expiry — not secret values)
az ad app credential list \
  --id <app-id> \
  --output table

# Delete a specific credential
az ad app credential delete \
  --id <app-id> \
  --key-id <key-id>
```


```text title="Expected output"
{
  "appId": "550e8400-e29b-41d4-a716-446655440000",
  "password": "Eby8vdM02xNcWQbOo1xNYcK1xNcWQbOo1x",
  "tenant": "72f988bf-86f1-41af-91ab-2d7cd011db47"
}
KeyId                                DisplayName    StartDate              EndDate
───────────────────────────────────  ─────────────  ─────────────────────  ─────────────────────
a1b2c3d4-e5f6-7890-abcd-ef1234567890 key1           2024-01-15T10:22:33Z   2025-01-15T10:22:33Z
b2c3d4e5-f6a7-8901-bcde-f12345678901 key2           2023-06-20T14:45:12Z   2024-06-20T14:45:12Z
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Invalid value: '<app-id>' is not a valid UUID or application name.`** — Replace `<app-id>` with the actual application ID (UUID format) or registered app name from your Azure AD tenant.
    **`Authorization_RequestDenied: Insufficient privileges to complete the operation.`** — Ensure your Azure CLI account has Application Administrator or Global Administrator role in the Azure AD tenant.
### Secret Rotation Checklist

| Step | Action |
|---|---|
| 1 | Create a new secret on the app registration |
| 2 | Update all consuming services with the new secret |
| 3 | Validate authentication works with the new secret |
| 4 | Delete the old secret |

## Certificates

Certificates are preferred over client secrets for production workloads — they are harder to leak and support key rotation without value exposure.

```bash
# Upload a certificate to an app registration
az ad app credential reset \
  --id <app-id> \
  --cert "@/path/to/certificate.pem" \
  --append

# Generate a self-signed cert and upload in one step
az ad app credential reset \
  --id <app-id> \
  --create-cert \
  --cert "my-app-cert" \
  --keyvault <keyvault-name> \
  --append
```


```text title="Expected output"
{
  "appId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "displayName": "my-application",
  "objectId": "f9e8d7c6-b5a4-3210-fedc-ba9876543210",
  "servicePrincipalId": "12345678-1234-1234-1234-123456789012"
}

Certificate uploaded successfully.
Credential with keyId 'abc123def456' has been added to app registration.

{
  "appId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "displayName": "my-application",
  "objectId": "f9e8d7c6-b5a4-3210-fedc-ba9876543210",
  "servicePrincipalId": "12345678-1234-1234-1234-123456789012"
}

Certificate 'my-app-cert' created in Key Vault 'prod-kv-001'.
Credential with keyId 'xyz789uvw012' has been added to app registration.
```

!!! warning "Common errors"
    **`Certificate file not found: /path/to/certificate.pem`** — Verify the certificate file path exists and is readable with `ls -la /path/to/certificate.pem`.
    **`The Key Vault 'keyvault-name' was not found in subscription`** — Confirm the Key Vault name is correct and exists in the current subscription with `az keyvault list --query "[].name"`.
    **`Insufficient privileges to perform action on resource`** — Ensure your Azure account has the Application Administrator or Global Administrator role assigned in the tenant.
## API Permissions

App registrations request permissions to other APIs (Microsoft Graph, Azure Resource Manager, custom APIs) through the `requiredResourceAccess` manifest field.

```bash
# Add Microsoft Graph User.Read permission (delegated)
az ad app permission add \
  --id <app-id> \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope

# Add Microsoft Graph Directory.Read.All (application, requires admin consent)
az ad app permission add \
  --id <app-id> \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions 7ab1d382-f21e-4acd-a863-ba3e13f7da61=Role

# Grant admin consent for all permissions on the app
az ad app permission admin-consent \
  --id <app-id>

# List permissions on an app
az ad app permission list \
  --id <app-id> \
  --output table
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
Admin consent granted for application 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d'.
ResourceAppId                        PermissionId                         PermissionType    ConsentType
-----------------------------------  -----------------------------------  -----------------  -----------
00000003-0000-0000-c000-000000000000  e1fe6dd8-ba31-4d61-89e7-88639da4683d  Scope              Principal
00000003-0000-0000-c000-000000000000  7ab1d382-f21e-4acd-a863-ba3e13f7da61  Role               Admin
```

!!! warning "Common errors"
    **`Operation failed with status: 'Bad Request'. Details: Code: Authorization_RequestDenied`** — Ensure you have Application Administrator or Global Administrator role in the Azure AD tenant.
    **`No registered application found with identifier '<app-id>'.`** — Verify the app ID is correct and exists in your tenant by running `az ad app list --filter "appId eq '<app-id>'"`.
    **`The permission ID '7ab1d382-f21e-4acd-a863-ba3e13f7da61' does not exist for resource '00000003-0000-0000-c000-000000000000'.`** — Confirm the permission ID is valid for Microsoft Graph by checking the Microsoft Graph permissions reference documentation.
### Common API Permission Types

| Permission Type | Description | Consent |
|---|---|---|
| Delegated (Scope) | App acts on behalf of a signed-in user | User or admin |
| Application (Role) | App acts as itself, no user context | Admin only |

## Application Manifest

The manifest is the full JSON representation of the app registration. Edit it for advanced configuration (app roles, optional claims, token configuration).

```bash
# Export the manifest to a file
az ad app show \
  --id <app-id> \
  --query "@" \
  --output json > app-manifest.json

# Update the app using a modified manifest
az ad app update \
  --id <app-id> \
  --set appRoles=@app-roles.json
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Request_BadRequest: Invalid object identifier '<app-id>'.`** — Verify the app ID is a valid UUID format (e.g., `00000000-0000-0000-0000-000000000000`) and exists in your Azure AD tenant.
    **`FileNotFoundError: [Errno 2] No such file or directory: 'app-roles.json'`** — Ensure the `app-roles.json` file exists in the current working directory and contains valid JSON matching the appRoles schema.
    **`AuthorizationError: Insufficient privileges to complete the operation.`** — Confirm your Azure CLI account has Application Administrator or Global Administrator role in the tenant.
## Service Principal

Every app registration has an associated service principal (enterprise application) in the tenant. Use the service principal for role assignments.

```bash
# Create service principal for an existing app registration
az ad sp create \
  --id <app-id>

# Show the service principal
az ad sp show \
  --id <app-id>

# Assign Contributor role to the service principal on a subscription
az role assignment create \
  --assignee <app-id> \
  --role Contributor \
  --scope "/subscriptions/<subscription-id>"
```


```text title="Expected output"
{
  "appId": "550e8400-e29b-41d4-a716-446655440000",
  "displayName": "my-app-registration",
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "servicePrincipalNames": [
    "https://my-app-registration",
    "550e8400-e29b-41d4-a716-446655440000"
  ],
  "servicePrincipalType": "Application"
}
{
  "appId": "550e8400-e29b-41d4-a716-446655440000",
  "appOwnerOrganizationId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
  "displayName": "my-app-registration",
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "servicePrincipalType": "Application"
}
{
  "canDelegate": false,
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "principalId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "principalType": "ServicePrincipal",
  "roleDefinitionId": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c",
  "scope": "/subscriptions/12345678-1234-1234-1234-123456789012"
}
```

!!! warning "Common errors"
    **`Operation failed with status: 'Bad Request'. Details: Code: Authorization_RequestDenied`** — Ensure your Azure account has sufficient permissions (Owner or User Access Administrator role) on the subscription.
    **`Operation failed with status: 'Not Found'. Details: Code: ResourceNotFound`** — Verify the app-id exists by running `az ad app list --filter "appId eq '<app-id>'"` and use the correct application ID.
    **`The role assignment already exists.`** — Remove the existing role assignment with `az role assignment delete --assignee <app-id> --role Contributor --scope <scope>` before reassigning.
## Common App Registration Patterns

| Pattern | Description |
|---|---|
| Server-to-server daemon | Client credentials flow with certificate auth |
| Web app with user sign-in | Auth code flow with redirect URI |
| API exposing scopes | Defines `oauth2Permissions` for consuming apps |
| Automation service principal | App registration + role assignment to resource group |
