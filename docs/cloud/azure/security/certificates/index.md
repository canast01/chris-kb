---
tags:
  - azure
  - security
---
# Azure — Certificates


<div class="kb-summary">
Azure Key Vault manages X.509 certificates, providing lifecycle management including creation, import, auto-renewal, and expiry alerting. Key Vault integrates with App Gateway, API Management, App Service, and other services for SSL/TLS offloading.
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


## Creating a Key Vault Certificate

```bash
# Generate a self-signed certificate in Key Vault
az keyvault certificate create \
  --vault-name myKeyVault \
  --name myCert \
  --policy "$(az keyvault certificate get-default-policy)"

# Create with a custom policy (CA-issued, auto-renewal)
cat > cert-policy.json <<'EOF'
{
  "issuerParameters": {"name": "DigiCert"},
  "keyProperties": {"exportable": true, "keySize": 2048, "keyType": "RSA"},
  "lifetimeActions": [{"action": {"actionType": "AutoRenew"}, "trigger": {"daysBeforeExpiry": 30}}],
  "secretProperties": {"contentType": "application/x-pkcs12"},
  "x509CertificateProperties": {
    "subject": "CN=example.com",
    "subjectAlternativeNames": {"dnsNames": ["example.com", "www.example.com"]},
    "validityInMonths": 12
  }
}
EOF

az keyvault certificate create \
  --vault-name myKeyVault \
  --name my-ca-cert \
  --policy @cert-policy.json
```

## Importing Certificates

```bash
# Import a PFX certificate
az keyvault certificate import \
  --vault-name myKeyVault \
  --name imported-cert \
  --file mycert.pfx \
  --password "PfxP@ssword"

# Import a PEM certificate
az keyvault certificate import \
  --vault-name myKeyVault \
  --name imported-pem-cert \
  --file mycert.pem

# List certificates in a vault
az keyvault certificate list \
  --vault-name myKeyVault \
  --output table

# Show certificate details including expiry
az keyvault certificate show \
  --vault-name myKeyVault \
  --name myCert \
  --output json
```

## Certificate Versions and Rotation

Each update to a certificate creates a new version. The current version is the default unless a specific version is referenced.

```bash
# List all versions of a certificate
az keyvault certificate list-versions \
  --vault-name myKeyVault \
  --name myCert \
  --output table

# Download the certificate as a PEM file
az keyvault certificate download \
  --vault-name myKeyVault \
  --name myCert \
  --file downloaded-cert.pem \
  --encoding PEM

# Get the secret (includes private key) as base64 PFX
az keyvault secret download \
  --vault-name myKeyVault \
  --name myCert \
  --file cert-with-key.pfx \
  --encoding base64
```

## Auto-Rotation with Lifetime Actions

| Action Type     | Trigger                  | Effect                                   |
|-----------------|--------------------------|------------------------------------------|
| AutoRenew       | daysBeforeExpiry / pct   | Requests a new certificate automatically |
| EmailContacts   | daysBeforeExpiry / pct   | Sends email to vault contacts            |

```bash
# Update lifetime actions on an existing certificate policy
az keyvault certificate get-default-policy | \
  jq '.lifetimeActions = [{"action":{"actionType":"AutoRenew"},"trigger":{"daysBeforeExpiry":45}}]' > updated-policy.json

az keyvault certificate set-attributes \
  --vault-name myKeyVault \
  --name myCert \
  --policy @updated-policy.json
```

## App Gateway Integration

App Gateway can reference Key Vault certificates directly via a managed identity, avoiding manual certificate uploads.

```bash
# Assign managed identity to the App Gateway
az network application-gateway identity assign \
  --resource-group myRG \
  --gateway-name myAppGW \
  --identity /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myAppGWIdentity

# Grant the identity access to Key Vault secrets (for certificate retrieval)
az keyvault set-policy \
  --name myKeyVault \
  --object-id <identity-object-id> \
  --secret-permissions get list

# Add SSL cert to App Gateway referencing KV secret URI
az network application-gateway ssl-cert create \
  --gateway-name myAppGW \
  --resource-group myRG \
  --name kv-cert \
  --key-vault-secret-id "https://myKeyVault.vault.azure.net/secrets/myCert"
```

## Certificate Expiry Monitoring

```bash
# Query Log Analytics for certificates expiring within 30 days
az monitor log-analytics query \
  --workspace /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.OperationalInsights/workspaces/myWorkspace \
  --analytics-query "AzureDiagnostics | where ResourceType == 'VAULTS' | where OperationName == 'CertificateNearExpiry' | project TimeGenerated, requestUri_s, ResultDescription" \
  --output table

# Set up email contact for expiry alerts
az keyvault certificate set-attributes \
  --vault-name myKeyVault \
  --name myCert \
  --email-addresses ops@example.com
```
