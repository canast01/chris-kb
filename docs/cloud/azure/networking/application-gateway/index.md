---
tags:
  - azure
  - networking
---
# Application Gateway

<div class="kb-summary">
Azure Application Gateway is a Layer 7 load balancer that provides SSL termination, URL-based routing, Web Application Firewall (WAF), and autoscaling. It operates at the application layer and is the preferred entry point for HTTP/HTTPS workloads.

*Applies to: Azure*
</div>

## Application Gateway Traffic Flow

```d2
direction: right

client: "Internet Client\nHTTP / HTTPS" {shape: rectangle}
pip: "Public IP\nStatic · Standard SKU" {shape: rectangle}
waf: "WAF Policy\nOWASP rules · custom rules" {shape: rectangle}
listener: "Listener\nHTTP :80 · HTTPS :443" {shape: rectangle}
routing: "Routing Rules\nURL path · host header" {shape: rectangle}
backendPool: "Backend Pool\nVMs · VMSS · AKS · App Service" {shape: rectangle}
healthProbe: "Health Probe\nHTTP · HTTPS · custom" {shape: rectangle}

client -> pip
pip -> waf
waf -> listener
listener -> routing
routing -> backendPool
healthProbe -> backendPool
```

## Creating an Application Gateway

```bash
# Create a public IP for the Application Gateway
az network public-ip create \
  --resource-group myRG \
  --name appgw-pip \
  --sku Standard \
  --allocation-method Static

# Create the Application Gateway (WAF_v2 SKU)
az network application-gateway create \
  --name myAppGW \
  --resource-group myRG \
  --location eastus \
  --sku WAF_v2 \
  --capacity 2 \
  --vnet-name myVNet \
  --subnet appgw-subnet \
  --public-ip-address appgw-pip \
  --frontend-port 443 \
  --http-settings-port 80 \
  --http-settings-protocol Http \
  --routing-rule-type Basic \
  --priority 100
```


```text title="Expected output"
{
  "publicIp": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/publicIPAddresses/appgw-pip",
    "name": "appgw-pip",
    "publicIpAddress": "203.0.113.42",
    "resourceGroup": "myRG",
    "sku": {
      "name": "Standard"
    }
  }
}
{
  "applicationGateway": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW",
    "name": "myAppGW",
    "location": "eastus",
    "provisioningState": "Succeeded",
    "sku": {
      "name": "WAF_v2",
      "capacity": 2
    },
    "frontendIpConfigurations": [
      {
        "name": "appGatewayFrontendIP",
        "publicIpAddress": "203.0.113.42"
      }
    ]
  }
}
```

!!! warning "Common errors"
    **`The subnet 'appgw-subnet' does not exist in virtual network 'myVNet'.`** — Create the subnet first using `az network vnet subnet create --resource-group myRG --vnet-name myVNet --name appgw-subnet --address-prefix 10.0.1.0/24` before creating the gateway.
    **`The public IP address 'appgw-pip' does not exist in resource group 'myRG'.`** — Ensure the public IP creation command completes successfully and the resource group name matches exactly in both commands.
    **`Deployment failed with code: InvalidResourceReference. Message: The referenced resource '/subscriptions/.../publicIPAddresses/appgw-pip' could not be found.`** — Wait 10–15 seconds after public IP creation before creating the Application Gateway to allow replication across Azure regions.
## WAF Mode Configuration

WAF can run in Detection mode (log only) or Prevention mode (block and log). Start with Detection and switch to Prevention after validating no false positives.

```bash
# Enable WAF in Prevention mode
az network application-gateway waf-config set \
  --gateway-name myAppGW \
  --resource-group myRG \
  --enabled true \
  --firewall-mode Prevention \
  --rule-set-type OWASP \
  --rule-set-version 3.2

# Check current WAF config
az network application-gateway waf-config show \
  --gateway-name myAppGW \
  --resource-group myRG \
  --output json
```


```text title="Expected output"
{
  "disabledRuleGroups": [],
  "enabled": true,
  "fileUploadLimitMb": 100,
  "firewallMode": "Prevention",
  "requestBodyCheck": true,
  "requestBodyInspectLimitInKB": 128,
  "ruleSetType": "OWASP",
  "ruleSetVersion": "3.2",
  "state": "Enabled",
  "exclusions": []
}
```

!!! warning "Common errors"
    **`The resource 'Microsoft.Network/applicationGateways/myAppGW' under resource group 'myRG' was not found.`** — Verify the application gateway name and resource group exist using `az network application-gateway list --resource-group myRG`.
    **`The WAF policy version '3.2' is not supported for rule set type 'OWASP'.`** — Check available versions with `az network application-gateway waf-config list-available-rule-sets` and use a supported version like 3.1 or 3.0.
## Listener Configuration

Listeners define the frontend IP, port, and protocol. Multi-site listeners use host headers to route to different backends.

```bash
# Add an HTTPS listener with SSL certificate
az network application-gateway ssl-cert create \
  --gateway-name myAppGW \
  --resource-group myRG \
  --name mySSLCert \
  --cert-file cert.pfx \
  --cert-password "P@ssword123"

az network application-gateway http-listener create \
  --gateway-name myAppGW \
  --resource-group myRG \
  --name https-listener \
  --frontend-ip appGatewayFrontendIP \
  --frontend-port 443 \
  --ssl-cert mySSLCert
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b5c-d6e7-8f9a-0b1c-2d3e4f5a6b7c/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/sslCertificates/mySSLCert",
  "name": "mySSLCert",
  "etag": "W/\"a1b2c3d4-e5f6-7890-abcd-ef1234567890\"",
  "type": "Microsoft.Network/applicationGateways/sslCertificates",
  "properties": {
    "provisioningState": "Succeeded",
    "publicCertData": "MIIDXTCCAkWgAwIBAgIJAKZ..."
  }
}
{
  "id": "/subscriptions/12a34b5c-d6e7-8f9a-0b1c-2d3e4f5a6b7c/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/httpListeners/https-listener",
  "name": "https-listener",
  "etag": "W/\"f7e6d5c4-b3a2-1098-7654-321fedcba987\"",
  "type": "Microsoft.Network/applicationGateways/httpListeners",
  "properties": {
    "provisioningState": "Succeeded",
    "frontendIPConfiguration": {
      "id": "/subscriptions/12a34b5c-d6e7-8f9a-0b1c-2d3e4f5a6b7c/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/frontendIPConfigurations/appGatewayFrontendIP"
    },
    "frontendPort": {
      "id": "/subscriptions/12a34b5c-d6e7-8f9a-0b1c-2d3e4f5a6b7c/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/frontendPorts/port_443"
    },
    "protocol": "Https",
    "sslCertificate": {
      "id": "/subscriptions/12a34b5c-d6e7-8f9a-0b1c-2d3e4f5a6b7c/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/sslCertificates/mySSLCert"
    }
  }
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/applicationGateways/myAppGW' under resource group 'myRG' was not found.`** — Verify the application gateway name and resource group exist using `az network application-gateway list --resource-group myRG`.
    **`(InvalidArgument) The certificate file 'cert.pfx' does not exist or is not readable.`** — Ensure the PFX certificate file is in the current working directory and readable with `ls -la cert.pfx`.
    **`(BadRequest)
## Backend Pools and Health Probes

```bash
# Add a backend pool
az network application-gateway address-pool create \
  --gateway-name myAppGW \
  --resource-group myRG \
  --name myBackendPool \
  --servers 10.0.1.4 10.0.1.5

# Create a custom health probe
az network application-gateway probe create \
  --gateway-name myAppGW \
  --resource-group myRG \
  --name myHealthProbe \
  --protocol Http \
  --host-name-from-http-settings true \
  --path /health \
  --interval 30 \
  --timeout 30 \
  --threshold 3

# Create HTTP settings referencing the probe
az network application-gateway http-settings create \
  --gateway-name myAppGW \
  --resource-group myRG \
  --name myHTTPSettings \
  --port 80 \
  --protocol Http \
  --probe myHealthProbe \
  --cookie-based-affinity Disabled
```


```text title="Expected output"
{
  "backendAddresses": [
    {
      "ipAddress": "10.0.1.4"
    },
    {
      "ipAddress": "10.0.1.5"
    }
  ],
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/backendAddressPools/myBackendPool",
  "name": "myBackendPool",
  "provisioningState": "Succeeded",
  "type": "Microsoft.Network/applicationGateways/backendAddressPools"
}
{
  "etag": "W/\"b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7\"",
  "host": null,
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/probes/myHealthProbe",
  "interval": 30,
  "match": null,
  "name": "myHealthProbe",
  "path": "/health",
  "pickHostNameFromBackendHttpSettings": true,
  "port": null,
  "protocol": "Http",
  "provisioningState": "Succeeded",
  "threshold": 3,
  "timeout": 30,
  "type": "Microsoft.Network/applicationGateways/probes"
}
{
  "affinityCookieName": null,
  "authenticationCertificates": [],
  "connectionDraining": {
    "drainTimeoutInSec": 1,
    "enabled": false
  },
  "cookieBasedAffinity": "Disabled",
  "etag": "W/\"c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8\"",
  "hostName": null,
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/httpSettings/myHTTPSettings",
  "name": "myHTTPSettings",
  "port": 80,
  "probe": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/probes/myHealthProbe"
  },
  "protocol": "Http",
  "provisioningState": "Succeeded",
  "requestTimeout": 30,
  "trustedRootCertificates": [],
  "type": "Microsoft.Network/applicationGateways/httpSettings"
}
```

!!! warning "Common errors"
    **`The resource 'Microsoft.Network/applicationGateways/my
## SSL Termination and TLS Policy

```bash
# Set TLS policy to enforce minimum TLS 1.2
az network application-gateway ssl-policy set \
  --gateway-name myAppGW \
  --resource-group myRG \
  --policy-type Predefined \
  --policy-name AppGwSslPolicy20220101

# List available SSL policies
az network application-gateway ssl-policy list-options \
  --output table
```


```text title="Expected output"
(no output — command completes silently)

MinTlsVersion    MaxTlsVersion    CipherSuites
---------------  ---------------  --------------------------------------------------
TLSV1_0          TLSV1_3          TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
TLSV1_1          TLSV1_3          TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
TLSV1_2          TLSV1_3          TLS_DHE_RSA_WITH_AES_128_GCM_SHA256
TLSV1_2          TLSV1_3          TLS_DHE_RSA_WITH_AES_256_GCM_SHA384
TLSV1_2          TLSV1_3          TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
TLSV1_2          TLSV1_3          TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
...
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Network/applicationGateways/myAppGW' under resource group 'myRG' was not found.`** — Verify the application gateway name and resource group exist using `az network application-gateway list -g myRG`.
    **`InvalidPolicyName: Policy name 'AppGwSslPolicy20220101' is not a valid predefined policy.`** — Run `az network application-gateway ssl-policy list-options` to see valid policy names and use an existing one.
## SKU and Capacity Summary

| SKU          | WAF Support | Autoscale | Use Case                       |
|--------------|-------------|-----------|--------------------------------|
| Standard_v2  | No          | Yes       | General HTTP/HTTPS load balancing |
| WAF_v2       | Yes         | Yes       | Internet-facing workloads needing WAF |
| Standard v1  | No          | No        | Legacy, not recommended        |
| WAF v1       | Yes         | No        | Legacy, not recommended        |

```bash
# Show Application Gateway operational state and backend health
az network application-gateway show \
  --name myAppGW \
  --resource-group myRG \
  --output table

az network application-gateway show-backend-health \
  --name myAppGW \
  --resource-group myRG \
  --output json
```


```text title="Expected output"
Name      ResourceGroup    Location    ProvisioningState    OperationalState
--------  ---------------  ----------  -------------------  ------------------
myAppGW   myRG             eastus      Succeeded            Running

{
  "backendAddressPools": [
    {
      "backendHttpSettingsCollection": [
        {
          "servers": [
            {
              "address": "10.0.1.5",
              "health": "Healthy",
              "healthProbeLog": ""
            },
            {
              "address": "10.0.1.6",
              "health": "Healthy",
              "healthProbeLog": ""
            }
          ],
          "backendHttpSettings": "myBackendSettings"
        }
      ],
      "backendAddressPoolName": "myBackendPool"
    }
  ]
}
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Network/applicationGateways/myAppGW' under resource group 'myRG' was not found.`** — Verify the Application Gateway name and resource group name are correct using `az network application-gateway list --resource-group myRG`.
    **`AuthorizationFailed : The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.Network/applicationGateways/read' over scope '/subscriptions/...'.`** — Ensure your Azure account has the Network Contributor or Reader role assigned to the resource group using `az role assignment list --resource-group myRG`.