---
tags:
  - azure
  - security
description: "TLS validation in Azure covers certificate management for App Gateway, App Service custom domains, API Management, and Azure Front Door, plus monitoring..."
---
# Azure — TLS Validation

<div class="kb-summary">
TLS validation in Azure covers certificate management for App Gateway, App Service custom domains, API Management, and Azure Front Door, plus monitoring expiry across all endpoints.

*Applies to: Azure*
</div>

```d2
direction: down

tls_termination_points_in_azure: "TLS Termination Points in Azure" {shape: rectangle}
app_gateway_tls_configuration: "App Gateway — TLS Configuration" {shape: rectangle}
app_service_custom_domain_tls: "App Service — Custom Domain TLS" {shape: rectangle}
key_vault_certificate_integration: "Key Vault Certificate Integration" {shape: rectangle}
validating_tls_from_azure_endpoints: "Validating TLS from Azure Endpoints" {shape: rectangle}
monitoring_cert_expiry_prometheus_bl: "Monitoring Cert Expiry — Prometheus Blackbox Exporter" {shape: rectangle}

tls_termination_points_in_azure -> app_gateway_tls_configuration: uses
app_gateway_tls_configuration -> app_service_custom_domain_tls: uses
app_service_custom_domain_tls -> key_vault_certificate_integration: uses
key_vault_certificate_integration -> validating_tls_from_azure_endpoints: uses
validating_tls_from_azure_endpoints -> monitoring_cert_expiry_prometheus_bl: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## TLS Termination Points in Azure

| Service | TLS handling |
|---|---|
| **Application Gateway** | TLS offload or end-to-end TLS; custom cert or managed cert |
| **App Service** | Managed cert (auto-renew) or custom cert from Key Vault |
| **Azure Front Door** | Managed cert (auto-renew) or custom cert |
| **API Management** | Custom cert for developer portal and gateway |
| **Load Balancer** | Layer 4 only — no TLS termination |
| **Azure Firewall Premium** | TLS inspection with CA cert injected into traffic |

## App Gateway — TLS Configuration

```bash
# Create App Gateway with HTTPS listener using a PFX cert
az network application-gateway ssl-cert create \
  --resource-group <rg> \
  --gateway-name <agw-name> \
  --name "my-tls-cert" \
  --cert-file cert.pfx \
  --cert-password <pfx-password>

# Create HTTPS listener
az network application-gateway http-listener create \
  --resource-group <rg> \
  --gateway-name <agw-name> \
  --name "https-listener" \
  --frontend-ip <frontend-ip-config-name> \
  --frontend-port 443 \
  --ssl-cert "my-tls-cert"

# View current SSL policy
az network application-gateway ssl-policy show \
  --resource-group <rg> \
  --gateway-name <agw-name>

# Set minimum TLS 1.2 policy
az network application-gateway ssl-policy set \
  --resource-group <rg> \
  --gateway-name <agw-name> \
  --policy-type Predefined \
  --policy-name AppGwSslPolicy20220101
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Network/applicationGateways/app-gw-01/sslCertificates/my-tls-cert",
  "name": "my-tls-cert",
  "provisioningState": "Succeeded",
  "type": "Microsoft.Network/applicationGateways/sslCertificates"
}
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Network/applicationGateways/app-gw-01/httpListeners/https-listener",
  "name": "https-listener",
  "frontendIpConfiguration": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Network/applicationGateways/app-gw-01/frontendIPConfigurations/appGwPublicFrontendIp"
  },
  "frontendPort": 443,
  "protocol": "Https",
  "sslCertificate": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Network/applicationGateways/app-gw-01/sslCertificates/my-tls-cert"
  },
  "provisioningState": "Succeeded"
}
{
  "cipherSuites": [
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
  ],
  "minProtocolVersion": "TLSv1_2",
  "policyType": "Predefined",
  "policyName": "AppGwSslPolicy20220101"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`(BadRequest) The certificate file 'cert.pfx' does not exist or is not readable.`** — Verify the PFX file path is correct and readable with `ls -l cert.pfx` before running the command.
    **`(BadRequest) The specified frontend IP configuration '<frontend-ip-config-name>' does not exist.`** — List available frontend IP configs with `az network application-gateway frontend-ip list --resource-group <rg> --gateway-name <agw-name>` and use the correct name.
    **`(BadRequest) The certificate password is incorrect or the PFX file is corrupted.`** — Test the PFX password locally with `openssl pkcs12 -in cert.pfx -noout -passin pass:<pfx-password>` to validate before uploading.
## App Service — Custom Domain TLS

```bash
# Upload a custom certificate (PFX) to App Service
az webapp config ssl upload \
  --resource-group <rg> \
  --name <app-name> \
  --certificate-file cert.pfx \
  --certificate-password <pfx-password>

# Get the certificate thumbprint
THUMBPRINT=$(az webapp config ssl list \
  --resource-group <rg> \
  --query "[?name=='<cert-name>'].thumbprint" --output tsv)

# Bind the certificate to the custom domain
az webapp config ssl bind \
  --resource-group <rg> \
  --name <app-name> \
  --certificate-thumbprint "$THUMBPRINT" \
  --ssl-type SNI

# Use App Service managed certificate (auto-renews, free)
az webapp config ssl create \
  --resource-group <rg> \
  --name <app-name> \
  --hostname <custom-domain>
```


```text title="Expected output"
{
  "name": "cert-2024-prod",
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Web/certificates/cert-2024-prod",
  "type": "Microsoft.Web/certificates",
  "location": "eastus",
  "thumbprint": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0",
  "issuer": "CN=*.example.com",
  "subject": "CN=*.example.com",
  "validFrom": "2024-01-15T00:00:00+00:00",
  "validTo": "2025-01-14T23:59:59+00:00",
  "expirationDate": "2025-01-14T23:59:59+00:00"
}
A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0
{
  "name": "myapp-example-com",
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Web/sites/myapp/hostNameSslStates/example.com",
  "hostName": "example.com",
  "sslState": "SniEnabled",
  "thumbprint": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0",
  "virtualIP": "203.0.113.45"
}
{
  "name": "myapp-managed-cert",
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Web/certificates/myapp-managed-cert",
  "type": "Microsoft.Web/certificates",
  "thumbprint": "F9E8D7C6B5A4Z3Y2X1W0V9U8T7S6R5Q4P3O2N1M0",
  "issuer": "CN=example.com, O=Microsoft",
  "validFrom": "2024-02-01T00:00:00+00:00",
  "validTo": "2025-02-01T23:59:59+00:00",
  "managedCertificate": true
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Web/sites/<app-name>' under resource group '<rg>' was not found.`** — Verify the app name and resource group name are correct with `az webapp list --resource-group <rg>`.
    **`BadRequest: Certificate with thumbprint '<THUMBPRINT>' not found in the resource group.`** — Ensure the certificate was successfully uploaded and the thumbprint query matches the actual certificate name with `az webapp config ssl list --resource-group <rg>`.
    **`Conflict: Hostname '<custom-domain>' is not assigned to the app.`
## Key Vault Certificate Integration

App Gateway and App Service can pull TLS certificates directly from Key Vault.

```bash
# App Gateway — reference Key Vault cert (requires managed identity)
az network application-gateway ssl-cert create \
  --resource-group <rg> \
  --gateway-name <agw-name> \
  --name "kv-cert" \
  --key-vault-secret-id "https://<vault-name>.vault.azure.net/secrets/<cert-name>"

# App Service — bind cert from Key Vault
az webapp config ssl import \
  --resource-group <rg> \
  --name <app-name> \
  --key-vault <vault-name> \
  --key-vault-certificate-name <cert-name>
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Network/applicationGateways/agw-prod-01/sslCertificates/kv-cert",
  "name": "kv-cert",
  "provisioningState": "Succeeded",
  "type": "Microsoft.Network/applicationGateways/sslCertificates",
  "keyVaultSecretId": "https://vault-prod-01.vault.azure.net/secrets/wildcard-cert-2024"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Web/sites/myapp-prod/config/web",
  "name": "web",
  "thumbprint": "A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B",
  "hostNames": [
    "myapp-prod.azurewebsites.net",
    "api.example.com"
  ],
  "sslState": "SniEnabled",
  "type": "Microsoft.Web/sites/config/web"
}
```

!!! warning "Common errors"
    **`The user, group or application does not have permission to get the secret from the key vault.`** — Ensure the App Gateway or App Service managed identity has Key Vault Secret User role assigned on the certificate secret.
    **`The specified certificate was not found in the key vault.`** — Verify the certificate name matches exactly in Key Vault (case-sensitive) and use the full secret URI format including `/secrets/` path.
    **`The key vault secret is not in a valid certificate format.`** — Confirm the Key Vault secret contains a valid PFX or PEM certificate with private key, not just the public certificate.
## Validating TLS from Azure Endpoints

```bash
# Check certificate served by an App Service / App Gateway
openssl s_client -connect <hostname>:443 -servername <hostname> </dev/null 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer

# Check full chain
openssl s_client -connect <hostname>:443 -servername <hostname> -showcerts </dev/null 2>/dev/null

# Check expiry only
echo | openssl s_client -connect <hostname>:443 -servername <hostname> 2>/dev/null \
  | openssl x509 -noout -enddate

# Bulk check across multiple endpoints
for host in app1.example.com app2.example.com api.example.com; do
  expiry=$(echo | openssl s_client -connect "${host}:443" -servername "$host" 2>/dev/null \
    | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "$host: $expiry"
done
```


```text title="Expected output"
notBefore=Jan 15 10:22:33 2023 GMT
notAfter=Jan 15 10:22:33 2024 GMT
subject=CN = app1.example.com
issuer=C = US, O = Microsoft Corporation, CN = Microsoft Azure TLS Issuing CA 01

-----BEGIN CERTIFICATE-----
MIIFWzCCBEOgAwIBAgIQfmtf1G8W2uCDA54i1NbqHDANBgkqhkiG9w0BAQsFADBG
MQswCQYDVQQGEwJVUzEiMCAGA1UEChMZTWljcm9zb2Z0IENvcnBvcmF0aW9uMRYw
...
-----END CERTIFICATE-----

app1.example.com: Jan 15 10:22:33 2024 GMT
app2.example.com: Mar 22 14:55:18 2025 GMT
api.example.com: Feb 28 09:11:47 2024 GMT
```

!!! warning "Common errors"
    **`error:0909006C:PEM routines:get_name:no start line`** — Ensure the hostname resolves and port 443 is accessible; check firewall rules and NSG configuration.
    **`unable to get local issuer certificate`** — This is expected for self-signed or internal CAs; add `-CAfile <cert-bundle>` or use `-showcerts` to verify the full chain is served by the endpoint.
## Monitoring Cert Expiry — Prometheus Blackbox Exporter

```yaml
# prometheus.yml scrape config
- job_name: azure_tls_expiry
  metrics_path: /probe
  params:
    module: [tcp_connect]
  static_configs:
    - targets:
        - app.example.com:443
        - api.example.com:443
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: blackbox-exporter:9115
```

Alert rules:

```yaml
- alert: AzureTLSCertExpiryWarning
  expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 30
  labels:
    severity: warning
  annotations:
    summary: "TLS cert on {{ $labels.instance }} expires in < 30 days"

- alert: AzureTLSCertExpiryCritical
  expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 7
  labels:
    severity: critical
  annotations:
    summary: "TLS cert on {{ $labels.instance }} expires in < 7 days"
```

## Minimum TLS Standards

| Component | Minimum required | Recommended |
|---|---|---|
| App Gateway SSL policy | TLS 1.2 | `AppGwSslPolicy20220101` (TLS 1.2 + strong ciphers) |
| App Service | TLS 1.2 (enforced by default) | TLS 1.2 minimum in App Service → TLS/SSL settings |
| API Management | TLS 1.2 | Disable TLS 1.0/1.1 in APIM portal settings |
| Azure Front Door | TLS 1.2 | Enforced automatically |

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| Browser shows cert warning on custom domain | Certificate not bound to SNI or wrong cert | Verify binding: `az webapp config ssl list --resource-group <rg>` |
| App Gateway returning self-signed cert | Listener not using the uploaded SSL cert | Check listener SSL cert association in AGW config |
| Key Vault cert integration failing | App Gateway managed identity missing Key Vault access | Assign `Key Vault Secrets User` to AGW managed identity |
| Managed cert not renewing | Custom domain DNS no longer points to App Service | Verify DNS A/CNAME record; remove and re-add managed cert |
| TLS 1.0/1.1 still negotiated | Policy not enforced at App Service level | Set minimum TLS in App Service → Configuration → TLS/SSL settings → Minimum TLS Version |
