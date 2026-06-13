---
tags:
  - networking
---
# Azure OpenAI Networking


<div class="kb-summary">
By default, Azure OpenAI resources accept traffic from all public IP addresses. For production deployments, restrict access using private endpoints, VNet integration, and firewall rules.

*Applies to: Azure OpenAI*
</div>
```text
┌───────────────────────────────────── Ai Azure Openai Networking ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                       Azure Openai: Ai Azure Openai Networking platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Ai Azure Openai Networking management console                   │   │
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
│    Physical: Ai Azure Openai Networking infrastructure · management network · monitoring              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure Openai       = Ai Azure Openai Networking platform overview and core concepts                │
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


## Private Endpoints

Private endpoints place the Azure OpenAI resource on your VNet with a private IP address, removing exposure to the public internet.

```bash
# Create a private endpoint for the Azure OpenAI resource
az network private-endpoint create \
  --name aoai-private-ep \
  --resource-group my-rg \
  --vnet-name my-vnet \
  --subnet private-endpoints-subnet \
  --private-connection-resource-id \
    "/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource" \
  --group-id account \
  --connection-name aoai-private-connection \
  --location eastus

# Create private DNS zone for resolution
az network private-dns zone create \
  --resource-group my-rg \
  --name "privatelink.openai.azure.com"

az network private-dns link vnet create \
  --resource-group my-rg \
  --zone-name "privatelink.openai.azure.com" \
  --name aoai-dns-link \
  --virtual-network my-vnet \
  --registration-enabled false

# Add DNS record group to auto-manage A records
az network private-endpoint dns-zone-group create \
  --resource-group my-rg \
  --endpoint-name aoai-private-ep \
  --name aoai-dns-zone-group \
  --private-dns-zone "privatelink.openai.azure.com" \
  --zone-name openai
```

## Disabling Public Access

After a private endpoint is in place, disable public network access:

```bash
az cognitiveservices account update \
  --name my-aoai-resource \
  --resource-group my-rg \
  --custom-subdomain-name my-aoai-resource \
  --public-network-access Disabled
```

Traffic now flows only through the private endpoint.

## Firewall Rules

If public access must remain on, restrict to known CIDR ranges:

```bash
# Allow only specific IP ranges
az cognitiveservices account network-rule add \
  --name my-aoai-resource \
  --resource-group my-rg \
  --ip-address "203.0.113.0/24"

# Allow traffic from a specific VNet subnet
az cognitiveservices account network-rule add \
  --name my-aoai-resource \
  --resource-group my-rg \
  --vnet-name my-vnet \
  --subnet app-subnet

# Set default action to Deny
az cognitiveservices account update \
  --name my-aoai-resource \
  --resource-group my-rg \
  --default-action Deny
```

## Network Architecture Patterns

| Pattern | Use Case | Pros | Cons |
|---|---|---|---|
| Public endpoint + API key | Development | Simple setup | No network isolation |
| Public endpoint + IP allowlist | Internal tools | Easy, no VNet required | Requires static IPs |
| Private endpoint + VNet | Production workloads | Full isolation | Requires DNS config |
| Private endpoint + Azure API Management | Multi-team API gateway | Centralised auth, routing | Added complexity |

## Testing Connectivity

```bash
# From within the VNet, resolve the private endpoint
nslookup my-aoai-resource.openai.azure.com
# Should return a 10.x.x.x or 172.x.x.x private IP

# Test from inside the VNet
curl -s \
  "https://my-aoai-resource.openai.azure.com/openai/deployments?api-version=2024-02-01" \
  -H "api-key: $AZURE_OPENAI_API_KEY" | jq '.data[].id'

# From outside the VNet (should fail with private endpoint + public disabled)
curl -v "https://my-aoai-resource.openai.azure.com/openai/models?api-version=2024-02-01" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
# Expected: connection refused or 403 PublicAccessDisabled
```

## Outbound Connectivity for App Services

When deploying applications on Azure App Service or Azure Functions, use VNet Integration to route outbound calls through the VNet:

```bash
az webapp vnet-integration add \
  --name my-app \
  --resource-group my-rg \
  --vnet my-vnet \
  --subnet app-subnet
```

Ensure the subnet has `Microsoft.CognitiveServices` service endpoint enabled if using service endpoints instead of private endpoints.
