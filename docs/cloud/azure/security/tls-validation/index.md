# Azure — TLS Validation


<div class="kb-summary">
TLS validation in Azure covers certificate management for App Gateway, App Service custom domains, API Management, and Azure Front Door, plus monitoring expiry across all endpoints.
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
