---
tags:
  - azure
  - troubleshooting
search:
  boost: 1.5
description: "Troubleshooting reference covering NSG Troubleshooting, Azure AD Authentication Errors, Azure Storage Access Denied, AKS Pod Not Starting, App Service..."
---
# Azure — Troubleshooting

<div class="kb-summary">
Troubleshooting reference covering NSG Troubleshooting, Azure AD Authentication Errors, Azure Storage Access Denied, AKS Pod Not Starting, App Service 502/503.

*Applies to: Azure*
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known problems, symptoms, and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to Microsoft Support with the right data.</span>
</a>

</div>

Common causes:
- Conditional Access policy blocking (no MFA, non-compliant device, suspicious location)
- Service principal client secret expired
- Missing API permission or admin consent not granted

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
azure_storage_access_denied: "Azure Storage Access Denied" {shape: rectangle}
aks_pod_not_starting: "AKS Pod Not Starting" {shape: rectangle}
app_service_502503: "App Service 502/503" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> azure_storage_access_denied: investigate
symptom -> aks_pod_not_starting: investigate
symptom -> app_service_502503: investigate
azure_storage_access_denied -> resolution
aks_pod_not_starting -> resolution
app_service_502503 -> resolution
```

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
  "ipRules": [
    {
      "action": "Allow",
      "value": "203.0.113.45"
    }
  ],
  "virtualNetworkRules": [
    {
      "action": "Allow",
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Network/virtualNetworks/prod-vnet/subnets/app-subnet"
    }
  ]
}
[
  {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Authorization/roleAssignments/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "principalId": "98765432-0987-6543-2109-876543210987",
    "roleDefinitionId": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/roleDefinitions/2a2b9908-6ea1-4ae2-8e65-a410df84e7d1",
    "roleDefinitionName": "Storage Blob Data Contributor",
    "scope": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstg001"
  }
]
Finished[#############################################] 100.0000%
Downloaded blob to /tmp/test
true
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `AuthorizationPermissionMismatch: The user, group or application does not have the correct permissions to access the storage account.` | Verify the user or service principal has a Storage Blob Data Reader or Contributor role assigned at the storage account scope. |
    | `InvalidSasToken: The provided SAS token is invalid or has expired.` | Regenerate the SAS token with a future expiration time and ensure it includes the required permissions (read, list, etc.). |
    | `StorageAccountNotFound: The storage account '<storage-account>' was not found within the specified resource group.` | Verify the storage account name is correct and exists in the current subscription and resource group. |
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
Name:         nginx-deployment-5d59d4b4f6-7kx2m
Namespace:    default
Priority:     0
Node:         aks-nodepool1-12345678-vmss000001/10.224.0.4
Start Time:   Thu, 15 Feb 2024 14:32:18 +0000
Labels:       app=nginx,pod-template-hash=5d59d4b4f6
Status:       Running
Events:
  Type    Reason     Age   From               Message
  ----    ------     ---   ----               -------
  Normal  Scheduled  5m    default-scheduler  Successfully assigned default/nginx-deployment-5d59d4b4f6-7kx2m to aks-nodepool1-12345678-vmss000001

LAST SEEN   TYPE     REASON              OBJECT                                    MESSAGE
2m18s       Normal   Pulling             pod/nginx-deployment-5d59d4b4f6-7kx2m     Pulling image "nginx:1.21"
2m10s       Normal   Pulled              pod/nginx-deployment-5d59d4b4f6-7kx2m     Successfully pulled image "nginx:1.21" in 8.2s
2m8s        Normal   Created             pod/nginx-deployment-5d59d4b4f6-7kx2m     Created container nginx
2m7s        Normal   Started             pod/nginx-deployment-5d59d4b4f6-7kx2m     Started container nginx

Conditions:
  Type                 Status  LastHeartbeatTime         LastTransitionTime        Reason                       Message
  ----                 ------  -----------------         ------------------        ------                       -------
  Ready                True    Thu, 15 Feb 2024 15:12:33 +0000   Thu, 15 Feb 2024 14:28:10 +0000   KubeletReady            kubelet is posting ready status
  MemoryPressure       False   Thu, 15 Feb 2024 15:12:33 +0000   Thu, 15 Feb 2024 14:28:10 +0000   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         False   Thu, 15 Feb 2024 15:12:33 +0000   Thu, 15 Feb 2024 14:28:10 +0000   KubeletHasNoDiskPressure    kubelet has no disk pressure

NAME                                    CPU(cores)   MEMORY(Mi)
aks-nodepool1-12345678-vmss000001       487m         2156Mi
aks-nodepool1-12345678-vmss000002       312m         1847Mi

{
  "defaultAction": "Allow",
  "virtualNetworkRules": [],
  "ipRules": []
}

pod/test-pod created
Server:    10.0.0.10
Address:   10.0.0.10:53

Name:      kubernetes.default
Address:   10.0.0.1

pod "test-pod" deleted
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "pod" (get pods)` | Verify |
**Expected output:** Node conditions show `Ready True`. `kubectl top nodes` shows CPU and memory below 80%. DNS test returns an address for `kubernetes.default`. Events show `Pulled` and `Started` rather than `BackOff` or `ErrImagePull`.

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
    | Error | Fix |
    |---|---|
    | `ResourceNotFound : The Resource 'Microsoft.Web/serverfarms/<plan-name>' under resource group '<rg>' was not found.` | Verify the plan name and resource group name are correct with `az appservice plan list -g <rg>`. |
    | `AuthorizationFailed : The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Web/serverfarms/write' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Web/serverfarms/<plan-name>'.` | Ensure your Azure account has Contributor or higher role on the resource group using `az role assignment list -g <rg>`. |