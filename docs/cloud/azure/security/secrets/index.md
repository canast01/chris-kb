---
tags:
  - azure
  - security
---
# Azure — Key Vault Secrets


<div class="kb-summary">
Key Vault secrets store arbitrary string values — passwords, connection strings, API keys, tokens — with versioning, expiry, access control, and audit logging.
</div>
```text
┌──────────────────────────────────────── Cloud Azure Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Azure: Cloud Azure Security platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: Cloud Azure Security management console                      │   │
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
│    Physical: Cloud Azure Security infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Security platform overview and core concepts                      │
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


## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Secret Structure

```text
Vault: my-vault
  └── Secret: db-connection-string
        ├── Version: abc123  (current)  → "Server=sql01;User=app;Password=S3cr3t"
        ├── Version: def456  (previous) → "Server=sql01;User=app;Password=0ldP@ss"
        └── Version: ghi789  (disabled)
```

Each `set` operation creates a new version. The current version is the most recently set enabled version.

## Managing Secrets

```bash
# Create / update a secret (creates new version)
az keyvault secret set \
  --vault-name <vault-name> \
  --name "db-password" \
  --value "S3cur3P@ss!"

# Set with expiry and content type
az keyvault secret set \
  --vault-name <vault-name> \
  --name "api-key" \
  --value "<api-key-value>" \
  --expires "2026-12-31T00:00:00Z" \
  --content-type "application/x-api-key"

# Read current value
az keyvault secret show \
  --vault-name <vault-name> \
  --name "db-password" \
  --query value --output tsv

# Read a specific version
az keyvault secret show \
  --vault-name <vault-name> \
  --name "db-password" \
  --version <version-id> \
  --query value --output tsv

# List secrets (names only — values require Secrets User role)
az keyvault secret list --vault-name <vault-name> --output table

# List all versions of a secret
az keyvault secret list-versions \
  --vault-name <vault-name> \
  --name "db-password" \
  --output table

# Disable a specific version
az keyvault secret set-attributes \
  --vault-name <vault-name> \
  --name "db-password" \
  --version <version-id> \
  --enabled false

# Delete (soft-delete — recoverable)
az keyvault secret delete --vault-name <vault-name> --name "db-password"

# Recover deleted secret
az keyvault secret recover --vault-name <vault-name> --name "db-password"
```

## Secret References in Azure Services

### App Service — Key Vault Reference

Reference secrets directly in App Service configuration without copying them.

```bash
# Get the secret URI
SECRET_URI=$(az keyvault secret show \
  --vault-name <vault-name> \
  --name "db-password" \
  --query id --output tsv)

# Set App Service config to reference the secret
az webapp config appsettings set \
  --name <app-name> \
  --resource-group <rg> \
  --settings "DB_PASSWORD=@Microsoft.KeyVault(SecretUri=${SECRET_URI})"
```

The App Service managed identity must have `Key Vault Secrets User` role on the vault.

### AKS — External Secrets Operator (ESO)

```yaml
# ExternalSecret — pulls from Key Vault and creates a Kubernetes Secret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: azure-keyvault-store
    kind: SecretStore
  target:
    name: db-credentials
  data:
    - secretKey: password
      remoteRef:
        key: db-password
```

### AKS — CSI Secret Store Driver

```yaml
# SecretProviderClass
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: azure-kv-secrets
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    clientID: "<managed-identity-client-id>"
    keyvaultName: <vault-name>
    objects: |
      array:
        - |
          objectName: db-password
          objectType: secret
    tenantID: <tenant-id>
```

## Secret Rotation

Secret rotation is a manual process (or automated via Event Grid + Azure Functions):

```text
Pattern: dual-secret rotation
  1. Generate new credential and write to secret (new version)
  2. Update application to use new version
  3. Revoke old credential
  4. Disable old secret version
```

```bash
# Write new version
az keyvault secret set --vault-name <vault-name> --name "db-password" --value "<new-password>"

# After confirming app works on new version, disable old version
az keyvault secret set-attributes \
  --vault-name <vault-name> \
  --name "db-password" \
  --version <old-version-id> \
  --enabled false
```

## Monitoring Secret Expiry

```bash
# List secrets expiring within 30 days
az keyvault secret list --vault-name <vault-name> --query \
  "[?attributes.expires != null && attributes.expires < '$(date -u -d '+30 days' +%Y-%m-%dT%H:%M:%SZ)'].{name:name, expires:attributes.expires}" \
  --output table
```

Log Analytics alert for expiring secrets:

```kusto
AzureDiagnostics
| where ResourceType == "VAULTS" and Category == "AuditEvent"
| where OperationName == "SecretGet" and ResultType == "Success"
| extend SecretName = tostring(id_s)
| summarize LastAccessed=max(TimeGenerated) by SecretName
```

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| App returns empty string for secret reference | Managed identity lacks Secrets User role | Assign `Key Vault Secrets User` to the app's identity |
| App Service reference shows `Microsoft.KeyVault(...)` instead of value | App hasn't restarted after config change, or vault reference URL malformed | Restart app; verify URI format includes `/secrets/` path |
| Secret value is stale in app | App caches config at startup; Key Vault references refresh on app restart | Restart app or use SDK to read secrets dynamically |
| Secret version missing | Deleted and purge-protected vault | List deleted: `az keyvault secret list-deleted --vault-name <vault>` |
| Cannot list secrets | Missing `Key Vault Reader` or `Secrets Officer` on control plane | `az role assignment list --scope /subscriptions/.../vaults/<vault>` |
