---
tags:
  - azure
  - troubleshooting
search:
  boost: 1.5
description: "Azure common issues — VM connectivity failures, NSG rule analysis, effective route troubleshooting, Azure Firewall and NVA blocks, DNS resolution errors..."
---
# Azure — Common Issues

<div class="kb-summary">
Azure common issues — VM connectivity failures, NSG rule analysis, effective route troubleshooting, Azure Firewall and NVA blocks, DNS resolution errors, and VM provisioning failures. Includes connectivity triage flowchart and CLI diagnostic commands.

*Applies to: Azure*
</div>

> Known failure modes, symptoms, causes, and fixes.

See also: [Troubleshooting](../index.md) for full diagnostic procedures.

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
azure_connectivity_triage: "Azure Connectivity Triage" {shape: rectangle}
vm_connectivity_issues: "VM Connectivity Issues" {shape: rectangle}
nsg_troubleshooting: "NSG Troubleshooting" {shape: rectangle}
azure_ad_authentication_errors: "Azure AD Authentication Errors" {shape: rectangle}
azure_storage_access_denied: "Azure Storage Access Denied" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> azure_connectivity_triage: investigate
symptom -> vm_connectivity_issues: investigate
symptom -> nsg_troubleshooting: investigate
symptom -> azure_ad_authentication_errors: investigate
symptom -> azure_storage_access_denied: investigate
diagnostic_flow -> resolution
azure_connectivity_triage -> resolution
vm_connectivity_issues -> resolution
nsg_troubleshooting -> resolution
azure_ad_authentication_errors -> resolution
azure_storage_access_denied -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "VM Connectivity Issues" {shape: rectangle}
D2: "D2" {shape: rectangle}
R2: "Azure Storage Access Denied" {shape: rectangle}
D3: "D3" {shape: rectangle}
R3: "AKS Pod Not Starting" {shape: rectangle}
D4: "D4" {shape: rectangle}
R4: "NSG Troubleshooting" {shape: rectangle}
D5: "D5" {shape: rectangle}
R5: "App Service 502/503" {shape: rectangle}
R6: "Azure AD Authentication Errors" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}

D1 -> R1
D2 -> R2
D3 -> R3
D4 -> R4
D5 -> R5
R1 -> R6
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Azure Connectivity Triage

```d2
direction: right

connFail: "VM / Resource connectivity failure" {shape: rectangle}
vmState: "vmState" {shape: rectangle}
dnsCheck: "dnsCheck" {shape: rectangle}
resolved: "Issue identified\nand resolved" {shape: rectangle}
nsgCheck: "nsgCheck" {shape: rectangle}
routeCheck: "routeCheck" {shape: rectangle}
fwCheck: "fwCheck" {shape: rectangle}

connFail -> vmState
dnsCheck -> resolved
```

## VM Connectivity Issues

```bash
# 1. Check effective NSG rules on the NIC
az network nic show-effective-nsg --name <nic-name> -g <rg> | \
    jq '.effectiveNetworkSecurityGroups[].effectiveSecurityRules[] | select(.access=="Deny")'

# 2. Check effective routes on the NIC
az network nic show-effective-route-table --name <nic-name> -g <rg>

# 3. Use Network Watcher to test connectivity
az network watcher test-connectivity \
    --source-resource <source-vm-id> \
    --dest-address <destination-ip> --dest-port 443

# 4. Packet capture on NIC
az network watcher packet-capture create \
    --vm <vm-name> -g <rg> --name my-capture --storage-account <sa>
```


```text title="Expected output"
{
  "name": "DenyAllOutbound",
  "description": "Deny all outbound traffic",
  "protocol": "*",
  "sourcePortRange": "*",
  "destinationPortRange": "*",
  "sourceAddressPrefix": "*",
  "destinationAddressPrefix": "*",
  "access": "Deny",
  "priority": 100,
  "direction": "Outbound"
}
{
  "name": "DenyHTTPS",
  "protocol": "Tcp",
  "destinationPortRange": "443",
  "access": "Deny",
  "priority": 200
}

Name                 State      AddressPrefix    NextHopType      NextHopIpAddress
-------------------  ---------  ---------------  ---------------  ------------------
default              Active     0.0.0.0/0        VirtualNetworkGateway  10.0.0.1
RouteToOnPrem        Active     192.168.0.0/16   VirtualNetworkGateway  10.0.0.1
InternetRoute        Active     0.0.0.0/0        Internet         
UDR-AppSubnet        Active     10.1.0.0/24      VirtualAppliance 10.0.1.4

Connectivity Status: Unreachable
Avg Latency (ms): N/A
Hops: [{"type": "Source", "id": "/subscriptions/.../vm-prod-01", "resourceId": "/subscriptions/.../vm-prod-01", "previousHopType": "VirtualMachine", "issues": []}]
Hops: [{"type": "Destination", "address": "203.0.113.45", "resourceId": "Unknown", "issues": [{"origin": "Outbound", "severity": "Error", "type": "NetworkSecurityRule", "context": ["DenyAllOutbound"]}]}]

Packet capture created successfully.
Name: my-capture
Status: NotStarted
CaptureStartTime: 2024-01-15T10:32:45.123456+00:00
StorageLocation: {
  "storageId": "/subscriptions/abc123/resourceGroups/rg-prod/providers/Microsoft.Storage/storageAccounts/saprodlogs",
  "storagePath": "https://saprodlogs.blob.core.windows.net/network-captures/my-capture.cap"
}
```

!!! warning "Common errors"
    **`The resource with name '<nic-name>' does not exist in the resource group '<rg>'`** — Verify the NIC name and resource group name match exactly using `az network nic list -g <rg>`.
    **`(ResourceNotFound) Resource not found`** — Ensure the Network Watcher extension is enabled in the region and the source VM exists with `az network watcher list -g <rg>`.
    **`The storage account '<sa>' does not exist or you do not have access to it`** — Confirm the storage account name is correct and your account has Contributor role on it using `az storage account show -n <sa> -g <rg>`.
Common causes:
- NSG deny rule at NIC level (NIC NSG takes precedence over Subnet NSG)
- User-defined route sending traffic to wrong next hop
- Azure Firewall blocking traffic between hub and spoke
- Service endpoint not configured on subnet (for PaaS services)

## NSG Troubleshooting

```bash
# Check if traffic is allowed by NSG
az network watcher check-nsg-flow --direction Inbound \
    --protocol TCP --local 10.0.0.4 --local-port 443 \
    --remote 10.1.0.10 --remote-port 52000 \
    --nsg <nsg-id>
# Output: access = Allow or Deny, with matching rule name

# View NSG flow logs (query Log Analytics)
# Workspace → Logs:
AzureNetworkAnalytics_CL
| where SubType_s == "FlowLog"
| where FlowStatus_s == "D"   // Denied flows
| where DestIP_s == "<target-ip>"
| project TimeGenerated, SrcIP_s, DestIP_s, DestPort_d, NSGName_s, NSGRule_s
```


```text title="Expected output"
{
  "access": "Deny",
  "evaluatedRules": [
    {
      "name": "DenyAllInbound",
      "direction": "Inbound",
      "access": "Deny",
      "priority": 100,
      "sourceAddressPrefix": "*",
      "destinationAddressPrefix": "*",
      "destinationPortRange": "*"
    }
  ]
}

TimeGenerated                 SrcIP_s      DestIP_s     DestPort_d  NSGName_s           NSGRule_s
2024-01-15T14:32:18.456Z     10.1.0.10    10.0.0.4     443         prod-nsg-eastus     DenyAllInbound
2024-01-15T14:32:19.123Z     10.1.0.10    10.0.0.4     443         prod-nsg-eastus     DenyAllInbound
2024-01-15T14:32:20.789Z     10.1.0.10    10.0.0.4     443         prod-nsg-eastus     DenyAllInbound
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Network/networkSecurityGroups/<nsg-id>' under resource group '<rg>' was not found.`** — Verify the NSG ID is correct and exists in the target resource group with `az network nsg list -g <resource-group>`.
    **`AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Network/networkWatchers/checkIPFlow/action'.`** — Ensure your Azure account has Network Contributor or higher role assigned to the subscription or resource group.
## Azure AD Authentication Errors

```bash
# Check token issuance via Entra ID sign-in logs
az monitor activity-log list --correlation-id <correlation-id>

# Via Entra ID portal: Monitor → Sign-in logs → filter by app/user
# Look for: failure reason, conditional access policy that blocked sign-in

# Check service principal credential expiry
az ad sp credential list --id <sp-object-id>

# If federated credential issue (OIDC):
az ad app federated-credential list --id <app-id>
```


```text title="Expected output"
[
  {
    "correlationId": "a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p",
    "eventName": {
      "value": "Sign-in activity",
      "localizedValue": "Sign-in activity"
    },
    "eventTimestamp": "2024-01-15T14:32:18.456789Z",
    "status": {
      "value": "Failure",
      "localizedValue": "Failure"
    },
    "subStatus": {
      "value": "50058",
      "localizedValue": "Silent sign-out requested"
    },
    "resourceId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg"
  }
]

[
  {
    "customKeyIdentifier": "MjAxOS0wNy0xNQ==",
    "displayName": "sp-prod-cert",
    "endDateTime": "2024-02-10T09:15:00Z",
    "keyId": "a7f8b9c0-d1e2-4f3g-5h6i-7j8k9l0m1n2o",
    "startDateTime": "2023-02-10T09:15:00Z",
    "type": "AsymmetricX509Cert",
    "usage": "Sign"
  }
]

[
  {
    "audiences": [
      "api://prod-app-id"
    ],
    "description": "GitHub Actions OIDC",
    "id": "c5d6e7f8-9a0b-1c2d-3e4f-5g6h7i8j9k0l",
    "issuer": "https://token.actions.githubusercontent.com",
    "name": "github-actions-prod",
    "subject": "repo:myorg/myrepo:ref:refs/heads/main"
  }
]
```

!!! warning "Common errors"
    **`The provided object id '<sp-object-id>' does not refer to a valid service principal object.`** — Verify the service principal object ID with `az ad sp list --filter "displayName eq 'your-sp-name'"` and use the correct `id` field.
    **`Federated credential not found for the given application.`** — Confirm the app ID is correct and that federated credentials have been configured; if none exist, create one with `az ad app federated-credential create`.
    **`Authorization_RequestDenied: Insufficient privileges to complete the operation.`** — Ensure your Azure CLI session has the `Application.ReadWrite.All` or `Directory.ReadWrite.All` permission in Entra ID.
Common causes:
- Conditional Access policy blocking (no MFA, non-compliant device, suspicious location)
- Service principal client secret expired
- Missing API permission or admin consent not granted

## Azure Storage Access Denied

```bash
# Check storage firewall rules
az storage account show -n <storage-account> --query 'networkRuleSet'

# Check role assignments on storage account
az role assignment list --scope <storage-account-resource-id>

# Test access via SAS token
az storage blob download --account-name <sa> --container-name <container> \
    --name <blob> --file /tmp/test --sas-token "<sas>"

# Check if data plane access uses Entra ID or key-based auth
# Key-based access can be disabled in Shared Key authorization:
az storage account show -n <sa> --query 'allowSharedKeyAccess'
```


```text title="Expected output"
{
  "bypass": "AzureServices",
  "defaultAction": "Deny",
  "virtualNetworkRules": [
    {
      "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodsa/virtualNetworkRules/vnet-rule-1",
      "action": "Allow"
    }
  ],
  "ipRules": [
    {
      "value": "203.0.113.45",
      "action": "Allow"
    }
  ]
}
[
  {
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/prod-rg/providers/roleAssignments/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "roleDefinitionName": "Storage Blob Data Contributor",
    "principalName": "user@contoso.com",
    "scope": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodsa"
  }
]
Finished[#############################################] 100.0000%
Downloaded blob to /tmp/test
true
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Storage/storageAccounts/<storage-account>' under resource group '<rg>' was not found.`** — Verify the storage account name and resource group are correct, and that you are querying the correct subscription.
    **`AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Storage/storageAccounts/read' over scope '<scope>'.`** — Ensure your user or service principal has at least Reader role on the storage account or its resource group.
    **`InvalidAuthenticationTokenTenant: The access token is from the wrong tenant.`** — Run `az account set --subscription <subscription-id>` to switch to the correct subscription context.
## AKS Pod Not Starting

```bash
# Get pod description and events
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# Check node resource pressure
kubectl describe node <node-name> | grep -A 5 "Conditions:"
kubectl top nodes

# Image pull error
kubectl get events -n <namespace> | grep "Failed to pull"
# Check Azure Container Registry firewall if using private ACR:
az acr show --name <acr-name> --query 'networkRuleSet'

# DNS resolution in pod (network policy blocking?)
kubectl run test-pod --rm -i --image=busybox -- nslookup kubernetes.default
```


```text title="Expected output"
Name:         app-deployment-5d8f7c9b2-kx4m9
Namespace:    production
Priority:    0
Node:        aks-nodepool-12345678-vmss000001/10.224.0.5
Start Time:   Thu, 14 Nov 2024 09:32:15 +0000
Labels:       app=myapp,version=v1.2.3
Status:       Running
Events:
  Type     Reason                 Age    From               Message
  ----     ------                 ----   ----               -------
  Normal   Scheduled              5m12s  default-scheduler  Successfully assigned production/app-deployment-5d8f7c9b2-kx4m9 to aks-nodepool-12345678-vmss000001
  Normal   Pulling                5m10s  kubelet            Pulling image "myacr.azurecr.io/myapp:v1.2.3"
  Normal   Pulled                 4m58s  kubelet            Successfully pulled image "myacr.azurecr.io/myapp:v1.2.3"
  Normal   Created                4m57s  kubelet            Created container app
  Normal   Started                4m56s  kubelet            Started container app

LAST SEEN   TYPE     REASON                    OBJECT                                MESSAGE
4m12s       Normal   Scheduled                 pod/app-deployment-5d8f7c9b2-kx4m9   Successfully assigned production/app-deployment-5d8f7c9b2-kx4m9 to aks-nodepool-12345678-vmss000001
3m58s       Normal   Pulled                    pod/app-deployment-5d8f7c9b2-kx4m9   Successfully pulled image "myacr.azurecr.io/myapp:v1.2.3" in 12.234s
3m57s       Normal   Created                   pod/app-deployment-5d8f7c9b2-kx4m9   Created container app
3m56s       Normal   Started                   pod/app-deployment-5d8f7c9b2-kx4m9   Started container app
2m30s       Warning  BackOff                   pod/test-pod-xyz123                   Back-off restarting failed container

Conditions:
  Type                 Status  LastHeartbeatTime         LastTransitionTime        Reason                       Message
  ----                 ------  -----------------         ------------------        ------                       -------
  Ready                True    Thu, 14 Nov 2024 10:15:22 +0000  Thu, 14 Nov 2024 09:28:01 +0000  KubeletReady            kubelet is posting ready status
  MemoryPressure       False   Thu, 14 Nov 2024 10:15:22 +0000  Thu, 14 Nov 2024 09:28:01 +0000  KubeletHasSufficientMemory  kubelet has sufficient memory available
  DiskPressure         False   Thu, 14 Nov 2024 10:15:22 +0000  Thu, 14 Nov 2024 09:28:01 +0000  KubeletH
```
## App Service 502/503

1. Azure Portal → App Service → Diagnose and solve problems → Availability and Performance
2. Check App Service Plan metrics: CPU %, Memory % (Metrics blade)
3. Review application logs: App Service → App Service Logs → enable File System logging
4. Check health probe configuration: App Service → Health Check — confirm probe returning 200

```bash
# Check App Service Plan scale out status
az appservice plan show --name <plan-name> -g <rg> \
    --query 'properties.numberOfWorkers'

# Manual scale up (if throttled)
az appservice plan update --name <plan-name> -g <rg> --sku P2V3
```


```text title="Expected output"
2
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Web/serverfarms/<plan-name>' under resource group '<rg>' was not found.`** — Verify the App Service Plan name and resource group name are correct with `az appservice plan list -g <rg>`.
    **`AuthorizationFailed : The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Web/serverfarms/write' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Web/serverfarms/<plan-name>'.`** — Ensure your Azure account has Contributor or App Service Plan Contributor role on the resource group.
---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Azure — Diagnostics](../diagnostics/)
- [Azure — Escalation](../escalation/)
- [Azure — Health Checks](../../operations/health-checks/)
